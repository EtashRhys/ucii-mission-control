from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="UCII Mission Control Console",
    description="Private operator console for UCII Mission Control",
    version="0.1.0",
)


app.mount(
    "/static",
    StaticFiles(
        directory=BASE_DIR / "static"
    ),
    name="static",
)


templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


def render_console(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="base.html",
        context={
            "status": "online",
        },
    )


@app.get(
    "/",
    response_class=HTMLResponse,
)
def console_home(
    request: Request,
):
    return render_console(request)


@app.get(
    "/console",
    response_class=HTMLResponse,
)
def console_route(
    request: Request,
):
    return render_console(request)


@app.get("/health")
def health():

    return {
        "service": "UCII Mission Control Console",
        "status": "healthy",
    }
