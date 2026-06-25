import streamlit as st
from utils.styles import load_css

load_css()  
pages = [
    st.Page(page="pages/sales.py", title="Sales", icon=":material/bar_chart:"),
    st.Page(page="pages/customer.py", title="Customer", icon=":material/diversity_3:"),
    st.Page(page="pages/product.py", title="Product", icon=":material/package_2:"),
]

pg = st.navigation(pages, position="sidebar", expanded=True)

pg.run()