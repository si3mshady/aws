from water import extract_keys,extract_values
from bokeh.io import show, output_file
from bokeh.plotting import figure


def processData():
    output_file("templates/bars.html")

    keys = extract_keys()
    values = extract_values()

    p = figure(x_range=keys, plot_height=250, title="Water Consumption",
               toolbar_location=None, tools="")

    p.vbar(x=keys, top=values, width=0.9)

    p.xgrid.grid_line_color = None
    p.xaxis.major_label_orientation = 1
    p.y_range.start = 0

    show(p)


#proof of concept - created a tool for myself - a mini web app using Flask, Pynamodb, & Bokeh to chart and visualize the amount of water I drink.
#Elliott Arnold - si3mshady  6-12-19