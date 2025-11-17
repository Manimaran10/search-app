import mimetypes
# from pdf2image import convert_from_bytes
# from PIL import Image
# import pytesseract
import io
from services.indexer.indexer import TextIndexer
class FileProcesser:

    def __init__(self):
        self.indexer = TextIndexer()

    def process(self, file_bytes, source) -> None:
        source  = str(source)
        file_type = self.detect_file_type(str(source))

        result = {
        "source": source,
        "file_type": file_type,
        "raw_text": None,
        }

        if file_type == "image":
            result["raw_text"] = self.ocr_image(file_bytes)

        elif file_type == "pdf":
            result["raw_text"] = self.ocr_pdf(file_bytes)

        else:
            result["raw_text"] = file_bytes.decode(errors="ignore")

        if not result["raw_text"]:
            raise Exception("No text extracted from the file or invalid source")
        print("Indexing extracted text...")
        index_response = self.indexer.process(result["raw_text"], source=source)
        print("Indexing completed.")
        return index_response

    def detect_file_type(self,source):
        mime = mimetypes.guess_type(source)[0]

        if not mime:
            return "unknown"

        if mime.startswith("image/"):
            return "image"

        if mime == "application/pdf":
            return "pdf"

        return "other"
    
    # def ocr_image(self,file_bytes):
    #     img = Image.open(io.BytesIO(file_bytes))
    #     return pytesseract.image_to_string(img)

    # def ocr_pdf(self, file_bytes) -> str:
    #     pages = convert_from_bytes(file_bytes)
        
    #     text = ""
    #     for page in pages:
    #         text += pytesseract.image_to_string(page) + "\n"

    #     return text.strip()
