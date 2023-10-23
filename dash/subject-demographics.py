from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
import os
import xnat
import pandas as pd
import plotly.express as px

# Logging to stdout
import logging

logging.basicConfig(level=logging.DEBUG)

# Dash setup
user = os.getenv('JUPYTERHUB_USER')
jupyterhub_base_url = os.getenv('JUPYTERHUB_SERVICE_PREFIX', f"/jupyterhub/user/{user}/")

logging.debug(f"JupyterHub base URL: {jupyterhub_base_url}")
logging.debug(f"Starting Dash app")

app = Dash(
    __name__,
    requests_pathname_prefix=f"{jupyterhub_base_url}/",
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

logging.debug(f"Dash app created")

# XNAT setup
xnat_host = os.getenv('XNAT_HOST')
xnat_user = os.getenv('XNAT_USER')
xnat_password = os.getenv('XNAT_PASS')

project_id = os.getenv('XNAT_ITEM_ID')

logging.debug(f"XNAT host: {xnat_host}")
logging.debug(f"XNAT user: {xnat_user}")
logging.debug(f"XNAT password: {xnat_password}")
logging.debug(f"XNAT project ID: {project_id}")

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
        html.P(f"Project: {project_id}", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Project Overview", href=jupyterhub_base_url, active="exact"),
                dbc.NavLink("Subject Overview", href=f"{jupyterhub_base_url}subject-overview", active="exact"),
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
    elif pathname == "/subject-overview":
        return render_iris()
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
        html.P(f"Project: {project_id}", className="lead"),
        html.P(f"Subjects: {len(project.subjects)}", className="lead"),
        html.P(f"Experiments: {len(project.experiments)}", className="lead"),
    ])

def render_iris():
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length")
    
    return html.Div([
        html.P("Iris Data", className="lead"),
        dcc.Graph(id='iris-graph', figure=fig),
    ])


# def render_subjects():
#     return html.Div([
#         html.P("Subject Overview", className="lead"),
#         dcc.Graph(id='subject-age-distribution', figure=subject_age_distribution()),
#     ])

# # Cache for subject data
# subject_data_cache = None

# # Compile subject data or return cached data
# def get_subject_data():
#     global subject_data_cache
    
#     if subject_data_cache is not None:
#         return subject_data_cache
    
#     subject_data = {
#         'id': [],
#         'gender': [],
#         'age': []
#     }

#     for subject in project.subjects.values():
#         subject_data['id'].append(subject.label)
#         subject_data['gender'].append(subject.demographics.gender)
#         subject_data['age'].append(subject.demographics.age)
        
#     df = pd.DataFrame(subject_data)
    
#     subject_data_cache = df

#     return df

# def subject_age_distribution():
#     ages = get_subject_data()['age']

#     fig = px.histogram(ages, nbins=20)
#     fig.update_layout(
#         title_text='Age Distribution',
#         xaxis_title_text='Age',
#         yaxis_title_text='Count',
#         bargap=0.2,
#         bargroupgap=0.1
#     )

#     return fig

if __name__ == "__main__":
    app.run_server(port=8050, host='0.0.0.0', debug=True)