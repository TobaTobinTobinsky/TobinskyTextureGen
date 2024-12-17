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

def create_composite_image(diffuse_image, height_map, normal_map, metallic_map, smoothness_map, edge_map, ao_map, resolution=None, light_intensity=1.0):
    """Crea una imagen compuesta combinando todos los mapas de texturas, ajustándolos a una resolución única y garantizando modos de color compatibles."""

    if not all([diffuse_image, height_map, normal_map, metallic_map, smoothness_map, edge_map, ao_map]):
        print("Error: Falta uno o más mapas de texturas.")
        return None  # Retorna None si falta algun mapa

    # Determinar la resolución de referencia
    if resolution is None:
        resolution = diffuse_image.size[0]  # Usar el ancho de diffuse_image como referencia
    width, height = resolution, resolution
    print(f"Resolución objetivo: {width}x{height}")

    # Función para redimensionar y ajustar el modo de color
    def ensure_resolution_and_mode(image, name):
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
    composite_image = enhancer.enhance(light_intensity)

    return composite_image