export function formatEventDate(raw) {
  if (!raw) return "";

  // 1. Remove "When"
  let text = raw.replace(/^When/i, "").trim();

  // 2. Match dates like:
  // Thursday 19 February
  // Sunday 8 March
  const dateRegex =
    /(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s+\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)/gi;

  const matches = text.match(dateRegex);

  if (!matches || matches.length === 0) {
    return text; // fallback: show raw text
  }

  // 3. Only one date
  if (matches.length === 1) {
    return matches[0];
  }

  // 4. Range
  const first = matches[0];
  const last = matches[matches.length - 1];

  return `${first} – ${last}`;
}
