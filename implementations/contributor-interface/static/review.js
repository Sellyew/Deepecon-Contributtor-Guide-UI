// Selection (M2): autosave with visible conflicts, and keyboard shortcuts (MVP §4.2, plan §2.4).
// The page works without this script: every control is an ordinary form post.
//
// Saves are sent one at a time (a change made while a save is under way is sent after it, with
// the new version), so the page never reports a conflict with itself. Before the page is left
// by a link, a shortcut, or another form on the page (language, "Ask the team"), pending changes
// are saved first. On reload or closing, the save starts at once and the browser asks before
// leaving while anything is unsaved. The question does not hold the next page's request until
// the save has arrived, so a short-lived note in sessionStorage says a save was under way. A page
// that finds the note and may be out of date asks the server for the item's version for about
// two seconds, locked, and loads itself again (a plain GET) only if a newer version appears.
(function () {
  "use strict";
  var form = document.getElementById("review-form");
  if (!form) return;
  var status = document.getElementById("save-status");
  var version = form.querySelector("input[name=version]");
  var verdict = form.querySelector("input[name=verdict]");
  var d = form.dataset;
  var labels = {
    saving: d.saving || "Saving…",
    saved: d.saved || "Saved",
    conflict: d.conflict || "Not saved: this item was changed in another tab. Reload the page.",
    offline: d.offline || "Not saved: no connection. Your text is still here; try again.",
    invalid: d.invalid || "Not saved: please check the highlighted fields.",
    frozen: d.frozen || "Not saved: the review is frozen.",
    session: d.session || "Not saved: your session has ended. Copy your text, then open your personal link again.",
    server: d.server || "Not saved: the site could not save this answer. Copy your text, then reload the page.",
    needsAnswer: d.needsAnswer || "Not saved yet: choose an answer, and your notes are saved with it.",
    refreshing: d.refreshing || "Loading your latest saved answer…"
  };
  var timer = null;       // a scheduled autosave
  var inflight = null;    // the promise of the save under way
  var pending = false;    // a change arrived while a save was under way
  var dirty = false;      // the form has changes the server has not stored
  var failed = false;     // the last save did not succeed
  var leaving = false;    // the page is being left on purpose (a form post or a saved navigation)
  var unloading = false;  // the page is going away (pagehide)
  var partnerVersion = form.querySelector("input[name=partner_version]");
  var noteKey = "review-saving:" + window.location.pathname;
  var asked = false;      // the browser has asked whether to leave (beforeunload)

  function readNote() {
    try { return JSON.parse(window.sessionStorage.getItem(noteKey) || "null"); } catch (err) { return null; }
  }
  function writeNote(note) {
    try {
      if (note) window.sessionStorage.setItem(noteKey, JSON.stringify(note));
      else window.sessionStorage.removeItem(noteKey);
    } catch (err) { /* storage unavailable: the page still works, without this check */ }
  }

  function show(text, problem) {
    if (!status) return;
    status.textContent = text;
    status.classList.toggle("problem", !!problem);
  }

  function clearFieldErrors() {
    Array.prototype.forEach.call(form.querySelectorAll(".js-error"), function (el) { el.remove(); });
    Array.prototype.forEach.call(form.querySelectorAll("[aria-invalid]"), function (el) { el.removeAttribute("aria-invalid"); });
  }

  function showFieldErrors(errors) {
    Object.keys(errors || {}).forEach(function (name) {
      var field = form.elements[name];
      if (!field || !field.parentNode || !field.tagName) return;
      var list = document.createElement("ul");
      list.className = "errorlist js-error";
      (errors[name] || []).forEach(function (e) {
        var li = document.createElement("li");
        li.textContent = e.message;
        list.appendChild(li);
      });
      field.parentNode.insertBefore(list, field);
      field.setAttribute("aria-invalid", "true");
      var details = field.closest("details");
      if (details) details.open = true;
    });
  }

  function send(keepalive) {
    var data = new FormData(form);
    data.set("save", "1");
    // A save that starts after the browser asked to leave may land after the next page is built.
    if (asked) writeNote({ version: version.value, pending: false, at: Date.now() });
    return fetch(window.location.pathname, { method: "POST", body: data, credentials: "same-origin",
                                             headers: { "X-Requested-With": "fetch" }, keepalive: !!(keepalive || asked) });
  }

  function handle(r) {
    var type = r.headers.get("Content-Type") || "";
    if (type.indexOf("application/json") !== 0) {
      // Not an answer from the save itself: the session ended (403), or the site failed.
      writeNote(null);                      // nothing was stored, so no page needs to wait for it
      failed = true; dirty = true;
      show(r.status === 403 ? labels.session : labels.server, true);
      return;
    }
    return r.json().then(function (body) {
      clearFieldErrors();
      if (r.status === 200 && body.ok) {
        version.value = body.version;
        if (partnerVersion && body.partner_version !== undefined) partnerVersion.value = body.partner_version;
        show(labels.saved + " " + body.saved_at, false);
        return;
      }
      writeNote(null);                      // refused: nothing was stored, so no page needs to wait for it
      if (r.status === 423) {             // frozen: nothing more can be saved, so do not hold the page
        dirty = false; pending = false;
        show(labels.frozen, true);
        return;
      }
      failed = true; dirty = true;
      if (r.status === 409) {
        show(labels.conflict, true);
      } else {
        showFieldErrors(body.errors);
        show(labels.invalid, true);
      }
    });
  }

  function autosave(keepalive) {
    clearTimeout(timer); timer = null;
    if (inflight) { if (dirty) pending = true; return inflight; }
    if (!dirty) return Promise.resolve();
    if (!verdict || !verdict.value) { show(labels.needsAnswer, false); return Promise.resolve(); }
    dirty = false; failed = false;
    show(labels.saving, false);
    // No writeNote(null) here: a page that is going away sees its keepalive save "fail" although
    // the browser still delivers it, so only an answer from the server may remove the note.
    var request = send(keepalive).then(handle).catch(function () { failed = true; dirty = true; show(labels.offline, true); });
    inflight = request.then(function () {
      inflight = null;
      if (pending) { pending = false; return autosave(); }
    });
    return inflight;
  }

  function schedule(ms) {
    dirty = true;
    clearTimeout(timer);
    if (!verdict || !verdict.value) { show(labels.needsAnswer, false); return; }
    timer = setTimeout(autosave, ms);
  }

  form.addEventListener("input", function () { schedule(1500); });
  form.addEventListener("change", function () { schedule(300); });   // includes leaving a text field

  // A form post (an answer button, Save, or Enter) carries the whole form. If a save is under way,
  // wait for it, so the post carries the version that save produced.
  form.addEventListener("submit", function (e) {
    clearTimeout(timer); timer = null;
    if (inflight) {
      e.preventDefault();
      pending = false;
      var button = e.submitter || null;
      inflight.then(function () { form.requestSubmit(button); });
      return;
    }
    leaving = true;
  });

  // Links that leave the page (previous, next, map markers, header links): save first.
  document.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("a[href]") : null;
    if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || a.target) return;
    // After a failed save, let the contributor leave: the browser asks first (beforeunload).
    if (!verdict || !verdict.value || failed || !(timer || dirty || inflight)) return;
    e.preventDefault();
    autosave().then(function () {
      if (!failed) { leaving = true; window.location.href = a.href; }
    });
  });

  // The page's other forms (the language switch, "Ask the team"): save first, then send them.
  document.addEventListener("submit", function (e) {
    var other = e.target;
    if (other === form || e.defaultPrevented) return;
    if (!verdict || !verdict.value || failed || !(timer || dirty || inflight)) return;
    e.preventDefault();
    autosave().then(function () { if (!failed) { leaving = true; other.submit(); } });
  });

  // Reloading, closing, or the address bar: start the save now and ask before leaving while
  // anything is unsaved. The question does not hold the next page's request until the save has
  // arrived; the note checked at the end of this script covers a page built too early.
  window.addEventListener("beforeunload", function (e) {
    if (leaving) return;
    asked = true;
    var queued = !!(inflight && (timer || dirty || pending));     // more to send after the save under way
    if ((timer || dirty) && verdict && verdict.value && !inflight && !failed) autosave(true);
    if (inflight) writeNote({ version: version.value, pending: queued, at: Date.now() });
    if (inflight || dirty) { e.preventDefault(); e.returnValue = ""; }
  });
  // Switching tabs: save, since the page may not come back (phones discard background tabs).
  window.addEventListener("pagehide", function () { unloading = true; });
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden" && !leaving && !unloading) autosave(true);
  });

  var keys = { k: "keep", c: "keep_with_changes", r: "reject", u: "unsure" };
  document.addEventListener("keydown", function (e) {
    var tag = (e.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea" || tag === "select" || e.target.isContentEditable ||
        e.altKey || e.ctrlKey || e.metaKey || e.repeat) return;
    if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
      var link = document.getElementById(e.key === "ArrowLeft" ? "prev-link" : "next-link");
      if (link) { e.preventDefault(); link.click(); }    // the click handler saves first
      return;
    }
    var value = keys[(e.key || "").toLowerCase()];
    if (!value) return;
    var button = form.querySelector('button[name=set_verdict][value="' + value + '"]');
    if (button && !button.disabled) { e.preventDefault(); button.click(); }
  });

  // Was this page built before a save from the previous page had arrived? If a note says a save
  // was under way (within the last 30 s) and this page may be older than it, lock the form, ask
  // the server for the item's version for about two seconds, and load the page again (a GET,
  // never a resubmitted form) only if a newer version appears; otherwise unlock.
  var note = readNote();
  if (note && (Date.now() - (note.at || 0) > 30000 || (Number(version.value) > Number(note.version) && !note.pending))) {
    writeNote(null);
    note = null;
  }
  if (note) {
    var mine = Number(version.value);
    var before = Array.prototype.map.call(form.elements, function (el) { return el.disabled; });
    leaving = true;                         // no saves from this page while it may be out of date
    Array.prototype.forEach.call(form.elements, function (el) { el.disabled = true; });
    show(labels.refreshing, false);
    var polls = 0;
    var poll = function () {
      fetch(window.location.pathname, { credentials: "same-origin", headers: { "X-Requested-With": "fetch" } })
        .then(function (r) { return r.ok && (r.headers.get("Content-Type") || "").indexOf("application/json") === 0 ? r.json() : null; })
        .catch(function () { return null; })
        .then(function (body) {
          if (body && Number(body.version) > mine) {
            writeNote(null);
            window.location.replace(window.location.pathname + window.location.search);
            return;
          }
          if (++polls < 8) { window.setTimeout(poll, 300); return; }
          writeNote(null);                  // nothing newer arrived: this page is current
          Array.prototype.forEach.call(form.elements, function (el, i) { el.disabled = before[i]; });
          leaving = false;
          show("", false);
        });
    };
    poll();
  }
})();
