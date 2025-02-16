import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
from PIL import Image

# Impostazioni Layout (DEVE essere il primo comando Streamlit)
st.set_page_config(page_title="Team Composition",
                   page_icon="Logo.png", layout="wide")

# Titolo della pagina
st.title("Most used Pokémon for each generation")

FILE_NAME = "Pokemon teams.xlsx"

# 🔹 Funzione per contare i Pokémon
def count_values(df):
    all_pkm = df.iloc[:, :-1].values.ravel()
    return Counter(all_pkm)

# 🔹 Funzione per trovare i primi N Pokémon più usati
def top_n(dict_pkm, n):
    return sorted(dict_pkm.items(), key=lambda x: x[1], reverse=True)[:n]

# 🔹 Funzione per calcolare la percentuale d'uso
def frequency_pkm(df, count_dict):
    num_teams = df.shape[0]
    return {pkm: round(count / num_teams * 100, 2) for pkm, count in count_dict.items()}

# 🔹 Funzione per caricare le immagini dei Pokémon
def load_pokemon_image(pokemon):
    path = f"images/{pokemon.capitalize()}.png"
    try:
        return Image.open(path)
    except FileNotFoundError:
        return None

# 🔹 Funzione generica per visualizzare Pokémon in una griglia
def display_pokemon_grid(pokemon_data, cols_per_row=5):
    cols = st.columns(cols_per_row)
    for i, (name, img, usage, se) in enumerate(pokemon_data):
        with cols[i % cols_per_row]:  # Distribuisce i Pokémon nelle colonne
            st.write(f"**{name}**")
            if img:
                st.image(img, width=200)
            else:
                st.write("Image not found")
            st.write(f"**%usage: {usage:.2f} ± {se*100:.2f}%**")

# 🔹 Cache per il caricamento del dataset (evita ricaricamenti inutili)
@st.cache_data
def load_data():
    return pd.read_excel(FILE_NAME, engine="openpyxl")

dataset = load_data()

# Introduzione alla dashboard
st.markdown("Welcome to the interactive dashboard where you can get information about the most used Pokémon in Pokémon games.")

# Menù a tendina per selezionare il gioco
selected_game = st.selectbox("Select a game:", dataset["Game"].unique())

# 🔹 Filtrare il dataset in base al gioco selezionato
filtered_data = dataset[dataset["Game"] == selected_game]

# 🔹 Contiamo i Pokémon e calcoliamo le statistiche
count_pkm = count_values(filtered_data)
pkm_abs_freq = frequency_pkm(filtered_data, count_pkm)
top_10_pkm = top_n(pkm_abs_freq, 10)

# 🔹 Pokémon totali usati
used_pkm = len(set(filtered_data.iloc[:, :-1].values.ravel()))
st.write(f"{used_pkm} different Pokémon were used in {len(filtered_data)} teams.")

# 🔹 Mostriamo i top 10 Pokémon
st.subheader(f"Top 10 most used Pokémon in Pokémon {selected_game} version")

pokemon_data = [
    (pkm, load_pokemon_image(pkm), usage, 1.96 * np.sqrt(usage / 100 * (1 - usage / 100) / len(filtered_data)))
    for pkm, usage in top_10_pkm
]
display_pokemon_grid(pokemon_data)

st.write("-------------------------------------------------------------")

# 🔹 Visualizziamo i team più usati per ogni starter
starters = set(filtered_data.iloc[:, 0])
for starter in starters:
    st.subheader(f"Most used team for {starter}")

    df_starter = filtered_data[filtered_data["Starter"] == starter]
    count_pkm_starter = count_values(df_starter)
    pkm_abs_freq_starter = frequency_pkm(df_starter, count_pkm_starter)
    top_starters = top_n(pkm_abs_freq_starter, 6)

    pokemon_data_starter = [
        (pkm, load_pokemon_image(pkm), usage, 1.96 * np.sqrt(usage / 100 * (1 - usage / 100) / len(filtered_data)))
        for pkm, usage in top_starters
    ]
    display_pokemon_grid(pokemon_data_starter, cols_per_row=6)

    st.write("-------------------------------------------------------------")
