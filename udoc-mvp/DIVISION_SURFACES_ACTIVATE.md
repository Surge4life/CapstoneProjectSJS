# Division surfaces activation

## Already on main (static)
- `platform-core/static/ts.html`
- `platform-core/static/madiba.html`

## main.py routes (paste after divisions_console)

```python
@app.get("/ts", tags=["root"], include_in_schema=False)
@app.get("/ts/", tags=["root"], include_in_schema=False)
def ts_console():
    """TS Industries division operator — SPV deploy + SETHS worker absorb."""
    return FileResponse(_static("ts.html"))


@app.get("/madiba", tags=["root"], include_in_schema=False)
@app.get("/madiba/", tags=["root"], include_in_schema=False)
def madiba_console():
    """MADIBA / EIF division operator — recognition cycles + honest capital status."""
    return FileResponse(_static("madiba.html"))
```

Full file: artifacts/main_WITH_TS_ROUTE.py
