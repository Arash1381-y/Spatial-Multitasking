import numpy as np
import matplotlib.pyplot as plt

# Generate random data for three normal distributions
data_1 = np.random.normal(loc=0, scale=1, size=10000)
data_2 = np.random.normal(loc=4, scale=0.5, size=10000)
data_3 = np.random.normal(loc=7, scale=0.8, size=10000)

# Concatenate the data to create a trimodal distribution
trimodal_data = np.concatenate((data_1, data_2, data_3))

# Plot the histogram to visualize the trimodal distribution
plt.hist(trimodal_data, bins=250, alpha=0.7, color='skyblue')
plt.title('Trimodal Distribution')
plt.xlabel('Time Unit')
plt.ylabel('Frequency')
plt.show()

