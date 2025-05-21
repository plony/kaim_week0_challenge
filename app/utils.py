# app/utils.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from windrose import WindroseAxes

def load_data():
    """Load and label cleaned datasets"""
    benin = pd.read_csv('../data/benin_clean.csv', parse_dates=['Timestamp'])
    sl = pd.read_csv('../data/sierra_leone_clean.csv', parse_dates=['Timestamp'])
    togo = pd.read_csv('../data/togo_clean.csv', parse_dates=['Timestamp'])

    benin['Country'] = 'Benin'
    sl['Country'] = 'Sierra Leone'
    togo['Country'] = 'Togo'

    return benin, sl, togo


def plot_boxplot(data, selected_countries):
    """Plot interactive boxplot of GHI by selected countries"""
    df_filtered = data[data['Country'].isin(selected_countries)]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df_filtered, x='Country', y='GHI', palette='Set3')
    ax.set_title('Global Horizontal Irradiance (GHI) by Country')
    ax.set_ylabel('GHI (W/m²)')
    return fig


def plot_time_series(data, selected_countries):
    """Plot daily average GHI over time for selected countries"""
    df_filtered = data[data['Country'].isin(selected_countries)].copy()
    df_filtered['Date'] = df_filtered['Timestamp'].dt.date
    daily_avg = df_filtered.groupby(['Date', 'Country'])['GHI'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=daily_avg, x='Date', y='GHI', hue='Country', style='Country', markers=True, dashes=False)
    ax.set_title('Daily Average GHI Over Time')
    ax.set_ylabel('GHI (W/m²)')
    ax.set_xlabel('Date')
    plt.xticks(rotation=45)
    return fig


def plot_wind_rose(data, selected_countries):
    """Plot wind direction and speed using windrose charts"""
    df_filtered = data[data['Country'].isin(selected_countries)].copy()
    
    fig = plt.figure(figsize=(8, 8))
    for i, country in enumerate(selected_countries):
        ax = fig.add_subplot(2, 2, i+1, projection='windrose')
        df_country = df_filtered[df_filtered['Country'] == country]
        ax.bar(df_country['WD'], df_country['WS'], bins=np.arange(0, 10, 2), normed=True, opening=0.8, edgecolor='white')
        ax.set_title(country)
        ax.set_legend(title="Wind Speed (m/s)")

    plt.tight_layout()
    return fig


def plot_bubble_chart(data, selected_countries):
    """Plot GHI vs Tamb with bubble size = RH"""
    df_filtered = data[data['Country'].isin(selected_countries)]

    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(df_filtered['Tamb'], df_filtered['GHI'],
                         c=df_filtered['RH'], s=df_filtered['RH']*10,
                         alpha=0.6, cmap='viridis', edgecolor='w', linewidth=0.5)
    plt.colorbar(scatter, label='Relative Humidity (%)')
    ax.set_title('GHI vs Ambient Temperature\n(Bubble Size = Relative Humidity)')
    ax.set_xlabel('Ambient Temp (°C)')
    ax.set_ylabel('GHI (W/m²)')
    ax.grid(True)
    return fig


def get_summary_table(data, selected_countries):
    """Generate summary stats for selected countries"""
    df_filtered = data[data['Country'].isin(selected_countries)]
    summary = df_filtered.groupby('Country')[['GHI', 'DNI', 'DHI', 'Tamb', 'RH']].agg(['mean', 'median', 'std'])
    return summary.round(2)