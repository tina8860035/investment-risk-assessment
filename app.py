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
import tempfile
import time
import platform

# 版本兼容性處理
def safe_rerun():
    """安全的重新運行函數，兼容不同Streamlit版本"""
    try:
        # 新版本Streamlit使用st.rerun()
        st.rerun()
    except AttributeError:
        try:
            # 舊版本Streamlit使用st.experimental_rerun()
            st.experimental_rerun()
        except AttributeError:
            # 如果都不可用，顯示提示信息
            st.info("評估已完成，請向下滾動查看結果")

# PDF相關導入（添加錯誤處理）
try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    st.warning("PDF功能暫時不可用，但不影響評估功能的使用")

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

# 改進的中文字體設置
def setup_chinese_fonts():
    """設置中文字體支援"""
    try:
        if platform.system() == 'Darwin':  # macOS
            matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'STHeiti', 'SimHei']
        elif platform.system() == 'Windows':  # Windows
            matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
        else:  # Linux (包括Streamlit Cloud)
            # 在Linux環境下使用基本字體，避免中文顯示問題
            matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Liberation Sans', 'Arial']
        
        matplotlib.rcParams['axes.unicode_minus'] = False
    except Exception as e:
        # 如果字體設置失敗，使用默認設置
        pass

# 調用字體設置
setup_chinese_fonts()

# 其他代碼保持不變...
# 將您的原始代碼複製到這裡，但要做以下替換：

# 1. 將所有的 st.experimental_rerun() 替換為 safe_rerun()
# 2. 在PDF生成部分添加條件檢查

# 例如，在評估完成部分：
# 原來的代碼：
# st.experimental_rerun()
# 
# 修改為：
# safe_rerun()

# PDF生成部分修改：
def create_pdf():
    """創建PDF報告"""
    if not PDF_AVAILABLE:
        st.error("PDF功能不可用，請聯繫管理員")
        return None
    
    try:
        # 您原來的PDF生成代碼...
        # 省略具體實現，使用您原來的代碼
        pass
    except Exception as e:
        st.error(f"生成PDF時發生錯誤: {str(e)}")
        return None

# 在PDF下載部分添加檢查：
if PDF_AVAILABLE:
    # 生成PDF並提供下載
    pdf_bytes = create_pdf()
    if pdf_bytes:
        # 顯示下載鏈接
        b64 = base64.b64encode(pdf_bytes).decode()
        current_date = datetime.now().strftime("%Y%m%d")
        pdf_filename = f"投資風險評估報告_{current_date}.pdf"
        href = f'<a href="data:application/pdf;base64,{b64}" download="{pdf_filename}">下載PDF評估報告</a>'
        st.markdown(href, unsafe_allow_html=True)
else:
    st.info("PDF下載功能暫時不可用，但您可以截圖保存評估結果")