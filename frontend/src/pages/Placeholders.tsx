import React from 'react';
import NeumorphicBox from '../components/common/NeumorphicBox';
import { Construction } from 'lucide-react';

const PlaceholderPage = ({ title }: { title: string }) => (
    <div className="space-y-10">
        <div>
            <h2 className="text-3xl font-black text-slate-700 tracking-tight">{title}</h2>
            <p className="text-slate-500 font-medium">This module is currently being optimized by the AI Agent.</p>
        </div>

        <NeumorphicBox variant="card" className="p-20 flex flex-col items-center justify-center border-4 border-dashed border-[#d1d9e6]">
            <div className="p-8 rounded-full neumorphic-inset mb-8 text-slate-400">
                <Construction size={64} />
            </div>
            <h3 className="text-2xl font-black text-slate-700 mb-2">Under Construction</h3>
            <p className="text-slate-400 font-medium text-center max-w-sm">
                We're building a state-of-the-art interface for {title.toLowerCase()}. Stay tuned for the upcoming update.
            </p>

            <button
                disabled
                className="mt-10 px-8 py-3 rounded-2xl font-bold bg-[#e0e5ec] neumorphic-pressed text-slate-400 cursor-not-allowed"
            >
                Sync Module
            </button>
        </NeumorphicBox>
    </div>
);

export const Goals = () => <PlaceholderPage title="Strategic Goals" />;
export const Tasks = () => <PlaceholderPage title="Task Management" />;
export const Team = () => <PlaceholderPage title="Team Roster" />;
