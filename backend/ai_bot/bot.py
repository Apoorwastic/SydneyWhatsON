from events import find_events
from preferences import save_preference, get_preference

def handle_message(user_id: int, text: str):
    text = text.lower()

    # Preference detection
    for keyword in ["music", "comedy", "festival", "art", "cinema"]:
        if keyword in text:
            save_preference(user_id, keyword)
            return f"✅ Got it! I’ll look for {keyword} events in Sydney."

    pref = get_preference(user_id)
    if not pref:
        return "👋 Tell me what you like (music, comedy, art, cinema)."

    events = find_events(pref)

    if events.empty:
        return "😔 No matching events right now."

    reply = "🎉 Here are some events you may like:\n\n"
    for _, e in events.iterrows():
        reply += f"• {e['title']}\n  📍 {e['venue']}\n  🎟️ {e['ticket_url']}\n\n"

    return reply
