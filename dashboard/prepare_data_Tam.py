"""Export the compact dataset used by index_Tam.html from a Tableau TWBX.

Usage:
    python3 prepare_data_Tam.py "/path/to/NYC AirBnB.twbx"

Dependency:
    python3 -m pip install tableauhyperapi
"""

from __future__ import annotations

import argparse
import json
import os
import tempfile
import zipfile
from pathlib import Path

from tableauhyperapi import Connection, HyperProcess, Telemetry


DEFAULT_OUTPUT = Path(__file__).resolve().parent / "data" / "dt_tam_market_analysis.json"

# The extract mixes nightly USD with cent-denominated values. The clearest
# examples are Hotel room prices around 40,000–50,000, while the dataset median
# is 154. Keep the raw value in `pr` whenever this conservative rule is applied.
CENT_DENOMINATED_PRICE_THRESHOLD = 5_000


def find_hyper_member(workbook: zipfile.ZipFile) -> str:
    members = [name for name in workbook.namelist() if name.lower().endswith(".hyper")]
    if not members:
        raise ValueError("Không tìm thấy Tableau Hyper extract trong file TWBX.")
    return members[0]


def export_records(twbx_path: Path, output_path: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="tableau_tam_") as temporary_directory:
        temporary_path = Path(temporary_directory)
        with zipfile.ZipFile(twbx_path) as workbook:
            member = find_hyper_member(workbook)
            extracted_path = Path(workbook.extract(member, temporary_path))

        # Hyper writes hyperd.log to the current directory. Run it inside the
        # disposable extraction folder so preprocessing leaves the repo clean.
        previous_working_directory = Path.cwd()
        os.chdir(temporary_path)
        try:
            process_context = HyperProcess(Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU)
            process = process_context.__enter__()
            connection_context = Connection(process.endpoint, extracted_path)
            connection = connection_context.__enter__()
            try:
                tables = [
                    table
                    for schema in connection.catalog.get_schema_names()
                    for table in connection.catalog.get_table_names(schema)
                ]
                listing_tables = [table for table in tables if "listings_clean" in str(table)]
                if not listing_tables:
                    raise ValueError("Không tìm thấy bảng listings_clean trong Hyper extract.")

                table = listing_tables[0]
                query = f'''SELECT
                    "id", "neighbourhood_group_cleansed", "neighbourhood_cleansed",
                    "room_type", "price_numeric", "reviews_per_month", "host_id",
                    "calculated_host_listings_count", "latitude", "longitude"
                FROM {table}
                WHERE "has_observed_price" = TRUE
                  AND "price_numeric" IS NOT NULL'''

                records = []
                normalized_price_count = 0
                for row in connection.execute_list_query(query):
                    raw_price = float(row[4])
                    is_cent_denominated = raw_price >= CENT_DENOMINATED_PRICE_THRESHOLD
                    normalized_price = raw_price / 100 if is_cent_denominated else raw_price
                    record = {
                        "i": str(row[0]),
                        "b": row[1] or "Unknown",
                        "n": row[2] or "Unknown",
                        "r": row[3] or "Unknown",
                        "p": round(normalized_price, 2),
                        "d": round(float(row[5] or 0), 3),
                        "h": str(row[6] or "Unknown"),
                        "s": int(row[7] or 1),
                        "lt": round(float(row[8]), 5) if row[8] is not None else None,
                        "lg": round(float(row[9]), 5) if row[9] is not None else None,
                    }
                    if is_cent_denominated:
                        record["pr"] = round(raw_price, 2)
                        normalized_price_count += 1
                    records.append(record)
            finally:
                connection_context.__exit__(None, None, None)
                process_context.__exit__(None, None, None)
        finally:
            os.chdir(previous_working_directory)

    payload = {
        "meta": {
            "source": twbx_path.name,
            "price_q1": 90,
            "price_q3": 269,
            "record_count": len(records),
            "price_normalization": {
                "rule": "raw price >= 5000 is treated as cents and divided by 100",
                "normalized_records": normalized_price_count,
            },
        },
        "listings": records,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"Đã xuất {len(records):,} listings vào {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export dữ liệu Tableau cho index_Tam.html")
    parser.add_argument("twbx", type=Path, help="Đường dẫn tới file Tableau .twbx")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    export_records(args.twbx.expanduser().resolve(), args.output.expanduser().resolve())


if __name__ == "__main__":
    main()
