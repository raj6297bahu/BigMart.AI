
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Read data
print("Reading data...")
train = pd.read_csv("train.csv")
df = pd.DataFrame(train)

# Preprocessing
print("Preprocessing...")

# Drop columns
df.drop("Outlet_Size", axis=1, inplace=True)
df.drop("Item_Weight", axis=1, inplace=True)
df.drop("Item_Identifier", inplace=True, axis=1)

# Map Item_Fat_Content
fat = {"Low Fat": 0, "Regular": 1, "low fat": 0, "LF": 0, "reg": 1}
df['Item_Fat_Content'] = [fat[item] for item in df['Item_Fat_Content']]

# Handle Item_Visibility outliers
q3, q1 = np.percentile(df["Item_Visibility"], [75, 25])
iqr = q3 - q1
df.loc[df["Item_Visibility"] > 1.5 * iqr, "Item_Visibility"] = 0.066132

# Map Item_Type
itemtype = {'Baking Goods': 0, 'Breads': 1, 'Breakfast': 2, 'Canned': 3, 'Dairy': 4,
            'Frozen Foods': 5, 'Fruits and Vegetables': 6, 'Hard Drinks': 7,
            'Health and Hygiene': 12, 'Household': 11, 'Meat': 10, 'Others': 9, 'Seafood': 8,
            'Snack Foods': 13, 'Soft Drinks': 14, 'Starchy Foods': 15}
df['Item_Type'] = [itemtype[item] for item in df['Item_Type']]

# Drop Outlet_Identifier
df.drop("Outlet_Identifier", axis=1, inplace=True)

# Age
df["Age_Outlet"] = 2021 - df["Outlet_Establishment_Year"]
df.drop("Outlet_Establishment_Year", axis=1, inplace=True)

# Map Outlet_Location_Type
tier = {'Tier 1': 0, 'Tier 2': 1, 'Tier 3': 2}
df['Outlet_Location_Type'] = [tier[item] for item in df['Outlet_Location_Type']]

# Map Outlet_Type
market_type = {'Grocery Store': 0, 'Supermarket Type1': 1, 'Supermarket Type2': 2,
               'Supermarket Type3': 3}
df['Outlet_Type'] = [market_type[item] for item in df['Outlet_Type']]

# Split Data
print("Splitting data...")
X = df.drop("Item_Outlet_Sales", axis=1)
y = df["Item_Outlet_Sales"]
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=42)

# Train Model
print("Training Random Forest model...")
rf = RandomForestRegressor(n_estimators=400, max_depth=6, min_samples_leaf=100, n_jobs=-1)
rf.fit(x_train, y_train)

# Save Model
print("Saving model.pkl...")
with open('model.pkl', 'wb') as file:
    pickle.dump(rf, file)

print("Done.")
