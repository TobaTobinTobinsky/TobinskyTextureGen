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

from PIL import Image, ImageFilter, ImageEnhance

def generate_edge_map(diffuse_image, smoothness_map, edge_intensity):
    """Genera un mapa de bordes usando un filtro de contorno e influenciado por el mapa de suavidad."""
    gray_image = diffuse_image.convert('L')
    edge_map = gray_image.filter(ImageFilter.FIND_EDGES)

    # Ajustar intensidad de los bordes en función del suavizado
    width, height = edge_map.size
    pixels_edge = edge_map.load()
    pixels_smoothness = smoothness_map.load()

    for y in range(height):
        for x in range(width):
            smoothness_value = pixels_smoothness[x, y]
            if isinstance(smoothness_value, tuple): # Se verifica que el valor de smoothness sea una tupla
                smoothness_value = smoothness_value[0] # Si es una tupla, se obtiene el primer valor

            smoothness_value = smoothness_value / 255

            edge_value = pixels_edge[x, y]
            if isinstance(edge_value, tuple):  # Se verifica que el valor de edge sea una tupla
                edge_value = edge_value[0]  # Si es una tupla, se obtiene el primer valor

            new_edge_value = int(edge_value * (1-smoothness_value))
            pixels_edge[x, y] = new_edge_value

    # Ajustar intensidad usando brillo
    enhancer = ImageEnhance.Brightness(edge_map)
    edge_map = enhancer.enhance(edge_intensity)

    return edge_map
