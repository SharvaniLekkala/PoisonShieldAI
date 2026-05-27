import { Link } from "react-router-dom";


export default function Details() {

  const response = JSON.parse(
    localStorage.getItem("latest_response")
  );

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

      <h1>
        Workflow Details
      </h1>

      <Link to="/">
        ← Back to Chat
      </Link>

      {!response ? (

        <p style={{ marginTop: "20px" }}>
          No response data available.
        </p>

      ) : (

        <div
          style={{
            marginTop: "25px",
            padding: "25px",
            borderRadius: "16px",
            border: "1px solid #ddd",
            background: "#f9fafb"
          }}
        >

          <p>
            <strong>Status:</strong>{" "}
            {response.status}
          </p>

          <p>
            <strong>Trust Score:</strong>{" "}
            {response.trust_score}
          </p>

          <p>
            <strong>Memory Status:</strong>{" "}
            {response.memory_status}
          </p>

          <p>
            <strong>Retrieval Source:</strong>{" "}
            {response.retrieval_source}
          </p>

          <p>
            <strong>Reason:</strong>{" "}
            {response.reason}
          </p>

          <div style={{ marginTop: "20px" }}>

            <strong>
              Retrieved Documents:
            </strong>

            {response.retrieved_documents?.length > 0 ? (

              <ul>

                {response.retrieved_documents.map(
                  (doc, index) => (

                    <li
                      key={index}
                      style={{
                        marginTop: "10px",
                        lineHeight: "1.6"
                      }}
                    >
                      {doc}
                    </li>
                  )
                )}

              </ul>

            ) : (

              <p>
                No documents retrieved.
              </p>

            )}

          </div>

        </div>

      )}

    </div>
  );
}