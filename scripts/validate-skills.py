#!/usr/bin/env python3
# Copyright 2026 Jean-Francois Arcand
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ABOUTME: Validation script for mirroir-skills files (SKILL.md and YAML).
# ABOUTME: Checks required fields, step types, variable syntax, metadata formats, and front matter.

"""
Validate all skill files under apps/, testing/, workflows/, and legacy/.

Supports both SKILL.md (.md) files and legacy YAML (.yaml) files.
Exit 0 if no errors (warnings are OK), exit 1 if any error found.
"""

import os
import re
import sys

# ---------------------------------------------------------------------------
# YAML loading — prefer PyYAML, fall back to a minimal regex-based parser.
# ---------------------------------------------------------------------------

try:
    import yaml

    def load_yaml(path):
        with open(path, "r", encoding="utf-8") as fh:
            return yaml.safe_load(fh)

except ImportError:
    def load_yaml(path):
        """Minimal YAML parser using regex — handles the flat structure of skill files."""
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()

        data = {}
        # Extract top-level scalar fields (name, app, description, ios_min, locale)
        for match in re.finditer(r'^(\w+):\s*(?:"([^"]*)"|(\S.*))\s*$', text, re.MULTILINE):
            key = match.group(1)
            value = match.group(2) if match.group(2) is not None else match.group(3)
            if key == "steps":
                continue
            data[key] = value.strip()

        # Handle block scalar descriptions (> or |)
        block_match = re.search(r'^description:\s*[>|]\s*\n((?:[ \t]+\S.*\n?)+)', text, re.MULTILINE)
        if block_match:
            data["description"] = block_match.group(1).strip()

        # Extract tags list
        tags_match = re.search(r'^tags:\s*\[([^\]]*)\]', text, re.MULTILINE)
        if tags_match:
            raw = tags_match.group(1)
            data["tags"] = [t.strip().strip('"').strip("'") for t in raw.split(",") if t.strip()]

        # Extract steps list
        steps = []
        for step_match in re.finditer(r'^\s+-\s+(\w+):\s*(.*)', text, re.MULTILINE):
            steps.append({step_match.group(1): step_match.group(2).strip().strip('"')})
        if steps:
            data["steps"] = steps

        return data

# ---------------------------------------------------------------------------
# Canonical step types (kept in sync with SKILL.md).
# ---------------------------------------------------------------------------

VALID_STEP_TYPES = {
    "launch",
    "tap",
    "long_press",
    "type",
    "swipe",
    "wait_for",
    "assert_visible",
    "assert_not_visible",
    "screenshot",
    "press_key",
    "press_home",
    "open_url",
    "shake",
    "remember",
    "scroll_to",
    "set_network",
    "reset_app",
    "target",
    "measure",
    "condition",
    "repeat",
}

VALID_CONDITION_TYPES = {"if_visible", "if_not_visible"}
VALID_REPEAT_MODES = {"while_visible", "until_visible", "times"}

REQUIRED_YAML_FIELDS = {"name", "app", "description", "steps"}
REQUIRED_MD_FRONT_MATTER = {"version", "name"}
OPTIONAL_MD_FRONT_MATTER = {
    "app", "ios_min", "locale", "tags", "description",
    # kind:game scene-skill schema, checked by the scene gate below.
    "kind", "surface", "playable", "controls", "budget", "success", "fail",
    "image_width", "decider",
}

# Skill variants a `kind:` header may name. "game" is a model-interpreted scene:
# mirroir-mcp never replays it step by step.
VALID_KINDS = {"game"}

# Surfaces a kind:game skill drives. A shell screen is ordinary UI and is an
# ordinary skill, so only the playfield is a game surface.
VALID_GAME_SURFACES = {"scene"}

# The typed frame/token/time budget every kind:game skill declares, each a
# positive integer: a scene stops at the first limit it reaches.
BUDGET_FIELDS = ("max_frames", "max_tokens", "max_seconds")

# How a scene's success and fail predicates are judged: `visible` is a text the
# frame's OCR reads, so the verdict never rests on the model's opinion. Its value
# is one text or a non-empty list of texts, any of which matches.
PREDICATE_KINDS = ("visible",)

# Front matter only a kind:game skill takes. `image_width` is the width in px a
# frame is resized to before the model reads it; `decider: required` means an
# external move picker (named by the scenario step, never the skill) chooses
# each action while the model only reads the frame.
SCENE_ONLY_FIELDS = ("image_width", "decider")
IMAGE_WIDTH_RANGE = (200, 2000)
VALID_DECIDERS = {"required"}

# A board control's size limits: one column per letter a..z, rows 1..99.
GRID_MAX_COLUMNS = 26
GRID_MAX_ROWS = 99

# The control name a scene action uses to wait one frame without a touch; a
# skill never declares it.
RESERVED_CONTROL = "none"

# The gestures a scene control may make, written in `## Controls` as window
# fractions in [0, 1]:
#   - <control>: tap at X,Y
#   - <control>: drag from X,Y radius R      (the model picks the direction)
#   - <control>: hold at X,Y for <ms>
#   - <control>: grid CxR from X,Y to X,Y    (a board: top-left to bottom-right
#                                             corner; an action taps named cells)
CONTROL_LINE = re.compile(
    r"^-\s*(?P<name>[A-Za-z][A-Za-z0-9_-]*)\s*:\s*(?:"
    r"tap at (?P<tx>[0-9.]+)\s*,\s*(?P<ty>[0-9.]+)"
    r"|drag from (?P<dx>[0-9.]+)\s*,\s*(?P<dy>[0-9.]+) radius (?P<r>[0-9.]+)"
    r"|hold at (?P<hx>[0-9.]+)\s*,\s*(?P<hy>[0-9.]+) for (?P<ms>[0-9]+)"
    r"|grid (?P<cols>[0-9]+)x(?P<rows>[0-9]+)"
    r" from (?P<fx>[0-9.]+)\s*,\s*(?P<fy>[0-9.]+)"
    r" to (?P<gx>[0-9.]+)\s*,\s*(?P<gy>[0-9.]+)"
    r")\s*$")

# Supported `playable` control classes. A value outside this set is rejected,
# which is how a twin-stick / simultaneous-control scene is kept out: it has no
# valid playable value (stock single-touch cannot drive two controls at once).
VALID_PLAYABLE = {"observe-only", "single-control", "pc-controls"}

SEMVER_ISH = re.compile(r"^\d+\.\d+(\.\d+)?$")
LOCALE_CODE = re.compile(r"^[a-z]{2}_[A-Z]{2}$")
VARIABLE_SYNTAX = re.compile(r"\$\{[^}]*\}")
MALFORMED_VARIABLE = re.compile(r"\$\{[^A-Za-z_]|\$\{[^}]*[^A-Za-z0-9_:}./-]")

# ---------------------------------------------------------------------------
# Directories to scan for each file type.
# ---------------------------------------------------------------------------

# Skill directories: new structure (skills/*) and legacy top-level directories.
# Files named APP.md are patterns, not skills — skipped by find_md_files.
MD_SKILL_DIRS = [
    "skills/apps", "skills/testing", "skills/workflows", "skills/ci",
    "apps", "testing", "workflows", "ci",
    # archetype reference docs and game scene skills — previously unvalidated.
    "archetypes",
]
YAML_SKILL_DIRS = ["legacy"]

# ---------------------------------------------------------------------------
# File discovery.
# ---------------------------------------------------------------------------


def find_md_files(root):
    """Walk MD_SKILL_DIRS and yield paths to .md files (skipping APP.md patterns)."""
    seen = set()
    for dirname in MD_SKILL_DIRS:
        dirpath = os.path.join(root, dirname)
        if not os.path.isdir(dirpath):
            continue
        for dirpath_walk, _, filenames in os.walk(dirpath):
            for fname in sorted(filenames):
                if not fname.endswith(".md"):
                    continue
                # APP.md files are app patterns, not skills — skip
                if fname.upper() == "APP.MD":
                    continue
                full = os.path.join(dirpath_walk, fname)
                if full not in seen:
                    seen.add(full)
                    yield full


def find_yaml_files(root):
    """Walk YAML_SKILL_DIRS and yield paths to .yaml files."""
    for dirname in YAML_SKILL_DIRS:
        dirpath = os.path.join(root, dirname)
        if not os.path.isdir(dirpath):
            continue
        for dirpath_walk, _, filenames in os.walk(dirpath):
            for fname in sorted(filenames):
                if fname.endswith(".yaml"):
                    yield os.path.join(dirpath_walk, fname)


# ---------------------------------------------------------------------------
# SKILL.md front matter parsing.
# ---------------------------------------------------------------------------


def split_unquoted(text, separator):
    """Split `text` on `separator` wherever it is outside double or single quotes
    and outside `[...]` brackets."""
    parts, current, quote, depth = [], "", None, 0
    for char in text:
        if quote:
            if char == quote:
                quote = None
        elif char in "\"'":
            quote = char
        elif char == "[":
            depth += 1
        elif char == "]":
            depth = max(0, depth - 1)
        elif char == separator and depth == 0:
            parts.append(current)
            current = ""
            continue
        current += char
    parts.append(current)
    return parts


def unquote(raw):
    """`raw` stripped of whitespace and one pair of surrounding quotes."""
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        return raw[1:-1]
    return raw


def parse_inline_map(value):
    """Parse an inline `{ key: value, ... }` map into a dict, or return None when
    the braces do not close or an entry has no `key: value`. A comma or colon
    inside a quoted value is part of the value, and the quotes around a value
    are stripped. A `[a, "b"]` value becomes a list of strings; an unclosed
    one stays a string."""
    if not value.endswith("}"):
        return None
    entries = {}
    for entry in split_unquoted(value[1:-1], ","):
        if not entry.strip():
            continue
        if ":" not in entry:
            return None
        key, raw = entry.split(":", 1)
        raw = raw.strip()
        if raw.startswith("[") and raw.endswith("]"):
            entries[key.strip()] = [
                unquote(item) for item in split_unquoted(raw[1:-1], ",") if item.strip()]
        else:
            entries[key.strip()] = unquote(raw)
    return entries


def markdown_section(body, heading):
    """The text under `## <heading>` in `body`, up to the next `## `, or None."""
    match = re.search(
        r"^##\s+" + re.escape(heading) + r"\s*$(?P<text>.*?)(?=^##\s|\Z)",
        body, re.MULTILINE | re.DOTALL)
    return match.group("text") if match else None


def validate_predicate(front_matter, field, rel):
    """Errors for a scene predicate: one `{ visible: "<text>" }` map, whose value
    may also be a non-empty list of texts (`visible: ["Vaincu", "Rejouer"]`)."""
    predicate = front_matter.get(field)
    if not isinstance(predicate, dict) or len(predicate) != 1:
        return [f"  ERROR  {rel}: {field} must be one predicate, e.g. "
                f"{field}: {{ visible: \"VICTOIRE\" }}"]
    (kind, text), = predicate.items()
    if kind not in PREDICATE_KINDS:
        return [f"  ERROR  {rel}: {field} predicate '{kind}' is not one of "
                f"{', '.join(PREDICATE_KINDS)}"]
    if isinstance(text, list):
        if not text:
            return [f"  ERROR  {rel}: {field} predicate {kind} lists no text"]
        if not all(text):
            return [f"  ERROR  {rel}: {field} predicate {kind} lists an empty text"]
        return []
    if not text:
        return [f"  ERROR  {rel}: {field} predicate {kind} names no text"]
    return []


def validate_scene_options(front_matter, rel):
    """Errors for a kind:game skill's optional `image_width` (an integer in
    IMAGE_WIDTH_RANGE) and `decider` (only `required`)."""
    errors = []
    low, high = IMAGE_WIDTH_RANGE
    width = front_matter.get("image_width")
    if width is not None and (not width.isdigit() or not low <= int(width) <= high):
        errors.append(
            f"  ERROR  {rel}: image_width must be an integer in [{low}, {high}] "
            f"(got {width!r})")
    decider = front_matter.get("decider")
    if decider is not None and decider not in VALID_DECIDERS:
        errors.append(
            f"  ERROR  {rel}: decider must be one of {', '.join(sorted(VALID_DECIDERS))} "
            f"(got {decider!r}); the move picker itself is named by the scenario step")
    return errors


def validate_grid_control(match, name, rel):
    """Errors for a `grid CxR from X,Y to X,Y` control: a size within
    GRID_MAX_COLUMNS x GRID_MAX_ROWS and a bottom-right corner past the top-left."""
    errors = []
    cols, rows = int(match.group("cols")), int(match.group("rows"))
    if not 1 <= cols <= GRID_MAX_COLUMNS:
        errors.append(
            f"  ERROR  {rel}: control '{name}' grid has {cols} columns "
            f"(1..{GRID_MAX_COLUMNS})")
    if not 1 <= rows <= GRID_MAX_ROWS:
        errors.append(
            f"  ERROR  {rel}: control '{name}' grid has {rows} rows (1..{GRID_MAX_ROWS})")
    if float(match.group("gx")) <= float(match.group("fx")) or \
            float(match.group("gy")) <= float(match.group("fy")):
        errors.append(
            f"  ERROR  {rel}: control '{name}' grid must run from its top-left "
            f"corner to its bottom-right one (to > from on both axes)")
    return errors


def validate_controls_section(body, controls, rel):
    """Errors for `## Controls`: one calibrated gesture per declared control,
    every coordinate a window fraction in [0, 1]."""
    section = markdown_section(body, "Controls")
    if section is None:
        return [f"  ERROR  {rel}: a scene needs a ## Controls section calibrating "
                f"each control (e.g. '- fire: tap at 0.85,0.72')"]
    errors, calibrated = [], []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("-"):
            continue
        match = CONTROL_LINE.match(line)
        if not match:
            errors.append(
                f"  ERROR  {rel}: control line '{line}' is not 'tap at X,Y', "
                f"'drag from X,Y radius R', 'hold at X,Y for MS' or "
                f"'grid CxR from X,Y to X,Y'")
            continue
        name = match.group("name")
        calibrated.append(name)
        if match.group("cols") is not None:
            errors.extend(validate_grid_control(match, name, rel))
        for coord in ("tx", "ty", "dx", "dy", "hx", "hy", "r", "fx", "fy", "gx", "gy"):
            raw = match.group(coord)
            if raw is not None and not (0.0 <= float(raw) <= 1.0):
                errors.append(
                    f"  ERROR  {rel}: control '{name}' coordinate {raw} is not a "
                    f"window fraction in [0, 1]")
        if match.group("r") is not None and float(match.group("r")) == 0.0:
            errors.append(f"  ERROR  {rel}: control '{name}' drags a radius of 0")
        if match.group("ms") is not None and int(match.group("ms")) == 0:
            errors.append(f"  ERROR  {rel}: control '{name}' holds for 0 ms")
    declared = controls if isinstance(controls, list) else []
    for name in sorted(set(calibrated)):
        if calibrated.count(name) > 1:
            errors.append(f"  ERROR  {rel}: control '{name}' is calibrated twice")
    for name in declared:
        if name not in calibrated:
            errors.append(f"  ERROR  {rel}: control '{name}' has no line in ## Controls")
    for name in calibrated:
        if name not in declared:
            errors.append(
                f"  ERROR  {rel}: ## Controls calibrates '{name}', which controls: "
                f"does not declare")
        if name == RESERVED_CONTROL:
            errors.append(
                f"  ERROR  {rel}: ## Controls calibrates '{RESERVED_CONTROL}', the reserved "
                f"wait-one-frame action")
    return errors


def validate_game_scene(front_matter, body, rel):
    """Errors for a kind:game skill's scene schema: a known surface and playable
    class, controls used one at a time and calibrated in ## Controls, an
    objective, OCR predicates, and a complete typed budget."""
    errors = []
    if front_matter.get("playable") == "observe-only":
        errors.append(
            f"  ERROR  {rel}: an observe-only scene drives nothing; a scene step "
            f"plays the game, so its skill must be playable")
    errors.extend(validate_predicate(front_matter, "success", rel))
    if front_matter.get("fail") is not None:
        errors.extend(validate_predicate(front_matter, "fail", rel))
    errors.extend(validate_scene_options(front_matter, rel))
    objective = markdown_section(body, "Objective")
    if objective is None or not objective.strip():
        errors.append(f"  ERROR  {rel}: a scene needs an ## Objective the model plays toward")
    surface = front_matter.get("surface")
    if surface not in VALID_GAME_SURFACES:
        errors.append(
            f"  ERROR  {rel}: kind:game needs surface one of "
            f"{', '.join(sorted(VALID_GAME_SURFACES))} (got {surface!r})")
    if front_matter.get("playable") is None:
        errors.append(f"  ERROR  {rel}: kind:game needs a playable class")
    controls = front_matter.get("controls")
    if controls is not None:
        if not isinstance(controls, list):
            errors.append(f"  ERROR  {rel}: controls must be an inline list, e.g. [move, fire]")
        else:
            # Stock single-touch drives one control at a time: a control that
            # joins two (move+aim) needs a second finger the mirror never sends.
            for control in controls:
                if "+" in control:
                    errors.append(
                        f"  ERROR  {rel}: control '{control}' drives two controls at "
                        f"once; single-touch input uses one at a time")
                if control == RESERVED_CONTROL:
                    errors.append(
                        f"  ERROR  {rel}: control '{RESERVED_CONTROL}' is reserved for the "
                        f"wait-one-frame action and is never declared")
    if front_matter.get("playable") not in (None, "observe-only") and not controls:
        errors.append(f"  ERROR  {rel}: a playable scene must declare its controls")
    if isinstance(controls, list) and controls:
        errors.extend(validate_controls_section(body, controls, rel))
    budget = front_matter.get("budget")
    if not isinstance(budget, dict):
        errors.append(
            f"  ERROR  {rel}: kind:game needs budget: "
            f"{{ {', '.join(f + ': N' for f in BUDGET_FIELDS)} }}")
        return errors
    for field in BUDGET_FIELDS:
        raw = budget.get(field)
        if raw is None:
            errors.append(f"  ERROR  {rel}: budget is missing {field}")
        elif not isinstance(raw, str) or not raw.isdigit() or int(raw) <= 0:
            errors.append(f"  ERROR  {rel}: budget {field} must be a positive integer (got {raw!r})")
    for field in budget:
        if field not in BUDGET_FIELDS:
            errors.append(
                f"  ERROR  {rel}: unknown budget field '{field}' "
                f"(expected {', '.join(BUDGET_FIELDS)})")
    return errors


def parse_front_matter(text):
    """Parse YAML front matter from a markdown file (between --- delimiters).

    Returns (front_matter_dict, body_text) or (None, text) if no front matter.
    """
    if not text.startswith("---"):
        return None, text

    # Find the closing ---
    end_idx = text.find("\n---", 3)
    if end_idx == -1:
        return None, text

    front_matter_raw = text[4:end_idx]  # skip opening "---\n"
    body = text[end_idx + 4:]  # skip closing "\n---"

    # Parse the front matter as simple key: value pairs
    data = {}
    for line in front_matter_raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r'^(\w+):\s*(.*)', line)
        if match:
            key = match.group(1)
            value = match.group(2).strip()
            # Strip surrounding quotes
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            # Parse inline arrays (tags, controls) and inline maps (budget)
            if key in ("tags", "controls") and value.startswith("["):
                inner = value[1:-1] if value.endswith("]") else value[1:]
                data[key] = [t.strip().strip('"').strip("'") for t in inner.split(",") if t.strip()]
            elif key in ("budget", "success", "fail") and value.startswith("{"):
                data[key] = parse_inline_map(value)
            else:
                data[key] = value

    return data, body


# ---------------------------------------------------------------------------
# SKILL.md validation.
# ---------------------------------------------------------------------------


def validate_archetype_header(text, rel):
    """Check an archetype file's leading ```yaml block: it must close and carry
    `version: 1` and a `name`. Returns the list of errors."""
    end_idx = text.find("\n```", len("```yaml"))
    if end_idx == -1:
        return [f"  ERROR  {rel}: unclosed ```yaml header block"]
    header = text[len("```yaml"):end_idx]
    errors = []
    if not re.search(r'^version:\s*1\s*$', header, re.MULTILINE):
        errors.append(f"  ERROR  {rel}: archetype header must declare 'version: 1'")
    if not re.search(r'^name:\s*\S', header, re.MULTILINE):
        errors.append(f"  ERROR  {rel}: archetype header missing 'name'")
    return errors


def validate_md_file(filepath, root):
    """Validate a single SKILL.md file. Returns (errors, warnings) lists."""
    errors = []
    warnings = []
    rel = os.path.relpath(filepath, root)

    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            text = fh.read()
    except Exception as exc:
        errors.append(f"  ERROR  {rel}: failed to read file: {exc}")
        return errors, warnings

    if not text.strip():
        errors.append(f"  ERROR  {rel}: empty file")
        return errors, warnings

    # Archetype files carry their header in a leading ```yaml block, the shape
    # mirroir-run's archetype parser reads (runner/src/parser/archetype.rs).
    if rel.startswith("archetypes" + os.sep) and text.startswith("```yaml"):
        return validate_archetype_header(text, rel), warnings

    # Parse front matter
    front_matter, body = parse_front_matter(text)

    if front_matter is None:
        errors.append(f"  ERROR  {rel}: missing YAML front matter (must start with ---)")
        return errors, warnings

    # Check required front matter fields
    for field in REQUIRED_MD_FRONT_MATTER:
        if field not in front_matter or not front_matter[field]:
            errors.append(f"  ERROR  {rel}: missing required front matter field '{field}'")

    # Validate version
    version = front_matter.get("version")
    if version is not None:
        try:
            version_int = int(version)
            if version_int != 1:
                errors.append(f"  ERROR  {rel}: unsupported front matter version '{version}' (expected 1)")
        except (ValueError, TypeError):
            errors.append(f"  ERROR  {rel}: front matter version must be an integer, got '{version}'")

    # Validate optional metadata fields
    ios_min = front_matter.get("ios_min")
    if ios_min is not None:
        if not SEMVER_ISH.match(str(ios_min)):
            errors.append(f"  ERROR  {rel}: ios_min '{ios_min}' is not semver-ish (e.g. '17.0')")

    tags = front_matter.get("tags")
    if tags is not None:
        if not isinstance(tags, list):
            errors.append(f"  ERROR  {rel}: tags must be a list of strings")
        elif not all(isinstance(t, str) for t in tags):
            errors.append(f"  ERROR  {rel}: tags must be a list of strings")

    locale = front_matter.get("locale")
    if locale is not None:
        if not LOCALE_CODE.match(str(locale)):
            errors.append(f"  ERROR  {rel}: locale '{locale}' is not a valid locale code (e.g. 'en_US')")

    # Check for unknown front matter fields
    known_fields = REQUIRED_MD_FRONT_MATTER | OPTIONAL_MD_FRONT_MATTER
    for key in front_matter:
        if key not in known_fields:
            warnings.append(f"  WARN   {rel}: unknown front matter field '{key}'")

    kind = front_matter.get("kind")
    if kind is not None and kind not in VALID_KINDS:
        errors.append(
            f"  ERROR  {rel}: kind '{kind}' is not one of {', '.join(sorted(VALID_KINDS))}")
    if kind == "game":
        errors.extend(validate_game_scene(front_matter, body, rel))
    else:
        for field in SCENE_ONLY_FIELDS:
            if field in front_matter:
                errors.append(f"  ERROR  {rel}: {field} applies only to a kind:game skill")

    # Scene-schema gate (kind:game skills). `playable` must name a supported
    # control class, and an observe-only scene must declare no controls:
    # "observe" means watch, not drive. `controls` is an inline list in front
    # matter (e.g. `controls: [move, fire]`); for single-control those are used
    # one at a time (stock single-touch serializes input), which is allowed.
    playable = front_matter.get("playable")
    if playable is not None and playable not in VALID_PLAYABLE:
        errors.append(
            f"  ERROR  {rel}: playable '{playable}' is not one of "
            f"{', '.join(sorted(VALID_PLAYABLE))}")
    controls = front_matter.get("controls")
    if playable == "observe-only" and controls and str(controls).strip() not in ("", "[]", "{}"):
        errors.append(
            f"  ERROR  {rel}: observe-only skill must not declare controls "
            f"(got controls: {controls})")

    # Validate variable syntax in the body
    for match in VARIABLE_SYNTAX.finditer(text):
        var_expr = match.group(0)
        inner = var_expr[2:-1]  # strip ${ and }
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*(?::-[^}]*)?$', inner):
            errors.append(f"  ERROR  {rel}: malformed variable syntax '{var_expr}'")

    # Detect unclosed ${
    for line_num, line in enumerate(text.splitlines(), 1):
        opens = line.count("${")
        closes = line.count("}")
        if opens > closes:
            errors.append(f"  ERROR  {rel}:{line_num}: unclosed '${{' in variable expression")

    # Check body has content
    if not body.strip():
        warnings.append(f"  WARN   {rel}: empty body (no steps)")

    return errors, warnings


# ---------------------------------------------------------------------------
# YAML validation logic.
# ---------------------------------------------------------------------------


def validate_condition(cond, rel, path, depth=0):
    """Validate a condition step value. Returns (errors, has_assert)."""
    errors = []
    has_assert = False

    if depth > 3:
        errors.append(f"  ERROR  {rel}: condition nesting too deep at {path} (max 3 levels)")
        return errors, has_assert

    if not isinstance(cond, dict):
        errors.append(f"  ERROR  {rel}: {path} value must be a mapping with if_visible/if_not_visible, then, and optional else")
        return errors, has_assert

    # Must have exactly one condition type
    cond_types = [k for k in cond if k in VALID_CONDITION_TYPES]
    if len(cond_types) == 0:
        errors.append(f"  ERROR  {rel}: {path} must have 'if_visible' or 'if_not_visible'")
    elif len(cond_types) > 1:
        errors.append(f"  ERROR  {rel}: {path} must have only one of 'if_visible' or 'if_not_visible', found both")

    for ct in cond_types:
        if not isinstance(cond[ct], str) or not cond[ct].strip():
            errors.append(f"  ERROR  {rel}: {path}.{ct} must be a non-empty string")

    # Must have 'then'
    if "then" not in cond:
        errors.append(f"  ERROR  {rel}: {path} is missing required 'then' branch")
    else:
        then_steps = cond["then"]
        if not isinstance(then_steps, list) or len(then_steps) == 0:
            errors.append(f"  ERROR  {rel}: {path}.then must be a non-empty list of steps")
        else:
            step_errors, branch_assert = validate_steps(then_steps, rel, f"{path}.then", depth + 1)
            errors.extend(step_errors)
            has_assert = has_assert or branch_assert

    # 'else' is optional
    if "else" in cond:
        else_steps = cond["else"]
        if not isinstance(else_steps, list) or len(else_steps) == 0:
            errors.append(f"  ERROR  {rel}: {path}.else must be a non-empty list of steps")
        else:
            step_errors, branch_assert = validate_steps(else_steps, rel, f"{path}.else", depth + 1)
            errors.extend(step_errors)
            has_assert = has_assert or branch_assert

    # Check for unknown keys
    allowed_keys = VALID_CONDITION_TYPES | {"then", "else"}
    for key in cond:
        if key not in allowed_keys:
            errors.append(f"  ERROR  {rel}: {path} has unknown key '{key}'")

    return errors, has_assert


def validate_repeat(rep, rel, path, depth=0):
    """Validate a repeat step value. Returns (errors, has_assert)."""
    errors = []
    has_assert = False

    if depth > 3:
        errors.append(f"  ERROR  {rel}: repeat nesting too deep at {path} (max 3 levels)")
        return errors, has_assert

    if not isinstance(rep, dict):
        errors.append(f"  ERROR  {rel}: {path} value must be a mapping with a loop mode, max, and steps")
        return errors, has_assert

    # Must have exactly one loop mode
    modes = [k for k in rep if k in VALID_REPEAT_MODES]
    if len(modes) == 0:
        errors.append(f"  ERROR  {rel}: {path} must have one of: while_visible, until_visible, times")
    elif len(modes) > 1:
        errors.append(f"  ERROR  {rel}: {path} must have only one of: while_visible, until_visible, times (found {', '.join(modes)})")

    for mode in modes:
        if mode == "times":
            if not isinstance(rep[mode], int) or rep[mode] < 1:
                errors.append(f"  ERROR  {rel}: {path}.times must be a positive integer")
        else:
            if not isinstance(rep[mode], str) or not rep[mode].strip():
                errors.append(f"  ERROR  {rel}: {path}.{mode} must be a non-empty string")

    # Must have 'max' safety bound
    if "max" not in rep:
        errors.append(f"  ERROR  {rel}: {path} is missing required 'max' safety bound")
    else:
        if not isinstance(rep["max"], int) or rep["max"] < 1:
            errors.append(f"  ERROR  {rel}: {path}.max must be a positive integer")

    # Must have 'steps'
    if "steps" not in rep:
        errors.append(f"  ERROR  {rel}: {path} is missing required 'steps' list")
    else:
        rep_steps = rep["steps"]
        if not isinstance(rep_steps, list) or len(rep_steps) == 0:
            errors.append(f"  ERROR  {rel}: {path}.steps must be a non-empty list of steps")
        else:
            step_errors, branch_assert = validate_steps(rep_steps, rel, f"{path}.steps", depth + 1)
            errors.extend(step_errors)
            has_assert = has_assert or branch_assert

    # Check for unknown keys
    allowed_keys = VALID_REPEAT_MODES | {"max", "steps"}
    for key in rep:
        if key not in allowed_keys:
            errors.append(f"  ERROR  {rel}: {path} has unknown key '{key}'")

    return errors, has_assert


VALID_BARE_KEYWORDS = {"home", "press_home", "shake"}


def validate_steps(steps, rel, prefix, depth=0):
    """Validate a list of steps. Returns (errors, has_assert)."""
    errors = []
    has_assert = False

    for i, step in enumerate(steps):
        step_label = f"{prefix} {i + 1}"
        # Bare keyword steps like `- home` are parsed as strings by PyYAML
        if isinstance(step, str):
            if step not in VALID_BARE_KEYWORDS:
                errors.append(f"  ERROR  {rel}: unknown bare keyword '{step}' at {step_label}")
            continue
        if not isinstance(step, dict):
            errors.append(f"  ERROR  {rel}: {step_label} is not a mapping")
            continue
        for step_type in step:
            if step_type not in VALID_STEP_TYPES:
                errors.append(f"  ERROR  {rel}: unknown step type '{step_type}' at {step_label}")
            if step_type in ("assert_visible", "assert_not_visible"):
                has_assert = True
            if step_type == "condition":
                cond_errors, cond_assert = validate_condition(step[step_type], rel, step_label + " condition", depth)
                errors.extend(cond_errors)
                has_assert = has_assert or cond_assert
            if step_type == "repeat":
                rep_errors, rep_assert = validate_repeat(step[step_type], rel, step_label + " repeat", depth)
                errors.extend(rep_errors)
                has_assert = has_assert or rep_assert

    return errors, has_assert


def validate_yaml_file(filepath, root):
    """Validate a single YAML skill file. Returns (errors, warnings) lists."""
    errors = []
    warnings = []
    rel = os.path.relpath(filepath, root)

    try:
        data = load_yaml(filepath)
    except Exception as exc:
        errors.append(f"  ERROR  {rel}: failed to parse YAML: {exc}")
        return errors, warnings

    if data is None:
        errors.append(f"  ERROR  {rel}: empty or invalid YAML")
        return errors, warnings

    # --- Required fields ---
    for field in REQUIRED_YAML_FIELDS:
        if field not in data or data[field] is None:
            errors.append(f"  ERROR  {rel}: missing required field '{field}'")

    # --- Steps validation ---
    steps = data.get("steps", [])
    if isinstance(steps, list):
        step_errors, has_assert = validate_steps(steps, rel, "step")
        errors.extend(step_errors)

        if not has_assert:
            warnings.append(f"  WARN   {rel}: no assert_visible or assert_not_visible step")

    # --- Variable syntax ---
    with open(filepath, "r", encoding="utf-8") as fh:
        raw_text = fh.read()

    for match in VARIABLE_SYNTAX.finditer(raw_text):
        var_expr = match.group(0)
        inner = var_expr[2:-1]  # strip ${ and }
        # Valid forms: VAR, VAR:-default
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*(?::-[^}]*)?$', inner):
            errors.append(f"  ERROR  {rel}: malformed variable syntax '{var_expr}'")

    # Detect unclosed ${
    for line_num, line in enumerate(raw_text.splitlines(), 1):
        opens = line.count("${")
        closes = line.count("}")
        if opens > closes:
            errors.append(f"  ERROR  {rel}:{line_num}: unclosed '${{' in variable expression")

    # --- Optional metadata validation ---
    ios_min = data.get("ios_min")
    if ios_min is not None:
        ios_min_str = str(ios_min)
        if not SEMVER_ISH.match(ios_min_str):
            errors.append(f"  ERROR  {rel}: ios_min '{ios_min_str}' is not semver-ish (e.g. '17.0')")

    tags = data.get("tags")
    if tags is not None:
        if not isinstance(tags, list):
            errors.append(f"  ERROR  {rel}: tags must be a list of strings")
        elif not all(isinstance(t, str) for t in tags):
            errors.append(f"  ERROR  {rel}: tags must be a list of strings")

    locale = data.get("locale")
    if locale is not None:
        if not LOCALE_CODE.match(str(locale)):
            errors.append(f"  ERROR  {rel}: locale '{locale}' is not a valid locale code (e.g. 'en_US')")

    return errors, warnings


BOARD_SKILL = """---
version: 1
name: Board Scene
app: Grid Frames
kind: game
surface: scene
playable: single-control
controls: [CONTROLS]
DECIDER
image_width: WIDTH
budget: { max_frames: 3, max_tokens: 100000, max_seconds: 60 }
success: { visible: SUCCESS }
fail: { visible: ["DEFAITE", "Jouer contre des bots"] }
---

Read the board.

## Objective

Read the board into a list of the cells that are marked.

## Controls

- board: GRID
"""


def board_selftest_cases():
    """Selftest cases for a board scene: a `grid` control, list predicates,
    `image_width` and `decider`. Each case swaps one token of BOARD_SKILL."""
    defaults = {
        "CONTROLS": "board", "DECIDER": "decider: required", "WIDTH": "800",
        "SUCCESS": '"GOAL"', "GRID": "grid 3x3 from 0.134,0.216 to 0.866,0.540",
    }

    def skill(**swaps):
        text = BOARD_SKILL
        for token, value in {**defaults, **swaps}.items():
            text = text.replace(token, value)
        return text

    return [
        ("well-formed board scene (grid, decider, image_width, list fail)", True, skill()),
        ("board scene with a list success predicate", True,
         skill(SUCCESS='["GOAL", "Bravo, gagne"]')),
        ("board scene without decider or image_width", True, skill(DECIDER="", WIDTH="1170")),
        ("grid of 26x99 cells", True, skill(GRID="grid 26x99 from 0,0 to 1,1")),
        ("grid of 27 columns", False, skill(GRID="grid 27x3 from 0.1,0.2 to 0.9,0.6")),
        ("grid of 100 rows", False, skill(GRID="grid 3x100 from 0.1,0.2 to 0.9,0.6")),
        ("grid of 0 columns", False, skill(GRID="grid 0x3 from 0.1,0.2 to 0.9,0.6")),
        ("grid corner past the window", False, skill(GRID="grid 3x3 from 0.1,0.2 to 1.2,0.6")),
        ("grid running bottom-right to top-left", False,
         skill(GRID="grid 3x3 from 0.9,0.6 to 0.1,0.2")),
        ("grid with no height", False, skill(GRID="grid 3x3 from 0.1,0.4 to 0.9,0.4")),
        ("grid with no size", False, skill(GRID="grid from 0.1,0.2 to 0.9,0.6")),
        ("reserved control none declared", False, skill(CONTROLS="board, none")),
        ("reserved control none calibrated", False, skill(
            CONTROLS="board, none",
            GRID="grid 3x3 from 0.134,0.216 to 0.866,0.540\n- none: tap at 0.5,0.5")),
        ("empty list success predicate", False, skill(SUCCESS="[]")),
        ("list success predicate with an empty text", False, skill(SUCCESS='["GOAL", ""]')),
        ("image_width below 200", False, skill(WIDTH="150")),
        ("image_width above 2000", False, skill(WIDTH="2001")),
        ("image_width not an integer", False, skill(WIDTH="wide")),
        ("decider other than required", False, skill(DECIDER="decider: ./sf.sh")),
    ]


def run_selftest():
    """Self-check the scene-schema gate: a well-formed game skill validates and
    malformed ones are rejected. Returns 0 when every case matches expectation.

    Proves the carnet acceptance ("a malformed game skill fails, a well-formed
    one passes") without committing a deliberately-broken file to the tree.
    """
    import tempfile

    cases = [
        ("well-formed single-control game", True, """---
version: 1
name: Tutorial Scene
app: Brawl Stars
kind: game
surface: scene
playable: single-control
controls: [move, fire]
budget: { max_frames: 12, max_tokens: 288000, max_seconds: 180 }
success: { visible: "VICTOIRE" }
fail: { visible: "DÉFAITE, encore" }
---

Drive the Brawl Stars tutorial scene.

## Objective

Collect the power cubes.

## Controls

- move: drag from 0.18,0.80 radius 0.08
- fire: tap at 0.85,0.72
"""),
        ("invalid playable value (twin-stick)", False, """---
version: 1
name: Bad Playable
kind: game
playable: twin-stick
---

Body.
"""),
        ("observe-only declaring controls", False, """---
version: 1
name: Bad ObserveOnly
kind: game
playable: observe-only
controls: [move, fire]
---

Body.
"""),
        ("simultaneous move and aim", False, """---
version: 1
name: Bad Scene
kind: game
surface: scene
playable: single-control
controls: [move+aim]
budget: { max_frames: 12, max_tokens: 288000, max_seconds: 180 }
---

Body.
"""),
        ("untyped budget (est_tokens, max_minutes)", False, """---
version: 1
name: Bad Scene
kind: game
surface: scene
playable: single-control
controls: [move]
budget: { max_frames: 12, est_tokens: 2700, max_minutes: 3 }
---

Body.
"""),
        ("budget field not a positive integer", False, """---
version: 1
name: Bad Scene
kind: game
surface: scene
playable: single-control
controls: [move]
budget: { max_frames: 0, max_tokens: lots, max_seconds: 180 }
---

Body.
"""),
        ("game without a budget", False, """---
version: 1
name: Bad Scene
kind: game
surface: scene
playable: single-control
controls: [move]
---

Body.
"""),
        ("game without a scene surface", False, """---
version: 1
name: Bad Scene
kind: game
surface: shell
playable: single-control
controls: [move]
budget: { max_frames: 12, max_tokens: 288000, max_seconds: 180 }
---

Body.
"""),
        ("playable scene without controls", False, """---
version: 1
name: Bad Scene
kind: game
surface: scene
playable: single-control
budget: { max_frames: 12, max_tokens: 288000, max_seconds: 180 }
---

Body.
"""),
        ("scene without a success predicate", False, """---
version: 1
name: Bad Scene
kind: game
surface: scene
playable: single-control
controls: [move, fire]
budget: { max_frames: 12, max_tokens: 288000, max_seconds: 180 }
fail: { visible: "DÉFAITE" }
---

## Objective

Collect the power cubes.

## Controls

- move: drag from 0.18,0.80 radius 0.08
- fire: tap at 0.85,0.72
"""),
        ("unknown predicate kind", False, """---
version: 1
name: Bad Scene
kind: game
surface: scene
playable: single-control
controls: [move, fire]
budget: { max_frames: 12, max_tokens: 288000, max_seconds: 180 }
success: { score: "100" }
---

## Objective

Collect the power cubes.

## Controls

- move: drag from 0.18,0.80 radius 0.08
- fire: tap at 0.85,0.72
"""),
        ("control missing from ## Controls", False, """---
version: 1
name: Bad Scene
kind: game
surface: scene
playable: single-control
controls: [move, fire]
budget: { max_frames: 12, max_tokens: 288000, max_seconds: 180 }
success: { visible: "VICTOIRE" }
---

## Objective

Collect the power cubes.

## Controls

- move: drag from 0.18,0.80 radius 0.08

"""),
        ("control coordinate outside [0, 1]", False, """---
version: 1
name: Bad Scene
kind: game
surface: scene
playable: single-control
controls: [move, fire]
budget: { max_frames: 12, max_tokens: 288000, max_seconds: 180 }
success: { visible: "VICTOIRE" }
---

## Objective

Collect the power cubes.

## Controls

- move: drag from 0.18,0.80 radius 0.08
- fire: tap at 850,720
"""),
        ("pinch gesture", False, """---
version: 1
name: Bad Scene
kind: game
surface: scene
playable: single-control
controls: [move, fire]
budget: { max_frames: 12, max_tokens: 288000, max_seconds: 180 }
success: { visible: "VICTOIRE" }
---

## Objective

Collect the power cubes.

## Controls

- move: drag from 0.18,0.80 radius 0.08
- fire: pinch at 0.85,0.72
"""),
        ("scene without an objective", False, """---
version: 1
name: Bad Scene
kind: game
surface: scene
playable: single-control
controls: [move, fire]
budget: { max_frames: 12, max_tokens: 288000, max_seconds: 180 }
success: { visible: "VICTOIRE" }
---

## Controls

- move: drag from 0.18,0.80 radius 0.08
- fire: tap at 0.85,0.72
"""),
        ("observe-only scene", False, """---
version: 1
name: Bad Scene
kind: game
surface: scene
playable: observe-only
budget: { max_frames: 12, max_tokens: 288000, max_seconds: 180 }
success: { visible: "VICTOIRE" }
---

## Objective

Watch.
"""),
        ("unknown kind", False, """---
version: 1
name: Bad Kind
kind: gmae
---

Body.
"""),
        ("decider on a skill that is not a game", False, """---
version: 1
name: Bad Decider
decider: required
---

Body.
"""),
    ]
    cases.extend(board_selftest_cases())

    all_ok = True
    for label, should_pass, content in cases:
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as fh:
            fh.write(content)
            path = fh.name
        errors, _ = validate_md_file(path, os.path.dirname(path))
        os.unlink(path)
        passed = len(errors) == 0
        matched = passed == should_pass
        all_ok = all_ok and matched
        status = "OK  " if matched else "FAIL"
        detail = "" if passed else f" ({'; '.join(e.strip() for e in errors)})"
        print(f"  [{status}] {label}: expected "
              f"{'pass' if should_pass else 'fail'}, "
              f"got {'pass' if passed else 'fail'}{detail}")

    archetype_cases = [
        ("archetype ```yaml header", True,
         "```yaml\nversion: 1\nname: x/y\narchetype_version: 1.0.0\n```\n\n# X\n"),
        ("archetype header without name", False,
         "```yaml\nversion: 1\narchetype_version: 1.0.0\n```\n\n# X\n"),
        ("archetype header never closed", False,
         "```yaml\nversion: 1\nname: x/y\n"),
    ]
    with tempfile.TemporaryDirectory() as tmp_root:
        archetype_dir = os.path.join(tmp_root, "archetypes", "x")
        os.makedirs(archetype_dir)
        path = os.path.join(archetype_dir, "archetype.md")
        for label, should_pass, content in archetype_cases:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)
            errors, _ = validate_md_file(path, tmp_root)
            passed = len(errors) == 0
            matched = passed == should_pass
            all_ok = all_ok and matched
            status = "OK  " if matched else "FAIL"
            print(f"  [{status}] {label}: expected "
                  f"{'pass' if should_pass else 'fail'}, "
                  f"got {'pass' if passed else 'fail'}")

    print("\nselftest: " + ("all cases matched" if all_ok else "MISMATCH"))
    return 0 if all_ok else 1


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    all_errors = []
    all_warnings = []
    md_count = 0
    yaml_count = 0

    # Validate SKILL.md files
    for filepath in find_md_files(root):
        md_count += 1
        errs, warns = validate_md_file(filepath, root)
        all_errors.extend(errs)
        all_warnings.extend(warns)

    # Validate legacy YAML files
    for filepath in find_yaml_files(root):
        yaml_count += 1
        errs, warns = validate_yaml_file(filepath, root)
        all_errors.extend(errs)
        all_warnings.extend(warns)

    total = md_count + yaml_count
    if total == 0:
        print("No skill files found.")
        sys.exit(1)

    print(f"Validated {total} skill files ({md_count} SKILL.md, {yaml_count} YAML).\n")

    for w in all_warnings:
        print(w)
    for e in all_errors:
        print(e)

    if all_warnings:
        print(f"\n{len(all_warnings)} warning(s)")
    if all_errors:
        print(f"{len(all_errors)} error(s)")
        sys.exit(1)
    else:
        print("\nAll checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(run_selftest())
    main()
