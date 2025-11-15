import mimetypes
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
import io
from services.categorization.topic_categorizer import TopicCategorizer
from services.categorization.project_categorizer import ProjectCategorizer
from services.categorization.team_categorizer import TeamCategorizer
class FileProcesser:
    def process(self, file_bytes, filename) -> None:
        file_type = self.detect_file_type(filename, file_bytes)

        result = {
        "filename": filename,
        "file_type": file_type,
        "raw_text": None,
        }

        if file_type == "image":
            result["raw_text"] = self.ocr_image(file_bytes)

        elif file_type == "pdf":
            result["raw_text"] = self.ocr_pdf(file_bytes)

        else:
            result["raw_text"] = file_bytes.decode(errors="ignore")

        def categorize_text(text):
            topic_categorizer = TopicCategorizer()
            project_categorizer = ProjectCategorizer()
            team_categorizer = TeamCategorizer()
            topic_result = topic_categorizer.categorize(text)
            project_result = project_categorizer.categorize(text)
            team_result = team_categorizer.categorize(text)
            return {
                "topic": topic_result,
                "project": project_result,
                "team": team_result
            }
        result["categories"] = categorize_text(result["raw_text"])

        return result

    def detect_file_type(self,filename, file_bytes):
        mime = mimetypes.guess_type(filename)[0]

        if not mime:
            return "unknown"

        if mime.startswith("image/"):
            return "image"

        if mime == "application/pdf":
            return "pdf"

        return "other"
    
    def ocr_image(self,file_bytes):
        img = Image.open(io.BytesIO(file_bytes))
        return pytesseract.image_to_string(img)

    def ocr_pdf(self, file_bytes) -> str:
        pages = convert_from_bytes(file_bytes)
        
        text = ""
        for page in pages:
            text += pytesseract.image_to_string(page) + "\n"

        return text.strip()