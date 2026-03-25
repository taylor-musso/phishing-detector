import csv
import json

csv_file = "data/Webpages_Classification_test_data.csv"
json_file = "data/webpages_classification.json"

with open(csv_file, mode="r", encoding="utf-8") as infile, \
     open(json_file, mode="w", encoding="utf-8") as outfile:

    reader = csv.DictReader(infile)

    for row in reader:
        json_line = json.dumps(row)
        outfile.write(json_line + "\n")

print("Done! NDJSON file created.")