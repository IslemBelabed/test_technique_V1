import streamlit as st
import pandas as pd
import plotly.express as px


# Import data file
data = pd.read_csv('./exercice_data.csv', encoding='latin1') 

# Show first line of the data file
print(data.head())

# Select relevant features
features = data[['StudentID' , 'FinalGrade', 'absences', 'traveltime' , 'studytime' , 'failures' , 'famrel' , 'Dalc', 'Walc', 'health' , 'schoolsup' , 'famsup' , 'paid' , 'activities' , 'nursery']]

# Replace 'yes'/'no' features with 1/0
features['schoolsup'] = features['schoolsup'].replace({'yes': 1, 'no': 0})
features['famsup'] = features['famsup'].replace({'yes': 1, 'no': 0})
features['paid'] = features['paid'].replace({'yes': 1, 'no': 0})
features['activities'] = features['activities'].replace({'yes': 1, 'no': 0})
features['nursery'] = features['nursery'].replace({'yes': 1, 'no': 0})


# Create the 'existant_support' feature by adding the yes or no features together
features['existant_support'] = features['schoolsup'] + features['famsup'] + features['paid'] + features['activities'] + features['nursery']

# Check for any missing values and handle them if necessary
features.dropna(inplace=True)

# Define the function to calculate absences_rate to bring it the value to scale from 1 to 5
def calculate_absences_rate(absences):
    if absences <= 5:
        return 1
    elif absences <= 10:
        return 2
    elif absences <= 15:
        return 3
    elif absences <= 20:
        return 4
    else:
        return 5

# Apply the function to create the new absence rate 
features['absences_rate'] = features['absences'].apply(calculate_absences_rate)

# Calculate complexity score based on a formula taking into account relevant features 
# Bring all values to the lowest commun multiple of 4 and 5 which is 20 (as all values used are on scales from 0 to 4 or 5)
# Assign coefficients to balance the equation and then devide by the number of coifficients (17)
# Divide by 2 to get the complexity score on a scale from 0 to 10 
# Equation was updated on 19/07 as there was an initial mistake regarding the parenthesis
features['complexity_score'] = ((features['traveltime'] * 5 - features['studytime'] * 5 + features['failures'] * 5 - features['famrel'] * 5 + 
                           (features['Dalc'] * 4) * 4 + (features['Walc'] * 4) * 3 + (features['health'] * 4) * 3 + 
                           (features['absences_rate'] * 4) * 2 - (features['existant_support'] * 4)) / 17) / 2

# Create 'complexity' based on 'complexity_score' with minimum value of 0
# This is necessary as the complexity score equation contains both substructions and additions 
# This means that theoritically we might get negative values 
# In order to avoid any bugs, we give the complexity score a minimum of 0
features['complexity'] = features['complexity_score'].apply(lambda x: max(x, 0))

# Calculate values needed for the summary statistics section

# Calculate the mean values of final grades and complexity
final_grade_mean = features['FinalGrade'].mean()
complexity_mean = features['complexity'].mean()

# Calculate the percentage of students with final grades under 10
students_below_10 = features[features['FinalGrade'] < 10]
percentage_below_10 = (len(students_below_10) / len(features)) * 100

# Calculate percentage of students with complexity > 2
students_above_complexity_4 = features[features['complexity'] > 4]
percentage_complexity_above_4 = (len(students_above_complexity_4) / len(features)) * 100

# Create The Mouse Hover Text
features['hover_text'] = "Student ID: " + features['StudentID'].astype(str)

# Streamlit app
st.title('Student Support Prioritization Dashboard')

# Plotting 
# We show Improvability score instead of complexity score to the user to avoid the negative connotations of "complexity"
fig = px.scatter(
    features,
    x='FinalGrade',
    y='complexity',
    color='complexity',
    size='complexity',
    hover_name='hover_text',
    title='Student Support Prioritization',
    labels={'FinalGrade': 'Final Grade', 'complexity': 'Improvability Score'},
    color_continuous_scale='viridis',
    size_max=10)

# Streamlit plotting
st.subheader('Student Support Needs')
st.write('Students needing support are highlighted based on their final grades and their improvability scores.')
st.plotly_chart(fig)

# Display the summary values below the plot
st.subheader('Summary Statistics')
st.write(f"**Mean Final Grade:** {final_grade_mean:.2f}")
st.write(f"**Percentage of Students with Final Grades Below 10:** {percentage_below_10:.2f}%")
st.write(f"**Mean Improvability Score:** {complexity_mean:.2f}")
st.write(f"**Percentage of Students with Improvability Scores Above 4:** {percentage_complexity_above_4:.2f}%")