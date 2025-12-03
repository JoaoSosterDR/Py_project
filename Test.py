

import streamlit as st
import pandas as pd

# -------------------------------
# Inicialização do estado da aplicação
# -------------------------------
if "dealers" not in st.session_state:
    # Dados iniciais simulados com todos os campos
    st.session_state.dealers = pd.DataFrame([{
        "Sold to (Short Name)": "Dealer A",
        "Sold to (Sap Code)": "1001",
        "Sold to (Flex Code)": "F001",
        "City": "Campinas",
        "State": "SP",
        "SO Carrier": "Carrier X",
        "Active": "Sim",
        "CNPJ": "12.345.678/0001-99",
        "Distance (KM)": 15,
        "Lat": -22.90,
        "Long": -47.06,
        "Country": "Brasil",
        "Region": "Sudeste",
        "Product Agreement": "PA-01",
        "Store Type": "Loja Física",
        "TT-SO - ZPIS": "OK",
        "TT-STD-ZPIR": "OK",
        "TT EXP Air DHL": "OK",
        "TT EXP Road DHL": "OK",
        "Cut Off Picking ZPIS": "18:00",
        "Cut Off Picking STD": "17:00",
        "Cut Off Shipping STD": "20:00",
        "Cut Off Shipping EXP": "22:00"
    }])

if "modo" not in st.session_state:
    st.session_state.modo = "listar"
if "dealer_edit" not in st.session_state:
    st.session_state.dealer_edit = None

# -------------------------------
# Funções auxiliares
# -------------------------------
def reset_modo():
    st.session_state.modo = "listar"
    st.session_state.dealer_edit = None

def adicionar_dealer(dados):
    st.session_state.dealers = pd.concat([st.session_state.dealers, pd.DataFrame([dados])], ignore_index=True)

def editar_dealer(index, dados):
    st.session_state.dealers.loc[index] = dados

def apagar_dealer(index):
    st.session_state.dealers = st.session_state.dealers.drop(index).reset_index(drop=True)

# -------------------------------
# Layout principal
# -------------------------------
st.title("Controle de Concessionários (Dealers)")

aba = st.tabs(["Lista de Dealers", "Adicionar Dealer"])

# -------------------------------
# Aba 1: Lista de Dealers (sem ações)
# -------------------------------
with aba[0]:
    st.subheader("Lista de Dealers")
    # Apenas exibe a tabela, sem botões de ação
    st.dataframe(st.session_state.dealers, use_container_width=True, height=600)


# -------------------------------
# Aba 2: Adicionar Dealer
# -------------------------------
with aba[1]:
    st.subheader("Adicionar Novo Dealer")

    # Lista de campos na ordem definida
    campos = [
        "Sold to (Short Name)", "Sold to (Sap Code)", "Sold to (Flex Code)", "City", "State",
        "Carrier","Ship Via", "Active", "CNPJ", "Distance (KM)", "Lat", "Long", "Country", "Region",
        "Product Agreement", "Store Type", "Stock order - ZPIS", "Machine Down - ZPIR", "Expresso DHL",
        "Cut Off Picking ZPIS", "Cut Off Picking ZPIR", "Cut Off Shipping ZPIR",
        "Cut Off Shipping EXP"
    ]

    # Dicionário para armazenar os dados do novo dealer
    novo_dealer = {}

    # Loop para criar os inputs dinamicamente
    for campo in campos:
        # Campos numéricos
        if campo in ["Distance (KM)", "Lat", "Long"]:
            novo_dealer[campo] = st.number_input(campo, value=0.0)

        # Campo Active com opções Sim/Não
        elif campo == "Active":
            novo_dealer[campo] = st.selectbox(campo, ["Sim", "Não"])

        # Campo Product Agreement com opções C&F e A&T
        elif campo == "Product Agreement":
            novo_dealer[campo] = st.selectbox(campo, ["C&F", "A&T"])

        # Demais campos como texto
        else:
            novo_dealer[campo] = st.text_input(campo)

    # Botão para salvar novo dealer
    if st.button("Salvar Novo Dealer"):
        if novo_dealer["Sold to (Short Name)"]:
            adicionar_dealer(novo_dealer)
            st.success(f"Dealer '{novo_dealer['Sold to (Short Name)']}' adicionado com sucesso!")
        else:
            st.error("Preencha pelo menos o nome do Dealer.")



# -------------------------------
# Modo Editar (Sidebar)
# -------------------------------
if st.session_state.modo == "editar" and st.session_state.dealer_edit is not None:
    st.sidebar.subheader("Editar Dealer")
    index, dealer = st.session_state.dealer_edit
    editado = {}
    for campo in campos:
        if campo in ["Distance (KM)", "Lat", "Long"]:
            editado[campo] = st.sidebar.number_input(campo, value=float(dealer[campo]))
        elif campo == "Active":
            editado[campo] = st.sidebar.selectbox(campo, ["Sim", "Não"], index=0 if dealer[campo] == "Sim" else 1)
                
        else:
            editado[campo] = st.sidebar.text_input(campo, dealer[campo])

    if st.sidebar.button("Salvar Alterações"):
        editar_dealer(index, editado)
        st.sidebar.success("Dealer atualizado com sucesso!")
        reset_modo()

    if st.sidebar.button("Cancelar"):
        reset_modo()
    
# -------------------------------
# Fim do código         