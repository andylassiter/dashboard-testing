from dash import Dash, html, dcc, Output, Input, dash_table
import dash_bootstrap_components as dbc
import os
import xnat
import pandas as pd
import plotly.express as px

# Logging to a file
import logging

logging.basicConfig(
    filename='dash.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)

# # For local testing
# os.environ['JUPYTERHUB_USER'] = 'admin'
# os.environ['JUPYTERHUB_SERVICE_PREFIX'] = '/'
# os.environ['XNAT_HOST'] = 'http://localhost'
# os.environ['XNAT_USER'] = 'admin'
# os.environ['XNAT_PASS'] = 'admin'
# os.environ['XNAT_ITEM_ID'] = 'C4KC-KiTS'

# Dash setup
user = os.getenv('JUPYTERHUB_USER')
jupyterhub_base_url = os.getenv('JUPYTERHUB_SERVICE_PREFIX', f"/jupyterhub/user/{user}/")

logging.info(f"JupyterHub base URL: {jupyterhub_base_url}")
logging.info(f"Creating Dash app")

app = Dash(
    __name__,
    requests_pathname_prefix=f"{jupyterhub_base_url}",
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

logging.info(f"Dash app created")

# XNAT setup
xnat_host = os.getenv('XNAT_HOST')
xnat_user = os.getenv('XNAT_USER')
xnat_password = os.getenv('XNAT_PASS')

project_id = os.getenv('XNAT_ITEM_ID')

logging.info(f"XNAT host: {xnat_host}")
logging.info(f"XNAT user: {xnat_user}")
logging.info(f"XNAT password: {xnat_password}")
logging.info(f"XNAT project ID: {project_id}")

connection = xnat.connect(xnat_host, user=xnat_user, password=xnat_password)
project = connection.projects[project_id]

logging.info(f"Connected to XNAT")

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

logging.info(f"Creating sidebar")

sidebar = html.Div(
    [
        html.H3("XNAT Dash App", className="display-7"),
        html.Hr(),
        html.P(f"Project: {project_id}"),
        html.P(f"Subjects: {len(project.subjects)}"),
        html.P(f"Experiments: {len(project.experiments)}"),
        dbc.Nav(
            [
                dbc.NavLink("Project Overview", href=jupyterhub_base_url, active="exact"),
                dbc.NavLink("Subject Overview", href=f"{jupyterhub_base_url}page-1", active="exact"),
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

logging.info(f"Sidebar created")

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    logging.info(f"Rendering page content for pathname: {pathname}")

    # remove jupyterhub_base_url from pathname
    pathname = pathname.replace(jupyterhub_base_url, '/')

    if pathname == "/":
        return html.P("This is the content of page 1. Yay!")
        # return render_home()
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

# logging.info(f"Page content callback function created")

# def render_home():
#     logging.info(f"Rendering home page")
#     return html.Div(
#         [
#             dbc.Col([
#                 dbc.Row([
#                     dbc.Col([
#                         dash_table.DataTable(data=get_subject_data().to_dict('records'), page_size=10, style_table={'overflowX': 'auto'})
#                     ])
#                 ]),
#                 dbc.Row([
#                     dbc.Col([
#                         dcc.Graph(id='subject-age-distribution', figure=subject_age_distribution())
#                     ], width=6),
#                     dbc.Col([
#                         dcc.Graph(id='subject-gender-distribution', figure=subject_gender_distribution())
#                     ], width=6),
#                 ]),
#             ])
#         ]
#     ) 

# logging.info(f"Render home function created")

# def render_iris():
#     logging.info(f"Rendering iris page")
#     df = px.data.iris()
#     fig = px.scatter(df, x="sepal_width", y="sepal_length")
    
#     return dbc.Container([
#         dbc.Col([
#             dcc.Graph(figure=fig, id='my-first-graph-final')
#         ], width=6),
#     ], fluid=True)

# logging.info(f"Render iris function created")

# def render_subjects():
#     logging.info(f"Rendering subjects graph")
#     return html.Div([
#         html.P("Subject Overview", className="lead"),
#         dcc.Graph(id='subject-age-distribution', figure=subject_age_distribution()),
#     ])

# logging.info(f"Render subjects function created")

# # Cache for subject data
# subject_data_cache = None

# logging.info(f"Subject data cache created")

# # Compile subject data or return cached data
# def get_subject_data():
#     logging.info(f"Getting subject data")

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

# logging.info(f"Get subject data function created")

# def subject_age_distribution():
#     logging.info(f"Rendering subject age distribution")

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

# logging.info(f"Subject age distribution function created")

# def subject_gender_distribution():
#     logging.info("Rendering subject gender pie chart")

#     genders = get_subject_data()['gender'].value_counts()

#     fig = px.pie(genders, values=genders.values, names=genders.index)
#     fig.update_layout(
#         title_text='Gender Distribution',
#         showlegend=True
#     )

#     return fig

# logging.info("Subject gender distribution function created")

if __name__ == "__main__":
    logging.info(f"Starting Dash app {__name__}")
    app.run_server(port=8050, host='0.0.0.0', debug=True)