import axios from "axios";

export async function fetchEvents() {
  const res = await axios.get("http://localhost:8000/events");
  return res.data;
}
