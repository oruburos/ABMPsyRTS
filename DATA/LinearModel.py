import pandas as pd
from sklearn import linear_model

# load the dataset into memory
training_dataset = pd.read_csv("SimplestData.csv")

# create a model using the linear regression algorithm
# and train it with the data from our csv
regression_model = linear_model.LinearRegression()
print ("Training model...")

# model training
regression_model.fit(training_dataset[['exploration']], training_dataset.competitors)
print ("Model trained.")

# ask user to enter an area and calculate
# its price using our model
input_area = 3
proped_price = regression_model.predict([[input_area]])
print ("Proped price:", round(proped_price[0], 2))