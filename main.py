import os
from src.downloader import download_google_font
from src.processor import process_font_spacing_complete
from src.exporter import generate_full_csv
import time

# Substitua pela sua chave da API do Google Fonts
GOOGLE_FONTS_API_KEY = "SUA CHAVE"

def main():
    # Lista de fontes
    lista_fontes = [
        "ABeeZee", "Abel", "Acme", "Actor", "Agdasima", "Alata", "Alatsi", "Aldrich",
        "Alef", "Alegreya Sans", "Allerta", "Almarai", "Amaranth", "Amiko", "Andika",
        "Anta", "Antic", "Armata", "Arsenal", "Arya", "Athiti", "Atkinson Hyperlegible",
        "Average Sans", "B612", "Bai Jamjuree", "Barlow", "Basic", "Be Vietnam Pro",
        "Belanosima", "Belleza", "BenchNine", "Biryani", "Blinker", "Bubbler One",
        "Cagliostro", "Cambay", "Candal", "Cantarell", "Cantora One", "Capriola",
        "Carlito", "Carme", "Carrois Gothic", "Chakra Petch", "Chathura",
        "Chau Philomene One", "Convergence", "Days One", "Denk One", "Dhurjati",
        "Dhyana", "Didact Gothic", "Dongle", "Doppio One", "DotGothic16", "Duru Sans",
        "Economica", "Ek Mukta", "Electrolize", "Englebert", "Fahkwang", "Farro",
        "Federo", "Fira Sans", "Fjalla One", "Francois One", "Fresca", "Gafata",
        "Galdeano", "Gayathri", "Geo", "GFS Neohellenic", "Gidugu", "Gothic A1",
        "Gotu", "Gowun Dodum", "Gruppo", "Gudea", "Hammersmith One",
        "Hedvig Letters Sans", "Hind", "Homenaje", "Hubballi", "IBM Plex Sans",
        "Imprima", "Inclusive Sans", "Inder", "Inria Sans", "Istok Web", "Jaldi",
        "Jaro", "Jockey One", "K2D", "Kanit", "Kdam Thmor Pro", "Khand", "Khula",
        "Kodchasan", "KoHo", "Krona One", "Krub", "Kulim Park", "Laila", "Lalezar",
        "Lato", "League Gothic", "Livvic", "Madimi One", "Magra", "Mako", "Marmelad",
        "Marvel", "Meera Inimai", "Merge One", "Metrophobic", "Michroma", "Mina",
        "Miriam Libre", "Mitr", "Mochiy Pop One", "Molengo", "Mooli", "Moulpali",
        "Mouse Memoirs", "Mukta", "Nanum Gothic", "NATS", "News Cycle", "Niramit",
        "Nobile", "Nokora", "NTR", "Numans", "Orienta", "Oxygen", "Palanquin",
        "Pavanam", "Paytone One", "Philosopher", "Play", "Poppins", "Pragati Narrow",
        "Preahvihear", "Prompt", "Proza Libre", "PT Sans", "Puritan", "Quantico",
        "Quattrocento Sans", "Questrial", "Rajdhani", "Ramabhadra", "Rambla",
        "Rationale", "RocknRoll One", "Ropa Sans", "Rubik One", "Ruluko", "Rum Raisin",
        "Russo One", "Sansation", "Sansita", "Sarabun", "Sarala", "Sarpanch", "Scada",
        "Secular One", "Seymour One", "Shanti", "Share", "Share Tech", "Shippori Antique",
        "Sintony", "Snippet", "Spinnaker", "Stick", "Strait", "Stylish", "Sulphur Point",
        "Sunflower", "Tac One", "Tajawal", "Tauri", "Telex", "Tenor Sans", "Text Me One",
        "Thasadith", "Titillium Web", "Tomorrow", "Tuffy", "Varela", "Varela Round",
        "Viga", "Voces", "Voltaire", "Wendy One", "Yantramanav", "Yusei Magic"
    ]
    
    resultados_csv = []
    
    # Prepara as pastas
    for folder in ["data/raw", "data/processed", "data/output"]:
        os.makedirs(folder, exist_ok=True)

    # Início do Loop Único
    for index, font_name in enumerate(lista_fontes):
        print(f"[{index + 1}/{len(lista_fontes)}] Processando: {font_name}...")
        
        # 1. Download (Idempotente)
        raw_path = download_google_font(font_name, GOOGLE_FONTS_API_KEY)
        
        if not raw_path:
            continue
            
        processed_path = f"data/processed/{font_name.replace(' ', '')}-Spaced.ttf"
        
        # 2. Processamento (DEVE ESTAR DENTRO DO FOR)
        metricas = process_font_spacing_complete(raw_path, processed_path)
        
        if metricas:
            linha = {
                "classificacao": "Analise Manual",
                "nome_fonte": font_name,
                "resolucao": 1000, 
                "peso": 400,
                "manual?": "N",
                **metricas 
            }
            resultados_csv.append(linha)
            print(f"    [OK] {font_name} adicionada à lista.")
            time.sleep(0.1) 
    
    # 3. Exportação Final (FORA DO FOR)
    if resultados_csv:
        print(f"\n[!] Finalizado! Salvando {len(resultados_csv)} fontes no CSV...")
        generate_full_csv(resultados_csv, "data/output/metricas_fontes_lote.csv")

if __name__ == "__main__":
    main()
