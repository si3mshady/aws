from flask import Flask, render_template, request
from water_chart import processData
from water import drink

app=application=Flask(__name__)

@app.route('/water')
def start():
    return render_template('index.html')

@app.route('/water', methods=['POST'])
def send_oz_to_DynamoDB():
    ounces = request.form.get('oz')
    drink(int(ounces))
    processData()
    return render_template('bars.html')

if __name__ == "__main__":
    app.run(debug=True)


#proof of concept - created a tool for myself - a mini web app using Flask, Pynamodb, & Bokeh to chart and visualize the amount of water I drink.
#Elliott Arnold - si3mshady  6-12-19