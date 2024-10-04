import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#changing seaborn style
sns.set(style='dark')

#importing data
all_data = pd.read_csv('main_data.csv')

datetime_columns = ['date']
all_data.sort_values(by='date', inplace=True)
all_data.reset_index(inplace=True)
 
for column in datetime_columns:
    all_data[column] = pd.to_datetime(all_data[column])

#preparing dataframe
def create_month_recap(df):
    plot_month = df['month'].astype(str)
    plot_year = df['year'].astype(str)
    df['year_month'] = plot_month + ' ' + plot_year
    df['total_sum'] = df.groupby('year_month')['total'].transform('sum')
    return df[['year_month', 'total_sum']]

def create_season_recap(df):
    season_recap = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_recap

def create_weather_recap(df):
    weather_recap = df.groupby(by='weather').agg({
    'total': 'mean'
    }).reset_index()
    return weather_recap

def create_weekday_hour_recap(df):
    filter_weekday = df[(df['weekday'] == 1)]
    weekday_hour_recap = filter_weekday.groupby(by='hour').agg({
    'total': 'sum'
    }).reset_index()
    return weekday_hour_recap

def create_holiday_hour_recap(df):
    filter_holiday = df[(df['holiday'] == 1)|(df['weekday'] == 0)]
    holiday_hour_recap = filter_holiday.groupby(by='hour').agg({
    'total': 'sum'
    }).reset_index()
    return holiday_hour_recap


def create_daily_recap(df):
    daily_recap = df.groupby(by='date').agg({
        'total': 'sum'
    }).reset_index()
    return daily_recap

def create_registered_recap(df):
    registered_recap = df.groupby(by='date').agg({
        'registered': 'sum'
    }).reset_index()
    return registered_recap

def create_casual_recap(df):
    casual_recap = df.groupby(by='date').agg({
        'casual': 'sum'
    }).reset_index()
    return casual_recap

def create_temperature_recap(df):
    temperature_recap = df.groupby(by='date').agg({
        'temperature': 'mean'
    }).reset_index()
    return temperature_recap

def create_hum_recap(df):
    hum_recap = df.groupby(by='date').agg({
        'hum': 'mean'
    }).reset_index()
    return hum_recap

#time span sidebar
max_date = pd.to_datetime(all_data['date']).dt.date.max()
min_date = pd.to_datetime(all_data['date']).dt.date.min()

with st.sidebar:
    st.image('cykling_logo.png')

    #input start_date dan end_date
    start_date, end_date = st.date_input(
        label='Time Span:',
        max_value=max_date,
        min_value=min_date,
        value=[min_date, max_date]
    )
    if st.checkbox("Display Dataset"):
        st.subheader("Dataset")
        st.write(all_data)
    
    
    st.title ('By:')
    st.write(
        """ 
        **ANNISA ESADORA HARTANTO**\n
        Email: **annisaessadorahartanto@gmail.com**
        Dicoding ID: **annisaesadora**\n
        """
    )

main_df = all_data[(all_data['date'] >= str(start_date)) & 
                (all_data['date'] <= str(end_date))]

month_recap_df = create_month_recap(main_df)
season_recap_df = create_season_recap(main_df)
weather_recap_df = create_weather_recap(main_df)
weekday_hour_recap_df = create_weekday_hour_recap(main_df)
holiday_hour_recap_df = create_holiday_hour_recap(main_df)
daily_recap_df = create_daily_recap(main_df)
casual_recap_df = create_casual_recap(main_df)
registered_recap_df = create_registered_recap(main_df)
temperature_recap_df = create_temperature_recap(main_df)
hum_recap_df = create_hum_recap(main_df)

#UI Making
st.header('CYKLING ANALYTICS DASHBOARD')

#Subheader Rent Summary
st.subheader('CYKLING Rent Summary')
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    daily_recap = daily_recap_df['total'].sum()
    st.metric('Total User', value= daily_recap)

with col2:
    registered_recap = registered_recap_df['registered'].sum()
    st.metric('Registered User', value= registered_recap)

with col3:
    casual_recap = casual_recap_df['casual'].sum()
    st.metric('Casual User', value= casual_recap)

with col4:
    temperature_recap = temperature_recap_df['temperature'].mean()
    st.metric('Mean Temperature', value= temperature_recap)

with col5:
    hum_recap = hum_recap_df['hum'].mean()
    st.metric('Mean Humidity', value= hum_recap)

#Subheader Monthly Recap
# Joining column year and month 'year_month'
month_recap_df['year_month'] = main_df['date'].dt.strftime('%m %Y')  # Format month year

# Calculating total sum per 'year_month'
month_recap_df['total_sum'] = main_df.groupby('year_month')['total'].transform('sum')

# Showing CYKLING Monthly Trend on Streamlit
st.subheader('CYKLING Monthly Trend')

# Making plot using seaborn
sns.set(style='whitegrid')  
fig, ax = plt.subplots(figsize=(20, 6))

sns.lineplot(
    data=month_recap_df,
    x='year_month',
    y='total_sum',
    marker='o',
    linewidth=5,
    ax=ax
)

# Adjusting axis
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15, rotation=45)
ax.set_title("Total Rented Bikes in Past 2 Years", fontsize=20)
ax.set_xlabel(None)
ax.set_ylabel(None)

# Showing Plot in Streamlit
st.pyplot(fig)

# Plot Total Rents based on Customers
st.subheader('Total Rents Based on Customers')

# Making dataframe based on customer
plot_total = pd.DataFrame({
    'user_type': ['casual', 'registered'],
    'total': [main_df['casual'].sum(), main_df['registered'].sum()]
})

# Coloring for each data with highest and lower number
colors = ['tab:grey' if total < plot_total['total'].max() else 'tab:pink' for total in plot_total['total']]

# Barplot making using seaborn
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=plot_total,
    x='user_type',
    y='total',
    palette=colors,
    ax=ax
)

# adding title and adjusting axis
ax.set_title("Total of Rents Based on Customers", fontsize=20)
ax.set_xlabel(None)
ax.set_ylabel(None)

# showing plot on streamlit
st.pyplot(fig)

#Subheader Weekday and Holiday Time Recap
st.subheader('Weekday and Holiday Time Recap')
 
col1, col2 = st.columns(2)
 
with col1:
    weekday_max_col = weekday_hour_recap_df['total'].idxmax()
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y='total', 
        x='hour',
        data=weekday_hour_recap_df,
        color='tab:grey',
        ax=ax
    )
    plt.bar(weekday_max_col, weekday_hour_recap_df.loc[weekday_max_col, 'total'], color='tab:pink', label='Most Rented Hour')
    ax.set_title('Weekday Rent Hour Recap', loc='center', fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    ax.legend(fontsize=20)
    st.pyplot(fig)

with col2:
    holiday_max_col = holiday_hour_recap_df['total'].idxmax()
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y='total', 
        x='hour',
        data=holiday_hour_recap_df,
        color='tab:grey',
        ax=ax
    )
    plt.bar(holiday_max_col, holiday_hour_recap_df.loc[holiday_max_col, 'total'], color='tab:pink', label='Most Rented Hour')
    ax.set_title('Holiday Rent Hour Recap', loc='center', fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    ax.legend(fontsize=20)
    st.pyplot(fig)

#using style seaborn
sns.set(style='whitegrid')

# Data recap
plot_weather = main_df.groupby(by='weather').agg({
    'total': 'mean'
}).reset_index()

# weather color
colors_weather = ['tab:grey' if total < plot_weather['total'].max() else 'tab:pink' for total in plot_weather['total']]

plot_season = main_df.groupby('season')[['registered', 'casual']].sum().reset_index()
plot_season['total'] = plot_season['registered'] + plot_season['casual']
max_index_season = plot_season['total'].idxmax()

#Subheader Weather and Season Recap
st.subheader('Weather and Season Recap')

col1, col2 = st.columns(2)

# weather graphic
with col1:
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.barplot(
        data=plot_weather,
        x='weather',
        y='total',
        palette=colors_weather,
        ax=ax
    )
    
    ax.set_title('Total Rented Bikes based on Weathers Recap', fontsize=20)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    
    st.pyplot(fig)

# season graphic
with col2:
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.barplot(
        data=plot_season,
        x='season',
        y='total',
        color='tab:grey',
        ax=ax
    )
    
    # changing bar color for highest rent number
    ax.bar(plot_season.loc[max_index_season, 'season'], 
           plot_season.loc[max_index_season, 'total'], 
           color='tab:pink', label='Highest Rent')
    
    ax.set_title('Total Rented Bikes based on Seasons Recap', fontsize=20)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.legend(fontsize=12)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    
    st.pyplot(fig)

st.caption('Copyright (c) CYKLING 2024')