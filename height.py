# ----------------------------------------------------------------------------
#  File:        height.py
#  Module:      Height
#  Description: Módulo para generar el mapa de altura.
#
#  Author:      Mauricio José Tobares
#  Created:     15/12/2024
#  Copyright:   (c) 2024 Mauricio José Tobares
#  License:     MIT License
# ----------------------------------------------------------------------------

from PIL import Image, ImageOps, ImageEnhance

def generate_height_map(diffuse_image: Image.Image, height_percentage: float) -> Image.Image:
    """
    Convierte la imagen diffuse a escala de grises y ajusta el contraste para un mapa de altura.

    Este mapa de altura se utiliza como base para generar el mapa normal.
    Aplica autocontraste a la imagen en escala de grises y luego ajusta su intensidad.

    Args:
        diffuse_image (PIL.Image.Image): La imagen diffuse de entrada.
        height_percentage (float): El porcentaje de contraste a aplicar (0-100).

    Returns:
        PIL.Image.Image: El mapa de altura generado.
    """
    # Convierte la imagen diffuse a escala de grises
    height_map = diffuse_image.convert('L')
    # Aplica autocontraste para mejorar el rango dinámico
    height_map = ImageOps.autocontrast(height_map)

    # Ajustar intensidad con un slider
    enhancer = ImageEnhance.Contrast(height_map)
    height_map = enhancer.enhance(height_percentage * 0.1) # Se multiplica el porcentaje por un valor para conseguir más contraste

    return height_map

