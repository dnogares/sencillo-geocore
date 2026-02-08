"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ORQUESTADOR PIPELINE GIS CATASTRAL                        ║
║                          Scripts 1-19 Integrados                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

FLUJO DEL PIPELINE (19 PASOS):

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 1: ADQUISICIÓN DE DATOS (Pasos 1-3)                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Paso 1: Leer referencias catastrales desde archivo .txt                   │
│ • Paso 2: Descargar XML desde servicio INSPIRE de Catastro                  │
│ • Paso 3: Descargar PDF (Croquis y Datos Gráficos) desde Catastro           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 2: GENERACIÓN VECTORIAL (Pasos 4-5)                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Paso 4: Generar archivos KML (individuales + MAPA_MAESTRO_TOTAL.kml)      │
│ • Paso 5: Generar siluetas PNG (individuales + CONJUNTO_TOTAL.png)          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 3: EXPORTACIÓN TABULAR (Paso 6)                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Paso 6: Crear tablas Excel y CSV con datos catastrales                    │
│           (superficie, coordenadas, polígono, parcela)                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 4: DOCUMENTACIÓN (Paso 7)                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Paso 7: Generar log.txt con resumen del expediente                        │
│           (fecha, referencias procesadas, superficies totales)               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 5: ANÁLISIS ESPACIAL (Paso 8)                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Paso 8: Analizar afecciones con capas GPKG locales                        │
│           (intersecciones, porcentajes, mapas de afecciones)                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 6: PLANOS DE EMPLAZAMIENTO BÁSICOS (Pasos 9-10)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Paso 9:  PLANO-EMPLAZAMIENTO.jpg (OpenStreetMap)                          │
│ • Paso 10: PLANO-EMPLAZAMIENTO-ORTO.jpg (Ortofoto Esri)                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 7: PLANOS CATASTRALES (Paso 11)                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Paso 11: PLANO-CATASTRAL-map.jpg                                          │
│            (WMS Catastro, encuadre 1000m)                                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 8: PLANOS IGN DETALLADOS (Paso 12)                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Paso 12a: PLANO-IGN-V1.jpg (margen 500m, zoom 16)                         │
│ • Paso 12b: PLANO-IGN-V2.jpg (margen 3000m, zoom 16)                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 9: PLANOS DE LOCALIZACIÓN PROVINCIAL (Paso 13)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Paso 13a: PLANO-PROVINCIAL-V1-STREETS.jpg (ArcGIS Streets)                │
│ • Paso 13b: PLANO-PROVINCIAL-V1-TOPO.jpg (ArcGIS Topo)                      │
│ • Paso 13c: PLANO-PROVINCIAL-V1-OSM.jpg (OpenStreetMap)                     │
│            (Encuadre 100km, zoom 10, con chincheta de ubicación)            │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 10: PLANOS CARTOGRÁFICOS HISTÓRICOS (Paso 14)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Paso 14a: PLANO-MTN25.jpg (Mapa Topográfico Nacional 1:25.000)            │
│ • Paso 14b: PLANO-MTN50.jpg (Mapa Topográfico Nacional 1:50.000)            │
│ • Paso 14c: PLANO-CATASTRONES.jpg (Catastro histórico)                      │
│            (WMS IGN primera edición, encuadre 5km)                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 11: PLANOS TEMÁTICOS AMBIENTALES (Pasos 16-17)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Paso 16: PLANO-PENDIENTES-LEYENDA.jpg                                     │
│            (Mapa de pendientes con leyenda superpuesta)                      │
│ • Paso 17: PLANO-NATURA-2000.jpg                                            │
│            (Red Natura 2000 sobre ortofoto PNOA con leyenda)                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FASE 12: PLANOS DE PROTECCIÓN AMBIENTAL (Pasos 18-19) 🆕                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Paso 18: PLANO-MONTES-PUBLICOS.jpg                                        │
│            (Catálogo de Montes de Utilidad Pública - IEPF/CMUP)             │
│            WFS del MITECO con polígonos oficiales + leyenda                 │
│ • Paso 19: PLANO-VIAS-PECUARIAS.jpg                                         │
│            (Red de Vías Pecuarias desde GPKG local RGVP2024)                │
│            Cañadas, Cordeles, Veredas clasificadas por tipo                 │
└─────────────────────────────────────────────────────────────────────────────┘

ESTRUCTURA DE OUTPUTS GENERADOS:
────────────────────────────────
OUTPUTS/
└── [nombre-archivo]-[timestamp]/
    ├── [RC]_INSPIRE.xml              ← XML con geometría INSPIRE
    ├── [RC]_CDyG.pdf                 ← PDF Croquis y Datos Gráficos
    ├── [RC].kml                      ← KML individual
    ├── [RC]_silueta.png              ← Silueta PNG individual
    ├── MAPA_MAESTRO_TOTAL.kml        ← KML con todas las parcelas
    ├── CONJUNTO_TOTAL.png            ← Siluetas combinadas
    ├── DATOS_CATASTRALES.xlsx        ← Tabla Excel con datos
    ├── DATOS_CATASTRALES.csv         ← Tabla CSV con datos
    ├── log.txt                       ← Resumen del expediente
    ├── afecciones_resultados.xlsx    ← Análisis de afecciones
    ├── mapa_[capa].png               ← Mapas de afecciones
    ├── PLANO-EMPLAZAMIENTO.jpg       ← Plano OSM
    ├── PLANO-EMPLAZAMIENTO-ORTO.jpg  ← Plano ortofoto
    ├── PLANO-CATASTRAL-map.jpg       ← Plano catastral
    ├── PLANO-IGN-V1.jpg              ← IGN cercano
    ├── PLANO-IGN-V2.jpg              ← IGN alejado
    ├── PLANO-PROVINCIAL-V1-*.jpg     ← 3 variantes provinciales
    ├── PLANO-MTN25.jpg               ← Histórico MTN 1:25.000
    ├── PLANO-MTN50.jpg               ← Histórico MTN 1:50.000
    ├── PLANO-CATASTRONES.jpg         ← Histórico catastrones
    ├── PLANO-PENDIENTES-LEYENDA.jpg  ← Pendientes
    ├── PLANO-NATURA-2000.jpg         ← Red Natura 2000
    ├── PLANO-MONTES-PUBLICOS.jpg     ← Montes Públicos CMUP 🆕
    └── PLANO-VIAS-PECUARIAS.jpg      ← Vías Pecuarias 🆕

"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Optional
import csv
import tempfile
import warnings

import matplotlib.pyplot as plt
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import geopandas as gpd
import contextily as cx
import fiona
from PIL import Image
from io import BytesIO
from shapely.geometry import box

# Ignorar advertencias de geometrías medidas (M) para limpiar la consola
warnings.filterwarnings("ignore", category=UserWarning)

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN GLOBAL
# ═══════════════════════════════════════════════════════════════════════════

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0"
)

# Habilitar soporte para archivos KML en Fiona
if 'KML' not in fiona.supported_drivers:
    fiona.drvsupport.supported_drivers['KML'] = 'rw'

# ═══════════════════════════════════════════════════════════════════════════
# CLASE DE DATOS: PARCELA
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ParcelaData:
    """
    Representa una parcela catastral con toda su información asociada.
    
    Attributes:
        refcat: Referencia catastral (identificador único)
        provincia: Código de provincia (primeros 2 dígitos de refcat)
        geometria: Lista de coordenadas (lon, lat) que definen el polígono
        info_catastral: Diccionario con m2, latitud, longitud
        recintos_sigpac: Lista de recintos SIGPAC asociados
        afecciones: Lista de afecciones detectadas
        rutas: Diccionario con rutas a archivos generados (xml, pdf, kml, png)
    """
    refcat: str
    provincia: str = field(init=False)
    geometria: List[Tuple[float, float]] = field(default_factory=list)
    info_catastral: dict = field(default_factory=dict)
    recintos_sigpac: List[dict] = field(default_factory=list)
    afecciones: List[dict] = field(default_factory=list)
    rutas: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Extrae automáticamente la provincia de la referencia catastral."""
        self.provincia = self.refcat[:2]

    @property
    def poligono(self) -> str:
        """Extrae el código de polígono (caracteres 7-9)."""
        return self.refcat[6:9]

    @property
    def parcela(self) -> str:
        """Extrae el código de parcela (caracteres 10-14)."""
        return self.refcat[9:14]

    def has_geometry(self) -> bool:
        """Verifica si la parcela tiene geometría cargada."""
        return bool(self.geometria)

    def actualizar_geometria(self, coords: List[Tuple[float, float]], superficie: float) -> None:
        """
        Actualiza la geometría y la información catastral de la parcela.
        
        Args:
            coords: Lista de tuplas (longitud, latitud)
            superficie: Superficie en metros cuadrados
        """
        self.geometria = coords
        if coords:
            self.info_catastral = {
                "m2": superficie,
                "latitud": coords[0][1],  # Primera coordenada como referencia
                "longitud": coords[0][0],
            }

    def registro_tabla(self) -> dict:
        """
        Genera un registro para exportación a tabla (Excel/CSV).
        
        Returns:
            Diccionario con campos: Referencia, Polígono, Parcela, m2, Ha, Latitud, Longitud
        """
        m2 = self.info_catastral.get("m2", 0)
        return {
            "Referencia": self.refcat,
            "Polígono": self.poligono,
            "Parcela": self.parcela,
            "m2": m2,
            "Ha": round(m2 / 10000, 4),
            "Latitud": self.info_catastral.get("latitud"),
            "Longitud": self.info_catastral.get("longitud"),
        }


# ═══════════════════════════════════════════════════════════════════════════
# CLASE PRINCIPAL: ORQUESTADOR DEL PIPELINE
# ═══════════════════════════════════════════════════════════════════════════

class OrquestadorPipeline:
    """
    Orquestador principal que ejecuta el pipeline completo de 19 pasos.
    
    El pipeline procesa referencias catastrales desde archivos .txt en INPUTS
    y genera todos los productos cartográficos en OUTPUTS.
    """
    
    def __init__(self, base_dir: Path) -> None:
        """
        Inicializa el orquestador y crea las carpetas necesarias.
        
        Args:
            base_dir: Directorio base del proyecto (donde están INPUTS y OUTPUTS)
        """
        self.base_dir = base_dir
        self.inputs = base_dir / "INPUTS"
        self.outputs = base_dir / "OUTPUTS"
        self.fuentes = base_dir / "FUENTES"
        self.carpeta_afecciones = self.fuentes / "CAPAS_gpkg" / "afecciones"
        
        # Sesión HTTP reutilizable para eficiencia
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
        
        # Crear estructura de directorios
        self.inputs.mkdir(parents=True, exist_ok=True)
        self.outputs.mkdir(parents=True, exist_ok=True)
        self.carpeta_afecciones.mkdir(parents=True, exist_ok=True)

    # ═══════════════════════════════════════════════════════════════════════
    # MÉTODO PRINCIPAL: EJECUTAR PIPELINE COMPLETO
    # ═══════════════════════════════════════════════════════════════════════

    def run(self) -> None:
        """
        Ejecuta el pipeline completo para todos los archivos .txt encontrados en INPUTS.
        
        Para cada archivo .txt:
            1. Lee las referencias catastrales
            2. Descarga datos (XML, PDF)
            3. Genera productos vectoriales (KML, PNG)
            4. Crea tablas de datos
            5. Genera log y análisis
            6. Produce todos los planos cartográficos (19 pasos en total)
        """
        archivos_txt = sorted(self.inputs.glob("*.txt"))
        
        if not archivos_txt:
            print(f"🔍 No hay archivos .txt en {self.inputs}. Añade una lista de RCs y vuelve a intentar.")
            return

        # Procesar cada archivo de texto
        for txt_path in archivos_txt:
            print(f"\n{'═'*80}")
            print(f"📄 PROCESANDO: {txt_path.name}")
            print(f"{'═'*80}\n")
            
            # PASO 1: Leer referencias catastrales
            referencias = self._leer_referencias(txt_path)
            if not referencias:
                print(f"⚠️ {txt_path.name} está vacío o no contiene RCs válidos.")
                continue

            print(f"✅ {len(referencias)} referencias catastrales leídas\n")
            
            # Crear carpeta de salida con timestamp
            carpeta = self._crear_subcarpeta(txt_path.stem)
            print(f"📁 Carpeta de salida: {carpeta.name}\n")
            
            # PASOS 2-3: Descargar y procesar datos catastrales
            print(f"{'─'*80}")
            print(f"FASE 1: ADQUISICIÓN DE DATOS")
            print(f"{'─'*80}")
            parcelas = self._procesar_referencias(referencias, carpeta)
            
            if not parcelas:
                print(f"⚠️ Ninguna referencia de {txt_path.name} pudo completarse.")
                continue

            print(f"\n✅ {len(parcelas)} parcelas procesadas correctamente\n")

            # FASE 2: GENERACIÓN VECTORIAL (Pasos 4-5)
            print(f"{'─'*80}")
            print(f"FASE 2: GENERACIÓN VECTORIAL")
            print(f"{'─'*80}")
            self._generar_kml(carpeta, parcelas)
            self._generar_png(carpeta, parcelas)
            
            # FASE 3: EXPORTACIÓN TABULAR (Paso 6)
            print(f"\n{'─'*80}")
            print(f"FASE 3: EXPORTACIÓN TABULAR")
            print(f"{'─'*80}")
            self._crear_tablas(carpeta, parcelas)
            
            # FASE 4: DOCUMENTACIÓN (Paso 7)
            print(f"\n{'─'*80}")
            print(f"FASE 4: DOCUMENTACIÓN")
            print(f"{'─'*80}")
            self._generar_log_expediente(carpeta, parcelas)
            
            # FASE 5: ANÁLISIS ESPACIAL (Paso 8)
            print(f"\n{'─'*80}")
            print(f"FASE 5: ANÁLISIS ESPACIAL")
            print(f"{'─'*80}")
            self._procesar_afecciones(carpeta)
            
            # FASE 6: PLANOS DE EMPLAZAMIENTO BÁSICOS (Pasos 9-10)
            print(f"\n{'─'*80}")
            print(f"FASE 6: PLANOS DE EMPLAZAMIENTO BÁSICOS")
            print(f"{'─'*80}")
            self._generar_plano_emplazamiento(carpeta)
            self._generar_plano_ortofoto(carpeta)
            
            # FASE 7: PLANOS CATASTRALES (Paso 11)
            print(f"\n{'─'*80}")
            print(f"FASE 7: PLANOS CATASTRALES")
            print(f"{'─'*80}")
            self._generar_plano_catastral(carpeta)
            
            # FASE 8: PLANOS IGN DETALLADOS (Paso 12)
            print(f"\n{'─'*80}")
            print(f"FASE 8: PLANOS IGN DETALLADOS")
            print(f"{'─'*80}")
            self._generar_planos_ign(carpeta)
            
            # FASE 9: PLANOS DE LOCALIZACIÓN PROVINCIAL (Paso 13)
            print(f"\n{'─'*80}")
            print(f"FASE 9: PLANOS DE LOCALIZACIÓN PROVINCIAL")
            print(f"{'─'*80}")
            self._generar_planos_provinciales(carpeta)
            
            # FASE 10: PLANOS CARTOGRÁFICOS HISTÓRICOS (Paso 14)
            print(f"\n{'─'*80}")
            print(f"FASE 10: PLANOS CARTOGRÁFICOS HISTÓRICOS")
            print(f"{'─'*80}")
            self._generar_planos_historicos(carpeta)
            
            # FASE 11: PLANOS TEMÁTICOS AMBIENTALES (Pasos 16-17)
            print(f"\n{'─'*80}")
            print(f"FASE 11: PLANOS TEMÁTICOS AMBIENTALES")
            print(f"{'─'*80}")
            self._generar_plano_pendientes(carpeta)
            self._generar_plano_natura2000(carpeta)
            
            # FASE 12: PLANOS DE PROTECCIÓN AMBIENTAL (Pasos 18-19) 🆕
            print(f"\n{'─'*80}")
            print(f"FASE 12: PLANOS DE PROTECCIÓN AMBIENTAL 🆕")
            print(f"{'─'*80}")
            self._generar_plano_montes_publicos(carpeta)
            self._generar_plano_vias_pecuarias(carpeta)
            
            print(f"\n{'═'*80}")
            print(f"✅ PIPELINE COMPLETO FINALIZADO: {txt_path.name}")
            print(f"{'═'*80}\n")

    # ═══════════════════════════════════════════════════════════════════════
    # PASO 1: LECTURA Y ORGANIZACIÓN
    # ═══════════════════════════════════════════════════════════════════════
    
    def _leer_referencias(self, ruta_txt: Path) -> List[str]:
        """
        Lee referencias catastrales desde un archivo de texto.
        
        Formato esperado: Una referencia catastral por línea (mínimo 14 caracteres).
        
        Args:
            ruta_txt: Ruta al archivo .txt con las referencias
            
        Returns:
            Lista de referencias catastrales en mayúsculas
        """
        referencias: List[str] = []
        with ruta_txt.open("r", encoding="utf-8") as handle:
            for linea in handle:
                texto = linea.strip().upper()
                if len(texto) >= 14:
                    referencias.append(texto)
        return referencias

    def _crear_subcarpeta(self, nombre_base: str) -> Path:
        """
        Crea una subcarpeta en OUTPUTS con timestamp para los resultados.
        
        Formato: [nombre_base]-[YYYYMMDD-HHMMSS]
        
        Args:
            nombre_base: Nombre base del archivo (sin extensión)
            
        Returns:
            Path de la carpeta creada
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        nombre = f"{nombre_base}-{timestamp}".replace(" ", "_")
        carpeta = self.outputs / nombre
        carpeta.mkdir(parents=True, exist_ok=True)
        return carpeta

    # ═══════════════════════════════════════════════════════════════════════
    # PASOS 2-3: ADQUISICIÓN (XML + PDF)
    # ═══════════════════════════════════════════════════════════════════════
    
    def _procesar_referencias(self, referencias: List[str], carpeta: Path) -> List[ParcelaData]:
        """
        Procesa cada referencia catastral: descarga XML y PDF, extrae geometría.
        
        Args:
            referencias: Lista de referencias catastrales
            carpeta: Carpeta donde guardar los archivos descargados
            
        Returns:
            Lista de ParcelaData con geometría válida
        """
        parcelas: List[ParcelaData] = []
        
        for i, rc in enumerate(referencias, 1):
            print(f"[{i}/{len(referencias)}] Procesando {rc}...", end=" ")
            
            parcela = ParcelaData(rc)
            xml_path = carpeta / f"{rc}_INSPIRE.xml"
            pdf_path = carpeta / f"{rc}_CDyG.pdf"

            # Descargar archivos
            self._descargar_xml(rc, xml_path)
            self._descargar_pdf(rc, pdf_path)

            # Extraer geometría del XML
            if xml_path.exists():
                superficie, coords = self._extraer_geometria(xml_path)
                if coords:
                    parcela.actualizar_geometria(coords, superficie)
                    parcela.rutas.update({
                        "xml": str(xml_path),
                        "pdf": str(pdf_path),
                    })
                    parcelas.append(parcela)
                    print(f"✅ OK ({superficie:,.0f} m²)")
                else:
                    print(f"⚠️ Sin geometría")
            else:
                print(f"❌ XML no disponible")
                
        return parcelas
    
    def _descargar_xml(self, rc: str, destino: Path) -> None:
        """
        Descarga el archivo XML INSPIRE desde el servicio WFS de Catastro.
        
        Args:
            rc: Referencia catastral
            destino: Ruta donde guardar el XML
        """
        if destino.exists():
            return  # No volver a descargar si ya existe
            
        url = (
            "https://ovc.catastro.meh.es/INSPIRE/wfsCP.aspx?service=WFS&vrsion=2.0.0"
            f"&request=GetFeature&STOREDQUERY_ID=GetParcel&refcat={rc}"
        )
        
        try:
            respuesta = self.session.get(url, timeout=20)
            respuesta.raise_for_status()
            destino.write_bytes(respuesta.content)
        except requests.RequestException as exc:
            print(f"❌ Error descargando XML {rc}: {exc}")

    def _descargar_pdf(self, rc: str, destino: Path) -> None:
        """
        Descarga el PDF de Croquis y Datos Gráficos desde Catastro.
        
        Args:
            rc: Referencia catastral
            destino: Ruta donde guardar el PDF
        """
        if destino.exists():
            return  # No volver a descargar si ya existe
            
        url = (
            "https://www1.sedecatastro.gob.es/CYCBienInmueble/SECImprimirCroquisYDatos.aspx"
            f"?del={rc[:2]}&mun={rc[2:5]}&refcat={rc}"
        )
        
        try:
            respuesta = self.session.get(url, timeout=20)
            respuesta.raise_for_status()
            # Verificar que el PDF tiene contenido válido (> 8KB)
            if len(respuesta.content) > 8000:
                destino.write_bytes(respuesta.content)
        except requests.RequestException as exc:
            print(f"❌ Error descargando PDF {rc}: {exc}")

    def _extraer_geometria(self, ruta_xml: Path) -> Tuple[float, List[Tuple[float, float]]]:
        """
        Extrae la superficie y las coordenadas del polígono desde el XML INSPIRE.
        
        Args:
            ruta_xml: Ruta al archivo XML
            
        Returns:
            Tupla (superficie_m2, lista_coordenadas)
            lista_coordenadas es una lista de tuplas (longitud, latitud)
        """
        superficie = 0.0
        coords: List[Tuple[float, float]] = []
        
        try:
            tree = ET.parse(str(ruta_xml))
            root = tree.getroot()
            
            # Namespaces del XML INSPIRE
            ns = {
                "cp": "http://inspire.ec.europa.eu/schemas/cp/4.0",
                "gml": "http://www.opengis.net/gml/3.2"
            }
            
            # Extraer superficie
            area_node = root.find(".//cp:areaValue", ns)
            if area_node is not None:
                superficie = float(area_node.text)
            
            # Extraer coordenadas (vienen como: lat1 lon1 lat2 lon2 ...)
            pos_list = root.find(".//gml:posList", ns)
            if pos_list is not None:
                raw = pos_list.text.split()
                for i in range(0, len(raw), 2):
                    lat = float(raw[i])
                    lon = float(raw[i + 1])
                    coords.append((lon, lat))  # Guardamos como (lon, lat)
                    
        except ET.ParseError as exc:
            print(f"❌ XML corrupto {ruta_xml.name}: {exc}")
        except (ValueError, IndexError):
            print(f"⚠️ Lista de coordenadas incompleta en {ruta_xml.name}.")
            
        return superficie, coords

    # ═══════════════════════════════════════════════════════════════════════
    # PASO 4: GENERACIÓN DE KML
    # ═══════════════════════════════════════════════════════════════════════
    
    def _generar_kml(self, carpeta: Path, parcelas: List[ParcelaData]) -> None:
        """
        Genera archivos KML individuales para cada parcela y un KML maestro.
        
        Archivos generados:
        - [RC].kml: KML individual de cada parcela
        - MAPA_MAESTRO_TOTAL.kml: KML con todas las parcelas juntas
        
        Args:
            carpeta: Carpeta donde guardar los KML
            parcelas: Lista de parcelas a procesar
        """
        elementos: List[str] = []
        
        for parcela in parcelas:
            if not parcela.has_geometry():
                continue
                
            # Crear Placemark KML para esta parcela
            bloque = self._crear_placemark(parcela)
            elementos.append(bloque)
            
            # Guardar KML individual
            archivo_kml = carpeta / f"{parcela.refcat}.kml"
            archivo_kml.write_text(self._envoltorio_kml(bloque), encoding="utf-8")
            parcela.rutas["kml"] = str(archivo_kml)
        
        # Crear KML maestro con todas las parcelas
        if elementos:
            maestro = carpeta / "MAPA_MAESTRO_TOTAL.kml"
            maestro.write_text(self._envoltorio_kml("".join(elementos)), encoding="utf-8")
            print(f"🗺️  KML maestro generado: {maestro.name}")

    @staticmethod
    def _crear_placemark(parcela: ParcelaData) -> str:
        """
        Crea un elemento Placemark KML para una parcela.
        
        Args:
            parcela: Datos de la parcela
            
        Returns:
            String XML con el Placemark
        """
        # Convertir coordenadas al formato KML: lon,lat,alt
        coords = " ".join(f"{lon},{lat},0" for lon, lat in parcela.geometria)
        
        return (
            f"<Placemark>"
            f"<name>{parcela.refcat}</name>"
            f"<description>m²: {parcela.info_catastral.get('m2', 0):,.0f}</description>"
            "<Style>"
            "<LineStyle><color>ff00ff00</color><width>2</width></LineStyle>"
            "<PolyStyle><color>4d00ff00</color></PolyStyle>"
            "</Style>"
            f"<Polygon><outerBoundaryIs><LinearRing>"
            f"<coordinates>{coords}</coordinates>"
            "</LinearRing></outerBoundaryIs></Polygon>"
            "</Placemark>"
        )

    @staticmethod
    def _envoltorio_kml(contenido: str) -> str:
        """
        Envuelve el contenido en la estructura XML de un archivo KML válido.
        
        Args:
            contenido: Contenido (uno o más Placemarks)
            
        Returns:
            String con el KML completo
        """
        return (
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
            "<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n"
            "<Document>\n"
            f"{contenido}\n"
            "</Document>\n"
            "</kml>"
        )

    # ═══════════════════════════════════════════════════════════════════════
    # PASO 5: GENERACIÓN DE PNG (SILUETAS)
    # ═══════════════════════════════════════════════════════════════════════
    
    def _generar_png(self, carpeta: Path, parcelas: List[ParcelaData]) -> None:
        """
        Genera siluetas PNG de las parcelas (individuales y conjunto).
        
        Archivos generados:
        - [RC]_silueta.png: Silueta individual de cada parcela
        - CONJUNTO_TOTAL.png: Todas las siluetas juntas
        
        Args:
            carpeta: Carpeta donde guardar los PNG
            parcelas: Lista de parcelas a dibujar
        """
        siluetas = []
        
        for parcela in parcelas:
            if not parcela.has_geometry():
                continue
                
            # Generar silueta individual
            ruta = carpeta / f"{parcela.refcat}_silueta.png"
            self._dibujar_parcelas([parcela.geometria], ruta, title=parcela.refcat)
            parcela.rutas["png"] = str(ruta)
            siluetas.append(parcela.geometria)
        
        # Generar silueta conjunta
        if siluetas:
            conjunto = carpeta / "CONJUNTO_TOTAL.png"
            self._dibujar_parcelas(siluetas, conjunto, title="Conjunto total", color="blue")
            print(f"🖼️  PNG conjunto generado: {conjunto.name}")

    @staticmethod
    def _dibujar_parcelas(
        lista_parcelas: List[List[Tuple[float, float]]],
        destino: Path,
        *,
        color: str = "red",
        title: str = ""
    ) -> None:
        """
        Dibuja una o más parcelas como siluetas PNG.
        
        Args:
            lista_parcelas: Lista de geometrías (cada una es una lista de coordenadas)
            destino: Ruta donde guardar el PNG
            color: Color de relleno y borde
            title: Título del gráfico
        """
        if not lista_parcelas:
            return
            
        fig, ax = plt.subplots(figsize=(6, 6))
        
        for coords in lista_parcelas:
            x, y = zip(*coords)
            ax.fill(x, y, color=color, alpha=0.3)
            ax.plot(x, y, color=color, linewidth=2)
        
        ax.axis("off")
        ax.set_aspect("equal", adjustable="box")
        
        if title:
            ax.set_title(title)
        
        fig.savefig(destino, transparent=True, bbox_inches="tight", pad_inches=0)
        plt.close(fig)

    # ═══════════════════════════════════════════════════════════════════════
    # PASO 6: CREAR TABLAS EXCEL/CSV
    # ═══════════════════════════════════════════════════════════════════════
    
    def _crear_tablas(self, carpeta: Path, parcelas: List[ParcelaData]) -> None:
        """
        Crea tablas Excel y CSV con los datos catastrales de las parcelas.
        
        Campos: Referencia, Polígono, Parcela, m2, Ha, Latitud, Longitud
        
        Archivos generados:
        - DATOS_CATASTRALES.xlsx
        - DATOS_CATASTRALES.csv (separador ;)
        
        Args:
            carpeta: Carpeta donde guardar las tablas
            parcelas: Lista de parcelas con datos
        """
        filas = [p.registro_tabla() for p in parcelas if p.info_catastral]
        
        if not filas:
            print("⚠️  No hay registros catastrales para exportar.")
            return
        
        df = pd.DataFrame(filas)
        excel = carpeta / "DATOS_CATASTRALES.xlsx"
        csv_path = carpeta / "DATOS_CATASTRALES.csv"
        
        df.to_excel(excel, index=False)
        df.to_csv(csv_path, sep=";", encoding="utf-8-sig", index=False)
        
        print(f"📊 Tablas generadas: {excel.name} / {csv_path.name}")

    # ═══════════════════════════════════════════════════════════════════════
    # PASO 7: GENERAR LOG DE EXPEDIENTE
    # ═══════════════════════════════════════════════════════════════════════
    
    def _generar_log_expediente(self, carpeta: Path, parcelas: List[ParcelaData]) -> None:
        """
        Genera archivo log.txt con resumen del expediente.
        
        Contenido:
        - Nombre del expediente
        - Fecha de proceso
        - Listado de referencias con superficies
        - Totales
        
        Args:
            carpeta: Carpeta donde guardar el log
            parcelas: Lista de parcelas procesadas
        """
        log_path = carpeta / "log.txt"
        
        with log_path.open("w", encoding="utf-8") as f:
            f.write(f"RESUMEN DE EXPEDIENTE: {carpeta.name}\n")
            f.write(f"FECHA DE PROCESO: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("-" * 50 + "\n\n")
            
            total_m2 = 0
            for parcela in parcelas:
                m2 = parcela.info_catastral.get("m2", 0)
                total_m2 += m2
                f.write(f"RC: {parcela.refcat} | Superficie: {m2:,.0f} m2 | ({m2/10000:.4f} Ha)\n")
            
            f.write("\n" + "-" * 50 + "\n")
            f.write(f"TOTAL PARCELAS: {len(parcelas)}\n")
            f.write(f"SUPERFICIE TOTAL: {total_m2:,.0f} m2 | ({total_m2/10000:.4f} Ha)\n")
        
        print(f"📝 Archivo log.txt generado con éxito.")

    # ═══════════════════════════════════════════════════════════════════════
    # PASO 8: ANÁLISIS DE AFECCIONES
    # ═══════════════════════════════════════════════════════════════════════
    
    def _procesar_afecciones(self, carpeta: Path) -> None:
        """
        Analiza las intersecciones de las parcelas con capas de afecciones (GPKG).
        
        Para cada capa GPKG en FUENTES/CAPAS_gpkg/afecciones:
        - Calcula el área de intersección
        - Calcula el porcentaje de afección
        - Genera un mapa visual de la afección
        
        Archivos generados:
        - afecciones_resultados.xlsx
        - afecciones_resultados.csv
        - mapa_[nombre_capa].png (uno por cada capa)
        
        Args:
            carpeta: Carpeta donde guardar los resultados
        """
        archivo_parcela = carpeta / "MAPA_MAESTRO_TOTAL.kml"
        
        if not archivo_parcela.exists():
            print(f"⚠️  Falta {archivo_parcela.name} para procesar afecciones.")
            return

        capas_locales = self._listar_capas_locales()
        
        if not capas_locales:
            print(f"ℹ️  No hay capas de afecciones en {self.carpeta_afecciones}")
            return
        
        resultados = []

        try:
            # Cargar KML de parcelas y proyectar a UTM 30N
            parcela_gdf = gpd.read_file(str(archivo_parcela), driver='KML')
            if parcela_gdf.crs is None:
                parcela_gdf.crs = "EPSG:4326"
            parcela_utm = parcela_gdf.to_crs(epsg=25830)
            area_total_m2 = parcela_utm.area.sum()

            # Procesar cada capa de afecciones
            for capa in capas_locales:
                print(f"🔍 Procesando capa: {capa['nombre']}...", end=" ")
                
                try:
                    # Cargar capa GPKG con filtro espacial (bbox)
                    capa_gdf = gpd.read_file(capa['ruta'], bbox=parcela_gdf).to_crs(epsg=25830)

                    if not capa_gdf.empty:
                        # Calcular intersección
                        interseccion = gpd.overlay(parcela_utm, capa_gdf, how='intersection')
                        area_afectada_m2 = interseccion.area.sum()
                    else:
                        area_afectada_m2 = 0

                    porcentaje = (area_afectada_m2 / area_total_m2) * 100 if area_total_m2 > 0 else 0
                    afecta_si_no = "SÍ" if area_afectada_m2 > 0.1 else "NO"

                    resultados.append({
                        'parcela': archivo_parcela.name,
                        'capa': capa['nombre'],
                        'afecta': afecta_si_no,
                        'superficie_m2': area_afectada_m2,
                        'superficie_ha': area_afectada_m2 / 10000,
                        'porcentaje': porcentaje
                    })

                    # Generar mapa visual de la afección
                    fig, ax = plt.subplots(figsize=(10, 10))
                    
                    # Dibujar parcela en rojo
                    parcela_gdf.to_crs(epsg=3857).plot(
                        ax=ax, facecolor="none", edgecolor="red", linewidth=2, zorder=10
                    )
                    
                    # Dibujar capa de afección en azul
                    if not capa_gdf.empty:
                        capa_gdf.to_crs(epsg=3857).plot(
                            ax=ax, color='blue', alpha=0.3, zorder=5
                        )
                    
                    # Añadir mapa base
                    cx.add_basemap(ax, source=cx.providers.OpenStreetMap.Mapnik)
                    
                    plt.title(f"Afección: {capa['nombre']}\nPorcentaje: {porcentaje:.2f}%", fontsize=12)
                    ax.set_axis_off()

                    nombre_mapa = f"mapa_{capa['nombre']}.png"
                    plt.savefig(carpeta / nombre_mapa, dpi=200, bbox_inches='tight')
                    plt.close()
                    
                    print(f"✅ {porcentaje:.1f}%")

                except Exception as e:
                    print(f"❌ Error: {e}")

            # Guardar resultados en Excel y CSV
            if resultados:
                df = pd.DataFrame(resultados)
                df.to_csv(carpeta / "afecciones_resultados.csv", index=False)
                df.to_excel(carpeta / "afecciones_resultados.xlsx", index=False)
                print(f"✅ Análisis de afecciones completado: {len(resultados)} capas procesadas.")

        except Exception as e:
            print(f"❌ No se pudo procesar afecciones: {e}")

    def _listar_capas_locales(self) -> List[dict]:
        """
        Busca archivos .gpkg en la carpeta de afecciones.
        
        Returns:
            Lista de diccionarios con 'nombre' y 'ruta' de cada capa
        """
        capas = []
        if self.carpeta_afecciones.exists():
            for archivo in self.carpeta_afecciones.glob("*.gpkg"):
                capas.append({
                    'nombre': archivo.stem,
                    'ruta': str(archivo)
                })
        return capas

    # ═══════════════════════════════════════════════════════════════════════
    # PASO 9: PLANO DE EMPLAZAMIENTO (MAPA BASE)
    # ═══════════════════════════════════════════════════════════════════════
    
    def _generar_plano_emplazamiento(self, carpeta: Path) -> None:
        """
        Genera plano de emplazamiento sobre mapa base OpenStreetMap.
        
        Características:
        - Formato 4:3 (12x9 pulgadas)
        - 300 DPI (alta resolución)
        - Margen 1.8x alrededor de las parcelas
        - Parcelas en rojo semi-transparente
        
        Archivo generado: PLANO-EMPLAZAMIENTO.jpg
        
        Args:
            carpeta: Carpeta donde guardar el plano
        """
        ruta_kml = carpeta / "MAPA_MAESTRO_TOTAL.kml"
        if not ruta_kml.exists():
            print(f"⚠️  No se encontró {ruta_kml.name}")
            return

        try:
            # Cargar KML
            gdf = gpd.read_file(str(ruta_kml), driver='KML')
            if gdf.empty:
                return
            if gdf.crs is None:
                gdf.crs = "EPSG:4326"
            
            # Configurar figura en formato 4:3
            fig, ax = plt.subplots(figsize=(12, 9))
            
            # Calcular límites con margen
            minx, miny, maxx, maxy = gdf.total_bounds
            centro_x, centro_y = (minx + maxx) / 2, (miny + maxy) / 2
            
            ancho_parcelas = (maxx - minx) * 1.8  # Margen 1.8x
            alto_parcelas = (maxy - miny) * 1.8
            
            # Ajustar para mantener proporción 4:3
            if ancho_parcelas / alto_parcelas > 4/3:
                alto_final = ancho_parcelas * (3/4)
                ancho_final = ancho_parcelas
            else:
                ancho_final = alto_parcelas * (4/3)
                alto_final = alto_parcelas
                
            ax.set_xlim(centro_x - ancho_final/2, centro_x + ancho_final/2)
            ax.set_ylim(centro_y - alto_final/2, centro_y + alto_final/2)

            # Dibujar parcelas en rojo
            gdf.plot(ax=ax, facecolor='red', alpha=0.3, edgecolor='darkred', linewidth=1.5, zorder=2)
            
            # Añadir mapa base OpenStreetMap
            cx.add_basemap(ax, crs=gdf.crs.to_string(), source=cx.providers.OpenStreetMap.Mapnik, zorder=1)
            
            ax.set_axis_off()
            
            ruta_jpg = carpeta / "PLANO-EMPLAZAMIENTO.jpg"
            plt.savefig(ruta_jpg, dpi=300, bbox_inches='tight', pad_inches=0)
            plt.close()
            print(f"✅ PLANO-EMPLAZAMIENTO.jpg generado (300 DPI)")
            
        except Exception as e:
            print(f"❌ Error al generar el plano: {e}")

    # ═══════════════════════════════════════════════════════════════════════
    # PASO 10: PLANO DE EMPLAZAMIENTO (ORTOFOTO)
    # ═══════════════════════════════════════════════════════════════════════
    
    def _generar_plano_ortofoto(self, carpeta: Path) -> None:
        """
        Genera plano de emplazamiento sobre ortofoto satelital Esri.
        
        Características:
        - Formato 4:3 (12x9 pulgadas)
        - 300 DPI (alta resolución)
        - Margen 1.8x alrededor de las parcelas
        - Parcelas en cian (resalta sobre la imagen)
        - Fondo: Esri WorldImagery
        
        Archivo generado: PLANO-EMPLAZAMIENTO-ORTO.jpg
        
        Args:
            carpeta: Carpeta donde guardar el plano
        """
        ruta_kml = carpeta / "MAPA_MAESTRO_TOTAL.kml"
        if not ruta_kml.exists():
            print(f"⚠️  No se encontró {ruta_kml.name}")
            return

        try:
            # Cargar KML
            gdf = gpd.read_file(str(ruta_kml), driver='KML')
            if gdf.empty:
                return
            if gdf.crs is None:
                gdf.crs = "EPSG:4326"
            
            # Configurar figura en formato 4:3
            fig, ax = plt.subplots(figsize=(12, 9))
            
            # Calcular límites con margen
            minx, miny, maxx, maxy = gdf.total_bounds
            centro_x, centro_y = (minx + maxx) / 2, (miny + maxy) / 2
            
            ancho_parcelas = (maxx - minx) * 1.8
            alto_parcelas = (maxy - miny) * 1.8
            
            # Ajustar para mantener proporción 4:3
            if ancho_parcelas / alto_parcelas > 4/3:
                alto_final = ancho_parcelas * (3/4)
                ancho_final = ancho_parcelas
            else:
                ancho_final = alto_parcelas * (4/3)
                alto_final = alto_parcelas
                
            ax.set_xlim(centro_x - ancho_final/2, centro_x + ancho_final/2)
            ax.set_ylim(centro_y - alto_final/2, centro_y + alto_final/2)

            # Dibujar parcelas en cian (solo borde, sin relleno)
            gdf.plot(ax=ax, facecolor='none', edgecolor='cyan', linewidth=2.5, zorder=2)
            
            # Añadir ortofoto Esri WorldImagery
            cx.add_basemap(ax, crs=gdf.crs.to_string(), source=cx.providers.Esri.WorldImagery, zorder=1)
            
            ax.set_axis_off()
            
            ruta_jpg = carpeta / "PLANO-EMPLAZAMIENTO-ORTO.jpg"
            plt.savefig(ruta_jpg, dpi=300, bbox_inches='tight', pad_inches=0)
            plt.close()
            print(f"✅ PLANO-EMPLAZAMIENTO-ORTO.jpg generado (300 DPI)")
            
        except Exception as e:
            print(f"❌ Error al generar la ortofoto: {e}")

    # ═══════════════════════════════════════════════════════════════════════
    # PASO 11: PLANO CATASTRAL (1000m)
    # ═══════════════════════════════════════════════════════════════════════
    
    def _generar_plano_catastral(self, carpeta: Path) -> None:
        """
        Genera plano catastral con encuadre fijo de 1000m usando WMS de Catastro.
        
        Características:
        - Encuadre cuadrado de 1000m x 1000m
        - Centrado en el centro geométrico de las parcelas
        - Proyección: EPSG:25830 (UTM 30N)
        - Parcelas en cian sobre la cartografía catastral
        
        Archivo generado: PLANO-CATASTRAL-map.jpg
        
        Args:
            carpeta: Carpeta donde guardar el plano
        """
        ruta_kml = carpeta / "MAPA_MAESTRO_TOTAL.kml"
        if not ruta_kml.exists():
            print(f"⚠️  No se encontró {ruta_kml.name}")
            return

        try:
            # Cargar y proyectar a UTM 30N
            gdf = gpd.read_file(str(ruta_kml), driver='KML').to_crs(epsg=25830)
            b = gdf.total_bounds
            
            # Calcular encuadre cuadrado de 1000m
            centro_x = (b[0] + b[2]) / 2
            centro_y = (b[1] + b[3]) / 2
            lado_cuadrado = 1000  # metros
            
            xmin = centro_x - (lado_cuadrado / 2)
            xmax = centro_x + (lado_cuadrado / 2)
            ymin = centro_y - (lado_cuadrado / 2)
            ymax = centro_y + (lado_cuadrado / 2)
            
            bbox_str = f"{xmin},{ymin},{xmax},{ymax}"
            
            print(f"🌍 Generando plano catastral (1000m)...", end=" ", flush=True)
            
            # Petición WMS al servidor de Catastro
            url = (
                f"https://ovc.catastro.meh.es/Cartografia/WMS/ServidorWMS.aspx?"
                f"SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS=CATASTRO"
                f"&SRS=EPSG:25830&BBOX={bbox_str}&WIDTH=1800&HEIGHT=1800&FORMAT=image/png"
            )
            
            r = self.session.get(url, timeout=30)
            if r.status_code == 200:
                img_mapa = Image.open(BytesIO(r.content))
                
                # Crear figura cuadrada
                fig = plt.figure(figsize=(10, 10))
                ax = fig.add_axes([0, 0, 1, 1])
                ax.imshow(img_mapa, extent=[xmin, xmax, ymin, ymax])
                
                # Dibujar parcelas en cian
                gdf.plot(ax=ax, facecolor='none', edgecolor='cyan', linewidth=1.5)
                
                ax.set_axis_off()
                ax.set_xlim(xmin, xmax)
                ax.set_ylim(ymin, ymax)
                
                # Guardar como JPEG
                buf = BytesIO()
                plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
                plt.close()
                buf.seek(0)
                final_img = Image.open(buf).convert('RGB')
                nombre_salida = carpeta / "PLANO-CATASTRAL-map.jpg"
                final_img.save(nombre_salida, "JPEG", quality=85, optimize=True)
                print(f"✅")
            else:
                print(f"❌ Error del servidor WMS")
        except Exception as e:
            print(f"❌ Error: {e}")

    # ═══════════════════════════════════════════════════════════════════════
    # PASO 12: PLANOS IGN (V1 y V2)
    # ═══════════════════════════════════════════════════════════════════════
    
    def _generar_planos_ign(self, carpeta: Path) -> None:
        """
        Genera planos IGN con zoom fijo 16 y dos variantes de encuadre.
        
        Variantes:
        - V1: Margen de 500m (vista cercana)
        - V2: Margen de 3000m (vista alejada, contexto)
        
        Características:
        - Formato 4:3 (12x9 pulgadas)
        - Zoom 16 fijo (máximo detalle de topónimos)
        - 150 DPI
        - Parcelas en cian
        - Fondo: Mapa Topográfico Nacional del IGN (WMTS)
        
        Archivos generados:
        - PLANO-IGN-V1.jpg
        - PLANO-IGN-V2.jpg
        
        Args:
            carpeta: Carpeta donde guardar los planos
        """
        ruta_kml = carpeta / "MAPA_MAESTRO_TOTAL.kml"
        if not ruta_kml.exists():
            print(f"⚠️  No se encontró {ruta_kml.name}")
            return

        try:
            # Cargar y proyectar a Web Mercator
            gdf = gpd.read_file(str(ruta_kml), driver='KML')
            if gdf.empty:
                return
            if gdf.crs is None:
                gdf.crs = "EPSG:4326"
            gdf_3857 = gdf.to_crs(epsg=3857)
            
            minx, miny, maxx, maxy = gdf_3857.total_bounds
            
            # URL del servicio WMTS del IGN
            ign_url = (
                "https://www.ign.es/wmts/mapa-raster?"
                "layer=MTN&style=default&tilematrixset=GoogleMapsCompatible"
                "&Service=WMTS&Request=GetTile&Version=1.0.0&Format=image/jpeg"
                "&TileMatrix={z}&TileCol={x}&TileRow={y}"
            )
            
            # Generar ambas variantes
            for margen, nombre in [(500, "PLANO-IGN-V1.jpg"), (3000, "PLANO-IGN-V2.jpg")]:
                print(f"🗺️  Generando {nombre} (margen {margen}m, zoom 16)...", end=" ", flush=True)
                
                fig, ax = plt.subplots(figsize=(12, 9))
                
                # Calcular límites con margen
                x_min, x_max = minx - margen, maxx + margen
                y_min, y_max = miny - margen, maxy + margen
                ancho, alto = x_max - x_min, y_max - y_min
                
                # Ajustar para mantener proporción 4:3
                if ancho / alto > 4/3:
                    alto_f = ancho * (3/4)
                    cy = (y_min + y_max) / 2
                    ax.set_ylim(cy - alto_f/2, cy + alto_f/2)
                    ax.set_xlim(x_min, x_max)
                else:
                    ancho_f = alto * (4/3)
                    cx_coord = (x_min + x_max) / 2
                    ax.set_xlim(cx_coord - ancho_f/2, cx_coord + ancho_f/2)
                    ax.set_ylim(y_min, y_max)
                
                # Añadir mapa IGN con zoom 16 fijo
                cx.add_basemap(ax, source=ign_url, zorder=1, zoom=16)
                
                # Dibujar parcelas en cian
                gdf_3857.plot(ax=ax, facecolor='none', edgecolor='cyan', linewidth=2, zorder=2)
                ax.set_axis_off()
                
                ruta_final = carpeta / nombre
                plt.savefig(ruta_final, dpi=150, bbox_inches='tight', pad_inches=0, pil_kwargs={'quality': 80})
                plt.close()
                print(f"✅")
        except Exception as e:
            print(f"❌ Error: {e}")

    # ═══════════════════════════════════════════════════════════════════════
    # PASO 13: PLANOS PROVINCIALES (3 variantes)
    # ═══════════════════════════════════════════════════════════════════════
    
    def _generar_planos_provinciales(self, carpeta: Path) -> None:
        """
        Genera planos de localización provincial con 3 estilos de mapa base.
        
        Variantes:
        - STREETS: ArcGIS World Street Map
        - TOPO: ArcGIS World Topo Map
        - OSM: OpenStreetMap Mapnik
        
        Características:
        - Encuadre de 100km (vista provincial completa)
        - Zoom 10 (óptimo para topónimos provinciales)
        - Formato 4:3 (12x9 pulgadas)
        - 120 DPI (suficiente para escala provincial)
        - Parcelas en cian con chincheta roja de ubicación
        
        Archivos generados:
        - PLANO-PROVINCIAL-V1-STREETS.jpg
        - PLANO-PROVINCIAL-V1-TOPO.jpg
        - PLANO-PROVINCIAL-V1-OSM.jpg
        
        Args:
            carpeta: Carpeta donde guardar los planos
        """
        ruta_kml = carpeta / "MAPA_MAESTRO_TOTAL.kml"
        if not ruta_kml.exists():
            print(f"⚠️  No se encontró {ruta_kml.name}")
            return

        try:
            # Cargar y proyectar
            gdf = gpd.read_file(str(ruta_kml), driver='KML')
            if gdf.empty:
                return
            gdf_3857 = gdf.to_crs(epsg=3857)
            minx, miny, maxx, maxy = gdf_3857.total_bounds
            centro_x, centro_y = (minx + maxx) / 2, (miny + maxy) / 2
            
            # Definir las 3 variantes de mapa base
            variantes = {
                "STREETS": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
                "TOPO": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
                "OSM": cx.providers.OpenStreetMap.Mapnik
            }
            
            for nombre, fuente in variantes.items():
                print(f"🗺️  Generando PLANO-PROVINCIAL-V1-{nombre}.jpg...", end=" ", flush=True)
                
                fig, ax = plt.subplots(figsize=(12, 9))
                
                # Encuadre de 100km
                ancho_vista = 100000  # metros
                alto_vista = ancho_vista * (3/4)  # Mantener 4:3
                
                ax.set_xlim(centro_x - ancho_vista/2, centro_x + ancho_vista/2)
                ax.set_ylim(centro_y - alto_vista/2, centro_y + alto_vista/2)
                
                # Añadir mapa base con zoom 10
                cx.add_basemap(ax, source=fuente, zoom=10, interpolation='lanczos', zorder=1)
                
                # Dibujar parcelas en cian (relleno y borde)
                gdf_3857.plot(ax=ax, color='cyan', edgecolor='cyan', linewidth=3, zorder=3)
                
                # Añadir chincheta roja en el centro
                ax.plot(centro_x, centro_y, marker='v', color='red', markersize=20, 
                        markeredgecolor='white', markeredgewidth=1.5, zorder=4)
                
                ax.set_axis_off()
                
                nombre_archivo = f"PLANO-PROVINCIAL-V1-{nombre}.jpg"
                ruta_final = carpeta / nombre_archivo
                plt.savefig(ruta_final, dpi=120, bbox_inches='tight', pad_inches=0, 
                           pil_kwargs={'quality': 85, 'optimize': True, 'progressive': True})
                plt.close()
                print(f"✅")
        except Exception as e:
            print(f"❌ Error provincial: {e}")

    # ═══════════════════════════════════════════════════════════════════════
    # PASO 14: PLANOS HISTÓRICOS (MTN25, MTN50, CATASTRONES)
    # ═══════════════════════════════════════════════════════════════════════
    
    def _generar_planos_historicos(self, carpeta: Path) -> None:
        """
        Genera planos con cartografía histórica del IGN.
        
        Capas:
        - MTN25: Mapa Topográfico Nacional 1:25.000 (primera edición)
        - MTN50: Mapa Topográfico Nacional 1:50.000 (primera edición)
        - CATASTRONES: Planos del Catastro histórico
        
        Características:
        - Encuadre de 5km alrededor de las parcelas
        - Formato 4:3 (12x9 pulgadas)
        - 150 DPI
        - Parcelas en cian con chincheta roja semi-transparente
        - Fuente: WMS del IGN (primera edición MTN)
        
        Archivos generados:
        - PLANO-MTN25.jpg
        - PLANO-MTN50.jpg
        - PLANO-CATASTRONES.jpg
        
        Args:
            carpeta: Carpeta donde guardar los planos
        """
        ruta_kml = carpeta / "MAPA_MAESTRO_TOTAL.kml"
        if not ruta_kml.exists():
            print(f"⚠️  No se encontró {ruta_kml.name}")
            return

        try:
            # Cargar y proyectar
            gdf = gpd.read_file(str(ruta_kml), driver='KML')
            if gdf.empty:
                return
            gdf_3857 = gdf.to_crs(epsg=3857)
            minx, miny, maxx, maxy = gdf_3857.total_bounds
            cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
            
            # Encuadre de 5km
            m = 5000
            bbox = [cx - m, cy - m * 0.75, cx + m, cy + m * 0.75]
            
            # Definir las 3 capas históricas
            capas = {
                "MTN25": "MTN25",
                "MTN50": "MTN50",
                "CATASTRONES": "catastrones"
            }
            
            url_wms = "https://www.ign.es/wms/primera-edicion-mtn"
            
            for nombre_file, id_capa in capas.items():
                print(f"🛰️  Capturando {nombre_file}...", end=" ", flush=True)
                
                # Parámetros de la petición WMS
                params = {
                    "SERVICE": "WMS",
                    "VERSION": "1.3.0",
                    "REQUEST": "GetMap",
                    "LAYERS": id_capa,
                    "STYLES": "",
                    "CRS": "EPSG:3857",
                    "BBOX": f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
                    "WIDTH": "1200",
                    "HEIGHT": "900",
                    "FORMAT": "image/jpeg",
                    "TRANSPARENT": "FALSE"
                }
                
                try:
                    response = self.session.get(url_wms, params=params, timeout=30)
                    if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
                        img = Image.open(BytesIO(response.content))
                        
                        fig, ax = plt.subplots(figsize=(12, 9))
                        ax.imshow(img, extent=[bbox[0], bbox[2], bbox[1], bbox[3]], interpolation='lanczos')
                        
                        # Dibujar parcelas en cian
                        gdf_3857.plot(ax=ax, facecolor='none', edgecolor='cyan', linewidth=1.5, zorder=10)
                        
                        # Añadir chincheta roja semi-transparente
                        ax.plot(cx, cy, marker='v', color='red', markersize=18, 
                                markeredgecolor='white', markeredgewidth=1.5, alpha=0.5, zorder=11)
                        
                        ax.set_xlim(bbox[0], bbox[2])
                        ax.set_ylim(bbox[1], bbox[3])
                        ax.set_axis_off()
                        
                        nombre_archivo = f"PLANO-{nombre_file}.jpg"
                        ruta_final = carpeta / nombre_archivo
                        plt.savefig(ruta_final, dpi=150, bbox_inches='tight', pad_inches=0, pil_kwargs={'quality': 90})
                        plt.close()
                        print(f"✅")
                    else:
                        print(f"❌ Error del servidor")
                except Exception as e:
                    print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Error crítico: {e}")

    # ═══════════════════════════════════════════════════════════════════════
    # PASO 16: PLANO DE PENDIENTES CON LEYENDA
    # ═══════════════════════════════════════════════════════════════════════
    
    def _generar_plano_pendientes(self, carpeta: Path) -> None:
        """
        Genera plano de pendientes del terreno con leyenda superpuesta.
        
        Características:
        - Encuadre de 500m alrededor de las parcelas (vista cercana)
        - Formato 4:3 (12x9 pulgadas)
        - 150 DPI
        - Parcelas en azul (#0000FF)
        - Chincheta en rojo (#CC0000) con transparencia
        - Leyenda superpuesta en la esquina inferior derecha
        - Fuente: WMS de Pendientes IDEE (capa MDP05)
        
        Archivo generado: PLANO-PENDIENTES-LEYENDA.jpg
        
        Args:
            carpeta: Carpeta donde guardar el plano
        """
        ruta_kml = carpeta / "MAPA_MAESTRO_TOTAL.kml"
        if not ruta_kml.exists():
            print(f"⚠️  No se encontró {ruta_kml.name}")
            return

        try:
            # Cargar y proyectar
            gdf = gpd.read_file(str(ruta_kml), driver='KML')
            if gdf.empty:
                return
            gdf_3857 = gdf.to_crs(epsg=3857)
            minx, miny, maxx, maxy = gdf_3857.total_bounds
            cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
            
            # Encuadre cercano de 500m
            m = 500
            bbox = [cx - m, cy - m * 0.75, cx + m, cy + m * 0.75]
            
            url_wms = "https://wms-pendientes.idee.es/pendientes"
            
            # Parámetros para el mapa de pendientes
            params_mapa = {
                "SERVICE": "WMS",
                "VERSION": "1.1.1",
                "REQUEST": "GetMap",
                "LAYERS": "MDP05",
                "STYLES": "",
                "SRS": "EPSG:3857",
                "BBOX": f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
                "WIDTH": "1500",
                "HEIGHT": "1125",
                "FORMAT": "image/png",
                "TRANSPARENT": "FALSE"
            }
            
            # Parámetros para la leyenda
            params_leyenda = {
                "SERVICE": "WMS",
                "VERSION": "1.1.1",
                "REQUEST": "GetLegendGraphic",
                "LAYER": "MDP05",
                "FORMAT": "image/png",
                "WIDTH": "200",
                "HEIGHT": "400"
            }
            
            print(f"🛰️  Capturando Pendientes y Leyenda...", end=" ", flush=True)
            
            response_mapa = self.session.get(url_wms, params=params_mapa, timeout=45)
            response_leyenda = self.session.get(url_wms, params=params_leyenda, timeout=45)
            
            if response_mapa.status_code == 200 and 'image' in response_mapa.headers.get('Content-Type', ''):
                img_mapa = Image.open(BytesIO(response_mapa.content))
                img_leyenda = None
                
                if response_leyenda.status_code == 200 and 'image' in response_leyenda.headers.get('Content-Type', ''):
                    img_leyenda = Image.open(BytesIO(response_leyenda.content))
                
                fig, ax = plt.subplots(figsize=(12, 9))
                ax.imshow(img_mapa, extent=[bbox[0], bbox[2], bbox[1], bbox[3]], interpolation='lanczos')
                
                # Dibujar parcelas en azul
                gdf_3857.plot(ax=ax, facecolor='none', edgecolor='#0000FF', linewidth=1.5, zorder=10)
                
                # Chincheta roja con transparencia
                ax.plot(cx, cy, marker='v', color='#CC0000', markersize=22, 
                        markeredgecolor='white', markeredgewidth=2.5, alpha=0.7, zorder=11)
                
                # Añadir leyenda si se descargó correctamente
                if img_leyenda:
                    ax_leg = fig.add_axes([0.75, 0.15, 0.15, 0.3])
                    ax_leg.imshow(img_leyenda)
                    ax_leg.axis('off')
                    ax_leg.patch.set_facecolor('white')
                    ax_leg.patch.set_alpha(0.8)
                
                ax.set_xlim(bbox[0], bbox[2])
                ax.set_ylim(bbox[1], bbox[3])
                ax.set_axis_off()
                
                ruta_final = carpeta / "PLANO-PENDIENTES-LEYENDA.jpg"
                plt.savefig(ruta_final, dpi=150, bbox_inches='tight', pad_inches=0)
                plt.close()
                print(f"✅")
        except Exception as e:
            print(f"❌ Error: {e}")

    # ═══════════════════════════════════════════════════════════════════════
    # PASO 17: PLANO RED NATURA 2000
    # ═══════════════════════════════════════════════════════════════════════
    
    def _generar_plano_natura2000(self, carpeta: Path) -> None:
        """
        Genera plano de Red Natura 2000 sobre ortofoto PNOA con leyenda.
        
        Características:
        - Encuadre de 5km (vista de contexto ambiental)
        - Formato 4:3 (12x9 pulgadas)
        - 150 DPI
        - Base: Ortofoto PNOA del IGN
        - Capa: Red Natura 2000 con transparencia 70%
        - Parcelas en azul (#0000FF)
        - Chincheta en rojo (#CC0000) con alta opacidad
        - Leyenda reducida en esquina inferior izquierda
        - Fuentes: WMS PNOA (IGN) + WMS Red Natura (MAPAMA)
        
        Archivo generado: PLANO-NATURA-2000.jpg
        
        Args:
            carpeta: Carpeta donde guardar el plano
        """
        ruta_kml = carpeta / "MAPA_MAESTRO_TOTAL.kml"
        if not ruta_kml.exists():
            print(f"⚠️  No se encontró {ruta_kml.name}")
            return

        try:
            # Cargar y proyectar
            gdf = gpd.read_file(str(ruta_kml), driver='KML')
            if gdf.empty:
                return
            gdf_3857 = gdf.to_crs(epsg=3857)
            minx, miny, maxx, maxy = gdf_3857.total_bounds
            cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
            
            # Encuadre de 5km
            m = 5000
            bbox = [cx - m, cy - m * 0.75, cx + m, cy + m * 0.75]
            
            url_pnoa = "https://www.ign.es/wms-inspire/pnoa-ma"
            url_natura = "https://wms.mapama.gob.es/sig/Biodiversidad/RedNatura/wms.aspx"
            capa_natura = "PS.ProtectedSite"
            
            # Parámetros para la ortofoto base
            params_base = {
                "SERVICE": "WMS",
                "VERSION": "1.1.1",
                "REQUEST": "GetMap",
                "LAYERS": "OI.OrthoimageCoverage",
                "STYLES": "",
                "SRS": "EPSG:3857",
                "BBOX": f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
                "WIDTH": "1500",
                "HEIGHT": "1125",
                "FORMAT": "image/jpeg"
            }
            
            # Parámetros para la capa de Red Natura
            params_natura = {
                "SERVICE": "WMS",
                "VERSION": "1.1.1",
                "REQUEST": "GetMap",
                "LAYERS": capa_natura,
                "STYLES": "",
                "SRS": "EPSG:3857",
                "BBOX": f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
                "WIDTH": "1500",
                "HEIGHT": "1125",
                "FORMAT": "image/png",
                "TRANSPARENT": "TRUE"
            }
            
            # Parámetros para la leyenda
            params_leyenda = {
                "SERVICE": "WMS",
                "VERSION": "1.1.1",
                "REQUEST": "GetLegendGraphic",
                "LAYER": capa_natura,
                "FORMAT": "image/png"
            }
            
            print(f"🛰️  Generando Plano Natura 2000...", end=" ", flush=True)
            
            response_base = self.session.get(url_pnoa, params=params_base, timeout=45)
            response_natura = self.session.get(url_natura, params=params_natura, timeout=45)
            response_leyenda = self.session.get(url_natura, params=params_leyenda, timeout=45)
            
            if (response_base.status_code == 200 and response_natura.status_code == 200 and
                'image' in response_base.headers.get('Content-Type', '') and
                'image' in response_natura.headers.get('Content-Type', '')):
                
                img_base = Image.open(BytesIO(response_base.content))
                img_natura = Image.open(BytesIO(response_natura.content))
                img_leyenda = None
                
                if response_leyenda.status_code == 200 and 'image' in response_leyenda.headers.get('Content-Type', ''):
                    img_leyenda = Image.open(BytesIO(response_leyenda.content))
                
                # Crear figura sin márgenes
                fig = plt.figure(figsize=(12, 9))
                ax = fig.add_axes([0, 0, 1, 1])
                
                # Capa base: ortofoto PNOA
                ax.imshow(img_base, extent=[bbox[0], bbox[2], bbox[1], bbox[3]])
                
                # Capa de Red Natura 2000 con transparencia 70%
                ax.imshow(img_natura, extent=[bbox[0], bbox[2], bbox[1], bbox[3]], alpha=0.7)
                
                # Dibujar parcelas en azul
                gdf_3857.plot(ax=ax, facecolor='none', edgecolor='#0000FF', linewidth=1.5, zorder=10)
                
                # Chincheta roja con alta opacidad
                ax.plot(cx, cy, marker='v', color='#CC0000', markersize=22,
                        markeredgecolor='white', markeredgewidth=2.5, alpha=0.9, zorder=11)
                
                # Añadir leyenda reducida en esquina inferior izquierda
                if img_leyenda:
                    ax_leg = fig.add_axes([0.01, 0.01, 0.10, 0.12])
                    ax_leg.imshow(img_leyenda, aspect='equal')
                    ax_leg.axis('off')
                
                ax.set_xlim(bbox[0], bbox[2])
                ax.set_ylim(bbox[1], bbox[3])
                ax.set_axis_off()
                
                ruta_final = carpeta / "PLANO-NATURA-2000.jpg"
                plt.savefig(ruta_final, dpi=150, bbox_inches=None, pad_inches=0, pil_kwargs={'quality': 95})
                plt.close()
                print(f"✅")
        except Exception as e:
            print(f"❌ Error: {e}")

    # ═══════════════════════════════════════════════════════════════════════
    # PASO 18: PLANO MONTES PÚBLICOS (CMUP) 🆕
    # ═══════════════════════════════════════════════════════════════════════

    def _descargar_imagen_wms(self, url: str, params: dict) -> Optional[Image.Image]:
        """
        Descarga una imagen desde un servicio WMS.
        
        Args:
            url: URL del servicio WMS
            params: Parámetros de la petición
            
        Returns:
            Imagen PIL o None si hay error
        """
        try:
            response = self.session.get(url, params=params, timeout=60)
            if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
                return Image.open(BytesIO(response.content))
        except Exception as e:
            print(f"Error WMS: {e}", end=" ")
        return None

    def _descargar_cmup_wfs(self) -> Optional[gpd.GeoDataFrame]:
        """
        Descarga los polígonos del Catálogo de Montes de Utilidad Pública vía WFS.
        
        Returns:
            GeoDataFrame con los polígonos CMUP o None si hay error
        """
        url_wfs = "https://wms.mapama.gob.es/sig/Biodiversidad/IEPF_CMUP"
        capa_wfs = "IEPF_CMUP:CMUP_Poligono"
        
        try:
            url = (
                f"{url_wfs}?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&"
                f"TYPENAME={capa_wfs}&SRSNAME=EPSG:4326"
            )
            
            print("Descargando CMUP vía WFS...", end=" ", flush=True)
            
            response = self.session.get(url, timeout=60)
            response.raise_for_status()
            
            # Guardar GML temporal
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".gml")
            tmp.write(response.content)
            tmp.close()
            
            # Leer con GeoPandas
            gdf = gpd.read_file(tmp.name, driver="GML")
            
            # Limpiar archivo temporal
            Path(tmp.name).unlink()
            
            print(f"{len(gdf)} polígonos descargados...", end=" ", flush=True)
            return gdf
            
        except Exception as e:
            print(f"Error WFS: {e}", end=" ")
            return None

    def _generar_plano_montes_publicos(self, carpeta: Path) -> None:
        """
        Genera plano de Montes de Utilidad Pública (CMUP/IEPF).
        
        Descarga los polígonos oficiales vía WFS del MITECO y los superpone
        sobre ortofoto PNOA con la leyenda oficial.
        
        Args:
            carpeta: Carpeta con KML y donde guardar el plano
        """
        print(f"🌲 Generando Plano Montes Públicos (CMUP)...", end=" ", flush=True)
        
        kml = carpeta / "MAPA_MAESTRO_TOTAL.kml"
        
        if not kml.exists():
            print("⚠️ KML no encontrado")
            return
        
        try:
            # 1) Leer KML de las parcelas
            gdf_kml = gpd.read_file(str(kml), driver="KML")
            if gdf_kml.empty:
                print("⚠️ KML vacío")
                return
            
            gdf_kml_3857 = gdf_kml.to_crs(3857)
            minx, miny, maxx, maxy = gdf_kml_3857.total_bounds
            cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
            
            margin = 5000
            bbox = [cx - margin, cy - margin * 0.75, cx + margin, cy + margin * 0.75]
            
            # 2) Descargar CMUP vía WFS
            gdf_cmup = self._descargar_cmup_wfs()
            if gdf_cmup is None or gdf_cmup.empty:
                print("⚠️ Sin datos CMUP")
                return
            
            # 3) Recortar CMUP al área del KML
            gdf_cmup = gdf_cmup.to_crs(3857)
            gdf_clip = gpd.overlay(gdf_cmup, gdf_kml_3857, how="intersection")
            
            # 4) Descargar ortofoto PNOA
            url_pnoa = "https://www.ign.es/wms-inspire/pnoa-ma"
            params_base = {
                "SERVICE": "WMS",
                "VERSION": "1.1.1",
                "REQUEST": "GetMap",
                "LAYERS": "OI.OrthoimageCoverage",
                "STYLES": "",
                "SRS": "EPSG:3857",
                "BBOX": f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
                "WIDTH": "1500",
                "HEIGHT": "1125",
                "FORMAT": "image/jpeg"
            }
            img_base = self._descargar_imagen_wms(url_pnoa, params_base)
            
            # 5) Descargar leyenda del WMS de CMUP
            url_wms = "https://wms.mapama.gob.es/sig/Biodiversidad/IEPF_CMUP"
            capa_wms = "AM.ForestManagementArea"
            
            params_leyenda = {
                "SERVICE": "WMS",
                "VERSION": "1.1.1",
                "REQUEST": "GetLegendGraphic",
                "LAYER": capa_wms,
                "FORMAT": "image/png"
            }
            img_leyenda = self._descargar_imagen_wms(url_wms, params_leyenda)
            
            # 6) Dibujar plano
            fig = plt.figure(figsize=(12, 9))
            ax = fig.add_axes([0, 0, 1, 1])
            
            # Fondo: ortofoto
            if img_base:
                ax.imshow(img_base, extent=[bbox[0], bbox[2], bbox[1], bbox[3]])
            
            # Polígonos CMUP reales (WFS) en verde
            if not gdf_clip.empty:
                gdf_clip.plot(ax=ax, facecolor="none", edgecolor="#00AA00",
                              linewidth=2.0, zorder=10)
            
            # Parcelas KML en azul
            gdf_kml_3857.plot(ax=ax, facecolor="none", edgecolor="#0000FF",
                              linewidth=1.5, zorder=11)
            
            # Marcador rojo
            ax.plot(cx, cy, marker='v', color='#CC0000', markersize=22,
                    markeredgecolor='white', markeredgewidth=2.5, alpha=0.9, zorder=12)
            
            # Leyenda en esquina inferior izquierda
            if img_leyenda:
                ax_leg = fig.add_axes([0.01, 0.01, 0.12, 0.15])
                ax_leg.imshow(img_leyenda)
                ax_leg.axis("off")
            
            ax.set_xlim(bbox[0], bbox[2])
            ax.set_ylim(bbox[1], bbox[3])
            ax.set_axis_off()
            
            ruta_final = carpeta / "PLANO-MONTES-PUBLICOS.jpg"
            plt.savefig(ruta_final, dpi=150, bbox_inches=None, pad_inches=0,
                        pil_kwargs={'quality': 95})
            plt.close()
            
            print("✅")
            
        except Exception as e:
            print(f"❌ Error: {e}")

    # ═══════════════════════════════════════════════════════════════════════
    # PASO 19: PLANO VÍAS PECUARIAS 🆕
    # ═══════════════════════════════════════════════════════════════════════

    def _generar_plano_vias_pecuarias(self, carpeta: Path) -> None:
        """
        Genera plano de Vías Pecuarias desde GPKG local.
        
        Utiliza el archivo RGVP2024.gpkg (Red de Vías Pecuarias) con clasificación
        por tipo (Cañadas, Cordeles, Veredas, etc.) sobre fondo OpenStreetMap.
        
        Args:
            carpeta: Carpeta con KML y donde guardar el plano
        """
        print(f"🐄 Generando Plano Vías Pecuarias...", end=" ", flush=True)
        
        kml = carpeta / "MAPA_MAESTRO_TOTAL.kml"
        
        if not kml.exists():
            print("⚠️ KML no encontrado")
            return
        
        # Ruta al GPKG de Vías Pecuarias
        gpkg_vvpp = self.fuentes / "CAPAS_gpkg" / "afecciones" / "RGVP2024.gpkg"
        
        if not gpkg_vvpp.exists():
            print(f"⚠️ GPKG no encontrado: {gpkg_vvpp}")
            return
        
        try:
            # 1) Leer KML y convertir a EPSG:3857
            print("Leyendo KML...", end=" ", flush=True)
            gdf = gpd.read_file(str(kml), driver="KML")
            gdf_3857 = gdf.to_crs(epsg=3857)
            
            # 2) Calcular área de búsqueda
            minx, miny, maxx, maxy = gdf_3857.total_bounds
            margen = 5000  # 5km de margen
            area_busqueda = box(minx - margen, miny - margen, maxx + margen, maxy + margen)
            
            # 3) Cargar Vías Pecuarias con filtro espacial
            print("Cargando Vías Pecuarias...", end=" ", flush=True)
            vvpp = gpd.read_file(str(gpkg_vvpp), bbox=area_busqueda)
            vvpp_3857 = vvpp.to_crs(epsg=3857)
            
            # 4) Crear figura
            fig = plt.figure(figsize=(12, 12))
            ax = fig.add_axes([0, 0, 1, 1])
            
            # Establecer límites antes del basemap
            ax.set_xlim(minx - margen, maxx + margen)
            ax.set_ylim(miny - margen, maxy + margen)
            
            # 5) Añadir fondo OpenStreetMap
            print("Añadiendo basemap...", end=" ", flush=True)
            try:
                cx.add_basemap(ax, source=cx.providers.OpenStreetMap.Mapnik)
            except Exception as e:
                print(f"⚠️ Error basemap: {e}...", end=" ")
            
            # 6) Dibujar Vías Pecuarias si existen
            if not vvpp_3857.empty:
                print(f"Encontradas {len(vvpp_3857)} vías...", end=" ", flush=True)
                
                # Usar columna de clasificación si existe
                columna_label = "FC_CLASIF" if "FC_CLASIF" in vvpp_3857.columns else None
                
                vvpp_3857.plot(
                    ax=ax,
                    linewidth=4,
                    column=columna_label,
                    cmap="viridis",
                    zorder=5,
                    alpha=0.7,
                    legend=True,
                    legend_kwds={
                        'loc': 'lower left',
                        'title': 'Vías Pecuarias',
                        'fontsize': 'large'
                    }
                )
            else:
                print("⚠️ Sin vías pecuarias en esta zona...", end=" ", flush=True)
            
            # 7) Dibujar parcela (KML) en azul
            gdf_3857.plot(ax=ax, facecolor="none", edgecolor="blue",
                          linewidth=3, zorder=10)
            
            # 8) Marcador en centroide
            centro = gdf_3857.geometry.centroid.iloc[0]
            ax.plot(centro.x, centro.y, marker="v", color="red", markersize=25,
                    markeredgecolor="white", markeredgewidth=2, zorder=15)
            
            ax.set_axis_off()
            
            # 9) Guardar
            ruta_final = carpeta / "PLANO-VIAS-PECUARIAS.jpg"
            plt.savefig(ruta_final, dpi=150, bbox_inches=None, pad_inches=0)
            plt.close()
            
            print("✅")
            
        except Exception as e:
            print(f"❌ Error: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# FUNCIÓN WRAPPER PARA INTEGRACIÓN CON API (main.py)
# ═══════════════════════════════════════════════════════════════════════════

async def run_cadastral_processing(
    refcat: str, 
    log_callback, 
    output_dir: str,
    fuentes_dir: str
) -> bool:
    """
    Procesa una referencia catastral individual (wrapper async para API).
    
    Args:
        refcat: Referencia catastral a procesar
        log_callback: Función async para enviar logs
        output_dir: Directorio donde guardar los resultados
        fuentes_dir: Directorio donde están las FUENTES (capas GPKG, etc.)
        
    Returns:
        True si el procesamiento fue exitoso, False en caso contrario
    """
    import asyncio
    from pathlib import Path
    
    try:
        await log_callback(f"Procesando {refcat}...", "info")
        
        # Convertir rutas a Path
        output_path = Path(output_dir)
        fuentes_path = Path(fuentes_dir)
        
        # Crear un orquestador temporal con las rutas correctas
        class OrquestadorSingle(OrquestadorPipeline):
            def __init__(self, output_dir: Path, fuentes_dir: Path):
                self.base_dir = output_dir.parent
                self.outputs = output_dir
                self.fuentes = fuentes_dir
                self.carpeta_afecciones = fuentes_dir / "CAPAS_gpkg" / "afecciones"
                
                # Sesión HTTP reutilizable
                self.session = requests.Session()
                self.session.headers.update({"User-Agent": USER_AGENT})
                
                # No crear carpetas, asumimos que ya existen
                output_dir.mkdir(parents=True, exist_ok=True)
        
        orq = OrquestadorSingle(output_path, fuentes_path)
        
        # Procesar la referencia
        await log_callback(f"Descargando datos catastrales...", "info")
        parcela = ParcelaData(refcat)
        
        # Descargar XML y PDF
        xml_path = output_path / f"{refcat}_INSPIRE.xml"
        pdf_path = output_path / f"{refcat}_CDyG.pdf"
        
        orq._descargar_xml(refcat, xml_path)
        orq._descargar_pdf(refcat, pdf_path)
        
        # Extraer geometría
        if not xml_path.exists():
            await log_callback(f"❌ No se pudo descargar XML para {refcat}", "error")
            return False
            
        superficie, coords = orq._extraer_geometria(xml_path)
        if not coords:
            await log_callback(f"❌ No se pudo extraer geometría de {refcat}", "error")
            return False
            
        parcela.actualizar_geometria(coords, superficie)
        parcela.rutas.update({"xml": str(xml_path), "pdf": str(pdf_path)})
        
        await log_callback(f"✅ Datos descargados ({superficie:,.0f} m²)", "info")
        
        # Generar KML
        await log_callback("Generando archivos KML...", "info")
        orq._generar_kml(output_path, [parcela])
        
        # Generar PNG
        await log_callback("Generando siluetas PNG...", "info")
        orq._generar_png(output_path, [parcela])
        
        # Crear tablas
        await log_callback("Creando tablas de datos...", "info")
        orq._crear_tablas(output_path, [parcela])
        
        # Generar log
        await log_callback("Generando log de expediente...", "info")
        orq._generar_log_expediente(output_path, [parcela])
        
        # Análisis de afecciones
        await log_callback("Analizando afecciones...", "info")
        orq._procesar_afecciones(output_path)
        
        # Generar planos
        await log_callback("Generando planos de emplazamiento...", "info")
        orq._generar_plano_emplazamiento(output_path)
        orq._generar_plano_ortofoto(output_path)
        
        await log_callback("Generando planos catastrales...", "info")
        orq._generar_plano_catastral(output_path)
        
        await log_callback("Generando planos IGN...", "info")
        orq._generar_planos_ign(output_path)
        
        await log_callback("Generando planos provinciales...", "info")
        orq._generar_planos_provinciales(output_path)
        
        await log_callback("Generando planos históricos...", "info")
        orq._generar_planos_historicos(output_path)
        
        await log_callback("Generando planos temáticos...", "info")
        orq._generar_plano_pendientes(output_path)
        orq._generar_plano_natura2000(output_path)
        
        await log_callback("Generando planos de protección ambiental...", "info")
        orq._generar_plano_montes_publicos(output_path)
        orq._generar_plano_vias_pecuarias(output_path)
        
        await log_callback(f"✅ Procesamiento de {refcat} completado", "success")
        return True
        
    except Exception as e:
        await log_callback(f"❌ Error procesando {refcat}: {str(e)}", "error")
        import traceback
        traceback.print_exc()
        return False


# ═══════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    """
    Ejecuta el orquestador desde el directorio donde se encuentra el script.
    
    Uso:
        python orquestador_completo_final.py
    
    El script buscará archivos .txt en la carpeta INPUTS y generará todos
    los productos cartográficos en OUTPUTS.
    """
    base = Path(__file__).resolve().parent
    
    print(f"\n{'═'*80}")
    print(f"║{'ORQUESTADOR PIPELINE GIS CATASTRAL'.center(78)}║")
    print(f"║{'Scripts 1-19 Integrados'.center(78)}║")
    print(f"{'═'*80}\n")
    print(f"📂 Directorio base: {base}")
    print(f"📥 Buscando archivos .txt en: {base / 'INPUTS'}")
    print(f"📤 Resultados se guardarán en: {base / 'OUTPUTS'}\n")
    
    orquestador = OrquestadorPipeline(base)
    orquestador.run()
    
    print(f"\n{'═'*80}")
    print(f"║{'PIPELINE FINALIZADO'.center(78)}║")
    print(f"{'═'*80}\n")
