from dash import Dash, dcc, html
import requests as rq
import pandas as pd
import plotly.express as px

def aka_get(api):
    return rq.get(api, verify=False)

def get_NFT_record(tokenId):
    return aka_get(f"https://akaswap.com/api/akaobjs/{tokenId}/records").json()

def pieChartByTokenId(tokenID):
    data = get_NFT_record(tokenID)
    df = pd.DataFrame({
        "type": [i["type"] for i in data["records"]], 
        "address": [i["address"] for i in data["records"]]
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