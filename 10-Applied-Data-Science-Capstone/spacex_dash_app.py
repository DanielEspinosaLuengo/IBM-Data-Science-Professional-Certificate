"""IBM SpaceX Falcon 9 Dash lab — completed student implementation.
Run: pip install dash plotly pandas; python spacex_dash_app.py
Data requires network access to the IBM-hosted CSV.
"""
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv'
spacex_df = pd.read_csv(URL)
app = Dash(__name__)
server = app.server
sites = sorted(spacex_df['Launch Site'].dropna().unique())
app.layout = html.Div([
    html.H1('SpaceX Falcon 9 Launch Success Dashboard', style={'textAlign':'center','color':'#183778'}),
    html.P('Explore launch success by site, payload mass and booster version.'),
    dcc.Dropdown(id='site-dropdown', options=[{'label':'All Sites','value':'ALL'}] + [{'label':s,'value':s} for s in sites], value='ALL', clearable=False),
    dcc.Graph(id='success-pie-chart'),
    html.P('Payload mass range (kg)'),
    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=500, marks={i:str(i) for i in range(0,10001,2000)}, value=[0,10000]),
    dcc.Graph(id='success-payload-scatter-chart')
], style={'maxWidth':'1150px','margin':'auto','fontFamily':'Arial'})

@app.callback(Output('success-pie-chart','figure'), Input('site-dropdown','value'))
def update_pie(site):
    if site == 'ALL':
        counts = spacex_df.loc[spacex_df['class'] == 1].groupby('Launch Site').size().reset_index(name='Successes')
        return px.pie(counts, values='Successes', names='Launch Site', title='Successful launches by site')
    subset = spacex_df[spacex_df['Launch Site']==site]
    counts = subset['class'].value_counts().rename(index={0:'Failure',1:'Success'}).reset_index()
    counts.columns=['Outcome','Count']
    return px.pie(counts, values='Count', names='Outcome', title=f'Landing outcomes at {site}')

@app.callback(Output('success-payload-scatter-chart','figure'), Input('site-dropdown','value'), Input('payload-slider','value'))
def update_scatter(site, payload_range):
    data = spacex_df if site == 'ALL' else spacex_df[spacex_df['Launch Site']==site]
    data = data[data['Payload Mass (kg)'].between(payload_range[0], payload_range[1])]
    return px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category', hover_data=['Launch Site'], title='Payload mass and landing success', labels={'class':'Landing success (0=no, 1=yes)'})

if __name__ == '__main__':
    app.run(debug=True)
