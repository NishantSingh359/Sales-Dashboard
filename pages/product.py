import streamlit as st
from utils.kpis import ProductKPIs
from utils.common import fact_sales, product,year_filter, metric, bar_chart, text

st.set_page_config(page_title='Product', layout='wide')

st.title(":material/package_2: Product")
st.space()

df = fact_sales()
df1 = product()

with st.sidebar:
    st.title(":material/filter_alt: Filters")
    year = ["All"] + df['prd_added_year'].unique().tolist()
    filter1 = st.sidebar.selectbox("Year", year, index=0, key='product_year')
    
kpi1 = ProductKPIs(df)
kpi2 = ProductKPIs(df1)

chart1 = ProductKPIs(year_filter(df, 'prd_added_year', filter1))
chart2 = ProductKPIs(year_filter(df1, 'prd_added_year', filter1))

# =======================================
# FIRST ROW
# =======================================

col1, col2 = st.columns([2,8], gap="medium")

df = year_filter(kpi2.total_product(), 'year', filter1)
value = df["product"].sum()
with col1:
    metric(
        key=23,
        kpi_name="Total Product",
        value=value,
        data=df,
        x='year',
        y='product',
        tipname1='Year',
        tipname2='Product',
        tipname3='Growth'
    )

with col2:
    text("Product by Sub Category")
    bar_chart(
        key=30,
        data=chart2.product_by_sub_category(),
        x='subcategory',
        y='product',
        xtitle='Sub_Category',
        ytitle='Total Product',
        height=330
    )

# =======================================
# SECOND ROW
# =======================================

col1, col2, col3 = st.columns([7,1.5,1.5], gap='medium')

with col1:
    text("Top Product by Revenue")
    bar_chart(
        key=24,
        data=chart1.top_product_by_revenue(),
        x='product_name',
        y='revenue',
        xtitle='Product Name',
        ytitle='Revenue',
        height=400
    )
        
with col2:
    text("Product by Category")
    bar_chart(
        key=25,
        data=chart2.product_by_category(),
        x='category',
        y='product',
        xtitle='Category',
        ytitle='Product',
        height=400
    )

with col3:
    text("Product by Product line")
    bar_chart(
        key=26,
        data=chart2.product_by_line(),
        x='product_line',
        y='product',
        xtitle='Product Line',
        ytitle='Product',
        height=400
    )

    