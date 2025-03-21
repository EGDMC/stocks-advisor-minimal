from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from flask import Flask

server = Flask(__name__)
app = Dash(
    __name__,
    server=server,
    url_base_pathname='/',
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Stock Market Analysis", className="text-center mb-4"),
            dbc.Card([
                dbc.CardBody([
                    html.H3("Upload Data", className="card-title"),
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files')
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        }
                    )
                ])
            ], className="mb-4")
        ])
    ])
], fluid=True, className="p-5")

def handler(request):
    return app.index()