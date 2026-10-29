/**
 * ==============================================================================
 * GLOBAL RETAIL ANALYTICS - PORTFOLIO SHOWCASE JAVASCRIPT
 * Pure ES6 JavaScript - Zero external runtime dependencies
 * ==============================================================================
 */

document.addEventListener("DOMContentLoaded", function () {
  initCounters();
  initTabs();
  initAccordion();
  initGalleryModal();
  initCopyButtons();
  initSmoothScroll();
});

/* ------------------------------------------------------------------------------
 * 1. Animated Metric Counters
 * ------------------------------------------------------------------------------ */
function initCounters() {
  const counterElements = document.querySelectorAll(".counter-anim");
  let hasAnimated = false;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && !hasAnimated) {
          hasAnimated = true;
          counterElements.forEach((el) => {
            const target = parseFloat(el.getAttribute("data-target"));
            const prefix = el.getAttribute("data-prefix") || "";
            const suffix = el.getAttribute("data-suffix") || "";
            const decimals = parseInt(el.getAttribute("data-decimals") || "0", 10);
            animateValue(el, 0, target, 1600, prefix, suffix, decimals);
          });
        }
      });
    },
    { threshold: 0.2 }
  );

  const kpiSection = document.querySelector(".kpi-section");
  if (kpiSection) {
    observer.observe(kpiSection);
  }
}

function animateValue(obj, start, end, duration, prefix, suffix, decimals) {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    // Ease-out expo
    const easeProgress = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
    const currentVal = easeProgress * (end - start) + start;
    obj.innerHTML = prefix + currentVal.toFixed(decimals) + suffix;
    if (progress < 1) {
      window.requestAnimationFrame(step);
    } else {
      obj.innerHTML = prefix + end.toFixed(decimals) + suffix;
    }
  };
  window.requestAnimationFrame(step);
}

/* ------------------------------------------------------------------------------
 * 2. Interactive Tool Showcase Tabs
 * ------------------------------------------------------------------------------ */
function initTabs() {
  const tabButtons = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  tabButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-tab");

      tabButtons.forEach((b) => b.classList.remove("active"));
      tabContents.forEach((c) => c.classList.remove("active"));

      btn.classList.add("active");
      const targetContent = document.getElementById(targetId);
      if (targetContent) {
        targetContent.classList.add("active");
      }
    });
  });
}

/* ------------------------------------------------------------------------------
 * 3. Business Questions Accordion
 * ------------------------------------------------------------------------------ */
function initAccordion() {
  const headers = document.querySelectorAll(".accordion-header");

  headers.forEach((header) => {
    header.addEventListener("click", () => {
      const item = header.parentElement;
      const isActive = item.classList.contains("active");

      // Optional: close other open items for single-accordion behavior
      document.querySelectorAll(".accordion-item").forEach((it) => {
        it.classList.remove("active");
      });

      if (!isActive) {
        item.classList.add("active");
      }
    });
  });
}

/* ------------------------------------------------------------------------------
 * 4. Image Gallery Modal Preview
 * ------------------------------------------------------------------------------ */
const galleryData = {
  fig1: {
    title: "Monthly Sales Revenue vs. Net Profit Trend (2023 - 2026)",
    src: "reports/figures/01_monthly_sales_profit_trend.png",
    desc: "Visualizes monthly financial trajectory over 46 operating months. Demonstrates persistent, predictable seasonal spikes in Q4 (November/December holiday surges) averaging over $330,000 in monthly sales volume while maintaining positive cumulative profitability.",
  },
  fig2: {
    title: "Product Sub-Category Profitability Ranking Matrix",
    src: "reports/figures/02_category_subcategory_profit.png",
    desc: "A horizontal diverging bar chart isolating positive profit generators from loss-makers. Copiers leads enterprise earnings with +$1,138,940 in profit, while Tables (-$296,061) and Bookcases (-$76,723) incur severe operational losses due to heavy shipping weight.",
  },
  fig3: {
    title: "Discount Tier vs. Realized Transaction Profit Margin (%)",
    src: "reports/figures/03_discount_vs_profit_margin.png",
    desc: "Box plot analysis examining margin distribution across 5 discount tiers. Margins start at +22.98% at zero discount, but collapse into negative returns (-8.91% and -38.53%) when discounts exceed 20%. Capping discounts recovers +$253,959 in lost EBITDA.",
  },
  fig4: {
    title: "Geographic Performance: Sales Revenue vs. Net Profit Margin %",
    src: "reports/figures/04_regional_performance.png",
    desc: "Compares the 4 macro territories. West leads sales volume ($3.18M, 33.05% share), while Central achieves the highest profit margin efficiency at 14.23% ($413.2K profit) supported by high-performing corporate hubs in Texas and Michigan.",
  },
  fig5: {
    title: "Customer Segment Economics: Volume vs. Transaction Ticket Size",
    src: "reports/figures/05_customer_segment_distribution.png",
    desc: "Donut chart of sales share and bar chart of Average Order Value (AOV). Consumer drives 52.3% of volume ($5.03M), but Home Office achieves both the highest ticket size ($1,005.23 AOV) and the highest net profit margin (13.50%).",
  },
};

function initGalleryModal() {
  const modal = document.getElementById("galleryModal");
  const modalImg = document.getElementById("modalImg");
  const modalTitle = document.getElementById("modalTitle");
  const modalDesc = document.getElementById("modalDesc");
  const modalClose = document.getElementById("modalClose");

  if (!modal) return;

  document.querySelectorAll(".gallery-card").forEach((card) => {
    card.addEventListener("click", () => {
      const figKey = card.getAttribute("data-fig");
      const data = galleryData[figKey];
      if (data) {
        modalImg.src = data.src;
        modalTitle.textContent = data.title;
        modalDesc.textContent = data.desc;
        modal.classList.add("active");
        document.body.style.overflow = "hidden";
      }
    });
  });

  const closeModal = () => {
    modal.classList.remove("active");
    document.body.style.overflow = "";
  };

  if (modalClose) modalClose.addEventListener("click", closeModal);
  modal.addEventListener("click", (e) => {
    if (e.target === modal) closeModal();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.classList.contains("active")) closeModal();
  });
}

/* ------------------------------------------------------------------------------
 * 5. Copy to Clipboard Functionality
 * ------------------------------------------------------------------------------ */
function initCopyButtons() {
  document.querySelectorAll(".copy-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const pre = btn.closest(".code-box").querySelector("pre");
      if (pre) {
        navigator.clipboard.writeText(pre.innerText).then(() => {
          const originalText = btn.innerText;
          btn.innerText = "Copied!";
          btn.style.backgroundColor = "#10B981";
          btn.style.color = "#FFFFFF";
          setTimeout(() => {
            btn.innerText = originalText;
            btn.style.backgroundColor = "";
            btn.style.color = "";
          }, 2000);
        });
      }
    });
  });
}

/* ------------------------------------------------------------------------------
 * 6. Smooth Scroll & Active Nav State
 * ------------------------------------------------------------------------------ */
function initSmoothScroll() {
  const navLinks = document.querySelectorAll(".nav-links a");
  const sections = document.querySelectorAll("section[id]");

  window.addEventListener("scroll", () => {
    let current = "";
    sections.forEach((section) => {
      const sectionTop = section.offsetTop - 100;
      const sectionHeight = section.offsetHeight;
      if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
        current = section.getAttribute("id");
      }
    });

    navLinks.forEach((link) => {
      link.classList.remove("active");
      if (link.getAttribute("href") === `#${current}`) {
        link.classList.add("active");
      }
    });
  });
}
