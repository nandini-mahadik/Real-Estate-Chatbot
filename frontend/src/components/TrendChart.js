import React from "react";
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Legend } from "recharts";

export default function TrendChart({ data, multi = false }) {
    if (!data) return null;

    if (multi) {
        return (
            <>
                {Object.keys(data).map(area => (
                    <div key={area} className="mb-4">
                        <h6>{area}</h6>

                        <LineChart width={600} height={250} data={data[area]}>
                            <Line type="monotone" dataKey="Price" stroke="blue" />
                            <Line type="monotone" dataKey="Demand" stroke="green" />
                            <CartesianGrid stroke="#ccc" />
                            <XAxis dataKey="Year" />
                            <YAxis />
                            <Tooltip />
                        </LineChart>

                    </div>
                ))}
            </>
        );
    }

    return (
        <LineChart width={700} height={300} data={data}>
            <Line type="monotone" dataKey="Price" stroke="blue" />
            <Line type="monotone" dataKey="Demand" stroke="green" />
            <CartesianGrid stroke="#ccc" />
            <XAxis dataKey="Year" />
            <YAxis />
            <Tooltip />
            <Legend />
        </LineChart>
    );
}
