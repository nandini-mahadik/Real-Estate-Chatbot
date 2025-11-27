import axios from 'axios';

const API_BASE = "http://127.0.0.1:8000/api";

export async function analyze(query) {
    const response = await axios.post(`${API_BASE}/analyze/`, { query });
    return response.data;
}
