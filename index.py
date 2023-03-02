
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import app, server
from apps import main


#create the header that will be used for the page
header = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Global Electric Car Market Share by Car Brand"), className="col-12 col-center", id= "header"),
    ], className="col-center")
])

# create the page layout, which sets each page's url, includes and header and what will be the page content
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    header,
    dbc.Container(id="page-content", className = "col-12 col-center")
], style = {"textAlign": "center"})

# callback to load the page content
@app.callback(Output("page-content", "children"),
              Input("url", "pathname"))
def create_page_content(pathname):
    if pathname == "/main":
        return main.layout
    else:
        return main.layout

# run the app
if __name__ == "__main__":
    # print("Running in development mode")
    app.run_server(host="0.0.0.0", port=5000, debug=False)
