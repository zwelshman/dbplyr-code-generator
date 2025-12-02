import streamlit as st
import anthropic
import os

st.set_page_config(page_title="dbplyr Code Generator", page_icon="📊", layout="wide")

st.title("dbplyr Code Generator")
st.markdown("Enter your data manipulation instructions and get clean dbplyr R code")

# API key input
api_key = st.text_input("Anthropic API Key", type="password", value=os.getenv("ANTHROPIC_API_KEY", ""))

# Instructions input
instructions = st.text_area(
    "Instructions",
    placeholder="E.g., Filter patients where age > 65, select id and diagnosis, group by diagnosis and count",
    height=150
)

if st.button("Generate Code", type="primary"):
    if not api_key:
        st.error("Please enter your Anthropic API key")
    elif not instructions.strip():
        st.error("Please enter instructions")
    else:
        with st.spinner("Generating code..."):
            try:
                client = anthropic.Anthropic(api_key=api_key)
                
                message = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1000,
                    system="You are a dbplyr code generator. Return ONLY clean, executable R code using dbplyr syntax. No explanations, no markdown code blocks, no comments, no preamble. Just the raw R code that can be directly copied and pasted.",
                    messages=[
                        {
                            "role": "user",
                            "content": f"Generate dbplyr R code for the following instructions. Return ONLY the R code with no explanations, no markdown formatting, no comments, and no extra text. Just raw executable dbplyr code.\n\nInstructions: {instructions}"
                        }
                    ]
                )
                
                # Extract code from response
                code = message.content[0].text.strip()
                
                # Clean up any markdown formatting
                code = code.replace("```r", "").replace("```", "").strip()
                
                st.subheader("Generated Code")
                st.code(code, language="r")
                
            except Exception as e:
                st.error(f"Error generating code: {str(e)}")
