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
    fetchEvents().then(setEvents);
  }, []);

  if (!events.length) return null;

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
