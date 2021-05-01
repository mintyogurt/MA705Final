import plotly.express as px
import pandas as pd
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import base64

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#F0F8FF',
    'text': '#00008B'
}

image_filename = 'fastfood-hand-drawn-cartoon-doodles-260nw-1656501355.jpg' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

df = pd.read_csv('causual dining.csv')
df1 = df[['date','brand_name','impression.score','quality.score','value.score','reputation.score','buzz.score','satisfaction.score']]
options = ['impression.score','quality.score','value.score','reputation.score','buzz.score','satisfaction.score']

dff = df.groupby(['brand_name'], as_index=False)[['impression.score','quality.score','value.score','reputation.score','buzz.score','satisfaction.score']].mean()
dff = dff.round({'impression.score':2,'quality.score':2,'value.score':2,'reputation.score':2,'buzz.score':2,'satisfaction.score':2})

df3 = df[['brand_name','adaware.score','attention.score','consider.score','likelybuy.score']]
df3 = df3.groupby(['brand_name'], as_index=False).mean()
df3f = df3.set_index('brand_name').stack().reset_index()
df3f.columns = ['brand_name', 'score', 'value']

bar = px.bar(df3f, x="brand_name", y="value", color = 'score')
fig = px.scatter(df1, x='date', y='impression.score', color='brand_name')
fig.update_traces(mode='markers+lines')

app.layout = html.Div(children=[
    html.H1(children='Brand Index Dashboard - Fast Casual Dining (2021Q1)',
            style={'margin':25, 'textAlign': 'center'}),

    html.Div(children='''MA705 Final Project by Candice Wu''',
            style={'margin':25, 'textAlign': 'center'}),

    html.Div(children='''This dashboard reflects public’s perception of popular Fast Casual Dining Brands in 2021 Q1 measured by YouGov BrandIndex.''',
            style={'margin':25, 'textAlign': 'center'}),

        html.Div(children='''The scores help business to measure brand health, monitor growth, track advertising campaigns and inform competitive strategy.''',
            style={'margin':25, 'textAlign': 'center'}),



    html.Div([html.Img(src='data:image/jpg;base64,{}'.format(encoded_image.decode()))],style={'margin':25, 'textAlign': 'center'}),

    html.H2(children='Section 1: Customer Action Score',
            style={'margin':25, 'textAlign': 'center'}),

    html.H6(children='This section provides a visualization of customer action scores',style={'margin':25, 'textAlign': 'center'}
    ),

    html.Div([html.H6('Please select the brand(s) you want to display:'),
              dcc.Checklist(
                  options=[{'label': 'IHOP', 'value': 'IHOP'},
                           {'label': 'LongHorn Steakhouse', 'value': 'LongHorn Steakhouse'},
                           {'label': 'Outback Steakhouse', 'value': 'Outback Steakhouse'},
                           {'label': 'Five Guys', 'value': 'Five Guys'},
                           {'label': 'Burger King', 'value': 'Burger King'},
                           {'label': 'Fleming\'s', 'value': 'Fleming\'s'},
                           {'label': 'McDonald\'s', 'value': 'McDonald\'s'},
                           {'label': 'Olive Garden', 'value': 'Olive Garden'},
                           {'label': 'Chipotle', 'value': 'Chipotle'},
                           {'label': 'KFC', 'value': 'KFC'},
                           {'label': 'Popeyes', 'value': 'Popeyes'},
                           {'label': 'Romano\'s Macaroni Grill', 'value': 'Romano\'s Macaroni Grill'},
                           {'label': 'Panera Bread', 'value': 'Panera Bread'},
                           {'label': 'Taco Bell', 'value': 'Taco Bell'}],
                  value=['IHOP', 'LongHorn Steakhouse', 'Outback Steakhouse','Five Guys','Burger King','Fleming\'s','McDonald\'s','Olive Garden','Chipotle','KFC','Popeyes''Romano\'s Macaroni Grill','Panera Bread','Taco Bell'],
                  labelStyle={'display': 'inline-block'},
                  id = 'brand_checklist')
    ]),

    html.Div([dcc.Graph(id='bar-graph',figure=bar)]),


    html.H2(children='Section 2: Brand Impact Score',
            style={'margin':25, 'textAlign': 'center'}),

    html.H6(children='This section provides week over week brand impact score trend lines and an avg scores per brand table.',style={'margin':25, 'textAlign': 'center'}
    ),

    html.H6(children='Please use the dropdown to choose the score to display. You can also click on brand names to see and unsee brand:'
    ),

    html.Div(children='''Week over Week Impact Score by Brand''',
            style={'margin':25, 'textAlign': 'center'}),

    html.Div([
        dcc.Dropdown(
            id='score_checklist',
            options=[{'label': i, 'value': i} for i in options],
            value= options
        )
    ]),

    html.Div([dcc.Graph(
        id='line-graph',
        figure=fig)
    ]),

    html.H6(children='Please use the sort and filter function to see individual brand/top score/botton score:'),

    html.Div(children='''Average Impact Score by Brand''',
            style={'margin':25, 'textAlign': 'center'}),

    html.Div([
        dash_table.DataTable(
            id='table-viz',
            data=dff.to_dict('records'),
            columns=[
                {'name': i, 'id': i} for i in dff.columns
            ],
            filter_action = "native",
            sort_action = "native",
            sort_mode = "multi",
            fixed_rows={ 'headers': True, 'data': 0},
            style_cell={
                'whiteSpace': 'normal'
            },
            style_data_conditional=[
                {'if': {'column_id': 'brand_name'},
                 'width': '100px', 'textAlign': 'center'},
                {'if': {'column_id': 'impression.score'},
                 'width': '50px', 'textAlign': 'center'},
                {'if': {'column_id': 'quality.score'},
                 'width': '50px', 'textAlign': 'center'},
                {'if': {'column_id': 'value.score'},
                 'width': '50px', 'textAlign': 'center'},
                {'if': {'column_id': 'reputation.score'},
                 'width': '50px', 'textAlign': 'center'},
                {'if': {'column_id': 'buzz.score'},
                 'width': '50px', 'textAlign': 'center'},
                {'if': {'column_id': 'satisfaction.score'},
                 'width': '50px', 'textAlign': 'center'},
            ],
            virtualization=True,
            page_action='none')
    ]),

    html.A('Data powered by YouGov Brand Index, click to learn more.',
           href='https://business.yougov.com/product/brandindex',
           target='_blank',
           style={'margin':25, 'textAlign': 'center'})
])


@app.callback(
    Output(component_id="bar-graph", component_property="figure"),
    [Input(component_id="brand_checklist", component_property="value")]
)
def update_plot(brand):
    df2 = df3f[df3f.brand_name.isin(brand)].sort_values('value', ascending=False)
    bar = px.bar(df2, x="brand_name", y="value", color = 'score')
    return bar

@app.callback(
    Output(component_id="line-graph", component_property="figure"),
    [Input(component_id="score_checklist", component_property="value")]
)
def update_plot(options):
    fig = px.scatter(df1, x='date', y=df[options], color='brand_name')
    fig.update_traces(mode='markers+lines')
    return fig

server = app.server

if __name__ == '__main__':
    app.run_server(debug=False)
