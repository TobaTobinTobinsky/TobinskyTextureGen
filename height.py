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

from PIL import Image, ImageOps, ImageEnhance

def generate_height_map(diffuse_image, height_percentage):
    """Convierte la imagen diffuse a escala de grises y ajusta el contraste para un mapa de altura."""
    height_map = diffuse_image.convert('L')
    height_map = ImageOps.autocontrast(height_map)

    # Ajustar intensidad
    enhancer = ImageEnhance.Contrast(height_map)
    height_map = enhancer.enhance(height_percentage)

    return height_map
