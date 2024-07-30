from jinja2 import Environment, select_autoescape, FileSystemLoader


def get_template(name):
    templateLoader = FileSystemLoader(searchpath="./ui/print/")
    env = Environment(
        loader=templateLoader,
        autoescape=select_autoescape()
    )
    return env.get_template(name)
