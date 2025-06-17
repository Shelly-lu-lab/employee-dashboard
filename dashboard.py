import streamlit as st
import pandas as pd
from pyecharts.charts import Radar, Bar, Pie
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts
from streamlit.components.v1 import html

st.set_page_config(page_title="员工敬业度调研数据分析", layout="wide", page_icon="📊")

# 自定义CSS美化
st.markdown(
    '''
    <style>
    body, .stApp {background: linear-gradient(120deg, #f8fbff 0%, #e9f0fa 100%) !important;}
    .block-container {padding-top: 2rem;}
    .big-title {font-size: 2.5rem; font-weight: 800; color: #22223b; margin-bottom: 0.2em;}
    .subtitle {font-size: 1.1rem; color: #6c757d; margin-bottom: 1.5em;}
    .card {
        background: #fff;
        border-radius: 18px;
        box-shadow: 0 4px 24px 0 rgba(60,72,100,0.08);
        padding: 1.5rem 2rem 1.2rem 2rem;
        margin-bottom: 1.2rem;
    }
    .metric-title {color: #6c757d; font-size: 1.1rem;}
    .metric-value {font-size: 2.2rem; font-weight: 700; color: #22223b;}
    .metric-sub {color: #4caf50; font-size: 1rem;}
    .section-title {font-size: 1.3rem; font-weight: 700; color: #22223b; margin: 1.5em 0 0.5em 0;}
    .stTabs [data-baseweb="tab-list"] {justify-content: center;}
    .stTabs [data-baseweb="tab"] {font-size: 1.1rem; font-weight: 600;}
    </style>
    ''', unsafe_allow_html=True)

# 顶部标题
st.markdown('<div class="big-title">员工敬业度调研数据分析</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Employee Engagement Survey Dashboard</div>', unsafe_allow_html=True)

# 读取数据
overall_df = pd.read_csv('填写率.csv')
conclusion_df = pd.read_csv('结论概览.csv')
dept_df = pd.read_csv('按部门总体.csv')
level_df = pd.read_csv('按职级.csv')
manager_df = pd.read_csv('按管理岗位.csv')

# 顶部卡片区
col1, col2, col3, col4 = st.columns([1.2,1,1,1])
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">总体填写率</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{overall_df["填写率"][0]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-sub">{overall_df["填写人数"][0]}/{overall_df["总体人数"][0]}人</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-sub">↑ {overall_df["对比去年"][0]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">2024年敬业度</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value" style="color:#2196f3">{conclusion_df["24年敬业度"][0]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-sub">较去年提升</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-sub">↑ {int(conclusion_df["24年敬业度"][0].replace("%","")) - int(conclusion_df["23年敬业度"][0].replace("%",""))}%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">2024年满意度</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value" style="color:#7c3aed">{conclusion_df["24年满意度"][0]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-sub">较去年提升</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-sub">↑ {int(conclusion_df["24年满意度"][0].replace("%","")) - int(conclusion_df["23年满意度"][0].replace("%",""))}%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">去年敬业度</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value" style="color:#61677c">{conclusion_df["23年敬业度"][0]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-sub">2023年数据</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Tab区块
section = st.tabs(["部门分析", "岗位对比", "职级分析", "数据洞察"])

with section[0]:
    st.markdown('<div class="section-title">部门维度分析</div>', unsafe_allow_html=True)
    dept_select = st.selectbox("选择部门", dept_df['一级组织'].dropna().unique(), key="dept_select")
    sub_df = dept_df[dept_df['一级组织'] == dept_select]
    # 条形图：部门敬业度&满意度
    bar = (
        Bar()
        .add_xaxis(["敬业度", "满意度"])
        .add_yaxis(dept_select, [float(sub_df['敬业度'].iloc[0].replace('%','')), float(sub_df['满意度'].iloc[0].replace('%',''))], color="#2196f3")
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"{dept_select} 敬业度&满意度", pos_left="center", title_textstyle_opts=opts.TextStyleOpts(font_size=16)),
            legend_opts=opts.LegendOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(max_=100)
        )
    )
    st_pyecharts(bar, height=320)
    # 蛛网图
    detail_cols = dept_df.columns[6:-4]
    radar_data = sub_df[detail_cols].astype(str).replace('%','',regex=True).astype(float).mean().tolist()
    radar_schema = [opts.RadarIndicatorItem(name=col, max_=100) for col in detail_cols]
    radar = (
        Radar()
        .add_schema(schema=radar_schema, shape="circle", splitarea_opt=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(color="#f3f6fd")))
        .add(dept_select, [radar_data], color="#7c3aed")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title=f"{dept_select} 维度达成蛛网图", pos_left="center", title_textstyle_opts=opts.TextStyleOpts(font_size=16)))
    )
    st_pyecharts(radar, height=350)
    # 四类员工占比
    st.markdown('<div class="section-title">四类员工占比</div>', unsafe_allow_html=True)
    ratio_cols = ['高效-敬业且满意','受挫-敬业不满意','漠然-不敬业满意','低效-不敬业不满意']
    ratio_data = sub_df[ratio_cols].astype(str).replace('%','',regex=True).astype(float).mean().tolist()
    pie = (
        Pie()
        .add("", [list(z) for z in zip(ratio_cols, ratio_data)], radius=["40%","70%"])
        .set_global_opts(title_opts=opts.TitleOpts(title=f"{dept_select} 四类员工占比", pos_left="center", title_textstyle_opts=opts.TextStyleOpts(font_size=16)), legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    )
    st_pyecharts(pie, height=350)

with section[1]:
    st.markdown('<div class="section-title">管理岗与非管理岗对比</div>', unsafe_allow_html=True)
    bar1 = (
        Bar()
        .add_xaxis(["敬业度", "满意度"])
        .add_yaxis("管理岗位", [int(manager_df['敬业度'][0].replace('%','')), int(manager_df['满意度'][0].replace('%',''))], color="#2196f3")
        .add_yaxis("非管理岗位", [int(manager_df['敬业度'][1].replace('%','')), int(manager_df['满意度'][1].replace('%',''))], color="#7c3aed")
        .set_global_opts(title_opts=opts.TitleOpts(title="管理岗/非管理岗 敬业度满意度对比", pos_left="center", title_textstyle_opts=opts.TextStyleOpts(font_size=16)), yaxis_opts=opts.AxisOpts(max_=100))
    )
    st_pyecharts(bar1, height=350)

with section[2]:
    st.markdown('<div class="section-title">职级对比</div>', unsafe_allow_html=True)
    bar2 = (
        Bar()
        .add_xaxis(["敬业度", "满意度"])
        .add_yaxis("3和4职级", [int(level_df['敬业度'][0].replace('%','')), int(level_df['满意度'][0].replace('%',''))], color="#2196f3")
        .add_yaxis("1和2职级", [int(level_df['敬业度'][1].replace('%','')), int(level_df['满意度'][1].replace('%',''))], color="#7c3aed")
        .set_global_opts(title_opts=opts.TitleOpts(title="高低职级 敬业度满意度对比", pos_left="center", title_textstyle_opts=opts.TextStyleOpts(font_size=16)), yaxis_opts=opts.AxisOpts(max_=100))
    )
    st_pyecharts(bar2, height=350)

with section[3]:
    st.markdown('<div class="section-title">数据洞察</div>', unsafe_allow_html=True)
    insights = []
    if int(conclusion_df['24年敬业度'][0].replace('%','')) > int(conclusion_df['23年敬业度'][0].replace('%','')):
        insights.append(f"2024年敬业度较去年提升了{int(conclusion_df['24年敬业度'][0].replace('%','')) - int(conclusion_df['23年敬业度'][0].replace('%',''))}个百分点。")
    if int(conclusion_df['24年满意度'][0].replace('%','')) > int(conclusion_df['23年满意度'][0].replace('%','')):
        insights.append(f"2024年满意度较去年提升了{int(conclusion_df['24年满意度'][0].replace('%','')) - int(conclusion_df['23年满意度'][0].replace('%',''))}个百分点。")
    if int(manager_df['敬业度'][0].replace('%','')) > int(manager_df['敬业度'][1].replace('%','')):
        insights.append("管理岗位的敬业度高于非管理岗位。")
    if int(manager_df['满意度'][0].replace('%','')) > int(manager_df['满意度'][1].replace('%','')):
        insights.append("管理岗位的满意度高于非管理岗位。")
    if int(level_df['敬业度'][0].replace('%','')) > int(level_df['敬业度'][1].replace('%','')):
        insights.append("高职级员工的敬业度高于低职级员工。")
    if int(level_df['满意度'][0].replace('%','')) > int(level_df['满意度'][1].replace('%','')):
        insights.append("高职级员工的满意度高于低职级员工。")
    if not insights:
        st.info("暂无明显洞察。")
    for i, ins in enumerate(insights):
        st.success(f"{i+1}. {ins}")

st.markdown('<div style="text-align:center;color:#b0b3c6;margin-top:2em;">© 2024 员工敬业度调研Dashboard | Powered by Streamlit & Pyecharts</div>', unsafe_allow_html=True) 