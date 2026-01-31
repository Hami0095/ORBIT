import React from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import {
    BarChart2,
    Target,
    CheckSquare,
    Users,
    LogOut,
    LayoutDashboard,
    Menu,
    X
} from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import NeumorphicBox from '../components/common/NeumorphicBox';

const SidebarItem = ({ to, icon: Icon, label }: { to: string, icon: any, label: string }) => {
    return (
        <NavLink to={to} className="w-full">
            {({ isActive }) => (
                <div
                    className={`flex items-center space-x-4 w-full p-4 rounded-2xl transition-all duration-200 
            ${isActive ? 'neumorphic-pressed text-blue-500' : 'hover:neumorphic-flat text-slate-500'}`}
                >
                    <Icon size={20} />
                    <span className="font-semibold text-sm">{label}</span>
                </div>
            )}
        </NavLink>
    );
};

const DashboardLayout: React.FC = () => {
    const { logout } = useAuth();
    const navigate = useNavigate();
    const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div className="flex h-screen bg-[#e0e5ec] overflow-hidden">
            {/* Sidebar - Desktop */}
            <aside className="hidden md:flex w-72 flex-col p-6 space-y-8">
                <NeumorphicBox variant="card" className="h-full p-6 flex flex-col">
                    <div className="mb-12 text-center p-4">
                        <h2 className="text-3xl font-black text-slate-700 tracking-tighter">
                            ORBIT
                        </h2>
                    </div>

                    <nav className="flex-1 space-y-4">
                        <SidebarItem to="/dashboard" icon={LayoutDashboard} label="Dashboard" />
                        <SidebarItem to="/goals" icon={Target} label="Strategic Goals" />
                        <SidebarItem to="/tasks" icon={CheckSquare} label="Task Queue" />
                        <SidebarItem to="/team" icon={Users} label="Team Roster" />
                    </nav>

                    <div className="mt-auto border-t border-slate-200 pt-6 space-y-4">
                        <SidebarItem to="/analytics" icon={BarChart2} label="Analytics" />
                        <button
                            onClick={handleLogout}
                            className="flex items-center space-x-4 w-full p-4 rounded-2xl text-red-500 hover:neumorphic-flat transition-all"
                        >
                            <LogOut size={20} />
                            <span className="font-semibold text-sm">Logout</span>
                        </button>
                    </div>
                </NeumorphicBox>
            </aside>

            {/* Main Content Area */}
            <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
                {/* Mobile Header */}
                <header className="md:hidden flex items-center justify-between p-4 bg-[#e0e5ec]">
                    <h1 className="text-2xl font-black text-slate-700">ORBIT</h1>
                    <button
                        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                        className="p-3 rounded-xl neumorphic-flat"
                    >
                        {isMobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
                    </button>
                </header>

                {/* Scrollable Content */}
                <div className="flex-1 overflow-y-auto p-4 md:p-8">
                    <div className="max-w-6xl mx-auto">
                        <Outlet />
                    </div>
                </div>
            </main>

            {/* Mobile Menu Overlay */}
            {isMobileMenuOpen && (
                <div className="fixed inset-0 z-50 md:hidden bg-[#e0e5ec] p-6 animate-in fade-in slide-in-from-top duration-300">
                    <div className="flex justify-end mb-8">
                        <button onClick={() => setIsMobileMenuOpen(false)} className="p-3 rounded-xl neumorphic-flat">
                            <X size={20} />
                        </button>
                    </div>
                    <nav className="space-y-4">
                        <SidebarItem to="/dashboard" icon={LayoutDashboard} label="Dashboard" />
                        <SidebarItem to="/goals" icon={Target} label="Strategic Goals" />
                        <SidebarItem to="/tasks" icon={CheckSquare} label="Task Queue" />
                        <SidebarItem to="/team" icon={Users} label="Team Roster" />
                    </nav>
                </div>
            )}
        </div>
    );
};

export default DashboardLayout;
