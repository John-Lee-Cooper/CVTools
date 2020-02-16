def update_docstring(f, **kw):
    for key, value in kw.items():
        f.__doc__ = f.__doc__.replace(f"{{{key}}}", value)
