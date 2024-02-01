import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score

# Sample data (replace with your actual data)
traffic_data = {
    'timestamp': pd.date_range('2024-01-01', '2024-02-01', freq='H'),
    'traffic_volume': [100, 120, 110, 90, 150, 130, 160, 140, 180, 200, 190, 170, 220, 210, 230, 250, 240, 260, 280, 270, 290, 300, 320, 310, 330, 350, 340, 360, 380, 370, 390]
}

crime_data = {
    'timestamp': pd.date_range('2024-01-01', '2024-02-01', freq='H'),
    'crime_rate': [10, 8, 12, 15, 11, 9, 13, 14, 10, 8, 12, 15, 11, 9, 13, 14, 10, 8, 12, 15, 11, 9, 13, 14, 10, 8, 12, 15, 11, 9, 13, 14]
}

# Merge different datasets (you'd have more data sources)
df_traffic = pd.DataFrame(traffic_data)

df_crime = pd.DataFrame(crime_data)

# Assume a shared timestamp between traffic and crime data
df = pd.merge(df_traffic, df_crime, on='timestamp')

# Feature engineering (add more features as needed)
df['hour'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.dayofweek

# Split data for traffic prediction and crime classification
X_traffic = df[['hour', 'day_of_week']]
y_traffic = df['traffic_volume']

X_crime = df[['hour', 'day_of_week']]
y_crime = df['crime_rate']

X_train_traffic, X_test_traffic, y_train_traffic, y_test_traffic = train_test_split(X_traffic, y_traffic, test_size=0.2, random_state=42)
X_train_crime, X_test_crime, y_train_crime, y_test_crime = train_test_split(X_crime, y_crime, test_size=0.2, random_state=42)

# Train models for traffic prediction and crime classification
model_traffic = RandomForestRegressor(n_estimators=100, random_state=42)
model_traffic.fit(X_train_traffic, y_train_traffic)

model_crime = RandomForestClassifier(n_estimators=100, random_state=42)
model_crime.fit(X_train_crime, y_train_crime)

# Make predictions
y_pred_traffic = model_traffic.predict(X_test_traffic)
y_pred_crime = model_crime.predict(X_test_crime)

# Evaluate models
mse_traffic = mean_squared_error(y_test_traffic, y_pred_traffic)
accuracy_crime = accuracy_score(y_test_crime, y_pred_crime)

print(f'Traffic Mean Squared Error: {mse_traffic}')
print(f'Crime Classification Accuracy: {accuracy_crime}')
