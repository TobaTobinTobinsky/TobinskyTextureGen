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

from PIL import Image, ImageColor, ImageEnhance

def generate_metallic_map(diffuse_image, metallic_intensity):
    """Genera un mapa metálico donde todo es blanco (puede ajustarse) en formato RGB."""
    width, height = diffuse_image.size
    metallic_map = Image.new('RGB', (width, height), color=(255, 255, 255))  # Todo blanco, ajustable

    # Ajustar intensidad usando brillo
    enhancer = ImageEnhance.Brightness(metallic_map)
    metallic_map = enhancer.enhance(metallic_intensity)

    return metallic_map
