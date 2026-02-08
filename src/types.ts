export type AppState = 'input' | 'processing' | 'results';

export type LogEntry = {
    id: string;
    timestamp: string;
    message: string;
    type: 'info' | 'success' | 'warning' | 'error'
};

export type OutputFile = {
    name: string;
    type: 'gml' | 'xlsx' | 'json' | 'zip';
    size: string;
    downloadUrl?: string; // URL real del backend
};

export type Project = {
    id: string;
    name: string;
    originalFile: File;
    references: string[];
    status: 'pending' | 'processing' | 'completed' | 'error';
    outputs: OutputFile[];
};
