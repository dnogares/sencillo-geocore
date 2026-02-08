import React from 'react';
import { Map, Table, Settings, Activity, Layers } from 'lucide-react';
import { UI } from '../styles/ui';

interface SidebarProps {
    activeTab: string;
    setActiveTab: (tab: string) => void;
}

export function Sidebar({ activeTab, setActiveTab }: SidebarProps) {
    const menuItems = [
        { id: 'processor', icon: <Activity size={24} />, label: 'Procesador', disabled: false },
        { id: 'map', icon: <Map size={24} />, label: 'Visor Mapa', disabled: true },
        { id: 'data', icon: <Table size={24} />, label: 'Visor Datos', disabled: true },
        { id: 'settings', icon: <Settings size={24} />, label: 'Configuración', disabled: true },
    ];

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
                            className={`w-full flex items-center p-3 rounded-lg transition-all ${activeTab === item.id
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
}
