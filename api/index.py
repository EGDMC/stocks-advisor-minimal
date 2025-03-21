from flask import Flask, Response

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handler():
    html_content = """
    <html>
        <head>
            <title>Stock Advisor</title>
        </head>
        <body>
            <h1>Stock Advisor App</h1>
            <p>This is a placeholder page. The full application functionality will be added soon.</p>
            <div style="padding: 1rem; background-color: #e3f2fd; border-radius: 4px;">
                The application is being configured. Please check back later.
            </div>
        </body>
    </html>
    """
    return Response(html_content, mimetype='text/html')