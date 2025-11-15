import re
from typing import List, Dict


from langchain_text_splitters import RecursiveCharacterTextSplitter



class TextChunker:
    def __init__(self, chunk_size: int = 800, overlap: int = 120, mode: str = "char"):
        """
        :param chunk_size: Max size of each chunk
        :param overlap: Overlapping characters between chunks
        :param mode: "char" | "sentence" | "paragraph"
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.mode = mode

    def clean_text(self, text: str) -> str:
        """Normalize whitespace and remove noise."""
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def split_sentences(self, text: str) -> List[str]:
        """Simple rule-based sentence splitter."""
        return re.split(r"(?<=[.!?]) +", text)

    def split_paragraphs(self, text: str) -> List[str]:
        return [p.strip() for p in text.split("\n") if p.strip()]

    def chunk_by_chars(self, text: str) -> List[Dict]:
        splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
        chunks = splitter.split_text(text)
        return chunks

    def chunk_by_sentences(self, text: str) -> List[Dict]:
        sentences = self.split_sentences(text)
        chunks = []
        current_chunk = ""
        start_index = 0
        idx = 0

        for s in sentences:
            if len(current_chunk) + len(s) <= self.chunk_size:
                current_chunk += s + " "
            else:
                chunks.append({
                    "id": idx,
                    "start": start_index,
                    "end": start_index + len(current_chunk),
                    "text": current_chunk.strip(),
                })
                start_index += len(current_chunk)
                idx += 1
                current_chunk = s + " "

        if current_chunk.strip():
            chunks.append({
                "id": idx,
                "start": start_index,
                "end": start_index + len(current_chunk),
                "text": current_chunk.strip(),
            })

        return chunks

    def chunk_by_paragraphs(self, text: str) -> List[Dict]:
        paragraphs = self.split_paragraphs(text)
        chunks = []
        curr = ""
        idx = 0

        for p in paragraphs:
            if len(curr) + len(p) <= self.chunk_size:
                curr += p + " "
            else:
                chunks.append({
                    "id": idx,
                    "text": curr.strip(),
                })
                idx += 1
                curr = p + " "

        if curr.strip():
            chunks.append({
                "id": idx,
                "text": curr.strip()
            })

        return chunks

    def chunk(self, text: str) -> List[Dict]:
        text = self.clean_text(text)

        if not text:
            return []

        if self.mode == "sentence":
            return self.chunk_by_sentences(text)
        if self.mode == "paragraph":
            return self.chunk_by_paragraphs(text)

        # default = char-based chunking
        return self.chunk_by_chars(text)
