export const generateId = () => Math.random().toString(36).substr(2, 9);
export const getTimestamp = () => new Date().toLocaleTimeString('es-ES', { hour12: false });
