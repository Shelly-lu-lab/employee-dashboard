import streamlit as st
import pandas as pd
from pyecharts.charts import Radar, Bar, Pie
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts

# 页面配置
st.set_page_config(
    page_title="员工敬业度调研数据分析",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="collapsed"
)

# 自定义CSS样式
st.markdown("""
<style>
    /* 全局样式 */
    .stApp {
        background: linear-gradient(135deg, #f8f9fe 0%, #f1f4f9 100%);
    }
    .block-container {
        padding-top: 2rem;
        padding-right: 3rem;
        padding-left: 3rem;
    }
    
    /* 标题样式 */
    .main-title {
        font-family: "SF Pro Display", "PingFang SC", "Microsoft YaHei", sans-serif;
        font-size: 2.2rem;
        font-weight: 600;
        color: #1a1f36;
        margin-bottom: 0.2rem;
        padding-left: 0.5rem;
    }
    .sub-title {
        font-size: 1rem;
        color: #697386;
        margin-bottom: 2rem;
        padding-left: 0.5rem;
    }
    
    /* 卡片样式 */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.8);
        margin-bottom: 1rem;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #697386;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 600;
        color: #1a1f36;
        margin-bottom: 0.3rem;
    }
    .metric-delta {
        font-size: 0.9rem;
        color: #2ecc71;
        display: flex;
        align-items: center;
        gap: 0.2rem;
    }
    
    /* 部分样式 */
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a1f36;
        margin: 2rem 0 1rem 0;
        padding-left: 0.5rem;
    }
    
    /* Tab样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        padding: 0 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 0;
        font-weight: 500;
        font-size: 0.95rem;
    }
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background: #4c6ef5;
        border-radius: 3px;
    }
    
    /* 选择器样式 */
    .stSelectbox [data-baseweb="select"] {
        background: white;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    /* 隐藏Streamlit默认样式 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 读取数据
overall_df = pd.read_csv('填写率.csv')
conclusion_df = pd.read_csv('结论概览.csv')
dept_df = pd.read_csv('按部门总体.csv')
level_df = pd.read_csv('按职级.csv')
manager_df = pd.read_csv('按管理岗位.csv')

# 标题
st.markdown('<div class="main-title">员工敬业度调研数据分析</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Employee Engagement Survey Dashboard</div>', unsafe_allow_html=True)

# 顶部指标卡片
col1, col2, col3, col4 = st.columns([1.2,1,1,1])

with col1:
    st.markdown('''
        <div class="metric-card">
            <div class="metric-label">总体填写率</div>
            <div class="metric-value">{}</div>
            <div style="font-size: 0.9rem; color: #697386; margin-bottom: 0.3rem;">{}/{} 人</div>
            <div class="metric-delta">↑ {}</div>
        </div>
    '''.format(
        overall_df['填写率'][0],
        overall_df['填写人数'][0],
        overall_df['总体人数'][0],
        overall_df['对比去年'][0]
    ), unsafe_allow_html=True)

with col2:
    st.markdown('''
        <div class="metric-card">
            <div class="metric-label">2024年敬业度</div>
            <div class="metric-value" style="color: #4c6ef5">{}</div>
            <div class="metric-delta">↑ {}%</div>
        </div>
    '''.format(
        conclusion_df['24年敬业度'][0],
        int(conclusion_df['24年敬业度'][0].replace('%','')) - int(conclusion_df['23年敬业度'][0].replace('%',''))
    ), unsafe_allow_html=True)

with col3:
    st.markdown('''
        <div class="metric-card">
            <div class="metric-label">2024年满意度</div>
            <div class="metric-value" style="color: #7950f2">{}</div>
            <div class="metric-delta">↑ {}%</div>
        </div>
    '''.format(
        conclusion_df['24年满意度'][0],
        int(conclusion_df['24年满意度'][0].replace('%','')) - int(conclusion_df['23年满意度'][0].replace('%',''))
    ), unsafe_allow_html=True)

with col4:
    st.markdown('''
        <div class="metric-card">
            <div class="metric-label">去年敬业度</div>
            <div class="metric-value" style="color: #868e96">{}</div>
            <div style="font-size: 0.9rem; color: #697386;">2023年数据</div>
        </div>
    '''.format(conclusion_df['23年敬业度'][0]), unsafe_allow_html=True)

# 创建标签页
tab1, tab2, tab3, tab4 = st.tabs(["📊 部门分析", "👥 岗位对比", "📈 职级分析", "💡 数据洞察"])

with tab1:
    st.markdown('<div class="section-title">部门维度分析</div>', unsafe_allow_html=True)
    dept_select = st.selectbox("选择部门", dept_df['一级组织'].dropna().unique())
    sub_df = dept_df[dept_df['一级组织'] == dept_select]

    # 部门敬业度&满意度条形图
    bar = (
        Bar()
        .add_xaxis(["敬业度", "满意度"])
        .add_yaxis(
            dept_select,
            [float(sub_df['敬业度'].iloc[0].replace('%','')), 
             float(sub_df['满意度'].iloc[0].replace('%',''))],
            color="#4c6ef5",
            category_gap="50%"
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=f"{dept_select}敬业度&满意度",
                subtitle="单位：%",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=16,
                    color="#1a1f36"
                )
            ),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(color="#697386")
            ),
            yaxis_opts=opts.AxisOpts(
                max_=100,
                axislabel_opts=opts.LabelOpts(color="#697386")
            )
        )
    )
    st_pyecharts(bar, height=300)

    # 蛛网图
    detail_cols = dept_df.columns[6:-4]
    radar_data = sub_df[detail_cols].astype(str).replace('%','',regex=True).astype(float).mean().tolist()
    radar_schema = [opts.RadarIndicatorItem(name=col, max_=100) for col in detail_cols]
    radar = (
        Radar()
        .add_schema(
            schema=radar_schema,
            shape="circle",
            splitarea_opt=opts.SplitAreaOpts(
                is_show=True,
                areastyle_opts=opts.AreaStyleOpts(opacity=0.1)
            ),
            axisline_opt=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#e9ecef")),
            splitline_opt=opts.SplitLineOpts(linestyle_opts=opts.LineStyleOpts(color="#e9ecef"))
        )
        .add(
            dept_select,
            [radar_data],
            linestyle_opts=opts.LineStyleOpts(width=2),
            areastyle_opts=opts.AreaStyleOpts(opacity=0.3),
            color="#7950f2"
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=f"{dept_select}维度达成蛛网图",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=16,
                    color="#1a1f36"
                )
            )
        )
    )
    st_pyecharts(radar, height=500)

    # 四类员工占比
    st.markdown('<div class="section-title">四类员工占比</div>', unsafe_allow_html=True)
    ratio_cols = ['高效-敬业且满意','受挫-敬业不满意','漠然-不敬业满意','低效-不敬业不满意']
    ratio_data = sub_df[ratio_cols].astype(str).replace('%','',regex=True).astype(float).mean().tolist()
    colors = ["#4c6ef5", "#51cf66", "#fcc419", "#ff6b6b"]
    pie = (
        Pie()
        .add(
            "",
            [list(z) for z in zip(ratio_cols, ratio_data)],
            radius=["40%", "70%"],
            center=["50%", "50%"],
            itemstyle_opts=opts.ItemStyleOpts(border_color="#fff", border_width=2)
        )
        .set_colors(colors)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=f"{dept_select}四类员工占比",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=16,
                    color="#1a1f36"
                )
            ),
            legend_opts=opts.LegendOpts(
                orient="vertical",
                pos_left="right",
                pos_top="center",
                textstyle_opts=opts.TextStyleOpts(color="#697386")
            )
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(
                formatter="{b}: {d}%",
                color="#697386"
            )
        )
    )
    st_pyecharts(pie, height=400)

with tab2:
    st.markdown('<div class="section-title">管理岗与非管理岗对比</div>', unsafe_allow_html=True)
    bar1 = (
        Bar()
        .add_xaxis(["敬业度", "满意度"])
        .add_yaxis(
            "管理岗位",
            [int(manager_df['敬业度'][0].replace('%','')),
             int(manager_df['满意度'][0].replace('%',''))],
            color="#4c6ef5"
        )
        .add_yaxis(
            "非管理岗位",
            [int(manager_df['敬业度'][1].replace('%','')),
             int(manager_df['满意度'][1].replace('%',''))],
            color="#7950f2"
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="管理岗/非管理岗 敬业度满意度对比",
                subtitle="单位：%",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=16,
                    color="#1a1f36"
                )
            ),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(color="#697386")
            ),
            yaxis_opts=opts.AxisOpts(
                max_=100,
                axislabel_opts=opts.LabelOpts(color="#697386")
            ),
            legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="#697386"))
        )
    )
    st_pyecharts(bar1, height=400)

with tab3:
    st.markdown('<div class="section-title">职级对比</div>', unsafe_allow_html=True)
    bar2 = (
        Bar()
        .add_xaxis(["敬业度", "满意度"])
        .add_yaxis(
            "3和4职级",
            [int(level_df['敬业度'][0].replace('%','')),
             int(level_df['满意度'][0].replace('%',''))],
            color="#4c6ef5"
        )
        .add_yaxis(
            "1和2职级",
            [int(level_df['敬业度'][1].replace('%','')),
             int(level_df['满意度'][1].replace('%',''))],
            color="#7950f2"
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="高低职级 敬业度满意度对比",
                subtitle="单位：%",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=16,
                    color="#1a1f36"
                )
            ),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(color="#697386")
            ),
            yaxis_opts=opts.AxisOpts(
                max_=100,
                axislabel_opts=opts.LabelOpts(color="#697386")
            ),
            legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="#697386"))
        )
    )
    st_pyecharts(bar2, height=400)

with tab4:
    st.markdown('<div class="section-title">数据洞察</div>', unsafe_allow_html=True)
    insights = []
    if int(conclusion_df['24年敬业度'][0].replace('%','')) > int(conclusion_df['23年敬业度'][0].replace('%','')):
        insights.append(f"2024年敬业度较去年提升了{int(conclusion_df['24年敬业度'][0].replace('%','')) - int(conclusion_df['23年敬业度'][0].replace('%',''))}个百分点")
    if int(conclusion_df['24年满意度'][0].replace('%','')) > int(conclusion_df['23年满意度'][0].replace('%','')):
        insights.append(f"2024年满意度较去年提升了{int(conclusion_df['24年满意度'][0].replace('%','')) - int(conclusion_df['23年满意度'][0].replace('%',''))}个百分点")
    if int(manager_df['敬业度'][0].replace('%','')) > int(manager_df['敬业度'][1].replace('%','')):
        insights.append("管理岗位的敬业度高于非管理岗位")
    if int(manager_df['满意度'][0].replace('%','')) > int(manager_df['满意度'][1].replace('%','')):
        insights.append("管理岗位的满意度高于非管理岗位")
    if int(level_df['敬业度'][0].replace('%','')) > int(level_df['敬业度'][1].replace('%','')):
        insights.append("高职级员工的敬业度高于低职级员工")
    if int(level_df['满意度'][0].replace('%','')) > int(level_df['满意度'][1].replace('%','')):
        insights.append("高职级员工的满意度高于低职级员工")

    for i, insight in enumerate(insights, 1):
        st.markdown(f'''
            <div style="
                background: white;
                padding: 1rem 1.2rem;
                border-radius: 8px;
                margin-bottom: 0.8rem;
                border: 1px solid #e9ecef;
                color: #1a1f36;
                font-size: 0.95rem;
            ">
                {i}. {insight}
            </div>
        ''', unsafe_allow_html=True)

# 页脚
st.markdown('''
    <div style="
        text-align: center;
        color: #697386;
        padding: 2rem 0;
        font-size: 0.9rem;
    ">
        © 2024 员工敬业度调研Dashboard | Powered by Streamlit & Pyecharts
    </div>
''', unsafe_allow_html=True) 