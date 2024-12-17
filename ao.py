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

def generate_ao_map(diffuse_image, ao_intensity):
    """Genera un mapa de oclusión ambiental donde todo es blanco (puede ajustarse) en formato RGB."""
    width, height = diffuse_image.size
    ao_map = Image.new('RGB', (width, height), color=(255, 255, 255)) # Todo blanco, ajustable

    # Ajustar intensidad usando brillo
    enhancer = ImageEnhance.Brightness(ao_map)
    ao_map = enhancer.enhance(ao_intensity)

    return ao_map
