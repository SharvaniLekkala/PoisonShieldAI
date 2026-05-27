import { useState } from "react";

import API from "../services/api";

import {
  Link
} from "react-router-dom";


export default function ChatWindow() {

  const [message, setMessage] = useState("");

  const [response, setResponse] = useState(() => {

  const saved = localStorage.getItem(
    "latest_response"
  );

  return saved ? JSON.parse(saved) : null;
});

  const [loading, setLoading] = useState(false);


  const sendMessage = async () => {

    if (!message.trim()) return;

    setLoading(true);

    try {

      const res = await API.post(
        "/chat",
        {
          message
        }
      );

      setResponse(res.data);

      // Store response globally
      localStorage.setItem(
        "latest_response",
        JSON.stringify(res.data)
      );

    } catch (error) {

      console.error(error);

      setResponse({
        response:
          "Backend connection failed."
      });

    } finally {

      setLoading(false);
    }
  };


  return (

    <div
      style={{
        maxWidth: "900px",
        margin: "40px auto",
        padding: "20px",
        fontFamily: "Arial",
        color: "#111827",
        background: "#ffffff",
        minHeight: "100vh"
      }}
    >

      <h1
        style={{
          textAlign: "center",
          marginBottom: "30px",
          color: "#111827"
        }}
      >
        PoisonShield AI
      </h1>


      {/* INPUT */}
      <div
        style={{
          display: "flex",
          gap: "10px"
        }}
      >

        <input
          type="text"
          placeholder="Ask something..."
          value={message}
          onChange={(e) =>
            setMessage(e.target.value)
          }
          style={{
            flex: 1,
            padding: "14px",
            borderRadius: "10px",
            border: "1px solid #171111",
            fontSize: "16px",
            color: "#111827",
            background: "#ffffff"
          }}
        />

        <button
          onClick={sendMessage}
          disabled={loading}
          style={{
            padding: "14px 22px",
            borderRadius: "10px",
            border: "none",
            background: "#111827",
            color: "#ffffff",
            cursor: "pointer",
            fontWeight: "bold"
          }}
        >
          {loading
            ? "Loading..."
            : "Send"}
        </button>

      </div>


      {/* RESPONSE */}
      {response && (

        <div
          style={{
            marginTop: "30px",
            padding: "25px",
            borderRadius: "16px",
            border: "1px solid #ddd",
            background: "#f9fafb",
            boxShadow:
              "0 4px 12px rgba(0,0,0,0.06)"
          }}
        >

          <h2
            style={{
              color: "#111827"
            }}
          >
            Response
          </h2>

          <p
            style={{
              lineHeight: "1.7",
              fontSize: "16px",
              whiteSpace: "pre-wrap",
              color: "#111827"
            }}
          >
            {response.response}
          </p>


          <Link
            to="/details"
            style={{
              display: "inline-block",
              marginTop: "20px",
              textDecoration: "none",
              color: "#2563eb",
              fontWeight: "bold"
            }}
          >
            View Workflow Details 
          </Link>

        </div>

      )}

    </div>
  );
}