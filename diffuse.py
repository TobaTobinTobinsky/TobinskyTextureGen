# ----------------------------------------------------------------------------
#  File:        diffuse.py
#  Module:      Diffuse
#  Description: Módulo para procesar la imagen diffuse.
#
#  Author:      Mauricio José Tobares
#  Created:     15/12/2024
#  Copyright:   (c) 2024 Mauricio José Tobares
#  License:     MIT License
# ----------------------------------------------------------------------------

from PIL import Image

def process_diffuse(diffuse_image: Image.Image) -> Image.Image:
    """
    Procesa la imagen diffuse (en este caso, no se hace ninguna modificación).

    Esta función sirve como un punto de entrada para el procesamiento de la imagen diffuse,
    aunque en su implementación actual no realiza ninguna modificación.
    Se mantiene para posibles futuras expansiones o ajustes en el procesamiento de la imagen.

    Args:
        diffuse_image (PIL.Image.Image): La imagen diffuse de entrada.

    Returns:
        PIL.Image.Image: La misma imagen diffuse de entrada (sin modificaciones).
    """
    # En este caso, no se realiza ninguna modificación a la imagen
    return diffuse_image
