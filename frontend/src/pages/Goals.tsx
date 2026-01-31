import React, { useState, useEffect } from 'react';
import {
    Target,
    Plus,
    Play,
    Clock,
    CheckCircle2,
    AlertCircle,
    Loader2,
    ListTodo
} from 'lucide-react';
import NeumorphicBox from '../components/common/NeumorphicBox';
import { goalService, orchestrateService } from '../services/api';
import { useNavigate } from 'react-router-dom';

const Goals = () => {
    const [goals, setGoals] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [showAddModal, setShowAddModal] = useState(false);
    const [orchestratingId, setOrchestratingId] = useState<number | null>(null);
    const navigate = useNavigate();

    // New Goal State
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');

    const fetchGoals = async () => {
        setIsLoading(true);
        try {
            const data = await goalService.getGoals();
            setGoals(data);
        } catch (err) {
            console.error("Failed to fetch goals", err);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchGoals();
    }, []);

    const handleCreateGoal = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await goalService.createGoal({ title, description });
            setShowAddModal(false);
            setTitle('');
            setDescription('');
            fetchGoals();
        } catch (err) {
            alert("Failed to create goal");
        }
    };

    const handleRunOrchestrator = async (goalId: number) => {
        setOrchestratingId(goalId);
        try {
            const res = await orchestrateService.startOrchestration(goalId);
            if (res.orchestration_result?.status === 'completed') {
                alert("AI Agent Finished! Tasks have been generated.");
                navigate('/tasks');
            } else {
                alert("Orchestration in progress or failed. Check logs.");
            }
        } catch (err) {
            console.error(err);
            alert("Orchestration pipeline failed.");
        } finally {
            setOrchestratingId(null);
            fetchGoals(); // Refresh status
        }
    };

    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'COMPLETED': return <CheckCircle2 size={16} className="text-green-500" />;
            case 'IN_PROGRESS': return <Loader2 size={16} className="text-blue-500 animate-spin" />;
            case 'FAILED': return <AlertCircle size={16} className="text-red-500" />;
            default: return <Clock size={16} className="text-slate-400" />;
        }
    };

    return (
        <div className="space-y-10">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-3xl font-black text-slate-700 tracking-tight">Strategic Goals</h2>
                    <p className="text-slate-500 font-medium">Define objectives and let AI Agents handle the logistics.</p>
                </div>
                <button
                    onClick={() => setShowAddModal(true)}
                    className="flex items-center space-x-2 px-6 py-3 rounded-2xl font-bold text-blue-600 neumorphic-flat hover:neumorphic-pressed transition-all"
                >
                    <Plus size={20} />
                    <span>New Goal</span>
                </button>
            </div>

            {isLoading ? (
                <div className="flex justify-center p-20">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
                </div>
            ) : (
                <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
                    {goals.map((goal) => (
                        <NeumorphicBox key={goal.id} variant="card" className="p-8">
                            <div className="flex justify-between items-start mb-6">
                                <div className="flex items-center space-x-3">
                                    <div className="p-3 rounded-xl neumorphic-inset text-blue-500">
                                        <Target size={24} />
                                    </div>
                                    <div>
                                        <h3 className="text-xl font-bold text-slate-700">{goal.title}</h3>
                                        <div className="flex items-center space-x-2 mt-1">
                                            {getStatusIcon(goal.status)}
                                            <span className="text-[10px] font-black uppercase tracking-widest text-slate-400">{goal.status}</span>
                                        </div>
                                    </div>
                                </div>

                                {goal.status !== 'COMPLETED' && (
                                    <button
                                        onClick={() => handleRunOrchestrator(goal.id)}
                                        disabled={orchestratingId === goal.id}
                                        className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-black tracking-widest transition-all
                      ${orchestratingId === goal.id ? 'neumorphic-pressed opacity-50' : 'neumorphic-flat text-blue-600 hover:scale-105'}`}
                                    >
                                        {orchestratingId === goal.id ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />}
                                        <span>{orchestratingId === goal.id ? 'RUNNING...' : 'TRIGGER AI'}</span>
                                    </button>
                                )}

                                {goal.status === 'COMPLETED' && (
                                    <button
                                        onClick={() => navigate('/tasks')}
                                        className="flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-black tracking-widest neumorphic-flat text-green-600"
                                    >
                                        <ListTodo size={14} />
                                        <span>VIEW TASKS</span>
                                    </button>
                                )}
                            </div>

                            <p className="text-slate-500 text-sm leading-relaxed mb-6 italic">
                                "{goal.description}"
                            </p>

                            <div className="flex justify-between items-center pt-6 border-t border-slate-200">
                                <div className="flex -space-x-2">
                                    {[1, 2].map(i => (
                                        <div key={i} className="w-8 h-8 rounded-full neumorphic-flat border-2 border-[#e0e5ec] flex items-center justify-center text-[10px] font-bold text-slate-400">
                                            AI
                                        </div>
                                    ))}
                                </div>
                                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-tight">Created by System Admin</p>
                            </div>
                        </NeumorphicBox>
                    ))}

                    {goals.length === 0 && (
                        <div className="col-span-full">
                            <NeumorphicBox variant="flat" className="p-20 flex flex-col items-center justify-center border-2 border-dashed border-slate-300 text-center">
                                <p className="text-slate-400 font-bold mb-4">No objectives defined yet.</p>
                                <button
                                    onClick={() => setShowAddModal(true)}
                                    className="px-6 py-2 rounded-xl neumorphic-flat text-blue-500 font-bold text-sm"
                                >
                                    Create Your First Goal
                                </button>
                            </NeumorphicBox>
                        </div>
                    )}
                </div>
            )}

            {/* Add Modal */}
            {showAddModal && (
                <div className="fixed inset-0 z-[100] flex items-center justify-center bg-[#e0e5ec]/80 backdrop-blur-sm p-4">
                    <NeumorphicBox variant="card" className="max-w-md w-full p-10">
                        <h3 className="text-2xl font-black text-slate-700 mb-8">Define Objective</h3>
                        <form onSubmit={handleCreateGoal} className="space-y-6">
                            <div>
                                <label className="block text-sm font-semibold text-slate-600 mb-2">Goal Title</label>
                                <input
                                    value={title}
                                    onChange={(e) => setTitle(e.target.value)}
                                    className="w-full h-12 bg-[#e0e5ec] rounded-xl px-4 neumorphic-inset focus:outline-none"
                                    placeholder="e.g. Migration to AWS"
                                    required
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-semibold text-slate-600 mb-2">Detailed Description</label>
                                <textarea
                                    value={description}
                                    onChange={(e) => setDescription(e.target.value)}
                                    className="w-full h-32 bg-[#e0e5ec] rounded-xl p-4 neumorphic-inset focus:outline-none resize-none"
                                    placeholder="Explain exactly what needs to be achieved..."
                                    required
                                />
                            </div>
                            <div className="flex space-x-4 pt-4">
                                <button
                                    type="button"
                                    onClick={() => setShowAddModal(false)}
                                    className="flex-1 py-4 rounded-xl font-bold text-slate-500 neumorphic-flat"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    className="flex-1 py-4 rounded-xl font-bold text-blue-600 neumorphic-flat active:neumorphic-pressed"
                                >
                                    Create Goal
                                </button>
                            </div>
                        </form>
                    </NeumorphicBox>
                </div>
            )}
        </div>
    );
};

export default Goals;
