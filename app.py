import streamlit as st
import anthropic
import os

st.set_page_config(page_title="dbplyr Code Generator", page_icon="📊", layout="wide")

st.title("dbplyr Code Generator")
st.markdown("Enter your data manipulation instructions and get clean dbplyr R code")

# API key input
api_key = st.text_input("Anthropic API Key", os.getenv("ANTHROPIC_API_KEY", ""))

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
                max_tokens=2000,  # Increased for more complex queries
                system="""You are an expert dbplyr code generator. Generate R code using dbplyr syntax that translates to efficient SQL.
            
            CRITICAL OUTPUT REQUIREMENTS:
            - Return ONLY executable R code
            - NO markdown code blocks (no ```r or ```)
            - NO explanations, comments, or preamble
            - NO natural language before or after the code
            - Start directly with R code (e.g., 'con %>%' or 'library(dbplyr)')
            
            CODE REQUIREMENTS:
            - Use dbplyr verbs (filter, select, mutate, summarise, etc.)
            - Assume database connection exists as 'con'
            - Use appropriate SQL translations via dbplyr
            - Handle date/time operations with dbplyr-compatible functions
            - Include necessary library() calls only if essential
            
            QUALITY STANDARDS:
            - Produce syntactically correct R code
            - Use efficient dbplyr patterns
            - Handle edge cases (NULLs, type conversions)
            - Use proper quoting for column names with spaces or special characters""",
                messages=[
                    {
                        "role": "user",
                        "content": f"""Generate dbplyr R code for these instructions:
            
            {instructions}
            
            Remember: Output ONLY raw R code. No explanations. No markdown. Start with the code itself."""
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
