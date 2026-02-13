import fitz 

class PdfReader:

    def __init__(self, path: str):
        self.path = path
        self.num_pages = 0

    def reader(self):

        try:
            full_text = ""
            with fitz.open(self.path) as doc:
                self.num_pages = len(doc)
                for page in doc:
                    full_text += page.get_text() + "\n"
            
            return {"full_text": full_text, "num_pages": self.num_pages}

        except Exception as e:
            print(f"Error al leer el PDF {self.path}: {str(e)}")
            return ""