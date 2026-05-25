import pandas as pd
import numpy as np
import pickle
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
print(" Step 1: Downloading Titanic Dataset from source repository...")
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)
print(" Step 2: Executing Data Engineering & Feature Transformations...")
# Feature Engineering: Combine family indicators
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
# Drop completely unique metadata identifiers that cause overfitting
df.drop(columns=['PassengerId', 'Name', 'Ticket', 'Cabin'], inplace=True, errors='ignore')
# Fix missing data anomalies without generating chained assignment warning flags
df['Age'] = df['Age'].fillna(df['Age'].median())
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
# Feature Encoding: Structural conversion of text flags into numeric one-hot arrays
df = pd.get_dummies(df, columns=['Sex', 'Embarked'], drop_first=True)
# Separate input arrays from target output classifications
X = df.drop(columns=['Survived'])
y = df['Survived']
# Record clean feature sorting arrays to guarantee alignment across API layers
model_columns = list(X.columns)
with open('columns.json', 'w') as f:
 json.dump(model_columns, f)
print(" Feature sequence schema correctly recorded to columns.json")
# Split dataset partitions cleanly using 80/20 standard operational division
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(" Step 3: Initializing and Training Random Forest Classifier Ensemble...")
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)
# Evaluate model performance against the validation dataset
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f" Model Training Phase Complete. Validation Holdout Accuracy: {accuracy:.2%}")
print("\n--- Detailed Classification Metrics Report ---")
print(classification_report(y_test, predictions, target_names=['Perished', 'Survived']))
print(" Step 4: Serializing trained model state to binary disk array...")
with open('titanic_model.pkl', 'wb') as f:
 pickle.dump(model, f)
print(" Pipeline complete. Artifact saved as titanic_model.pkl")
