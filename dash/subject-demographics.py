import logging
import os
import xnat

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from dash import Dash, dash_table, dcc, html

# For local testing
# os.environ['JUPYTERHUB_USER'] = 'admin'
# os.environ['JUPYTERHUB_SERVICE_PREFIX'] = '/'
# os.environ['XNAT_HOST'] = 'http://localhost'
# os.environ['XNAT_USER'] = 'admin'
# os.environ['XNAT_PASS'] = 'admin'
# os.environ['XNAT_ITEM_ID'] = 'C4KC-KiTS'

# Logging to a file
logging.basicConfig(
    filename='dash.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)

# Dash setup
user = os.getenv('JUPYTERHUB_USER')
jupyterhub_base_url = os.getenv('JUPYTERHUB_SERVICE_PREFIX', f"/jupyterhub/user/{user}/")

app = Dash(
    __name__,
    requests_pathname_prefix=jupyterhub_base_url,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

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

df = get_subject_data()

def subject_age_distribution():
    ages = get_subject_data()['age']

    fig = px.histogram(ages, nbins=20)
    fig.update_layout(
        title_text='Subject Ages',
        xaxis_title_text='Age',
        yaxis_title_text='Count',
        bargap=0.2,
        bargroupgap=0.1
    )

    return fig

def subject_gender_distribution():
    genders = get_subject_data()['gender'].value_counts()

    fig = px.pie(genders, values=genders.values, names=genders.index)
    fig.update_layout(
        title_text='Subject Genders',
        showlegend=True
    )

    return fig

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H1(children=f"Dash App for {project.id}", style={'textAlign':'center'}),
            html.H2(children=f"Subject Demographics for {project.id}"),
            # dash_table.DataTable(data=df.to_dict('records'), page_size=10),
            # dbc.Row([
            #     dbc.Col([
            #         dcc.Graph(id='subject-age-distribution', figure=subject_age_distribution())
            #     ], width=6),
            #     dbc.Col([
            #         dcc.Graph(id='subject-gender-distribution', figure=subject_gender_distribution())
            #     ], width=6),
            # ])
        ], width=8)
    ], justify="center")
])

if __name__ == "__main__":
    logging.info(f"Starting Dash app {__name__}")
    app.run_server(port=8050, host='0.0.0.0', debug=True)