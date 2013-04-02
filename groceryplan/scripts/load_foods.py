import os
from os.path import abspath, dirname
import sys
import csv
from django.template.defaultfilters import slugify

# Set up django path to run in the VM
project_dir = abspath(dirname(dirname(__file__)))
sys.path.insert(0, project_dir)
os.environ["DJANGO_SETTINGS_MODULE"] = "groceryplan.settings"

from prices.models import Food

f1 = csv.reader(open('scripts/foods.csv', 'rU'))
for row in f1:
    food_name = row[0]
    food_category = row[1]
    c = Food(name=food_name, section=food_category, slug=slugify(food_name))
    c.save()
