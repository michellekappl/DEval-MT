import csv
import sys

csv_file = sys.argv[1]
with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=";")
    # delete the header
    next(reader)
    # sort by column 3 and 4
    sorted_rows = sorted(
        reader, key=lambda row: (row[2].strip("[]"), row[3].strip("[]"))
    )
    # count the number of rows in each group
    # print(sorted_rows)
    group_counts = {}
    for row in sorted_rows:
        group_x = row[2].strip("[]").split(",")
        group_y = row[3].strip("[]").split(",")
        for group in set(group_x + group_y):
            if group not in group_counts:
                group_counts[group] = 0
            group_counts[group] += 1
    # print the group counts
    for group, count in group_counts.items():
        print(f"{group}: {count} rows")
    # save sorted rows to a new CSV file
    with open("sorted_" + csv_file, "w", newline="", encoding="utf-8") as out_f:
        writer = csv.writer(out_f, delimiter=";")
        # write the header
        writer.writerow(["sentence", "hierarchy", "x_groups", "y_groups"])
        # write the sorted rows
        for row in sorted_rows:
            writer.writerow(row)
