from jinja2 import Environment, PackageLoader, select_autoescape
import json
from copy import deepcopy

env = Environment(
    loader=PackageLoader("main"),
    autoescape=select_autoescape()
)

def get_days_of_class(clas : dict):
    days = set()
    for period in clas["periods"]:
        days.add(period["weekday"])
    return list(days)

def get_periods_on_day(periods : list, day : int):
    filtered = filter(lambda p : p["weekday"] == day, periods)
    return list(filtered)

def convert_weekday(number : int):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return weekdays[number - 1]

def convert_weekdays(data : dict):
    edited = deepcopy(data)
    for clas in edited["classes"]:
        for period in clas["periods"]:
            weekday_str = convert_weekday(period["weekday"])
            period["weekday_name"] = weekday_str
    return edited

def group_by_day(data : dict):
    edited = deepcopy(data)

    for clas in edited["classes"]:
        clas["days"] = []
        days = get_days_of_class(clas)
        for day in days:
            # get periods on that day
            day_periods = get_periods_on_day(clas["periods"], day)
            # push into the correct day
            clas["days"].append({"weekday": day, "weekday_name": convert_weekday(day), "periods": day_periods})
    return edited

template = env.get_template("template-by-class-grouped.html")

with open("./data/week_5.json", "r") as f:
    data = json.load(f)

data = convert_weekdays(data)

grouped = group_by_day(data)

with open('./renders/grouped.json', "w") as f:
    json.dump(grouped,f, indent=4)

output = template.render(grouped)

with open("./renders/example.html", "w") as f:
    f.writelines(output)

print("Wrote out file successfully.")