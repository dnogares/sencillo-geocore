import React, { useEffect, useRef } from 'react';
import { Terminal } from 'lucide-react';
import { LogEntry } from '../types';

interface ProcessingTerminalProps {
    logs: LogEntry[];
}

export function ProcessingTerminal({ logs }: ProcessingTerminalProps) {
    const endRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        endRef.current?.scrollIntoView({ behavior: 'smooth' });
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
            <div className="flex-1 overflow-y-auto p-4 space-y-1">
                {logs.map((log) => (
                    <div key={log.id} className="flex gap-3 animate-in fade-in slide-in-from-left-2 duration-300">
                        <span className="text-slate-600 select-none">[{log.timestamp}]</span>
                        <span className={`${log.type === 'error' ? 'text-red-400' :
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
}
