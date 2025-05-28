import pdfplumber
import pytesseract
import fitz  # PyMuPDF
from PIL import Image
import io
import re
import logging
from pydantic import BaseModel, ValidationError
from typing import List, Optional
from collections import defaultdict

# Configurar logging
logging.basicConfig(level=logging.INFO)

# ---------------------------
# MODELO PYDANTIC MELHORADO
# ---------------------------
class ArticleMetadata(BaseModel):
    title: str
    authors: List[str]
    abstract: str
    keywords: List[str] = []
    doi: Optional[str] = None
    publication_date: Optional[str] = None
    journal: Optional[str] = None

class Section(BaseModel):
    heading: str
    content: str
    page: int
    sub_sections: List[str] = []

class FigureDescription(BaseModel):
    caption: str
    page: int
    ocr_text: Optional[str] = None
    figure_type: Optional[str] = None  # 'graph', 'photo', 'diagram'

class ScientificArticle(BaseModel):
    metadata: ArticleMetadata
    sections: List[Section]
    figures: List[FigureDescription] = []
    references: List[str] = []

# ---------------------------
# FUNÇÕES AUXILIARES
# ---------------------------
def extract_text_hybrid(pdf_path: str) -> str:
    """Extrai texto do PDF com fallback inteligente."""
    full_text = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                if len(text.split()) < 50:  # Fallback por página
                    doc = fitz.open(pdf_path)
                    text = doc.load_page(page.page_number-1).get_text("text")
                full_text.append(text)
        return "\n".join(full_text)
    except Exception as e:
        logging.error(f"Erro na extração de texto: {e}")
        return ""

def extract_metadata(text: str) -> ArticleMetadata:
    """Extrai metadados do texto do artigo."""
    title_match = re.search(r"^(.*?)(?=\n(Abstract|Authors?|Introduction))", text, re.S | re.I)
    authors_match = re.search(r"Authors?:\n((?:.*?\(.*?\)\n?)+)", text, re.I)
    abstract_match = re.search(r"Abstract\n(.*?)(?=\n\b(Introduction|Methods?|References)\b)", text, re.S | re.I)
    doi_match = re.search(r"\b(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)\b", text)

    return ArticleMetadata(
        title=title_match.group(1).strip() if title_match else "Título não encontrado",
        authors=[a.strip() for a in authors_match.group(1).split(",")] if authors_match else [],
        abstract=abstract_match.group(1).strip() if abstract_match else "",
        doi=doi_match.group(1) if doi_match else None
    )

def extract_sections(text: str) -> List[Section]:
    """Identifica e extrai seções do artigo."""
    sections = []
    matches = re.finditer(r"(?:\n\s*)?(?P<heading>[A-Z][^\n]+?)\n", text, re.I)
    for match in matches:
        sections.append(Section(
            heading=match.group('heading').strip(),
            content="...",
            page=1  # Melhorar com rastreamento real de página
        ))
    return sections

def process_images(pdf_path: str):
    """Processa imagens do PDF e aplica OCR."""
    doc = fitz.open(pdf_path)
    figures = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        img_list = page.get_images(full=True)
        
        for img_index, img in enumerate(img_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            img_data = base_image["image"]

            # Converte para imagem PIL e aplica OCR
            image = Image.open(io.BytesIO(img_data))
            ocr_text = pytesseract.image_to_string(image).strip()

            figures.append({
                "page": page_num+1,
                "ocr_text": ocr_text if ocr_text else "Nenhum texto detectado"
            })

    return figures

def extract_references(text: str) -> List[str]:
    """Extrai referências da seção correta."""
    ref_section = re.search(r'(References|Bibliography)\n(.+?)(?=\n\b[A-Z]+\b)', text, re.S | re.I)
    if not ref_section:
        return []
    return [match.group(1).strip() for match in re.finditer(r'\[\d+\]\s+(.+?)(?=\n\[\d+\]|\Z)', ref_section.group(2), re.S)]

# ---------------------------
# EXECUÇÃO DO PROCESSO
# ---------------------------
def main(pdf_path):
    try:
        # Extração do texto do PDF
        main_text = extract_text_hybrid(pdf_path)

        # Extração de metadados
        metadata = extract_metadata(main_text)

        # Extração das seções do artigo
        sections = extract_sections(main_text)

        # Processamento de imagens (OCR e legendas)
        figures = process_images(pdf_path)

        # Extração das referências
        references = extract_references(main_text)

        # Estruturação final do artigo
        scientific_article = ScientificArticle(
            metadata=metadata,
            sections=sections,
            figures=figures,
            references=references
        )

        # Exibir saída formatada
        print("\n### Parsed Scientific Article\n")
        print(scientific_article.json(indent=4, exclude_none=True))

    except ValidationError as e:
        logging.error(f"Erro de validação: {e}")
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main("2309.17102v2.pdf")
