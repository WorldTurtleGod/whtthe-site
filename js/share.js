/* Share bar: copy link, native share on phones. Links for X, Facebook, Reddit, and email are plain hrefs. */
(function () {
  "use strict";

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var input = document.createElement("textarea");
      input.value = text;
      input.setAttribute("readonly", "");
      input.style.position = "fixed";
      input.style.left = "-9999px";
      document.body.appendChild(input);
      input.select();
      try {
        document.execCommand("copy");
        resolve();
      } catch (err) {
        reject(err);
      } finally {
        document.body.removeChild(input);
      }
    });
  }

  document.querySelectorAll(".share-bar").forEach(function (bar) {
    var url = bar.getAttribute("data-share-url") || "";
    var title = bar.getAttribute("data-share-title") || "";
    var copyBtn = bar.querySelector("[data-copy-link]");
    var copied = bar.querySelector(".share-copied");
    var nativeBtn = bar.querySelector(".share-native");

    if (copyBtn) {
      copyBtn.addEventListener("click", function () {
        copyText(url).then(function () {
          if (!copied) return;
          copied.hidden = false;
          copied.textContent = "Copied";
          window.setTimeout(function () {
            copied.hidden = true;
          }, 2000);
        }).catch(function () {
          if (!copied) return;
          copied.hidden = false;
          copied.textContent = "Could not copy. Select the address bar instead.";
        });
      });
    }

    if (nativeBtn && typeof navigator.share === "function") {
      nativeBtn.hidden = false;
      nativeBtn.addEventListener("click", function () {
        navigator.share({ title: title, text: title, url: url }).catch(function () {
          /* User cancelled, or the browser refused. No error needed. */
        });
      });
    }
  });
})();
