# ----------------------------------------------------------------------------
#  File:        ao.py
#  Module:      AO
#  Description: Módulo para generar el mapa de oclusión ambiental (AO).
#
#  Author:      Mauricio José Tobares
#  Created:     15/12/2024
#  Copyright:   (c) 2024 Mauricio José Tobares
#  License:     MIT License
# ----------------------------------------------------------------------------

from PIL import Image, ImageEnhance

def generate_ao_map(diffuse_image: Image.Image, ao_intensity: float) -> Image.Image:
    """
    Genera un mapa de oclusión ambiental donde todo es blanco (puede ajustarse) en formato RGB.

    Este mapa se utiliza para simular sombras de oclusión ambiental, que indican qué tan expuesta
    está una superficie a la iluminación ambiente. Por defecto, genera una imagen completamente
    blanca que puede ser ajustada en intensidad.

    Args:
        diffuse_image (PIL.Image.Image): La imagen diffuse de entrada (utilizada solo para obtener las dimensiones).
        ao_intensity (float): La intensidad del brillo a aplicar al mapa de oclusión ambiental (0-100).

    Returns:
        PIL.Image.Image: El mapa de oclusión ambiental generado.
    """
    width, height = diffuse_image.size
    # Crear una imagen completamente blanca
    ao_map = Image.new('RGB', (width, height), color=(255, 255, 255))

    # Ajustar intensidad usando brillo
    enhancer = ImageEnhance.Brightness(ao_map)
    ao_map = enhancer.enhance(ao_intensity * 0.01)  # Se multiplica el porcentaje por un valor para conseguir más brillo

    return ao_map
