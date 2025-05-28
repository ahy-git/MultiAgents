from crewai.tools import BaseTool
from reportlab.pdfgen import canvas 
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import os

class PDFCreationTool(BaseTool):
    name: str = "Pdf Creation tool"
    description: str = """
    Esta ferramenta gera um arquivo PDF que inclui
    um título , uma descri ção e uma imagem . É útil para criar relat ó rios
    com elementos visuais incorporados .
    """
    
    def _run(self, title: str, text: str,
             image_path: str, output_path: str = "output.pdf" 
             )-> str :
        """
        Gera um PDF contendo o título , texto e uma imagem especificada .
        Args :
            title (str): O tí tulo a ser exibido no PDF.
            text (str): O texto a ser inclu ído.
            image_path ( str): O caminho para a imagem .
            output_path (str): O caminho onde o PDF " output .pdf ".
            Returns :
            str : nome do arquivo gerado .
        """
        
        if not os.path.exists(image_path):
            return f"Erro: arquivo de imagen nao existente em {image_path}"
        
        #cria pdf
        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4
        margin = 10
        
        #titulo ao pdf
        c.setFont('Helvetica-Bold',16)
        c.drawString(margin, height - 50,title)
        
        # adiciona texto
        c.setFont("Helvetica",12)
        y_pos = height - 80
        # implementar draw_wrapped_text
        # y_pos = draw_wrapped_text (c,text,margin,y_pos,width-2*margin) 
        
        #adiciona imagem
        try:
            image = ImageReader(image_path)
            c.drawImage(image, 50, height -350, width=500,height=250, 
                        preserveAspectRatio=True)
        except Exception as e:
            return f'Erro ao inserir imagem: {e}'
        
        #finaliza pdf
        c.showPage()
        c.save()
        
        return f'PDF criado com sucesso em: {output_path}'
    