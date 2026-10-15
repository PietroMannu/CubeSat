class Sensore:
    """Rappresenta un singolo sensore a bordo del CubeSat."""

    def __init__(
        self,
        codice: str,
        grandezza: str,
        unita_misura: str,
        soglia_massima: float,
    ):
        self.codice = codice
        self.grandezza = grandezza
        self.unita_misura = unita_misura
        self.soglia_massima = float(soglia_massima)

    def __str__(self) -> str:
        return f"Sensore[{self.codice}]: {self.grandezza} ({self.unita_misura}) - Soglia Max: {self.soglia_massima}"


class SensoreNonTrovatoError(Exception):
    """Eccezione personalizzata per codice sensore non registrato."""

    pass