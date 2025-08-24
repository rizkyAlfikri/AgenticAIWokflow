import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

mistral_client = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY")
)

# Upload to S3
uploaded_pdf = mistral_client.files.upload(
    file = {
        "file_name": "company.pdf",
        "content": open("company.pdf", "rb"),
    },
    purpose="ocr"
)   

signed_url = mistral_client.files.get_signed_url(
    file_id=uploaded_pdf.id
)

ocr_response = mistral_client.ocr.process(
    model="mistral-ocr-latest",
    document = {
        "type": "document_url",
        "document_url": signed_url.url,
    }
)

pages: dict[str: any] = ocr_response.model_dump().get("pages")

all_text = ""
for page in pages:
    all_text += page.get("markdown")

with open("company.md", "w") as f:
    f.write(all_text)

print("OCR processing complete. Text saved to company.txt.")
