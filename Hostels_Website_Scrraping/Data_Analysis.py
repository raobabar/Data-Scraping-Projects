import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#To read file
df = pd.read_csv('Atira_dataset.csv')

#To print some rows in the dataframe
print(df.head())

#To print shape of the dataframe
print(df.shape)

#To print some of the statistics of the dataframe
print(df.describe())

#To show the histogram of capacity_of_persons
plt.hist(df['capacity_of_persons'])
plt.title('Histogram of Capacity of persons')
plt.xlabel('capacity_of_persons')
plt.ylabel('Frequency of capacity_of_persons')
plt.show()

#To show the graph of building_name
df['building_name'].value_counts().sort_values(ascending=True).plot(color='red')
df['building_name'].value_counts().sort_values(ascending=True).plot(kind='bar')
plt.title('Histogram of building_name')
plt.legend()
plt.xlabel('Building Name')
plt.ylabel('Frequency of Building Name')
plt.show()

#To show the histogram of price
plt.hist(df.price, bins=10)
plt.title('Histogram of price')
plt.xlabel('price')
plt.ylabel('Frequency of price')
plt.show()

#To show the scatter plot of capacity_of_persons Vs price
plt.scatter(x=df['capacity_of_persons'], y=df['price'])
plt.title('Scatter plot of capacity_of_persons Vs price')
plt.xlabel('Capacity of Persons')
plt.ylabel('Prices')
plt.show()

#To show the scatter plot of building_name Vs price
plt.scatter(x=df['building_name'], y=df['price'])
plt.title('Scatter plot of building_name Vs price')
plt.xlabel('Building Names')
plt.ylabel('Prices')
plt.show()

#To show the plot of building_name Vs location
df['building_name'].value_counts().plot(color='red')
df['location'].value_counts().plot(kind='bar')
plt.title('building_name Vs location')
plt.ylabel("Frequency")
plt.title("Count of buildings by location")
plt.legend()
plt.show()

#To group the data with respect to location and capacity_of_persons
grouped = df.groupby(['location', 'capacity_of_persons'])['location', 'capacity_of_persons', 'price']
grouped_data = grouped.aggregate(np.mean)
grouped_data['location'] = grouped_data.index
grouped_data.reset_index(drop=True, inplace=True)
grouped_data['capacity_of_persons'] = grouped_data['capacity_of_persons'].astype('int')

#To lower the values of price and plot it with price for getting insights from graph
grouped_data['price'] = grouped_data['price']/100
grouped_data[['capacity_of_persons', 'price']].plot(kind='line')
plt.show()

#To print the grouped data and sort it with respect to price
print(grouped_data.sort_values(by='price', ascending=True))

