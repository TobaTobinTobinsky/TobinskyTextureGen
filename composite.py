# ----------------------------------------------------------------------------
#  File:        composite.py
#  Module:      Composite
#  Description: Módulo para crear la imagen compuesta final.
#
#  Author:      Mauricio José Tobares
#  Created:     15/12/2024
#  Copyright:   (c) 2024 Mauricio José Tobares
#  License:     MIT License
# ----------------------------------------------------------------------------

from PIL import Image, ImageEnhance
from typing import Optional

def create_composite_image(diffuse_image: Image.Image, height_map: Image.Image, normal_map: Image.Image,
                           metallic_map: Image.Image, smoothness_map: Image.Image, edge_map: Image.Image,
                           ao_map: Image.Image, resolution: Optional[int] = None, light_intensity: float = 1.0) -> Optional[Image.Image]:
    """
    Crea una imagen compuesta combinando todos los mapas de texturas.

    Este método toma como entrada los mapas de texturas generados (diffuse, altura, normal,
    metálico, suavidad, bordes y AO), los ajusta a una resolución única y combina los mapas
    utilizando la función Image.blend de Pillow. También permite ajustar la intensidad de la luz
    a la composición final.

    Args:
        diffuse_image (PIL.Image.Image): La imagen diffuse.
        height_map (PIL.Image.Image): El mapa de altura.
        normal_map (PIL.Image.Image): El mapa normal.
        metallic_map (PIL.Image.Image): El mapa metálico.
        smoothness_map (PIL.Image.Image): El mapa de suavidad.
        edge_map (PIL.Image.Image): El mapa de bordes.
        ao_map (PIL.Image.Image): El mapa de oclusión ambiental.
        resolution (int, optional): La resolución objetivo para todos los mapas. Si es None, usa el ancho de la imagen diffuse. Defaults to None.
        light_intensity (float): La intensidad de la luz a aplicar a la composición final (0.0-1.0). Defaults to 1.0.

    Returns:
        PIL.Image.Image or None: La imagen compuesta resultante o None si hay un error.
    """

    if not all([diffuse_image, height_map, normal_map, metallic_map, smoothness_map, edge_map, ao_map]):
        print("Error: Falta uno o más mapas de texturas.")
        return None  # Retorna None si falta algun mapa

    # Determinar la resolución de referencia
    if resolution is None:
        resolution = diffuse_image.size[0]  # Usar el ancho de diffuse_image como referencia
    width, height = resolution, resolution
    print(f"Resolución objetivo: {width}x{height}")

    # Función para redimensionar y ajustar el modo de color
    def ensure_resolution_and_mode(image: Image.Image, name: str) -> Image.Image:
        """
        Asegura que una imagen tenga la resolución y el modo de color correctos.

        Args:
            image (PIL.Image.Image): La imagen a procesar.
            name (str): El nombre de la imagen para mensajes de log.

        Returns:
            PIL.Image.Image: La imagen procesada.
        """
        # Convertir a RGB si no está en ese modo
        if image.mode != 'RGB':
            print(f"Convirtiendo {name} de modo {image.mode} a RGB")
            image = image.convert('RGB')
        # Redimensionar si las dimensiones no coinciden
        if image.size != (width, height):
            print(f"Redimensionando {name} de {image.size} a ({width}, {height})")
            image = image.resize((width, height), Image.Resampling.LANCZOS)
        else:
            print(f"{name} ya tiene la resolución correcta: {image.size}")
        return image

    # Ajustar todas las imágenes
    diffuse_image = ensure_resolution_and_mode(diffuse_image, "Diffuse")
    height_map = ensure_resolution_and_mode(height_map, "Height")
    normal_map = ensure_resolution_and_mode(normal_map, "Normal")
    metallic_map = ensure_resolution_and_mode(metallic_map, "Metallic")
    smoothness_map = ensure_resolution_and_mode(smoothness_map, "Smoothness")
    edge_map = ensure_resolution_and_mode(edge_map, "Edge")
    ao_map = ensure_resolution_and_mode(ao_map, "AO")

    # Sobreponer los mapas de textura
    composite_image = Image.new('RGB', (width, height), color=(0,0,0))
    print("Iniciando blending con Diffuse...")
    composite_image = Image.blend(composite_image, diffuse_image, 0.75)
    print("Blending con Diffuse completado.")

    print("Iniciando blending con Normal...")
    composite_image = Image.blend(composite_image, normal_map, 0.35)
    print("Blending con Normal completado.")

    print("Iniciando blending con Edge...")
    composite_image = Image.blend(composite_image, edge_map, 0.35)
    print("Blending con Edge completado.")

    print("Iniciando blending con AO...")
    composite_image = Image.blend(composite_image, ao_map, 0.35)
    print("Blending con AO completado.")

     # Ajustar la intensidad de la imagen usando brillo
    enhancer = ImageEnhance.Brightness(composite_image)
    composite_image = enhancer.enhance(light_intensity * 2) # Ajustamos el brillo por un factor

    return composite_image
