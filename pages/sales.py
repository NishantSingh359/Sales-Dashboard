import streamlit as st
from utils.kpis import SalesKPIs
from utils.common import fact_sales, metric, bar_chart, text
from utils.common import year_filter, gender_filter, marital_status_filter, age_group_filter

st.set_page_config(page_title="Sales", layout="wide")

st.title(":material/bar_chart: Sales")
st.space()

df = fact_sales()

with st.sidebar:
    st.title(":material/filter_alt: Filters")

    year = ["All"] + df['year'].unique().tolist()
    filter1 = st.sidebar.selectbox("Year", year, index=0, key='sales_year')

    gender = ["All"] + ['Male', 'Female']
    filter2 = st.sidebar.selectbox("Gender", gender, index=0, key='sales_gender')

    marital_stauts = ["All"] + ['Married', 'Single']
    filter3 = st.sidebar.selectbox("Marital Status", marital_stauts, index=0, key='sales_marital_status')

    age_group = ["All"] + ['Teen', 'Adult', 'Young Adult', 'Senior']
    filter4 = st.sidebar.selectbox("Age Group", age_group, index=0, key='sales_age_group')
  
kpi = SalesKPIs(
    age_group_filter(
        marital_status_filter(
            gender_filter(
                year_filter(
                    df, 'year', filter1
                ), filter2
            ), filter3
        ),filter4,
    )
)

# =======================================
# First ROW
# =======================================

col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

df = year_filter(kpi.total_orders(), 'year', filter1)
value = df["orders"].sum()
delta = df['growth'].mean()
with col1:
    metric(
        kpi_name="Total Orders",
        value=value,
        data=df,
        x="year",
        y="orders",
        key=1,
        tipname1='Year',
        tipname2='Orders',
        tipname3='Growth'
    )

df = year_filter(kpi.total_revenue(), 'year', filter1)
value = df["revenue"].sum()
delta = round(df['growth'].mean(), 2)
with col2:
    metric(
        kpi_name="Total Revenue",
        value=value,
        data=df,
        x="year",
        y="revenue",
        key=2,
        tipname1='Year',
        tipname2='Revenue',
        tipname3='Growth'
    )

df = year_filter(kpi.total_quantity(), 'year', filter1)
value = df["quantity"].sum()
delta = round(df['growth'].mean(), 2)
with col3:
    metric(
        kpi_name="Total Quantity",
        value=value,
        data=df,
        x="year",
        y="quantity",
        key=3,
        tipname1='Year',
        tipname2='Quantity',
        tipname3='Growth'
    )

df = year_filter(kpi.total_profit(), 'year', filter1)
value = df["profit"].sum()
delta = round(df['growth'].mean(), 2)
with col4:
    metric(
        kpi_name="Total Profit",
        value=value,
        data=df,
        x="year",
        y="profit",
        key=4,
        tipname1='Year',
        tipname2='Profit',
        tipname3='Growth'
    )

df = year_filter(kpi.AOV(), 'year', filter1)
value = df["AOV"].mean()
delta = round(df['growth'].mean(), 2)
with col5:
    metric(
        kpi_name="AOV",
        value=value,
        data=df,
        x="year",
        y="AOV",
        key=5,
        tipname1='Year',
        tipname2='AOV',
        tipname3='Growth'
    )

# =======================================
# SECOND ROW
# =======================================

col1, col2, col3 = st.columns([4, 4, 2], gap="medium")

with col1:
    text("Revenue by Month")
    bar_chart(
        key=6,
        data=kpi.revenue_by_month(),
        x="month_name",
        y="revenue",
        xtitle="Month Name",
        ytitle="Revenue",
        height=400
    )

with col2:
    text("Revenue by Country")
    bar_chart(
        key=7,
        data=kpi.revenue_by_country(),
        x="country",
        y="revenue",
        xtitle="Country",
        ytitle="Revenue",
        height=400
    )

with col3:
    text("Revenue by Product Line")
    bar_chart(
        key=8,
        data=kpi.revenue_by_product_line(),
        x="product_line",
        y="revenue",
        xtitle="Product Line",
        ytitle="Revenue",
        height=400
    )

# =======================================
# THIRED ROW
# =======================================

col1, col2 = st.columns([7, 2], gap="medium")

with col1:
    text("Revenue by Sub-Category")
    bar_chart(
        key=9,
        data=kpi.revenue_by_sub_category(),
        x="subcategory",
        y="revenue",
        xtitle="Sub-Category",
        ytitle="Revenue",
    )

with col2:
    text("Revenue by Category")
    bar_chart(
        key=10,
        data=kpi.revenue_by_category(),
        x="category",
        y="revenue",
        xtitle="Category",
        ytitle="Revenue",
    )


