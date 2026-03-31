#!/usr/bin/env python3

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "_data" / "inventory-export.json"
OUTPUT_DIR = ROOT / "_inventory"

FIELD_ORDER = [
    "title",
    "item_code",
    "short_code",
    "permalink",
    "category",
    "manufacturer_name",
    "model_name",
    "accession_number",
    "serial_number",
    "year_of_manufacture",
    "country_of_origin",
    "quantity",
    "condition",
    "operational_status",
    "restoration_status",
    "location",
    "acquisition_date",
    "acquisition_source",
    "provenance",
    "materials",
    "dimensions",
    "notes",
    "description",
]


def extract_short_code(item_code: str) -> str:
    digits = "".join(character for character in str(item_code) if character.isdigit())
    if not digits:
        raise ValueError(f"item_code {item_code!r} has no digits")
    return digits[-4:] if len(digits) > 4 else digits


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def build_document(item: dict, short_code: str) -> str:
    front_matter = {
        "layout": "inventory-item",
        "title": item.get("name") or "Inventory Item",
        "item_code": item.get("item_code"),
        "short_code": short_code,
        "permalink": f"/m/{short_code}/",
        "category": item.get("category"),
        "manufacturer_name": item.get("manufacturer_name"),
        "model_name": item.get("model_name"),
        "accession_number": item.get("accession_number"),
        "serial_number": item.get("serial_number"),
        "year_of_manufacture": item.get("year_of_manufacture"),
        "country_of_origin": item.get("country_of_origin"),
        "quantity": item.get("quantity"),
        "condition": item.get("condition"),
        "operational_status": item.get("operational_status"),
        "restoration_status": item.get("restoration_status"),
        "location": item.get("location"),
        "acquisition_date": item.get("acquisition_date"),
        "acquisition_source": item.get("acquisition_source"),
        "provenance": item.get("provenance"),
        "materials": item.get("materials"),
        "dimensions": item.get("dimensions"),
        "notes": item.get("notes"),
        "description": item.get("description"),
    }

    lines = ["---"]
    for field_name in ["layout", *FIELD_ORDER]:
        if field_name not in front_matter:
          continue
        value = front_matter[field_name]
        if value is None:
            continue
        if isinstance(value, str):
            lines.append(f"{field_name}: {yaml_quote(value)}")
        else:
            lines.append(f"{field_name}: {value}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    items = data.get("inventory_items", [])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for existing_file in OUTPUT_DIR.glob("*.md"):
        existing_file.unlink()

    seen_codes = {}
    for item in items:
        if not item.get("is_active"):
            continue

        short_code = extract_short_code(item.get("item_code"))
        if short_code in seen_codes:
            raise ValueError(
                f"duplicate short code {short_code} for {item.get('item_code')} and {seen_codes[short_code]}"
            )
        seen_codes[short_code] = item.get("item_code")

        slug = f"{short_code}-{item.get('item_code')}".lower()
        file_path = OUTPUT_DIR / f"{slug}.md"
        file_path.write_text(build_document(item, short_code), encoding="utf-8")


if __name__ == "__main__":
    main()