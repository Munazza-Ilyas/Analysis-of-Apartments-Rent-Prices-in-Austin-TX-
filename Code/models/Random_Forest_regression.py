import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score, mean_absolute_error
import numpy as np
from sklearn.preprocessing import StandardScaler

# Load your CSV file
data = pd.read_csv('artifacts/result.csv')

# Use the selected columns as X
X = data.iloc[:, [1, 3, 5, 6, 7]]

# Use the first column (price) as Y
y = data.iloc[:, 0]

# split data into training and testing set
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.2,
                                                    random_state=42)

# Standardize X
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
X_scaled = scaler.transform(X)

# Initialize the Random Forest regressor
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model on the training data
rf_regressor.fit(X_train_scaled, y_train)

# Make predictions on the test data
y_pred = rf_regressor.predict(X_test_scaled)
''''Evaluate the model, we don't have to print all the evaluation metrics, 
just pick out those metrics that can clearly show the performance and easy to be interpreted.'''

# evaluate the model
# calculate the middle products
n = X_test.shape[0]  # number of observations
p = X_test.shape[1]  # number of coefficients except intercept
residuals = y_test - rf_regressor.predict(X_test)
rss = np.sum(residuals**2)
sum_percentage_error = 0

# calculate the final results
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
explained_variance = explained_variance_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
adjusted_r_squared = 1 - (1 - r2) * ((n - 1) / (n - p - 1))
aic = 2 * p + n * np.log(rss / n)
bic = n * np.log(rss / n) + (p + 1) * np.log(n)
rmse = mse**(1/2)
for i in range(n):
    if y_test.iloc[i] != 0:  # Avoid division by zero
        percentage_error = ((y_test.iloc[i] - y_pred[i]) / y_test.iloc[i]) * 100
        sum_percentage_error += percentage_error
mpe = sum_percentage_error / n

# show the result
print(f'R-squared (R2) Score: {r2}')
print(f'Adjusted R-squared: {adjusted_r_squared}')
print(f'Mean Squared Error: {mse}')
print(f'Mean Absolute Error: {mae}')
print(f'AIC: {aic}')
print(f'BIC: {bic}')
print(f'Rooted Mean Squared Error: {rmse}')
print(f'Mean Percentage Error: {mpe}')

'''Interaction with users'''

zip_code = str(
    input(
        'Please input the expected zip code (in Austin, TX) of your apartment: '
    ))  # input an integer like 78712, 78750, etc.
distance = str(
    input(
        'Please input the expected distance (in miles and keep two decimal places) to UT Austin of your apartment: '
    ))  # input a float like 0.85, 1.56, 2.08, etc.
bathrooms = str(
    input('Please input the expected number of bathrooms of your apartment: ')
)  # input an integer like 1, 2, 3, etc.
bedrooms = str(
    input('Please input the expected number of bedrooms of your apartment: ')
)  # input an integer like 1, 2, 3, etc.
living_area = str(
    input('Please input the expected living area in sqft. of your apartment: ')
)  # input a float like 1020, 805, 1874, etc.

data_user = {
    'Zip': zip_code,
    'Distance to the university (in miles)': distance,
    'Bathrooms': bathrooms,
    'Bedrooms': bedrooms,
    'LivingArea': living_area
}

X_user = pd.DataFrame(data_user, index=[0])
X_user_scaled = scaler.transform(X_user)
Y_user = rf_regressor.predict(X_user_scaled)

print(f'The estimated cost for your expected apartment is: {Y_user[0]}')
