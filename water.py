from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from datetime import datetime

def genDateString():
    now = datetime.now()
    dateString = now.strftime("%b-%d-%Y %H:%M:%S")
    return dateString

class DrinkWater(Model):
    """  Create Table  """
    class Meta:
        table_name = "drink-water"
        region = 'us-east-1'

    username = UnicodeAttribute(hash_key=True, default='Elliott')
    dayString = UnicodeAttribute(range_key=True, default=genDateString)
    ounces = NumberAttribute(default=0)

if not DrinkWater.exists():
        DrinkWater.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

def drink(oz):
    h20 = DrinkWater(ounces=oz)
    h20.save()

def getDrinks():
    pour = DrinkWater.query('Elliott')
    drinks = {x.dayString:x.ounces for x in pour}
    return drinks

#x-axis
def extract_keys():
    vals = getDrinks()
    keys = [key for key in vals.keys()]
    return keys

#y-axis
def extract_values():
    vals = getDrinks()
    values = [val for val in vals.values()]
    return values

#proof of concept - created a tool for myself - a mini web app using Flask, Pynamodb, & Bokeh to chart and visualize the amount of water I drink.
#Elliott Arnold - si3mshady  6-12-19



