import pandas as pd
import numpy as np
import streamlit as st
import xnat
import os
import plotly.express as px
import matplotlib.pyplot as plt

# # For local testing
# os.environ['JUPYTERHUB_USER'] = 'admin'
# os.environ['JUPYTERHUB_SERVICE_PREFIX'] = '/'
# os.environ['XNAT_HOST'] = 'http://localhost'
# os.environ['XNAT_USER'] = 'admin'
# os.environ['XNAT_PASS'] = 'admin'
# os.environ['XNAT_ITEM_ID'] = 'C4KC-KiTS'

# XNAT Setup
xnat_host = os.getenv('XNAT_HOST')
xnat_user = os.getenv('XNAT_USER')
xnat_password = os.getenv('XNAT_PASS')

project_id = os.getenv('XNAT_ITEM_ID')

connection = xnat.connect(xnat_host, user=xnat_user, password=xnat_password)
project = connection.projects[project_id]

# Cache for subject data
subject_data_cache = None

# Compile subject data or return cached data
def get_subject_data():
    global subject_data_cache
    
    if subject_data_cache is not None:
        return subject_data_cache
    
    subject_data = {
        'id': [],
        'gender': [],
        'age': []
    }

    for subject in project.subjects.values():
        subject_data['id'].append(subject.label)
        subject_data['gender'].append(subject.demographics.gender)
        subject_data['age'].append(subject.demographics.age)
        
    df = pd.DataFrame(subject_data)
    
    subject_data_cache = df

    return df

# Start Streamlit

st.title(f"Subject demographics for project {project_id}")

st.write("This is a demo of a Streamlit app that shows subject demographics for a project in XNAT.")

st.markdown("### Subject data")

# Show a table of subject data
df = get_subject_data()
st.dataframe(df, width=700, height=300)

# Histogram of ages
st.markdown("## Histogram of ages")
st.markdown("### Using Plotly")
fig1 = px.histogram(df, x="age")
fig1.update_layout(bargap=0.2)
st.plotly_chart(fig1)

# Pie chart of genders
st.markdown("## Pie chart of genders")
st.markdown("### Using Matplotlib")
fig2, ax = plt.subplots()
df['gender'].value_counts().plot.pie(ax=ax, autopct='%1.1f%%')
st.pyplot(fig2)


