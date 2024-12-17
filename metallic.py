# ----------------------------------------------------------------------------
#  File:        metallic.py
#  Module:      Metallic
#  Description: Módulo para generar el mapa metálico.
#
#  Author:      Mauricio José Tobares
#  Created:     15/12/2024
#  Copyright:   (c) 2024 Mauricio José Tobares
#  License:     MIT License
# ----------------------------------------------------------------------------

from PIL import Image, ImageEnhance

def generate_metallic_map(diffuse_image: Image.Image, metallic_intensity: float) -> Image.Image:
    """
    Genera un mapa metálico donde todo es blanco (puede ajustarse) en formato RGB.

    Este mapa se utiliza para indicar qué partes de la superficie son metálicas.
    Por defecto, genera una imagen completamente blanca que puede ser ajustada en intensidad.

    Args:
        diffuse_image (PIL.Image.Image): La imagen diffuse de entrada (utilizada solo para obtener las dimensiones).
        metallic_intensity (float): La intensidad del brillo a aplicar al mapa metálico (0-100).

    Returns:
        PIL.Image.Image: El mapa metálico generado.
    """
    width, height = diffuse_image.size
    # Crear una imagen completamente blanca
    metallic_map = Image.new('RGB', (width, height), color=(255, 255, 255))

    # Ajustar intensidad usando brillo
    enhancer = ImageEnhance.Brightness(metallic_map)
    metallic_map = enhancer.enhance(metallic_intensity * 0.01) # Se multiplica el porcentaje por un valor para conseguir más brillo

    return metallic_map
