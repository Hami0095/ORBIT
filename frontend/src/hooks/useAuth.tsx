import { useState, useEffect, createContext, useContext } from 'react';
import { authService } from '../services/api';

interface AuthContextType {
    user: any;
    token: string | null;
    loading: boolean;
    login: (formData: FormData) => Promise<void>;
    register: (data: any) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [user, setUser] = useState<any>(null);
    const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const initAuth = async () => {
            if (token) {
                try {
                    // You might need a /users/me endpoint for this
                    // const userData = await authService.getCurrentUser();
                    // setUser(userData);
                } catch (err) {
                    console.error("Failed to fetch user", err);
                    logout();
                }
            }
            setLoading(false);
        };
        initAuth();
    }, [token]);

    const login = async (formData: FormData) => {
        const data = await authService.login(formData);
        const accessToken = data.access_token;
        localStorage.setItem('token', accessToken);
        setToken(accessToken);
    };

    const register = async (data: any) => {
        await authService.register(data);
    };

    const logout = () => {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
