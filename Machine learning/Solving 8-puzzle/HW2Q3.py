import matplotlib.pyplot as plt

# random data points
high_risk = [(35, 20), (40, 15), (38, 10)]
low_risk = [(20, 60), (25, 70), (22, 80)]

plt.figure(figsize=(8, 6))

# points
plt.scatter(*zip(*high_risk), color='red', label='High Risk', marker='o', s=100)
plt.scatter(*zip(*low_risk), color='blue', label='Low Risk', marker='s', s=100)

# linear classifier 
plt.plot([10, 70], [40, 70], 'k--', label='Decision Boundary')

plt.title('Forest Fire Risk Classification', fontsize=14)
plt.xlabel('Temperature (°C)', fontsize=12)
plt.ylabel('Humidity (%)', fontsize=12)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.legend(fontsize=12)
plt.show()
