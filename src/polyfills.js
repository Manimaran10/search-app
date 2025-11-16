if (typeof window === "undefined") {
  global.localStorage = {
    getItem() { return null; },
    setItem() {},
    removeItem() {}
  };
}