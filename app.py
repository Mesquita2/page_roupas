import streamlit as st
import requests
from PIL import Image
import io

st.title("Classificação de Roupas + Busca de Produtos")

# URL do seu servidor FastAPI
API_URL = "http://127.0.0.1:8000"


file = st.file_uploader("Escolha uma imagem", type=["jpg","jpeg","png"])

if file:
    files = {"file": (file.name, file, file.type)}
    response = requests.post("http://127.0.0.1:8000/upload-image", files=files)
    data = response.json()
    
    if response.status_code == 200:
        predicted_class = data["classe_predita"]
        confidence = data["confianca"]
        st.success(f"Classe prevista: **{predicted_class}**")
        st.info(f"Confiança: **{confidence:.2f}**")

        # Perguntar se quer buscar produtos
        if st.button("Buscar produtos desta categoria"):
            filtro = {"categoria": predicted_class}
            resp_produtos = requests.post(f"{API_URL}/buscar-produtos", json=filtro)
            if resp_produtos.status_code == 200:
                produtos = resp_produtos.json()
                st.subheader("Resultados da Busca")

                for loja, items in produtos.items():
                    st.markdown(f"### {loja.replace('_',' ').title()}")
                    for item in items:
                        st.write(f"**{item.get('titulo')}**")
                        st.write(f"Preço: {item.get('preco', 'N/A')} {item.get('moeda','')}")
                        st.write(f"[Link]({item.get('url')})")
                        if item.get("imagem"):
                            st.image(item.get("imagem"), width=150)
            else:
                st.error("Erro ao buscar produtos")
    else:
        st.error("Erro ao enviar imagem para predição")
