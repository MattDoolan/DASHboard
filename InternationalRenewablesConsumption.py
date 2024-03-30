#Importing everything we need for this script
import pandas as pd
import matplotlib.pyplot as plt
import dash
# importing dash core components 
from dash import dcc, html
#importing dash dependencies in order to build the callback function, this lets us utilise an input to create an output.
from dash.dependencies import Input, Output
#importing plotly as go, plotly is a graphical tool,Matplotlib might be preferred for static, publication-quality plots.
#while Plotly might be chosen for interactive visualizations or web applications.
import plotly.graph_objs as go
import urllib.parse
from flask import Flask




#Defining and importing our data from CSV_file (local)
#df = pd.read_csv(r'projects/python/CSV_FILES/Renewable energy consumption (% of total final energy consumption).csv')

# URL of the raw CSV file on GitHub defining and importing our data from online

csv_url = 'https://raw.githubusercontent.com/MattDoolan/DASHboard/main/Renewableenergyconsumption.csv'

df = pd.read_csv(csv_url)



Years = df.columns[1:]  # The years are the column names from the second column onwards
CountriesRegions = df.iloc[:, 0]  # The energy sources are the values in the first column
Percentage = df.iloc[:, 1:]  # Here we define our numerical values

# Years = df.columns[1:]  #The years are the column names from the second column onwards
# CountriesRegions = df.iloc[:, 0]  #The energy sources are the values in the first column
# Percentage = df.iloc[:, 1:] #Here we define our numerical values

# Initialize Dash app
app = dash.Dash(__name__) #In simpler terms, it's creating a Dash application object that you can use to build your web application. Naming the application 'app'

#server = app.server

# #This sets the layout of your Dash application, specifying how the components (like dropdowns, graphs, etc.) will be arranged.
app.layout = html.Div([  #This creates a division or container. Inside the square brackets,Everything inside this html.Div will be grouped together visually on your web page.
    dcc.Dropdown(
        id='countries-dropdown', #This is the id of the dropdown, this is used to reference the dropdown in the callback function   
        options=[{'label': source, 'value': source} for source in CountriesRegions], #This is the options of the dropdown, this is used to define the options of the dropdown
        value=CountriesRegions[0]  # Default value
    ),
    dcc.Graph(id='renewable-energy-graph')
])

# Define callback to update the graph based on dropdown selection
@app.callback(
    Output('renewable-energy-graph', 'figure'),
    [Input('countries-dropdown', 'value')]
)

def update_graph(selected_source):
    data = df[df.iloc[:, 0] == selected_source] #This line filters the DataFrame (df) based on the selected energy source.
    trace = go.Scatter(x=Years, y=data.iloc[:, 1:].values[0], mode='lines+markers') #This line creates a scatter plot of the filtered data.
    layout = go.Layout( #This line creates a layout for the graph.
        title=f'Renewable energy consumption (% of total final energy consumption)   {selected_source}',  #This line sets the title of the graph.
        xaxis=dict(title='Year'), #This line sets the title of the x-axis.
        yaxis=dict(title='Percentage'), #This line sets the title of the y-axis.
        showlegend=True, 
        margin=dict(l=40, r=40, t=40, b=40)  #In simpler terms, it's like specifying how much space you want to leave around the edges of your plot.
    )
    
    #So, this line essentially prepares the plot data in a format that Dash can handle
    #Ensuring that the plot is properly formatted before it's returned to the Dash application for rendering.
    fig = go.Figure(data=[trace], layout=layout)
    return fig.to_dict()

#Run the app
if __name__ == '__main__':
    app.run_server(debug=False)

    



