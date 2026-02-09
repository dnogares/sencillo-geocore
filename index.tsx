import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { createRoot } from 'react-dom/client';
import { 
  Map, 
  FileText, 
  Table, 
  Settings, 
  Upload, 
  Play, 
  CheckCircle, 
  AlertCircle, 
  FileCode, 
  Download, 
  Layers,
  Activity,
  Terminal,
  Database,
  Trash2,
  FolderOpen,
  Box,
  Plus,
  FileArchive,
  FolderTree
} from 'lucide-react';

// --- Types ---
type AppState = 'input' | 'processing' | 'results';
type LogEntry = { id: string; timestamp: string; message: string; type: 'info' | 'success' | 'warning' | 'error' };
type OutputFile = { name: string; type: 'gml' | 'xlsx' | 'json' | 'zip'; size: string };
type Project = {
  id: string;
  name: string;
  originalFile: File;
  references: string[];
  status: 'pending' | 'processing' | 'completed' | 'error';
  outputs: OutputFile[];
};

// --- Styles (Tailwind abstraction) ---
const UI = {
  Container: "min-h-screen bg-slate-950 text-slate-200 font-sans flex overflow-hidden",
  Sidebar: "w-20 lg:w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between transition-all duration-300",
  Main: "flex-1 flex flex-col relative overflow-hidden",
  Header: "h-16 border-b border-slate-800 bg-slate-950/50 backdrop-blur flex items-center justify-between px-6",
  Content: "flex-1 overflow-y-auto p-6 relative",
  Card: "bg-slate-900 border border-slate-800 rounded-lg p-6 shadow-xl",
  ButtonPrimary: "bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-md font-medium flex items-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_15px_rgba(37,99,235,0.3)]",
  ButtonSecondary: "bg-slate-800 hover:bg-slate-700 text-slate-200 px-4 py-2 rounded-md font-medium flex items-center gap-2 transition-all border border-slate-700",
  InputZone: "border-2 border-dashed border-slate-700 hover:border-blue-500 hover:bg-slate-900/50 rounded-xl p-8 flex flex-col items-center justify-center transition-all cursor-pointer h-full min-h-[200px]",
  Title: "text-2xl font-bold text-white tracking-tight",
  Subtitle: "text-slate-400 text-sm",
  StatusBadge: (status: string) => {
    const map: Record<string, string> = {
      idle: "bg-slate-800 text-slate-400",
      active: "bg-blue-900/30 text-blue-400 border border-blue-800",
      success: "bg-emerald-900/30 text-emerald-400 border border-emerald-800",
      pending: "bg-slate-700 text-slate-300",
      processing: "bg-blue-900/50 text-blue-300 border border-blue-700 animate-pulse",
      completed: "bg-emerald-900/30 text-emerald-400 border border-emerald-800",
    };
    return `px-2 py-1 rounded text-xs font-mono uppercase tracking-wider ${map[status] || map.idle}`;
  }
};

// --- Helper Functions ---
const generateId = () => Math.random().toString(36).substr(2, 9);
const getTimestamp = () => new Date().toLocaleTimeString('es-ES', { hour12: false });

// --- Components (OPTIMIZADOS) ---

// ✅ OPTIMIZACIÓN: Sidebar memoizado
const Sidebar = React.memo(({ activeTab, setActiveTab }: { activeTab: string, setActiveTab: (t: string) => void }) => {
  const menuItems = useMemo(() => [
    { id: 'processor', icon: <Activity size={24} />, label: 'Procesador', disabled: false },
    { id: 'map', icon: <Map size={24} />, label: 'Visor Mapa', disabled: true },
    { id: 'data', icon: <Table size={24} />, label: 'Visor Datos', disabled: true },
    { id: 'settings', icon: <Settings size={24} />, label: 'Configuración', disabled: true },
  ], []);

  return (
    <div className={UI.Sidebar}>
      <div>
        <div className="h-16 flex items-center justify-center lg:justify-start lg:px-6 border-b border-slate-800">
          <Layers className="text-blue-500 mr-0 lg:mr-3" size={28} />
          <span className="font-bold text-xl hidden lg:block tracking-wider">GEO<span className="text-blue-500">CORE</span></span>
        </div>
        <nav className="p-4 space-y-2">
          {menuItems.map((item) => (
            <button
              key={item.id}
              onClick={() => !item.disabled && setActiveTab(item.id)}
              className={`w-full flex items-center p-3 rounded-lg transition-all ${
                activeTab === item.id 
                  ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/50' 
                  : item.disabled 
                    ? 'text-slate-600 cursor-not-allowed opacity-50' 
                    : 'text-slate-400 hover:bg-slate-800 hover:text-white'
              }`}
            >
              <span className="flex-shrink-0">{item.icon}</span>
              <span className="ml-3 font-medium hidden lg:block">{item.label}</span>
              {item.disabled && <span className="ml-auto text-[10px] bg-slate-800 px-1 rounded hidden lg:block text-slate-500">WIP</span>}
            </button>
          ))}
        </nav>
      </div>
      
      <div className="p-4 border-t border-slate-800">
        <div className="flex items-center p-2 rounded-lg bg-slate-900/50 border border-slate-800">
          <div className="w-8 h-8 rounded bg-gradient-to-tr from-blue-500 to-purple-600 flex items-center justify-center font-bold text-xs text-white">
            U
          </div>
          <div className="ml-3 hidden lg:block">
            <div className="text-sm font-medium text-white">Usuario GIS</div>
            <div className="text-xs text-slate-500">Admin</div>
          </div>
        </div>
      </div>
    </div>
  );
});
Sidebar.displayName = 'Sidebar';

// ✅ OPTIMIZACIÓN: ProcessingTerminal con auto-scroll eficiente
const ProcessingTerminal = React.memo(({ logs }: { logs: LogEntry[] }) => {
  const endRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll optimizado: solo si el usuario está al final
  useEffect(() => {
    if (!containerRef.current) return;
    
    const container = containerRef.current;
    const isScrolledToBottom = container.scrollHeight - container.scrollTop <= container.clientHeight + 50;
    
    if (isScrolledToBottom) {
      endRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }
  }, [logs]);

  return (
    <div className="bg-slate-950 rounded-lg border border-slate-800 font-mono text-sm overflow-hidden flex flex-col h-[500px] shadow-2xl">
      <div className="bg-slate-900 border-b border-slate-800 p-2 px-4 flex items-center gap-2">
        <Terminal size={14} className="text-slate-400" />
        <span className="text-slate-400 text-xs">completo.py — python3.11</span>
        <div className="ml-auto flex gap-1.5">
          <div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div>
          <div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div>
          <div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div>
        </div>
      </div>
      <div ref={containerRef} className="flex-1 overflow-y-auto p-4 space-y-1 scroll-container">
        {logs.map((log) => (
          <div key={log.id} className="flex gap-3 animate-in fade-in slide-in-from-left-2 duration-300">
            <span className="text-slate-600 select-none">[{log.timestamp}]</span>
            <span className={`${
              log.type === 'error' ? 'text-red-400' :
              log.type === 'success' ? 'text-emerald-400' :
              log.type === 'warning' ? 'text-amber-400' :
              'text-blue-200'
            }`}>
              {log.type === 'info' && <span className="text-blue-500 mr-2">ℹ</span>}
              {log.type === 'success' && <span className="text-emerald-500 mr-2">✔</span>}
              {log.type === 'error' && <span className="text-red-500 mr-2">✖</span>}
              {log.message}
            </span>
          </div>
        ))}
        <div ref={endRef} />
      </div>
    </div>
  );
});
ProcessingTerminal.displayName = 'ProcessingTerminal';

// ✅ OPTIMIZACIÓN: ResultsView memoizado
const ResultsView = React.memo(({ projects, onReset }: { projects: Project[], onReset: () => void }) => {
  return (
    <div className="space-y-6 animate-in zoom-in-95 duration-500">
      <div className="flex items-center gap-4 mb-8">
        <div className="w-12 h-12 rounded-full bg-emerald-500/10 flex items-center justify-center border border-emerald-500/50">
          <CheckCircle className="text-emerald-500" size={24} />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-white">Procesamiento Completado</h2>
          <p className="text-slate-400">Se han procesado {projects.length} proyectos correctamente.</p>
        </div>
      </div>

      <div className="space-y-6">
        {projects.map((project) => (
          <div key={project.id} className="bg-slate-900/50 border border-slate-800 rounded-lg overflow-hidden">
            <div className="bg-slate-900 p-4 border-b border-slate-800 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <FolderOpen size={20} className="text-blue-500" />
                    <h3 className="font-medium text-slate-200">{project.name}</h3>
                    <span className="text-xs bg-slate-800 text-slate-400 px-2 py-0.5 rounded">
                        {project.references.length} refs
                    </span>
                </div>
            </div>
            
            <div className="p-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {project.outputs.map((file, idx) => (
                <div key={idx} className="bg-slate-950 hover:bg-slate-800 transition-colors border border-slate-800 p-4 rounded-lg flex items-center justify-between group col-span-1 md:col-span-2 lg:col-span-1">
                    <div className="flex items-center gap-4">
                      <div className={`p-2.5 rounded-lg ${
                          file.type === 'zip' ? 'bg-yellow-500/10 text-yellow-400' :
                          'bg-blue-500/10 text-blue-400'
                      }`}>
                          {file.type === 'zip' ? <FileArchive size={24} /> : <FileCode size={24} />}
                      </div>
                      <div className="overflow-hidden">
                          <div className="font-medium text-slate-200 text-sm truncate">{file.name}</div>
                          <div className="text-xs text-slate-500 mb-1">{file.size}</div>
                          {file.type === 'zip' && (
                            <div className="flex items-center gap-1.5 text-[10px] text-slate-400 bg-slate-900/50 px-1.5 py-0.5 rounded w-fit">
                              <FolderTree size={10} />
                              <span>Estructura: /GML, /XLSX, /JSON</span>
                            </div>
                          )}
                      </div>
                    </div>
                    <button className="p-2 hover:bg-blue-600 hover:text-white rounded-md text-slate-400 transition-colors bg-slate-900 border border-slate-800 group-hover:border-blue-500/50">
                      <Download size={18} />
                    </button>
                </div>
                ))}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-8 flex gap-4">
        <button onClick={onReset} className={UI.ButtonSecondary}>
          Procesar nuevos proyectos
        </button>
        <button className={UI.ButtonPrimary}>
          <Layers size={18} />
          Ver en Mapa (Demo)
        </button>
      </div>
    </div>
  );
});
ResultsView.displayName = 'ResultsView';

function Processor() {
  const [appState, setAppState] = useState<AppState>('input');
  const [projects, setProjects] = useState<Project[]>([]);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  
  // ✅ OPTIMIZACIÓN: Cleanup de timeouts en unmount
  const timeoutIdsRef = useRef<NodeJS.Timeout[]>([]);

  useEffect(() => {
    return () => {
      // Limpia todos los timeouts pendientes
      timeoutIdsRef.current.forEach(clearTimeout);
      timeoutIdsRef.current = [];
    };
  }, []);

  // ✅ OPTIMIZACIÓN: useCallback para evitar recrear funciones
  const handleFileUpload = useCallback(async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = e.target.files;
    if (selectedFiles && selectedFiles.length > 0) {
      const newFiles = Array.from(selectedFiles).filter(f => f.type === 'text/plain');
      
      const newProjects: Project[] = [];
      
      for (const file of newFiles) {
        try {
          const text = await file.text();
          const lines = text.split(/\r?\n/).filter(line => line.trim().length > 0);
          
          newProjects.push({
            id: generateId(),
            name: file.name,
            originalFile: file,
            references: lines,
            status: 'pending',
            outputs: []
          });
        } catch (err) {
          console.error(`Error reading file ${file.name}`, err);
        }
      }

      setProjects(prev => [...prev, ...newProjects]);
    }
  }, []);

  const removeProject = useCallback((id: string) => {
    setProjects(prev => prev.filter(p => p.id !== id));
  }, []);

  const startProcessing = useCallback(() => {
    if (projects.length === 0) return;

    setAppState('processing');
    setLogs([{ id: generateId(), timestamp: getTimestamp(), message: 'Inicializando entorno GIS Python 3.11...', type: 'info' }]);

    // ✅ OPTIMIZACIÓN: Array para rastrear timeouts
    const newTimeoutIds: NodeJS.Timeout[] = [];
    
    let logQueue: { delay: number, msg: string, type: string }[] = [];
    let currentTime = 500;

    projects.forEach((proj, index) => {
        logQueue.push({ 
            delay: currentTime, 
            msg: `--- INICIANDO PROYECTO: ${proj.name} ---`, 
            type: 'info' 
        });
        currentTime += 800;

        logQueue.push({
            delay: currentTime,
            msg: `[${proj.name}] Leyendo ${proj.references.length} referencias catastrales.`,
            type: 'info'
        });
        currentTime += 1000;

        logQueue.push({
            delay: currentTime,
            msg: `[${proj.name}] Conectando con Servicio WFS Catastro...`,
            type: 'warning'
        });
        currentTime += 1500;

        logQueue.push({
            delay: currentTime,
            msg: `[${proj.name}] Generando geometrías GML y reproyectando a ETRS89.`,
            type: 'info'
        });
        currentTime += 1200;

        logQueue.push({
            delay: currentTime,
            msg: `[${proj.name}] Clasificando archivos por tipo (GML/XLSX/JSON)...`,
            type: 'info'
        });
        currentTime += 800;

        logQueue.push({
            delay: currentTime,
            msg: `[${proj.name}] Empaquetando resultados en archivo ZIP.`,
            type: 'success'
        });
        currentTime += 800;
    });

    logQueue.push({
        delay: currentTime,
        msg: 'Generación de archivos ZIP completada.',
        type: 'info'
    });
    currentTime += 1000;

    logQueue.push({
        delay: currentTime,
        msg: 'PROCESO DE LOTES COMPLETADO EXITOSAMENTE.',
        type: 'success'
    });

    // Execute Log Queue con cleanup tracking
    logQueue.forEach(step => {
        const timeoutId = setTimeout(() => {
            setLogs(prev => [...prev, {
                id: generateId(),
                timestamp: getTimestamp(),
                message: step.msg,
                type: step.type as any
            }]);
        }, step.delay);
        newTimeoutIds.push(timeoutId);
    });

    // Finalize state
    const finalTimeout = setTimeout(() => {
        const completedProjects = projects.map(p => ({
            ...p,
            status: 'completed' as const,
            outputs: [
                { 
                  name: p.name.replace('.txt', '_complete.zip'), 
                  type: 'zip' as const, 
                  size: `${(Math.random() * 5 + 2).toFixed(1)} MB` 
                }
            ]
        }));
        setProjects(completedProjects);
        setAppState('results');
    }, currentTime + 500);
    newTimeoutIds.push(finalTimeout);
    
    // Guarda referencias para cleanup
    timeoutIdsRef.current = newTimeoutIds;
  }, [projects]);

  const reset = useCallback(() => {
    // Limpia timeouts antes de reset
    timeoutIdsRef.current.forEach(clearTimeout);
    timeoutIdsRef.current = [];
    
    setAppState('input');
    setProjects([]);
    setLogs([]);
  }, []);

  return (
    <div className="max-w-6xl mx-auto h-full flex flex-col">
      <div className="mb-6 flex-shrink-0">
        <h1 className={UI.Title}>Procesador Catastral Multiproyecto</h1>
        <p className={UI.Subtitle}>Gestión de proyectos GIS independientes basados en completo.py</p>
      </div>

      {appState === 'input' && (
        <div className="flex-1 overflow-hidden grid grid-cols-1 lg:grid-cols-3 gap-6 min-h-0">
          
          <div className="lg:col-span-1 flex flex-col gap-6">
            <div className={`${UI.Card} flex-1 flex flex-col min-h-[300px]`}>
              <h3 className="text-lg font-medium text-white mb-4">Nuevo Proyecto</h3>
              <div className="flex-1">
                <label className={UI.InputZone}>
                    <input 
                    type="file" 
                    className="hidden" 
                    accept=".txt" 
                    multiple 
                    onChange={handleFileUpload} 
                    />
                    <Upload size={40} className="text-slate-500 mb-4" />
                    <span className="text-center font-medium text-slate-300">
                    Añadir TXT
                    </span>
                    <span className="text-xs text-slate-500 mt-2 text-center">
                    Cada archivo crea un proyecto independiente
                    </span>
                </label>
              </div>
            </div>
            
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-lg">
                <div className="flex justify-between items-center mb-4">
                    <span className="text-slate-400 text-sm">Proyectos:</span>
                    <span className="font-mono text-white text-lg">{projects.length}</span>
                </div>
                <div className="flex justify-between items-center mb-6">
                    <span className="text-slate-400 text-sm">Total Referencias:</span>
                    <span className="font-mono text-blue-400 text-lg">
                        {projects.reduce((acc, p) => acc + p.references.length, 0)}
                    </span>
                </div>
                <button 
                    onClick={startProcessing} 
                    disabled={projects.length === 0}
                    className={`${UI.ButtonPrimary} w-full justify-center py-3`}
                >
                    <Play size={20} fill="currentColor" />
                    Ejecutar Lote
                </button>
            </div>
          </div>

          <div className="lg:col-span-2 flex flex-col min-h-0">
            <div className="flex items-center gap-2 mb-4">
                <FolderOpen className="text-blue-500" size={20} />
                <h3 className="text-lg font-medium text-white">Proyectos en Cola</h3>
            </div>
            
            <div className="flex-1 overflow-y-auto pr-2 pb-2 scroll-container">
                {projects.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {projects.map((proj) => (
                            <div key={proj.id} className="bg-slate-900 border border-slate-800 p-4 rounded-lg group hover:border-blue-500/50 transition-all shadow-lg animate-in zoom-in-95">
                                <div className="flex justify-between items-start mb-3">
                                    <div className="p-2 bg-blue-900/20 text-blue-400 rounded-lg">
                                        <FileText size={20} />
                                    </div>
                                    <button 
                                        onClick={() => removeProject(proj.id)}
                                        className="text-slate-500 hover:text-red-400 transition-colors"
                                    >
                                        <Trash2 size={16} />
                                    </button>
                                </div>
                                <h4 className="text-slate-200 font-medium truncate mb-1" title={proj.name}>
                                    {proj.name}
                                </h4>
                                <div className="flex items-center gap-2 text-xs text-slate-500 mb-3">
                                    <span>{(proj.originalFile.size / 1024).toFixed(1)} KB</span>
                                    <span>•</span>
                                    <span>TXT</span>
                                </div>
                                <div className="pt-3 border-t border-slate-800 flex justify-between items-center">
                                    <span className="text-xs text-slate-400">Referencias</span>
                                    <span className="text-sm font-mono text-blue-400 bg-blue-900/20 px-2 py-0.5 rounded">
                                        {proj.references.length}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="h-full border-2 border-dashed border-slate-800 rounded-xl flex flex-col items-center justify-center text-slate-600">
                        <Box size={48} className="opacity-20 mb-4" />
                        <p>No hay proyectos configurados</p>
                    </div>
                )}
            </div>
          </div>
        </div>
      )}

      {appState === 'processing' && (
        <div className="max-w-4xl mx-auto w-full flex-1 flex flex-col min-h-0">
          <div className="flex items-center justify-between mb-4 flex-shrink-0">
            <div className="flex items-center gap-3">
              <div className="w-3 h-3 rounded-full bg-blue-500 animate-pulse"></div>
              <span className="font-mono text-blue-400">EJECUTANDO LOTE COMPLETO.PY</span>
            </div>
            <span className="text-xs text-slate-500 font-mono">Procesando {projects.length} proyectos</span>
          </div>
          <div className="flex-1 min-h-0">
             <ProcessingTerminal logs={logs} />
          </div>
        </div>
      )}

      {appState === 'results' && (
        <ResultsView projects={projects} onReset={reset} />
      )}
    </div>
  );
}

function App() {
  const [activeTab, setActiveTab] = useState('processor');

  return (
    <div className={UI.Container}>
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className={UI.Main}>
        <header className={UI.Header}>
            <div className="flex items-center gap-3">
                 <div className={`p-2 rounded-lg ${
                     activeTab === 'processor' ? 'bg-blue-500/10 text-blue-400' : 'bg-slate-800 text-slate-400'
                 }`}>
                    {activeTab === 'processor' && <Activity size={20} />}
                    {activeTab === 'map' && <Map size={20} />}
                    {activeTab === 'data' && <Table size={20} />}
                    {activeTab === 'settings' && <Settings size={20} />}
                 </div>
                 <h2 className="text-lg font-medium text-white">
                  {activeTab === 'processor' && 'Procesador de Expedientes'}
                  {activeTab === 'map' && 'Visor Geográfico'}
                  {activeTab === 'data' && 'Base de Datos'}
                  {activeTab === 'settings' && 'Configuración del Sistema'}
                </h2>
            </div>
            
            <div className="flex items-center gap-4">
                <div className="hidden md:flex items-center gap-2 text-xs text-slate-500 bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-full">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                    API Conectada
                </div>
            </div>
        </header>

        <div className={UI.Content}>
          {activeTab === 'processor' ? (
            <Processor />
          ) : (
             <div className="h-full flex flex-col items-center justify-center text-slate-500">
               <div className="w-16 h-16 bg-slate-900 rounded-2xl flex items-center justify-center mb-4 border border-slate-800">
                  <FolderOpen size={32} className="opacity-20" />
               </div>
               <h3 className="text-lg font-medium text-slate-400">Módulo no disponible</h3>
               <p className="text-sm">Esta sección se encuentra en mantenimiento.</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

const root = createRoot(document.getElementById('root')!);
root.render(<App />);
