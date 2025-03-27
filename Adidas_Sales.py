import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import datetime
from PIL import Image

df = pd.read_excel('Adidas.xlsx')

st.set_page_config(layout='wide', page_title='Adidas Sales Dashboard', page_icon=':bar_chart:')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

logo = Image.open('adidas-logo.jpg')

# Header Section
col1, col2 = st.columns([0.1, 0.9])

with col1:
    st.image(logo, width=100)

with col2:
    st.markdown("""
        <style>
        .title {
            font-weight: bold;
            font-size: 2.5rem;
            text-align: center;
            padding: 10px 0;
        }
        </style>
        <div class='title'>Adidas Interactive Sales Dashboard</div>
    """, unsafe_allow_html=True)

# Last Updated Section
st.write(f":calendar: **Last updated on:** {datetime.datetime.now().strftime('%d %B, %Y')}")

# Total Sales by Retailers
new_df = df.groupby('Retailer')['TotalSales'].sum().sort_values(ascending=False)

col3, col4 = st.columns(2)

with col3:
    fig1 = go.Figure(data=[go.Bar(x=new_df.index, y=new_df.values, marker=dict(color='royalblue'))])
    fig1.update_layout(title='Total Sales by Retailers', xaxis_title='Retailer', yaxis_title='Total Sales')
    st.plotly_chart(fig1, use_container_width=True)

    st.expander('🔍 **View Retailer Wise Sales**').write(new_df)
    st.download_button('📥 Download Data', data=new_df.to_csv().encode('utf-8'), file_name='Total_Sales_by_Retailers.csv', mime='text/csv')

# Total Sales by Date
df['Month_year'] = df['InvoiceDate'].dt.strftime("%b '%y")
sales_by_date = df.groupby('Month_year')['TotalSales'].sum()

with col4:
    fig2 = go.Figure(data=[go.Scatter(x=sales_by_date.index, y=sales_by_date.values, mode='lines+markers', marker=dict(color='seagreen'))])
    fig2.update_layout(title='Total Sales Over Time', xaxis_title='Month-Year', yaxis_title='Total Sales')
    st.plotly_chart(fig2, use_container_width=True)

    st.expander('🔍 **View Date Wise Sales**').write(sales_by_date)
    st.download_button('📥 Download Data', data=sales_by_date.to_csv().encode('utf-8'), file_name='Total_Sales_by_Date.csv', mime='text/csv')

st.divider()

# State Wise Sales and Units Sold
state_sales = df.groupby('State')[['TotalSales', 'UnitsSold']].sum().reset_index()

st.subheader('📊 **Total Sales and Units Sold by State**')

fig3 = go.Figure()
fig3.add_trace(go.Bar(x=state_sales['State'], y=state_sales['TotalSales'], name='Total Sales', marker=dict(color='indianred')))
fig3.add_trace(go.Scatter(x=state_sales['State'], y=state_sales['UnitsSold'], name='Units Sold', yaxis='y2', marker=dict(color='dodgerblue')))

fig3.update_layout(
    xaxis=dict(title='State'),
    yaxis=dict(title='Total Sales'),
    yaxis2=dict(title='Units Sold', overlaying='y', side='right'),
    legend=dict(x=1, y=1.1),
)

st.plotly_chart(fig3, use_container_width=True)

st.expander('🔍 **View State Wise Sales**').write(state_sales)
st.download_button('📥 Download Data', data=state_sales.to_csv().encode('utf-8'), file_name='State_Wise_Sales.csv', mime='text/csv')

st.divider()

# Treemap - Sales by Region and City
treemap = df.groupby(['Region', 'City'])['TotalSales'].sum().reset_index()

def format_sales(value):
    return f"{value / 1_00_000:.2f} Lakh" if value > 0 else "0"

treemap['TotalSales (Formatted)'] = treemap['TotalSales'].apply(format_sales)

st.subheader(':earth_africa: **Total Sales by Region and City (Treemap)**')

fig4 = px.treemap(
    treemap,
    path=['Region', 'City'],
    values='TotalSales',
    hover_name='TotalSales (Formatted)',
    color='City',
    height=700
)
fig4.update_traces(textinfo='label+value')

st.plotly_chart(fig4, use_container_width=True)

st.expander('🔍 **View Region and City Wise Sales**').write(treemap)
st.download_button('📥 Download Data', data=treemap.to_csv().encode('utf-8'), file_name='Region_City_Wise_Sales.csv', mime='text/csv')

st.divider()

# Raw Data Section
st.subheader('📄 **Sales Raw Data**')
st.expander('🔍 **View Raw Data**').write(df)
st.download_button('📥 Download Data', data=df.to_csv().encode('utf-8'), file_name='Adidas_Sales_Data.csv', mime='text/csv')
