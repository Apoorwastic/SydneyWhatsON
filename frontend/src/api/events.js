export const fetchEvents = async () => {
  const res = await fetch(`${API_BASE}/events`);
  const data = await res.json();
  return data.events; // ✅ return ARRAY only
};
