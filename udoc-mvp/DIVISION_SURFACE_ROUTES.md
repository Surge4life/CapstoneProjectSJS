# Division operator routes

Static consoles on main:

| Path | File |
|------|------|
| `/ts` | `platform-core/static/ts.html` |
| `/madiba` | `platform-core/static/madiba.html` |
| `/seths` | `platform-core/static/seths.html` |

Add to `platform-core/app/main.py` after `divisions_console`:

```python
@app.get("/ts", tags=["root"], include_in_schema=False)
@app.get("/ts/", tags=["root"], include_in_schema=False)
def ts_console():
    return FileResponse(_static("ts.html"))

@app.get("/madiba", tags=["root"], include_in_schema=False)
@app.get("/madiba/", tags=["root"], include_in_schema=False)
def madiba_console():
    return FileResponse(_static("madiba.html"))

@app.get("/seths", tags=["root"], include_in_schema=False)
@app.get("/seths/", tags=["root"], include_in_schema=False)
def seths_console():
    return FileResponse(_static("seths.html"))
```

Full patched main: `artifacts/main_WITH_DIVISION_ROUTES.py`
