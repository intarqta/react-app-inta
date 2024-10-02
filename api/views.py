import os
import ee
from django.http import JsonResponse
from google.oauth2 import service_account
from django.shortcuts import render
from pathlib import Path

# Obtener la ruta del directorio actual
directorio_actual = Path.cwd()

# Establecer la ruta relativa
ruta_relativa = directorio_actual.parent / 'key.json'
def initialize_earth_engine():
    service_account = 'api-monitoreo-forrajero@proyec2020.iam.gserviceaccount.com'
    credentials = ee.ServiceAccountCredentials(service_account, str(ruta_relativa))
    ee.Initialize(credentials)

def get_ndvi_map(request):
    initialize_earth_engine()

    # Define la región y el tiempo
    geometry = ee.Geometry.Polygon(
        [[[-60.21717442782064, -29.586786459767556],
          [-60.223697560144856, -29.625740558910287],
          [-60.16035451204915, -29.636483868430226],
          [-60.15486134798665, -29.591413979324752]]])  # Cambia a tu área de interés
    start_date = '2024-01-01'
    end_date = '2024-10-31'

    # Cargar la imagen de Landsat 8
    image = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
        .filterBounds(geometry) \
        .filterMetadata('CLOUDY_PIXEL_PERCENTAGE','less_than',10)\
        .filterDate(start_date, end_date) \
        .mean() \
        .select(['B8', 'B4'])\
        .clip(geometry)  # B5: NIR, B4: Red

    # Calcular NDVI
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')

    # Obtener la URL de la imagen
    ndvi_url = ndvi.getThumbUrl({'min': -1, 'max': 1, 'palette': ['blue', 'white', 'green']})

    print()

    return JsonResponse({'ndvi_url': ndvi_url})

def index(request):
    return render(request, 'index.html')