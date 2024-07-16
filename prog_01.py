import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Charger les données
data = pd.read_csv('./exercice_data.csv', encoding='latin1')  # You can change 'latin1' to the correct encoding

# Afficher les premières lignes du dataset
print(data.head())
# Select relevant features
features = data[['StudentID', 'FinalGrade', 'absences', 'Dalc', 'Walc', 'studytime']]

# Check for any missing values and handle them if necessary
features.dropna(inplace=True)

# Calculate complexity score
features['complexity'] = features['absences'] + features['Dalc'] + features['Walc'] - features['studytime']

# Streamlit app
st.title('Student Support Prioritization Dashboard')

# Plotting
plt.figure(figsize=(10, 6))
sns.scatterplot(x='FinalGrade', y='complexity', data=features, hue='complexity', palette='viridis', size='complexity', sizes=(20, 200))
plt.title('Student Support Prioritization')
plt.xlabel('Final Grade')
plt.ylabel('Complexity of Support')
plt.legend(title='Complexity')

# Streamlit plotting
st.subheader('Student Support Needs')
st.write('Students needing support are highlighted based on their final grades and complexity of support required.')
st.pyplot(plt)