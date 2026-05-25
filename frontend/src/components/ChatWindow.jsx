import { useState } from "react";
import API from "../services/api";

function ChatWindow() {

    const [message, setMessage] = useState("");
    const [response, setResponse] = useState(null);
    const [loading, setLoading] = useState(false);

    const sendMessage = async () => {

        if (!message.trim()) {
            alert("Please enter a message");
            return;
        }

        setLoading(true);

        try {

            const res = await API.post("/chat", {
                message: message
            });

            console.log("Backend Response:", res.data);

            setResponse(res.data);

        } catch (error) {

            console.error("Connection Error:", error);

            alert("Backend connection failed");

        } finally {

            setLoading(false);
        }
    };

    return (

        <div
            style={{
                padding: "30px",
                fontFamily: "Arial"
            }}
        >

            <h1>PoisonShield AI</h1>

            <div
                style={{
                    marginTop: "20px"
                }}
            >

                <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Enter query..."
                    style={{
                        width: "400px",
                        padding: "10px",
                        fontSize: "16px"
                    }}
                />

                <button
                    onClick={sendMessage}
                    style={{
                        marginLeft: "10px",
                        padding: "10px 20px",
                        cursor: "pointer"
                    }}
                >
                    Send
                </button>

            </div>

            {loading && (
                <p style={{ marginTop: "20px" }}>
                    Loading...
                </p>
            )}

            {response && (

                <div
                    style={{
                        marginTop: "30px",
                        border: "1px solid #ccc",
                        padding: "20px",
                        borderRadius: "10px",
                        width: "600px"
                    }}
                >

                    <h2>Response Details</h2>

                    <h3>Status</h3>
                    <p>{response.status || "N/A"}</p>

                    <h3>Trust Score</h3>
                    <p>
                        {response.trust_score !== undefined
                            ? response.trust_score
                            : "N/A"}
                    </p>
                    <h3>Memory Status</h3>
                    <p>{response.memory_status}</p>

                    
                    <h3>Response</h3>
                    <p>{response.response || "No response returned"}</p>

                    <h3>Reason</h3>
                    <p>{response.reason || "No issues detected"}</p>

                </div>

            )}

        </div>
    );
}

export default ChatWindow;