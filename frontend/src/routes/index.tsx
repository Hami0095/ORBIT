import { Routes, Route, Navigate } from 'react-router-dom';
import Login from '../pages/Login';
import Register from '../pages/Register';
import Dashboard from '../pages/Dashboard';
import Goals from '../pages/Goals';
import Tasks from '../pages/Tasks';
import Team from '../pages/Team';
import DashboardLayout from '../layouts/DashboardLayout';
import { useAuth } from '../hooks/useAuth';

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
    const { token, loading } = useAuth();

    if (loading) return null; // Or a loader
    if (!token) return <Navigate to="/login" replace />;

    return <>{children}</>;
};

const AppRoutes = () => {
    return (
        <Routes>
            {/* Public Routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Protected Dashboard Routes */}
            <Route
                path="/"
                element={
                    <ProtectedRoute>
                        <DashboardLayout />
                    </ProtectedRoute>
                }
            >
                <Route index element={<Navigate to="/dashboard" replace />} />
                <Route path="dashboard" element={<Dashboard />} />
                <Route path="goals" element={<Goals />} />
                <Route path="tasks" element={<Tasks />} />
                <Route path="team" element={<Team />} />
            </Route>

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
    );
};

export default AppRoutes;
