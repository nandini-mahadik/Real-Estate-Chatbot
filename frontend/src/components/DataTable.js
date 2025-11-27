import React from 'react';

export default function DataTable({ rows }) {
    if (!rows || rows.length === 0) return <div>No data available.</div>;

    const columns = Object.keys(rows[0]);

    return (
        <table className="table table-bordered mt-3">
            <thead>
                <tr>
                    {columns.map(col => <th key={col}>{col}</th>)}
                </tr>
            </thead>
            <tbody>
                {rows.map((row, i) => (
                    <tr key={i}>
                        {columns.map(col => <td key={col}>{row[col]}</td>)}
                    </tr>
                ))}
            </tbody>
        </table>
    );
}
