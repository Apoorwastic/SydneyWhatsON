export const categorizeEvent = (title = "") => {
  const t = title.toLowerCase();

  if (t.match(/concert|music|gig|dj|band|live/)) return "music";
  if (t.match(/food|wine|beer|dining|taste/)) return "food";
  if (t.match(/art|exhibition|gallery|museum/)) return "art";
  if (t.match(/football|cricket|soccer|tennis|match|sports/)) return "sports";
  if (t.match(/movie|film|cinema|screening/)) return "movies";
  if (t.match(/tech|startup|ai|coding|developer|hackathon/)) return "tech";

  return "other";
};
