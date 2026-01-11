import { useEffect, useState } from "react";
import { formatEventDate } from "../utils/formatEventDate";
import "../styles/hero.css";

export default function HeroSlider({ events, onGetTickets }) {
  const slides = events.slice(0, 6);
  const [index, setIndex] = useState(0);

  // 🔥 FIX 1: reset slider when filtered events change
  useEffect(() => {
    setIndex(0);
  }, [events]);

  // auto-slide
  useEffect(() => {
    if (!slides.length) return;

    const id = setInterval(() => {
      setIndex((i) => (i + 1) % slides.length);
    }, 3000);

    return () => clearInterval(id);
  }, [slides.length]);

  if (!slides.length) return null;

  // 🔥 FIX 2: safety fallback (prevents white screen)
  const e = slides[index] || slides[0];

  return (
    <section className="hero">
      <div
        className="hero-slide"
        style={{ backgroundImage: `url(${e.image_url})` }}
      >
        {/* LCP image */}
        <img
          src={e.image_url}
          alt={e.title}
          className="hero-lcp-image"
          fetchpriority="high"
        />

        <div className="hero-overlay" />

        <div
          className="hero-arrow left"
          onClick={() =>
            setIndex(index === 0 ? slides.length - 1 : index - 1)
          }
        >
          ❮
        </div>

        <div
          className="hero-arrow right"
          onClick={() =>
            setIndex((index + 1) % slides.length)
          }
        >
          ❯
        </div>

        <div className="hero-content">
          <h1>{e.title}</h1>
          <h3>{e.category || "Live Music Festival"}</h3>

          <p>
            {formatEventDate(e.start_datetime)} • {e.venue}
          </p>

          <button
            className="ticket-btn"
            onClick={() => onGetTickets(e.ticket_url)}
          >
            GET TICKETS
          </button>
        </div>
      </div>
    </section>
  );
}
