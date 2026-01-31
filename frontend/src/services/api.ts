import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
    baseURL: API_BASE_URL,
});

// Inject token into requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Handle expired tokens
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export const authService = {
    async login(formData: FormData) {
        // login needs application/x-www-form-urlencoded
        const params = new URLSearchParams();
        formData.forEach((value, key) => {
            params.append(key, value as string);
        });

        const response = await api.post('/auth/login/access-token', params, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });
        return response.data;
    },

    async register(data: any) {
        const response = await api.post('/auth/register', data);
        return response.data;
    },

    async getCurrentUser() {
        const response = await api.get('/users/me'); // Assuming this exists or will exist
        return response.data;
    }
};

export const goalService = {
    async getGoals() {
        const response = await api.get('/goals/');
        return response.data;
    },
    async createGoal(data: any) {
        const response = await api.post('/goals/', data);
        return response.data;
    }
};

export const taskService = {
    async getTasks(goalId?: number) {
        const url = goalId ? `/tasks/?goal_id=${goalId}` : '/tasks/';
        const response = await api.get(url);
        return response.data;
    }
};

export const teamService = {
    async getTeam() {
        const response = await api.get('/team/');
        return response.data;
    },
    async addMember(data: any) {
        const response = await api.post('/team/', data);
        return response.data;
    }
};

export const orchestrateService = {
    async startOrchestration(goalId: number) {
        const response = await api.post(`/orchestrate/start/${goalId}`);
        return response.data;
    },
    async startWithPrompt(goalText: string) {
        const response = await api.post('/orchestrate/start', { goal_text: goalText });
        return response.data;
    }
};

export default api;
