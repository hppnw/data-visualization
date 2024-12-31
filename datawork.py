import plotly.express as px
import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output,callback
from plotly.graph_objects import Bar, Figure
from dash import dcc, html
import dash_bootstrap_components as dbc
from wordcloud import WordCloud
from io import BytesIO
import plotly.graph_objects as go
import base64
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体
plt.rcParams['axes.unicode_minus'] = False   # 正常显示负号
# 读取投票统计数据
data = pd.read_excel(r"harris_vs_trump.xlsx")
cleaned_data = pd.read_csv(r"cleaned_data.csv")
# 添加胜者字段和颜色字段
data["Winner"] = ["Harris" if h > t else "Trump" for h, t in zip(data["Harris support"], data["Trump support"])]
data["Color"] = ["blue" if winner == "Harris" else "red" for winner in data["Winner"]]

def create_race_figure():
    # Define the nodes
    nodes = {
        "label": ["White", "Black", "Latino", "Asian", "Native American", "Other",
                  "Donald Trump", "Kamala Harris"]
    }

    # Define the links between nodes (source -> target -> value)
    links = [
        {"source": 0, "target": 6, "value": 0.57},
        {"source": 0, "target": 7, "value": 0.42},
        {"source": 1, "target": 6, "value": 0.13},
        {"source": 1, "target": 7, "value": 0.86},
        {"source": 2, "target": 6, "value": 0.46},
        {"source": 2, "target": 7, "value": 0.51},
        {"source": 3, "target": 6, "value": 0.40},
        {"source": 3, "target": 7, "value": 0.55},
        {"source": 4, "target": 6, "value": 0.68},
        {"source": 4, "target": 7, "value": 0.31},
        {"source": 5, "target": 6, "value": 0.52},
        {"source": 5, "target": 7, "value": 0.44}
    ]

    # Define colors for the links
    colors = ["#1f77b4","#1f77b4", "#ff7f0e", "#ff7f0e","#2ca02c","#2ca02c", "#d62728", "#d62728","#9467bd", "#9467bd","#8c564b", "#8c564b"]

    # Create Sankey chart
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,  # space between nodes
            thickness=40,  # node thickness
            line=dict(color="black", width=1),  # node borders
            label=nodes["label"]  # set the labels of the nodes
        ),
        link=dict(
            source=[link["source"] for link in links],  # sources
            target=[link["target"] for link in links],  # targets
            value=[link["value"] for link in links],  # values
            color=colors  # link colors
        )
    ))

    fig.update_layout(
        title="Race Composition",
        font=dict(size=10)
    )

    return fig


def create_education_figure():
    # Define the nodes
    nodes = {
        "label": ["College degree", "No College degree",
                  "Donald Trump", "Kamala Harris"]
    }

    # Define the links between nodes (source -> target -> value)
    links = [
        {"source": 0, "target": 2, "value": 0.43},
        {"source": 0, "target": 3, "value": 0.56},
        {"source": 1, "target": 2, "value": 0.56},
        {"source": 1, "target": 3, "value": 0.43},
    ]

    # Define colors for the links
    colors = ["#1f77b4","#1f77b4", "#ff7f0e","#ff7f0e"]

    # Create Sankey chart
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,  # space between nodes
            thickness=20,  # node thickness
            line=dict(color="black", width=0.5),  # node borders
            label=nodes["label"]  # set the labels of the nodes
        ),
        link=dict(
            source=[link["source"] for link in links],  # sources
            target=[link["target"] for link in links],  # targets
            value=[link["value"] for link in links],  # values
            color=colors  # link colors
        )
    ))

    fig.update_layout(
        title="Education Composition",
        font=dict(size=10)
    )

    return fig


def create_area_type_figure():
    # Define the nodes
    nodes = {
        "label": ["Urban", "Suburban", "Rural",
                  "Donald Trump", "Kamala Harris"]
    }

    # Define the links between nodes (source -> target -> value)
    links = [
        {"source": 0, "target": 3, "value": 0.38},
        {"source": 0, "target": 4, "value": 0.60},
        {"source": 1, "target": 3, "value": 0.51},
        {"source": 1, "target": 4, "value": 0.47},
        {"source": 2, "target": 3, "value": 0.64},
        {"source": 2, "target": 4, "value": 0.34},
    ]

    # Define colors for the links
    colors = ["#1f77b4", "#1f77b4","#ff7f0e", "#ff7f0e","#2ca02c", "#2ca02c"]

    # Create Sankey chart
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,  # space between nodes
            thickness=20,  # node thickness
            line=dict(color="black", width=0.5),  # node borders
            label=nodes["label"]  # set the labels of the nodes
        ),
        link=dict(
            source=[link["source"] for link in links],  # sources
            target=[link["target"] for link in links],  # targets
            value=[link["value"] for link in links],  # values
            color=colors  # link colors
        )
    ))

    fig.update_layout(
        title="Area type Composition",
        font=dict(size=10)
    )

    return fig


def create_age_gender_figure():
    # Define the nodes
    nodes = {
        "label": ["Men 18-29", "Men 30-44", "Men 45-64", "Men 65 or older", "Women 18-29", "Women 30-44", "Women 45-64", "Women 65 or older",
                  "Donald Trump", "Kamala Harris"]
    }

    # Define the links between nodes (source -> target -> value)
    links = [
        {"source": 0, "target": 8, "value": 0.49},
        {"source": 0, "target": 9, "value": 0.48},
        {"source": 1, "target": 8, "value": 0.52},
        {"source": 1, "target": 9, "value": 0.45},
        {"source": 2, "target": 8, "value": 0.59},
        {"source": 2, "target": 9, "value": 0.39},
        {"source": 3, "target": 8, "value": 0.56},
        {"source": 3, "target": 9, "value": 0.43},
        {"source": 4, "target": 8, "value": 0.38},
        {"source": 4, "target": 9, "value": 0.61},
        {"source": 5, "target": 8, "value": 0.41},
        {"source": 5, "target": 9, "value": 0.56},
        {"source": 6, "target": 8, "value": 0.50},
        {"source": 6, "target": 9, "value": 0.49},
        {"source": 7, "target": 8, "value": 0.46},
        {"source": 7, "target": 9, "value": 0.53},
    ]

    # Define colors for the links
    colors = ["#1f77b4","#1f77b4", "#ff7f0e","#ff7f0e", "#2ca02c", "#2ca02c","#d62728","#d62728", "#9467bd","#9467bd", "#8c564b", "#8c564b", "#e377c2", "#e377c2", "#7f7f7f","#7f7f7f"]

    # Create Sankey chart
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,  # space between nodes
            thickness=20,  # node thickness
            line=dict(color="black", width=1),  # node borders
            label=nodes["label"]  # set the labels of the nodes
        ),
        link=dict(
            source=[link["source"] for link in links],  # sources
            target=[link["target"] for link in links],  # targets
            value=[link["value"] for link in links],  # values
            color=colors  # link colors
        )
    ))

    fig.update_layout(
        title="Age gender Composition",
        font=dict(size=10)
    )

    return fig


def generate_wordcloud(candidate_policies):
    wc = WordCloud(width=400, height=300, background_color="white").generate(candidate_policies)
    img = BytesIO()
    wc.to_image().save(img, format="PNG")
    return "data:image/png;base64," + base64.b64encode(img.getvalue()).decode()

trump_policies = "Economy, Tax Cuts, Immigration, America First, Defense Spending"
harris_policies = "Healthcare, Climate Change, Social Justice, Gun Control, Education"
trump_wordcloud = generate_wordcloud(trump_policies)
harris_wordcloud = generate_wordcloud(harris_policies)

def load_image_as_base64(path):
    with open(path, "rb") as image_file:
        return "data:image/png;base64," + base64.b64encode(image_file.read()).decode()

trump_image = load_image_as_base64("Trump.png")
harris_image = load_image_as_base64("Harris.jpg")

def create_us_map():
    fig = px.choropleth(
        data,
        locations="id",
        locationmode="USA-states",
        color="Winner",
        hover_name="name",
        scope="usa",
        color_discrete_map={"Harris": "blue", "Trump": "red"}
    )
    fig.update_layout(geo=dict(bgcolor="rgba(0,0,0,0)"))
    return fig

def create_state_detail(state_id):
    state_data = data[data["id"] == state_id].iloc[0]

    state_map = px.choropleth(
        data[data["id"] == state_id],
        locations="id",
        locationmode="USA-states",
        color="Winner",
        hover_name="name",
        scope="usa",
        color_discrete_map={"Harris": "blue", "Trump": "red"}
    )

    elector_votes = px.bar(
        x=[state_data["HarrisNum"], state_data["trumpNum"]],
        y=["Harris", "Trump"],
        orientation='h',
        text=[state_data["HarrisNum"], state_data["trumpNum"]],
        title=f"{state_data['name']} 选举人票分布"
    )
    elector_votes.update_traces(textposition="outside")

    total_votes = px.bar(
        x=[state_data["Harris support"], state_data["Trump support"]],
        y=["Harris", "Trump"],
        orientation='h',
        text=[state_data["Harris support"], state_data["Trump support"]],
        title=f"{state_data['name']} 总得票数分布"
    )
    total_votes.update_traces(textposition="outside")

    return state_map, elector_votes, total_votes
def create_electoral_bar():
    harris_votes = 70910573
    trump_votes = 74644300
    total_votes = harris_votes + trump_votes

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[trump_votes],
        y=["Electoral Votes"],
        orientation='h',
        marker=dict(color="red"),
        name="Donald Trump",
        text=f"{trump_votes} votes",
        textposition="inside",
        insidetextanchor="middle"
    ))
    fig.add_trace(go.Bar(
        x=[harris_votes],
        y=["Electoral Votes"],
        orientation='h',
        marker=dict(color="blue"),
        name="Kamala Harris",
        text=f"{harris_votes} votes",
        textposition="inside",
        insidetextanchor="middle"
    ))
    fig.update_layout(
        barmode='stack',
        height=100,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[0, total_votes]
        ),
        yaxis=dict(
            showticklabels=False
        ),
        plot_bgcolor="white"
    )
    return fig

def create_summary_charts():
    house_fig = Figure(
        data=[
            Bar(x=["Republicans", "Democrats"], y=[220, 215], marker_color=["red", "blue"])
        ]
    )
    house_fig.update_layout(
        title="U.S. House",
        xaxis_title="Party",
        yaxis_title="Seats",
        template="plotly_white"
    )

    senate_fig = Figure(
        data=[
            Bar(x=["Republicans", "Democrats"], y=[53, 47], marker_color=["red", "blue"])
        ]
    )
    senate_fig.update_layout(
        title="U.S. Senate",
        xaxis_title="Party",
        yaxis_title="Seats",
        template="plotly_white"
    )

    return house_fig, senate_fig

# 1. 各州候选人筹款金额的地图
def categorize_receipt(value):
    if value < 1_000_000:
        return "<1M"
    elif 1_000_000 <= value < 5_000_000:
        return "1M-5M"
    elif 5_000_000 <= value < 10_000_000:
        return "5M-10M"
    else:
        return ">10M"

cleaned_data["Receipt_Category"] = cleaned_data["Total_Receipt"].apply(categorize_receipt)

def create_state_fundraising_figure():
    fig = px.choropleth(
        cleaned_data,
        locations="Cand_State",
        locationmode="USA-states",
        color="Receipt_Category",  # 使用分段后的类别
        hover_name="Cand_Name",
        scope="usa",
        color_discrete_map={
            "<1M": "blue",
            "1M-5M": "green",
            "5M-10M": "orange",
            ">10M": "red"
        },
        title="各州候选人筹款金额"
    )
    return fig

# 2. 候选人筹款来源流向图
def create_fundraising_flow_figure():
    fig = go.Figure(
        data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=["Individual", "Party", "Other Committee", "Candidate", "Total"],
                color=["blue", "green", "orange", "purple", "red"]
            ),
            link=dict(
                source=[0, 1, 2, 3],
                target=[4, 4, 4, 4],
                value=[
                    cleaned_data["Individual_Contribution"].sum(),
                    cleaned_data["Party_Committee_Contribution"].sum(),
                    cleaned_data["Other_Committee_Contribution"].sum(),
                    cleaned_data["Cand_Contribution"].sum()
                ],
                color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
            )
        )]
    )
    fig.update_layout(title_text="候选人筹款来源流向图", font_size=12)
    return fig

# 3. 候选人筹款、支出与债务三维分析
def create_3d_analysis_figure():
    fig = px.scatter_3d(
        cleaned_data,
        x="Total_Receipt",
        y="Total_Disbursement",
        z="Debt_Owed_By_Committee",
        color="Cand_Party_Affiliation",
        hover_name="Cand_Name",
        title="候选人筹款、支出与债务三维分析"
    )
    return fig


electoral_bar = create_electoral_bar()
house_fig, senate_fig = create_summary_charts()

# 创建 Dash 应用
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# 主页面布局
main_layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.H1("2024美国大选可视化大屏", style={"textAlign": "center"}),

    # 柱状图
    dcc.Graph(
        id="vote-bar-chart",
        figure=electoral_bar,
        style={"height": "100px", "margin": "auto"}
    ),

    # 左右布局：候选人图像和地图
    html.Div([
        html.Div([
            html.Img(src=trump_image, style={"width": "150px", "height": "150px", "borderRadius": "50%", "margin": "auto"}),
            html.Img(src=trump_wordcloud, style={"width": "100%", "marginTop": "20px"}),
            html.P("Donald Trump", style={"textAlign": "center", "fontSize": "20px"})
        ], style={"width": "20%", "display": "inline-block"}),

        html.Div([
            dcc.Graph(id="us_map", figure=create_us_map(), style={"height": "500px"})
        ], style={"width": "60%", "display": "inline-block"}),

        html.Div([
            html.Img(src=harris_image, style={"width": "150px", "height": "150px", "borderRadius": "50%", "margin": "auto"}),
            html.Img(src=harris_wordcloud, style={"width": "100%", "marginTop": "20px"}),
            html.P("Kamala Harris", style={"textAlign": "center", "fontSize": "20px"}),
            dbc.Button("Finance", id="finance-button", color="primary", style={"display": "block", "margin": "20px auto"})
        ], style={"width": "20%", "display": "inline-block"})
    ], style={"display": "flex", "justifyContent": "center"}),

    # 选项卡：众议院与参议院
    html.Div([
        dbc.Tabs([
            dbc.Tab(dcc.Graph(figure=house_fig), label="U.S. House"),
            dbc.Tab(dcc.Graph(figure=senate_fig), label="U.S. Senate")
        ])
    ], style={"marginTop": "20px", "width": "70%", "margin": "auto"}),

    # 结论文本
    html.P(
        "共和党赢得国会控制权",
        style={"textAlign": "center", "marginTop": "20px", "fontSize": "18px", "fontWeight": "bold"}
    ),

    # 州详情占位符
    html.Div(id="state-detail-container", children=[
        html.Div(id="state_detail", style={"marginTop": "20px", "textAlign": "center", "fontSize": "20px"}),
        html.Div(id="state_map", style={"marginTop": "20px"})
    ]),

    # 主内容占位符
    html.Div(id="main-content")
])


# Finance 页面布局
finance_layout = html.Div([
    html.H1("候选人筹款分析"),
    dbc.Tabs([
        dbc.Tab(label="各州候选人筹款金额", children=[dcc.Graph(figure=create_state_fundraising_figure())]),
        dbc.Tab(label="候选人筹款来源流向图", children=[dcc.Graph(figure=create_fundraising_flow_figure())]),
        dbc.Tab(label="候选人筹款、支出与债务三维分析", children=[dcc.Graph(figure=create_3d_analysis_figure())])
    ])
])

state_detail_layout = html.Div([
    html.H1("州详情页面", style={"textAlign": "center"}),
    dcc.Graph(id="state-map"),  # 州地图
    dcc.Graph(id="elector-votes-chart"),  # 选举人票分布图
    dcc.Graph(id="total-votes-chart")  # 总得票数分布图
])

# 选项卡布局页面
tab_layout = html.Div([
    html.H1("How key groups of Americans voted in 2024",
            style={"textAlign": "center", "marginTop": "20px", "fontSize": "18px", "fontWeight": "bold"}),
    dbc.Tabs([
        dbc.Tab(label="种族分布", children=[dcc.Graph(figure=create_race_figure())]),
        dbc.Tab(label="教育程度分布", children=[dcc.Graph(figure=create_education_figure())]),
        dbc.Tab(label="区域类型分布", children=[dcc.Graph(figure=create_area_type_figure())]),
        dbc.Tab(label="年龄性别分布", children=[dcc.Graph(figure=create_age_gender_figure())])
    ])
])

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="main-layout", children=main_layout, style={"display": "block"}),
    html.Div(id="finance-layout", children=finance_layout, style={"display": "none"}),
    html.Div(id="state-detail-container", children=state_detail_layout, style={"display": "none"}),
    html.Div(id="tab-layout", children=tab_layout, style={"display": "none"})
])


@app.callback(
    [Output("main-layout", "style"),
     Output("finance-layout", "style"),
     Output("state-detail-container", "style"),
     Output("tab-layout", "style")],
    Input("url", "pathname")
)
def toggle_pages(pathname):
    if pathname == "/finance":
        return {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "none"}
    elif pathname == "/state-detail":
        return {"display": "none"}, {"display": "none"}, {"display": "block"}, {"display": "none"}
    elif pathname == "/tab-layout":
        return {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "block"}
    return {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}

@app.callback(
    [Output("state-map", "figure"),
     Output("elector-votes-chart", "figure"),
     Output("total-votes-chart", "figure")],
    Input("us_map", "clickData")
)
def update_state_detail(clickData):

    if not clickData or "points" not in clickData or not clickData["points"]:
        return {}, {}, {}

    state_id = clickData["points"][0]["location"]

    try:
        state_map, elector_votes, total_votes = create_state_detail(state_id)
        return state_map, elector_votes, total_votes
    except Exception as e:
        print(f"Error updating state detail: {e}")
        return {}, {}, {}

@app.callback(
    Output("url", "pathname"),
    [Input("finance-button", "n_clicks"),
     Input("us_map", "clickData"),
     Input("vote-bar-chart", "clickData")],
    prevent_initial_call=True
)
def navigate_to_pages(finance_click, us_map_click, bar_click):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "/"

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "finance-button" and finance_click:
        return "/finance"

    if triggered_id == "us_map" and us_map_click:
        return "/state-detail"

    if triggered_id == "vote-bar-chart" and bar_click:
        return "/tab-layout"

    return "/"


# 运行应用
if __name__ == "__main__":
    app.run_server(debug=True)
