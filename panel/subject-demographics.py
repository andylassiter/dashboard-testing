import panel as pn
import hvplot.pandas
import pandas as pd
import numpy as np
import xnat
import os

# XNAT setup
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


# Panel setup
pn.extension(design='material')

csv_file = ("https://raw.githubusercontent.com/holoviz/panel/main/examples/assets/occupancy.csv")
data = pd.read_csv(csv_file, parse_dates=["date"], index_col="date")

df = get_subject_data()
df_pane = pn.pane.DataFrame(df, sizing_mode="stretch_both", max_height=300)

first_app = pn.Column(df_pane)

first_app.servable()
first_app