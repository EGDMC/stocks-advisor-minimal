from flask import Flask
from dash import Dash
import dash_bootstrap_components as dbc
from dash import html

server = Flask(__name__)

app = Dash(
    __name__,
    server=server,
    url_base_pathname='/',
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = dbc.Container([
    html.H1("Stock Advisor App", className="my-4"),
    html.P("This is a placeholder page. The full application functionality will be added soon."),
    dbc.Alert(
        "The application is being configured. Please check back later.",
        color="info"
    )
], className="p-5")

if __name__ == '__main__':
    app.run_server(debug=False)