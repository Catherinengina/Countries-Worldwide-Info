#!/usr/bin/env python
# coding: utf-8

# Libraries

# In[48]:


import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


# Load the clean data

# In[49]:


df = pd.read_csv(r"C:\Users\hp\Documents\Countries Worldwide Info\cleaned_countriesdata.csv")
print(df.head())


# Drop rows with missing/invalid data

# In[50]:


df = df.dropna(subset=["Area", "Population"])


# Define X(Feature) and Y(Target) and train-test split.

# In[51]:


X = df[["Area"]] 
y = df["Population"]  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Train Model

# In[52]:


model = LinearRegression()
model.fit(X_train, y_train)


# Prediction

# In[53]:


y_pred = model.predict(X_test)


# Evaluate Model

# In[54]:


mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.2f}")


# In[55]:


print(f"R² Score: {r2:.2f}")


# Plot

# In[56]:


plt.scatter(X_test, y_test, color='blue', label="Actual")
plt.plot(X_test, y_pred, color='red', linewidth=2, label="Predicted")
plt.title("Population vs Area (Regression)")
plt.xlabel("Area")
plt.ylabel("Population")
plt.legend()
plt.grid(True)
plt.show()


# In[57]:


get_ipython().system('jupyter nbconvert --to script "ML_Model.ipynb"')

