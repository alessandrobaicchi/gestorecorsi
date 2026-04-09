from dataclasses import dataclass

# E' un DTO

@dataclass
class Corso:
    codins: str
    crediti: int
    nome: str
    pd: int

    def __eq__(self, other):
        # Il metodo eq() compara SOLO LE CHIAVI PRIMARIE
        return self.codins == other.codins
        # Return True se il codins dei due oggetti confrontati è lo stesso

    def __hash__(self):
        # Il metodo hash() è sulla chiave primaria
        return hash(self.codins)

    def __str__(self):
        return f"{self.nome} ({self.codins}) - {self.crediti} CFU"