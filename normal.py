# ----------------------------------------------------------------------------
#  File:        normal.py
#  Module:      Normal
#  Description: Módulo para generar el mapa normal.
#
#  Author:      Mauricio José Tobares
#  Created:     15/12/2024
#  Copyright:   (c) 2024 Mauricio José Tobares
#  License:     MIT License
# ----------------------------------------------------------------------------

from PIL import Image, ImageEnhance

def generate_normal_map(height_map: Image.Image, normal_intensity: float) -> Image.Image:
    """
    Genera un mapa normal basado en los gradientes del mapa de altura.

    Este mapa normal se calcula manualmente a partir de las diferencias de altura
    en el mapa de altura dado. Los valores de los normales se convierten al rango RGB (0-255).

    Args:
        height_map (PIL.Image.Image): El mapa de altura de entrada.
        normal_intensity (float): La intensidad del contraste a aplicar al mapa normal (0-100).

    Returns:
        PIL.Image.Image: El mapa normal generado.
    """
    width, height = height_map.size

    # Crear una imagen en blanco para almacenar el resultado
    normal_map = Image.new("RGB", (width, height), color="black")
    pixels = normal_map.load()

    # Obtener los pixeles del mapa altura
    height_pixels = height_map.load()

    # Calcular los gradientes y normales manualmente
    for y in range(height):
        for x in range(width):
            # Obtener altura actual y vecina
            h_center = height_pixels[x,y]

            h_left = height_pixels[x - 1, y] if x > 0 else h_center
            h_right = height_pixels[x + 1, y] if x < width - 1 else h_center
            h_top = height_pixels[x, y - 1] if y > 0 else h_center
            h_bottom = height_pixels[x, y + 1] if y < height - 1 else h_center

            # Gradientes
            gx = h_right - h_left
            gy = h_bottom - h_top

            # Vector normal
            normal_x = -gx
            normal_y = -gy
            normal_z = 1

            # Normalización
            magnitude = (normal_x ** 2 + normal_y ** 2 + normal_z ** 2) ** 0.5

            if magnitude != 0:
               normal_x /= magnitude
               normal_y /= magnitude
               normal_z /= magnitude

            # Convertir a RGB (0-255)
            normal_x = int((normal_x * 0.5 + 0.5) * 255)
            normal_y = int((normal_y * 0.5 + 0.5) * 255)
            normal_z = int((normal_z * 0.5 + 0.5) * 255)

            # Mapear los valores al rango 0-255
            pixels[x,y] = (normal_x, normal_y, normal_z)

    # Ajustar intensidad usando contraste
    enhancer = ImageEnhance.Contrast(normal_map)
    normal_map = enhancer.enhance(normal_intensity * 0.1) # Se multiplica el porcentaje por un valor para conseguir más contraste

    return normal_map
