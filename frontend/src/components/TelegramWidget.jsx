import "../styles/telegram-widget.css";

export default function TelegramWidget() {
  return (
    <div className="telegram-widget">
      <div className="telegram-preview">
        <p>👋 Hi! Need help choosing an event?</p>
        <p className="muted">Chat with our AI assistant</p>
      </div>

      <a
        href="https://t.me/SydneyWhatsOnBot"
        target="_blank"
        rel="noopener noreferrer"
        className="telegram-button"
      >
        💬
      </a>
    </div>
  );
}
