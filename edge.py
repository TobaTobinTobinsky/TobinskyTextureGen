# ----------------------------------------------------------------------------
#  File:        edge.py
#  Module:      Edge
#  Description: Módulo para generar el mapa de bordes.
#
#  Author:      Mauricio José Tobares
#  Created:     15/12/2024
#  Copyright:   (c) 2024 Mauricio José Tobares
#  License:     MIT License
# ----------------------------------------------------------------------------

from PIL import Image, ImageFilter, ImageEnhance

def generate_edge_map(diffuse_image: Image.Image, smoothness_map: Image.Image, edge_intensity: float) -> Image.Image:
    """
    Genera un mapa de bordes usando un filtro de contorno e influenciado por el mapa de suavidad.

    Este mapa de bordes se crea aplicando un filtro de detección de bordes a la imagen
    diffuse en escala de grises. Luego, los bordes se atenúan en función del mapa de
    suavidad y su intensidad final se ajusta.

    Args:
        diffuse_image (PIL.Image.Image): La imagen diffuse de entrada.
        smoothness_map (PIL.Image.Image): El mapa de suavidad que influencia el resultado.
        edge_intensity (float): La intensidad del brillo a aplicar al mapa de bordes (0-100).

    Returns:
        PIL.Image.Image: El mapa de bordes generado.
    """
    # Convierte la imagen diffuse a escala de grises
    gray_image = diffuse_image.convert('L')
    # Aplica un filtro para detectar bordes
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
    edge_map = enhancer.enhance(edge_intensity * 0.01)  # Se multiplica el porcentaje por un valor para conseguir más brillo

    return edge_map
