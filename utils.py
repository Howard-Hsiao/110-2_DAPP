from dash import Dash, dcc, html
import requests as rq
import pandas as pd
import plotly.express as px
from sklearn.exceptions import DataConversionWarning

def aka_get(api):
    return rq.get(api, verify=False)

def get_NFT_record(tokenId):
    return aka_get(f"https://akaswap.com/api/akaobjs/{tokenId}/records").json()


def get_wallet_record(address):
    return aka_get(f"https://api.akaswap.com/v2/accounts/{address}/records").json()


def pieChartByTokenId(data):
    df = pd.DataFrame({
        "type": [i["type"] for i in data], 
        "address": [i["address"] for i in data]
    })
    fig = px.pie(df, names="type", title='The operation made on this NFT', template="plotly_dark")
    fig.update_layout(
        autosize=False,
        width=500,
        height=500,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)'
    )
    return fig

def pieChartByWallet(data):
    df = pd.DataFrame({
        "type": [i["type"] for i in data] 
    })
    fig = px.pie(df, names="type", title='The operation made by this wallet', template="plotly_dark")
    fig.update_layout(
        autosize=False,
        width=500,
        height=500,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)'
    )
    return fig

def lineChartbyOp(data, op="collect"):
    # data is of json format
    df = pd.DataFrame({
        "price": [i["price"] for i in data if i["type"] == op], 
        "time": [i["timestamp"] for i in data if i["type"] == op], 
    })

    fig = px.line(df, x="time", y="price", title=f'Trend of {op}', template="plotly_dark")
    fig.update_layout(
        autosize=False,
        width=500,
        height=500,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)'
    )
    return fig