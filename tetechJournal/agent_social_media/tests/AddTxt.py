
from core.image_processing.textOverlay import ImageTextOverlay
    
input_image = "sandeco.png"  # Caminho da imagem de entrada
output_image = "output.png"  # Caminho para salvar a imagem editada
text_to_add = "Atenção!!"

# Chamada da função
ImageTextOverlay.add_text_to_image(
    input_image, text_to_add, output_image,
    position=(100,100), 
    font_size=100, font_color="white", outline_color="black",
    box_enabled=True, box_color="blue", box_opacity=180,
    box_padding=30, box_border_thickness=5, box_border_color="yellow",
    box_roundness=20
)

print(f"Imagem salva em: {output_image}")