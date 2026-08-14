"""Division operator HTML surfaces — TS / MADIBA / SETHS."""
from fastapi.responses import FileResponse, HTMLResponse


def _html_with_density(path: str):
    """Serve HTML and inject shared div-density.js (assessor + EVA + cross-nav)."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
    except Exception:
        return FileResponse(path)
    tag = '<script src="/div-density.js" defer></script>'
    if "div-density.js" not in html:
        html = html.replace("</body>", tag + "\n</body>") if "</body>" in html else html + tag
    return HTMLResponse(html, media_type="text/html")


def register_division_surfaces(app, static_fn):
    """Wire GET /ts /madiba /seths routes with density inject."""

    @app.get("/ts", tags=["root"], include_in_schema=False)
    @app.get("/ts/", tags=["root"], include_in_schema=False)
    def ts_console():
        """TS Industries division operator — SPV deploy + SETHS worker absorb."""
        return _html_with_density(static_fn("ts.html"))

    @app.get("/madiba", tags=["root"], include_in_schema=False)
    @app.get("/madiba/", tags=["root"], include_in_schema=False)
    def madiba_console():
        """MADIBA / EIF recognition operator."""
        return _html_with_density(static_fn("madiba.html"))

    @app.get("/seths", tags=["root"], include_in_schema=False)
    @app.get("/seths/", tags=["root"], include_in_schema=False)
    def seths_console():
        """SETHS human capability operator — enrol / advance / place."""
        return _html_with_density(static_fn("seths.html"))
