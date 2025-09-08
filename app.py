import streamlit as st
import random
import re
from historias import BANCO_DE_HISTORIAS # Mantém a importação do seu banco de dados com as 10 histórias

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Oficina de Histórias",
    page_icon="📚",
    layout="wide"
)

# --- BANCO DE DADOS DO GLOSSÁRIO ---
GLOSSARIO = {
    "nebulosa": "Nuvem gigante de gás e poeira no espaço onde nascem as estrelas.",
    "faraó": "Título dos antigos reis do Egito, considerados deuses.",
    "sarcófago": "Caixão de pedra ornamentado, usado para abrigar corpos no Egito Antigo.",
    "hieróglifos": "Escrita do Egito Antigo, feita com desenhos e símbolos.",
    "trapezistas": "Artistas de circo que realizam acrobacias aéreas em um trapézio.",
    "ilusionista": "Mágico que cria ilusões para entreter, fazendo o que parece impossível.",
    "oceanógrafo": "Cientista que estuda os oceanos, suas plantas, animais e fenômenos.",
    "paradoxo temporal": "Situação ilógica que surge ao viajar no tempo e mudar o passado ou futuro.",
    "biosfera": "A parte da Terra onde existe vida, incluindo ar, terra e água.",
    "autômato": "Máquina que opera sozinha, como um robô.",
    "criptografado": "Informação transformada em código secreto para proteção.",
    "artefato": "Objeto feito por humanos, geralmente de interesse histórico ou cultural."
}

# --- ESTILIZAÇÃO CSS FINAL ---
def injetar_css_final():
    st.markdown(r"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
        
        /* --- LAYOUT GERAL --- */
        .stApp {
            background-color: #f0f4f8; height: 100vh; overflow: hidden; font-family: 'Poppins', sans-serif;
        }
        .main-container {
            width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 2rem;
        }

        /* --- TELA DE SELEÇÃO (COM CARTÕES CLICÁVEIS CORRIGIDOS) --- */
        .selection-header { text-align: center; margin-bottom: 40px; }
        .selection-header h1 { font-weight: 700; color: #1e3a5f; }
        .selection-header p { font-size: 1.2rem; color: #5a7a9d; }
        .card-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 30px; width: 100%; max-width: 1200px; }
        
        /* NOVO CONTAINER PARA O CARTÃO E O BOTÃO JUNTOS */
        .card-wrapper {
            background-color: #ffffff;
            border-radius: 20px;
            box-shadow: 0 8px 24px rgba(20, 49, 89, 0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            height: 250px;
            display: flex;
            flex-direction: column;
            overflow: hidden; /* Garante que o botão não "vaze" */
        }
        .card-wrapper:hover { transform: translateY(-12px); box-shadow: 0 12px 32px rgba(20, 49, 89, 0.15); }
        
        .story-card-content {
            padding: 25px 20px;
            text-align: center;
            flex-grow: 1; /* Faz esta parte ocupar o espaço disponível */
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .story-card-content .icon { font-size: 4.5rem; line-height: 1; }
        .story-card-content .title { font-size: 1.2rem; font-weight: 600; color: #1e3a5f; margin: 15px 0; }
        
        /* BOTÃO INTEGRADO AO CARTÃO */
        .card-wrapper .stButton button {
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 0; /* Remove o raio para se juntar ao cartão */
            font-weight: 600;
            width: 100%;
            padding: 12px 0;
            transition: background-color 0.2s;
        }
        .card-wrapper .stButton button:hover {
            background-color: #0056b3;
        }

        /* --- TELA DE JOGO (sem alterações críticas) --- */
        .game-card { background-color: #fff; padding: 50px 60px; border-radius: 20px; box-shadow: 0 8px 30px rgba(20, 49, 89, 0.1); width: 100%; max-width: 1100px; text-align: center; }
        .game-card .question { font-size: 1.8rem; font-weight: 600; color: #1e3a5f; margin: 20px 0 40px 0; min-height: 100px; }
        .choice-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 30px; width: 100%; }
        .choice-grid .stButton button {
            background-color: #f8f9fa; color: #1e3a5f; border: 2px solid #d3e0ed; padding: 20px; font-size: 1.1rem; font-weight: 600;
            height: 100%; width: 100%; white-space: normal; border-radius: 12px; transition: all 0.2s ease;
        }
        .choice-grid .stButton button:hover { border-color: #007bff; background-color: #007bff; color: #ffffff; }

        /* --- TELA FINAL (sem alterações críticas) --- */
        .final-story-card { background: #fff; padding: 40px 60px; border-radius: 20px; box-shadow: 0 8px 30px rgba(20, 49, 89, 0.1); width: 100%; max-width: 1000px; max-height: 90vh; overflow-y: auto; }
        .final-story-card h1 { text-align: center; color: #1e3a5f; font-weight: 700; margin-bottom: 30px; }
        .final-story-card p { text-indent: 2.5em; line-height: 1.9; font-size: 1.15rem; color: #212529; margin-bottom: 1.5em; }
        .alternative-ending { margin-top: 40px; padding: 25px; background-color: #f8f9fa; border-left: 6px solid #17a2b8; border-radius: 8px; }
        .glossary-section { margin-top: 50px; padding-top: 30px; border-top: 1px solid #e6e9ee; }
        .glossary-section h2 { text-align: center; color: #1e3a5f; }
        .glossary-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
        .glossary-item { padding: 15px 20px; }
        .glossary-item strong { color: #007bff; }
        .glossary-item p { font-size: 0.95rem; color: #555; text-indent: 0; }
        .final-story-card .stButton button { width: 100%; margin-top: 30px; background-color: #28a745; color: white; border: none; padding: 15px; font-size: 1.2rem; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- GERENCIAMENTO DE ESTADO ---
if 'etapa_app' not in st.session_state:
    st.session_state.etapa_app = 'selecao'
# ... (o resto do gerenciamento de estado permanece idêntico) ...
if 'historia_selecionada' not in st.session_state:
    st.session_state.historia_selecionada = None
if 'estagio_atual' not in st.session_state:
    st.session_state.estagio_atual = 0
if 'caminho_percorrido' not in st.session_state:
    st.session_state.caminho_percorrido = []


# --- FUNÇÕES DE RENDERIZAÇÃO DE TELA (REESCRITAS) ---

def renderizar_tela_selecao():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="selection-header"><h1>📚 Oficina de Histórias 🖋️</h1><p>Escolha uma aventura e dê vida a uma nova história!</p></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card-grid">', unsafe_allow_html=True)
    sorted_historias = sorted(BANCO_DE_HISTORIAS.items())
    cols = st.columns(len(sorted_historias))

    for i, (id_historia, detalhes) in enumerate(sorted_historias):
        with cols[i]:
            # Criamos um container para o cartão e o botão, que será estilizado pelo CSS
            with st.container():
                st.markdown(f"""
                <div class="card-wrapper">
                    <div class="story-card-content">
                        <div class="icon">{detalhes['icone']}</div>
                        <div class="title">{detalhes['titulo']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("Começar Aventura", key=f"btn_{id_historia}", use_container_width=True):
                    st.session_state.etapa_app = 'jogando'
                    st.session_state.historia_selecionada = id_historia
                    st.session_state.estagio_atual = 0
                    st.session_state.caminho_percorrido = []
                    st.rerun()
                
                # Fechamos a div do wrapper aqui, após o botão ser renderizado
                st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

# ... (As funções renderizar_tela_jogo e renderizar_tela_final permanecem idênticas à versão anterior, pois já estavam estáveis) ...

def renderizar_tela_jogo():
    id_historia = st.session_state.historia_selecionada
    estagio = st.session_state.estagio_atual
    detalhes_historia = BANCO_DE_HISTORIAS[id_historia]
    detalhes_estagio = detalhes_historia['estagios'][estagio]

    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="game-card"><p class="question">{detalhes_estagio["pergunta"]}</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="choice-grid">', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (opcao, fragmento) in enumerate(detalhes_estagio['opcoes'].items()):
        with cols[i]:
            if st.button(opcao, key=f"opcao_{i}", use_container_width=True):
                st.session_state.caminho_percorrido.append(fragmento)
                if st.session_state.estagio_atual < 9:
                    st.session_state.estagio_atual += 1
                else:
                    st.session_state.etapa_app = 'final'
                st.rerun()
    st.markdown('</div></div></div>', unsafe_allow_html=True)

def renderizar_tela_final():
    id_historia = st.session_state.historia_selecionada
    detalhes_historia = BANCO_DE_HISTORIAS[id_historia]
    texto_completo = " ".join(st.session_state.caminho_percorrido)
    
    sentencas = re.split(r'(?<=[.!?])\s+', texto_completo)
    paragrafos = [""] * 4
    if sentencas:
        sentencas_por_paragrafo = (len(sentencas) + 3) // 4
        idx_paragrafo = 0
        for i, sentenca in enumerate(sentencas):
            if i > 0 and i % sentencas_por_paragrafo == 0 and idx_paragrafo < 3:
                idx_paragrafo += 1
            paragrafos[idx_paragrafo] += sentenca + " "
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    with st.container():
        st.markdown(f'<div class="final-story-card"><h1>{detalhes_historia["titulo"]}</h1>', unsafe_allow_html=True)
        for p in paragrafos:
            if p.strip():
                st.markdown(f'<p>{p.strip()}</p>', unsafe_allow_html=True)

        # Final Alternativo
        fragmentos_alternativos = list(detalhes_historia['estagios'][9]['opcoes'].values())
        fragmento_atual_final = st.session_state.caminho_percorrido[-1]
        if fragmento_atual_final in fragmentos_alternativos:
            fragmentos_alternativos.remove(fragmento_atual_final)
        resumo_alternativo = random.choice(fragmentos_alternativos) if fragmentos_alternativos else ""
        st.markdown(f'<div class="alternative-ending"><h4>E se você tivesse escolhido diferente?</h4><p><em>Em um final alternativo, sua história poderia ter terminado assim: "{resumo_alternativo}"</em></p></div>', unsafe_allow_html=True)

        # Glossário
        palavras_na_historia = set(re.findall(r'\b\w+\b', texto_completo.lower()))
        palavras_para_glossario = {palavra: definicao for palavra, definicao in GLOSSARIO.items() if palavra.lower() in palavras_na_historia}
        if palavras_para_glossario:
            st.markdown('<div class="glossary-section"><h2>Glossário da Aventura</h2><div class="glossary-list">', unsafe_allow_html=True)
            for palavra, definicao in sorted(palavras_para_glossario.items()):
                st.markdown(f'<div class="glossary-item"><strong>{palavra.capitalize()}:</strong><p>{definicao}</p></div>', unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)

        if st.button("Criar uma Nova História"):
            # Limpa o estado da sessão para um novo jogo
            for key in list(st.session_state.keys()):
                st.session_state.pop(key)
            st.session_state.etapa_app = 'selecao'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ROTEADOR PRINCIPAL DA APLICAÇÃO ---
injetar_css_final()

etapa = st.session_state.get('etapa_app', 'selecao')
if etapa == 'selecao':
    renderizar_tela_selecao()
elif etapa == 'jogando':
    renderizar_tela_jogo()
else:
    renderizar_tela_final()
