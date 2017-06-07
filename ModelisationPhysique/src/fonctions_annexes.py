RAPPORT_PIXEL_METTRES = 75

def convertirMetresPixels(mesure):
    return mesure * RAPPORT_PIXEL_METTRES

def convertirSurfacePixelsSurfaceMetres(surface):
    return surface / RAPPORT_PIXEL_METTRES**2
