import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体
plt.rcParams['axes.unicode_minus'] = False   # 正常显示负号


# 加载数据
cleaned_data = pd.read_csv(r"cleaned_data.csv")

# 分段数据处理
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

# 创建分段颜色地图
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
fig.show()

# Sankey 图
fig = go.Figure(
    data=[
        go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=["Individual", "Party", "Other Committee", "Candidate", "Total"],
                color=["blue", "green", "orange", "purple", "red"]
            ),
            link=dict(
                source=[0, 1, 2, 3],  # 来源节点
                target=[4, 4, 4, 4],  # 目标节点
                value=[
                    cleaned_data["Individual_Contribution"].sum(),
                    cleaned_data["Party_Committee_Contribution"].sum(),
                    cleaned_data["Other_Committee_Contribution"].sum(),
                    cleaned_data["Cand_Contribution"].sum()
                ],
                color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
            )
        )
    ]
)

fig.update_layout(title_text="候选人筹款来源流向图", font_size=12)
fig.show()

fig = px.box(
    cleaned_data,
    x="Cand_Party_Affiliation",  # 政党
    y="Total_Receipt",  # 筹款金额
    color="Cand_Party_Affiliation",
    title="不同政党候选人筹款分布箱线图",
    labels={"Cand_Party_Affiliation": "政党", "Total_Receipt": "筹款金额"}
)
fig.show()



# 计算相关性矩阵
correlation_matrix = cleaned_data[["Total_Receipt", "Total_Disbursement", "Cash_On_Hand_COP"]].corr()

# 绘制热力图
plt.figure(figsize=(8, 6))
sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    linewidths=0.5
)
plt.title("候选人筹款与支出相关性热力图")
plt.show()

fig = px.scatter_3d(
    cleaned_data,
    x="Total_Receipt",  # 筹款金额
    y="Total_Disbursement",  # 支出金额
    z="Debt_Owed_By_Committee",  # 债务金额
    color="Cand_Party_Affiliation",  # 按政党分色
    hover_name="Cand_Name",  # 悬停显示候选人名称
    title="候选人筹款、支出与债务三维分析"
)
fig.show()


