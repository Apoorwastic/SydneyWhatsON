import EventCard from "./EventCard";
import "../styles/cards.css";

export default function EventGrid({ events, onGetTickets }) {
  return (
    <div className="grid">
      {events.map((e) => (
        <EventCard
          key={e.id}
          e={e}
          onGetTickets={onGetTickets}
        />
      ))}
    </div>
  );
}
