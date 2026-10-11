# -*- coding: utf-8 -*-
import streamlit as st
from paddleocr import PaddleOCR
import openai
import os
import uuid

# ====================== 仅需修改这里（填你豆包Key） ======================
DOUBAO_API_KEY = "你的火山方舟API密钥"
CURRENT_PROGRESS = "高一数学：函数单调性、奇偶性；高一化学：离子反应、物质的量计算"
# =====================================================================

# 豆包API固定配置（无需改动）
MODEL_NAME = "doubao-seed-2.0-pro"
openai.api_base = "https://ark.cn-beijing.volces.com/api/v3"
openai.api_key = api-key-20260309094850

# 多用户隔离，云端零冲突
session_id = str(uuid.uuid4())
temp_path = f"temp_paper_{session_id}.jpg"

# OCR稳定配置
ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False, show_log=False)

# 移动端自适应
st.set_page_config(page_title="试卷AI学情分析", layout="centered")
st.title("📚 AI试卷学情分析系统｜豆包引擎版")
st.caption("✅ 豆包大模型驱动｜手机/iPad/电脑全网可用")

# 拍照上传
uploaded_file = st.file_uploader("📷 拍照或上传试卷照片", type=["jpg","png","jpeg"])

if uploaded_file:
    st.success("✅ 上传成功，正在OCR识别试卷...")
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # 识别试卷全文
    result = ocr.ocr(temp_path, cls=True)
    txt_list = []
    for res in result:
        for line in res:
            txt_list.append(line[1][0])
    full_text = "\n".join(txt_list)

    st.subheader("📄 识别结果")
    st.text_area("试卷全文", full_text, height=200)

    st.divider()
    st.subheader("✏️ 粘贴本次错题题干")
    wrong_content = st.text_area("错题内容", height=180)

# 豆包AI学情分析
if st.button("🚀 豆包AI生成薄弱点 + 预习复习计划") and wrong_content.strip():
    prompt = f"""
你是资深新高一学情分析师，非常熟悉国内高中教材、北师大附中教学进度与考试重难点。
【当前校内讲课进度】
{CURRENT_PROGRESS}

【学生本次考试错题】
{wrong_content}

请严格输出四段清晰、落地、适合高中生执行的内容：
1. 【薄弱知识点精准定位】细分最小知识点，不笼统概括
2. 【错误原因精准归因】区分：概念不清 / 审题失误 / 计算粗心 / 知识盲区
3. 【本周针对性复习方案】给出可直接落地的刷题、复盘、纠错方法
4. 【下周贴合进度预习重点】结合当前校内进度，给出新课核心必学知识点、预习重点

输出通俗易懂、专业、不空泛，适合高中生提分。
"""

    with st.spinner("豆包AI深度分析学情中..."):
        resp = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[{"role":"user","content":prompt}],
            temperature=0.3
        )
        st.divider()
        st.subheader("🎯 专属学情报告 & 学习计划")
        st.markdown(resp.choices[0].message.content)

# 自动清理缓存
if os.path.exists(temp_path):
    os.remove(temp_path)
