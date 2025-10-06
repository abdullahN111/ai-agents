export const generateSlug = (title) => {
  return title
    .toLowerCase()
    .replace(/\?/g, "")
    .replace(/[^\w ]+/g, "")
    .replace(/ +/g, "-");
};
