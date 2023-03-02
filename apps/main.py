import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots


from app import app
from apps.data import df
from apps.functions import create_heatmap_array

# set graph variables
MARGIN = {"t": 60, "r": 40, "b": 40, "l": 40}
WIDTH = 1280
# WIDTH = 980
# HEIGHT = 720
HEIGHT = 420
PLOT_BGCOLOUR = "#F8F9F9"
FONT_SIZE = 20

COLOUR_BYD_AUTO = 'RGB(250, 97, 97)' 
COLOUR_BYD_AUTO_LIGHT = 'RGBA(250, 97, 97, 0.2)' 
COLOUR_VOLKSWAGEN =  'rgb(8, 247, 8)'
COLOUR_VOLKSWAGEN_LIGHT = 'RGBA(8, 247, 8, 0.2)' 
COLOUR_GAC_MOTOR = 'RGB(250, 173, 97)'
COLOUR_GAC_MOTOR_LIGHT = 'RGBA(250, 173, 97, 0.2)'
COLOUR_TESLA = 'RGB(173, 97, 250)'
COLOUR_TESLA_LIGHT = 'RGBA(173, 97, 250, 0.2)'
COLOUR_WULING = 'rgb(7, 223, 223)' 
COLOUR_WULING_LIGHT = 'RGBA(7, 223, 223, 0.2)' 
COLOUR_OTHERS = 'RGB(99, 110, 250)' 
COLOUR_OTHERS_LIGHT = 'RGBA(99, 110, 250, 0.2)' 

BRAND_COLOUR_DICT = {
    "BYD Auto": COLOUR_BYD_AUTO,
    "Volkswagen": COLOUR_VOLKSWAGEN,
    "GAC Motor": COLOUR_GAC_MOTOR,
    "Tesla": COLOUR_TESLA,
    "Wuling": COLOUR_WULING,
    "Others": COLOUR_OTHERS
}

BRAND_COLOUR_LIGHT_DICT = {
    "BYD Auto": COLOUR_BYD_AUTO_LIGHT,
    "Volkswagen": COLOUR_VOLKSWAGEN_LIGHT,
    "GAC Motor": COLOUR_GAC_MOTOR_LIGHT,
    "Tesla": COLOUR_TESLA_LIGHT,
    "Wuling": COLOUR_WULING_LIGHT,
    "Others": COLOUR_OTHERS_LIGHT
}

# #filter only the most recent quarter
# df = df.loc[df["Quarter"] == "Q3 2022"].copy()

#create the order each category should appear on the heatmp
df["Order"] = 1
df.loc[df["Brands"] == "Volkswagen", "Order"] = 3
df.loc[df["Brands"] == "GAC Motor", "Order"] = 4
df.loc[df["Brands"] == "Tesla", "Order"] = 2
df.loc[df["Brands"] == "Wuling", "Order"] = 5
df.loc[df["Brands"] == "Others", "Order"] = 6

#sort each brand
df.sort_values(by = "Order", inplace = True)


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.P("Select Car Brand:", style={"font-size": 20}),
            dbc.RadioItems(id = "car-brand-radio", label_checked_class_name = "car-brand-label-checked",
                            # options = [{"label": dbc.Label(brand, style ={"color": BRAND_COLOUR_DICT[brand]}), "value": brand} for brand in df["Brands"].unique()],
                            options = [{"label": brand, "value": brand, "label_id": "radio-label-{}".format(brand.lower().replace(" ", "-")), "input-id": "radio-input-{}".format(brand.lower().replace(" ", "-"))} for brand in df["Brands"].unique()],
                            
                            value = "BYD Auto",
                            inline = True
                            )
        ], style={"display": "inline-flex"})
    ], className = "radio-row"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "waffle-graph", config = {"displayModeBar": False})
        ])
    ])
], style={"display": "inline-flex", "flex-wrap": "wrap", "justify-content": "center"})



#create the callback
@app.callback(Output("waffle-graph", "figure"),
            [Input("car-brand-radio", "value")])


def create_layout(car_brand):
    
    # car_brand = "BYD Auto"

    for brand, colour in BRAND_COLOUR_DICT.items():
        if brand == car_brand:
            COLOUR = colour
            df.loc[df["Brands"] == brand, "Colour"] = colour
        else:
            df.loc[df["Brands"] == brand, "Colour"] = BRAND_COLOUR_LIGHT_DICT[brand]

    # create an array of the colours and the lower and upper bounds for each colour
    colours = [    [0, df.loc[df["Brands"] == "BYD Auto", "Colour"].iloc[0]],
                [0.166, df.loc[df["Brands"] == "BYD Auto", "Colour"].iloc[0]],
                [0.166, df.loc[df["Brands"] == "Tesla", "Colour"].iloc[0]],
                [0.333, df.loc[df["Brands"] == "Tesla", "Colour"].iloc[0]],

                [0.333, df.loc[df["Brands"] == "Volkswagen", "Colour"].iloc[0]],
                [0.5, df.loc[df["Brands"] == "Volkswagen", "Colour"].iloc[0]],

                [0.5, df.loc[df["Brands"] == "GAC Motor", "Colour"].iloc[0]],
                [0.666, df.loc[df["Brands"] == "GAC Motor", "Colour"].iloc[0]],
                [0.666, df.loc[df["Brands"] == "Wuling", "Colour"].iloc[0]],
                [0.833, df.loc[df["Brands"] == "Wuling", "Colour"].iloc[0]],
                [0.833, df.loc[df["Brands"] == "Others", "Colour"].iloc[0]],
                [1, df.loc[df["Brands"] == "Others", "Colour"].iloc[0]]
    ]



    #create the 10x10 arrays for each quarter to be passed to heatmap
    data_q3_2022 = create_heatmap_array(df.loc[df["Quarter"] == "Q3 2022"])
    data_q2_2022 = create_heatmap_array(df.loc[df["Quarter"] == "Q2 2022"])
    
    df.loc[(df["Brands"] == "Others") & (df["Quarter"] == "Q1 2022"), "MarketShareReformat"] = 0.585
    data_q1_2022 = create_heatmap_array(df.loc[df["Quarter"] == "Q1 2022"])
    data_q4_2021 = create_heatmap_array(df.loc[df["Quarter"] == "Q4 2021"])

    fig = make_subplots(cols = 4, rows = 1)

    fig.add_trace(go.Heatmap(z=data_q4_2021,
                        xgap = 3,
                        ygap = 3, 
                        colorscale = colours,
                        showscale = False), row = 1, col = 1)
    
    fig.add_trace(go.Heatmap(z=data_q1_2022,
                        xgap = 3,
                        ygap = 3, 
                        colorscale = colours,
                        showscale = False), row = 1, col = 2)

    fig.add_trace(go.Heatmap(z=data_q2_2022,
                        xgap = 3,
                        ygap = 3, 
                        colorscale = colours,
                        showscale = False), row = 1, col = 3)

    fig.add_trace(go.Heatmap(z=data_q3_2022,
                        xgap = 3,
                        ygap = 3, 
                        colorscale = colours,
                        showscale = False), row = 1, col = 4)

    fig.update_layout(plot_bgcolor = PLOT_BGCOLOUR,
                        paper_bgcolor = PLOT_BGCOLOUR,
                        width = WIDTH,
                        height = HEIGHT,
                        margin = MARGIN,
                        )

    #hide the tick marks on the x and y axes
    fig.update_xaxes(showticklabels = False)
    fig.update_yaxes(showticklabels = False)


    df_annotations = pd.DataFrame({
        "Quarter": ["Q4 2021", "Q1 2022", "Q2 2022", "Q3 2022"],
        "ref": [1, 2, 3, 4]
    })

    df_annotations = df_annotations.merge(df.loc[df["Brands"] == car_brand, ["Quarter", "MarketShareReformat", "Colour", "Brands"]], on = "Quarter").copy()

        
    
    for index, row in df_annotations.iterrows():
        fig.add_annotation(text = '{}: <span style="color:'.format(row["Quarter"]) + COLOUR +'"><b>{:.0%}</b></span>'.format(row["MarketShareReformat"]),
                            xref = "x{}".format(row["ref"]),
                            yref = "paper",
                            x = 5,
                            y = 1.05,
                            showarrow = False,
                            font = dict(size = FONT_SIZE),
                            yanchor = "bottom"
                            )



    return fig


