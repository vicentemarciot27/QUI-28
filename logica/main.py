##logica principal
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Generate random data

np.random.seed(42)  # For reproducibility
data = {
    'x': np.random.rand(50),
    'y': np.random.rand(50),
    'z': np.random.rand(50)
}

# Create DataFrame
df = pd.DataFrame(data)

# Fit a quadratic model
X = df[['x', 'y']]
X = sm.add_constant(X)
y = df['z']
model = sm.OLS(y, X).fit()

# Create a meshgrid for prediction
x_vals = np.linspace(df['x'].min(), df['x'].max(), 50)
y_vals = np.linspace(df['y'].min(), df['y'].max(), 50)
x_mesh, y_mesh = np.meshgrid(x_vals, y_vals)
x_flat = x_mesh.flatten()
y_flat = y_mesh.flatten()
X_pred = sm.add_constant(pd.DataFrame({'x': x_flat, 'y': y_flat}))

# Predict z values using the model
z_pred = model.predict(X_pred)
z_mesh = z_pred.values.reshape(x_mesh.shape)  # Corrected line

# Create a 3D surface plot with the quadratic model
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x_mesh, y_mesh, z_mesh, cmap='viridis')

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Surface Plot with Quadratic Model')

# Show the plot
plt.show()