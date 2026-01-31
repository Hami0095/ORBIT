import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Mail, Lock, User as UserIcon } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import NeumorphicBox from '../components/common/NeumorphicBox';

const registerSchema = z.object({
    name: z.string().min(2, 'Name must be at least 2 characters'),
    email: z.string().email('Invalid email address'),
    password: z.string().min(6, 'Password must be at least 6 characters'),
});

type RegisterForm = z.infer<typeof registerSchema>;

const Register: React.FC = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const { register: authRegister } = useAuth();
    const navigate = useNavigate();

    const { register, handleSubmit, formState: { errors } } = useForm<RegisterForm>({
        resolver: zodResolver(registerSchema),
    });

    const onSubmit = async (data: RegisterForm) => {
        setIsLoading(true);
        setError(null);
        try {
            await authRegister(data);
            navigate('/login');
        } catch (error: any) {
            setError(error.response?.data?.detail || 'Registration failed. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-[#e0e5ec] p-4">
            <NeumorphicBox variant="card" className="max-w-md w-full p-10">
                <div className="flex flex-col space-y-8">
                    <div className="text-center">
                        <h1 className="text-4xl font-black text-slate-700 mb-2">ORBIT</h1>
                        <p className="text-slate-500">Create account</p>
                    </div>

                    {error && (
                        <div className="p-4 bg-red-50 text-red-500 rounded-xl text-sm border border-red-100">
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                        <div>
                            <label className="block text-sm font-semibold text-slate-600 mb-2 ml-1">Full Name</label>
                            <div className="relative">
                                <input
                                    {...register('name')}
                                    placeholder="John Doe"
                                    className="w-full h-12 bg-[#e0e5ec] rounded-xl px-4 neumorphic-inset focus:outline-none"
                                />
                                <div className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400">
                                    <UserIcon size={18} />
                                </div>
                            </div>
                            {errors.name && <p className="text-red-500 text-xs mt-1 ml-1">{errors.name.message}</p>}
                        </div>

                        <div>
                            <label className="block text-sm font-semibold text-slate-600 mb-2 ml-1">Email</label>
                            <div className="relative">
                                <input
                                    {...register('email')}
                                    type="email"
                                    placeholder="name@example.com"
                                    className="w-full h-12 bg-[#e0e5ec] rounded-xl px-4 neumorphic-inset focus:outline-none"
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
                                <input
                                    {...register('password')}
                                    type="password"
                                    placeholder="••••••••"
                                    className="w-full h-12 bg-[#e0e5ec] rounded-xl px-4 neumorphic-inset focus:outline-none"
                                />
                                <div className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400">
                                    <Lock size={18} />
                                </div>
                            </div>
                            {errors.password && <p className="text-red-500 text-xs mt-1 ml-1">{errors.password.message}</p>}
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading}
                            className={`w-full h-14 rounded-xl font-bold text-slate-700 transition-all duration-200 
                ${isLoading ? 'neumorphic-pressed opacity-70' : 'neumorphic-flat active:neumorphic-pressed hover:scale-[1.01]'}`}
                        >
                            {isLoading ? 'Creating Account...' : 'Register Now'}
                        </button>
                    </form>

                    <div className="text-center">
                        <p className="text-slate-500 text-sm">
                            Already have an account?{' '}
                            <Link to="/login" className="text-blue-500 font-bold hover:underline">
                                Sign In
                            </Link>
                        </p>
                    </div>
                </div>
            </NeumorphicBox>
        </div>
    );
};

export default Register;
