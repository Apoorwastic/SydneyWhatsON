import { useEffect, useState } from "react";
import Header from "./components/Header";
import HeroSlider from "./components/HeroSlider";
import EventGrid from "./components/EventGrid";
import EmailModal from "./components/EmailModal";
import TelegramWidget from "./components/TelegramWidget";
import { fetchEvents } from "./api/events";
import { categorizeEvent } from "./utils/categorizeEvent";
import "./styles/theme.css";

export default function App() {
  const [events, setEvents] = useState([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("all"); // ✅ ADD
  const [modalOpen, setModalOpen] = useState(false);
  const [ticketUrl, setTicketUrl] = useState(null);

  useEffect(() => {
    // ✅ Load cached events immediately
    const cached = localStorage.getItem("events_cache");
    if (cached) {
      const parsed = JSON.parse(cached).map((e) => ({
        ...e,
        category: e.category || categorizeEvent(e.title)
      }));
      setEvents(parsed);
    }

    // ✅ Fetch fresh events in background
    fetchEvents()
      .then((data) => {
        if (Array.isArray(data) && data.length) {
          const categorized = data.map((e) => ({
            ...e,
            category: categorizeEvent(e.title)
          }));
          setEvents(categorized);
          localStorage.setItem("events_cache", JSON.stringify(categorized));
        }
      })
      .catch(() => {
        // Keep cached data
      });
  }, []);

  // ❌ Never return null
  if (!events.length) {
    return <p style={{ padding: "2rem" }}>Loading events…</p>;
  }

  // 🔥 SEARCH + CATEGORY FILTER
  const filteredEvents = events
    .filter((e) => {
      const matchSearch = e.title
        .toLowerCase()
        .includes(search.toLowerCase());

      const matchCategory =
        category === "all" || e.category === category;

      return matchSearch && matchCategory;
    })
    .sort((a, b) => {
      const q = search.toLowerCase();
      return a.title.toLowerCase().startsWith(q) ? -1 : 1;
    });

  return (
    <>
      <Header
        search={search}
        setSearch={setSearch}
        category={category}       // ✅ ADD
        setCategory={setCategory} // ✅ ADD
      />

      <HeroSlider
        events={filteredEvents}
        onGetTickets={(url) => {
          setTicketUrl(url);
          setModalOpen(true);
        }}
      />

      <section className="events-section">
        <h2>Upcoming Events</h2>

        <EventGrid
          events={filteredEvents}
          onGetTickets={(url) => {
            setTicketUrl(url);
            setModalOpen(true);
          }}
        />
      </section>

      <EmailModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        ticketUrl={ticketUrl}
      />

      {/* 🔥 TELEGRAM AI ASSISTANT */}
      <TelegramWidget botUsername="SydneyWhatsOnBot" />
    </>
  );
}
