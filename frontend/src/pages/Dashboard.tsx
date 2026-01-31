import React from 'react';
import {
    Target,
    CheckCircle2,
    Clock,
    Zap,
    ChevronRight,
    Plus
} from 'lucide-react';
import NeumorphicBox from '../components/common/NeumorphicBox';

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
    return (
        <div className="space-y-10">
            {/* Top Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-3xl font-black text-slate-700 tracking-tight">Intelligence Dashboard</h2>
                    <p className="text-slate-500 font-medium">System status: <span className="text-green-500">All Agents Online</span></p>
                </div>
                <button className="flex items-center space-x-2 px-6 py-3 rounded-2xl font-bold text-blue-600 neumorphic-flat hover:neumorphic-pressed transition-all">
                    <Plus size={20} />
                    <span>Initialize Goal</span>
                </button>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard label="Active Goals" value="12" icon={Target} colorClass="text-blue-500" />
                <StatCard label="Completed" value="154" icon={CheckCircle2} colorClass="text-green-500" />
                <StatCard label="Efficiency" value="98%" icon={Zap} colorClass="text-orange-500" />
                <StatCard label="Saved Time" value="48h" icon={Clock} colorClass="text-purple-500" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Main Feed */}
                <div className="lg:col-span-2 space-y-6">
                    <NeumorphicBox variant="card" className="p-8">
                        <div className="flex items-center justify-between mb-8">
                            <h3 className="text-xl font-bold text-slate-700">Recent Orchestrations</h3>
                            <button className="text-sm font-bold text-blue-500 hover:underline">View All</button>
                        </div>

                        <div className="space-y-4">
                            {[
                                { title: 'Migrate Legacy DB to Postgres', time: '2h ago', status: 'IN PROGRESS', color: 'bg-blue-500' },
                                { title: 'Cloud Infrastructure Audit', time: '5h ago', status: 'COMPLETED', color: 'bg-green-500' },
                                { title: 'Security Patch Deployment', time: '1d ago', status: 'TODO', color: 'bg-amber-500' },
                            ].map((goal, i) => (
                                <div key={i} className="flex items-center justify-between p-5 rounded-2xl neumorphic-flat hover:neumorphic-pressed transition-all group">
                                    <div className="flex items-center space-x-4">
                                        <div className={`w-3 h-3 rounded-full ${goal.color}`} />
                                        <div>
                                            <h4 className="font-bold text-slate-700">{goal.title}</h4>
                                            <p className="text-xs text-slate-400 font-medium">Initiated {goal.time}</p>
                                        </div>
                                    </div>
                                    <div className="flex items-center space-x-4">
                                        <span className={`hidden sm:inline text-[10px] font-black tracking-widest px-3 py-1 rounded-full text-white ${goal.color}`}>
                                            {goal.status}
                                        </span>
                                        <ChevronRight size={18} className="text-slate-300 group-hover:text-slate-600 transition-colors" />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </NeumorphicBox>
                </div>

                {/* Side Panel */}
                <div className="space-y-8">
                    <NeumorphicBox variant="card" className="p-8">
                        <h3 className="text-xl font-bold text-slate-700 mb-8">Team Load</h3>
                        <div className="space-y-6">
                            {[
                                { name: 'Sarah Jenkins', role: 'Arch Agent', load: 85 },
                                { name: 'Michael Chen', role: 'Dev Agent', load: 45 },
                                { name: 'Emma Wilson', role: 'QA Agent', load: 30 },
                            ].map((member, i) => (
                                <div key={i} className="space-y-3">
                                    <div className="flex justify-between items-end">
                                        <div>
                                            <p className="font-bold text-slate-700 text-sm">{member.name}</p>
                                            <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">{member.role}</p>
                                        </div>
                                        <p className="text-xs font-black text-slate-600">{member.load}%</p>
                                    </div>
                                    <div className="h-3 rounded-full neumorphic-inset overflow-hidden p-0.5">
                                        <div
                                            className="h-full rounded-full bg-blue-500 transition-all duration-1000"
                                            style={{ width: `${member.load}%` }}
                                        />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </NeumorphicBox>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
