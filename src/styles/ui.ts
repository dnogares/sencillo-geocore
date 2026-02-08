export const UI = {
    // Layout
    Container: "min-h-screen bg-slate-950 text-slate-200 font-sans flex overflow-hidden",
    Sidebar: "w-20 lg:w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between transition-all duration-300",
    Main: "flex-1 flex flex-col relative overflow-hidden",
    Header: "h-16 border-b border-slate-800 bg-slate-950/50 backdrop-blur flex items-center justify-between px-6",
    Content: "flex-1 overflow-y-auto p-6 relative",

    // Components
    Card: "bg-slate-900 border border-slate-800 rounded-lg p-6 shadow-xl",
    ButtonPrimary: "bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-md font-medium flex items-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_15px_rgba(37,99,235,0.3)]",
    ButtonSecondary: "bg-slate-800 hover:bg-slate-700 text-slate-200 px-4 py-2 rounded-md font-medium flex items-center gap-2 transition-all border border-slate-700",
    InputZone: "border-2 border-dashed border-slate-700 hover:border-blue-500 hover:bg-slate-900/50 rounded-xl p-8 flex flex-col items-center justify-center transition-all cursor-pointer h-full min-h-[200px]",

    // Typography
    Title: "text-2xl font-bold text-white tracking-tight",
    Subtitle: "text-slate-400 text-sm",

    // States
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
