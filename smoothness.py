# ----------------------------------------------------------------------------
#  File:        smoothness.py
#  Module:      Smoothness
#  Description: Módulo para generar el mapa de suavidad.
#
#  Author:      Mauricio José Tobares
#  Created:     15/12/2024
#  Copyright:   (c) 2024 Mauricio José Tobares
#  License:     MIT License
# ----------------------------------------------------------------------------

from PIL import Image, ImageEnhance

def generate_smoothness_map(diffuse_image: Image.Image, smoothness_intensity: float) -> Image.Image:
    """
    Genera un mapa de suavidad donde todo es blanco (puede ajustarse) en formato RGB.

    Este mapa se utiliza para indicar la suavidad de la superficie,
    influyendo en cómo se reflejan las luces. Por defecto, genera una imagen
    completamente blanca que puede ser ajustada en intensidad.

    Args:
        diffuse_image (PIL.Image.Image): La imagen diffuse de entrada (utilizada solo para obtener las dimensiones).
        smoothness_intensity (float): La intensidad del brillo a aplicar al mapa de suavidad (0-100).

    Returns:
        PIL.Image.Image: El mapa de suavidad generado.
    """
    width, height = diffuse_image.size
    # Crear una imagen completamente blanca
    smoothness_map = Image.new('RGB', (width, height), color=(255, 255, 255))

    # Ajustar intensidad usando brillo
    enhancer = ImageEnhance.Brightness(smoothness_map)
    smoothness_map = enhancer.enhance(smoothness_intensity * 0.01)  # Se multiplica el porcentaje por un valor para conseguir más brillo

    return smoothness_map
