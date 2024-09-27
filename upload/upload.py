import json
import requests

pdf_file = "./invoice.pdf"
base_url = "https://smartaccount.hr"
key_id = "id"
api_key = "key"

data = {}
data["title"] = "Andrei Test"
data["date"] = "2024-09-27"
data["document_type"] = "incoming_invoice"

data = json.dumps(data)

response = requests.post(f"{base_url}/api/documents",
    data=data,
    headers={"content-type": "application/json", "key-id": key_id, "authorization": api_key},
)

document_id = response.json()["id"]
upload_url = f"{base_url}/api/documents/{document_id}/upload"

file = open(pdf_file, "rb")

response = requests.post(upload_url,
  files={"file": (pdf_file, file, "application/pdf")},
  headers={"key-id": key_id, "authorization": api_key},
)

print(response.text)
