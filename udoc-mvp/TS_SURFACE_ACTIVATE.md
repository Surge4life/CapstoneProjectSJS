# TS surface activation

`platform-core/static/ts.html` is on main.

Add to `platform-core/app/main.py` immediately after `divisions_console`:

```python
@app.get("/ts", tags=["root"], include_in_schema=False)
@app.get("/ts/", tags=["root"], include_in_schema=False)
def ts_console():
    """TS Industries division operator — SPV deploy + SETHS worker absorb."""
    return FileResponse(_static("ts.html"))
```

Then `/ts` is live on gods-platform-core.
