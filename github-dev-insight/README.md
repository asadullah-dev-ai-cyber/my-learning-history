# ⚡ DevInsight — GitHub Developer Analytics Platform

DevInsight is a modern Flask web application designed to analyze GitHub developer profiles, aggregate repository metrics, showcase top projects, and evaluate overall developer performance using custom scoring algorithms and dynamic visualizations.

---

## 🌟 Key Features

* **Dual-Theme 3D Interface**: Adaptive Dark and Light modes with local persistence, glassmorphic styling, and interactive mouse-tracking card physics.
* **Custom Scoring Engine**: Evaluates public profile metrics to derive custom **Quality Index**, **Tech Diversity**, and **Activity Index** scores (0–100 scale) alongside developer level tiers.
* **Top Repositories Grid**: Renders project cards featuring direct GitHub repository links, star counts, fork counters, primary languages, and calculated file sizes.
* **Account Tenure Tracking**: Formats and displays the developer's exact GitHub join date.
* **Interactive Visualizations**: Embedded Chart.js doughnut chart rendering real-time language distributions.
* **Rate-Limit Optimized**: Supports GitHub Personal Access Tokens (Classic and Fine-Grained) via environment configuration to enable up to 5,000 API requests per hour.

---

## 🛠️ Project Structure