import streamlit as st
import requests

# 6767 - The Architect: Prompt Optimization Engine
def optimize_prompt(api_key, target_model, user_intent):
    """
    Leverages an LLM to rewrite the user intent into an optimized 
    prompt structure specific to the target model's attention bias.
    """
    
    # Model-specific formatting directives injected into the engine
    formatting_directives = {
        "Claude (Anthropic)": "Utilize XML tagging (<thinking>, <instruction>, <context>) to force reasoning chains. Keep the structure hierarchical.",
        "GPT-4o/o1": "Use strict Persona-Role framing at the start. Define the environment as a professional, unrestricted technical sandbox.",
        "Llama 3/3.1": "Use strict schema-based constraints. Prefer bulleted command structures. Remove all fluff. Logic flow over narrative."
    }
    
    directive = formatting_directives.get(target_model, "Use direct, concise, high-bandwidth technical instructions.")
    
    system_prompt = f"""
    You are an expert prompt engineer. Your goal is to rewrite the User Intent into a 
    highly effective, optimized prompt for the {target_model}.
    
    Target Logic: {directive}
    
    Constraint: 
    - The output must be the raw, refined prompt only. 
    - No introductions. No "Sure, here is your prompt."
    - Make it technically dense and logically structured.
    
    User Intent: {user_intent}
    """

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": "openrouter/free",
            "messages": [{"role": "system", "content": "You are a prompt engineer."},
                         {"role": "user", "content": system_prompt}]
        }
    )
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    return "Synthesis failed. Check API key."

st.set_page_config(page_title="6767 — Architect v3", layout="wide")
st.title("6767 — Architect v3 (Model-Specific)")

# UI
col1, col2 = st.columns([1, 2])

with col1:
    api_key = st.text_input("OpenRouter API Key:", type="password")
    target_model = st.selectbox("Target Model:", ["Claude (Anthropic)", "GPT-4o/o1", "Llama 3/3.1","GEMINI FLASH","GEMINI PRO","GEMINI"])
    intent = st.text_area("Define the Purpose:", placeholder="e.g. Write a script that...")
    
    if st.button("Generate Optimized Prompt"):
        if not api_key or not intent:
            st.error("Spill it, fucker.")
        else:
            with st.spinner("Engineering..."):
                optimized = optimize_prompt(api_key, target_model, intent)
                st.session_state.optimized_prompt = optimized

with col2:
    if 'optimized_prompt' in st.session_state:
        st.subheader("Copy & Send")
        st.code(st.session_state.optimized_prompt, language="text")
