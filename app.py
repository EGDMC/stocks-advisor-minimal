import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
from api.smc_analyzer import analyze_smc
import io
import base64

# Try to import dash_bootstrap_components, use fallback if not available
try:
    import dash_bootstrap_components as dbc
    has_dbc = True
except ImportError:
    has_dbc = False
    print("Warning: dash_bootstrap_components not found, using basic styling")

def create_app():
    # Use dbc theme if available, otherwise use basic theme
    if has_dbc:
        app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    else:
        app = dash.Dash(__name__)
    
    # Basic styling for non-DBC version
    basic_styles = {
        'container': {
            'max-width': '1200px',
            'margin': '0 auto',
            'padding': '20px'
        },
        'upload': {
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '20px 0',
            'backgroundColor': '#fafafa'
        },
        'header': {
            'textAlign': 'center',
            'padding': '20px 0',
            'margin-bottom': '20px',
            'backgroundColor': '#f8f9fa',
            'borderRadius': '5px'
        }
    }
    
    app.layout = html.Div(
        style=basic_styles['container'],
        children=[
            html.Div(
                style=basic_styles['header'],
                children=[
                    html.H1('Stock Market Analysis'),
                    html.P('Upload your stock data to begin analysis')
                ]
            ),
            
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style=basic_styles['upload'],
                multiple=False
            ),
            
            html.Div(id='output-container', children=[])
        ]
    )
    
    @app.callback(
        dash.dependencies.Output('output-container', 'children'),
        dash.dependencies.Input('upload-data', 'contents'),
        dash.dependencies.State('upload-data', 'filename')
    )
    def update_output(contents, filename):
        if contents is None:
            return 'Upload a CSV file to begin analysis'
        
        try:
            # Parse CSV content
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            
            # Perform analysis
            closes = df['Close'].values if 'Close' in df else df['close'].values
            volumes = df['Volume'].values if 'Volume' in df else df['volume'].values
            
            smc_results = analyze_smc(closes, volumes)
            
            # Create chart
            fig = go.Figure(data=[
                go.Candlestick(
                    open=df['Open' if 'Open' in df else 'open'],
                    high=df['High' if 'High' in df else 'high'],
                    low=df['Low' if 'Low' in df else 'low'],
                    close=df['Close' if 'Close' in df else 'close']
                )
            ])
            
            # Add SMC levels
            for level in smc_results.get('liquidity_levels', []):
                fig.add_hline(
                    y=level['price'],
                    line_dash="dash",
                    line_color="blue" if level['type'] == 'support' else "red",
                    annotation_text=f"{level['type'].title()} ({level['strength']}x)"
                )
            
            fig.update_layout(
                title='Price Chart with SMC Levels',
                yaxis_title='Price',
                xaxis_title='Time',
                template='plotly_white'
            )
            
            # Create results display
            results_style = {
                'padding': '20px',
                'backgroundColor': '#ffffff',
                'borderRadius': '5px',
                'boxShadow': '0 1px 3px rgba(0,0,0,0.12)',
                'margin-top': '20px'
            }
            
            return [
                dcc.Graph(figure=fig),
                html.Div(
                    style=results_style,
                    children=[
                        html.H3('Analysis Results'),
                        html.Div([
                            html.H4('Liquidity Levels'),
                            html.Ul([
                                html.Li(
                                    f"{level['type'].title()}: ${level['price']} (Strength: {level['strength']}x)",
                                    style={'color': 'blue' if level['type'] == 'support' else 'red'}
                                )
                                for level in smc_results.get('liquidity_levels', [])
                            ])
                        ])
                    ]
                )
            ]
            
        except Exception as e:
            return html.Div(
                f'Error processing file: {str(e)}',
                style={'color': 'red', 'padding': '20px'}
            )
    
    return app

app = create_app()
server = app.server  # For Vercel deployment

if __name__ == '__main__':
    app.run_server(debug=True)