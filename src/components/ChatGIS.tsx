import React, { useState, useEffect, useRef } from 'react';
import { MessageCircle, Send, Sparkles, X, Loader2 } from 'lucide-react';

interface ChatMessage {
    role: 'user' | 'assistant';
    content: string;
}

interface ChatGISProps {
    taskId: string;
    isOpen: boolean;
    onClose: () => void;
}

export function ChatGIS({ taskId, isOpen, onClose }: ChatGISProps) {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [hasApiKey, setHasApiKey] = useState(true);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Preguntas sugeridas
    const suggestedQuestions = [
        '¿Qué afecciones tiene el terreno?',
        'Resume el expediente catastral',
        '¿Cuál es la superficie total?',
        '¿Hay espacios protegidos?'
    ];

    // Auto-scroll al final
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Mensaje de bienvenida
    useEffect(() => {
        if (isOpen && messages.length === 0) {
            setMessages([{
                role: 'assistant',
                content: '👋 Hola! He analizado tu expediente catastral. ¿En qué puedo ayudarte?\n\nPuedo explicarte:\n- Afecciones legales y ambientales\n- Superficies y coordenadas\n- Referencias procesadas\n- Interpretación de resultados'
            }]);
        }
    }, [isOpen]);

    const sendMessage = async (message: string) => {
        if (!message.trim() || isLoading) return;

        const userMessage: ChatMessage = { role: 'user', content: message };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await fetch(`/api/chat/${taskId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            if (!response.ok) {
                throw new Error('Error al comunicar con el chat');
            }

            const data = await response.json();

            // Verificar si hay problema con la API key
            if (data.response.includes('API Key de Gemini no configurada')) {
                setHasApiKey(false);
            }

            const assistantMessage: ChatMessage = {
                role: 'assistant',
                content: data.response
            };
            setMessages(prev => [...prev, assistantMessage]);

        } catch (error) {
            console.error('Error en el chat:', error);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: '❌ Error al procesar tu mensaje. Por favor, intenta de nuevo.'
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSuggestedQuestion = (question: string) => {
        sendMessage(question);
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-in fade-in duration-300">
            <div className="bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl w-full max-w-3xl h-[700px] flex flex-col animate-in zoom-in-95 duration-300">

                {/* Header */}
                <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-4 rounded-t-2xl flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-white/20 rounded-lg backdrop-blur-sm">
                            <Sparkles className="text-white" size={24} />
                        </div>
                        <div>
                            <h3 className="text-white font-semibold text-lg">Chat Especialista en GIS</h3>
                            <p className="text-blue-100 text-sm">Powered by Gemini Flash 2.0</p>
                        </div>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-white/20 rounded-lg transition-colors"
                    >
                        <X className="text-white" size={20} />
                    </button>
                </div>

                {/* Messages Area */}
                <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-slate-950/50">
                    {messages.map((msg, idx) => (
                        <div
                            key={idx}
                            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-in slide-in-from-bottom-2 duration-300`}
                        >
                            <div
                                className={`max-w-[80%] rounded-2xl px-4 py-3 ${msg.role === 'user'
                                        ? 'bg-blue-600 text-white'
                                        : 'bg-slate-800 text-slate-100 border border-slate-700'
                                    }`}
                            >
                                {msg.role === 'assistant' && (
                                    <div className="flex items-center gap-2 mb-2 text-blue-400">
                                        <Sparkles size={16} />
                                        <span className="text-xs font-semibold">ASISTENTE GIS</span>
                                    </div>
                                )}
                                <div className="whitespace-pre-wrap text-sm leading-relaxed">
                                    {msg.content}
                                </div>
                            </div>
                        </div>
                    ))}

                    {isLoading && (
                        <div className="flex justify-start animate-in fade-in duration-300">
                            <div className="bg-slate-800 border border-slate-700 rounded-2xl px-4 py-3 flex items-center gap-2">
                                <Loader2 className="text-blue-400 animate-spin" size={16} />
                                <span className="text-slate-400 text-sm">Analizando datos...</span>
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>

                {/* Suggested Questions (only show when no messages yet or after assistant response) */}
                {messages.length <= 2 && !isLoading && (
                    <div className="px-6 pb-3">
                        <p className="text-xs text-slate-500 mb-2">Preguntas sugeridas:</p>
                        <div className="flex flex-wrap gap-2">
                            {suggestedQuestions.map((question, idx) => (
                                <button
                                    key={idx}
                                    onClick={() => handleSuggestedQuestion(question)}
                                    className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 border border-slate-600 text-slate-300 text-sm rounded-full transition-colors"
                                >
                                    {question}
                                </button>
                            ))}
                        </div>
                    </div>
                )}

                {/* API Key Warning */}
                {!hasApiKey && (
                    <div className="px-6 pb-3">
                        <div className="bg-amber-900/30 border border-amber-700 rounded-lg p-3 text-sm text-amber-200">
                            ⚠️ <strong>API Key no configurada.</strong> Configura <code className="bg-amber-950/50 px-1 rounded">GEMINI_API_KEY</code> en Easypanel para usar el chat.
                        </div>
                    </div>
                )}

                {/* Input Area */}
                <div className="p-4 border-t border-slate-800 bg-slate-900/50">
                    <form
                        onSubmit={(e) => {
                            e.preventDefault();
                            sendMessage(input);
                        }}
                        className="flex gap-2"
                    >
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Pregunta sobre el expediente..."
                            disabled={isLoading}
                            className="flex-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50"
                        />
                        <button
                            type="submit"
                            disabled={isLoading || !input.trim()}
                            className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 py-3 rounded-xl font-medium transition-all flex items-center gap-2 shadow-lg hover:shadow-xl"
                        >
                            {isLoading ? (
                                <Loader2 className="animate-spin" size={20} />
                            ) : (
                                <>
                                    <Send size={20} />
                                    Enviar
                                </>
                            )}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}
