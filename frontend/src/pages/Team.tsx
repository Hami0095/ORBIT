import React, { useState, useEffect } from 'react';
import {
    Plus,
    Trash2,
    UserPlus,
    Search,
    Award
} from 'lucide-react';
import NeumorphicBox from '../components/common/NeumorphicBox';
import { teamService } from '../services/api';

const Team = () => {
    const [team, setTeam] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [showAddModal, setShowAddModal] = useState(false);

    // Form State
    const [name, setName] = useState('');
    const [skills, setSkills] = useState('backend: 5, python: 4');
    const [hours, setHours] = useState(40);

    const fetchTeam = async () => {
        setIsLoading(true);
        try {
            const data = await teamService.getTeam();
            setTeam(data);
        } catch (err) {
            console.error("Failed to fetch team", err);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchTeam();
    }, []);

    const handleAddMember = async (e: React.FormEvent) => {
        e.preventDefault();
        // Parse skills "key: val, key: val"
        const skillList = skills.split(',').reduce((acc: any, curr) => {
            const [key, val] = curr.split(':').map(s => s.trim());
            if (key && val) acc[key] = parseInt(val);
            return acc;
        }, {});

        try {
            await teamService.addMember({
                name,
                skill_set: skillList,
                availability_hours: hours
            });
            setShowAddModal(false);
            setName('');
            setSkills('backend: 5, python: 4');
            fetchTeam();
        } catch (err) {
            alert("Failed to add member");
        }
    };

    return (
        <div className="space-y-10">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-3xl font-black text-slate-700 tracking-tight">Team Roster</h2>
                    <p className="text-slate-500 font-medium">Manage your human resources for AI task assignment.</p>
                </div>
                <button
                    onClick={() => setShowAddModal(true)}
                    className="flex items-center space-x-2 px-6 py-3 rounded-2xl font-bold text-blue-600 neumorphic-flat hover:neumorphic-pressed transition-all"
                >
                    <UserPlus size={20} />
                    <span>Add Member</span>
                </button>
            </div>

            {isLoading ? (
                <div className="flex justify-center p-20">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
                    {team.map((member) => (
                        <NeumorphicBox key={member.id} variant="card" className="p-8">
                            <div className="flex flex-col items-center">
                                <div className="w-20 h-20 rounded-full neumorphic-inset flex items-center justify-center text-blue-500 mb-4">
                                    <span className="text-2xl font-black">{member.name[0]}</span>
                                </div>
                                <h3 className="text-xl font-bold text-slate-700 mb-1">{member.name}</h3>
                                <p className="text-xs text-slate-400 font-bold uppercase tracking-widest mb-6">{member.availability_hours}h / Week</p>

                                <div className="w-full space-y-3">
                                    <div className="flex items-center space-x-2 text-slate-500 mb-2">
                                        <Award size={16} />
                                        <span className="text-xs font-bold uppercase tracking-tighter">Skill Set</span>
                                    </div>
                                    <div className="flex flex-wrap gap-2">
                                        {Object.entries(member.skill_set || {}).map(([skill, level]: [string, any]) => (
                                            <span key={skill} className="px-3 py-1 rounded-full neumorphic-flat text-[10px] font-black text-slate-600">
                                                {skill.toUpperCase()}: {level}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </NeumorphicBox>
                    ))}

                    {team.length === 0 && (
                        <div className="col-span-full">
                            <NeumorphicBox variant="flat" className="p-20 flex flex-col items-center justify-center border-2 border-dashed border-slate-300">
                                <p className="text-slate-400 font-bold">No team members onboarded yet.</p>
                            </NeumorphicBox>
                        </div>
                    )}
                </div>
            )}

            {/* Add Modal */}
            {showAddModal && (
                <div className="fixed inset-0 z-[100] flex items-center justify-center bg-[#e0e5ec]/80 backdrop-blur-sm p-4">
                    <NeumorphicBox variant="card" className="max-w-md w-full p-10">
                        <h3 className="text-2xl font-black text-slate-700 mb-8">Onboard Member</h3>
                        <form onSubmit={handleAddMember} className="space-y-6">
                            <div>
                                <label className="block text-sm font-semibold text-slate-600 mb-2">Full Name</label>
                                <input
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    className="w-full h-12 bg-[#e0e5ec] rounded-xl px-4 neumorphic-inset focus:outline-none"
                                    placeholder="e.g. Sarah Jenkins"
                                    required
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-semibold text-slate-600 mb-2">Skills (key: level, ...)</label>
                                <input
                                    value={skills}
                                    onChange={(e) => setSkills(e.target.value)}
                                    className="w-full h-12 bg-[#e0e5ec] rounded-xl px-4 neumorphic-inset focus:outline-none"
                                    placeholder="backend: 5, react: 4"
                                    required
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-semibold text-slate-600 mb-2">Availability (Hours/Week)</label>
                                <input
                                    type="number"
                                    value={hours}
                                    onChange={(e) => setHours(parseInt(e.target.value))}
                                    className="w-full h-12 bg-[#e0e5ec] rounded-xl px-4 neumorphic-inset focus:outline-none"
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
                                    Confirm
                                </button>
                            </div>
                        </form>
                    </NeumorphicBox>
                </div>
            )}
        </div>
    );
};

export default Team;
