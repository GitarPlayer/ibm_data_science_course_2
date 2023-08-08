#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard



#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': '...........', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': '.........'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'fontSize': '24px'}),
    # First Dropdown for selecting report type
    html.Div([dcc.Dropdown(id='dropdown-statistics', 
                 options=[
                     {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                     {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                 ],
                 placeholder='Select a report type',
                 value='Select Statistics',
                 style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlignLast' : 'center'})
    ]),
    
    # Second Dropdown for selecting the year
    html.Div([dcc.Dropdown(id='input_year', 
                 options=[{'label': str(i), 'value': str(i)} for i in year_list],
                 placeholder='Select a year',
                 style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlignLast' : 'center'})
    ]),
    





    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'grid'}),
    ])
    
])
#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
from dash.dependencies import Input, Output

# Callback to enable or disable the 'input_year' dropdown based on the selected report type
@app.callback(
    Output(component_id='input_year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(report_type):
    if report_type == 'Yearly Statistics':
        return False
    else:
        return True


# Callback to generate and display the plots based on the selected report type and year
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='input_year', component_property='value')]
)
def update_output_container(report_type, input_year):
    
    
    if report_type == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        print(recession_data.columns)
        #TASK 2.5: Creating Graphs for Recession data

#Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        # use groupby to create relevant data for plotting
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Automobile Sales Fluctuation Over Recession Period (Year-wise)")
        )
        


#Plot 2 Calculate the average number of vehicles sold by vehicle type       
        # use groupby to create relevant data for plotting
        vehicle_avg_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()

        R_chart2 = dcc.Graph(
            figure=px.bar(vehicle_avg_sales, 
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Number of Vehicles Sold by Vehicle Type")
        )
        

        
# Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        # use groupby to create relevant data for plotting
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()

        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title="Total Advertising Expenditure Share by Vehicle Type During Recessions")
        )
        


# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        vehicle_unemployment_effect = recession_data.groupby(['Vehicle_Type', 'unemployment_rate'])['Automobile_Sales'].mean().reset_index()

        R_chart4 = dcc.Graph(
            figure=px.bar(vehicle_unemployment_effect, 
                x='Vehicle_Type',
                y='Automobile_Sales',
                color='unemployment_rate',
                title="Effect of Unemployment Rate on Vehicle Type and Sales")
        )
        
        return [
            # First row of plots
            html.Div(className='chart-item', children=[html.Div(children=[R_chart1]), html.Div(children=[R_chart2])],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=[R_chart3]), html.Div(children=[R_chart4])],style={'display': 'flex'})
        ]

        
    elif (input_year  and report_type  == 'Yearly Statistics'):
        input_year = int(input_year)
        yearly_data = data[data['Year'] == input_year ]
 
        
        
                                    
#plot 1 Yearly Automobile sales using line chart for the whole period.
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()

        Y_chart1 = dcc.Graph(
            figure=px.line(yas, 
                        x='Year',
                        y='Automobile_Sales',
                        title="Yearly Automobile Sales Over The Whole Period",
                        labels={'Automobile_Sales': 'Average Sales'})
        )
        
            
# Plot 2 Total Monthly Automobile sales using line chart.
        monthly_sales = data.groupby(['Year', 'Month'])['Automobile_Sales'].sum().reset_index()

        monthly_sales['Year-Month'] = monthly_sales['Year'].astype(str) + '-' + monthly_sales['Month'].astype(str)

        Y_chart2 = dcc.Graph(
            figure=px.line(monthly_sales, 
                        x='Year-Month',
                        y='Automobile_Sales',
                        title="Total Monthly Automobile Sales Over The Whole Period",
                        labels={'Automobile_Sales': 'Total Sales'})
        )

        

        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()

        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata, 
                        x='Vehicle_Type',
                        y='Automobile_Sales',
                        title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year),
                        labels={'Automobile_Sales': 'Average Sales'})
        )
        


        vehicle_ad_exp = data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()

        Y_chart4 = dcc.Graph(
            figure=px.pie(vehicle_ad_exp, 
                        values='Advertising_Expenditure',
                        names='Vehicle_Type',
                        title="Total Advertisement Expenditure for Each Vehicle Over The Whole Period",
                        labels={'Advertising_Expenditure': 'Expenditure in USD'})
        )
        
        return [
            # First row of plots
            html.Div(className='chart-item', children=[html.Div(children=[Y_chart1]), html.Div(children=[Y_chart2])],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=[Y_chart3]), html.Div(children=[Y_chart4])],style={'display': 'flex'})
        ]


    






                
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

