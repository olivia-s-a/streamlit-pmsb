import streamlit as st

# Cabeçalho com bolinhas

# Título
st.title("Dados de Abastecimento de Água")
st.subheader("Metodologia de análise dos dados | PMSB 2024 | CODATA")
st.text("Este material tem por objetivo registrar a metodologia referente ao processamento de dados elaborado por Codata para a elaboração do diagnóstico do Plano Municipal de Saneamento Básico (2024/2025). Nesse sentido, ele deve ser resultado de um processo enquanto as análises estão sendo realizadas.")

# Listagem com bolinhas azuis e o primeiro item
st.markdown("""
    <ul>
        <li style="font-size: 18px; display: flex; align-items: center;">
            <div style="width: 30px; height: 30px; background-color: #3498db; border-radius: 50%; color: white; display: flex; justify-content: center; align-items: center; margin-right: 10px;">1</div>
            <h4>Cálculo populacional e de domicílios com base no Censo 2022</h4>
        </li>
    </ul>
""", unsafe_allow_html=True)

st.markdown("<h5>Desagregado por</h5>", unsafe_allow_html=True)

# Criando as colunas
col1, col2, col3 = st.columns(3)

# Abrindo a lista ordenada antes das colunas

# futuramente arrumar esse 1... o ideal era que fosse um <ol><li>
with col1:
    st.markdown("<p><strong>1. Distrito</strong><br> Lorem ipsum dolor sit amet...</p>", unsafe_allow_html=True) 
with col2:
    st.markdown("<p><strong>2. Sub bacias</strong><br>Lorem ipsum dolor sit amet...</p>", unsafe_allow_html=True)
with col3:
    st.markdown("<p><strong>3. Setor censitário</strong> <br> Lorem ipsum dolor sit amet...</p>", unsafe_allow_html=True)

# Fechando a lista ordenada após as colunas
st.markdown("</ol>", unsafe_allow_html=True)


# 2. Demanda da População por água
st.markdown("""
    <ul>
        <li style="font-size: 18px; display: flex; align-items: center;">
            <div style="width: 30px; height: 30px; background-color: #3498db; border-radius: 50%; color: white; display: flex; justify-content: center; align-items: center; margin-right: 10px;">2</div>
            <strong>Demanda da população por água</strong>
        </li>
    </ul>
""", unsafe_allow_html=True)

# Teste com for 
st.markdown("<h5>Desagregado por</h5>", unsafe_allow_html=True)

# Lista de itens
itens = [
    ("Distrito", "Lorem ipsum dolor sit amet..."),
    ("Sub bacias", "Lorem ipsum dolor sit amet..."),
    ("Setor censitário", "Lorem ipsum dolor sit amet..."),
    ("Assentamentos Precários", "Lorem ipsum dolor sit amet...")
]

# Definindo o número de colunas baseado no número de itens
num_colunas = len(itens)
colunas = st.columns(num_colunas)  # Gera automaticamente a quantidade de colunas conforme o número de itens

# Gerando os itens nas colunas
for i, item in enumerate(itens):
    col = colunas[i]  # Acessando dinamicamente a coluna correspondente
    with col:
        st.markdown(f"<p><strong>{i + 1}. {item[0]}</strong><br> {item[1]}</p>", unsafe_allow_html=True)