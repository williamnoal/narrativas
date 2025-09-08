import streamlit as st
import google.generativeai as genai
import json

# --- Configuração da Página ---
# Interface moderna, minimalista e sem scroll horizontal, ideal para Chromebooks.
st.set_page_config(
    page_title="Fábrica de Narrativas",
    page_icon="📖",
    layout="centered" # Layout centralizado foca na história
)

# --- Configuração e Conexão Segura com o Modelo Generativo ---
try:
    # Método seguro para buscar a chave da API, essencial para publicação no GitHub.
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
except Exception:
    # Mensagem de erro clara caso a chave não seja configurada no ambiente de deploy.
    st.error("A conexão com o Mestre das Histórias não foi estabelecida. O administrador precisa configurar a chave de acesso.", icon="🔑")
    st.stop()

# --- Funções Principais ---

def gerar_conteudo_historia(prompt):
    """
    Função robusta para chamar o modelo generativo.
    Envia um prompt e processa a resposta, esperando um JSON bem-formado.
    """
    # Instrução aprimorada para o modelo, focando na consistência da saída JSON.
    # Esta técnica de "prompt engineering" é crucial para a estabilidade da aplicação.
    instrucao_sistema = """
    Você é um Mestre de Histórias para estudantes do sexto ano. Sua única função é gerar
    respostas em um formato JSON específico. NUNCA responda com texto comum ou explicações.
    Sua resposta DEVE ser um único bloco de código JSON com as seguintes chaves:
    1. "texto": Uma string contendo o próximo parágrafo da história (entre 40 e 70 palavras).
    2. "opcoes": Uma lista de exatamente 3 strings, cada uma sendo uma opção de escolha para o jogador.
       Se a história chegou a um final conclusivo, retorne uma lista vazia: [].
    A história deve ser criativa, apropriada para a idade e continuar o enredo fornecido.
    Exemplo de saída válida:
    {
        "texto": "Você segue o brilho misterioso e encontra uma clareira. No centro, uma raposa com pelos prateados te observa com olhos inteligentes.",
        "opcoes": ["Tentar fazer amizade com a raposa.", "Observar de longe.", "Ignorar a raposa e seguir em frente."]
    }
    """
    try:
        response = model.generate_content([instrucao_sistema, prompt])
        # Limpeza rigorosa da resposta para extrair apenas o conteúdo JSON.
        # Isso previne erros caso o modelo, por engano, adicione marcadores de código (```json).
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(json_text)
    except (json.JSONDecodeError, KeyError) as e:
        # Tratamento de erro específico para JSON inválido ou chaves faltando.
        st.error("O Mestre das Histórias parece confuso e retornou uma página em branco. Por favor, tente novamente.", icon="📜")
        return None
    except Exception as e:
        # Tratamento de erro genérico para problemas de API (ex: sobrecarga, falha de conexão).
        st.error(f"Houve uma falha na comunicação com o mundo das histórias. Tente recomeçar.", icon="⚡")
        return None

# --- Gerenciamento de Estado da Sessão ---
# Usar st.session_state é a forma correta de manter os dados durante a navegação do usuário.
if 'etapa' not in st.session_state:
    st.session_state.etapa = 'inicio' # Controla qual tela é exibida
if 'historico' not in st.session_state:
    st.session_state.historico = [] # Armazena os parágrafos da história
if 'tema' not in st.session_state:
    st.session_state.tema = ""

# --- Interface do Usuário ---

# ETAPA 1: TELA INICIAL
if st.session_state.etapa == 'inicio':
    st.title("📖 Fábrica de Narrativas Interativas ✨")
    st.markdown("### Uma aventura que se cria a cada escolha sua!")
    
    tema_input = st.text_input(
        "Qual será o tema da sua jornada? Comece com uma ideia:",
        placeholder="Ex: um mistério no laboratório da escola, uma viagem a um planeta de cristal..."
    )
    
    if st.button("Criar Aventura!", type="primary"):
        if tema_input:
            st.session_state.tema = tema_input
            with st.spinner("As páginas da sua aventura estão sendo escritas..."):
                prompt_inicial = f"Inicie uma história de aventura com o tema: '{st.session_state.tema}'"
                dados_historia = gerar_conteudo_historia(prompt_inicial)
            
            if dados_historia:
                st.session_state.historico = [dados_historia]
                st.session_state.etapa = 'jogando'
                st.experimental_rerun()
        else:
            st.warning("Toda grande história precisa de um começo. Por favor, digite um tema.")

# ETAPA 2: TELA DA AVENTURA
elif st.session_state.etapa == 'jogando':
    st.title("📖 A Sua Aventura")
    
    # Exibe o histórico da narrativa
    for i, parte in enumerate(st.session_state.historico):
        st.markdown(f"> {parte['texto']}")
        st.markdown("---")

    parte_atual = st.session_state.historico[-1]
    
    # Verifica se a história chegou ao fim (lista de opções vazia).
    if not parte_atual["opcoes"]:
        st.success("FIM DA AVENTURA!")
        st.balloons()
    else:
        st.subheader("O que você faz agora?")
        for opcao in parte_atual["opcoes"]:
            if st.button(opcao, key=opcao, use_container_width=True):
                with st.spinner("O destino está sendo traçado..."):
                    # Constrói o contexto da história para dar continuidade
                    contexto = f"O tema inicial era: '{st.session_state.tema}'.\n"
                    for p in st.session_state.historico:
                        contexto += p['texto'] + " "
                    
                    prompt_continuacao = f"Contexto da história: {contexto}\nA última escolha do jogador foi: '{opcao}'. Continue a história a partir daí."
                    
                    novos_dados = gerar_conteudo_historia(prompt_continuacao)
                    if novos_dados:
                        st.session_state.historico.append(novos_dados)
                        st.experimental_rerun()
    
    # Botão para reiniciar a qualquer momento
    if st.button("Começar uma Nova História", type="secondary"):
        st.session_state.etapa = 'inicio'
        st.session_state.historico = []
        st.session_state.tema = ""
        st.experimental_rerun()
