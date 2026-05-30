import { useState, useEffect } from "react";

import API from "../services/api";

import Sidebar from "./Sidebar";
import ChatMessage from "./ChatMessage";
import {
  createSession,
  getSessions,
  updateSession,
  deleteSession
} from "../utils/sessionManager";


export default function ChatWindow() {

  const [sessions, setSessions] =
    useState([]);

  const [activeSession,
    setActiveSession] =
    useState(null);

  const [message,
    setMessage] =
    useState("");

  const [loading,
    setLoading] =
    useState(false);

  useEffect(() => {

    let stored =
      getSessions();

    if (stored.length === 0) {

      const first =
        createSession();

      stored = [first];
    }

    setSessions(stored);

    setActiveSession(
      stored[0].id
    );

  }, []);

  const currentSession =
    sessions.find(
      (s) =>
        s.id === activeSession
    );

  const handleNewChat = () => {

    const session =
      createSession();

    const updated =
      getSessions();

    setSessions(updated);

    setActiveSession(
      session.id
    );
  };
const handleDeleteChat = (sessionId) => {

  const updated = deleteSession(sessionId);

  setSessions(updated);

  if (activeSession === sessionId) {

    if (updated.length > 0) {

      setActiveSession(updated[0].id);

    } else {

      const newSession = createSession();

      setSessions([newSession]);

      setActiveSession(newSession.id);

    }
  }
};
  const sendMessage = async () => {

    if (!message.trim()) return;

    try {

      setLoading(true);

      const userMsg = {
        role: "user",
        text: message
      };

      const res =
        await API.post(
          "/chat",
          {
            message
          }
        );

      const botMsg = {
  role: "assistant",

  text:
    res.data.response,

  metadata: {

    status:
      res.data.status,

    security_status:
      res.data.security_status,

    retrieval_quality:
      res.data.retrieval_quality,

    risk_score:
      res.data.risk_score,

    retrieval_source:
      res.data.retrieval_source,

    retrieved_documents:
      res.data.retrieved_documents,

    reason:
      res.data.reason
  }
};

      const updatedMessages = [

        ...(currentSession?.messages || []),

        userMsg,
        botMsg
      ];

      updateSession(
        activeSession,
        updatedMessages
      );

      setSessions(
        getSessions()
      );

      setMessage("");

    } catch {

      alert(
        "Backend connection failed."
      );

    } finally {

      setLoading(false);
    }
  };

  return (

    <div
      style={{
        display: "flex"
      }}
    >

      <Sidebar
  sessions={sessions}
  activeSession={activeSession}
  onNewChat={handleNewChat}
  onSelectChat={setActiveSession}
  onDeleteChat={handleDeleteChat}
/>

      <div
        style={{
          flex: 1,
          padding: "20px"
        }}
      >

        <h1>
          PoisonShield AI
        </h1>

        <div
          style={{
            height: "70vh",
            overflowY: "auto",
            marginBottom: "20px"
          }}
        >

          {currentSession?.messages?.map(
            (msg, index) => (

              <ChatMessage
  key={index}
  role={msg.role}
  text={msg.text}
  metadata={msg.metadata}
/>

            )
          )}

        </div>

        <div
          style={{
            display: "flex",
            gap: "10px"
          }}
        >

          <input
            value={message}
            onChange={(e) =>
              setMessage(
                e.target.value
              )
            }
            placeholder="Ask something..."
            style={{
              flex: 1,
              padding: "12px"
            }}
          />

          <button
            onClick={sendMessage}
            disabled={loading}
          >
            {loading
              ? "Loading..."
              : "Send"}
          </button>

        </div>

      </div>

    </div>
  );
}