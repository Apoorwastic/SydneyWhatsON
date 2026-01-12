import { useEffect, useState } from "react";
import Header from "./components/Header";
import HeroSlider from "./components/HeroSlider";
import EventGrid from "./components/EventGrid";
import EmailModal from "./components/EmailModal";
import TelegramWidget from "./components/TelegramWidget";
import { fetchEvents } from "./api/events";
import "./styles/theme.css";

export default function App() {
  const [events, setEvents] = useState([]);
  const [search, setSearch] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [ticketUrl, setTicketUrl] = useState(null);

  useEffect(() => {
    // ✅ 1. Load cached events immediately (prevents white page)
    const cached = localStorage.getItem("events_cache");
    if (cached) {
      setEvents(JSON.parse(cached));
    }

    // ✅ 2. Fetch fresh events in background
    fetchEvents()
      .then((data) => {
        if (Array.isArray(data) && data.length) {
          setEvents(data);
          localStorage.setItem("events_cache", JSON.stringify(data));
        }
      })
      .catch(() => {
        // ❌ Do nothing — cached data stays visible
      });
  }, []);

  // ✅ 3. NEVER return null (prevents blank screen)
  if (!events.length) {
    return <p style={{ padding: "2rem" }}>Loading events…</p>;
  }

  // 🔥 LIVE SEARCH FILTER
  const filteredEvents = events
    .filter((e) =>
      e.title.toLowerCase().includes(search.toLowerCase())
    )
    .sort((a, b) => {
      const q = search.toLowerCase();
      return a.title.toLowerCase().startsWith(q) ? -1 : 1;
    });

  return (
    <>
      <Header search={search} setSearch={setSearch} />

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

      {/* 🔥 TELEGRAM AI ASSISTANT WIDGET */}
      <TelegramWidget botUsername="SydneyWhatsOnBot" />
    </>
  );
}
