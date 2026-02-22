#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Creo una struttura per memorizzare i dati di ogni sensore
typedef struct {
    char nome[50];
    double somma;
    int conteggio;
    double massimo;
} Sensore;

int main() {
    FILE *file = fopen("log_monitoraggio_25-07-2022.csv", "r");
    if (!file) {
        printf("Errore: impossibile aprire il file.\n");
        return 1;
    }

    char linea[1024];
    Sensore sensori[100]; // Preparo un elenco che può contenere fino a 100 sensori diversi
    int numero_sensori = 0; // Tengo traccia di quanti sensori diversi ho trovato

    // Leggo il file riga per riga
    while (fgets(linea, sizeof(linea), file)) {
        // Ignoro i commenti e le righe vuote
        if (linea[0] == '#' || linea[0] == '\n' || linea[0] == '\r') {
            continue;
        }

        char *token;
        char *ptr = linea;
        int colonna = 0;
        char *valore_str = NULL;
        char *nome_sensore = NULL;

        // Faccio a pezzi la riga usando la virgola come separatore
        while ((token = strtok_r(ptr, ",", &ptr))) {
            if (colonna == 6) { 
                // Il valore numerico sta nella colonna 6
                valore_str = token;
            }
            // L'ultimo pezzo della riga sarà sempre il nome del sensore
            nome_sensore = token; 
            colonna++;
        }

        // Se ho trovato un valore e un nome sensore procedo
        if (valore_str && nome_sensore) {
            // Toglo il carattere di "a capo" dal nome del sensore per pulirlo
            nome_sensore[strcspn(nome_sensore, "\r\n")] = 0;
            
            char *endptr;
            double valore = strtod(valore_str, &endptr);
            
            // Verifico che il valore fosse davvero un numero valido
            if (valore_str != endptr) {
                int trovato = 0;
                
                // Controllo se questo sensore è già nell'elenco
                for (int i = 0; i < numero_sensori; i++) {
                    if (strcmp(sensori[i].nome, nome_sensore) == 0) {
                        // aggiorno i totali
                        sensori[i].somma += valore;
                        sensori[i].conteggio++;
                        // Se il valore attuale è più grande del massimo precedente lo aggiorno
                        if (valore > sensori[i].massimo) {
                            sensori[i].massimo = valore;
                        }
                        trovato = 1;
                        break;
                    }
                }
                
                // Se il sensore non era nell'elenco lo aggiungo
                if (!trovato && numero_sensori < 100) {
                    strcpy(sensori[numero_sensori].nome, nome_sensore);
                    sensori[numero_sensori].somma = valore;
                    sensori[numero_sensori].conteggio = 1;
                    sensori[numero_sensori].massimo = valore;
                    numero_sensori++;
                }
            }
        }
    }

    fclose(file);

    // Mostro i risultati finali sul terminale
    if (numero_sensori > 0) {
        printf("\n=== STATISTICHE AGGREGATE PER SENSORE ===\n");
        for (int i = 0; i < numero_sensori; i++) {
            double media = sensori[i].somma / sensori[i].conteggio;
            printf("Sensore: %s\n", sensori[i].nome);
            printf("  - Rilevazioni valide: %d\n", sensori[i].conteggio);
            printf("  - Media dei valori:   %.2f\n", media);
            printf("  - Valore Massimo:     %.2f\n", sensori[i].massimo);
            printf("-----------------------------------------\n");
        }
    } else {
        printf("Nessun dato valido trovato nel file.\n");
    }

    return 0;
}