import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Eye, EyeOff, Mail, Lock } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import NeumorphicBox from '../components/common/NeumorphicBox';

const loginSchema = z.object({
    email: z.string().email('Invalid email address'),
    password: z.string().min(6, 'Password must be at least 6 characters'),
});

type LoginForm = z.infer<typeof loginSchema>;

const Login: React.FC = () => {
    const [showPassword, setShowPassword] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const { login } = useAuth();
    const navigate = useNavigate();

    const { register, handleSubmit, formState: { errors } } = useForm<LoginForm>({
        resolver: zodResolver(loginSchema),
    });

    const onSubmit = async (data: LoginForm) => {
        setIsLoading(true);
        setError(null);
        try {
            const formData = new FormData();
            formData.append('username', data.email);
            formData.append('password', data.password);

            await login(formData);
            navigate('/dashboard');
        } catch (error: any) {
            setError(error.response?.data?.detail || 'Login failed. Please check your credentials.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Box className="min-h-screen flex items-center justify-center bg-[#e0e5ec] p-4">
            <NeumorphicBox variant="card" className="max-w-md w-full p-10">
                <div className="flex flex-col space-y-8">
                    <div className="text-center">
                        <h1 className="text-4xl font-black text-slate-700 mb-2">ORBIT</h1>
                        <p className="text-slate-500">Welcome Back</p>
                    </div>

                    {error && (
                        <div className="p-4 bg-red-50 text-red-500 rounded-xl text-sm border border-red-100 animate-pulse">
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                        <div>
                            <label className="block text-sm font-semibold text-slate-600 mb-2 ml-1">Email Address</label>
                            <div className="relative">
                                <Input
                                    {...register('email')}
                                    type="email"
                                    placeholder="name@example.com"
                                    className="w-full h-12 bg-[#e0e5ec] rounded-xl px-4 neumorphic-inset focus:outline-none transition-all"
                                />
                                <div className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400">
                                    <Mail size={18} />
                                </div>
                            </div>
                            {errors.email && <p className="text-red-500 text-xs mt-1 ml-1">{errors.email.message}</p>}
                        </div>

                        <div>
                            <label className="block text-sm font-semibold text-slate-600 mb-2 ml-1">Password</label>
                            <div className="relative">
                                <Input
                                    {...register('password')}
                                    type={showPassword ? 'text' : 'password'}
                                    placeholder="••••••••"
                                    className="w-full h-12 bg-[#e0e5ec] rounded-xl px-4 neumorphic-inset focus:outline-none transition-all"
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
                                >
                                    {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                                </button>
                            </div>
                            {errors.password && <p className="text-red-500 text-xs mt-1 ml-1">{errors.password.message}</p>}
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading}
                            className={`w-full h-14 rounded-xl font-bold text-slate-700 transition-all duration-200 
                ${isLoading ? 'neumorphic-pressed opacity-70' : 'neumorphic-flat active:neumorphic-pressed hover:scale-[1.01]'}`}
                        >
                            {isLoading ? 'Signing In...' : 'Sign In'}
                        </button>
                    </form>

                    <div className="text-center">
                        <p className="text-slate-500 text-sm">
                            Don't have an account?{' '}
                            <Link to="/register" className="text-blue-500 font-bold hover:underline">
                                Create Account
                            </Link>
                        </p>
                    </div>
                </div>
            </NeumorphicBox>
        </Box>
    );
};

// Simple Box for layout if needed
const Box = ({ children, className }: any) => <div className={className}>{children}</div>;
const Input = React.forwardRef<HTMLInputElement, any>((props, ref) => <input ref={ref} {...props} />);

export default Login;
