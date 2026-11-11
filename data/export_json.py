
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_DIR = ROOT / "data" / "generated"
JSON_DIR = CSV_DIR / "json"

JSON_DIR.mkdir(parents=True, exist_ok=True)

csv_files = sorted(CSV_DIR.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError(f"No CSV files found in {CSV_DIR}")

for csv_path in csv_files:
    json_path = JSON_DIR / f"{csv_path.stem}.jsonl"
    row_count = 0

    with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        with json_path.open("w", encoding="utf-8") as json_file:
            for row in reader:
                # Preserve source values; represent blank CSV fields as JSON null.
                record = {
                    key: (value if value != "" else None)
                    for key, value in row.items()
                }

                json_file.write(
                    json.dumps(record, ensure_ascii=False) + "\n"
                )
                row_count += 1

    print(f"Exported {csv_path.name}: {row_count:,} records")

print(f"\nSUCCESS: JSONL exports created in {JSON_DIR}")
