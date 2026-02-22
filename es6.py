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

# Creo l'area di disegno con 3 grafici impilati (condividono l'asse del tempo in basso)
fig, ax = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

# titolo
fig.suptitle("Analisi Temporale Rilevazioni Sensori", fontsize=16, fontweight='bold')

# giroscopi
for k in dati:
    if "gyro" in k: 
        ax[0].plot(dati[k][0], dati[k][1], label=k, linewidth=1)
if ax[0].get_lines():
    ax[0].legend()
ax[0].set_title("Andamento Sensori Giroscopio")

# sensori interni
for k in dati:
    if "internal" in k: 
        ax[1].plot(dati[k][0], dati[k][1], label=k, linewidth=1)
if ax[1].get_lines():
    ax[1].legend()
ax[1].set_title("Andamento Sensori Interni")

# qualità aria 
for k in dati:
    if "probe" in k or "airq" in k: 
        ax[2].plot(dati[k][0], dati[k][1], label=k, linewidth=1)
if ax[2].get_lines():
    ax[2].legend()
ax[2].set_title("Andamento Sonde e Qualità Aria")

# miglioramenti
for a in ax:
    a.grid(True, alpha=0.3) # Griglia di sfondo per leggere meglio i picchi
    a.margins(y=0.15) # Spazio extra sopra e sotto le linee

# Etichetta in basso per far capire che l'asse orizzontale è il tempo
plt.xlabel("Tempo (Data e Ora)")

plt.tight_layout() # Evita che le scritte dei vari grafici si sovrappongano
plt.show() # mostro la finestra sullo schermo