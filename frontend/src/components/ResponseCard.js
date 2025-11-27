import React from 'react';

export default function ResponseCard({ summary }) {
    return (
        <div className="card mb-3">
            <div className="card-body">
                <h5>Summary</h5>
                <p>{summary}</p>
            </div>
        </div>
    );
}
