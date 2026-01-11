import { formatEventDate } from "../utils/formatEventDate";
export default function EventCard({ e, onGetTickets }) {
  return (
    <div className="card">
      <img src={e.image_url} alt={e.title} />

      <div className="content">
        <h3>{e.title}</h3>

        

<div className="date">
  {formatEventDate(e.start_datetime)}
</div>



        <p>{e.description?.slice(0, 110)}...</p>

         <button
            className="ticket-btn"
            onClick={() => onGetTickets(e.ticket_url)}
          >
            GET TICKETS
          </button>
      </div>
    </div>
  );
}
