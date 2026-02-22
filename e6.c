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
    }
    return 0;
}