import logo from "../assets/logo.svg";

const CATEGORIES = [
  "all",
  "music",
  "food",
  "art",
  "sports",
  "movies",
  "tech"
];

export default function Header({
  search,
  setSearch,
  category,
  setCategory
}) {
  return (
    <header style={styles.header}>
      <div style={styles.logo}>
        <img src={logo} alt="Sydney What’s On" style={{ height: "42px" }} />
      </div>

      {/* ✅ CATEGORY FILTERS */}
      <div style={styles.categories}>
        {CATEGORIES.map((c) => (
          <button
            key={c}
            onClick={() => setCategory(c)}
            className={`category-btn ${
              category === c ? "active" : ""
            }`}
          >
            {c.toUpperCase()}
          </button>
        ))}
      </div>

      {/* SEARCH */}
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search events..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <span className="search-icon">🔍</span>
      </div>
    </header>
  );
}

const styles = {
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "18px 40px",
    background: "rgba(0,0,0,0.85)",
    position: "sticky",
    top: 0,
    zIndex: 10
  },
  logo: {
    display: "flex",
    alignItems: "center"
  },
  categories: {
    display: "flex",
    gap: "14px"
  }
};
