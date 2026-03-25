import json

input_file = "data/webpages_classification.json"
output_file = "data/filtered_malicious_webpages.json"

with open(input_file, "r", encoding="utf-8") as infile, \
     open(output_file, "w", encoding="utf-8") as outfile:

    for line in infile:
        data = json.loads(line)

        if data.get("label") == "bad":
            filtered = {
            "url": data.get("url"),
            "label": data.get("label")
            }
            outfile.write(json.dumps(filtered) + "\n")

print("Filtered bad links saved.")