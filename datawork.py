import plotly.express as px
import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output,callback,State
from plotly.graph_objects import Bar, Figure
from dash import dcc, html
import dash_bootstrap_components as dbc
from wordcloud import WordCloud
from io import BytesIO
import plotly.graph_objects as go
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import os
import us

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体
plt.rcParams['axes.unicode_minus'] = False   # 正常显示负号
# 读取投票统计数据
data = pd.read_excel(r"harris_vs_trump.xlsx")
cleaned_data = pd.read_csv(r"cleaned_data.csv")
# 添加胜者字段和颜色字段
data["Winner"] = ["Harris" if h > t else "Trump" for h, t in zip(data["Harris support"], data["Trump support"])]
data["Color"] = ["blue" if winner == "Harris" else "red" for winner in data["Winner"]]


def create_race_figure():
    # Define the data
    dt = {
        "Race": ["White", "Black", "Latino", "Asian", "Native American", "Other"],
        "Donald Trump": [0.57, 0.13, 0.46, 0.40, 0.68, 0.52],
        "Kamala Harris": [0.42, 0.86, 0.51, 0.55, 0.31, 0.44]
    }
    # Create a DataFrame
    df = pd.DataFrame(dt)

    # Create a stacked bar chart
    fig = px.bar(
        df,
        x="Race",
        y=["Donald Trump", "Kamala Harris"],
        title="Race Composition and Candidate Preference",
        labels={"value": "Proportion", "variable": "Candidate"},
        barmode="stack"
    )

    fig.update_layout(
        title="Race Composition",
        font=dict(size=10),
        xaxis_title="Race",
        yaxis_title="Proportion"
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
    # Define the data
    da = {
        "Area Type": ["Urban", "Urban", "Suburban", "Suburban", "Rural", "Rural"],
        "Candidate": ["Donald Trump", "Kamala Harris", "Donald Trump", "Kamala Harris", "Donald Trump", "Kamala Harris"],
        "Proportion": [0.38, 0.60, 0.51, 0.47, 0.64, 0.34],
        "Supporters (in millions)": [38, 60, 51, 47, 64, 34]  # Example size values for bubble size
    }

    # Create a DataFrame
    df = pd.DataFrame(da)

    # Create a bubble chart
    fig = px.scatter(
        df,
        x="Area Type",
        y="Proportion",
        size="Supporters (in millions)",  # Bubble size
        color="Candidate",
        title="Area Type Composition of Candidate Support",
        labels={"Proportion": "Proportion of Support", "Supporters (in millions)": "Supporters (millions)"},
        hover_name="Candidate",  # Show candidate name on hover
        size_max=40  # Max bubble size
    )

    # Update layout for better appearance
    fig.update_layout(
        font=dict(size=10),
        xaxis_title="Area Type",
        yaxis_title="Proportion of Support",
        legend_title="Candidate"
    )

    return fig
    
def create_age_gender_figure():
    # Define the data
    data = {
        "Group": ["Men 18-29", "Men 30-44", "Men 45-64", "Men 65 or older", 
                  "Women 18-29", "Women 30-44", "Women 45-64", "Women 65 or older"],
        "Gender": ["Men"] * 4 + ["Women"] * 4,
        "Proportion": [0.49, 0.52, 0.59, 0.56, 0.38, 0.41, 0.50, 0.46],
        "Candidate": ["Donald Trump"] * 8
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Define colors for each group based on the age range
    group_colors = {
        "18-29": "#1f77b4",
        "30-44": "#ff7f0e",
        "45-64": "#2ca02c",
        "65 or older": "#d62728"
    }

    # Extract the age range from the group names and assign colors
    df["Age Range"] = df["Group"].apply(lambda x: " ".join(x.split()[1:]))  # Get age range part
    df["Color"] = df["Age Range"].apply(lambda x: group_colors.get(x, "#000000"))  # Default to black if not found

    # Create pie charts, one for Men and one for Women
    fig = px.pie(
        df,
        names="Group",
        values="Proportion",
        color="Age Range",  # Use Age Range for color
        color_discrete_map=group_colors,  # Ensure correct colors
        facet_col="Gender",  # Split into two pies for Men and Women
        title="Support by Gender and Age Group",
        labels={"Proportion": "Proportion of Support"}
    )

    # Update layout for better appearance
    fig.update_layout(
        font=dict(size=10),
        legend_title="Age Group",
        legend=dict(orientation="h", y=-0.1)
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

def create_fundraising_flow_figure():
    # Prepare the data
    fundraising_data = {
        "Source": ["Individual", "Party", "Other Committee", "Candidate"],
        "Contribution": [
            cleaned_data["Individual_Contribution"].sum(),
            cleaned_data["Party_Committee_Contribution"].sum(),
            cleaned_data["Other_Committee_Contribution"].sum(),
            cleaned_data["Cand_Contribution"].sum()
        ]
    }

    # Create a DataFrame
    df = pd.DataFrame(fundraising_data)

    # Create doughnut chart
    fig = px.pie(
        df,
        names="Source",
        values="Contribution",
        title="候选人筹款来源分布",
        color="Source",
        color_discrete_map={
            "Individual": "#1f77b4",
            "Party": "#ff7f0e",
            "Other Committee": "#2ca02c",
            "Candidate": "#d62728"
        },
        hole=0.3,  # This creates the hole in the center for the doughnut chart
        labels={"Contribution": "Total Contribution"}
    )

    # Update layout for better appearance
    fig.update_layout(
        font=dict(size=12),
        legend_title="筹款来源",
        legend=dict(orientation="h", y=-0.2)
    )

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


def create_us_time_map(state_colors=None):
    if state_colors is None:
        state_colors = {}

    fig = go.Figure()

    # 默认颜色设置（灰色表示无数据）
    default_color = "gray"

    # 遍历州，根据颜色绘制地图
    for state in us.states.STATES:
        color = state_colors.get(state.abbr, default_color)  # 获取州的颜色，默认灰色
        fig.add_trace(go.Choropleth(
            locations=[state.abbr],
            z=[1],  # 伪数据
            locationmode="USA-states",
            colorscale=[[0, color], [1, color]],  # 自定义颜色
            showscale=False  # 隐藏颜色条
        ))

    # 设置地图布局
    fig.update_layout(
        geo=dict(
            scope="usa",
            showlakes=True,
            lakecolor="rgb(255, 255, 255)",  # 湖泊颜色
        ),
        margin={"l": 0, "r": 0, "t": 0, "b": 0}  # 去除多余边距
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
            dbc.Button("实时投票", id="time-button", color="info",style={"display": "block", "margin": "20px auto"}),
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

    html.P(
        "点击顶部横向条形图查看选民形象分析",
        style={"textAlign": "center", "marginTop": "20px", "fontSize": "18px"}
    ),

    html.P(
        "点击地图查看州投票详情",
        style={"textAlign": "center", "marginTop": "20px", "fontSize": "18px"}
    ),

    # 州详情占位符
    html.Div(id="state-detail-container", children=[
        html.Div(id="state_detail", style={"marginTop": "20px", "textAlign": "center", "fontSize": "20px"}),
        html.Div(id="state_map", style={"marginTop": "20px"})
    ]),

    # 主内容占位符
    html.Div(id="main-content")
])

# 修改时间选择器选项
time_switch_layout = html.Div([
    html.H1("实时投票", style={"textAlign": "center"}),

    # 时间选择器
    dcc.Dropdown(
        id="time-dropdown",
        options=[{"label": time, "value": time} for time in
                 ["8:00 a.m.", "8:30 a.m.", "9:00 a.m.", "9:30 a.m.", "10:00 a.m.", 
                  "11:00 a.m.", "12:00 p.m.", "1:00 p.m.", "2:00 p.m."]],
        placeholder="请选择时间点",
        style={"width": "50%", "margin": "20px auto"}
    ),

    # 动态地图
    dcc.Graph(id="time-vote-map", style={"height": "500px"})
])

# Finance 页面布局
finance_layout = html.Div([
    html.H1("候选人筹款分析"),
    dbc.Tabs([
        dbc.Tab(label="各州候选人筹款金额", children=[dcc.Graph(figure=create_state_fundraising_figure())]),
        dbc.Tab(label="候选人筹款来源分布图", children=[dcc.Graph(figure=create_fundraising_flow_figure())]),
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

# 修改后的主布局
app.layout = html.Div([
    dcc.Location(id="page-url", refresh=False),
    html.Div(id="main-layout", children=main_layout, style={"display": "block"}),
    html.Div(id="finance-layout", children=finance_layout, style={"display": "none"}),
    html.Div(id="state-detail-layout", children=state_detail_layout, style={"display": "none"}),
    html.Div(id="tab-layout", children=tab_layout, style={"display": "none"}),
    html.Div(id="time-switch-layout", children=time_switch_layout, style={"display": "none"}),

    # 用于存储每个州的投票状态
    dcc.Store(id="voting-status-store", data={})
])


# 修改回调函数中的 ID
@app.callback(
    [Output("main-layout", "style"),
     Output("finance-layout", "style"),
     Output("state-detail-layout", "style"),
     Output("tab-layout", "style"),
     Output("time-switch-layout", "style")],
    Input("page-url", "pathname")
)
def toggle_pages(pathname):
    if pathname == "/finance":
        return {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}
    elif pathname == "/state-detail":
        return {"display": "none"}, {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "none"}
    elif pathname == "/tab-layout":
        return {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "block"}, {"display": "none"}
    elif pathname == "/time-switch":
        return {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "block"}
    return {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}

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
    Output("time-vote-map", "figure"),
    [Input("time-dropdown", "value"),
     State("voting-status-store", "data")]
)
def update_time_map(selected_time, stored_voting_data):
    if not selected_time:
        print("No time selected, returning default map.")
        return create_us_time_map(stored_voting_data)

    try:
        voting_data = pd.read_excel(r"processed_file.xlsx")
    except Exception as e:
        print(f"Error loading data: {e}")
        return create_us_time_map(stored_voting_data)

    # 筛选当前时间及之前的数据
    valid_times = ["8:00 a.m.", "8:30 a.m.", "9:00 a.m.", "9:30 a.m.", "10:00 a.m.", 
                   "11:00 a.m.", "12:00 p.m.", "1:00 p.m.", "2:00 p.m."]
    valid_times = valid_times[:valid_times.index(selected_time) + 1] if selected_time in valid_times else []

    filtered_data = voting_data[voting_data["Time"].isin(valid_times)]

    # 累积更新 state_colors
    state_colors = stored_voting_data if stored_voting_data else {}
    for _, row in filtered_data.iterrows():
        if row["LeadingCandidate"] == "Trump":
            state_colors[row["State"]] = "red"
        elif row["LeadingCandidate"] == "Harris":
            state_colors[row["State"]] = "blue"

    # 返回更新后的地图
    return create_us_time_map(state_colors)


@app.callback(
    Output("voting-status-store", "data"),
    [Input("time-dropdown", "value"),
     State("voting-status-store", "data")]
)
def save_voting_status(selected_time, stored_voting_data):
    if not selected_time:
        print("No time selected, clearing stored data.")
        return {}

    try:
        voting_data = pd.read_excel(r"processed_file.xlsx")
    except Exception as e:
        print(f"Error loading data: {e}")
        return {}

    # 筛选当前时间及之前的数据
    valid_times = ["8:00 a.m.", "8:30 a.m.", "9:00 a.m.", "9:30 a.m.", "10:00 a.m.", 
                   "11:00 a.m.", "12:00 p.m.", "1:00 p.m.", "2:00 p.m."]
    valid_times = valid_times[:valid_times.index(selected_time) + 1] if selected_time in valid_times else []

    filtered_data = voting_data[voting_data["Time"].isin(valid_times)]

    # 累积更新 state_colors
    state_colors = stored_voting_data if stored_voting_data else {}
    for _, row in filtered_data.iterrows():
        if row["LeadingCandidate"] == "Trump":
            state_colors[row["State"]] = "red"
        elif row["LeadingCandidate"] == "Harris":
            state_colors[row["State"]] = "blue"
    return state_colors

@app.callback(
    Output("page-url", "pathname"),
    [Input("finance-button", "n_clicks"),
     Input("time-button", "n_clicks"),
     Input("us_map", "clickData"),
     Input("vote-bar-chart", "clickData")]
)
def navigate_to_pages(finance_click, time_click, us_map_click, bar_click):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "/"  # 默认返回主页

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "finance-button" and finance_click:
        return "/finance"
    elif triggered_id == "time-button" and time_click:
        return "/time-switch"
    elif triggered_id == "us_map" and us_map_click:
        return "/state-detail"
    elif triggered_id == "vote-bar-chart" and bar_click:
        return "/tab-layout"

    return "/"

if __name__ == "__main__":
    # 使用 Render 提供的端口
    port = int(os.environ.get("PORT", 8050))
    # 绑定到 0.0.0.0
    app.run_server(host="0.0.0.0", port=port)
