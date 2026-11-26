// Submit (M3): sends the chosen ZIP file in chunks, so an interrupted upload continues where it
// stopped (plan §2.5). Without this script the same form posts the whole file at once.
// Resuming: choose the same file again. The server resumes only the same file: same name, size,
// last-modified time, and SHA-256 of its first MiB; anything else starts a new upload.
// A finished upload is added to the table without reloading, so unsaved answers below are kept.
(function () {
  "use strict";
  var form = document.getElementById("upload-form");
  if (!form || !window.fetch || !window.Blob || !Blob.prototype.slice) return;
  var input = document.getElementById("id_package");
  var bar = document.getElementById("upload-progress");
  var status = document.getElementById("upload-status");
  var token = form.querySelector("input[name=csrfmiddlewaretoken]").value;
  var d = form.dataset;
  var busy = false;
  var HEAD = 1024 * 1024;
  var lastShown = 0;

  function show(text, problem) {
    status.textContent = text;
    status.classList.toggle("problem", !!problem);
  }
  // Progress is announced at most every 10 % (aria-live), the bar moves on every chunk.
  function progress(offset, size) {
    var percent = Math.floor(100 * offset / size);
    bar.hidden = false;
    bar.value = percent;
    if (percent - lastShown >= 10 || percent === 0) {
      lastShown = percent;
      show(d.sending + " " + percent + " %", false);
    }
  }
  function answer(r) {
    // An answer from the server: JSON from the upload views, or an HTML page (session ended, error).
    var type = r.headers.get("Content-Type") || "";
    if (type.indexOf("application/json") !== 0) return Promise.reject({ http: r.status });
    return r.json().then(function (body) { return { status: r.status, body: body }; });
  }
  function serverProblem(err) {
    if (err && err.http === 403) return d.session;
    if (err && err.http) return d.server;
    if (err && err.message) return d.failed + " " + err.message;
    return d.paused;
  }
  function headHash(file) {
    if (!window.crypto || !window.crypto.subtle) return Promise.resolve("");    // resume is then not offered
    return file.slice(0, Math.min(HEAD, file.size)).arrayBuffer()
      .then(function (buf) { return window.crypto.subtle.digest("SHA-256", buf); })
      .then(function (digest) {
        return Array.prototype.map.call(new Uint8Array(digest), function (b) { return ("0" + b.toString(16)).slice(-2); }).join("");
      }, function () { return ""; });
  }
  function statusOf(upload) {
    return fetch(d.base + encodeURIComponent(upload.id) + "/", { credentials: "same-origin", headers: { "X-Requested-With": "fetch" } })
      .then(answer);
  }

  function sendFrom(file, upload, offset, retries) {
    if (offset >= file.size) return statusOf(upload).then(function (res) { return res.body; });
    var end = Math.min(offset + upload.chunk_bytes, file.size);
    progress(offset, file.size);
    if (end === file.size) show(d.checking, false);
    return fetch(d.base + encodeURIComponent(upload.id) + "/chunk/?offset=" + offset, {
      method: "POST", body: file.slice(offset, end), credentials: "same-origin",
      headers: { "X-CSRFToken": token, "Content-Type": "application/octet-stream", "X-Requested-With": "fetch" }
    }).then(answer, function () { return { lost: true }; }).then(function (res) {
      if (res.lost) {
        // No answer arrived: the chunk may or may not have been stored. Ask before sending again.
        if (retries >= 5) throw { paused: true };
        return new Promise(function (resolve) { setTimeout(resolve, 1000 * Math.pow(2, retries)); })
          .then(function () { return statusOf(upload); })
          .then(function (state) {
            if (state.body.status === "received" || state.body.status === "refused") return state.body;
            if (state.body.status === "checking") return waitWhileChecking(upload, 0);
            return sendFrom(file, upload, state.body.offset, retries + 1);
          }, function (err) {
            if (err && err.http) throw err;
            return sendFrom(file, upload, offset, retries + 1);
          });
      }
      if (res.status === 200) {
        if (res.body.status === "received" || res.body.status === "refused") return res.body;
        return sendFrom(file, res.body, res.body.offset, 0);
      }
      if (res.status === 409 && typeof res.body.offset === "number") {     // the server has a different offset
        return sendFrom(file, upload, res.body.offset, retries);
      }
      throw { message: res.body.message };
    });
  }
  function waitWhileChecking(upload, n) {
    if (n > 120) throw { paused: true };
    return new Promise(function (resolve) { setTimeout(resolve, 2000); })
      .then(function () { return statusOf(upload); })
      .then(function (state) {
        if (state.body.status === "checking") return waitWhileChecking(upload, n + 1);
        return state.body;
      });
  }
  function addRow(done) {
    var table = document.querySelector(".uploads table tbody");
    if (!table) return;
    var empty = document.getElementById("no-upload-row");
    if (empty) empty.remove();
    var row = document.createElement("tr");
    [done.name, (done.size / 1048576).toFixed(1) + " MB", d.newRow, done.sha256, ""].forEach(function (text, i) {
      var cell = document.createElement("td");
      if (i === 3) { var span = document.createElement("span"); span.className = "hash"; span.textContent = text; cell.appendChild(span); }
      else cell.textContent = text;
      row.appendChild(cell);
    });
    table.appendChild(row);
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (busy) return;
    var file = input.files && input.files[0];
    if (!file) { input.focus(); return; }
    busy = true;
    lastShown = -10;
    headHash(file).then(function (head) {
      var data = new FormData();
      data.append("name", file.name);
      data.append("size", String(file.size));
      data.append("modified", String(file.lastModified || 0));
      data.append("head", head);
      return fetch(d.start, { method: "POST", body: data, credentials: "same-origin",
                              headers: { "X-CSRFToken": token, "X-Requested-With": "fetch" } })
        .then(answer, function () { throw { paused: true }; });
    }).then(function (res) {
      if (res.status !== 201) throw { message: res.body.message };
      if (res.body.status === "received" || res.body.status === "refused") return res.body;
      return sendFrom(file, res.body, res.body.offset, 0);
    }).then(function (done) {
      busy = false;
      bar.value = 100;
      if (done.status === "refused") { show(d.failed + " " + (done.message || ""), true); return; }
      show(d.done + " " + done.sha256, false);
      addRow(done);
      input.value = "";
    }).catch(function (err) {
      busy = false;
      show(err && err.paused ? d.paused : serverProblem(err), true);
    });
  });
})();
