import streamlit as st
import random
import re
from historias import BANCO_DE_HISTORIAS # Mantemos a importação do seu banco de dados de histórias

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Oficina de Histórias",
    page_icon="📚",
    layout="wide"
)

# --- Dicionário de Glossário ---
# Adicione mais palavras e suas definições aqui conforme necessário
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
    "crono-acelerador": "Dispositivo hipotético que manipula a passagem do tempo.",
    "quasar": "Objeto astronômico extremamente luminoso e distante, fonte de energia.",
    "gárgula": "Figura esculpida, geralmente em prédios antigos, que serve como escoamento de água.",
    "autômato": "Máquina que opera sozinha, como um robô.",
    "criptografado": "Informação transformada em código secreto para proteção.",
    "artefato": "Objeto feito por humanos, geralmente de interesse histórico ou cultural."
}


# --- INJEÇÃO DE CSS PARA UMA INTERFACE MODERNA E FLUIDA ---
def injetar_css_moderno():
    st.markdown(r"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

        /* --- RESET GERAL E LAYOUT SEM SCROLL --- */
        html, body, .stApp {
            height: 100%;
            margin: 0;
            padding: 0;
            overflow: hidden; /* A regra mais importante para remover a barra de rolagem */
            font-family: 'Poppins', sans-serif;
        }

        .stApp {
            background-color: #f0f4f8; /* Tom de azul-cinza claro e suave */
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* --- CONTÊINER PRINCIPAL PARA CENTRALIZAÇÃO --- */
        .main-container {
            width: 100%;
            max-width: 1200px;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 2rem;
        }

        /* --- TELA DE SELEÇÃO DE HISTÓRIAS --- */
        .selection-header {
            text-align: center;
            margin-bottom: 40px;
        }
        .selection-header h1 {
            font-weight: 700;
            color: #1e3a5f;
        }
        .selection-header p {
            font-size: 1.2rem;
            color: #5a7a9d;
        }

        .card-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 30px;
            width: 100%;
        }
        .story-card {
            background-color: #ffffff;
            border-radius: 20px;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 8px 24px rgba(20, 49, 89, 0.1);
            border: 1px solid #e6e9ee;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 25px 20px;
            height: 240px;
        }
        .story-card:hover {
            transform: translateY(-12px);
            box-shadow: 0 12px 32px rgba(20, 49, 89, 0.15);
        }
        .story-card .icon { font-size: 4.5rem; line-height: 1; }
        .story-card .title { font-size: 1.2rem; font-weight: 600; color: #1e3a5f; margin: 15px 0; }
        .story-card .stButton button {
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            width: 100%;
        }

        /* --- TELA DE JOGO (ESCOLHAS) --- */
        .game-card {
            background-color: #ffffff;
            padding: 50px 60px;
            border-radius: 20px;
            box-shadow: 0 8px 30px rgba(20, 49, 89, 0.1);
            width: 100%;
            max-width: 1000px;
            text-align: center;
            display: flex; /* Adicionado para controle de layout interno */
            flex-direction: column; /* Organiza os filhos em coluna */
            justify-content: center; /* Centraliza verticalmente o conteúdo */
            align-items: center; /* Centraliza horizontalmente o conteúdo */
        }
        .game-card .stage-icon { font-size: 4rem; color: #5a7a9d; }
        .game-card .question {
            font-size: 1.8rem;
            font-weight: 600;
            color: #1e3a5f;
            margin: 20px 0 40px 0;
            min-height: 100px; /* Garante altura mínima para o texto */
            display: flex; /* Para centralizar o texto da pergunta se for curto */
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .choice-buttons {
            display: flex;
            justify-content: center; /* Centraliza os botões */
            align-items: stretch; /* Faz os botões terem a mesma altura */
            gap: 20px; /* Espaço entre os botões */
            width: 100%; /* Ocupa a largura total */
            flex-wrap: wrap; /* Permite que os botões quebrem a linha em telas menores */
        }
        .choice-buttons .stButton {
            flex: 1; /* Permite que os botões se expandam igualmente */
            min-width: 250px; /* Largura mínima para botões em telas menores */
        }
        .choice-buttons .stButton button {
            background-color: transparent;
            color: #345c8c;
            border: 2px solid #d3e0ed;
            padding: 20px;
            font-size: 1.1rem;
            height: 100%; /* Para alinhar botões com textos de tamanhos diferentes */
            white-space: normal; /* Permite que o texto quebre a linha dentro do botão */
            text-align: center;
        }
        .choice-buttons .stButton button:hover {
            border-color: #007bff;
            background-color: #f0f8ff;
            color: #0056b3; /* Cor escura e legível no hover */
        }

        /* --- TELA FINAL (HISTÓRIA COMPLETA) --- */
        .final-story-card {
            background: #fff;
            padding: 50px 60px;
            border-radius: 20px;
            box-shadow: 0 8px 30px rgba(20, 49, 89, 0.1);
            width: 100%;
            max-width: 1000px;
            text-align: left;
            overflow-y: auto; /* Permite rolagem apenas nesta seção se o conteúdo for muito longo */
            max-height: 90vh; /* Altura máxima para evitar scroll da página inteira */
        }
        .final-story-card h1 { text-align: center; color: #1e3a5f; font-weight: 700; margin-bottom: 30px; }
        .final-story-card p {
            text-indent: 2.5em; /* Aumenta a indentação para melhor leitura */
            line-height: 1.9;
            font-size: 1.15rem;
            color: #333; /* Cor mais escura para melhor contraste */
            margin-bottom: 1.5em; /* Espaçamento entre parágrafos */
        }
        .alternative-ending { margin-top: 40px; padding: 25px; background-color: #f8f9fa; border-left: 6px solid #17a2b8; border-radius: 8px; }
        .alternative-ending h4 { color: #17a2b8; margin-top: 0; }
        .final-story-card .stButton button {
            width: 100%; margin-top: 30px; background-color: #28a745; color: white; border: none; padding: 15px; font-size: 1.2rem; border-radius: 12px;
        }

        /* --- Glossário --- */
        .glossary-section {
            margin-top: 50px;
            padding-top: 30px;
            border-top: 1px solid #e6e9ee;
        }
        .glossary-section h2 {
            text-align: center;
            color: #1e3a5f;
            margin-bottom: 25px;
            font-weight: 600;
        }
        .glossary-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); /* Responsivo */
            gap: 20px;
        }
        .glossary-item {
            background-color: #fefefe;
            border: 1px solid #e0e6ed;
            border-radius: 10px;
            padding: 15px 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        .glossary-item strong {
            color: #007bff;
            font-size: 1.1rem;
            margin-bottom: 5px;
            display: block;
        }
        .glossary-item p {
            font-size: 0.95rem;
            color: #555;
            line-height: 1.5;
            text-indent: 0 !important; /* Remove indentação para definição */
            margin-bottom: 0;
        }
    </style>
    """, unsafe_allow_html=True)

# --- GERENCIAMENTO DE ESTADO (sem alterações) ---
if 'etapa_app' not in st.session_state:
    st.session_state.etapa_app = 'selecao'
if 'historia_selecionada' not in st.session_state:
    st.session_state.historia_selecionada = None
if 'estagio_atual' not in st.session_state:
    st.session_state.estagio_atual = 0
if 'caminho_percorrido' not in st.session_state:
    st.session_state.caminho_percorrido = []

# --- FUNÇÕES DE RENDERIZAÇÃO DE TELA (RECONSTRUÍDAS) ---

def mostrar_tela_selecao():
    st.markdown("""
        <div class="main-container">
            <div class="selection-header">
                <h1>📚 Oficina de Histórias 🖋️</h1>
                <p>Escolha uma aventura e dê vida a uma nova história!</p>
            </div>
            <div class="card-grid">
    """, unsafe_allow_html=True)

    # Cria colunas para os cartões. O Streamlit gerencia o layout responsivo.
    cols = st.columns(5)
    sorted_historias = sorted(BANCO_DE_HISTORIAS.items())

    for i, (id_historia, detalhes) in enumerate(sorted_historias):
        with cols[i % 5]:
            # Usar st.container() para agrupar o markdown e o botão
            with st.container():
                st.markdown(f"""
                <div class="story-card">
                    <div>
                        <div class="icon">{detalhes['icone']}</div>
                        <div class="title">{detalhes['titulo']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Começar Aventura", key=f"btn_{id_historia}", use_container_width=True):
                    st.session_state.etapa_app = 'jogando'
                    st.session_state.historia_selecionada = id_historia
                    st.session_state.estagio_atual = 0
                    st.session_state.caminho_percorrido = []
                    st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)

def mostrar_tela_jogo():
    id_historia = st.session_state.historia_selecionada
    estagio = st.session_state.estagio_atual
    detalhes_historia = BANCO_DE_HISTORIAS[id_historia]
    detalhes_estagio = detalhes_historia['estagios'][estagio]

    st.markdown(f"""
        <div class="main-container">
            <div class="game-card">
                <div class="stage-icon">{detalhes_historia['icone']}</div>
                <p class="question">{detalhes_estagio['pergunta']}</p>
                <div class="choice-buttons">
    """, unsafe_allow_html=True)

    # Usar st.columns para distribuir os botões em 3 colunas
    cols = st.columns(3, gap="large")
    opcoes = list(detalhes_estagio['opcoes'].items())

    # Iterar pelas opções e colocá-las nas colunas
    for i, (opcao, fragmento) in enumerate(opcoes):
        with cols[i % 3]: # Isso garante que as opções se distribuam nas 3 colunas
            if st.button(opcao, key=f"opcao_{i}", use_container_width=True):
                st.session_state.caminho_percorrido.append(fragmento)
                if st.session_state.estagio_atual < 9:
                    st.session_state.estagio_atual += 1
                else:
                    st.session_state.etapa_app = 'final'
                st.rerun()

    st.markdown("</div></div></div>", unsafe_allow_html=True)


def mostrar_tela_final():
    id_historia = st.session_state.historia_selecionada
    detalhes_historia = BANCO_DE_HISTORIAS[id_historia]

    # --- LÓGICA DE TEXTO ROBUSTO ---
    # 1. Junta todos os fragmentos em um único texto.
    texto_completo = " ".join(st.session_state.caminho_percorrido)
    # 2. Divide o texto em sentenças. Usa regex para tratar diferentes pontuações.
    sentencas = re.split(r'(?<=[.!?])\s+', texto_completo)
    
    # 3. Agrupa as sentenças em 4 parágrafos de forma inteligente.
    paragrafos = ["", "", "", ""]
    num_sentencas = len(sentencas)
    if num_sentencas > 0:
        sentencas_por_paragrafo = (num_sentencas + 3) // 4 # Divisão arredondada para cima

        idx_paragrafo = 0
        for i, sentenca in enumerate(sentencas):
            if i > 0 and i % sentencas_por_paragrafo == 0 and idx_paragrafo < 3:
                idx_paragrafo += 1
            paragrafos[idx_paragrafo] += sentenca + " "
    else: # Caso raro de história vazia
        paragrafos = ["Sua história não possui conteúdo. Tente novamente!"]


    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="final-story-card">', unsafe_allow_html=True)
    st.markdown(f"<h1>{detalhes_historia['titulo']}</h1>", unsafe_allow_html=True)
    for p in paragrafos:
        if p.strip():
            st.markdown(f"<p>{p.strip()}</p>", unsafe_allow_html=True)

    # Lógica do final alternativo (mantida)
    fragmentos_alternativos = list(detalhes_historia['estagios'][9]['opcoes'].values())
    fragmento_atual_final = st.session_state.caminho_percorrido[-1]
    if fragmento_atual_final in fragmentos_alternativos:
        fragmentos_alternativos.remove(fragmento_atual_final)
    resumo_alternativo = random.choice(fragmentos_alternativos) if fragmentos_alternativos else "Não há outro caminho."

    st.markdown(f"""
    <div class="alternative-ending">
        <h4>E se você tivesse escolhido diferente?</h4>
        <p><em>Em um final alternativo, sua história poderia ter terminado assim: "{resumo_alternativo}" Explore outras escolhas para descobrir novos destinos!</em></p>
    </div>
    """, unsafe_allow_html=True)

    # --- GLOSSÁRIO ---
    st.markdown("""
        <div class="glossary-section">
            <h2>Glossário</h2>
            <div class="glossary-list">
    """, unsafe_allow_html=True)

    # Coleta palavras-chave relevantes da história e do glossário
    palavras_na_historia = set(re.findall(r'\b\w+\b', texto_completo.lower()))
    
    # Filtra o glossário para mostrar apenas palavras que aparecem na história OU que são importantes
    # E garante que apenas um número razoável de itens sejam mostrados.
    palavras_para_glossario = {}
    for palavra, definicao in GLOSSARIO.items():
        if palavra.lower() in palavras_na_historia or random.random() < 0.3: # Inclui algumas aleatórias
            palavras_para_glossario[palavra] = definicao
            if len(palavras_para_glossario) >= 8: # Limita a 8 itens para não sobrecarregar
                break
    
    # Se nenhuma foi encontrada, adiciona algumas aleatórias
    if not palavras_para_glossario and GLOSSARIO:
        chaves_aleatorias = random.sample(list(GLOSSARIO.keys()), min(3, len(GLOSSARIO)))
        for chave in chaves_aleatorias:
            palavras_para_glossario[chave] = GLOSSARIO[chave]

    for palavra, definicao in sorted(palavras_para_glossario.items()):
        st.markdown(f"""
            <div class="glossary-item">
                <strong>{palavra.capitalize()}:</strong>
                <p>{definicao}</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Criar uma Nova História"):
        st.session_state.etapa_app = 'selecao'
        # Limpa o estado para uma nova sessão de jogo
        for key in list(st.session_state.keys()):
            if key not in ['etapa_app']:
                del st.session_state[key]
        st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)


# --- LÓGICA PRINCIPAL DA APLICAÇÃO ---
injetar_css_moderno()

if st.session_state.etapa_app == 'selecao':
    mostrar_tela_selecao()
elif st.session_state.etapa_app == 'jogando':
    mostrar_tela_jogo()
elif st.session_state.etapa_app == 'final':
    mostrar_tela_final()
