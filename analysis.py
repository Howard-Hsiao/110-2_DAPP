from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import math
import plotly.express as px
from utils import *
from datetime import datetime

external_stylesheets = [dbc.themes.DARKLY]

app = Dash(__name__, external_stylesheets=external_stylesheets)

DISPLAY_LIMIT = 15
initial_nft = 919
initial_nft_data = get_NFT_record(initial_nft)
initial_records  = initial_nft_data["records"][:DISPLAY_LIMIT]
initial_nft_df = pd.DataFrame({
    "time": [datetime.fromtimestamp(i["timestamp"]) for i in initial_records], 
    "type": [i["type"] for i in initial_records], 
    "price": [i["price"] for i in initial_records], 
    "amount": [i["amount"] for i in initial_records], 
    "address": [i["address"] for i in initial_records]
})

app.layout = html.Div([
    html.Div([
        html.H5('R10944033 analyze tool')
    ], style={"display":"flex", "flex-direction": "row", "justify-content":"center", "background-color": "#2fa5ba"}), 
    html.Div([
        html.H1('Analysis of akaswap'),
        html.Div([
            html.H4('Please input tokenID'),
            dbc.Input(
                id="NFT_address_input", 
                placeholder='Enter Address of NFT',
                type='text',
                value=f'{initial_nft}',
                debounce=True
            ), 
            html.Div([
                dcc.Graph(
                    id="NFT_pie_chart",
                    figure=pieChartByTokenId(initial_nft), 
                ),
                html.Div([
                    html.H5("The records of a NFT", style={"text-align": "center"}), 
                    dbc.Table.from_dataframe(initial_nft_df, striped=True, bordered=True, hover=True), 
                ], id="NFT_table"
                , style={
                    "display": "flex", 
                    "flex-direction": "column", 
                    "justify-content": "center"
                })
            ], style={
                "display": "flex", 
                "flex-direction": "row", 
                "justify-content": "space-around"
            })
        ])
    ], style={"padding": "30px"}) # , style={"border-top": "50px #1f8a8c solid", "padding": "30px"})
])


@app.callback(Output('NFT_pie_chart', 'figure'), 
              Output('NFT_table', "children"), 
              Input('NFT_address_input', 'value')) 
def update_ana_NFT(NFT_tokenID):
    data = get_NFT_record(NFT_tokenID)
    data_records  = data["records"][:DISPLAY_LIMIT]

    pie_chart = pieChartByTokenId(NFT_tokenID)

    table_df = pd.DataFrame({
        "time": [datetime.fromtimestamp(i["timestamp"]) for i in data_records], 
        "type": [i["type"] for i in data_records], 
        "price": [i["price"] for i in data_records], 
        "amount": [i["amount"] for i in data_records], 
        "address": [i["address"] for i in data_records]
    })

    return pie_chart, [html.H5("The records of a NFT",  style={"text-align": "center"}), dbc.Table.from_dataframe(table_df, striped=True, bordered=True, hover=True)]


if __name__ == '__main__':
    app.run_server(debug=True)