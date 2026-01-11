# Sydney What’s On 🎉

Sydney What’s On is a full-stack event discovery platform that aggregates and displays upcoming events across Sydney from multiple public sources in near real time.

🔗 **Live Website:** https://sydneywhatson.netlify.app  
🔗 **Public API:** https://sydneywhatson.onrender.com/events  

<img width="1910" height="965" alt="SYDNEYEVENTS" src="https://github.com/user-attachments/assets/41010692-1380-4c78-b7e1-5136b152ccca" />

<img width="1917" height="910" alt="gettickets" src="https://github.com/user-attachments/assets/ee54bc5d-1101-4cbc-88b7-1c6ba69b1c59" />

<img width="1912" height="900" alt="search" src="https://github.com/user-attachments/assets/8d633344-15ed-4b00-a876-6eaf14cfd70f" />

---

## ✨ Features

- 📅 Aggregates upcoming events from multiple sources
- 🔄 Automated background scraping and data refresh
- 🔍 Live search and instant filtering
- 🎠 Featured events carousel
- 🗂️ Responsive event grid layout
- 📩 Ticket redirection with email modal
- 🤖 Telegram AI assistant for event discovery
- ⚡ Fast, lightweight frontend with modern UX

---

## 🛠️ Tech Stack

### Frontend
- React + Vite
- JavaScript (ES Modules)
- Custom CSS
- Hosted on **Netlify**

### Backend
- FastAPI (Python)
- PostgreSQL
- Background scheduler
- Hosted on **Render**

### Integrations
- Telegram Bot API
- Multiple public event listing sources

---

## 🚀 Deployment

- **Frontend:** Netlify (static build, environment-based API configuration)
- **Backend:** Render (FastAPI + PostgreSQL)
- **Database:** Render Managed PostgreSQL
- **Background Jobs:** In-process scheduler running alongside the API

---

## 🧠 Key Notes

### Event Scheduler
- A background scheduler runs automatically within the backend service
- Periodically scrapes multiple event sources
- Normalizes, deduplicates, and stores events in PostgreSQL
- Ensures fresh data without manual triggers or cron jobs

### Telegram Bot
- Integrated Telegram bot for conversational event discovery
- Allows users to explore events directly from Telegram
- Designed to scale into a full AI-powered city events assistant

### API Design
- Clean JSON-based REST API
- Single unified `/events` endpoint for frontend consumption
- Optimized for fast reads and frontend performance

---

## 🔮 Planned Improvements

- 🌍 Multi-city support
- 🔔 Push notifications for upcoming or trending events
- 📅 Advanced date and category filters
- 📈 Event popularity and recommendation logic
- 🧠 Smarter AI-based event suggestions

---

## 👤 Author

**Apoorwa**  
Full Stack Developer 

---

## 📜 License

Open-source project for learning, experimentation, and personal use.
