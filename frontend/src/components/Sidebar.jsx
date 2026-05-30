export default function Sidebar({
  sessions,
  activeSession,
  onNewChat,
  onSelectChat,
  onDeleteChat
}) {

  return (

    <div
      style={{
        width: "250px",
        borderRight: "1px solid #ddd",
        padding: "15px",
        height: "100vh",
        background: "#f8fafc"
      }}
    >

      <button
        onClick={onNewChat}
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "20px",
          cursor: "pointer"
        }}
      >
        + New Chat
      </button>

      {sessions.map((session) => (

  <div
    key={session.id}
    style={{
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      padding: "10px",
      marginBottom: "8px",
      borderRadius: "8px",
      background:
        activeSession === session.id
          ? "#000000"
          : "#000000"
    }}
  >

    <div
      onClick={() =>
        onSelectChat(session.id)
      }
      style={{
        flex: 1,
        cursor: "pointer"
      }}
    >
      {session.title}
    </div>

    <button
      onClick={(e) => {
        e.stopPropagation();
        onDeleteChat(session.id);
      }}
      style={{
        border: "none",
        background: "transparent",
        cursor: "pointer"
      }}
    >
      D
    </button>

  </div>

))}

    </div>
  );
}