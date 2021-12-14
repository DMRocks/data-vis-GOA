import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import pandas as pd
import plotly.express as px

url = 'https://raw.githubusercontent.com/DMRocks/data-vis-GOA/main/Landmine-Area/Areas%20contaminated%20by%20landmine%20(sq.km).cvs'
data = pd.read_csv(url, index_col = 'Year')

external_stylesheets= ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets= external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H3("Top Countries Contaminated by Landmines World Bank"),
        html.Div([
        dcc.Dropdown(
            id='region', clearable=False,
            value='Cambodia', options=[
                {'label': c, 'value': c}
                for c in data.columns
            ], multi = True),
    ],style={'display': 'inline', 'width': '15%'}),
        
        html.Div([
        dcc.Graph(id='graph'),
    ],style={'display': 'inline-block', 'width': '45%'}),
        
        html.Div([
        dcc.Graph(id='graph_2'),
    ],style={'display': 'inline-block', 'width': '55%'})
])

# Define callback to update graph
@app.callback(
    [dash.dependencies.Output('graph', 'figure'),dash.dependencies.Output('graph_2', 'figure')],
    [dash.dependencies.Input("region", "value")]
)

def multi_output(region):

    fig1 = px.line(data, x=data.index, y=region)
    fig2 = px.area(data, x=data.index, y=region)
    
    fig1.update_layout(
    yaxis_title='Square Kilometers',
    showlegend = False
    )
    
    fig2.update_layout(
    legend_title_text='Country',
    yaxis_title='Square Kilometers',
    )

    fig1.update_xaxes(showspikes=True)
    fig1.update_yaxes(showspikes=True)

    return fig1, fig2


# Run app
if __name__ == '__main__':
    app.run_server()
