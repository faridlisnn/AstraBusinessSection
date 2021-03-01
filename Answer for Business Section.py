# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 07:41:59 2021

@author: Farid
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('live_coding_dataset_v2.csv')

# Add total_price column
data['total_price'] = data['unit_price']*data['quantity']

# Calculate total transactions each month
data['invoice_date'] = pd.to_datetime(data['invoice_date'])
monthly_transactions = data.resample('M', on='invoice_date').sum()
monthly_transactions['month-year'] = monthly_transactions.index.strftime('%m-%Y')

# Visualize total transactions each month
def bar_graph(df,x,y,xticks=False):
    sns.barplot(data=df,x=x,y=y,palette='Set2')
    if xticks == True:
        plt.xticks(rotation=45)
    plt.show()
    return

bar_graph(monthly_transactions,'month-year','total_price')
bar_graph(monthly_transactions,'month-year','quantity')

# Create total_price and quantity correlation heatmap
def heatmap(df):
    sns.heatmap(df, annot=True)
    plt.show()
    return

heatmap(monthly_transactions[['total_price','quantity']].corr())

# Calculate and visualize total transaction in five highest provinces
province_transactions = data.groupby(by=['province']).sum()
province_transactions = province_transactions.sort_values(by=['total_price'],
                                                          axis=0,ascending=False)

bar_graph(province_transactions.head(5),
          province_transactions.head(5).index,'total_price')

# Calculate and visualize total transaction and quantity for five highest products
product_transactions = data.groupby(by=['stock_code']).sum()
product_transactions_price = product_transactions.sort_values(by=['total_price'],
                                                              axis=0,ascending=False)

bar_graph(product_transactions_price.head(5),
          product_transactions_price.head(5).index,'total_price')

product_transactions_quantity = product_transactions.sort_values(by=['quantity'],
                                                              axis=0,ascending=False)

bar_graph(product_transactions_quantity.head(5),
          product_transactions_quantity.head(5).index,'quantity')

# Find anomalies in each invoice
each_invoice = data.groupby(by=['invoice_no']).sum()
each_invoice.describe()

def boxplot(df,x):
    sns.boxplot(data=df, x=x, palette='Set3')
    plt.show()
    return

boxplot(each_invoice,'total_price')

# Calculate and visualize total transaction for five highest customers
each_customer = data.groupby(by=['customer_id']).sum()
each_customer = each_customer.sort_values(by=['total_price'],
                                          axis=0,ascending=False)

bar_graph(each_customer.head(5),
          each_customer.head(5).index.astype(str),
          'total_price')

