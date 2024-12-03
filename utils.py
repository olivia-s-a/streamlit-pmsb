import streamlit as st


def title_numbered_blue_dot(num, title_name):
    st.markdown(f"""
        <ul>
            <li style="font-size: 18px; display: flex; align-items: center;">
                <div style="width: 30px; height: 30px; background-color: #3498db; border-radius: 50%; color: white; display: flex; justify-content: center; align-items: center; margin-right: 10px;">{num}</div>
                <strong>{title_name}</strong>
            </li>
        </ul>
    """,
    unsafe_allow_html=True)

def columns_bullet_list(title_bullet_list, itens):
    st.markdown(f"<h5>{title_bullet_list}</h5>", unsafe_allow_html=True)

    cols = st.columns(len(itens))  
    for a, item in enumerate(itens):
        col = cols[a]  
        with col:
            st.markdown(f"<p><strong>{a + 1}. {item[0]}</strong><br> {item[1]}</p>", unsafe_allow_html=True)

def popover_metodologia(name_popover, metodologia, obstaculos):
    lines = [line for line in metodologia.splitlines() if line.strip()]
    with st.popover(name_popover):
        st.subheader(name_popover)
        st.markdown(
            "<ol>" + "".join([f"<li>{line}</li>" for line in lines]) + "</ol>", unsafe_allow_html=True)

        st.subheader("Obstáculos")
        st.text(obstaculos)