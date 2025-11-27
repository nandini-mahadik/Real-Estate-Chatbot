import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

import ChatInput from './components/ChatInput';
import ResponseCard from './components/ResponseCard';
import TrendChart from './components/TrendChart';
import DataTable from './components/DataTable';

import { analyze } from './api';

export default function App() {
    const [loading, setLoading] = useState(false);
    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);

    async function handleSend(query) {
        setLoading(true);
        setError(null);

        try {
            const res = await analyze(query);
            setResponse(res);
        } catch (err) {
            setError(err?.response?.data?.error || 'Server error');
        }

        setLoading(false);
    }

    return (
        <div className="container mt-4">

            <h2>Mini Real Estate Analysis Chatbot</h2>
            <p className="text-muted">Try: "Analyze Wakad", "Compare Aundh and Baner"</p>

            <ChatInput onSend={handleSend} />

            {loading && <div>Loading...</div>}
            {error && <div className="alert alert-danger">{error}</div>}

            {response && (
                <div>
                    <ResponseCard summary={response.summary} />

                    <h5>Chart</h5>
                    <TrendChart
                        data={response.trend}
                        multi={typeof response.trend === "object" && !Array.isArray(response.trend)}
                    />

                    <h5 className="mt-3">Filtered Data</h5>
                    <DataTable rows={response.table} />
                </div>
            )}

        </div>
    );
}
