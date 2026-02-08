import asyncio
import os
import requests
import geopandas as gpd
from io import BytesIO
from typing import Callable

# Configuración de URLs de Catastro (INSPIRE)
WFS_PARCELAS_URL = "https://ovc.catastro.meh.es/insivict/wfs-inspire/v/cp/CadastralParcels/wfs"

async def run_cadastral_processing(reference: str, log_callback: Callable, output_dir: str = "outputs"):
    """
    Descarga y procesa datos catastrales reales usando el servicio WFS de INSPIRE.
    """
    try:
        await log_callback(f"Solicitando datos WFS para ref: {reference}...", "info")
        
        # Parámetros para la consulta WFS (GET)
        # Filtro por referencia catastral (nationalCadastralReference)
        params = {
            "service": "WFS",
            "version": "2.0.0",
            "request": "GetFeature",
            "typenames": "cp:CadastralParcel",
            "outputFormat": "application/gml+xml; version=3.2",
            "filter": f"""<fes:Filter xmlns:fes="http://www.opengis.net/fes/2.0" xmlns:cp="http://inspire.ec.europa.eu/schemas/cp/4.0">
                <fes:PropertyIsEqualTo>
                    <fes:ValueReference>cp:nationalCadastralReference</fes:ValueReference>
                    <fes:Literal>{reference}</fes:Literal>
                </fes:PropertyIsEqualTo>
            </fes:Filter>"""
        }

        # Ejecutamos la petición de forma asíncrona para no bloquear el backend
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: requests.get(WFS_PARCELAS_URL, params=params, timeout=30)
        )

        if response.status_code != 200:
            await log_callback(f"Error HTTP {response.status_code} al contactar con Catastro.", "error")
            return False

        if "Exception" in response.text:
            await log_callback(f"El servicio de Catastro devolvió una excepción.", "error")
            return False

        await log_callback(f"Datos GML recibidos correctamente.", "success")

        # Intentamos leer el GML con GeoPandas para validarlo y reproyectarlo si es necesario
        try:
            # Convertimos el contenido en un archivo en memoria
            gml_file = BytesIO(response.content)
            
            # Cargar en GeoDataFrame
            await log_callback(f"Analizando geometría con GeoPandas...", "info")
            gdf = await loop.run_in_executor(
                None,
                lambda: gpd.read_file(gml_file)
            )

            if gdf.empty:
                await log_callback(f"No se encontró información para la referencia {reference}.", "warning")
                return False

            # Mostrar información básica de la parcela
            area = gdf.geometry.area.iloc[0] if not gdf.empty else 0
            await log_callback(f"Parcela validada. Área aproximada: {area:.2f} m²", "info")

            # Simulación de guardado de archivos (GML local)
            # En un entorno real guardaríamos esto en un volumen montado o S3
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            output_path = f"{output_dir}/{reference}.gml"
            await log_callback(f"Guardando archivo GML en disco...", "info")
            with open(output_path, "wb") as f:
                f.write(response.content)

            await log_callback(f"Archivo {reference}.gml guardado exitosamente.", "success")
            
            return True

        except Exception as e:
            await log_callback(f"Error al procesar el archivo GML: {str(e)}", "error")
            return False

    except Exception as e:
        await log_callback(f"Fallo crítico en el proceso: {str(e)}", "error")
        return False
