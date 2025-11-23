# app.py
import streamlit as st
import openai

st.set_page_config(page_title="WP Debug Bot", layout="wide")
st.title("WP Debug Bot com API da OpenAI")
st.markdown("### Diagnóstico instantâneo de erros do WordPress")
st.caption("Feito por Erick Costa – Nov/2025")

# API Key
api_key = st.text_input("Cole sua API Key abaixo", type="password", help="Mesma key do projeto anterior")
if api_key:
    openai.api_key = api_key

# Área grande para colar o erro
erro = st.text_area(
    "Cole aqui o erro completo do WordPress (log, tela branca, mensagem do PHP, etc.)",
    height=250,
    placeholder="Exemplo:\nFatal error: Uncaught Error: Call to undefined function get_header() in /wp-content/themes/meutema/index.php on line 15"
)

# Botão principal
if st.button("Diagnosticar erro agora", type="primary", use_container_width=True):
    if not api_key:
        st.error("Coloca a API Key primeiro!")
    elif not erro.strip():
        st.warning("Cola o erro aí, cara!")
    else:
        with st.spinner("Analisando com GPT-4o-mini..."):
            try:
                resposta = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    temperature=0.3,
                    messages=[
                        {"role": "system", "content": "Você é um especialista sênior em WordPress com 15 anos de experiência. Responda SEMPRE em português brasileiro, de forma clara, com passos numerados e >
                        {"role": "user", "content": f"Analise este erro do WordPress e me dê:\n1. O que está acontecendo\n2. Causa mais provável\n3. Solução passo a passo\n4. Como prevenir\n\nErro:\n{erro}"}
                    ]
                )
                diagnostico = resposta.choices[0].message.content
                
                st.success("Diagnóstico completo!")
                st.markdown(diagnostico)
                
                # Botão para copiar
                st.code(diagnostico, language="markdown")
                st.balloons()
                
            except Exception as e:
                st.error(f"Erro na API: {e}")

