import streamlit as st
import openai
import re
from graphviz import Digraph

st.set_page_config(page_title="AI Meeting Process Visualizer", layout="wide")

st.title("🧠 FlowSense AI – Demo MVP")
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

if api_key:
    openai.api_key = api_key
    st.subheader("From meeting transcript to live process mapping and insights")

    transcript = st.text_area("Paste your meeting transcript here:", height=300)

    if st.button("🔍 Analyze and Visualize"):
        with st.spinner("Thinking..."):
            system_prompt = """
            You are an AI that transforms business meeting transcripts into structured process flows.
            Extract the main process steps in order, list any pain points, and suggest future improvements.
            Return JSON with 3 fields: 'as_is', 'to_be', 'pain_points'.
            """

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript}
            ]

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.3
                )
                content = response.choices[0].message.content

                as_is = re.findall(r"as_is:(.*?)to_be:", content, re.DOTALL)
                to_be = re.findall(r"to_be:(.*?)pain_points:", content, re.DOTALL)
                pain_points = re.findall(r"pain_points:(.*)", content, re.DOTALL)

                as_is_steps = as_is[0].strip().split("->") if as_is else []
                to_be_steps = to_be[0].strip().split("->") if to_be else []
                pain_list = pain_points[0].strip().split("\n") if pain_points else []

                st.markdown("### 🔁 As-Is Process")
                dot_as_is = Digraph()
                for i, step in enumerate(as_is_steps):
                    dot_as_is.node(f"a{i}", step.strip())
                    if i > 0:
                        dot_as_is.edge(f"a{i-1}", f"a{i}")
                st.graphviz_chart(dot_as_is)

                st.markdown("### 🚀 To-Be Process")
                dot_to_be = Digraph()
                for i, step in enumerate(to_be_steps):
                    dot_to_be.node(f"b{i}", step.strip())
                    if i > 0:
                        dot_to_be.edge(f"b{i-1}", f"b{i}")
                st.graphviz_chart(dot_to_be)

                st.markdown("### ⚠️ Pain Points & Insights")
                for p in pain_list:
                    if p.strip():
                        st.markdown(f"- {p.strip()}")

            except openai.error.RateLimitError:
                st.error("⚠️ Rate limit exceeded. Try again later or use a different API key.")
            except openai.error.AuthenticationError:
                st.error("⚠️ Invalid API key. Please check and try again.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")
