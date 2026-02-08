import React, { useState } from 'react';
import { CheckCircle, FolderOpen, Download, FileArchive, FileCode, FolderTree, Layers, MessageCircle } from 'lucide-react';
import { Project } from '../types';
import { UI } from '../styles/ui';
import { ChatGIS } from './ChatGIS';

interface ResultsViewProps {
    projects: Project[];
    onReset: () => void;
}

export function ResultsView({ projects, onReset }: ResultsViewProps) {
    const [isChatOpen, setIsChatOpen] = useState(false);
    const [selectedTaskId, setSelectedTaskId] = useState<string>('');

    const openChat = (project: Project) => {
        // Extraer task_id de la downloadUrl (formato: /api/download/{task_id})
        const downloadUrl = project.outputs[0]?.downloadUrl || '';
        const taskId = downloadUrl.split('/').pop() || '';
        setSelectedTaskId(taskId);
        setIsChatOpen(true);
    };

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

                            {/* Botón de Chat */}
                            <button
                                onClick={() => openChat(project)}
                                className="flex items-center gap-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-4 py-2 rounded-lg font-medium transition-all shadow-lg hover:shadow-xl"
                            >
                                <MessageCircle size={18} />
                                Chat GIS
                            </button>
                        </div>

                        <div className="p-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {project.outputs.map((file, idx) => (
                                <div key={idx} className="bg-slate-950 hover:bg-slate-800 transition-colors border border-slate-800 p-4 rounded-lg flex items-center justify-between group col-span-1 md:col-span-2 lg:col-span-1">
                                    <div className="flex items-center gap-4">
                                        <div className={`p-2.5 rounded-lg ${file.type === 'zip' ? 'bg-yellow-500/10 text-yellow-400' :
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
                                    <button
                                        onClick={() => {
                                            if (file.downloadUrl) {
                                                window.open(file.downloadUrl, '_blank');
                                            } else {
                                                alert('El enlace de descarga no está disponible.');
                                            }
                                        }}
                                        className="p-2 hover:bg-blue-600 hover:text-white rounded-md text-slate-400 transition-colors bg-slate-900 border border-slate-800 group-hover:border-blue-500/50"
                                    >
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

            {/* Chat Modal */}
            {isChatOpen && (
                <ChatGIS
                    taskId={selectedTaskId}
                    isOpen={isChatOpen}
                    onClose={() => setIsChatOpen(false)}
                />
            )}
        </div>
    );
}
