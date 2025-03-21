import dash
from dash import html
import dash_bootstrap_components as dbc

# Initialize the app with the __name__ variable
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# For Vercel deployment, we need to reference the server variable
server = app.server

# Create the layout
app.layout = dbc.Container([
    html.H1("Stock Advisor App", className="my-4"),
    html.P("This is a placeholder page. The full application functionality will be added soon."),
    dbc.Alert(
        "The application is being configured. Please check back later.",
        color="info"
    )
], className="p-5")

# For local development
if __name__ == '__main__':
    app.run_server(debug=False)