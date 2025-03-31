# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()




# Create a dash application
app = dash.Dash(__name__)

# Create the dropdown menu options
dropdown_options = [
    {'label': 'All Sites', 'value': 'ALL'},
    {'label': 'CCAFS LC-40 - East Coast', 'value': 'CCAFS LC-40'},
    {'label': 'CCAFS SLC-40 - East Coast', 'value': 'CCAFS SLC-40'},
    {'label': 'KSC LC-39A - East Coast', 'value': 'KSC LC-39A'},
    {'label': 'VAFB SLC-4E - West Coast', 'value': 'VAFB SLC-4E'}
    ]

# Create an app layout
app.layout = html.Div([
    
    
        html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                
        html.Div([
                html.Label('Select a site:'),
                dcc.Dropdown
                    (
                    id='dropdown_sites',
                    options=dropdown_options,
                    value='ALL',
                    placeholder='Select a site',
                    searchable=True
                    )
                ]),

        html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),

        html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(id='payload_slider', min=0, max =10000, step=1000, marks={0:'0', 2500:'2500', 5000:'5000', 7500:'7500', 10000:'10000'}, value=[0, 10000]),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
        
        ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='dropdown_sites',component_property='value')
    )


def get_pie_chart(dropdown_sites_value):
    filtered_df = spacex_df
    if dropdown_sites_value == 'ALL':
        chart_title_ = 'Total Success Lauches for All Sites'
    else:
        chart_title_ = 'Total Success Lauches for site ' + dropdown_sites_value
        filtered_df = filtered_df[filtered_df['Launch Site'] == dropdown_sites_value ]
    
    labels = filtered_df['class'].value_counts().index
    values = filtered_df['class'].value_counts().values
    fig = px.pie(filtered_df, labels=labels, values=values, names=labels, title=chart_title_)
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='dropdown_sites',component_property='value'),
    Input(component_id='payload_slider',component_property='value')
    )

def get_scatter_plot(dropdown_sites_value, payload_slider_value):
    filtered_df = spacex_df[(spacex_df["Payload Mass (kg)"] >= payload_slider_value[0]) & (spacex_df["Payload Mass (kg)"] <= payload_slider_value[1])]
    if dropdown_sites_value == 'ALL':
        chart_title_= 'Success and Fail per Payload Mass for All Sites'
           
    else:
        chart_title_= 'Success and Fail per Payload Mass for Site ' + dropdown_sites_value
        filtered_df = filtered_df[filtered_df['Launch Site'] == dropdown_sites_value ]
    
    print(payload_slider_value[0])
    print(payload_slider_value[1])
    fig = px.scatter(filtered_df, x= 'Payload Mass (kg)', y='class', title=chart_title_, color='Launch Site')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
