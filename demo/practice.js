(function () {
  "use strict";
  const api = window.CSM_PRACTICE;
  const cases = api.buildCases(window.CSM_DATA, window.CSM_MODEL_RUNS);
  const links = window.CSM_REVIEW_LINKS;
  const checkpoints = window.CSM_PRACTICE_SESSION;
  const copyFeedback = window.CSM_COPY_FEEDBACK.create();
  let pending = null, fileAttempt = 0, restored = false;
  let route = links.readPractice(location.search, cases);
  let session = api.createSession(cases),
    current = cases.findIndex((c) => c.id === route.practiceId);
  const get = (id) => document.getElementById(id);
  const escape = (value) =>
    String(value).replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[c],
    );
  get("practice-select").innerHTML = cases
    .map((c, i) => `<option value="${i}">${i + 1}. ${escape(c.title)}</option>`)
    .join("");
  function warnBeforeLeaving(event) {
    if (!api.hasWork(session)) return;
    event.preventDefault();
    event.returnValue = "";
  }
  function updateExportAvailability() {
    const hasWork = api.hasWork(session);
    get("practice-export").disabled = !hasWork;
    get("practice-save").disabled = !hasWork;
    if (hasWork) window.addEventListener("beforeunload", warnBeforeLeaving);
    else window.removeEventListener("beforeunload", warnBeforeLeaving);
  }
  function render() {
    hideResetConfirmation();
    const c = cases[current],
      item = session[current];
    get("practice-select").value = String(current);
    get("share-practice-url").value = links.sharePractice(c.id, cases);
    copyFeedback.reset(get("copy-practice-link"), "Copy this practice link");
    get("practice-route-notice").textContent = route.invalid
      ? "This practice link is invalid or ambiguous. The first decision is shown; no answer or notes were loaded."
      : "";
    get("practice-progress").textContent =
      `${session.filter((s) => s.reviewed).length} / ${cases.length} decisions reviewed · written reasoning is not graded`;
    get("practice-restored").textContent = restored
      ? "Resumed from a user-editable local file. Saved response and guidance states are not verified history."
      : "";
    updateExportAvailability();
    get("practice-case").innerHTML =
      `<h3>${escape(c.title)}</h3><p>${escape(c.situation)}</p><div class="practice-evidence"><h4>Evidence available to you</h4><ul>${c.evidence.map((e) => `<li><b>${escape(e.label)}</b>: ${escape(e.value)}<small>${escape(e.sources.join(", ") || "No applicable record")}</small></li>`).join("")}</ul></div><fieldset ${item.reviewed ? "disabled" : ""}><legend>Choose the next action</legend>${c.options.map((o) => `<label class="practice-option"><input type="radio" name="practice-choice" value="${escape(o.id)}" ${item.choice === o.id ? "checked" : ""}><span>${escape(o.text)}</span></label>`).join("")}</fieldset><label class="practice-note" for="practice-reasoning">Your reasoning before guidance <span>(optional)</span></label><textarea id="practice-reasoning" maxlength="4000" rows="3" ${item.reviewed ? "readonly" : ""} placeholder="Which evidence supports your choice? What remains uncertain?">${escape(item.reasoning)}</textarea>${item.reviewed ? "" : `<button class="button primary" id="practice-reveal" ${item.choice ? "" : "disabled"}>Compare with the evidence</button>`}<div id="practice-feedback" ${item.reviewed ? 'tabindex="-1"' : ""}></div>`;
    get("practice-case")
      .querySelectorAll('input[name="practice-choice"]')
      .forEach((input) =>
        input.addEventListener("change", () => {
          item.choice = input.value;
          get("practice-reveal").disabled = false;
          updateExportAvailability();
        }),
      );
    get("practice-reasoning").addEventListener("input", (e) => {
      if (!item.reviewed) item.reasoning = e.target.value;
      updateExportAvailability();
    });
    if (!item.reviewed) {
      get("practice-reveal").addEventListener("click", () => {
        session[current] = api.reveal(item, c);
        render();
        get("practice-feedback").focus();
      });
      return;
    }
    const option = c.options.find((o) => o.id === item.initial.choice);
    get("practice-feedback").innerHTML =
      `<div class="practice-feedback"><h4>${item.initial.choice === c.expected ? "Your option matches the project policy" : "This option needs a different next step"}</h4><p>${escape(option.feedback)}</p><p>${escape(c.explanation)}</p><p class="boundary">This compares the selected option only. Your written reasoning has not been evaluated. The original choice and note are retained for reflection.</p><a class="text-link" data-review-link href="${escape(c.source)}">${escape(c.sourceLabel)} ↓</a><label class="practice-note" for="practice-reflection">Reflect after reading the guidance</label><p>${escape(c.prompt)}</p><textarea id="practice-reflection" maxlength="4000" rows="4" placeholder="What would you change or investigate next?">${escape(item.reflection)}</textarea></div>`;
    get("practice-reflection").addEventListener("input", (e) => {
      item.reflection = e.target.value;
    });
  }
  get("practice-select").addEventListener("change", (e) => {
    current = Number(e.target.value);
    window.dispatchEvent(new CustomEvent("csm-practice-selection", { detail: cases[current].id }));
  });
  window.addEventListener("csm-practice-route", (event) => {
    route = event.detail;
    current = cases.findIndex((c) => c.id === route.practiceId);
    render();
  });
  get("copy-practice-link").addEventListener("click", (event) => {
    const url = links.sharePractice(cases[current].id, cases);
    return copyFeedback.copy(event.currentTarget, url, "Practice link copied", "Select the link to copy", () => {
      get("practice-link-details").open = true;
      get("share-practice-url").focus();
      get("share-practice-url").select();
    });
  });
  function hideResetConfirmation() {
    get("practice-reset-confirm").hidden = true;
    get("practice-reset").setAttribute("aria-expanded", "false");
  }
  function cancelReset() {
    hideResetConfirmation();
    get("practice-progress").textContent = "Reset cancelled. Your practice work is unchanged.";
    get("practice-reset").focus();
  }
  function resetPractice() {
    hideResetConfirmation();
    clearPending();
    restored = false;
    get("practice-file-status").textContent = "";
    session = api.createSession(cases);
    current = 0;
    window.dispatchEvent(new CustomEvent("csm-practice-selection", { detail: cases[current].id }));
    get("practice-progress").textContent =
      `Practice reset. 0 / ${cases.length} decisions reviewed; all session notes cleared.`;
    get("practice-select").focus();
  }
  get("practice-reset").addEventListener("click", () => {
    if (!api.hasWork(session)) {
      resetPractice();
      return;
    }
    get("practice-reset-confirm").hidden = false;
    get("practice-reset").setAttribute("aria-expanded", "true");
    get("practice-reset-cancel").focus();
  });
  get("practice-reset-cancel").addEventListener("click", cancelReset);
  get("practice-reset-confirm").addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      event.preventDefault();
      cancelReset();
    }
  });
  get("practice-reset-apply").addEventListener("click", () => {
    if (!get("practice-reset-confirm").hidden) resetPractice();
  });
  get("practice-export").addEventListener("click", () => {
    const content = api.exportReflection(
      cases,
      session,
      window.CSM_DATA.workflow.as_of,
      restored,
    );
    const url = URL.createObjectURL(
      new Blob([content], { type: "text/markdown;charset=utf-8" }),
    );
    const link = document.createElement("a");
    link.href = url;
    link.download = "csm-practice-reflection.md";
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    get("practice-progress").textContent =
      "Notes download requested. Unreviewed drafts, original responses and later reflections are labeled separately. Reloading still clears this page's notes.";
  });
  function download(content, name, type) {
    const url = URL.createObjectURL(new Blob([content], { type }));
    const link = document.createElement("a");
    link.href = url;
    link.download = name;
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  function clearPending() {
    fileAttempt += 1;
    pending = null;
    get("practice-load-preview").hidden = true;
    get("practice-load").value = "";
  }
  get("practice-save").addEventListener("click", async () => {
    get("practice-save").disabled = true;
    try {
      const content = await checkpoints.save(cases, session, cases[current].id, window.CSM_DATA.workflow.as_of);
      download(content, "csm-practice-progress.json", "application/json;charset=utf-8");
      get("practice-file-status").textContent = "Progress download requested. Keep this JSON file to resume; it contains your notes and is not uploaded.";
    } catch {
      get("practice-file-status").textContent = "Progress could not be saved in this browser. Your current work remains here; download the readable notes before leaving.";
    } finally {
      updateExportAvailability();
    }
  });
  get("practice-load").addEventListener("change", async (event) => {
    const attempt = ++fileAttempt, file = event.target.files[0];
    pending = null;
    get("practice-load-preview").hidden = true;
    if (!file) {
      get("practice-file-status").textContent = "No file selected. Your current work is unchanged.";
      return;
    }
    get("practice-file-status").textContent = "Checking the selected progress file locally…";
    try {
      if (file.size > checkpoints.MAX_BYTES) throw new Error("Choose a progress JSON file no larger than 512 KiB.");
      const loaded = await checkpoints.load(await file.text(), cases, window.CSM_DATA.workflow.as_of);
      if (attempt !== fileAttempt) return;
      pending = loaded;
      const reviewed = loaded.session.filter((s) => s.reviewed).length;
      get("practice-load-summary").textContent = `${loaded.session.length} decisions · ${reviewed} with guidance revealed. Opens: ${cases.find((c) => c.id === loaded.selectedId).title}`;
      get("practice-load-preview").hidden = false;
      get("practice-file-status").textContent = "File is compatible. Review the replacement notice before resuming; your current work has not changed.";
    } catch (error) {
      if (attempt !== fileAttempt) return;
      get("practice-file-status").textContent = `${error.message || "The progress file could not be read."} Your current work has not changed.`;
    }
  });
  get("practice-cancel").addEventListener("click", () => {
    clearPending();
    get("practice-file-status").textContent = "Resume cancelled. Your current work is unchanged.";
  });
  get("practice-apply").addEventListener("click", () => {
    if (!pending) return;
    const loaded = pending;
    clearPending();
    session = loaded.session;
    restored = true;
    window.dispatchEvent(new CustomEvent("csm-practice-selection", { detail: loaded.selectedId }));
    get("practice-file-status").textContent = "Progress resumed locally. No notes were uploaded.";
    get("practice-select").focus();
  });
  render();
})();
