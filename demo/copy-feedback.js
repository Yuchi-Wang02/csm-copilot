/* Clipboard completion belongs to the selection that initiated it. */
(function (root) {
  "use strict";
  function create(writeText = (text) => root.navigator.clipboard.writeText(text)) {
    const attempts = new WeakMap();
    function reset(button, label) {
      attempts.set(button, {});
      button.textContent = label;
    }
    async function copy(button, text, successLabel, failureLabel, onFailure) {
      const attempt = {};
      attempts.set(button, attempt);
      button.textContent = "Copying…";
      let copied = false;
      try {
        // Capture the requested text before any asynchronous selection change.
        await writeText(text);
        copied = true;
      } catch {
        // Missing clipboard APIs and permission denial use the same fallback.
      }
      if (!button.isConnected || attempts.get(button) !== attempt) return;
      button.textContent = copied ? successLabel : failureLabel;
      if (!copied && onFailure) onFailure();
    }
    return { reset, copy };
  }
  const api = { create };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.CSM_COPY_FEEDBACK = api;
})(typeof window !== "undefined" ? window : this);
