import json
import csv

# Open and load the JSON file
with open("abuseipdb_blacklist.json") as f:
    data = json.load(f)

# Open CSV file for writing
with open('abuseipdb_blacklist.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the header row (modify based on your keys)
    writer.writerow(["ipAddress", "countryCode", "abuseConfidenceScore", "lastReportedAt"])
    
    # Iterate over the list of dictionaries
    for entry in data:
        writer.writerow([
            entry.get("ipAddress"),
            entry.get("countryCode"),
            entry.get("abuseConfidenceScore"),
            entry.get("lastReportedAt")
        ])

print("CSV file 'output.csv' created successfully.")