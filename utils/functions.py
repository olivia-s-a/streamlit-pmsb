import folium
import streamlit as st
from streamlit_folium import st_folium


def title_numbered_blue_dot(num, title_name):
    col_bd1, col_bd2 =st.columns([0.2, 0.7])

    with col_bd1:
        st.markdown(f"""
            <p class = "li-blue-dot">
                <div class = "blue-dot">{num}.</div>""", 
            unsafe_allow_html=True)
    with col_bd2:
        st.markdown(f"""
            <p class = "li-blue-dot">
                <div class = "title-blue-dot">{title_name}</div>""", 
            unsafe_allow_html=True)
    
    st.container(height= 2, border=False)

def columns_bullet_list(title_bullet_list, itens):
    st.markdown(f"<h5>{title_bullet_list}</h5>", unsafe_allow_html=True)

    cols = st.columns(len(itens))  
    for a, item in enumerate(itens):
        col = cols[a]  
        with col:
            st.markdown(
                f"""<p >
                    <strong>
                        {a + 1}. {item[0]}
                    </strong>
                    <br> 
                    <div class = "description-bullet-list">{item[1]}</div>
                </p>""",
                unsafe_allow_html=True
            )

def popover_metodologia(name_popover, metodologia, obstaculos):
    lines = [line for line in metodologia.splitlines() if line.strip()]
    with st.popover(name_popover):
        st.subheader(name_popover)
        st.markdown(
            "<ol>" 
            + ""
            .join(
                [f"""
                    <li>{line}</li>
                """ for line in lines]
            ) 
            + 
            "</ol>", 
            unsafe_allow_html=True
        )

        st.subheader("Obstáculos")
        st.text(obstaculos)

def map_1(gdf_unidade, columns_names):
    m = folium.Map(
        tiles = "Cartodb Positron",
        zoom_control=False,
        scrollWheelZoom = False,
        dragging = True
        )
    
    gdf_unidade.explore(
        m = m,
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
    minx += 0.25
    bounds=[(miny, minx),(maxy, maxx)]
    m.fit_bounds(bounds)
    
    plot_map = st_folium(m, height=600)




