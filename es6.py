import matplotlib.pyplot as plt
from datetime import datetime

# Dizionario per raggruppare i dati separatamente per ogni sensore
dati = {}
scartate = 0 # Contatore per le righe che hanno problemi

# Lettura del file in modo sicuro
with open("log_monitoraggio_25-07-2022.csv", "r") as file:
    for riga in file:
        # Ignoro i commenti o le righe di intestazione del CSV
        if riga.startswith("#") or "_value" in riga:
            continue
        
        # Spezzetto la riga usando la virgola e pulisco gli spazi extra
        p = [x.strip() for x in riga.split(",")]
            
        # Se la riga ha troppi pochi dati, la salto
        if len(p) < 11: 
            continue
