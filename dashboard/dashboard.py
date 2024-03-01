import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

dict_period = {"Hourly":"H","Daily":"D","Monthly":"M","Annually":"Y"}
dict_thresh = {"PM2.5":{"Daily":25,"Annually":10},"PM10":{"Daily":50,"Annually":20}}
 
st.title('Visualisasi Air Quality Beijing')

st.write('Dashboard ini merupakan visualisasi interaktif dari hasil analisis data yang sudah dilakukan. \
         Dashboard ini berisikan visualisasi rata-rata harian, bulanan, dan tahunan untuk konsentrasi \
         PM2.5 dan PM10. Sama halnya dengan yang ada di notebook, plot dilengkapi dengan garis batas \
         aman untuk periodisitas harian dan tahunan. Akan tetapi terdapat perbedaan dengan visualisasi \
         yang ada pada notebook, visualisasi disini dapat hanya memilih stasiun tertentu untuk di-plot-kan. \
         Untuk memilih parameter dapat dilakukan pada sidebar yang ada di dashboard ini. Selamat berinteraksi \
         dengan dashboard ini.')

df_pm25 = pd.read_csv("dashboard/Preprocessed Data/pm25.csv",index_col="date")
df_pm10 = pd.read_csv("dashboard/Preprocessed Data/pm10.csv",index_col="date")

df_pm25.index = pd.to_datetime(df_pm25.index)
df_pm10.index = pd.to_datetime(df_pm10.index)

min_date = df_pm25.index.min()
max_date = df_pm25.index.max()
 
with st.sidebar:
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu:',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
        )
    
    particle = st.selectbox(
        label="Ukuran Partikel:",
        options=('PM2.5', 'PM10')
        )

    periodicity = st.selectbox(
        label="Periodisitas:",
        options=('Daily', 'Monthly', 'Annually')
        )
    
    stations = st.multiselect(
        label="Stasiun Cuaca:",
        options=df_pm25.columns
        )

if particle == "PM2.5":
    df_plot = df_pm25[start_date:end_date]
else:
    df_plot = df_pm10[start_date:end_date]

df_plot = df_plot.groupby(pd.Grouper(freq=dict_period.get(periodicity))).mean()
 
fig1, ax1 = plt.subplots(figsize=(12, 5))
for station in stations:
    ax1.plot(df_plot.index.to_pydatetime(), df_plot[station],label=station)
if not periodicity=="Monthly":
    ax1.axhline(y = dict_thresh[particle][periodicity], linestyle = '-', label="Ambang Batas Aman",color="black")
ax1.legend()
ax1.set_title(f"Plot {particle} untuk tiap-tiap stasiun")
ax1.set_xlabel('Tanggal',size=15)
ax1.set_ylabel('Konsentrasi (µg/m³)',size=15)
st.pyplot(fig1)
