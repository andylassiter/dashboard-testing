import dash_bootstrap_components as dbc
import os
import xnat
from dash import Dash, html, dcc, Output, Input

# Dash setup
user = os.getenv('JUPYTERHUB_USER')
jupyterhub_base_url = os.getenv('JUPYTERHUB_SERVICE_PREFIX', f"/jupyterhub/user/{user}/")

app = Dash(
    __name__,
    requests_pathname_prefix=f"{jupyterhub_base_url}/",
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# XNAT setup
project_id = os.environ['XNAT_ITEM_ID']

connection = xnat.connect()
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
        html.H2("XNAT Dash App", className="display-4"),
        html.Hr(),
        html.P(f"Project: {project_id}", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Project Overview", href=jupyterhub_base_url, active="exact"),
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
        html.P(f"Project: {project_id}", className="lead"),
        html.P(f"Subjects: {project.subjects.count()}", className="lead"),
        html.P(f"Experiments: {project.experiments.count()}", className="lead"),
    ])

if __name__ == "__main__":
    app.run_server(port=8050, host='0.0.0.0')