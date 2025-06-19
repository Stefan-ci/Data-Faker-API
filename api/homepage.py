from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def homepage_view():
    return """
    <html>
        <head>
            <title>Fake Data API</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 2rem; }
                h1 { color: #2c3e50; }
                a { color: #3498db; text-decoration: none; }
                code { background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px; }
                ul { margin-top: 1rem; }
            </style>
        </head>
        <body>
            <h1>🧪 Fake Data API</h1>
            <p>This API provides dynamically generated fake data for development and testing purposes.</p>
            
            <h2>Locale Support</h2>
            <p>You can use the <code>?locale=fr_FR</code> query parameter to switch data language and format.</p>
            
            <h2>Documentation</h2>
            <p>Interactive API docs are available at:</p>
            <ul>
                <li><a href="/docs">Swagger UI</a></li>
                <li><a href="/redoc">ReDoc</a></li>
            </ul>
        </body>
    </html>
    """
