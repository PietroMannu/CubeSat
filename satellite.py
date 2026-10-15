class Satellite:
    """Gestisce la telemetria e i sensori del CubeSat."""

    def __init__(self, nome: str):
        self.nome = nome
        self.sensori = {}  # Dizionario: codice -> istanza di Sensore
        self.letture = []  # Lista di letture (dizionari)

    def aggiungi_sensore(self, sensore: Sensore):
        """Aggiunge un sensore al dizionario sensori gestito dal satellite."""
        if sensore.codice in self.sensori:
            print(
                f"[AVVISO] Sensore {sensore.codice} già presente. Verrà aggiornato."
            )
        self.sensori[sensore.codice] = sensore

    def registra_lettura(
        self, codice_sensore: str, valore: float, timestamp: str = "N/A"
    ):
        """Registra una nuova lettura verificando l'esistenza del sensore."""
        if codice_sensore not in self.sensori:
            raise SensoreNonTrovatoError(
                f"Errore: Il sensore con codice '{codice_sensore}' non è stato trovato nel satellite."
            )

        lettura = {
            "codice_sensore": codice_sensore,
            "valore": float(valore),
            "timestamp": timestamp,
        }
        self.letture.append(lettura)

    def elenca_letture_oltre_soglia(self) -> list:
        """Analizza le letture e restituisce quelle che superano la soglia massima del sensore."""
        anomalie = []
        for lettura in self.letture:
            sensore = self.sensori.get(lettura["codice_sensore"])
            if sensore and lettura["valore"] > sensore.soglia_massima:
                anomalie.append(
                    {
                        "sensore": sensore,
                        "valore": lettura["valore"],
                        "timestamp": lettura["timestamp"],
                    }
                )
        return anomalie

    def stampa_riepilogo(self):
        """Stampa un riepilogo completo dello stato del satellite e delle letture."""
        print("=" * 65)
        print(f"   RIEPILOGO TELEMETRIA - CUBESAT: {self.nome}")
        print("=" * 65)

        print(f"\n[Sensori Configurati ({len(self.sensori)})]")
        for sensore in self.sensori.values():
            print(f"  • {sensore}")

        print(f"\n[Totale Letture Registrate: {len(self.letture)}]")

        anomalie = self.elenca_letture_oltre_soglia()
        print(f"\n[Letture Oltre Soglia / Allarmi ({len(anomalie)})]")
        if anomalie:
            for item in anomalie:
                s = item["sensore"]
                print(
                    f"  ⚠️  [ALLARME] {s.codice} ({s.grandezza}): "
                    f"{item['valore']} {s.unita_misura} > Limit {s.soglia_massima} {s.unita_misura} "
                    f"[Orario: {item['timestamp']}]"
                )
        else:
            print("  ✅ Tutti i valori rientrano nei parametri di sicurezza.")
        print("=" * 65 + "\n")


# Execution / Script di esempio
if __name__ == "__main__":
    # Creazione del Satellite
    cubesat = Satellite("CubeSat-Alpha1")

    # 1. Definizione e inserimento di almeno 3 sensori
    s_temp = Sensore("TEMP_01", "Temperatura Batteria", "°C", 45.0)
    s_volt = Sensore("VOLT_01", "Tensione Pannelli", "V", 12.5)
    s_pres = Sensore("PRES_01", "Pressione Interna", "hPa", 1013.0)

    cubesat.aggiungi_sensore(s_temp)
    cubesat.aggiungi_sensore(s_volt)
    cubesat.aggiungi_sensore(s_pres)

    # 2. Registrazione letture di esempio
    dati_telemetria = [
        ("TEMP_01", 32.5, "10:00:00"),
        ("VOLT_01", 11.8, "10:00:05"),
        ("PRES_01", 1005.0, "10:00:10"),
        ("TEMP_01", 48.2, "10:05:00"),  # Oltre soglia!
        ("VOLT_01", 13.1, "10:05:05"),  # Oltre soglia!
        ("PRES_01", 1010.0, "10:05:10"),
    ]

    for codice, valore, timestamp in dati_telemetria:
        cubesat.registra_lettura(codice, valore, timestamp)

    # 3. Gestione di un codice sensore inesistente
    print("\n--- TEST GESTIONE CODICE SENSORE INESISTENTE ---")
    try:
        cubesat.registra_lettura("GYRO_99", 0.5, "10:06:00")
    except SensoreNonTrovatoError as err:
        print(f"Gestione Eccezione Riuscita: {err}")

    # 4. Stampa del riepilogo
    print("\n--- TEST STAMPA RIEPILOGO ---")
    cubesat.stampa_riepilogo()