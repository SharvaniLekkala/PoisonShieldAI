const STORAGE_KEY = "poisonshield_sessions";

export const getSessions = () => {
  const data = localStorage.getItem(STORAGE_KEY);
  return data ? JSON.parse(data) : [];
};

export const saveSessions = (sessions) => {
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify(sessions)
  );
};

export const createSession = () => {
  const session = {
    id: Date.now().toString(),
    title: "New Chat",
    messages: []
  };

  const sessions = getSessions();

  sessions.unshift(session);

  saveSessions(sessions);

  return session;
};

export const updateSession = (
  sessionId,
  messages
) => {

  const sessions = getSessions();

  const updated = sessions.map((s) => {

    if (s.id === sessionId) {

      return {
        ...s,
        title:
          messages[0]?.text?.slice(0, 25) ||
          "New Chat",
        messages
      };
    }

    return s;
  });

  saveSessions(updated);
};

export const getSession = (id) => {
  return getSessions().find(
    (s) => s.id === id
  );
};
export const deleteSession = (
  sessionId
) => {

  const sessions =
    getSessions().filter(
      (s) =>
        s.id !== sessionId
    );

  saveSessions(sessions);

  return sessions;
};