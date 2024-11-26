import streamlit as st
import geopandas as gpd
import pandas as pd
from os.path import join
import random



# Dados
distrito = gpd.read_file(join("data", "2024_11_26", "03_consumo_distrito"))
subbac = gpd.read_file(join("data", "2024_11_26", "03_consumo_subbac"))
subpref = gpd.read_file(join("data", "2024_11_26", "03_consumo_subprefeitura"))
fcu = gpd.read_file(join("data", "2024_11_26", "pop_fcu"))
#https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios_preliminares/malha_com_atributos/setores/shp/UF/SP/SP_Malha_Preliminar_2022.zip

itens = [
    ("Subprefeituras", "Lorem ipsum dolor sit amet...", 'subpref', 'nm_subpref'),
    ("Distritos", "Lorem ipsum dolor sit amet...", 'distrito', 'nm_distrit'),
    ("Favelas e Comunidades Urbanas", "Lorem ipsum dolor sit amet...", 'fcu', 'nm_fcu'),
    ("Sub Bacias Hidrográficas", "Lorem ipsum dolor sit amet...", 'subbac', 'nm_bacia_h')
]
unidades = pd.DataFrame(itens, columns=['name', 'desc', 'gdf_name', 'column_name'])


# Cabeçalho
st.title("Dados de Abastecimento de Água")
st.header("Metodologia de análise dos dados | PMSB 2024 | CODATA")
st.text("Este material tem por objetivo registrar a metodologia referente ao processamento de dados elaborado por Codata para a elaboração do diagnóstico do Plano Municipal de Saneamento Básico (2024/2025). Nesse sentido, ele deve ser resultado de um processo enquanto as análises estão sendo realizadas.")


#testes
num_rand = random.randint(1, 85)
num_rand
st.dataframe(fcu)

# 1: Cálculo populacional e de domicílios com base no Censo 2022
st.markdown("""
    <ul>
        <li style="font-size: 18px; display: flex; align-items: center;"> 
            <div style="width: 30px; height: 30px; background-color: #3498db; border-radius: 50%; color: white; display: flex; justify-content: center; align-items: center; margin-right: 10px;">1</div>
            <h3>Cálculo populacional e de domicílios com base no Censo 2022</h3>
        </li>
    </ul>
""", unsafe_allow_html=True)

st.markdown("<h5>Desagregado por</h5>", unsafe_allow_html=True)

cols_a = st.columns(len(itens))  
for a, item in enumerate(itens):
    col = cols_a[a]  
    with col:
        st.markdown(f"<p><strong>{a + 1}. {item[0]}</strong><br> {item[1]}</p>", unsafe_allow_html=True)



sum_mun = distrito['pop_total'].sum()
st.markdown("<h5>Total do Município</h5>", unsafe_allow_html=True)
st.subheader(f'{sum_mun} pessoas')

choice_unidade = st.selectbox("", unidades['name'])

name_gdf_unidade= (
    unidades[unidades['name']==choice_unidade]
    ['gdf_name']
    .values[0]
)
name_column_unidade= (
    unidades[unidades['name']==choice_unidade]
    ['column_name']
    .values[0]
)
gdf_unidade = locals()[name_gdf_unidade]

choice_name = st.selectbox(
    "", 
    gdf_unidade[name_column_unidade], 
    index=None, 
    placeholder= "Escolha uma unidade..."
    )

if choice_name !=None:
    if name_gdf_unidade == 'fcu':
        pop_column = 'pop_fcu'
    else:
        pop_column = 'pop_total'
    
    sum_unidade = (
            gdf_unidade[
                gdf_unidade[name_column_unidade]==choice_name
            ]
            [pop_column]
            .values[0]
        )
else:
    sum_unidade = sum_mun

st.subheader(f'{sum_unidade} pessoas')



cols_b1, cols_b2 = st.columns(3)











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
