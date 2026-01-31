import React, { useState, useEffect } from 'react';
import {
    Target,
    CheckCircle2,
    Clock,
    Zap,
    ChevronRight,
    Plus,
    Users
} from 'lucide-react';
import NeumorphicBox from '../components/common/NeumorphicBox';
import { goalService, taskService, teamService } from '../services/api';
import { useNavigate } from 'react-router-dom';

const StatCard = ({ label, value, icon: Icon, colorClass }: { label: string, value: string, icon: any, colorClass: string }) => (
    <NeumorphicBox variant="flat" className="p-6">
        <div className="flex items-center space-x-4">
            <div className={`p-4 rounded-2xl neumorphic-flat ${colorClass}`}>
                <Icon size={24} />
            </div>
            <div>
                <p className="text-sm text-slate-500 font-medium">{label}</p>
                <p className="text-2xl font-black text-slate-700">{value}</p>
            </div>
        </div>
    </NeumorphicBox>
);

const Dashboard: React.FC = () => {
    const [stats, setStats] = useState({ goals: 0, tasks: 0, completed: 0, team: 0 });
    const [recentGoals, setRecentGoals] = useState<any[]>([]);
    const [teamMembers, setTeamMembers] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const navigate = useNavigate();

    const fetchDashboardData = async () => {
        setIsLoading(true);
        try {
            const [goals, tasks, team] = await Promise.all([
                goalService.getGoals(),
                taskService.getTasks(),
                teamService.getTeam()
            ]);

            const completed = tasks.filter((t: any) => t.status === 'DONE').length;

            setStats({
                goals: goals.length,
                tasks: tasks.length,
                completed,
                team: team.length
            });

            setRecentGoals(goals.slice(0, 3));
            setTeamMembers(team.slice(0, 3));
        } catch (err) {
            console.error("Dashboard sync error", err);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchDashboardData();
    }, []);

    return (
        <div className="space-y-10">
            {/* Top Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-3xl font-black text-slate-700 tracking-tight">Intelligence Overview</h2>
                    <p className="text-slate-500 font-medium">System status: <span className="text-green-500">Live Sync Active</span></p>
                </div>
                <button
                    onClick={() => navigate('/goals')}
                    className="flex items-center space-x-2 px-6 py-3 rounded-2xl font-bold text-blue-600 neumorphic-flat hover:neumorphic-pressed transition-all"
                >
                    <Plus size={20} />
                    <span>New Initiative</span>
                </button>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard label="Active Goals" value={stats.goals.toString()} icon={Target} colorClass="text-blue-500" />
                <StatCard label="Tasks Queue" value={stats.tasks.toString()} icon={Zap} colorClass="text-orange-500" />
                <StatCard label="Completed" value={stats.completed.toString()} icon={CheckCircle2} colorClass="text-green-500" />
                <StatCard label="Team Size" value={stats.team.toString()} icon={Users} colorClass="text-purple-500" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Recent Initiatives */}
                <div className="lg:col-span-2 space-y-6">
                    <NeumorphicBox variant="card" className="p-8">
                        <div className="flex items-center justify-between mb-8">
                            <h3 className="text-xl font-bold text-slate-700">Recent Initiatives</h3>
                            <button
                                onClick={() => navigate('/goals')}
                                className="text-sm font-bold text-blue-500 hover:underline"
                            >
                                Manage All
                            </button>
                        </div>

                        <div className="space-y-4">
                            {recentGoals.map((goal, i) => (
                                <div key={i} className="flex items-center justify-between p-5 rounded-2xl neumorphic-flat hover:neumorphic-pressed transition-all group cursor-pointer" onClick={() => navigate('/goals')}>
                                    <div className="flex items-center space-x-4">
                                        <div className={`w-3 h-3 rounded-full ${goal.status === 'COMPLETED' ? 'bg-green-500' : 'bg-blue-500 animate-pulse'}`} />
                                        <div>
                                            <h4 className="font-bold text-slate-700">{goal.title}</h4>
                                            <p className="text-xs text-slate-400 font-medium">Status: {goal.status}</p>
                                        </div>
                                    </div>
                                    <ChevronRight size={18} className="text-slate-300 group-hover:text-slate-600 transition-colors" />
                                </div>
                            ))}
                            {recentGoals.length === 0 && (
                                <p className="text-center text-slate-400 py-10 font-medium">No results found.</p>
                            )}
                        </div>
                    </NeumorphicBox>
                </div>

                {/* Team Snapshot */}
                <div className="space-y-8">
                    <NeumorphicBox variant="card" className="p-8">
                        <h3 className="text-xl font-bold text-slate-700 mb-8">Agent Snapshot</h3>
                        <div className="space-y-6">
                            {teamMembers.map((member, i) => (
                                <div key={i} className="space-y-3">
                                    <div className="flex justify-between items-end">
                                        <div>
                                            <p className="font-bold text-slate-700 text-sm">{member.name}</p>
                                            <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">
                                                {Object.keys(member.skill_set || {}).slice(0, 2).join(' / ') || 'Generalist'}
                                            </p>
                                        </div>
                                        <p className="text-xs font-black text-slate-600">{member.availability_hours}h</p>
                                    </div>
                                    <div className="h-3 rounded-full neumorphic-inset overflow-hidden p-0.5">
                                        <div
                                            className="h-full rounded-full bg-blue-500"
                                            style={{ width: `${Math.min(100, (member.availability_hours / 40) * 100)}%` }}
                                        />
                                    </div>
                                </div>
                            ))}
                            {teamMembers.length === 0 && (
                                <p className="text-center text-slate-400 py-10 font-medium">No members added.</p>
                            )}
                        </div>
                    </NeumorphicBox>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
