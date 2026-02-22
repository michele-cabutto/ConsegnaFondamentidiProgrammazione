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
          
        try:
            s = p[-1] # nome del sensore è in fondo alla riga
            v = float(p[-5]) # valore numerico della misurazione
            
            # Trasformiamo la data testuale in un formato "Tempo"
            t = datetime.strptime(p[-6][:19], "%Y-%m-%dT%H:%M:%S")
            
            # Se è un sensore nuovo, preparo le sue liste per tempo e valori
            if s not in dati: 
                dati[s] = [[], []]

            # Inserisco i dati appena letti nelle liste del sensore
            dati[s][0].append(t)
            dati[s][1].append(v)
            
        except Exception:
            # Se la lettura fallisce, aumento il contatore degli errori e proseguo
            scartate += 1
            continue

print(f"Lettura completata. Righe scartate o non valide: {scartate}")

