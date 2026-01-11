Project Report: Sydney What’s On – Event Discovery Platform
1. Overview
Sydney What’s On is a full-stack web application designed to aggregate, normalize, and present upcoming events happening across Sydney from multiple public sources. The platform automates data collection, ensures regular updates, and delivers event information through a modern web interface and a Telegram bot.
The system is built with a focus on automation, scalability, and real-time usability.



2. Key Features
🔍 Event Search & Discovery
A dedicated search bar allows users to quickly filter events by title in real time.
Search results dynamically update as the user types, improving discoverability.
🎟️ Get Tickets
Each event includes a “Get Tickets” action.
Users are redirected to the official source platform for secure ticket booking.
🤖 Telegram Bot Integration
A Telegram bot provides event access outside the website.
Users can browse and query events directly from Telegram, increasing reach and accessibility.
🔄 Automated Data Refresh (Every 20 Minutes)
An in-app scheduler runs automatically every 20 minutes.
It refreshes event data, updates existing entries, and prevents duplicates without manual intervention or external cron jobs.

3. Tech Stack
Frontend
React (Vite)
JavaScript (ES6+)
CSS
Netlify
Backend
Python
FastAPI
Playwright
AsyncIO
Database
PostgreSQL (Render Managed)
Automation & Integrations
Internal scheduler (20-minute refresh cycle)
Telegram Bot API
Deployment
Render (Backend + Database)
Netlify (Frontend)
4. Approach


The system follows a modular, service-oriented architecture:
Scraper Layer: Playwright-based scrapers collect event data from multiple sources
Scheduler Layer: Automatically triggers scraping every 20 minutes
Backend API Layer: FastAPI exposes normalized event data via REST endpoints
Database Layer: PostgreSQL stores structured, de-duplicated events
Client Layer: React frontend and Telegram bot consume the same API
This design ensures scalability, separation of concerns, and consistent data delivery.

5. Challenges Faced
Inconsistent Data Sources
Event data varied widely in structure and completeness, requiring robust normalization.
Reliable Background Automation
Maintaining consistent scheduled execution within a hosted environment required careful lifecycle handling.
Production Integration Stability
Ensuring seamless communication between independently deployed frontend, backend, and database services.
6. Improvements & Future Enhancements
Multi-City Support – Extend the platform beyond Sydney
Push Notifications – Alert users about upcoming or trending events
Personalized Recommendations – Rank events based on interests or popularity
7. Conclusion
Sydney What’s On demonstrates a production-ready, automated event discovery platform with scheduled data ingestion, a clean API, multi-platform access, and a modern user interface. The system is designed to scale easily and adapt to additional cities, features, and integrations.

