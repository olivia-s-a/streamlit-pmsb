import streamlit as st
import geopandas as gpd
import pandas as pd
import leafmap.foliumap as leafmap
from folium import LayerControl, TileLayer
from os.path import join
import utils





# Dados
distrito = gpd.read_file(join("data", "2024_11_26", "03_consumo_distrito"))
subbac = gpd.read_file(join("data", "2024_11_26", "03_consumo_subbac"))
subpref = gpd.read_file(join("data", "2024_11_26", "03_consumo_subprefeitura"))
fcu = gpd.read_file(join("data", "2024_11_26", "pop_fcu"))
#https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios_preliminares/malha_com_atributos/setores/shp/UF/SP/SP_Malha_Preliminar_2022.zip

unidades_list = [
    ("Subprefeituras", "Lorem ipsum dolor sit amet...", 'subpref', 'nm_subpref'),
    ("Distritos", "Lorem ipsum dolor sit amet...", 'distrito', 'nm_distrit'),
    ("Favelas e Comunidades Urbanas", "Lorem ipsum dolor sit amet...", 'fcu', 'nm_fcu'),
    ("Sub Bacias Hidrográficas", "Lorem ipsum dolor sit amet...", 'subbac', 'nm_bacia_h')
]
unidades = pd.DataFrame(unidades_list, columns=['name', 'desc', 'gdf_name', 'column_name'])


# Cabeçalho
st.title("Dados de Abastecimento de Água")
st.header("Metodologia de análise dos dados | PMSB 2024 | CODATA")
st.text("Este material tem por objetivo registrar a metodologia referente ao processamento de dados elaborado por Codata para a elaboração do diagnóstico do Plano Municipal de Saneamento Básico (2024/2025). Nesse sentido, ele deve ser resultado de um processo enquanto as análises estão sendo realizadas.")


#testes
import random
num_rand = random.randint(1, 45)
abc = random.choice(["a", "b", "c"])
num_rand
abc
st.dataframe(fcu)

# 1: Cálculo populacional e de domicílios com base no Censo 2022
utils.title_numbered_blue_dot(num = 1, title_name = "Cálculo populacional e de domicílios com base no Censo 2022")

utils.columns_bullet_list(
    title_bullet_list = "Desagregado por", 
    itens=unidades_list)



sum_mun = distrito['pop_total'].sum()
st.markdown("<h5>Total do Município</h5>", unsafe_allow_html=True)
st.subheader(f'{sum_mun:,} pessoas'.replace(",", "."))

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

if name_gdf_unidade == 'fcu':
        pop_column = 'pop_fcu'
else:
        pop_column = 'pop_total'
if choice_name !=None:
    sum_unidade = (
            gdf_unidade[
                gdf_unidade[name_column_unidade]==choice_name
            ]
            [pop_column]
            .values[0]
        )
else:
    sum_unidade = gdf_unidade[pop_column].sum()

st.subheader(f'{sum_unidade:,} pessoas'.replace(",", "."))


columns_names ={
    name_column_unidade : 'Unidade',
    pop_column: 'População'
}
cols_b1, cols_b2 = st.columns(2)
with cols_b1:
    m1 = leafmap.Map(tiles = "Cartodb Positron")
    
    gdf_unidade.explore(
        m = m1,
        color= '#0D04FF',
        tooltip=list(columns_names.keys()),
        tooltip_kwds={
            'aliases': list(columns_names.values()),
            'localize': True
        },
        popup=list(columns_names.keys()),
        popup_kwds={
            'aliases': list(columns_names.values()),
            'localize': True
        }
    )
    minx, miny, maxx, maxy = gdf_unidade.to_crs('EPSG:4326').total_bounds
    bounds=[(miny, minx),(maxy, maxx)]
    m1.fit_bounds(bounds)
    st.components.v1.html(m1.to_html(), height=600)
with cols_b2:
    st.dataframe(
        gdf_unidade[
            [name_column_unidade, pop_column]
        ].sort_values(
            by =pop_column,
            ascending = False
        ),
        height=600,
        column_config=columns_names,
        hide_index=True
    )


with st.popover("Metodologia Completa de Cálculo de População"):
    st.markdown("""
        <ol >
            <li>Foram utilizadas as malhas disponíveis em duas bases de dados principais, a do Censo Demográfico de 2022, com as informações agregadas por setores censitários disponibilizada pelo IBGE1; e as das malhas das unidades de desagregação, disponibilizadas pelo GeoSampa2.</li>
            <li>Para a maior parte das unidades, nós selecionamos apenas os setores censitários que correspondessem ao município de São Paulo, mas para as sub bacias hidrográficas, que não se enquadram na precisão das fronteiras municipais, foram selecionados todos os municípios que tivessem ao menos alguma parte de seu território interseccionando com alguma das sub bacias da malha.</li> 
            <li>Para trabalhar com ambas as malhas, calculamos a similaridade entre elas, e realizamos a intersecção (com o método “overlay intersection” de uma biblioteca do Python chamada GeoPandas). Fizemos o cálculo de cada unidade individualmente, mas o processo permaneceu o mesmo na maioria dos casos. </li>
            <li>Primeiro, identificamos as áreas de interseção, ou seja, as regiões onde os polígonos dos setores e das unidades se sobrepõe. e fazemos um recorte disso. Ou seja se há um setor que fica dividido pelo contorno de dois ou mais polígonos da unidade, dividiremos esse setor seguindo o contorno da unidade. Contudo, estabelecemos um tamanho mínimo de  10m para essas intersecções, evitando que uma falsa intersecção permanecesse. </li>
            <li>Calculando a área desses setores antes e após a intersecção, para realizarmos para cada polígono da intersecção o cálculo da porcentagem de área que ela representa do setor total (área da intersecção/área total do setor).</li>
            <li>Para calcular o valor correspondente dos indicadores em cada intersecção, multiplicamos seus valores por sua percentagem da área do setor (valor do indicador total do setor * porcentagem da área do setor que corresponde ao polígono). Assim, é considerado que a variável, seja ela, por exemplo, população ou domicílios, está homogeneamente distribuída no setor e, portanto, a distribuição de seus valores pode ser equivalida à área da intersecção. </li>
        </ol>
        """, 
        unsafe_allow_html=True
    )

    st.subheader("Obstáculos")
    st.text("""
        Há uma incompatibilidade entre o limite municipal da malha do IBGE e a do GeoSampa, de forma que ao realizar o cálculo das intersecções alguns setores censitários ficaram para fora, enquanto regiões que deveriam ter setores estavam vazias. Para resolver isso, adicionamos os setores que haviam ficado de fora, independente da razão, manualmente. 
        Nossa metodologia não permite que identifiquemos precisamente a distribuição das variáveis em casos onde elas são distribuídas de forma não homogênea. 
    """)


# 2. Demanda da População por água
utils.title_numbered_blue_dot(num = 2, title_name = "Demanda da População por água")

utils.columns_bullet_list(
    title_bullet_list = "Desagregado por", 
    itens=unidades_list
)

with st.container(border=True):
    cols_c1, cols_c2 = st.columns(2)
    with cols_c1:
        st.text("Consumo por pessoa")
        st.subheader("140 L/dia")
    with cols_c2:
        st.text("População por setor")
        st.markdown("<h3>População <i>α</i></h3>", unsafe_allow_html=True)
    
    st.text("Demanda estimada por setor")
    st.markdown("<h3>População <i>α</i> X 140</h3>", unsafe_allow_html=True)

st.markdown(
    """<p><strong>Acesso aos materiais</strong></p>
    <ol>
        <li>Shapefiles</li>
        <li>Mapas Interativos</li>
        <li>Notebooks</li>
    </ol>
    """,
    unsafe_allow_html=True)





