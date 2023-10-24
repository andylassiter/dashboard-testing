import panel as pn
import hvplot.pandas

import pandas as pd
import numpy as np
import xnat
import os

# # For local testing
# os.environ['JUPYTERHUB_USER'] = 'admin'
# os.environ['JUPYTERHUB_SERVICE_PREFIX'] = '/'
# os.environ['XNAT_HOST'] = 'http://localhost'
# os.environ['XNAT_USER'] = 'admin'
# os.environ['XNAT_PASS'] = 'admin'
# os.environ['XNAT_ITEM_ID'] = 'C4KC-KiTS'

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

df = get_subject_data()
df_pane = pn.pane.DataFrame(df, sizing_mode="stretch_both", max_height=300)

histogram_age = df.hvplot.hist('age', bins=15, title='Age Distribution', height=300)
histogram_age.opts(xlabel='Age', ylabel='Count')
histogram_age.opts(width=500, height=300)

template = pn.template.BootstrapTemplate(
    title=f"XNAT Panel App",
    busy_indicator=pn.indicators.BooleanStatus(value=False)
)

template.main.append(
    pn.Row(
        pn.Column(df_pane),
        pn.Column(histogram_age)
    )
)

template.servable()