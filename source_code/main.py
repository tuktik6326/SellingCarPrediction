# Import packages
from dash import Dash, html, callback, Output, Input, State, dcc
import math
import numpy as np
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import pickle

# Import csv file
df = pd.read_csv("/root/code/Cars.csv")

# Split mileage, max_power into value and number
df[["mileage_value","mileage_unit"]] = df["mileage"].str.split(pat=' ', expand = True)
df[["max_power_value","max_power_unit"]] = df["max_power"].str.split(pat=' ', expand = True)
df.drop(["mileage","max_power"], axis=1, inplace=True)

# Filter dataframe not to include LPG and CNG in fuel column
df = df.loc[(df["fuel"] != 'LPG') & (df["fuel"] != 'CNG')]

# convert mileage, max_power from string to float64
df[["mileage" ,"max_power"]] = df[["mileage_value","max_power_value"]].astype('float64')
df.drop(["mileage_value","max_power_value",
        "mileage_unit","max_power_unit"], axis=1, inplace = True)

# Dicard dataframe containing test drive car in owner column
df = df[df["owner"] != 'Test Drive Car']

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.JOURNAL]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Create app layout
app.layout = html.Div([
        html.H1("Selling car price prediction"),
        html.Br(),
        html.H6("We provide this website for you can estimate selling car price by entering numbers of each texbox. There are three features,maximum power, mileage and kilometers driven. "),
        html.H6(" And then click submit to get result."),
        html.Br(),
        html.H4("Definition"),
        html.Br(),
        html.H6("Maximum power: Maximum power of a car "),
        html.H6("Kms driving: Total distance driven in a car by previous owner"),
        html.H6("Mileage: The fuel efficieny of a car or ratio of distance which a car could move per unit of fuel consumption measuring "),
        html.Br(),
        html.Div(["Maximum power",dbc.Input(id = "max_power", type = 'number', min = 0, placeholder="Enter bhp by number"),
        dbc.FormText("Please do not enter nagative numbers.",color="secondary"), html.Br()]),
        html.Div(["Kms driving", dbc.Input(id = "km_driven", type = 'number', min = 0, placeholder="Enter km by number"),
        dbc.FormText("Please do not enter nagative numbers.",color="secondary"), html.Br()]),
        html.Div(["Mileage", dbc.Input(id = "mileage", min = 0, type = 'number', placeholder ="Enter km/l by number"),
        dbc.FormText("Please do not enter nagative numbers.",color="secondary"), html.Br()]),
        dbc.Button(id="submit", children="submit", color="success", className="me-1"),
        html.Div(id="output", children = '')
])

# Callback input and output
@callback(
    Output(component_id = "output", component_property = "children"),
    State(component_id = "max_power", component_property = "value"),
    State(component_id = "km_driven", component_property = "value"),
    State(component_id = "mileage", component_property = "value"),
    Input(component_id = "submit", component_property = "n_clicks"),
    prevent_initial_call=True
)

# Function for finding estimated car price
def prediction (max_power, mileage, km_driven, submit):
    if max_power == None:
        max_power = df["max_power"].median() # Fill in maximum power if dosen't been inserted
    if km_driven == None:
        km_driven = df["km_driven"].median() # Fill in kilometers driven if doesn't been inserted
    if mileage == None:
        mileage = df["mileage"].mean() # Fill in mileage if dosen't been inserted
    model = pickle.load(open("/root/code/car_prediction.model", 'rb')) # Import model
    sample = np.array([[max_power, mileage, math.log(km_driven)]]) 
    result = np.exp(model.predict(sample)) #Predict price
    return f"The predicted selling car price is {int(result[0])}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8050', debug=True)