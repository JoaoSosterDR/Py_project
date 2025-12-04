
import streamlit as st
import pandas as pd

# -------------------------------
# CONFIGURAÇÃO INICIAL DA PÁGINA
# -------------------------------
st.set_page_config(page_title="Cadastro de Dealers", layout="wide")

# CSS customizado para melhorar aparência
st.markdown("""
<style>
    body {
        background-color: #f5f5f5;
        font-family: Arial, sans-serif;
    }
    .main-title {
        color: #205B2F;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .stTabs [role="tablist"] {
        justify-content: center;
        gap: 20px;
    }
    .stTabs [role="tab"] {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: bold;
    }
    .stTabs [role="tab"]:hover {
        background-color: #45a049;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

st.title("Cadastro de Dealers")

# -------------------------------
# INICIALIZAÇÃO DO ESTADO
# -------------------------------
# Mantemos os dados em memória usando st.session_state
if "dealers" not in st.session_state:
    st.session_state.dealers = pd.DataFrame(columns=[
        "Nome", "SAP Code", "Flex Code", "Cidade", "Estado", "Carrier", "Ship Via",
        "Ativo", "CNPJ", "Distância (KM)", "Lat", "Long", "País", "Região",
        "Product Agreement", "Tipo Loja", "Stock Order", "Machine Down", "Expresso DHL",
        "Cut Off Picking ZPIS", "Cut Off Picking ZPIR", "Cut Off Shipping ZPIR", "Cut Off Shipping EXP"
    ])

if "modo" not in st.session_state:
    st.session_state.modo = "listar"
if "dealer_edit" not in st.session_state:
    st.session_state.dealer_edit = None

# -------------------------------
# FUNÇÕES AUXILIARES (futuro: substituir por queries SQL)
# -------------------------------
def reset_modo():
    """Reseta o modo para listar e limpa dealer em edição."""
    st.session_state.modo = "listar"
    st.session_state.dealer_edit = None

def adicionar_dealer(dados):
    """Adiciona um novo dealer ao DataFrame."""
    st.session_state.dealers = pd.concat([st.session_state.dealers, pd.DataFrame([dados])], ignore_index=True)

def editar_dealer(index, dados):
    """Edita dealer existente pelo índice."""
    st.session_state.dealers.loc[index] = dados

def apagar_dealer(index):
    """Remove dealer pelo índice."""
    st.session_state.dealers = st.session_state.dealers.drop(index).reset_index(drop=True)

# -------------------------------
# INTERFACE PRINCIPAL
# -------------------------------
aba = st.tabs(["Lista de Dealers", "Adicionar Dealer"])

# -------------------------------
# ABA 1: LISTA DE DEALERS
# -------------------------------
with aba[0]:
    st.subheader("Lista de Dealers")
    if st.session_state.dealers.empty:
        st.info("Nenhum dealer cadastrado ainda.")
    else:
        # Exibe lista com botões Editar e Excluir
        for i, row in st.session_state.dealers.iterrows():
            col1, col2, col3 = st.columns([4, 1, 1])
            col1.write(f"**{row['Nome']}** - {row['Cidade']}/{row['Estado']}")
            if col2.button("Editar", key=f"edit_{i}"):
                st.session_state.modo = "editar"
                st.session_state.dealer_edit = (i, row)
            if col3.button("Excluir", key=f"del_{i}"):
                apagar_dealer(i)
                st.warning(f"Dealer '{row['Nome']}' excluído.")
                st.rerun()

        # Exibe tabela completa
        st.dataframe(st.session_state.dealers, use_container_width=True)

# -------------------------------
# ABA 2: ADICIONAR DEALER
# -------------------------------
with aba[1]:
    st.subheader("Adicionar Novo Dealer")
    campos = list(st.session_state.dealers.columns)
    novo_dealer = {}

    # Inputs dinâmicos
    for campo in campos:
        if campo in ["Distância (KM)", "Lat", "Long"]:
            novo_dealer[campo] = st.number_input(campo, value=0.0)
        elif campo == "Ativo":
            novo_dealer[campo] = st.selectbox(campo, ["Sim", "Não"])
        elif campo == "Product Agreement":
            novo_dealer[campo] = st.selectbox(campo, ["C&F", "A&T"])
        else:
            novo_dealer[campo] = st.text_input(campo)

    # Botão salvar
    if st.button("Salvar Novo Dealer"):
        if novo_dealer["Nome"]:
            adicionar_dealer(novo_dealer)
            st.success(f"Dealer '{novo_dealer['Nome']}' adicionado com sucesso!")
            st.rerun()
        else:
            st.error("Preencha pelo menos o nome do Dealer.")

# -------------------------------
# SIDEBAR: EDITAR DEALER
# -------------------------------
if st.session_state.modo == "editar" and st.session_state.dealer_edit is not None:
    st.sidebar.subheader("Editar Dealer")
    index, dealer = st.session_state.dealer_edit
    editado = {}

    for campo in campos:
        valor_atual = dealer[campo]
        if campo in ["Distância (KM)", "Lat", "Long"]:
            editado[campo] = st.sidebar.number_input(campo, value=float(valor_atual))
        elif campo == "Ativo":
            editado[campo] = st.sidebar.selectbox(campo, ["Sim", "Não"], index=0 if valor_atual == "Sim" else 1)
        elif campo == "Product Agreement":
            editado[campo] = st.sidebar.selectbox(campo, ["C&F", "A&T"], index=0 if valor_atual == "C&F" else 1)
        else:
            editado[campo] = st.sidebar.text_input(campo, value=str(valor_atual))

    if st.sidebar.button("Salvar Alterações"):
        if editado["Nome"]:
            editar_dealer(index, editado)
            st.sidebar.success(f"Dealer '{editado['Nome']}' atualizado com sucesso!")
            reset_modo()
            st.rerun()
        else:
            st.sidebar.error("O campo 'Nome' não pode ficar vazio.")

    if st.sidebar.button("Cancelar"):
        reset_modo()
        st.rerun()
