from logica.Processando_dados import QuadraticModel 
from logica.Processando_dados import optimal_point
import numpy as np
import pandas as pd
# Test data and coefficients
data = {
    'concentration': [3.252, 3.26, 3.251, 1.26, 5.2, 1.305, 5.198, 3.252, 3.242, 0.502, 6.001],
    'temperature': [880, 880, 880, 795.1, 795.1, 964.9, 964.9, 760, 1000, 880, 880],
    'IDT': [52.77, 77.77, 68.07, 80.57, 70.83, 31.93, 29.2, 81.25, 26.4, 179.15, 63.9]
}

coefficients = [-1228.82, 3.41, -49.37, -0.0021, 5.03397263, 0.0071]

# Create a DataFrame from the data
data_df = pd.DataFrame(data)

# Initialize the QuadraticModel with the data and coefficients
model = QuadraticModel(data_df)

# Test expected_response method
test_point = [3.5, 850]  # Replace with a realistic test point from your domain
expected_response = model.expected_response(test_point)
print(f"Expected response at point {test_point}: {expected_response}")
minimum = optimal_point(model)
print(f"Minimum is: {minimum.x} " )

# Test quadratic_plot method (this will show the plot)
print("Generating plot...")
model.quadratic_plot()
