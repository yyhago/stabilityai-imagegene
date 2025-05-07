import os
import streamlit as st
from image_generator import generate_image, decode_base64

def local_css(file_name):
    # Obtém o diretório do script atual
    dir_path = os.path.dirname(os.path.realpath(__file__))
    css_path = os.path.join(dir_path, file_name)
    
    try:
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Arquivo CSS não encontrado em: {css_path}")


def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://images.unsplash.com/photo-1639762681057-408e52192e55?q=80&w=2232&auto=format&fit=crop");
             background-attachment: fixed;
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

def main():
    st.set_page_config(
        page_title="✨ Magic Image Generator",
        page_icon="🧙‍♂️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    local_css("style.css")
    

    with st.container():
        st.markdown("""
        <div class='header'>
            <h1>✨ Gerador de Imagem</h1>
            <p>Crie imagens incríveis com IA</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.title("Configurações")
        engine_options = {
            "Stable Diffusion v1.6": "stable-diffusion-v1-6",
            "Stable Diffusion 512 v2.1": "stable-diffusion-512-v2-1",
            "Stable Diffusion XL": "stable-diffusion-xl-1024-v1-0"
        }
        selected_engine = st.selectbox("Modelo de IA:", list(engine_options.keys()))
        
        size_options = ["512x512", "768x768", "1024x1024"]
        selected_size = st.selectbox("Resolução:", size_options)
        
        advanced = st.expander("Configurações Avançadas")
        with advanced:
            cfg_scale = st.slider("Criatividade (CFG Scale)", 1.0, 20.0, 7.0)
            steps = st.slider("Nível de Detalhe (Steps)", 10, 150, 30)
            samples = st.slider("Número de Imagens", 1, 4, 1)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        with st.form("prompt_form"):
            prompt = st.text_area(
                "Descreva sua imagem:",
                placeholder="Ex: Um dragão celestial feito de galáxias, estilo arte conceitual digital hiper detalhada",
                height=150
            )
            
            negative_prompt = st.text_area(
                "O que evitar na imagem:",
                placeholder="Ex: texto, baixa qualidade, mãos deformadas, arte ruim",
                height=100
            )
            
            generate_button = st.form_submit_button(
                "🧙‍♂️ Conjurar Imagem",
                use_container_width=True
            )
    
    with col2:
        st.markdown("### Pré-visualização")
        image_placeholder = st.empty()
        image_placeholder.image("https://via.placeholder.com/512x512?text=Imagem+será+gerada+aqui", use_column_width=True)
        
        download_placeholder = st.empty()
    
    if generate_button and prompt:
        with st.spinner("🧙‍♂️ Criando sua imagem..."):
            try:
                width, height = map(int, selected_size.split("x"))
                
                response = generate_image(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    width=width,
                    height=height,
                    engine_id=engine_options[selected_engine],
                    steps=steps,
                    cfg_scale=cfg_scale,
                    samples=samples
                )
                
                if response and 'artifacts' in response:
                    st.balloons()
                    st.success("✨ Imagem mágica criada com sucesso!")
                    
                    for idx, image in enumerate(response['artifacts']):
                        img_data = f"data:image/png;base64,{image['base64']}"
                        image_placeholder.image(img_data, use_column_width=True)
                        
                        download_placeholder.download_button(
                            label="⬇️ Baixar Imagem Mágica",
                            data=decode_base64(image['base64']),
                            file_name=f"magic_image_{idx+1}.png",
                            mime="image/png",
                            use_container_width=True
                        )
                else:
                    st.error("O feitiço falhou! A varinha mágica (API) não respondeu.")
            
            except Exception as e:
                st.error(f"⚡ O feitiço falhou: {str(e)}")

if __name__ == "__main__":
    main()