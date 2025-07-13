import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.font_manager import FontProperties
import matplotlib
from datetime import datetime
import base64
from io import BytesIO
from fpdf import FPDF
import tempfile
import time

# 設置頁面配置
st.set_page_config(
    page_title="投資風險評估問卷",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 設置 Seaborn 風格
sns.set(style="whitegrid")
sns.set_context("talk")

# 設置中文字體支援
try:
    matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 'DejaVu Sans']
    matplotlib.rcParams['axes.unicode_minus'] = False
except:
    pass

# 側邊欄 - 主題選擇
with st.sidebar:
    
    
    # 顯示關於評估方法的資訊
    st.title("評估方法說明")
    with st.expander("評估方法學詳情"):
        st.write("""
        本評估系統基於現代投資理論原則設計，考量四個關鍵維度：財務狀況、投資經驗、投資目標和風險心理承受度。

        評分機制採用加權計算法，根據每個維度的重要性賦予不同權重：
        - 財務狀況: 25%
        - 投資經驗: 20%
        - 投資目標: 20%
        - 風險心理承受度: 35%

        最終風險評分在0-100分之間，根據得分將投資者分為五種風險類型：保守型、穩健型、平衡型、成長型和積極型。
        """)
    
    # 提供教育資源
    st.subheader("學習資源")
    st.markdown("課程內容涵蓋：")
    st.markdown("- 基礎投資知識與策略")
    st.markdown("- 資產配置原則")
    st.markdown("- 風險管理技巧")
    st.markdown("- 市場分析方法")
    st.markdown("""
### 📢 免責聲明
本系統僅供學術研究與教育用途，AI 提供的數據與分析結果僅供參考，**不構成投資建議或財務建議**。
請使用者自行判斷投資決策，並承擔相關風險。本系統作者不對任何投資行為負責，亦不承擔任何損失責任。
""")

# 設置主題顏色

primary_color = "#1E88E5"
secondary_color = "#26A69A"
background_color = "#FFFFFF"
text_color = "#212121"
chart_palette = "viridis"

# 應用自定義 CSS
st.markdown(f"""
<style>
    .main .block-container {{
        background-color: {background_color};
        color: {text_color};
        padding: 2rem;
        border-radius: 10px;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {primary_color} !important;
    }}
    .stButton>button {{
        background-color: {primary_color};
        color: white;
    }}
    .stProgress .st-bo {{
        background-color: {secondary_color};
    }}
    .reportview-container .sidebar-content {{
        background-color: {background_color};
    }}
    .css-1aumxhk {{
        background-color: {background_color};
    }}
</style>
""", unsafe_allow_html=True)

# 定義專業術語解釋功能
def term_tooltip(term, explanation):
    """創建帶有解釋的術語工具提示"""
    return f"""
    <span title="{explanation}" style="text-decoration: underline dotted; cursor: help;">{term}</span>
    """

# 設置頁面標題
st.title('投資風險評估問卷')
st.write('請回答以下問題，以評估您的投資風險承受能力')

# 初始化會話狀態變量 (用於儲存評估完成後的結果)
if 'assessment_complete' not in st.session_state:
    st.session_state.assessment_complete = False
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'results' not in st.session_state:
    st.session_state.results = {}

# 創建進度條
progress_bar = st.progress(0)
progress_text = st.empty()

# 創建表單
with st.form("risk_assessment_form"):
    total_questions = 20  # 總問題數
    current_question = 0
    
    # A. 財務狀況
    st.header('財務狀況')
    st.markdown('評估您的財務基礎穩定度與彈性')

    # A1. 收入穩定性
    income_stability = st.radio(
        "1. 您的主要收入來源是？", 
        ["固定薪資", "自由業/彈性收入", "投資收益", "無固定收入"],
        help="此問題評估您收入來源的穩定性，影響風險承受能力"
    )
    

    # A2. 應急資金
    emergency_fund = st.radio(
        "2. 您目前的應急資金可以維持幾個月的生活開支？", 
        ["6個月以上", "3-6個月", "1-3個月", "不到1個月"],
        help="應急資金是指在沒有收入的情況下能夠支付生活開支的儲備金"
    )
    

    # A3. 負債比例
    debt_ratio = st.radio(
        "3. 您的負債對收入比例為？", 
        ["無負債", "低於30%", "30%-50%", "50%以上"],
        help="負債比例是月負債還款除以月收入的百分比，用來衡量財務負擔程度"
    )
    

    # A4. 財務義務
    financial_obligations = st.multiselect(
        "4. 您目前的財務責任？(可多選)",
        ["無重大財務責任", "房貸/車貸", "教育支出", "家庭撫養責任"],
        help="了解您當前的財務責任可以評估您的財務彈性和風險承受能力"
    )
    

    # A5. 資產配置現況
    asset_allocation = st.radio(
        "5. 您目前的資產配置是？",
        ["主要為現金/存款", "平均分配於現金與投資", "主要為投資"],
        help="您當前的資產分配反映了您對風險的初步態度"
    )
    

    # B. 投資經驗
    st.header('投資經驗')
    st.markdown('評估您的投資知識和實際經驗')

    # B1. 投資年資
    investment_years = st.radio(
        "1. 您有多少年投資經驗？",
        ["5年以上", "3-5年", "1-3年", "1年以下或無經驗"],
        help="投資經驗年限可以反映您對市場的熟悉程度"
    )
    

    # B2. 投資知識
    investment_knowledge = st.multiselect(
        "2. 您對以下哪些投資工具有了解？(可多選)",
        ["股票", "債券", "ETF", "期貨/選擇權", "外匯"],
        help="對各種投資工具的了解程度反映您的投資知識廣度"
    )
    

    # B3. 交易頻率
    trading_frequency = st.radio(
        "3. 您多久檢視並調整您的投資組合？",
        ["每日", "每週", "每月", "每季或更少"],
        help="檢視和調整投資組合的頻率反映了您的投資參與度"
    )
    

    # B4. 投資規模
    investment_scale = st.radio(
        "4. 您的投資金額占總資產的比例是？",
        ["10%以下", "10%-30%", "30%-50%", "50%以上"],
        help="投資比例反映了您將資產用於投資的意願"
    )
    

    # C. 投資目標
    st.header('投資目標')
    st.markdown('了解您的投資時間期限與期望')

    # C1. 投資期限
    investment_horizon = st.radio(
        "1. 您計劃的投資時間範圍是？",
        ["10年以上", "5-10年", "1-5年", "1年以下"],
        help="投資期限越長，通常能承受的風險越高"
    )
    

    # C2. 投資目的
    investment_purpose = st.radio(
        "2. 您投資的主要目的是？(選最重要的一項)",
        ["保本為主", "穩定收入", "資本增值", "追求高報酬"],
        help="投資目的反映了您對風險和回報的偏好"
    )
    

    # C3. 資金需求
    fund_requirement = st.radio(
        "3. 在未來5年內，您可能需要動用這筆投資的比例？",
        ["0%", "25%以下", "25%-50%", "50%以上"],
        help="流動性需求會影響適合的投資選擇和風險水平"
    )
    

    # C4. 預期報酬率
    expected_return = st.radio(
        "4. 您期望的年化投資報酬率是？",
        ["3%以下", "3%-8%", "8%-15%", "15%以上"],
        help="較高的報酬率通常伴隨著較高的風險"
    )
    

    # D. 風險心理承受度
    st.header('風險心理承受度')
    st.markdown('評估您面對市場波動的心理反應')

    # D1. 市場下跌反應
    market_drop_reaction = st.radio(
        "1. 如果您的投資在短期內虧損20%，您會？",
        ["立即賣出止損", "賣出部分持倉", "持有不動", "加碼買入"],
        help="對市場下跌的反應反映您的風險承受心理"
    )
    

    # D2. 損失承受度
    loss_tolerance = st.radio(
        "2. 您能接受的最大投資損失比例是？",
        ["5%以下", "5%-15%", "15%-30%", "30%以上"],
        help="能接受的最大損失直接反映風險承受能力"
    )
    

    # D3. 選擇情境題
    scenario_choice = st.radio(
        "3. 兩個投資選擇：A有80%機會獲利10%，B有40%機會獲利25%。您選擇？",
        ["A選項", "B選項"],
        help="此題測試您對風險與報酬取捨的偏好"
    )
    

    # D4. 波動接受度
    volatility_acceptance = st.radio(
        "4. 您對投資價值波動的接受程度是？",
        ["希望完全穩定", "接受小幅波動", "能接受適度波動", "可以承受大幅波動"],
        help="對價值波動的接受程度是風險承受能力的重要指標"
    )
    

    # D5. 投資理念
    investment_philosophy = st.radio(
        "5. 以下哪項最符合您的投資理念？",
        ["安全第一，寧願低報酬也要低風險", "希望在安全與報酬間取得平衡", "願意承擔更多風險以獲取更高報酬"],
        help="投資理念反映您對風險和回報的整體態度"
    )
    

    # D6. 行為金融學測試
    behavioral_finance = st.radio(
        "6. 在一次市場大幅修正中，您的投資已經下跌12%。此時您會：",
        ["賣出部分持股，將剩餘資金轉向低風險資產", "利用手中現金加碼買入，期望在市場反彈時獲得更大收益"],
        help="此題測試您在虧損情況下的風險傾向"
    )
    

    # D7. 投資決策方式
    decision_making = st.radio(
        "7. 您的投資決策通常基於？",
        ["情緒和直覺", "他人建議", "基本面和技術分析結合", "系統化策略和數據分析"],
        help="決策方式反映您的投資紀律和系統性"
    )
    
    
    # 提交按鈕
    submitted = st.form_submit_button("提交問卷")

# 當表單提交時進行評分計算
if submitted:
    # 保存用戶回答
    st.session_state.user_answers = {
        "收入穩定性": income_stability,
        "應急資金": emergency_fund,
        "負債比例": debt_ratio,
        "財務責任": ", ".join(financial_obligations) if financial_obligations else "無選擇",
        "資產配置": asset_allocation,
        "投資年資": investment_years,
        "投資知識": ", ".join(investment_knowledge) if investment_knowledge else "無選擇",
        "交易頻率": trading_frequency,
        "投資規模": investment_scale,
        "投資期限": investment_horizon,
        "投資目的": investment_purpose,
        "資金需求": fund_requirement,
        "預期報酬率": expected_return,
        "市場下跌反應": market_drop_reaction,
        "損失承受度": loss_tolerance,
        "風險偏好情境選擇": scenario_choice,
        "波動接受度": volatility_acceptance,
        "投資理念": investment_philosophy,
        "行為金融學測試": behavioral_finance,
        "投資決策方式": decision_making
    }
    
    # A. 財務狀況評分計算
    a1_score = {"固定薪資": 5, "自由業/彈性收入": 3, "投資收益": 2, "無固定收入": 0}[income_stability]
    a2_score = {"6個月以上": 5, "3-6個月": 3, "1-3個月": 1, "不到1個月": 0}[emergency_fund]
    a3_score = {"無負債": 5, "低於30%": 4, "30%-50%": 2, "50%以上": 0}[debt_ratio]
    
    # A4需要特殊處理（多選題）
    a4_score = 0
    if "無重大財務責任" in financial_obligations:
        a4_score = 5
    else:
        if "房貸/車貸" in financial_obligations:
            a4_score -= 2
        if "教育支出" in financial_obligations:
            a4_score -= 1
        if "家庭撫養責任" in financial_obligations:
            a4_score -= 2
    # 確保A4分數不低於0
    a4_score = max(0, a4_score)
    
    a5_score = {"主要為現金/存款": 1, "平均分配於現金與投資": 3, "主要為投資": 5}[asset_allocation]
    
    # 計算財務狀況總分（標準化為0-100）
    financial_max_score = 25  # 最大可能得分
    financial_score = (a1_score + a2_score + a3_score + a4_score + a5_score) / financial_max_score * 100
    
    # B. 投資經驗評分計算
    b1_score = {"5年以上": 5, "3-5年": 4, "1-3年": 2, "1年以下或無經驗": 0}[investment_years]
    
    # B2需要特殊處理（多選題）
    b2_score = len(investment_knowledge)  # 每選一項得1分
    
    b3_score = {"每日": 5, "每週": 4, "每月": 3, "每季或更少": 1}[trading_frequency]
    b4_score = {"10%以下": 1, "10%-30%": 2, "30%-50%": 3, "50%以上": 5}[investment_scale]
    
    # 計算投資經驗總分（標準化為0-100）
    experience_max_score = 20  # 最大可能得分，B2最高可得5分
    experience_score = (b1_score + min(b2_score, 5) + b3_score + b4_score) / experience_max_score * 100
    
    # C. 投資目標評分計算
    c1_score = {"10年以上": 5, "5-10年": 4, "1-5年": 2, "1年以下": 0}[investment_horizon]
    c2_score = {"保本為主": 1, "穩定收入": 2, "資本增值": 4, "追求高報酬": 5}[investment_purpose]
    c3_score = {"0%": 5, "25%以下": 3, "25%-50%": 2, "50%以上": 0}[fund_requirement]
    c4_score = {"3%以下": 1, "3%-8%": 3, "8%-15%": 4, "15%以上": 5}[expected_return]
    
    # 計算投資目標總分（標準化為0-100）
    goal_max_score = 20  # 最大可能得分
    goal_score = (c1_score + c2_score + c3_score + c4_score) / goal_max_score * 100
    
    # D. 風險心理承受度評分計算
    d1_score = {"立即賣出止損": 0, "賣出部分持倉": 1, "持有不動": 3, "加碼買入": 5}[market_drop_reaction]
    d2_score = {"5%以下": 1, "5%-15%": 2, "15%-30%": 4, "30%以上": 5}[loss_tolerance]
    d3_score = {"A選項": 2, "B選項": 4}[scenario_choice]
    d4_score = {"希望完全穩定": 0, "接受小幅波動": 2, "能接受適度波動": 3, "可以承受大幅波動": 5}[volatility_acceptance]
    d5_score = {"安全第一，寧願低報酬也要低風險": 1, "希望在安全與報酬間取得平衡": 3, "願意承擔更多風險以獲取更高報酬": 5}[investment_philosophy]
    d6_score = {"賣出部分持股，將剩餘資金轉向低風險資產": 2, "利用手中現金加碼買入，期望在市場反彈時獲得更大收益": 4}[behavioral_finance]
    d7_score = {"情緒和直覺": 1, "他人建議": 2, "基本面和技術分析結合": 4, "系統化策略和數據分析": 5}[decision_making]
    
    # 計算風險心理承受度總分（標準化為0-100）
    psychology_max_score = 35  # 最大可能得分
    psychology_score = (d1_score + d2_score + d3_score + d4_score + d5_score + d6_score + d7_score) / psychology_max_score * 100
    
    # 根據權重計算最終得分
    final_score = (financial_score * 0.25 + experience_score * 0.20 + goal_score * 0.20 + psychology_score * 0.35)
    
    # 風險承受能力分類
    if final_score <= 40:
        risk_profile = "保守型"
        description = "您偏好低風險投資，以保本為主要考量。"
        color = "#4575b4"  # 藍色，代表保守
    elif final_score <= 60:
        risk_profile = "穩健型"
        description = "您偏好中低風險投資，追求收益與安全的平衡。"
        color = "#74add1"  # 淺藍色，代表中低風險
    elif final_score <= 75:
        risk_profile = "平衡型"
        description = "您能接受中等風險，追求成長與穩定的平衡。"
        color = "#46b337"  # 綠色，代表中等風險
    elif final_score <= 90:
        risk_profile = "成長型"
        description = "您偏好中高風險投資，注重資產增值。"
        color = "#fdae61"  # 橙色，代表中高風險
    else:
        risk_profile = "積極型"
        description = "您能接受高風險投資，以追求最大化報酬為目標。"
        color = "#d73027"  # 紅色，代表高風險
    
    # 保存結果到會話狀態
    st.session_state.results = {
        "financial_score": financial_score,
        "experience_score": experience_score,
        "goal_score": goal_score,
        "psychology_score": psychology_score,
        "final_score": final_score,
        "risk_profile": risk_profile,
        "description": description,
        "color": color,
        "assessment_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 標記評估已完成
    st.session_state.assessment_complete = True
    
    # 重新載入頁面以顯示結果
    st.experimental_rerun()

# 如果評估已完成，顯示結果
if st.session_state.assessment_complete:
    # 清除進度條和表單
    progress_bar.empty()
    progress_text.empty()
    
    # 獲取結果
    financial_score = st.session_state.results["financial_score"]
    experience_score = st.session_state.results["experience_score"] 
    goal_score = st.session_state.results["goal_score"]
    psychology_score = st.session_state.results["psychology_score"]
    final_score = st.session_state.results["final_score"]
    risk_profile = st.session_state.results["risk_profile"]
    description = st.session_state.results["description"]
    color = st.session_state.results["color"]
    assessment_date = st.session_state.results["assessment_date"]
    
    # 顯示結果
    st.header("風險評估結果")
    st.subheader(f"您的風險承受類型: {risk_profile}")
    st.markdown(f"<div style='background-color:{color}; padding:10px; border-radius:5px; color:white;'>{description}</div>", unsafe_allow_html=True)
    st.write(f"綜合風險評分: {final_score:.2f}/100")
    st.write(f"評估日期: {assessment_date}")
    
    # 使用整行寬度顯示儀表盤
    # 使用 Plotly 創建互動式儀表盤
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = final_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "風險承受能力指數", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#4575b4', 'name': '保守型'},
                {'range': [40, 60], 'color': '#74add1', 'name': '穩健型'},
                {'range': [60, 75], 'color': '#46b337', 'name': '平衡型'},
                {'range': [75, 90], 'color': '#fdae61', 'name': '成長型'},
                {'range': [90, 100], 'color': '#d73027', 'name': '積極型'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': final_score
            }
        }
    ))
    
    # 添加標註
    fig_gauge.add_annotation(x=0.2, y=0.25, text="保守型", showarrow=False)
    fig_gauge.add_annotation(x=0.4, y=0.25, text="穩健型", showarrow=False)
    fig_gauge.add_annotation(x=0.6, y=0.25, text="平衡型", showarrow=False)
    fig_gauge.add_annotation(x=0.8, y=0.25, text="成長型", showarrow=False)
    fig_gauge.add_annotation(x=0.95, y=0.25, text="積極型", showarrow=False)
    
    # 配置圖表布局
    fig_gauge.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(family="Arial", size=12)
    )
    
    # 顯示圖表
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    # 顯示分項評分
    st.subheader("分項評分")
    
    # 準備數據用於繪圖
    categories = ['財務狀況', '投資經驗', '投資目標', '風險心理承受度']
    scores = [financial_score, experience_score, goal_score, psychology_score]
    weights = [25, 20, 20, 35]  # 權重百分比
    
    # 創建 DataFrame 用於 Plotly
    df = pd.DataFrame({
        '評估項目': categories,
        '得分': scores,
        '權重百分比': weights
    })
    
    # 使用 Plotly 創建互動式柱狀圖
    fig_bar = px.bar(
        df, 
        x='評估項目', 
        y='得分',
        color='評估項目',
        color_discrete_sequence=px.colors.sequential.Viridis,
        text='得分',
        hover_data=['權重百分比'],
        labels={'權重百分比': '權重 (%)'}
    )
    
    # 更新圖表布局
    fig_bar.update_layout(
        xaxis_title='',
        yaxis_title='得分',
        yaxis=dict(range=[0, 105]),
        showlegend=False,
        title='風險評估分項得分',
        title_font_size=18,
        hovermode='closest'
    )
    
    # 更新文字標籤
    fig_bar.update_traces(
        texttemplate='%{text:.1f}',
        textposition='outside',
        width=0.4
    )
    
    # 顯示圖表
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # 創建雷達圖和圖例說明並放在同一行
    st.subheader("風險評估雷達圖")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # 準備雷達圖數據
        categories = ['財務狀況', '投資經驗', '投資目標', '風險心理承受度']
        
        # 創建 Plotly 雷達圖
        fig_radar = go.Figure()
        
        # 添加數據
        fig_radar.add_trace(go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            fillcolor=f'rgba{tuple(list(matplotlib.colors.to_rgba(color))[:3] + [0.2])}',
            line=dict(color=color, width=2),
            name=risk_profile
        ))
        
        # 更新布局
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False,
            height=500,
            margin=dict(l=80, r=80, t=20, b=80)
        )
        
        # 顯示圖表
        st.plotly_chart(fig_radar)
    
    with col2:
        # 添加圖例說明
        st.markdown("<h6 style='font-size:14px;'>圖示說明:</h6>", unsafe_allow_html=True)
        st.markdown("<span style='font-size:12px;'>- 財務狀況: 評估收入穩定性和財務彈性</span>", unsafe_allow_html=True)
        st.markdown("<span style='font-size:12px;'>- 投資經驗: 評估投資知識和實際經驗</span>", unsafe_allow_html=True)
        st.markdown("<span style='font-size:12px;'>- 投資目標: 評估投資期限和期望回報</span>", unsafe_allow_html=True)
        st.markdown("<span style='font-size:12px;'>- 風險心理承受度: 評估面對波動的心理反應</span>", unsafe_allow_html=True)
    
    # 顯示風險分析摘要
    st.subheader("投資風險分析摘要")
    
    # 創建評估摘要的資料框
    summary_data = []
    
    # 分析財務狀況
    if financial_score < 40:
        status = "需要改善"
        financial_analysis = "財務基礎較薄弱，收入穩定性或緊急資金準備可能不足。"
    elif financial_score < 70:
        status = "中等"
        financial_analysis = "財務狀況中等，具備基本的財務穩定性，但仍有優化空間。"
    else:
        status = "良好"
        financial_analysis = "財務基礎穩健，具備良好的收入穩定性和適當的應急準備。"
    summary_data.append(["財務狀況", status, financial_analysis])
    
    # 分析投資經驗
    if experience_score < 40:
        status = "有限"
        experience_analysis = "投資經驗較為有限，對投資工具和市場運作的了解可能不夠全面。"
    elif experience_score < 70:
        status = "一般"
        experience_analysis = "具有一定投資經驗，對基本投資工具有所了解，但深度可能有限。"
    else:
        status = "豐富"
        experience_analysis = "擁有豐富的投資經驗，對多種投資工具具備深入了解。"
    summary_data.append(["投資經驗", status, experience_analysis])
    
    # 分析投資目標
    if goal_score < 40:
        status = "保守短期"
        goal_analysis = "投資目標偏向短期和保守，偏好保本和流動性高的投資選項。"
    elif goal_score < 70:
        status = "平衡適中"
        goal_analysis = "投資目標平衡，期望在適當風險下獲得中等回報。"
    else:
        status = "成長導向"
        goal_analysis = "投資目標偏向長期成長，願意承受短期波動以追求長期收益。"
    summary_data.append(["投資目標", status, goal_analysis])
    
    # 分析風險心理承受度
    if psychology_score < 40:
        status = "保守"
        psychology_analysis = "風險承受度較低，面對市場波動時可能傾向保守決策。"
    elif psychology_score < 70:
        status = "中等"
        psychology_analysis = "具有中等風險承受能力，能在一定程度上接受市場波動。"
    else:
        status = "進取"
        psychology_analysis = "具有較高的風險承受能力，能夠面對較大市場波動並保持決策理性。"
    summary_data.append(["風險心理承受度", status, psychology_analysis])
    
    # 創建 DataFrame
    summary_df = pd.DataFrame(summary_data, columns=["評估項目", "狀態", "評估結果"])
    
    # 使用 Streamlit 的 DataFrame 樣式
    st.dataframe(summary_df, hide_index=True)
    
    # 創建回答摘要展示
    st.subheader("您的回答摘要")
    
    with st.expander("點擊查看您的所有回答"):
        # 將回答數據轉換為 DataFrame
        answers_df = pd.DataFrame(list(st.session_state.user_answers.items()), columns=["問題", "您的回答"])
        
        # 顯示表格
        st.dataframe(answers_df, hide_index=True)
    
    # 最終結論
    st.subheader("總體結論")
    
    # 根據風險類型提供最終分析
    if risk_profile == "保守型":
        final_advice = """
        綜合您的評估結果，您屬於保守型投資者。您傾向於優先考慮資金安全性，避免承擔過高風險。
        
        在投資前，您可能會考慮:
        - 確保擁有充足的應急資金
        - 增加對投資基礎知識的了解
        - 諮詢專業財務顧問以制定適合您的投資策略
        """
    elif risk_profile == "穩健型":
        final_advice = """
        綜合您的評估結果，您屬於穩健型投資者。您能接受適度風險以獲取相應回報，但仍重視資金安全。
        
        在投資前，您可能會考慮:
        - 確保財務規劃合理
        - 學習更多關於資產配置的知識
        - 制定明確的投資目標和期限
        """
    elif risk_profile == "平衡型":
        final_advice = """
        綜合您的評估結果，您屬於平衡型投資者。您尋求風險與回報的平衡，能接受中等程度的市場波動。
        
        在投資前，您可能會考慮:
        - 設計多元化的投資組合
        - 定期檢視投資表現並適時調整
        - 確立清晰的風險管理策略
        """
    elif risk_profile == "成長型":
        final_advice = """
        綜合您的評估結果，您屬於成長型投資者。您願意為追求較高回報而承擔相應風險，能接受較明顯的市場波動。
        
        在投資前，您可能會考慮:
        - 分散投資於不同資產類別和市場
        - 持續學習並完善投資知識和技巧
        - 設定停損點以控制潛在風險
        """
    else:  # 積極型
        final_advice = """
        綜合您的評估結果，您屬於積極型投資者。您追求最大化投資回報，願意承受較高風險和市場波動。
        
        在投資前，您可能會考慮:
        - 確保您理解所承擔的風險水平
        - 發展系統化的投資策略而非情緒化決策
        - 定期檢視投資表現並準備應對市場劇烈波動
        """
    
    # 使用美觀的方式呈現最終建議
    st.markdown(f"""
    <div style="background-color:#f8f9fa; padding:20px; border-radius:10px; border-left:5px solid {color};">
    {final_advice}
    </div>
    """, unsafe_allow_html=True)
    
    # 風險類型比較
    st.subheader("風險類型比較")
    
    # 準備各風險類型數據
    risk_types = ["保守型", "穩健型", "平衡型", "成長型", "積極型"]
    risk_scores = [20, 50, 67.5, 82.5, 95]  # 各類型的中心點得分
    risk_descriptions = [
        "低風險承受能力，以保本為主",
        "中低風險承受能力，平衡安全與收益",
        "中等風險承受能力，追求成長與穩健平衡",
        "中高風險承受能力，注重資產增值",
        "高風險承受能力，追求最大化回報"
    ]
    
    # 創建風險類型比較表格
    risk_comparison_df = pd.DataFrame({
        "風險類型": risk_types,
        "風險得分範圍": ["0-40", "41-60", "61-75", "76-90", "91-100"],
        "特點描述": risk_descriptions
    })
    
    # 高亮顯示用戶的風險類型
    user_risk_index = risk_types.index(risk_profile)
    
    # 使用 Streamlit 的 DataFrame 樣式，自訂格式化
    st.dataframe(
        risk_comparison_df.style.apply(
            lambda x: ['background-color: ' + color + '; color: white' if i == user_risk_index else '' for i in range(len(x))], 
            axis=0
        ),
        hide_index=True,
        use_container_width=True
    )
    
    # 添加重新評估按鈕
    if st.button("重新進行評估"):
        # 重置會話狀態變量
        st.session_state.assessment_complete = False
        st.session_state.user_answers = {}
        st.session_state.results = {}
        # 重新載入頁面
        st.experimental_rerun()
    
    # PDF報告生成函數
    def create_pdf():
        try:
            # 使用報告日期作為文件名的一部分
            report_date = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 使用英文建立PDF報告 - 完全避免中文字符
            # 創建PDF對象
            pdf = FPDF()
            pdf.add_page()
            
            # 添加標題
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="Investment Risk Assessment Report", ln=True, align='C')
            
            # 添加日期
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 10, txt=f"Assessment Date: {assessment_date}", ln=True)
            
            # 添加風險類型
            pdf.set_font("Arial", 'B', 14)
            # 使用英文表示風險類型
            risk_type_english = {
                "保守型": "Conservative",
                "穩健型": "Moderate",
                "平衡型": "Balanced",
                "成長型": "Growth-oriented",
                "積極型": "Aggressive"
            }.get(risk_profile, "Custom")
            
            pdf.cell(200, 10, txt=f"Risk Profile: {risk_type_english}", ln=True)
            
            # 添加總分
            pdf.cell(200, 10, txt=f"Risk Score: {final_score:.2f}/100", ln=True)
            
            # 添加分項評分
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(200, 15, txt="Category Scores", ln=True)
            
            # 分項評分表格 - 使用英文
            pdf.set_font("Arial", size=12)
            # 將中文類別轉為英文
            categories_english = {
                "財務狀況": "Financial Status",
                "投資經驗": "Investment Experience",
                "投資目標": "Investment Goals",
                "風險心理承受度": "Risk Tolerance"
            }
            
            for i, (cat, score) in enumerate(zip(categories, scores)):
                eng_cat = categories_english.get(cat, f"Category {i+1}")
                pdf.cell(100, 10, txt=eng_cat, border=1)
                pdf.cell(50, 10, txt=f"{score:.1f}", border=1, ln=True)
            
            # 添加Code Gym連結
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(200, 20, txt="", ln=True)  # 空行
            pdf.cell(200, 10, txt="For more investment knowledge, visit Code Gym at:", ln=True)
            pdf.cell(200, 10, txt="https://codegym.tech", ln=True)
            pdf.cell(200, 10, txt="Report generated by Code Gym Investment Risk Assessment System", ln=True)
            
            # 添加免責聲明
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 15, txt="Disclaimer", ln=True)
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(0, 10, txt="This system is for academic research and educational purposes only. The data and analysis provided are for reference only and DO NOT constitute investment or financial advice. Users should make their own investment decisions and bear the associated risks. The author of this system is not responsible for any investment behavior and does not assume any liability for losses.")
            
            # 返回PDF字節
            return pdf.output(dest='S').encode('latin-1')
        
        except Exception as e:
            st.error(f"生成PDF時發生錯誤: {str(e)}")
            return None
    
    # 添加下載PDF選項
    st.subheader("下載報告")
    
    # 生成PDF並提供下載
    pdf_bytes = create_pdf()
    
    # 生成下載連結
    b64 = base64.b64encode(pdf_bytes).decode()
    current_date = datetime.now().strftime("%Y%m%d")
    pdf_filename = f"投資風險評估報告_{current_date}.pdf"
    href = f'<a href="data:application/pdf;base64,{b64}" download="{pdf_filename}">下載PDF評估報告</a>'
    st.markdown(href, unsafe_allow_html=True)
    
    # 添加免責聲明
    st.markdown("""
    <div style="margin-top:30px; padding:10px; background-color:#f1f1f1; border-radius:5px; font-size:0.8em;">
    <strong>免責聲明：</strong>本系統僅供學術研究與教育用途，AI 提供的數據與分析結果僅供參考，<strong>不構成投資建議或財務建議</strong>。
    請使用者自行判斷投資決策，並承擔相關風險。本系統作者不對任何投資行為負責，亦不承擔任何損失責任。
    </div>
    """, unsafe_allow_html=True)