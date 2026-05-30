export default function ChatMessage({
  role,
  text,
  metadata
}) {

  const isUser =
    role === "user";

  return (

    <div
      style={{
        display: "flex",
        justifyContent:
          isUser
            ? "flex-end"
            : "flex-start",
        marginBottom: "10px"
      }}
    >

      <div
        style={{
          padding: "12px",
          borderRadius: "12px",
          maxWidth: "70%",
          background:
            isUser
              ? "#2563eb"
              : "#f3f4f6",
          color:
            isUser
              ? "#fff"
              : "#111827"
        }}
      >

        <div>
          {text}
        </div>

        {!isUser && metadata && (

          <details
            style={{
              marginTop: "12px",
              fontSize: "12px"
            }}
          >

            <summary
              style={{
                cursor: "pointer",
                fontWeight: "bold"
              }}
            >
               View Workflow Details
            </summary>

            <div
              style={{
                marginTop: "10px",
                lineHeight: "1.6"
              }}
            >

              <div>
                <strong>Status:</strong>{" "}
                {metadata.status}
              </div>

              <div>
                <strong>Security:</strong>{" "}
                {metadata.security_status}
              </div>

              <div>
                <strong>Retrieval:</strong>{" "}
                {metadata.retrieval_quality}
              </div>

              <div>
                <strong>Risk Score:</strong>{" "}
                {metadata.risk_score}
              </div>

              <div>
                <strong>Source:</strong>{" "}
                {metadata.retrieval_source}
              </div>

              <div>
                <strong>Documents:</strong>{" "}
                {
                  metadata
                    .retrieved_documents
                    ?.length || 0
                }
              </div>

              <div>
                <strong>Reason:</strong>{" "}
                {metadata.reason}
              </div>

            </div>

          </details>

        )}

      </div>

    </div>
  );
}