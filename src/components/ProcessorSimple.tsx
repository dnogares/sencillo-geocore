import React, { useState } from 'react';
import { Upload, Play, FileText, Trash2, Loader2, Download, CheckCircle } from 'lucide-react';
import { Project } from '../types';
import { UI } from '../styles/ui';
import { generateId } from '../utils/helpers';

export function ProcessorSimple() {
    const [projects, setProjects] = useState<Project[]>([]);
    const [isProcessing, setIsProcessing] = useState(false);
    const [currentProject, setCurrentProject] = useState<string | null>(null);

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;
        if (!files) return;

        const newProjects: Project[] = [];

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            if (file.name.endsWith('.txt')) {
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
        }

        setProjects(prev => [...prev, ...newProjects]);
    };

    const removeProject = (id: string) => {
        setProjects(prev => prev.filter(p => p.id !== id));
    };

    const startProcessing = async () => {
        if (projects.length === 0 || isProcessing) return;

        setIsProcessing(true);

        for (const proj of projects) {
            try {
                setCurrentProject(proj.name);

                const formData = new FormData();
                formData.append('file', proj.originalFile);

                // Petición síncrona que espera a que termine
                const response = await fetch('/api/process-sync', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error(`Error HTTP ${response.status}`);
                }

                const data = await response.json();

                if (data.success && data.download_url) {
                    // Marcar como completado
                    setProjects(prev => prev.map(p =>
                        p.id === proj.id
                            ? {
                                ...p,
                                status: 'completed',
                                outputs: [{
                                    name: p.name.replace('.txt', '_resultados.zip'),
                                    type: 'zip',
                                    size: data.file_size || 'Procesado',
                                    downloadUrl: data.download_url
                                }]
                            }
                            : p
                    ));
                } else {
                    throw new Error(data.error || 'Error desconocido');
                }

            } catch (error) {
                console.error('Error procesando:', error);
                setProjects(prev => prev.map(p =>
                    p.id === proj.id
                        ? { ...p, status: 'error' as const }
                        : p
                ));
            }
        }

        setIsProcessing(false);
        setCurrentProject(null);
    };

    const completedCount = projects.filter(p => p.status === 'completed').length;
    const pendingProjects = projects.filter(p => p.status === 'pending');

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-8">
            <div className="max-w-6xl mx-auto space-y-6">
                {/* Header */}
                <div className="text-center space-y-2">
                    <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                        Procesador GIS Catastral
                    </h1>
                    <p className="text-slate-400">Sube archivos .txt con referencias catastrales</p>
                </div>

                {/* Upload Section */}
                {!isProcessing && (
                    <div className={UI.card}>
                        <label className="flex flex-col items-center gap-4 p-8 border-2 border-dashed border-slate-700 rounded-lg cursor-pointer hover:border-blue-500 hover:bg-slate-800/50 transition-all">
                            <Upload size={48} className="text-blue-400" />
                            <div className="text-center">
                                <span className="text-lg font-medium text-slate-200">Click para subir archivos</span>
                                <p className="text-sm text-slate-400 mt-1">Archivos .txt con referencias catastrales</p>
                            </div>
                            <input
                                type="file"
                                multiple
                                accept=".txt"
                                onChange={handleFileUpload}
                                className="hidden"
                            />
                        </label>
                    </div>
                )}

                {/* Projects List */}
                {projects.length > 0 && !isProcessing && (
                    <div className={UI.card}>
                        <h2 className="text-xl font-bold text-slate-200 mb-4">
                            Archivos Cargados ({projects.length})
                        </h2>
                        <div className="space-y-2">
                            {projects.map(proj => (
                                <div key={proj.id} className="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg">
                                    <div className="flex items-center gap-3">
                                        <FileText size={20} className="text-blue-400" />
                                        <div>
                                            <div className="font-medium text-slate-200">{proj.name}</div>
                                            <div className="text-sm text-slate-400">{proj.references.length} referencias</div>
                                        </div>
                                    </div>
                                    {proj.status === 'completed' ? (
                                        <CheckCircle size={20} className="text-emerald-400" />
                                    ) : (
                                        <button
                                            onClick={() => removeProject(proj.id)}
                                            className="p-2 hover:bg-red-500/20 rounded-lg transition-colors"
                                        >
                                            <Trash2 size={18} className="text-red-400" />
                                        </button>
                                    )}
                                </div>
                            ))}
                        </div>
                        <button
                            onClick={startProcessing}
                            disabled={pendingProjects.length === 0}
                            className="mt-4 w-full flex items-center justify-center gap-
2 px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 disabled:from-slate-700 disabled:to-slate-700 disabled:cursor-not-allowed rounded-lg font-medium text-white transition-all"
                        >
                            <Play size={20} />
                            Procesar {pendingProjects.length} archivo{pendingProjects.length !== 1 ? 's' : ''}
                        </button>
                    </div>
                )}

                {/* Processing Status */}
                {isProcessing && (
                    <div className={UI.card}>
                        <div className="text-center space-y-4 py-8">
                            <Loader2 size={64} className="text-blue-400 animate-spin mx-auto" />
                            <div>
                                <h3 className="text-2xl font-bold text-slate-200">Procesando...</h3>
                                <p className="text-slate-400 mt-2">{currentProject}</p>
                                <p className="text-sm text-slate-500 mt-4">
                                    {completedCount} de {projects.length} completados
                                </p>
                            </div>
                            <div className="max-w-md mx-auto bg-slate-800/50 rounded-lg p-4 text-left text-sm">
                                <p className="text-slate-300">ℹ️ El procesamiento puede tardar varios minutos.</p>
                                <p className="text-slate-400 mt-2">Los logs detallados estarán en el archivo <code className="text-cyan-400">log.txt</code> dentro del ZIP.</p>
                            </div>
                        </div>
                    </div>
                )}

                {/* Results */}
                {projects.some(p => p.status === 'completed') && !isProcessing && (
                    <div className={UI.card}>
                        <h2 className="text-xl font-bold text-slate-200 mb-4">
                            Resultados ({completedCount})
                        </h2>
                        <div className="space-y-3">
                            {projects.filter(p => p.status === 'completed').map(proj => (
                                <div key={proj.id} className="p-4 bg-emerald-950/30 border border-emerald-900/50 rounded-lg">
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <div className="font-medium text-emerald-100">{proj.name}</div>
                                            <div className="text-sm text-emerald-400">Procesado exitosamente</div>
                                        </div>
                                        {proj.outputs[0]?.downloadUrl && (
                                            <a
                                                href={proj.outputs[0].downloadUrl}
                                                download
                                                className="flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 rounded-lg font-medium text-white transition-colors"
                                            >
                                                <Download size={18} />
                                                Descargar ZIP
                                            </a>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
