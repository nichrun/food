#!/usr/bin/env python3

import argparse
import json
import os
import sys
import tempfile
from datetime import date
from pathlib import Path


SCHEMA_VERSION = 1
REQUIRED_DIRECTORIES = ("meal-plans", "tesco-orders")
FILE_TEMPLATES = {
    "profile.md": """---
schema_version: 1
updated: null
---

# Food Profile

## Household

_Not recorded yet._

## Allergies and Hard Restrictions

_Not recorded yet._

## Likes and Favourite Cuisines

_Not recorded yet._

## Dislikes and Temporary Avoidances

_Not recorded yet._

## Meal Patterns and Portion Sizes

_Not recorded yet._

## Cooking Time, Effort and Equipment

_Not recorded yet._

## Budget and Shopping Priorities

_Not recorded yet._

## Retailer and Fulfilment Preferences

_Not recorded yet._

## Product and Substitution Preferences

_Not recorded yet._
""",
    "inventory.md": """---
schema_version: 1
updated: null
---

# Food Inventory

## Pantry

_Nothing recorded yet._

## Fridge

_Nothing recorded yet._

## Freezer

_Nothing recorded yet._

## Incoming Orders

_Nothing currently on order._

## Use Soon

_Nothing recorded yet._
""",
    "recipes.md": """---
schema_version: 1
updated: null
---

# Recipe Memory

Record recipes after the user cooks them and gives clear feedback.

_No recipes recorded yet._
""",
}


def config_path() -> Path:
    override = os.environ.get("FOOD_CONFIG_PATH")
    if override:
        return Path(override).expanduser().resolve()
    return Path.home() / ".config" / "food" / "config.json"


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temporary_name, path)
    except BaseException:
        Path(temporary_name).unlink(missing_ok=True)
        raise


def read_config() -> dict:
    path = config_path()
    if not path.exists():
        raise FileNotFoundError(f"Food is not configured. Missing {path}")
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Unsupported Food configuration schema")
    data_directory = data.get("data_directory")
    if not isinstance(data_directory, str) or not data_directory:
        raise ValueError("Food configuration has no data_directory")
    return data


def ensure_layout(data_directory: Path) -> list[str]:
    created = []
    data_directory.mkdir(parents=True, exist_ok=True)
    for directory_name in REQUIRED_DIRECTORIES:
        directory = data_directory / directory_name
        if not directory.exists():
            directory.mkdir(parents=True)
            created.append(str(directory))
    for file_name, template in FILE_TEMPLATES.items():
        destination = data_directory / file_name
        if not destination.exists():
            atomic_write(destination, template)
            created.append(str(destination))
    return created


def initialize(data_directory_value: str, replace_location: bool) -> dict:
    destination = Path(data_directory_value).expanduser().resolve()
    path = config_path()
    if path.exists():
        existing = read_config()
        existing_destination = Path(existing["data_directory"]).resolve()
        if existing_destination != destination and not replace_location:
            raise ValueError(
                f"Food already uses {existing_destination}. Use --replace-location to change it."
            )
    created = ensure_layout(destination)
    configuration = {
        "schema_version": SCHEMA_VERSION,
        "data_directory": str(destination),
        "updated": date.today().isoformat(),
    }
    atomic_write(path, json.dumps(configuration, indent=2) + "\n")
    return {"config": str(path), "data_directory": str(destination), "created": created}


def ensure() -> dict:
    configuration = read_config()
    destination = Path(configuration["data_directory"]).expanduser().resolve()
    created = ensure_layout(destination)
    return {"config": str(config_path()), "data_directory": str(destination), "created": created}


def status() -> dict:
    path = config_path()
    if not path.exists():
        return {"configured": False, "config": str(path)}
    configuration = read_config()
    destination = Path(configuration["data_directory"]).expanduser().resolve()
    missing = [
        name
        for name in (*FILE_TEMPLATES.keys(), *REQUIRED_DIRECTORIES)
        if not (destination / name).exists()
    ]
    return {
        "configured": True,
        "config": str(path),
        "data_directory": str(destination),
        "missing": missing,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Initialize and locate private Food plugin data")
    subparsers = parser.add_subparsers(dest="command", required=True)

    initialize_parser = subparsers.add_parser("init", help="Create or connect a Food data directory")
    initialize_parser.add_argument("--data-dir", required=True)
    initialize_parser.add_argument("--replace-location", action="store_true")

    subparsers.add_parser("locate", help="Print the configured Food data directory")
    subparsers.add_parser("ensure", help="Create any missing required files without overwriting data")
    subparsers.add_parser("status", help="Report configuration and layout status")
    return parser


def main() -> int:
    arguments = build_parser().parse_args()
    try:
        if arguments.command == "init":
            result = initialize(arguments.data_dir, arguments.replace_location)
        elif arguments.command == "locate":
            result = read_config()["data_directory"]
        elif arguments.command == "ensure":
            result = ensure()
        else:
            result = status()
        if isinstance(result, str):
            print(result)
        else:
            print(json.dumps(result, indent=2))
        return 0
    except (FileNotFoundError, ValueError, json.JSONDecodeError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
