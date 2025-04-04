export function debounce(func, wait = 300, immediate = false) {
  let timeout;
  return (...args) => {
    const later = () => {
      timeout = null;
      if (!immediate) func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (immediate && !timeout) func(...args);
  };
}