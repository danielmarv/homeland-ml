import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Function to generate synthetic anomaly data
def generate_anomaly_data():
    normal_data = np.random.normal(loc=10, scale=2, size=1000)
    anomaly_data = np.concatenate([normal_data[:800], normal_data[900:] + 20])
    all_data = np.concatenate([normal_data, anomaly_data])
    all_data = all_data.reshape(-1, 1)
    return all_data

# Function to generate synthetic electricity consumption data
def generate_electricity_data():
    time_points = np.arange(0, 100, 1)
    consumption = 50 + 2 * time_points + np.random.normal(scale=5, size=len(time_points))
    return time_points, consumption

# Function to update the anomaly and electricity consumption plots in real-time
def update_all(frame):
    global all_data, gmm, threshold, time_points, consumption, lr_model

    # Generate new anomaly data
    new_anomaly_data = generate_anomaly_data()

    # Update the anomaly detection model with the new data
    all_data = np.concatenate([all_data, new_anomaly_data])
    probs = gmm.score_samples(all_data)

    # Set a threshold for anomaly detection (adjust as needed)
    threshold = np.percentile(probs, 5)

    # Identify anomalies based on the threshold
    anomalies = all_data[probs < threshold]

    # Generate new electricity consumption data
    new_time, new_consumption = generate_electricity_data()

    # Update the linear regression model with the new electricity consumption data
    time_points = np.concatenate([time_points, new_time])
    consumption = np.concatenate([consumption, new_consumption])
    lr_model.fit(time_points.reshape(-1, 1), consumption)

    # Predict future consumption
    future_time = np.arange(0, 110, 1)
    future_consumption = lr_model.predict(future_time.reshape(-1, 1))

    # Clear the previous plots and plot the updated data
    plt.subplot(2, 1, 1)
    plt.cla()
    plt.hist(all_data, bins=50, density=True, alpha=0.5, color='blue', label='Normal Data')
    plt.hist(anomalies, bins=50, density=True, alpha=0.5, color='red', label='Anomalies')
    plt.title('Real-Time Anomaly Detection')
    plt.xlabel('Data Values')
    plt.ylabel('Density')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.cla()
    plt.plot(time_points, consumption, label='Actual Consumption', color='blue', marker='o')
    plt.plot(future_time, future_consumption, label='Predicted Consumption', linestyle='--', color='green', marker='x')
    plt.title('Real-Time Electricity Consumption Prediction')
    plt.xlabel('Time')
    plt.ylabel('Consumption')
    plt.legend()

# Initialize the anomaly and electricity consumption data and models
all_data = generate_anomaly_data()
gmm = GaussianMixture(n_components=2)
gmm.fit(all_data)
threshold = np.percentile(gmm.score_samples(all_data), 5)

time_points, consumption = generate_electricity_data()
lr_model = LinearRegression()

# Create a real-time updating plot for both anomaly detection and electricity consumption
fig = plt.figure(figsize=(12, 8))  # Set the figure size
ani_all = FuncAnimation(fig, update_all, interval=1000)  # Update every 1000 milliseconds (1 second)

# Display the integrated plot
plt.show()
