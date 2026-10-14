(function () {
  "use strict";
  const api = window.CSM_PRACTICE;
  const cases = api.buildCases(window.CSM_DATA, window.CSM_MODEL_RUNS);
  let session = api.createSession(cases),
    current = 0;
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
  function render() {
    const c = cases[current],
      item = session[current];
    get("practice-progress").textContent =
      `${session.filter((s) => s.reviewed).length} / ${cases.length} decisions reviewed · written reasoning is not graded`;
    get("practice-export").disabled = !session.some((s) => s.reviewed);
    get("practice-case").innerHTML =
      `<h3>${escape(c.title)}</h3><p>${escape(c.situation)}</p><div class="practice-evidence"><h4>Evidence available to you</h4><ul>${c.evidence.map((e) => `<li><b>${escape(e.label)}</b>: ${escape(e.value)}<small>${escape(e.sources.join(", ") || "No applicable record")}</small></li>`).join("")}</ul></div><fieldset ${item.reviewed ? "disabled" : ""}><legend>Choose the next action</legend>${c.options.map((o) => `<label class="practice-option"><input type="radio" name="practice-choice" value="${escape(o.id)}" ${item.choice === o.id ? "checked" : ""}><span>${escape(o.text)}</span></label>`).join("")}</fieldset><label class="practice-note" for="practice-reasoning">Your reasoning before guidance <span>(optional)</span></label><textarea id="practice-reasoning" maxlength="4000" rows="3" ${item.reviewed ? "readonly" : ""} placeholder="Which evidence supports your choice? What remains uncertain?">${escape(item.reasoning)}</textarea>${item.reviewed ? "" : `<button class="button primary" id="practice-reveal" ${item.choice ? "" : "disabled"}>Compare with the evidence</button>`}<div id="practice-feedback" ${item.reviewed ? 'tabindex="-1"' : ""}></div>`;
    get("practice-case")
      .querySelectorAll('input[name="practice-choice"]')
      .forEach((input) =>
        input.addEventListener("change", () => {
          item.choice = input.value;
          get("practice-reveal").disabled = false;
        }),
      );
    get("practice-reasoning").addEventListener("input", (e) => {
      if (!item.reviewed) item.reasoning = e.target.value;
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
    render();
  });
  get("practice-reset").addEventListener("click", () => {
    session = api.createSession(cases);
    current = 0;
    get("practice-select").value = "0";
    render();
    get("practice-progress").textContent =
      "Practice reset. 0 / 3 decisions reviewed; all session notes cleared.";
  });
  get("practice-export").addEventListener("click", () => {
    const content = api.exportReflection(
      cases,
      session,
      window.CSM_DATA.workflow.as_of,
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
      "Reflection download requested. Original choices and post-guidance notes are labeled separately.";
  });
  render();
})();
