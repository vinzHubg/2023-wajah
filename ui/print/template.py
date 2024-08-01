from jinja2 import Environment, select_autoescape, FileSystemLoader
from datetime import datetime

def time_diff_in_minutes(start_time, end_time, time_format="%H:%M:%S"):
    diff = start_time - end_time
    return int(diff.total_seconds() / 60)

def get_template(name):
    templateLoader = FileSystemLoader(searchpath="./ui/print/")
    env = Environment(
        loader=templateLoader,
        autoescape=select_autoescape()
    )

    env.filters['time_diff_in_minutes'] = time_diff_in_minutes

    return env.get_template(name)
