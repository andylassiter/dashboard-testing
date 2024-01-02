from dash import Dash, html
import os

port = 8050

jupyterhub_base_url = os.getenv('JUPYTERHUB_SERVICE_PREFIX')
jupyterhub_base_url = f"{jupyterhub_base_url}proxy/{port}/"

app = Dash(
    __name__,
    requests_pathname_prefix=jupyterhub_base_url,
)

app.layout = html.Div('Hello World, from Dash')

if __name__ == "__main__":
    app.run(host='0.0.0.0')