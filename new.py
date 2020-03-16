import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns

def main():
    st.write("Devices managed by serviceASSIST")


    dataset = st.file_uploader("Upload Dataset in .xlsx format",type=["xlsx"])
    if dataset is not None:
        #read data
        df=pd.read_excel(dataset)
         #preparing final DF
        df.rename(columns={"Asset Serviced By: Account Name": "Company"},inplace=True)
        df['Nº_of_managed_devices']=df['Asset Name'].apply(lambda a: a.split()[2])
        col_to_drop=['Asset Name','Account: Account Name','Opt-In','Created Date']
        df.drop(col_to_drop,axis=1,inplace=True)
        data=df.drop_duplicates(subset='Nº_of_managed_devices').copy()

    #Plot
    dfs=[]
    country_list=data['Country'].unique()
    for i in country_list:
        country=data['Country']==i
        agg_df=data[country].groupby('Company').agg('count').sort_values('Nº_of_managed_devices',ascending=False)
        to_plot=agg_df.groupby('Nº_of_managed_devices').agg('count').sort_values('Country',ascending=False)
        to_plot.rename(columns={"Country": i},inplace=True)
        dfs.append(to_plot)
        df_row = pd.concat(dfs,axis=1)

    if st.checkbox("Show bar chart for all countries"):
        st.write(df_row.plot(kind='bar',legend=True))
        sns.set(rc={'figure.figsize':(15,10)})
        plt.title("Boilers managed by serviceASSIST")
        plt.ylabel('Nº_of_companies')
        plt.xticks(rotation=0)
        st.pyplot()

    # plot by country
    st.subheader("Choose country to plot")
    all_countries_names= list(data['Country'].unique())
    select_countries=st.selectbox("Select country",all_countries_names)

    if st.button("Generate Plot"):
        for i in all_countries_names:
            if select_countries==i:
                country=data['Country']==i
                agg_df=data[country].groupby('Company').agg('count').sort_values('Nº_of_managed_devices',ascending=False)
                to_plot=agg_df.groupby('Nº_of_managed_devices').agg('count').sort_values('Country',ascending=False)
                to_plot.rename(columns={"Country": i},inplace=True)
                #dfs.append(to_plot)
                #df_row = pd.concat(dfs,axis=1)
                to_plot.plot(kind='bar',legend=False)
                sns.set(rc={'figure.figsize':(12,8)})
                plt.title("Managed boilers in %s" % i)
                plt.ylabel('Nº_of_companies')
                plt.xticks(rotation=0)
                plt.yticks(np.arange(0, (to_plot[i].iloc[0])+1, step=1))
                st.pyplot()


if __name__ == "__main__":
    main()
