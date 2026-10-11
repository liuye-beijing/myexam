# -*- coding: utf-8 -*-
import streamlit as st
import openai

# ========== 只改这两行 ==========
DOUBAO_API_KEY = "你的火山方舟API Key"
CURRENT_PROGRESS = "高一数学：函数单调性、奇偶性；高一化学：离子反应、物质的量计算"
# ===============================

# 豆包固定官方接口（稳定可用）
openai.api_base = "https://ark.cn-beijing.volces.com/api/v3"
openai.api_key = "282b34ab-cf9d-45a4-ac25-ada42ffc1330"
MODEL_NAME = "doubao-seed-2.0-pro"

st.set_page_config(page_title="试卷AI学情分析", layout="centered")
st.title("📚 试卷AI学情分析｜豆包云端版")
st.caption("✅ 手机 / iPad / 电脑 全网随时可用")

st.info("💡 使用方法：粘贴试卷错题文本 → AI自动分析薄弱点、错因、复习+预习计划")

# 错题输入
wrong_content = st.text_area("✏️ 粘贴本次错题内容", height=260)

# AI分析
if st.button("🚀 生成学情报告 & 学习计划") and wrong_content.strip():
    with st.spinner("豆包AI深度分析中..."):
        prompt = f"""
你是资深高一学情分析师，贴合北师大附中教学进度。
【当前校内讲课进度】
{CURRENT_PROGRESS}
【学生错题】
{wrong_content}

请输出：
1. 薄弱知识点精准定位（细分到小点）
2. 错误归因：概念不清/审题失误/计算粗心/知识盲区
3. 本周可直接落地的复习方案
4. 贴合学校进度的下周预习重点

输出清晰、结构化、可执行，适合高中生提分。
"""
        res = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[{"role":"user","content":prompt}],
            temperature=0.2
        )

    st.divider()
    st.subheader("🎯 专属学情分析报告")
    st.markdown(res.choices[0].message.content)
