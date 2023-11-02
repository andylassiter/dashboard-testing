import pandas
import numpy
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
        
    df = pandas.DataFrame(subject_data)
    
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


st.title("Streamlit intro demo")
st.write("Examples below were taken from:  https://streamlit.io/docs/getting_started.html#get-started")

st.subheader("Here's our first attempt at using data to create a table:")

st.code("""
df = pandas.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})
""", language='python')
df = pandas.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})
# here we use 'magic', 
# any time that Streamlit sees a variable or a literal value on its own line, 
# it automatically writes that to your app using st.write()
df


st.subheader("Draw a line hart:")
st.code("""
chart_data = pandas.DataFrame(
     numpy.random.randn(20, 3),
     columns=['a', 'b', 'c'])
st.line_chart(chart_data)
""", language='python')

chart_data = pandas.DataFrame(
     numpy.random.randn(20, 3),
     columns=['a', 'b', 'c'])
st.line_chart(chart_data)


st.subheader("Let’s use Numpy to generate some sample data and plot it on a map of San Francisco:")

st.code("""
map_data = pandas.DataFrame(
    numpy.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
st.map(map_data)
""", language='python')

map_data = pandas.DataFrame(
    numpy.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
st.map(map_data)


st.title("Add interactivity with widgets")

st.subheader("Use checkboxes to show/hide data")

st.code("""
if st.checkbox('Show dataframe'):
    chart_data = pandas.DataFrame(
       numpy.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    st.line_chart(chart_data)
""", language='python')

if st.checkbox('Show dataframe'):
    chart_data = pandas.DataFrame(
       numpy.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    st.line_chart(chart_data)


st.subheader("Put widgets in a sidebar")

st.code("""
if st.checkbox('Show in sidebar'):
    option = st.sidebar.selectbox(
        'Which number do you like best?',
        ["a", "b","c"])

    'You selected:', option
""", language='python')

if st.checkbox('Show in sidebar'):
    option = st.sidebar.selectbox(
        'Which number do you like best?',
        ["a", "b","c"])

    'You selected:', option


st.subheader("Show progress")

st.code("""
import time

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'
""", language='python')  

import time

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'
