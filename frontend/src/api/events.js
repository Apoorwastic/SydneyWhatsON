const API_BASE =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export const fetchEvents = async () => {
  const res = await fetch(`${API_BASE}/events`);
  return res.json();
};
