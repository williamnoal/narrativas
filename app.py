import streamlit as st
import random
from historias import BANCO_DE_HISTORIAS

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Oficina de Histórias",
    page_icon="📚",
    layout="wide"
)

# --- INJEÇÃO DE CSS PARA UMA INTERFACE MODERNA ---
def injecao_css():
    st.markdown(r"""
    <style>
        /* ... (Cole aqui o mesmo bloco de CSS da resposta anterior) ... */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        
        body, .stApp {
            font-family: 'Poppins', sans-serif;
        }

        .stApp {
            background-color: #f0f2f6;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }
        .main-container {
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 2rem;
        }

        .card-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 25px;
            justify-items: center;
        }
        .story-card {
            background-color: #ffffff;
            border-radius: 15px;
            text-align: center;
            width: 180px;
            height: 200px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border: 1px solid #e0e0e0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 15px;
        }
        .story-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        .story-card .icon { font-size: 4rem; }
        .story-card .title { font-size: 1.1rem; font-weight: 600; margin-top: 10px; color: #333; }
        .story-card .stButton button {
            margin-top: 15px;
            border-radius: 8px;
            width: 100%;
        }

        .game-container {
            background-color: #ffffff;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            width: 80%;
            max-width: 900px;
            text-align: center;
        }
        .game-container .stage-icon { font-size: 3rem; color: #555; }
        .game-container .question { font-size: 1.5rem; font-weight: 600; color: #111; margin: 15px 0 25px 0; }
        
        .stButton > button {
            border: 2px solid #ddd;
            border-radius: 10px;
            background-color: #f8f9fa;
            color: #333;
            padding: 15px;
            font-size: 1rem;
            font-weight: 600;
            transition: all 0.2s ease;
            height: 100%;
        }
        .stButton > button:hover { border-color: #007bff; background-color: #e7f1ff; color: #007bff; }
        .stButton > button:focus { box-shadow: 0 0 0 0.2rem rgba(0,123,255,.5); }

        .final-story-container {
            background: #fff;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            width: 80%;
            max-width: 900px;
            text-align: left;
        }
        .final-story-container h1 { text-align: center; color: #0056b3; }
        .final-story-container p { text-indent: 2em; line-height: 1.8; font-size: 1.1rem; color: #333; margin-block-start: 1em; margin-block-end: 1em;}
        .alternative-ending { margin-top: 30px; padding: 20px; background-color: #e9ecef; border-left: 5px solid #007bff; border-radius: 5px; }
        .final-story-container .stButton button { width: 100%; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- GERENCIAMENTO DE ESTADO ---
if 'etapa_app' not in st.session_state:
    st.session_state.etapa_app = 'selecao'
if 'historia_selecionada' not in st.session_state:
    st.session_state.historia_selecionada = None
if 'estagio_atual' not in st.session_state:
    st.session_state.estagio_atual = 0
if 'caminho_percorrido' not in st.session_state:
    st.session_state.caminho_percorrido = []

# --- FUNÇÕES DE RENDERIZAÇÃO DE TELA ---

def mostrar_tela_selecao():
    with st.container():
        st.markdown("<div class='main-container'>", unsafe_allow_html=True)
        st.title("📚 Oficina de Histórias 🖋️")
        st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Escolha uma aventura e dê vida a uma nova história!</p>", unsafe_allow_html=True)
        
        st.markdown("<div class='card-grid'>", unsafe_allow_html=True)
        for id_historia, detalhes in BANCO_DE_HISTORIAS.items():
            with st.container():
                st.markdown(f"""
                <div class="story-card">
                    <div class="icon">{detalhes['icone']}</div>
                    <div class="title">{detalhes['titulo']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Começar", key=f"btn_{id_historia}", use_container_width=True):
                    st.session_state.etapa_app = 'jogando'
                    st.session_state.historia_selecionada = id_historia
                    st.session_state.estagio_atual = 0
                    st.session_state.caminho_percorrido = []
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

def mostrar_tela_jogo():
    id_historia = st.session_state.historia_selecionada
    estagio = st.session_state.estagio_atual
    detalhes_historia = BANCO_DE_HISTORIAS[id_historia]
    detalhes_estagio = detalhes_historia['estagios'][estagio]

    with st.container():
        st.markdown("<div class='main-container'>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="game-container">
            <div class="stage-icon">{detalhes_historia['icone']}</div>
            <p class="question">{detalhes_estagio['pergunta']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3, gap="large")
        for i, (opcao, fragmento) in enumerate(detalhes_estagio['opcoes'].items()):
            if cols[i].button(opcao, key=f"opcao_{i}"):
                st.session_state.caminho_percorrido.append(fragmento)
                if st.session_state.estagio_atual < 9:
                    st.session_state.estagio_atual += 1
                else:
                    st.session_state.etapa_app = 'final'
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def mostrar_tela_final():
    id_historia = st.session_state.historia_selecionada
    detalhes_historia = BANCO_DE_HISTORIAS[id_historia]
    
    texto_completo = " ".join(st.session_state.caminho_percorrido)
    palavras = texto_completo.split()
    tamanho_paragrafo = len(palavras) // 4
    
    paragrafos = []
    inicio = 0
    for i in range(4):
        fim = inicio + tamanho_paragrafo
        # Garante que o parágrafo termine com um ponto final, se possível.
        if i < 3 and fim < len(palavras):
            while fim < len(palavras) and not palavras[fim-1].endswith('.'):
                fim += 1
        
        if i == 3: # Último parágrafo pega todo o resto
            fim = len(palavras)
            
        paragrafos.append(" ".join(palavras[inicio:fim]))
        inicio = fim
    
    with st.container():
        st.markdown("<div class='main-container'>", unsafe_allow_html=True)
        st.markdown('<div class="final-story-container">', unsafe_allow_html=True)
        st.markdown(f"<h1>{detalhes_historia['titulo']}</h1>", unsafe_allow_html=True)
        for p in paragrafos:
            if p.strip():
                st.markdown(f"<p>{p.strip()}</p>", unsafe_allow_html=True)

        fragmentos_alternativos = list(detalhes_historia['estagios'][9]['opcoes'].values())
        fragmento_atual_final = st.session_state.caminho_percorrido[-1]
        fragmentos_alternativos.remove(fragmento_atual_final)
        resumo_alternativo = random.choice(fragmentos_alternativos)
        
        st.markdown(f"""
        <div class="alternative-ending">
            <h4>E se você tivesse escolhido diferente?</h4>
            <p><em>Em um final alternativo, a história poderia ter terminado assim: "{resumo_alternativo}" Explore outras escolhas para descobrir novos destinos!</em></p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Criar uma Nova História"):
            st.session_state.etapa_app = 'selecao'
            st.rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)

# --- LÓGICA PRINCIPAL DA APLICAÇÃO ---
injecao_css()

if st.session_state.etapa_app == 'selecao':
    mostrar_tela_selecao()
elif st.session_state.etapa_app == 'jogando':
    mostrar_tela_jogo()
elif st.session_state.etapa_app == 'final':
    mostrar_tela_final()
