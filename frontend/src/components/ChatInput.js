import React, { useState } from 'react';

export default function ChatInput({ onSend }) {
    const [text, setText] = useState("");

    function submit() {
        if (!text.trim()) return;
        onSend(text);
        setText("");
    }

    return (
        <div className="input-group mb-3">
            <input
                className="form-control"
                placeholder="Ask something... e.g. Analyze Wakad"
                value={text}
                onChange={e => setText(e.target.value)}
                onKeyDown={e => e.key === "Enter" && submit()}
            />
            <button className="btn btn-primary" onClick={submit}>Send</button>
        </div>
    );
}
