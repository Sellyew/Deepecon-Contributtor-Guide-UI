// Keeps the danger-zone button disabled until the contributor's ID is typed exactly (GitHub's
// convention). The server checks the typed ID again; this only helps the team.
document.addEventListener("DOMContentLoaded", function () {
  var form = document.querySelector("form.danger-form");
  if (!form) return;
  var expected = form.getAttribute("data-confirm");
  var input = form.querySelector("input[name=confirmation]");
  var button = document.getElementById("danger-submit");
  if (!input || !button) return;
  var update = function () { button.disabled = input.value !== expected; };
  input.addEventListener("input", update);
  update();
});
