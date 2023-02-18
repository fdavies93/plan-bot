from jinja2 import Environment, PackageLoader, select_autoescape
import json

env = Environment(
    loader=PackageLoader("yourapp"),
    autoescape=select_autoescape()
)

