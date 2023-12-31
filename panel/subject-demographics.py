import os

import numpy as np
import pandas as pd
import xnat

import hvplot.pandas
import panel as pn
import plotly.express as px

pn.extension('plotly')

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

# Subject data table
df = get_subject_data()
df_pane = pn.pane.DataFrame(df, sizing_mode="stretch_both", max_height=500)

# Histogram of age distribution
histogram_age = df.hvplot.hist('age', bins=15, height=300)
histogram_age.opts(xlabel='Age', ylabel='Count')
histogram_age.opts(width=500, height=300)

# Create pie chart of gender distribution m vs f
genders = get_subject_data()['gender'].value_counts()
fig = px.pie(df, values=genders.values, names=genders.index)

## Card for basic project information
project_card = pn.Card(
    pn.pane.Markdown(f"**Project ID:** {project_id}"),
    pn.pane.Markdown(f"**Subject Count:** {len(project.subjects)}"),
    pn.pane.Markdown(f"**Experiment Count:** {len(project.experiments)}"),
    title='Project Information',
    collapsible=False,
    sizing_mode="stretch_width",
)

# Create template/layout
template = pn.template.BootstrapTemplate(
    title=f"XNAT Panel App for Project {project_id}",
    busy_indicator=pn.indicators.BooleanStatus(value=False)
)

# Add content
template.main.append(
    pn.Column(
        pn.pane.Markdown(f"### Subject Data"),
        df_pane,
        pn.Row(
            pn.Column(
                pn.pane.Markdown(f"### Subject Age Distribution"),
                histogram_age
            ),
            pn.Column(
                pn.pane.Markdown(f"### Gender Distribution"),
                fig
            )
        )
    )
)

# Add sidebar
template.sidebar.append(
    project_card
)

template.servable()
template