import React, { useState, useEffect } from 'react';
import {
    CheckSquare,
    Clock,
    User,
    ArrowUpRight,
    Filter,
    CheckCircle2,
    Calendar,
    Zap
} from 'lucide-react';
import NeumorphicBox from '../components/common/NeumorphicBox';
import { taskService, teamService } from '../services/api';

const Tasks = () => {
    const [tasks, setTasks] = useState<any[]>([]);
    const [team, setTeam] = useState<Record<number, string>>({});
    const [isLoading, setIsLoading] = useState(true);

    const fetchData = async () => {
        setIsLoading(true);
        try {
            const [taskData, teamData] = await Promise.all([
                taskService.getTasks(),
                teamService.getTeam()
            ]);

            const teamMap = teamData.reduce((acc: any, member: any) => {
                acc[member.id] = member.name;
                return acc;
            }, {});

            setTeam(teamMap);
            setTasks(taskData);
        } catch (err) {
            console.error("Failed to fetch tasks/team", err);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const getPriorityColor = (score: number) => {
        if (score > 0.8) return 'text-red-500';
        if (score > 0.5) return 'text-orange-500';
        return 'text-blue-500';
    };

    return (
        <div className="space-y-10">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-3xl font-black text-slate-700 tracking-tight">Task Queue</h2>
                    <p className="text-slate-500 font-medium">Orchestrated intelligence applied to active workflows.</p>
                </div>
                <button className="flex items-center space-x-2 px-6 py-3 rounded-2xl font-bold text-slate-600 neumorphic-flat hover:neumorphic-pressed transition-all">
                    <Filter size={20} />
                    <span>Active Filter</span>
                </button>
            </div>

            {isLoading ? (
                <div className="flex justify-center p-20">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
                </div>
            ) : (
                <div className="space-y-6">
                    {tasks.map((task) => (
                        <NeumorphicBox key={task.id} variant="card" className="p-6">
                            <div className="flex flex-col md:flex-row md:items-center gap-6">
                                {/* Status Icon */}
                                <div className="flex-shrink-0">
                                    <div className={`w-14 h-14 rounded-2xl neumorphic-inset flex items-center justify-center 
                    ${task.status === 'DONE' ? 'text-green-500' : 'text-slate-400'}`}>
                                        {task.status === 'DONE' ? <CheckCircle2 size={24} /> : <CheckSquare size={24} />}
                                    </div>
                                </div>

                                {/* Main Content */}
                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center space-x-3 mb-1">
                                        <h3 className="text-lg font-bold text-slate-700 truncate">{task.title}</h3>
                                        <div className="flex items-center space-x-1">
                                            <Zap size={12} className={getPriorityColor(task.priority_score)} />
                                            <span className={`text-[10px] font-black ${getPriorityColor(task.priority_score)}`}>
                                                {Math.round(task.priority_score * 100)}% PRIORITY
                                            </span>
                                        </div>
                                    </div>
                                    <p className="text-sm text-slate-500 line-clamp-2 leading-snug">
                                        {task.description}
                                    </p>
                                </div>

                                {/* Metadata */}
                                <div className="md:w-72 flex flex-wrap md:flex-nowrap items-center gap-6 justify-between border-t md:border-t-0 md:border-l border-slate-200 pt-4 md:pt-0 md:pl-6">
                                    <div className="flex flex-col space-y-1">
                                        <div className="flex items-center space-x-2 text-slate-400">
                                            <User size={14} />
                                            <span className="text-[10px] font-bold uppercase tracking-widest">Assigned To</span>
                                        </div>
                                        <p className="text-xs font-black text-slate-600">
                                            {team[task.assigned_to] || 'UNASSIGNED'}
                                        </p>
                                    </div>

                                    <div className="flex flex-col space-y-1">
                                        <div className="flex items-center space-x-2 text-slate-400">
                                            <Calendar size={14} />
                                            <span className="text-[10px] font-bold uppercase tracking-widest">Due Date</span>
                                        </div>
                                        <p className="text-xs font-black text-slate-600">
                                            {task.due_date ? new Date(task.due_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : 'TBD'}
                                        </p>
                                    </div>

                                    <button className="p-3 rounded-xl neumorphic-flat hover:neumorphic-pressed transition-all text-slate-400 hover:text-blue-500">
                                        <ArrowUpRight size={20} />
                                    </button>
                                </div>
                            </div>
                        </NeumorphicBox>
                    ))}

                    {tasks.length === 0 && (
                        <NeumorphicBox variant="flat" className="p-20 flex flex-col items-center justify-center border-2 border-dashed border-slate-300">
                            <Clock size={48} className="text-slate-300 mb-4" />
                            <p className="text-slate-400 font-bold">Queue is empty. Trigger an AI Agent to generate tasks.</p>
                        </NeumorphicBox>
                    )}
                </div>
            )}
        </div>
    );
};

export default Tasks;
