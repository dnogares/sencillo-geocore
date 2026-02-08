import asyncio
import os
import glob
import requests
import geopandas as gpd
from io import BytesIO
from typing import Callable

# Configuración de URLs de Catastro (INSPIRE)
WFS_PARCELAS_URL = "https://ovc.catastro.meh.es/insivict/wfs-inspire/v/cp/CadastralParcels/wfs"

async def check_intersections_gpkg(parcel_gdf, fuentes_dir, log_callback):
    """
    Busca archivos .gpkg en fuentes_dir/CAPAS_gpkg (recursivo) y comprueba intersecciones.
    """
    capas_root = os.path.join(fuentes_dir, "CAPAS_gpkg")
    if not os.path.exists(capas_root):
        await log_callback(f"No se encuentra el directorio de capas: {capas_root}", "warning")
        return

    # Buscar recursivamente todos los .gpkg
    await log_callback(f"Buscando capas en {capas_root}...", "info")
    gpkg_files = glob.glob(os.path.join(capas_root, "**/*.gpkg"), recursive=True)
    
    if not gpkg_files:
        await log_callback(f"No se encontraron archivos .gpkg en {capas_root}", "warning")
        return

    await log_callback(f"Se encontraron {len(gpkg_files)} archivos de capas. Iniciando análisis espacial...", "info")

    loop = asyncio.get_event_loop()

    for gpkg_path in gpkg_files:
        filename = os.path.basename(gpkg_path)
        relative_path = os.path.relpath(gpkg_path, capas_root)
        
        try:
            # Leer la capa en un executor para no bloquear
            # Leemos solo la geometría para ir rápido, o verificamos intersección con bbox primero si es posible
            # Por simplicidad, leemos el archivo (cuidado con archivos muy grandes)
            
            # TODO: Para archivos muy grandes, usar bbox filter si es posible o leer solo metadata primero
            # Aquí asumimos archivos razonables para el ejemplo
            
            layer_gdf = await loop.run_in_executor(None, lambda: gpd.read_file(gpkg_path))
            
            if layer_gdf.empty:
                continue

            # Asegurar CRS coincidente
            if layer_gdf.crs != parcel_gdf.crs:
                # Reproyectar la parcela (es una sola geometría, es rápido) al CRS de la capa
                parcel_reprojected = parcel_gdf.to_crs(layer_gdf.crs)
            else:
                parcel_reprojected = parcel_gdf

            # Verificar intersección
            # overlay es costoso, intersects es más rápido para true/false
            # Usamos sjoin o intersects. 
            # intersects devuelve una serie booleana
            intersection = await loop.run_in_executor(
                None, 
                lambda: layer_gdf.intersects(parcel_reprojected.geometry.iloc[0])
            )

            if intersection.any():
                # Obtener los registros que intersectan
                intersecting_features = layer_gdf[intersection]
                count = len(intersecting_features)
                await log_callback(f"⚡ INTERSECCIÓN DETECTADA en {relative_path}: {count} elementos.", "success")
                
                # Opcional: Mostrar algún atributo identificativo si existe (ej. 'rotulo', 'nombre', 'id')
                # cols = intersecting_features.columns
                # first_match = intersecting_features.iloc[0]
                # await log_callback(f"  > Detalle: {first_match.to_dict()}", "info")
            else:
                # await log_callback(f"Sin intersecciones en {filename}.", "info")
                pass

        except Exception as e:
            await log_callback(f"Error analizando capa {filename}: {str(e)}", "error")

async def run_cadastral_processing(reference: str, log_callback: Callable, output_dir: str = "outputs", fuentes_dir: str = "FUENTES"):
    """
    Descarga y procesa datos catastrales reales usando el servicio WFS de INSPIRE.
    """
    try:
        if not os.path.exists(fuentes_dir):
            await log_callback(f"ADVERTENCIA: Directorio de fuentes no encontrado en {fuentes_dir}", "warning")
        else:
            await log_callback(f"Directorio de fuentes detectado correctamente.", "info")

        await log_callback(f"Procesando referencia catastral: {reference}", "info")
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

            # --- NUEVO: Comprobar intersecciones con capas locales ---
            await check_intersections_gpkg(gdf, fuentes_dir, log_callback)
            # ---------------------------------------------------------

            # Simulación de guardado de archivos (GML local)
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
