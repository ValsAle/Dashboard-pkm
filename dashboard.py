import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from collections import Counter
from PIL import Image
import time

FILE_NAME = "Pokemon teams.xlsx"

#funzione che conta il numero di ogni pokemon
def count_values(df):
    all_pkm = df.iloc[:, :-1].values.ravel()

    count_pkm = Counter(all_pkm)
    
    return count_pkm

#funzione che mi ritorna una lista di 10 pokemon più utilizzati e le loro frequenze assolute
def top_10(dict, n):
    sorted_dict = sorted(dict.items(), reverse= True, key=lambda x: x[1])[:n]

    return sorted_dict

#funzione che mi ritorna le percentuali di ogni pokemon
def frequency_pkm(df, dict):
    num_teams = df.shape[0]
    freq = {pkm: round(count/num_teams*100, 2)  for pkm, count in dict.items()}

    return freq

dataset = pd.read_excel(FILE_NAME)

#-------------- Inizio dashboard ------------------#

#Impostazioni Layout
st.set_page_config(page_title="Team composition",
                   page_icon="Logo.png", layout="wide")

#Titolo della pagina
st.title("Most used Pokémon for each generations")

# Introduzione alla dashboard
st.markdown("""
Welcome to the interactive dashboard where you can get information about the most used Pokémon in Pokémon games. 
""")

# Menù a tendina per selezionare il gioco
selected_game = st.selectbox("Select a game:", dataset["Game"].unique())
with st.spinner("Loading data..."):
    time.sleep(1)  # Aspetta 1 secondo per simulare il caricamento

# Filtrare il dataset in base al gioco selezionato

filtered_data = dataset[dataset["Game"] == selected_game]

count_pkm = count_values(filtered_data)
pkm_abs_freq =  frequency_pkm(filtered_data, count_pkm)
top_10_pkm = top_10(pkm_abs_freq, 10)

all_pkm = filtered_data.iloc[:, :-1].values.ravel()
used_pkm = len(set(all_pkm))

st.write(f"{used_pkm} different pokèmon were used in {len(filtered_data)} teams.")
# Sottotitolo 1
st.subheader(f"Top 10 most used Pokémon in Pokèmon {selected_game} version")

# Creiamo una lista con le immagini e le percentuali di utilizzo dei primi 10 Pokémon più usati
pokemon_data = []
for items in top_10_pkm[:10]:  # Prendiamo solo i primi 10 Pokémon
    pokemon = items[0]
    percentage = items[1]
    se = 1.96 * np.sqrt(percentage/100*(1-percentage/100)/len(filtered_data))  # Percentuale di utilizzo
    pokemon_image_path = f"images/{pokemon.capitalize()}.png"
    
    try:
        image = Image.open(pokemon_image_path)
        pokemon_data.append((pokemon, image, percentage, se))  # Salviamo nome, immagine e percentuale
    except FileNotFoundError:
        pokemon_data.append((pokemon, None, percentage, se))  # Se manca l'immagine, mettiamo None


# Prima riga (primi 5 Pokémon)
cols = st.columns(5)  # Creiamo 5 colonne
for i in range(5):
    with cols[i]:  # Inseriamo contenuti nelle colonne
        name, img, usage, se = pokemon_data[i]
        st.write(f"**{name}**")  # Nome del Pokémon
        if img:
            st.image(img, width=200)  # Mostra l'immagine se esiste
        else:
            st.write("Image not found")
        st.write(f"**%usage: {usage:.2f} ± {se*100:.2f}%**")  # Mostra la percentuale sotto l'immagine

# Seconda riga (successivi 5 Pokémon)
cols = st.columns(5)  # Nuova riga con 5 colonne
for i in range(5, 10):
    with cols[i - 5]:  # Inseriamo contenuti nelle colonne
        name, img, usage, se = pokemon_data[i]
        st.write(f"**{name}**")  # Nome del Pokémon
        if img:
            st.image(img, width=200)  # Mostra l'immagine se esiste
        else:
            st.write("Image not found")
        st.write(f"**%usage: {usage:.2f} ± {se*100:.2f}%**")  # Mostra la percentuale sotto l'immagine

st.write("-------------------------------------------------------------")

starters_col = filtered_data.iloc[:, 0]
starters = set(starters_col)
for starter in starters:
    st.subheader(f"Most used team for {starter}")
    df_starter = filtered_data[filtered_data["Starter"] == starter]

    count_pkm_starter = count_values(df_starter)
    pkm_abs_freq_starter =  frequency_pkm(df_starter, count_pkm_starter)
    top_starters = top_10(pkm_abs_freq_starter, 6)

    pokemon_data_starter = []
    for items in top_starters[:6]:  # Prendiamo solo i primi 10 Pokémon
        pokemon = items[0]
        percentage = items[1]
        se = 1.96 * np.sqrt(percentage/100*(1-percentage/100)/len(filtered_data))  # Percentuale di utilizzo
        pokemon_image_path_starter = f"images/{pokemon.capitalize()}.png"
        
        try:
            image = Image.open(pokemon_image_path_starter)
            pokemon_data_starter.append((pokemon, image, percentage, se))  # Salviamo nome, immagine e percentuale
        except FileNotFoundError:
            pokemon_data_starter.append((pokemon, None, percentage, se))  # Se manca l'immagine, mettiamo None


    # Prima riga (primi 6 Pokémon)
    cols = st.columns(6)  # Creiamo 6 colonne
    for i in range(6):
        with cols[i]:  # Inseriamo contenuti nelle colonne
            name, img, usage, se = pokemon_data_starter[i]
            st.write(f"**{name}**")  # Nome del Pokémon
            if img:
                st.image(img, width=200)  # Mostra l'immagine se esiste
            else:
                st.write("Image not found")
            st.write(f"**%usage: {usage:.2f} ± {se*100:.2f}%**")
    
    st.write("-------------------------------------------------------------")