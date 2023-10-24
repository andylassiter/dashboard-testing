"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location, and a callback uses the
current location to render the appropriate page content. The active prop of
each NavLink is set automatically according to the current pathname. To use
this feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
import dash_bootstrap_components as dbc
import os
import xnat
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input, dash_table

user = os.getenv('JUPYTERHUB_USER')
jupyterhub_base_url = os.getenv('JUPYTERHUB_SERVICE_PREFIX', f"/jupyterhub/user/{user}/")

app = Dash(
    __name__,
    requests_pathname_prefix=f"{jupyterhub_base_url}/",
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# XNAT setup
xnat_host = os.getenv('XNAT_HOST')
xnat_user = os.getenv('XNAT_USER')
xnat_password = os.getenv('XNAT_PASS')

project_id = os.getenv('XNAT_ITEM_ID')

connection = xnat.connect(xnat_host, user=xnat_user, password=xnat_password)
project = connection.projects[project_id]

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H3("XNAT Dash App", className="display-7"),
        html.Hr(),
        html.P(f"Project: {project_id}"),
        html.P(f"Subjects: {len(project.subjects)}"),
        html.P(f"Experiments: {len(project.experiments)}"),
        dbc.Nav(
            [
                dbc.NavLink("Home", href=jupyterhub_base_url, active="exact"),
                dbc.NavLink("Page 1", href=f"{jupyterhub_base_url}page-1", active="exact"),
                dbc.NavLink("Page 2", href=f"{jupyterhub_base_url}page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    # remove jupyterhub_base_url from pathname
    pathname = pathname.replace(jupyterhub_base_url, '/')

    if pathname == "/":
        return render_home()
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

def render_home():
    return html.Div([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                        dash_table.DataTable(data=get_subject_data().to_dict('records'), page_size=10, style_table={'overflowX': 'auto'})
                ])
            ])
        ])
    ]) 

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

if __name__ == "__main__":
    app.run_server(port=8050, host='0.0.0.0')