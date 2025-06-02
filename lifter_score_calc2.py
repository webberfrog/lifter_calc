import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Coefficients for GL and DOTS
GL_COEFFS_MALE = [1199.72839, 1025.18162, .00921]
GL_COEFFS_FEMALE = [610.32796, 1045.59282, .03048]

DOTS_COEFFS_MALE = [-307.75076, 24.0900756, -0.1918759221, .0007391293, -1.093e-06]
DOTS_COEFFS_FEMALE = [-57.96288, 13.6175032, -0.1126655495, 0.0005158568, -1.0706e-06]

def calculate_score_gl(bw, total, coeffs):
    a, b, c = coeffs
    denominator = a - b * np.exp(-1 * c * bw)
    return 100 * (total / denominator)

def calculate_score_dots(bw, total, coeffs):
    a, b, c, d, e = coeffs
    denominator = a + b * bw + c * bw**2 + d * bw**3 + e * bw**4
    return 500 * (total / denominator)

def derivative_wrt_bw_gl(bw, total, coeffs, h=1e-3):
    s_plus = calculate_score_gl(bw + h, total, coeffs)
    s_minus = calculate_score_gl(bw - h, total, coeffs)
    return (s_plus - s_minus) / (2 * h)

def derivative_wrt_bw_dots(bw, total, coeffs, h=1e-3):
    s_plus = calculate_score_dots(bw + h, total, coeffs)
    s_minus = calculate_score_dots(bw - h, total, coeffs)
    return (s_plus - s_minus) / (2 * h)

# ----- Derivative of required total vs BW for fixed scores -----
def fixed_score_total_derivative_gl(bw, coeffs, fixed_score, h=1e-3):
    def total_from_bw(bw_val):
        a, b, c = coeffs
        denom = a - b * np.exp(-1 * c * bw_val)
        return (fixed_score / 100) * denom

    total_plus = total_from_bw(bw + h)
    total_minus = total_from_bw(bw - h)
    return (total_plus - total_minus) / (2 * h)

def fixed_score_total_derivative_dots(bw, coeffs, fixed_score, h=1e-3):
    def total_from_bw(bw_val):
        a, b, c, d, e = coeffs
        denom = a + b*bw_val + c*bw_val**2 + d*bw_val**3 + e*bw_val**4
        return (fixed_score / 500) * denom

    total_plus = total_from_bw(bw + h)
    total_minus = total_from_bw(bw - h)
    return (total_plus - total_minus) / (2 * h)

# ----- User input -----
gender = input("Enter gender (male/female): ").strip().lower()
if gender == "male":
    gl_coeffs = GL_COEFFS_MALE
    dots_coeffs = DOTS_COEFFS_MALE
elif gender == "female":
    gl_coeffs = GL_COEFFS_FEMALE
    dots_coeffs = DOTS_COEFFS_FEMALE
else:
    print("Invalid input. Please enter 'male' or 'female'.")
    exit(1)

try:
    user_bw = float(input("Enter your bodyweight in kg: "))
    user_total = float(input("Enter your total in kg: "))
except ValueError:
    print("Invalid number. Please enter numeric values for bodyweight and total.")
    exit(1)

# ----- Individual Calculations -----
user_gl = calculate_score_gl(user_bw, user_total, gl_coeffs)
user_dots = calculate_score_dots(user_bw, user_total, dots_coeffs)
# debugging

gl_deriv = derivative_wrt_bw_gl(user_bw, user_total, gl_coeffs)
dots_deriv = derivative_wrt_bw_dots(user_bw, user_total, dots_coeffs)

# Compute derivatives at user's bodyweight
dtotal_dbw_gl = fixed_score_total_derivative_gl(user_bw, gl_coeffs, user_gl)
dtotal_dbw_dots = fixed_score_total_derivative_dots(user_bw, dots_coeffs, user_dots)

# ----- Output Results -----
print(f"\n--- Results ({gender.capitalize()}) ---")
print(f"Bodyweight: {user_bw:.2f} kg")
print(f"Total:      {user_total:.2f} kg")
print(f"GL Points:  {user_gl:.2f}")
print(f"DOTS Score: {user_dots:.2f}")
print(f"∂GL/∂BW:    {gl_deriv:.4f} points/kg")
print(f"∂DOTS/∂BW:  {dots_deriv:.4f} points/kg")

print(f"dTotal/dBW @ fixed GL:    {dtotal_dbw_gl:.4f} kg/kg")
print(f"dTotal/dBW @ fixed DOTS:  {dtotal_dbw_dots:.4f} kg/kg")

# ----- Surface Plot Ranges -----
bw_range = np.linspace(40, 150, 100)
total_range = np.linspace(300, 1000, 100)
BW, TOTAL = np.meshgrid(bw_range, total_range)

GL_POINTS = calculate_score_gl(BW, TOTAL, gl_coeffs)
DOTS_POINTS = calculate_score_dots(BW, TOTAL, dots_coeffs)

# ----- Plot GL Points -----
fig1 = plt.figure(figsize=(12, 8))
ax1 = fig1.add_subplot(111, projection='3d')
surf1 = ax1.plot_surface(BW, TOTAL, GL_POINTS, cmap='viridis', edgecolor='none')
ax1.scatter(user_bw, user_total, user_gl, color='black', s=50, label='Your Score')
ax1.set_title(f'GL Points Surface Plot ({gender.capitalize()})')
ax1.set_xlabel('Bodyweight (kg)')
ax1.set_ylabel('Total (kg)')
ax1.set_zlabel('GL Points')
ax1.legend()
fig1.colorbar(surf1, shrink=0.5, aspect=10, label='GL Points')

# ----- Plot DOTS Score -----
fig2 = plt.figure(figsize=(12, 8))
ax2 = fig2.add_subplot(111, projection='3d')
surf2 = ax2.plot_surface(BW, TOTAL, DOTS_POINTS, cmap='plasma', edgecolor='none')
ax2.scatter(user_bw, user_total, user_dots, color='black', s=50, label='Your Score')
ax2.set_title(f'DOTS Score Surface Plot ({gender.capitalize()})')
ax2.set_xlabel('Bodyweight (kg)')
ax2.set_ylabel('Total (kg)')
ax2.set_zlabel('DOTS Score')
ax2.legend()
fig2.colorbar(surf2, shrink=0.5, aspect=10, label='DOTS Score')

# ----- 2D Plot: GL Points vs Total -----
totals_for_plot = np.linspace(300, 1000, 300)
gl_scores_for_plot = [calculate_score_gl(user_bw, t, gl_coeffs) for t in totals_for_plot]

fig3 = plt.figure(figsize=(10, 6))
plt.plot(totals_for_plot, gl_scores_for_plot, label=f'GL Points at BW = {user_bw:.1f}kg')
plt.scatter(user_total, user_gl, color='red', zorder=5, label='Your Score')
plt.title('GL Points vs Total at Fixed Bodyweight')
plt.xlabel('Total (kg)')
plt.ylabel('GL Points')
plt.grid(True)
plt.legend()

# ----- 2D Plot: Total vs Bodyweight for Fixed GL Score -----
bw_vals = np.linspace(40, 150, 300)
# Invert the GL formula to find total required to maintain same GL score
required_totals_gl = []
for bw in bw_vals:
    a, b, c = gl_coeffs
    denominator = a - b * np.exp(-1 * c * bw)
    total_required = (user_gl / 100) * denominator
    required_totals_gl.append(total_required)

# Calculate totals required to maintain fixed DOTS score
required_totals_dots = []
for bw in bw_vals:
    a, b, c, d, e = dots_coeffs
    denominator = a + b * bw + c * bw**2 + d * bw**3 + e * bw**4
    total_required = (user_dots / 500) * denominator
    required_totals_dots.append(total_required)

# Plot both curves
fig4 = plt.figure(figsize=(10, 6))
plt.plot(bw_vals, required_totals_gl, label=f'Total for {user_gl:.1f} GL Points', color='blue')
plt.plot(bw_vals, required_totals_dots, label=f'Total for {user_dots:.1f} DOTS Score', color='green')
plt.scatter(user_bw, user_total, color='red', zorder=5, label='Your Score')
plt.title(f'Total vs Bodyweight for Fixed Scores ({gender.capitalize()})')
plt.xlabel('Bodyweight (kg)')
plt.ylabel('Total (kg)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
