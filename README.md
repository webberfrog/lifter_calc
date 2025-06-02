# lifter_calc

# Powerlifting Score Visualizer

A Python tool for calculating and visualizing powerlifting scores — **GL Points** and **DOTS Score** — based on an athlete's bodyweight and powerlifting total.

This tool supports both **male** and **female** coefficient systems, and generates:
- 3D surface plots for GL and DOTS scores
- A 2D line plot of GL Points vs. Total at a fixed bodyweight
- Numerical derivatives of the scores with respect to bodyweight

---

## 📌 Features

- ✅ User input for gender, bodyweight, and total
- ✅ Calculates:
  - GL Points
  - DOTS Score
  - Derivatives with respect to bodyweight
- ✅ 3D surface plots:
  - GL Points vs Bodyweight & Total
  - DOTS Score vs Bodyweight & Total
  - Your input highlighted with a red marker
- ✅ 2D plot:
  - GL Points vs Total at your input bodyweight
  - Total vs bodyweight at your fixed gl score/dots score


---

## 🛠 Requirements

- Python 3.7+
- Required Python packages:

```bash
pip install numpy matplotlib
