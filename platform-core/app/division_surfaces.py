"""Division operator HTML surfaces — TS / MADIBA / SETHS."""
from fastapi.responses import FileResponse


def register_division_surfaces(app, static_fn):
    """Wire GET /ts /madiba /seths FileResponse routes onto the FastAPI app."""

    @app.get("/ts", tags=["root"], include_in_schema=False)
    @app.get("/ts/", tags=["root"], include_in_schema=False)
    def ts_console():
        """TS Industries division operator — SPV deploy + SETHS worker absorb."""
        return FileResponse(static_fn("ts.html"))

    @app.get("/madiba", tags=["root"], include_in_schema=False)
    @app.get("/madiba/", tags=["root"], include_in_schema=False)
    def madiba_console():
        """MADIBA / EIF recognition operator."""
        return FileResponse(static_fn("madiba.html"))

    @app.get("/seths", tags=["root"], include_in_schema=False)
    @app.get("/seths/", tags=["root"], include_in_schema=False)
    def seths_console():
        """SETHS human capability operator — enrol / advance / place."""
        return FileResponse(static_fn("seths.html"))
