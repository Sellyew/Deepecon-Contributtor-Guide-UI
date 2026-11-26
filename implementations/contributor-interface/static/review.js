// Selection (M2): autosave with visible conflicts, and keyboard shortcuts (MVP §4.2, plan §2.4).
// The page works without this script: every control is an ordinary form post.
(function () {
  "use strict";
  var form = document.getElementById("review-form");
  if (!form) return;
  var status = document.getElementById("save-status");
  var version = form.querySelector("input[name=version]");
  var verdict = form.querySelector("input[name=verdict]");
  var timer = null;
  var labels = {
    saving: form.dataset.saving || "Saving…",
    saved: form.dataset.saved || "Saved",
    conflict: form.dataset.conflict || "Not saved: this item was changed in another tab. Reload the page.",
    offline: form.dataset.offline || "Not saved: no connection. Your text is still here; try again.",
    invalid: form.dataset.invalid || "Not saved: please check the highlighted fields.",
    frozen: form.dataset.frozen || "Not saved: the review is frozen."
  };

  function show(text, problem) {
    if (!status) return;
    status.textContent = text;
    status.classList.toggle("problem", !!problem);
  }

  function autosave() {
    if (!verdict || !verdict.value) return;   // nothing to save until an answer is chosen
    var data = new FormData(form);
    data.set("save", "1");
    show(labels.saving, false);
    fetch(window.location.href, { method: "POST", body: data, credentials: "same-origin",
                                  headers: { "X-Requested-With": "fetch" } })
      .then(function (r) { return r.json().then(function (body) { return { status: r.status, body: body }; }); })
      .then(function (res) {
        if (res.status === 200 && res.body.ok) {
          version.value = res.body.version;
          show(labels.saved + " " + res.body.saved_at, false);
        } else if (res.status === 409) {
          show(labels.conflict, true);
        } else if (res.status === 423) {
          show(labels.frozen, true);
        } else {
          show(labels.invalid, true);
        }
      })
      .catch(function () { show(labels.offline, true); });
  }

  form.addEventListener("input", function (e) {
    if (e.target.name === "set_verdict") return;
    clearTimeout(timer);
    timer = setTimeout(autosave, 1500);
  });
  form.addEventListener("change", function (e) {
    if (e.target.type === "checkbox" || e.target.tagName === "SELECT") {
      clearTimeout(timer);
      timer = setTimeout(autosave, 300);
    }
  });

  var keys = { k: "keep", c: "keep_with_changes", r: "reject", u: "unsure" };
  document.addEventListener("keydown", function (e) {
    var tag = (e.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea" || tag === "select" || e.altKey || e.ctrlKey || e.metaKey) return;
    if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
      var link = document.getElementById(e.key === "ArrowLeft" ? "prev-link" : "next-link");
      if (link) { window.location.href = link.href; }
      return;
    }
    var value = keys[(e.key || "").toLowerCase()];
    if (!value) return;
    var button = form.querySelector('button[name=set_verdict][value="' + value + '"]');
    if (button && !button.disabled) { e.preventDefault(); button.click(); }
  });
})();
