import axios from "axios";

export const fetchEvents = async () => {
  const res = await fetch("https://sydneywhatson.onrender.com/events");
  return res.json();
};

