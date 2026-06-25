import pandas as pd


class KPIs:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df


class SalesKPIs(KPIs):

    def total_orders(self) -> pd.DataFrame:
        df = self.df.groupby('year')['order_number'].nunique().reset_index()
        df['growth'] = df['order_number'].pct_change()*100
        df = df.rename(columns={'order_number': 'orders'})
        return df[['year', 'orders', 'growth']]

    def total_revenue(self) -> pd.DataFrame:
        df = self.df.groupby('year')['revenue'].sum().reset_index()
        df['growth'] = df['revenue'].pct_change()*100
        return df[['year', 'revenue', 'growth']]

    def total_profit(self) -> pd.DataFrame:
        df = self.df.groupby('year')['profit'].sum().reset_index()
        df['growth'] = df['profit'].pct_change()*100
        return df[['year', 'profit', 'growth']]

    def total_quantity(self) -> pd.DataFrame:
        df = self.df.groupby('year')['quantity'].sum().reset_index()
        df['growth'] = df['quantity'].pct_change()*100
        return df[['year', 'quantity', 'growth']]

    def AOV(self) -> pd.DataFrame:
        df = pd.merge(self.total_revenue(), self.total_orders(), how='left', on='year')
        df['AOV'] = df['revenue'] / df['orders']
        df['growth'] = df['AOV'].pct_change()*100
        return df[['year', 'AOV', 'growth']]

    def revenue_by_month(self) -> pd.DataFrame:
        df = self.df.groupby(['month_name', 'month'])['revenue'].sum().reset_index()
        return df.sort_values(by='month',ascending=True)

    def revenue_by_category(self) -> pd.DataFrame:
        df = self.df.groupby('category')['revenue'].sum().reset_index()
        return df.sort_values(by='revenue', ascending=True)

    def revenue_by_country(self) -> pd.DataFrame:
        df = self.df.groupby('country')['revenue'].sum().reset_index()
        return df.sort_values(by='revenue', ascending=True)

    def revenue_by_sub_category(self) -> pd.DataFrame:
        df = self.df.groupby('subcategory')['revenue'].sum().reset_index()
        return df.sort_values(by='revenue', ascending=True)

    def revenue_by_product_line(self) -> pd.DataFrame:
        df = self.df.groupby('product_line')['revenue'].sum().reset_index()
        return df.sort_values(by='revenue', ascending=True)


class CustomerKPIs(KPIs):   

    def customer(self):
        df = self.df.groupby('login_year')['customer_key'].nunique().reset_index()
        df['cum_cust'] = df['customer_key'].cumsum()
        df['growth'] = df['cum_cust'].pct_change()*100
        df = df.rename(columns={'cum_cust': 'customer', 'login_year':'year'})
        return df[['year', 'customer', 'growth']]

    def ARPU(self) -> pd.DataFrame:
        df = self.df.groupby(["year", "customer_key"], as_index=False)["revenue"].sum()
        df = df.groupby("year", as_index=False)["revenue"].mean()
        df = df.rename(columns = {'revenue':'ARPU'})
        df['growth'] = df['ARPU'].pct_change()*100
        return df[['year', 'ARPU', 'growth']]
    
    def repeat_customer(self) -> pd.DataFrame:
        df = self.df.groupby(["year","customer_key"])[["customer_key"]].count()
        df = df[df["customer_key"] > 1].rename(columns={'customer_key':'rep_cust'}).reset_index()
        df =  df.groupby('year')[['rep_cust']].count().reset_index()
        df['growth'] = df['rep_cust'].pct_change()
        return df[['year', 'rep_cust', 'growth']]
    
    def frequency(self) -> pd.DataFrame:
        sales = SalesKPIs(self.df)
        order = sales.total_orders()
        customer = self.customer()  

        df = pd.merge(order, customer, how='inner', on='year')
        df['frequency'] = df['orders']/df['customer']
        df['growth'] = df['frequency'].pct_change()*100
        return df[['year', 'frequency', 'growth']]
    
    def customer_by_age_group(self):
        df = self.df.groupby('age_group')['customer_key'].nunique().reset_index()
        df = df.rename(columns={'customer_key':'customer'})
        df['percentage'] = df['customer']/df['customer'].sum()*100
        return df[['age_group', 'customer', 'percentage']]
    
    def customer_by_gender(self):
        df = self.df.groupby('gender')['customer_key'].nunique().reset_index()
        df = df.rename(columns={'customer_key':'customer'})
        df['percentage'] = df['customer']/df['customer'].sum()*100
        return df[['gender', 'customer', 'percentage']]

    def customer_by_marital_status(self):
        df = self.df.groupby('marital_status')['customer_key'].nunique().reset_index()
        df = df.rename(columns={'customer_key':'customer'})
        df['percentage'] = df['customer']/df['customer'].sum()*100
        return df[['marital_status', 'customer', 'percentage']]
    
    def customer_by_country(self) -> pd.DataFrame:
        df = self.df.groupby('country')['customer_key'].nunique().reset_index()
        df = df.sort_values(by='customer_key', ascending=True)
        return df.rename(columns={'customer_key':'customer'})
    
    def top_customer_by_revenue(self):
        df = self.df.groupby(['customer_key', 'first_name'])[['revenue']].sum().reset_index()
        df = df.sort_values(by='revenue', ascending=False)[0:20]
        return df[['first_name', 'revenue']]
        
class ProductKPIs(KPIs):
    
    def total_product(self):
        df = self.df.groupby('prd_added_year')['product_key'].nunique().reset_index()
        df['product'] = df['product_key'].cumsum()
        df['growth'] = df['product'].pct_change()
        df = df.rename(columns={'prd_added_year':'year'})
        return df[['year', 'product', 'growth']]

    def product_by_category(self):
        df = self.df.groupby('category')['product_key'].nunique().reset_index()
        df = df.rename(columns={'product_key':'product'})
        df = df.sort_values(by='product', ascending=False)
        return df[['category', 'product']]

    def product_by_sub_category(self):
        df = self.df.groupby('subcategory')['product_key'].nunique().reset_index()
        df = df.rename(columns={'product_key':'product'})
        df = df.sort_values(by='product', ascending=False)
        return df[['subcategory', 'product']]

    def product_by_line(self):
        df = self.df.groupby('product_line')['product_key'].nunique().reset_index()
        df = df.rename(columns={'product_key':'product'})
        df = df.sort_values(by='product', ascending=False)
        return df[['product_line', 'product']]
    
    def top_product_by_revenue(self):   
        df = self.df.groupby('product_name')['revenue'].sum().reset_index()
        df = df.sort_values(by='revenue', ascending=False)[0:25]
        return df[['product_name', 'revenue']]
        