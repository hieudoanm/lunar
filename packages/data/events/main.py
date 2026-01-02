import csv
import json


def parse_value(value):
    if value is None:
        return value

    value = value.strip()

    # Try int
    if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
        return int(value)

    # Try float
    try:
        return float(value)
    except ValueError:
        return value


def get_missing_days_by_month(rows):
    """
    Returns:
    {
      month: [missing_days]
    }
    """
    DAYS_IN_MONTH = {
        1: 31,
        2: 29,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }

    result = {}

    for month in range(1, 13):
        max_day = DAYS_IN_MONTH[month]

        existing_days = {
            row["date"]
            for row in rows
            if row.get("month") == month and row.get("date") is not None
        }

        missing_days = [d for d in range(1, max_day + 1) if d not in existing_days]

        if missing_days:
            result[month] = missing_days

    return result


def add_zero(number: int) -> str:
    if number > 9:
        return f"{number}"
    return f"0{number}"


# ---- Files ----
csv_file = "csv/events.csv"
json_file = "json/events.json"

# ---- Read CSV ----
with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = [{key: parse_value(value) for key, value in row.items()} for row in reader]

# ---- Write JSON ----
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2, ensure_ascii=False)

# ---- Find missing dates ----
missing_dates = get_missing_days_by_month(rows)

# ---- Output ----
print("Missing dates by month:")
for month, days in missing_dates.items():
    print(f"Month {add_zero(month)}: ({add_zero(len(days))}) {days}")

print("\nCSV converted to JSON with numbers parsed")
