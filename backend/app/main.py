from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from backend.app.api.v1.documents import router as documents_router
from backend.app.db.session import engine
from backend.app.models.document import Base

import os

# Создание таблиц SQLite
Base.metadata.create_all(bind=engine)

app = FastAPI()

# BASE PATHS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# DEBUG
print("TEMPLATES DIR:", TEMPLATES_DIR)
print("INDEX EXISTS:", os.path.exists(os.path.join(TEMPLATES_DIR, "index.html")))

# JINJA
templates = Jinja2Templates(directory=TEMPLATES_DIR)

templates.env.auto_reload = True
templates.env.enable_async = False

# STATIC
app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)

# ROUTES
app.include_router(documents_router)

# HOME PAGE
@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "debug": "test"
        }
    )