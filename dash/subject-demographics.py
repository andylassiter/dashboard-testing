# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import os
import logging
import xnat

# Logging to a file
logging.basicConfig(
    filename='dash.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)

# XNAT setup
xnat_host = os.getenv('XNAT_HOST')
xnat_user = os.getenv('XNAT_USER')
xnat_password = os.getenv('XNAT_PASS')

project_id = os.getenv('XNAT_ITEM_ID')

connection = xnat.connect(xnat_host, user=xnat_user, password=xnat_password)
project = connection.projects[project_id]

logging.info(f"Connected to XNAT project {project_id}")

# Incorporate data
# Compile subject data or return cached data
def get_subject_data():
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

    return df

df = get_subject_data()

# Dash setup
user = os.getenv('JUPYTERHUB_USER')
jupyterhub_base_url = os.getenv('JUPYTERHUB_SERVICE_PREFIX', f"/jupyterhub/user/{user}/")

logging.info(f"Creating Dash app named {__name__} with base URL {jupyterhub_base_url}/")

app = Dash(
    __name__,
    requests_pathname_prefix=f"{jupyterhub_base_url}/",
    external_stylesheets=[dbc.themes.CERULEAN]
)

logging.info(f"Created Dash app named {__name__} with base URL {jupyterhub_base_url}/")

# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div(f"My First App with Data, Graph, and Controls for {project_id}", className="text-primary text-center fs-3")
    ]),

    dbc.Row([
        dbc.RadioItems(options=[{"label": x, "value": x} for x in ['pop', 'lifeExp', 'gdpPercap']],
                       value='lifeExp',
                       inline=True,
                       id='radio-buttons-final')
    ]),

    dbc.Row([
        dbc.Col([
            dash_table.DataTable(data=df.to_dict('records'), page_size=12, style_table={'overflowX': 'auto'})
        ], width=6),

        dbc.Col([
            dcc.Graph(figure={}, id='my-first-graph-final')
        ], width=6),
    ]),

], fluid=True)



# Run the app
if __name__ == "__main__":
    app.run_server(port=8050, host='0.0.0.0', debug=True)
