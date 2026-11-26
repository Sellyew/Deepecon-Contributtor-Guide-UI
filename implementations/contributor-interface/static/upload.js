// Submit (M3): sends the chosen ZIP file in chunks, so an interrupted upload continues where it
// stopped (plan §2.5). Without this script the same form posts the whole file at once.
// Resuming: choose the same file again; the server finds the unfinished upload by name and size
// and answers with the number of bytes it already has.
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

  function show(text, problem) {
    status.textContent = text;
    status.classList.toggle("problem", !!problem);
  }
  function json(r) {
    var type = r.headers.get("Content-Type") || "";
    if (type.indexOf("application/json") !== 0) return Promise.reject(new Error("not json"));
    return r.json().then(function (body) { return { status: r.status, body: body }; });
  }
  function megabytes(n) { return (n / 1048576).toFixed(1) + " MB"; }

  function sendFrom(file, upload, offset, retries) {
    if (offset >= file.size) return Promise.resolve(upload);
    var end = Math.min(offset + upload.chunk_bytes, file.size);
    bar.hidden = false;
    bar.value = Math.floor(100 * offset / file.size);
    show(d.sending + " " + megabytes(offset) + " / " + megabytes(file.size), false);
    return fetch(d.base + encodeURIComponent(upload.id) + "/chunk/?offset=" + offset, {
      method: "POST", body: file.slice(offset, end), credentials: "same-origin",
      headers: { "X-CSRFToken": token, "Content-Type": "application/octet-stream", "X-Requested-With": "fetch" }
    }).then(json).then(function (res) {
      if (res.status === 200) {
        if (res.body.status === "received" || res.body.status === "refused") return res.body;
        return sendFrom(file, res.body, res.body.offset, 0);
      }
      if (res.status === 409 && typeof res.body.offset === "number") {     // the server has a different offset
        return sendFrom(file, upload, res.body.offset, retries);
      }
      throw { message: res.body.message };
    }, function () {
      if (retries < 5) {                                                   // a broken connection: wait and retry
        return new Promise(function (resolve) { setTimeout(resolve, 1000 * Math.pow(2, retries)); })
          .then(function () { return sendFrom(file, upload, offset, retries + 1); });
      }
      throw { paused: true };
    });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (busy) return;
    var file = input.files && input.files[0];
    if (!file) { input.focus(); return; }
    busy = true;
    var data = new FormData();
    data.append("name", file.name);
    data.append("size", String(file.size));
    fetch(d.start, { method: "POST", body: data, credentials: "same-origin",
                     headers: { "X-CSRFToken": token, "X-Requested-With": "fetch" } })
      .then(json)
      .then(function (res) {
        if (res.status !== 201) throw { message: res.body.message };
        if (res.body.offset > 0 && res.body.offset < file.size) bar.value = Math.floor(100 * res.body.offset / file.size);
        return sendFrom(file, res.body, res.body.offset, 0);
      })
      .then(function (done) {
        bar.value = 100;
        if (done.status === "refused") {
          show(d.failed + " " + (done.message || ""), true);
          busy = false;
          return;
        }
        show(d.done + " " + done.sha256, false);
        window.setTimeout(function () { window.location.reload(); }, 1500);   // list it with the other uploads
      })
      .catch(function (err) {
        busy = false;
        if (err && err.paused) show(d.paused, true);
        else show(d.failed + " " + ((err && err.message) || d.paused), true);
      });
  });
})();
