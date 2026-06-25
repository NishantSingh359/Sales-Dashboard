import streamlit as st
import pandas as pd
from utils.kpis import CustomerKPIs
from utils.common import fact_sales, customer, metric, bar_chart, pie_chart, text
from utils.common import year_filter, gender_filter, age_group_filter, marital_status_filter
    
st.set_page_config(page_title='Customer', layout='wide')

st.title(":material/diversity_3: Customer")
st.space()

df = fact_sales()
df1 = customer()

with st.sidebar:

    st.title(":material/filter_alt: Filters")

    year = ["All"] + df['year'].unique().tolist()
    filter1 = st.sidebar.selectbox("Year", year, index=0, key='customer_year')

    gender = ["All"] + ['Male', 'Female']
    filter2 = st.sidebar.selectbox("Gender", gender, index=0, key='customer_gender')

    marital_stauts = ["All"] + ['Married', 'Single']
    filter3 = st.sidebar.selectbox("Marital Status", marital_stauts, index=0,  key='customer_marital_status')

    age_group = ["All"] + ['Teen', 'Adult', 'Young Adult', 'Senier']
    filter4 = st.sidebar.selectbox("Age Group", age_group, index=0, key='customer_age_group')
    
kpi1 = CustomerKPIs(
    age_group_filter(
        marital_status_filter(
            gender_filter(df, filter2), filter3
        ),
        filter4,
    )
)

kpi2 = CustomerKPIs(
    age_group_filter(
        marital_status_filter(
            gender_filter(df1, filter2), filter3
        ),
        filter4,
    )
)

chart1 = CustomerKPIs(
    age_group_filter(
        marital_status_filter(
            gender_filter(year_filter(df, 'login_year',filter1), filter2), filter3
        ),
        filter4,
    )
)
    
chart2 = CustomerKPIs(
    age_group_filter(
        marital_status_filter(
            gender_filter(year_filter(df1, 'login_year',filter1), filter2), filter3
        ),
        filter4,
    )
)  

def conversion_rate():
    total_customer = kpi2.customer().rename(columns={'customer':'total'})
    active_customr = kpi1.customer().rename(columns={'customer':'active'})
     
    df = pd.merge(total_customer, active_customr, how='left', on='year')
    df['conversion_rate'] = df['active']/df['total']*100
    df['growth'] = df['conversion_rate'].pct_change() * 100
    return df[['year', 'conversion_rate', 'growth']]

def inactive_customer():
    total_customer = kpi2.customer()
    active_customer = kpi1.customer()
     
    df = pd.merge(total_customer, active_customer, how='left', on='year')
    df['inactive_customer'] = df['customer_x']-df['customer_y']
    df['growth'] = df['inactive_customer'].pct_change()
    return df[['year', 'inactive_customer', 'growth']]


# =======================================
# FIRST ROW
# =======================================

col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

df = year_filter(kpi2.customer(),'year',filter1)
value = df.iloc[df.shape[0]-1,1]

with col1:
    metric(  
        "Total Customer",
        value=value, #type:ignore
        data=df,
        x='year',
        y='customer',
        key=11,
        tipname1="Year",
        tipname2='Customer',
        tipname3='Growth'
    )

df = year_filter(kpi1.customer(), 'year', filter1)
value = df.iloc[df.shape[0]-1,1]

with col2:    
    metric(
        "Active Customer",
        value=value, #type:ignore
        data=df,
        x='year',
        y='customer',
        key=12,
        tipname1="Year",
        tipname2='Customer',
        tipname3='Growth'
    )

df = year_filter(kpi1.ARPU(), 'year', filter1)
value = df["ARPU"].mean()
with col3:
    metric(
        "ARPU",
        value=value,
        data=df,
        x='year',
        y='ARPU',
        key=13,
        tipname1="Year",
        tipname2='ARPU',
        tipname3='Growth'
    )

df = year_filter(kpi1.repeat_customer(),'year', filter1)
value = df["rep_cust"].sum()

with col4:
    metric(
        "Repeat Customer", 
        value=value,
        data=df,
        x='year',
        y='rep_cust',
        key=14,
        tipname1="Year",
        tipname2='Customer',
        tipname3='Growth'
    )

df = year_filter(kpi1.frequency(), 'year', filter1)
value = df['frequency'].mean()

with col5:
    metric(
        "Purchase Frequency",
        value=value,
        data=df,
        x='year',
        y='frequency',
        key=15,
        tipname1="Year",
        tipname2='Customer',
        tipname3='Growth'
    )

# =======================================
# SECOND ROW
# =======================================

col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

df = year_filter(conversion_rate(), 'year', filter1)
active_cust = year_filter(kpi1.customer(), 'year', filter1)['customer'].sum()
total_cust = year_filter(kpi2.customer(), 'year', filter1)['customer'].sum()
value = active_cust/total_cust*100

with col1:
    metric(
        "Conversion Rate",
        value=value,
        data=df,
        x='year',
        y='conversion_rate',
        key=16,
        tipname1="Year",
        tipname2='Conversion Rate',
        tipname3='Growth'
    )      

df = year_filter(inactive_customer(), 'year', filter1)
active_cust = year_filter(kpi1.customer(), 'year', filter1)['customer'].sum()
total_cust = year_filter(kpi2.customer(), 'year', filter1)['customer'].sum()
value = total_cust-active_cust

with col2:
    metric(
        "Inactive Customer",
        value=value,
        data=df,
        x='year',
        y='inactive_customer',
        key=17,
        tipname1="Year",
        tipname2='Customer',
        tipname3='Growth'
    )

with col3:
    text('Customer Age Group')
    pie_chart(
        key=18,
        data=chart2.customer_by_age_group(),
        names='age_group',
        values='customer',
        hole=.55,
        tipname='Customer',
        height=200,
        width=200
    )

with col4:
    text('Customer Marital Status')
    pie_chart(
        key=19,
        data=chart2.customer_by_marital_status(),
        names='marital_status',
        values='customer',
        hole=.55,
        tipname='Customer',
        height=200,
        width=200
    )

with col5:
    text('Customer Gender')
    pie_chart(
        key=20,
        data=chart2.customer_by_gender(),
        names='gender',
        values='customer',
        hole=.55,
        tipname='Customer',
        height=200,
        width=200
    )
    
# =======================================
# THIRED ROW
# =======================================

col1, col2 = st.columns([4,6], gap='medium')

with col1:
    text("Total Customer by Country")
    bar_chart(
        key=21,
        data=chart2.customer_by_country(),
        x='country',
        y='customer',
        xtitle='Country',
        ytitle='Customer',         
    )

with col2:
    text("Top 10 Customer by Revenue")
    bar_chart(
        key=22,
        data=chart1.top_customer_by_revenue(),
        x='first_name',
        y='revenue',
        xtitle='Customer',
        ytitle='Revenue', 
    )

