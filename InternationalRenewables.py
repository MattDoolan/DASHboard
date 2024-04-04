# Import necessary libraries
import pandas as pd
import plotly.graph_objs as go
from dash import dcc, html, Dash
from dash.dependencies import Input, Output


# Load your data before defining the Dash app
def load_data():
    print("Loading data...")
    csv_url = 'https://raw.githubusercontent.com/MattDoolan/DASHboard/main/Renewableenergyconsumption.csv'
    df = pd.read_csv(csv_url)
    return df

df = load_data()

# Initialize Dash app


app = Dash(__name__) 
server = app.server



# Define your data variables
Years = df.columns[1:]
CountriesRegions = df.iloc[:, 0]
Percentage = df.iloc[:, 1:]

# Define the layout of your Dash application
app.layout = html.Div([
    html.H1('Renewable Energy Consumption (% of Total Final Energy Consumption)', style={'margin-top': '50px'}),
    dcc.Dropdown(
        id='countries-dropdown',
        options=[{'label': source, 'value': source} for source in CountriesRegions],
        value=CountriesRegions[0]
    ),
    dcc.Graph(id='renewable-energy-graph'),
    html.Footer('Data source: World Data Bank', style={'textAlign': 'center', 'fontSize': '12px', 'color': 'gray'})
])


# Define callback to update the graph based on dropdown selection
@app.callback(
    Output('renewable-energy-graph', 'figure'),
    [Input('countries-dropdown', 'value')]
)
def update_graph(selected_source):
    data = df[df.iloc[:, 0] == selected_source]
    trace = go.Scatter(x=Years, y=data.iloc[:, 1:].values[0], mode='lines+markers')
    layout = go.Layout(
        title=f'{selected_source}',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Percentage', range=[0, 100], tickvals=list(range(0, 101, 10)), ticktext=[str(i) for i in range(0, 101, 10)]), 
        margin=dict(l=40, r=40, t=40, b=40)
    )
    fig = go.Figure(data=[trace], layout=layout)
    return fig.to_dict()


# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)


