document.addEventListener("DOMContentLoaded", function () {
  // Mobile nav toggle
  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      links.classList.toggle("open");
      toggle.innerHTML = links.classList.contains("open") ? "&times;" : "&#9776;";
    });
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        links.classList.remove("open");
        toggle.innerHTML = "&#9776;";
      });
    });
  }

  // Back to top
  var topBtn = document.querySelector(".float-btn.top");
  if (topBtn) {
    window.addEventListener("scroll", function () {
      if (window.scrollY > 500) topBtn.classList.add("show");
      else topBtn.classList.remove("show");
    });
    topBtn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // Gallery lightbox
  var lightbox = document.querySelector(".lightbox");
  if (lightbox) {
    var lbImg = lightbox.querySelector("img");
    document.querySelectorAll(".gallery-item[data-full]").forEach(function (item) {
      item.addEventListener("click", function () {
        lbImg.src = item.getAttribute("data-full");
        lightbox.classList.add("open");
      });
    });
    lightbox.addEventListener("click", function () {
      lightbox.classList.remove("open");
    });
  }

  // Simple counter animation for stats
  var counters = document.querySelectorAll("[data-count]");
  if (counters.length) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var el = entry.target;
          var target = parseInt(el.getAttribute("data-count"), 10);
          var current = 0;
          var step = Math.max(1, Math.ceil(target / 60));
          var timer = setInterval(function () {
            current += step;
            if (current >= target) {
              current = target;
              clearInterval(timer);
            }
            el.textContent = current.toLocaleString();
          }, 20);
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.4 });
    counters.forEach(function (el) { observer.observe(el); });
  }
});
