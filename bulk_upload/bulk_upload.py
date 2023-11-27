# Use python 3.11
#
# This scripts takes your CSV file and uploads all the files listed there.
# To use it:
# 1. generate an API key (or reuse an existing one), be sure to save both
#    the ID and the key
# 2. in the folder with your files create a csv file named "records.csv",
#    with the following format:
#    file_path;Title of the document;2023-12-25;type
#
#    supported types are: incoming_invoice outgoing_invoice contract paystub
#      travel_document payment_file other quote
# 3. run the script!

import csv
import json
import requests

csv_file = "records.csv"
base_url = "https://smartaccount.hr"
key_id = "api_<ID>"
api_key = "key_<YOUR_KEY>"

with open(csv_file, newline="") as csvfile:
  documents = csv.reader(csvfile, delimiter=";")
  for document in documents:
      file_path = document[0]
      file = open(file_path, "rb")

      data = {}
      data["title"] = document[1]
      data["date"] = document[2]
      data["document_type"] = document[3]

      data = json.dumps(data)

      response = requests.post(f"{base_url}/api/documents",
          data=data,
          headers={"content-type": "application/json", "key-id": key_id, "authorization": api_key},
      )

      document_id = response.json()["id"]
      upload_url = f"{base_url}/api/documents/{document_id}/upload"

      response = requests.post(upload_url,
        files={"file": (file_path, file, "application/pdf")},
        headers={"key-id": key_id, "authorization": api_key},
      )

      print(response.text)
