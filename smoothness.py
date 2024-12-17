#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Mauricio
#
# Created:     15/12/2024
# Copyright:   (c) Mauricio 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from PIL import Image, ImageEnhance

def generate_smoothness_map(diffuse_image, smoothness_intensity):
    """Genera un mapa de suavidad donde todo es blanco (puede ajustarse) en formato RGB."""
    width, height = diffuse_image.size
    smoothness_map = Image.new('RGB', (width, height), color=(255, 255, 255)) # Todo blanco, ajustable

    # Ajustar intensidad usando brillo
    enhancer = ImageEnhance.Brightness(smoothness_map)
    smoothness_map = enhancer.enhance(smoothness_intensity)

    return smoothness_map
