# -*- coding: utf-8 -*-
import streamlit as st
import openai
import uuid
from PIL import Image
import easyocr

# ====================== 只改这两行 ======================
DOUBAO_API_KEY = "你的火山方舟API_KEY"
CURRENT_PROGRESS = "高一数学：函数单调性、奇偶性；高一化学：离子反应、物质的量计算"
# ========================================================

# 豆包API固定配置（永久不变）
openai.api_base = "https://ark.cn-beijing.volces.com/api/v3"
openai.api_key = api-key-20260309094850
MODEL_NAME = "doubao-seed-2.0-pro"

# 缓存不冲突、多设备可用
st.set_page_config(page_title="试卷AI学情分析", layout="centered")
st.title("📚 试卷AI学情分析｜云端永久版")
st.caption("✅ 手机/iPad/电脑全网可用｜豆包大模型")

# 初始化OCR（云端兼容、无需系统依赖）
@st.cache_resource
def get_ocr():
    return easyocr.Reader(['ch_sim','en'])

reader = get_ocr()

# 上传试卷
uploaded_file = st.file_uploader("📷 拍照/上传试卷照片", type=["jpg","png","jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.success("✅ 上传成功，正在AI识别试卷...")

    # OCR识别中文试卷
    result = reader.readtext(img, detail=0)
    full_text = "\n".join(result)

    st.subheader("📄 试卷识别内容")
    st.text_area("全文文本", full_text, height=220)

    st.divider()
    wrong_content = st.text_area("✏️ 粘贴本次错题题干", height=180)

# 豆包AI学情分析
if st.button("🚀 生成薄弱点 + 预习复习计划") and wrong_content.strip():
    prompt = f"""
你是资深高一学情分析师，贴合北师大附中教学进度。
【当前校内讲课进度】
{CURRENT_PROGRESS}
【学生错题】
{wrong_content}

请输出四段清晰、可落地内容：
1. 精准薄弱知识点（细分到最小考点）
2. 错误归因：概念不清 / 审题失误 / 计算粗心 / 知识盲区
3. 本周针对性复习方案（具体做题、复盘方法）
4. 下周贴合校内进度的预习重点

输出适合高中生、家长可直接执行。
"""
    with st.spinner("豆包AI深度分析中..."):
        res = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[{"role":"user","content":prompt}],
            temperature=0.3
        )
        st.divider()
        st.subheader("🎯 专属学情分析报告")
        st.markdown(res.choices[0].message.content)
