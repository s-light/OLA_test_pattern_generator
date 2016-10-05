"""This file only exists to make this directory a valid python package."""
# more info at
# http://stackoverflow.com/a/32067984/574981
# raise an exception
# just to confirm that the .so file is loaded instead of the .py file
raise ImportError(
    "__init__.py loaded when __init__.so should have been loaded"
)
