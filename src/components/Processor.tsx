import React, { useState } from 'react';
import { Upload, Play, FolderOpen, FileText, Trash2, Box, CheckCircle } from 'lucide-react';
import { AppState, Project, LogEntry } from '../types';
import { UI } from '../styles/ui';
import { generateId, getTimestamp } from '../utils/helpers';
import { ProcessingTerminal } from './ProcessingTerminal';
import { ResultsView } from './ResultsView';

export function Processor() {
    const [appState, setAppState] = useState<AppState>('input');
    const [projects, setProjects] = useState<Project[]>([]);
    const [logs, setLogs] = useState<LogEntry[]>([]);
    const [isProcessingDone, setIsProcessingDone] = useState(false);

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFiles = e.target.files;
        if (selectedFiles && selectedFiles.length > 0) {
            const filesArray = Array.from(selectedFiles) as File[];
            const newFiles = filesArray.filter(f => f.type === 'text/plain');

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
    };

    const removeProject = (id: string) => {
        setProjects(prev => prev.filter(p => p.id !== id));
    };

    const startProcessing = async () => {
        if (projects.length === 0) return;

        setIsProcessingDone(false);
        setAppState('processing');
        setLogs([]);

        for (const proj of projects) {
            try {
                // 1. Subir el archivo al backend
                const formData = new FormData();
                formData.append('file', proj.originalFile);

                const API_BASE_URL = '/api';
                const response = await fetch(`${API_BASE_URL}/upload`, {
                    method: 'POST',
                    body: formData,
                });

                if (!response.ok) throw new Error('Error al subir el archivo');

                const data = await response.json();
                const taskId = data.task_id;

                // 2. Escuchar logs en tiempo real vía SSE
                const eventSource = new EventSource(`${API_BASE_URL}/stream/${taskId}`);

                eventSource.onmessage = (event) => {
                    const logEntry = JSON.parse(event.data);
                    setLogs(prev => [...prev, logEntry]);

                    if (logEntry.message.includes("EXITOSAMENTE")) {
                        eventSource.close();

                        // Extraer URL de descarga si existe en el mensaje
                        let downloadUrl = '';
                        if (logEntry.message.includes("URL:")) {
                            downloadUrl = logEntry.message.split("URL:")[1];
                        }

                        // Marcar proyecto como completado con el link real
                        setProjects(prev => prev.map(p =>
                            p.id === proj.id
                                ? {
                                    ...p,
                                    status: 'completed',
                                    outputs: [{
                                        name: p.name.replace('.txt', '_resultados.zip'),
                                        type: 'zip',
                                        size: 'Procesado',
                                        downloadUrl: downloadUrl // Añadimos la URL real
                                    }]
                                }
                                : p
                        ));
                    }
                };

                eventSource.onerror = () => {
                    console.error("Error en el stream de logs");
                    eventSource.close();
                };

            } catch (error) {
                console.error(error);
                setLogs(prev => [...prev, {
                    id: generateId(),
                    timestamp: getTimestamp(),
                    message: `Error al procesar ${proj.name}`,
                    type: 'error'
                }]);
            }

            // Un pequeño delay entre proyectos si hay varios
            await new Promise(resolve => setTimeout(resolve, 500));
        }

        setIsProcessingDone(true);
    };

    const reset = () => {
        setIsProcessingDone(false);
        setAppState('input');
        setProjects([]);
        setLogs([]);
    };

    return (
        <div className="max-w-6xl mx-auto h-full flex flex-col">
            <div className="mb-6 flex-shrink-0">
                <h1 className={UI.Title}>Procesador Catastral Multiproyecto</h1>
                <p className={UI.Subtitle}>Gestión de proyectos GIS . Version 1.0 por mucho que le cueste a Jorge tener paciencia e ir poco a poco subiendo actualizaciones/p>
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

                        <div className="flex-1 overflow-y-auto pr-2 pb-2">
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
                    {isProcessingDone && (
                        <div className="mt-6 flex justify-center animate-in fade-in slide-in-from-bottom-4 duration-500">
                            <button
                                onClick={() => setAppState('results')}
                                className={`${UI.ButtonPrimary} px-12 py-3 text-lg shadow-xl shadow-blue-500/20`}
                            >
                                <CheckCircle className="mr-2" size={24} />
                                Ver Resultados y Descargar
                            </button>
                        </div>
                    )}
                </div>
            )}

            {appState === 'results' && (
                <ResultsView projects={projects} onReset={reset} />
            )}
        </div>
    );
}
