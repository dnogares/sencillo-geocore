import React, { useState } from 'react';
import { Map, Table, Settings, Activity, FolderOpen } from 'lucide-react';
import { UI } from './styles/ui';
import { Sidebar } from './components/Sidebar';
import { ProcessorSimple as Processor } from './components/ProcessorSimple';

export default function App() {
    const [activeTab, setActiveTab] = useState('processor');

    return (
        <div className={UI.Container}>
            <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
            <main className={UI.Main}>
                <header className={UI.Header}>
                    <div className="flex items-center gap-3">
                        <div className={`p-2 rounded-lg ${activeTab === 'processor' ? 'bg-blue-500/10 text-blue-400' : 'bg-slate-800 text-slate-400'
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
