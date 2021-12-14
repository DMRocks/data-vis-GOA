import dash
from dash import dcc
from dash import html
from dash.dependencies import Input,Output
import pandas as pd
import plotly.express as px

#Get Data, Get Dash
url_main = 'https://raw.githubusercontent.com/DMRocks/data-vis-GOA/main/Landmine-Area/Areas%20contaminated%20by%20landmine%20(sq.km).cvs'
data = pd.read_csv(url_main, index_col= ["Table", "Unit", "Variety", "Year"])

url_average = 'https://raw.githubusercontent.com/DMRocks/Genetically-Engineered/main/GE%20Crops%20Averages%20-%20alltablesGEcrops%20(1).csv'
data_average = pd.read_csv(url_average, index_col= ["Table", "Variety", "Year"])

external_stylesheets= ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
server = app.server


#App Layout
app.layout = html.Div([
    html.H1("Adoption of Genetically Engineered Crops in the U.S.", style={'text-align':'center'}),
    html.H5("Data from the U.S. Deparment of Agriculture"),
    
    html.Div(f'Select what crops and what varity you would like to graph. *Note: The only dataset available for Soybean is Herbicide-tolerant.'),
    
    html.Div([
    dcc.RadioItems(
    id='crop',
    value= f"Genetically engineered (GE) corn varieties", options=[
        {'label': 'Corn varieties', 'value': 'Genetically engineered (GE) corn varieties'},
        {'label': 'Upland cotton varieties', 'value': 'Genetically engineered (GE) upland cotton varieties'},
        {'label': 'Soybean varieties', 'value': 'Genetically engineered (GE) soybean varieties'},
    ]), ], 
    style={'display': 'inline-block', 'width': '15%'}),
    
    html.Div([
    dcc.RadioItems(
    id='type',
    value= f"Insect-resistant (Bt) only", options=[
        {'label': 'Insect-resistant', 'value': 'Insect-resistant (Bt) only'},
        {'label': 'Herbicide-tolerant', 'value': 'Herbicide-tolerant only'},
        {'label': 'Stacked gene varieties', 'value': 'Stacked gene varieties'},
        {'label': 'All GE varieties', 'value': 'All GE varieties'},
    ]), ], 
    style={'display': 'inline-block', 'width': '15%'}),    

    dcc.Slider(
        id='year_selector',
        min=2000,
        max=2020,
        step=1,
        value=2000,
        tooltip={"placement": "bottom", "always_visible": True},
        marks={
            2000: {'label': '2000'},
            2010: {'label': '2010'},
            2020: {'label': '2020'}
    }),

    html.Div([
        dcc.Graph(id='main_map')
    ], style={'display': 'inline-block', 'width': '55%'}),
    html.Div([
        dcc.Graph(id='line_chart')
    ], style={'display': 'inline-block', 'width': '45%'}),
])

#Map
@app.callback(
    Output(component_id='main_map', component_property='figure'),
    Input("crop", "value"),
    Input("type", "value"),
    Input("year_selector", "value")
)
def run_main_map(crop, type, year):

    #Uhhhhhhhhh Probabably not the best way of doing this, but you know, if it works it works.
    if "corn" in crop:
        percent_var = "Percent of corn planted"
        crop_string = "Corn"

    if "cotton" in crop:
        percent_var = "Percent of upland cotton planted"
        crop_string = "Cotton"

    if "soybean" in crop:
        percent_var = "Percent of all soybeans planted"
        crop_string = "Soybean"

    if "Insect-resistant (Bt) only" in type:
        type_string = "Insect-resistant"
    
    if "Herbicide-tolerant only" in type:
        type_string = "Herbicide-tolerant"

    if "All GE varieties" in type:
        type_string = "Genetically Engineered"

    if "Stacked gene varieties" in type:
        type_string = "Stacked Gene"


    #Get that Data
    data_selcted = data.loc(axis=0)[crop, percent_var, type]

    #Max and Min Vaules
    data_max_min = data_selcted["Value"]
    max = data_max_min.max(axis=0)
    min = data_max_min.min(axis=0)

    #Finish with Data
    data_selcted = data_selcted.loc[year]
    data_selcted.set_index('Attribute', inplace= True)


    #Map it up
    main_map = px.choropleth(data_frame = data_selcted, locations=data_selcted.index, color = data_selcted['Value'], locationmode="USA-states", 
    scope="usa", color_continuous_scale = px.colors.sequential.algae, range_color=[min, max])

    main_map.update_layout(
        title_text = f'Percent of {type_string} {crop_string} Planted in {year} by State'
    )

    return main_map

#Map
@app.callback(
    Output(component_id='line_chart', component_property='figure'),
    Input("crop", "value"),
    Input("type", "value"),
)
def run_line_chart(crop, type):

    if "corn" in crop:
        crop_string = "Corn"

    if "cotton" in crop:
        crop_string = "Cotton"

    if "soybean" in crop:
        crop_string = "Soybean"
    
    if "Insect-resistant (Bt) only" in type:
        type_string = "Insect-resistant"
    
    if "Herbicide-tolerant only" in type:
        type_string = "Herbicide-tolerant"

    if "All GE varieties" in type:
        type_string = "Genetically Engineered"
    
    if "Stacked gene varieties" in type:
        type_string = "Stacked Gene"

    #Select Data
    data_average_selected = data_average.loc(axis=0)[crop, type]
    
    #Map Data
    line_chart = px.line(data_average_selected, x=data_average_selected.index, y="Value")
    line_chart.update_layout(
    title_text= f'Total Percent of {type_string} {crop_string} Planted in U.S',
    yaxis_title='Percent of affected Crops',
    xaxis_title= 'Year (2000-2020)',
    yaxis = dict(
        tickmode = 'linear',
        range=[0, 100],
        tick0 = 0,
        dtick = 20
        )
    )

    return line_chart




if __name__ == '__main__':
    app.run_server()
