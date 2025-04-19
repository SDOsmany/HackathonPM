// config/api.ts
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://hackathonpm.onrender.com';

export const API_ENDPOINTS = {
    RAG: `${API_BASE_URL}/api/rag`,
    GENERATE_PLAN: `${API_BASE_URL}/api/plans/generate`,
};