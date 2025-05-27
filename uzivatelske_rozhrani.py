from pojistenec import Pojistenec
from sprava_pojistencu import SpravcePojistencu

class UzivatelskeRozhrani:

    def __init__(self):
        self.spravce = SpravcePojistencu()

    def spustit(self):
        while True:
            print("\nVyberte akci:")
            print("1 - Přidat pojištěného")
            print("2 - Upravit pojištěného")
            print("3 - Smazat pojištěného")
            print("4 - Vypsat pojištěnce")
            print("5 - Vyhledat pojištěného")
            print("6 - Ukončit aplikaci")

            volba = input("Zadejte číslo akce: ").strip()
            match volba:
                case "1":
                    self.pridej_pojistence()
                case "2":
                    self.uprav_pojistence()
                case "3":
                    self.smaz_pojistence()
                case "4":
                    self.vypis_pojistence()
                case "5":
                    self.vyhledej_pojistence()
                case "6":
                    print("Ukončuji program.")
                    return
                case _:
                    print("Neplatná volba.")

    def ziskej_jmeno_a_prijmeni(self):
        while True:
            jmeno = input("Zadejte jméno pojištěnce: ").strip()
            if jmeno:
                break
            print("Jméno nesmí být prázdné.")
        while True:
            prijmeni = input("Zadejte příjmení pojištěnce: ").strip()
            if prijmeni:
                break
            print("Příjmení nesmí být prázdné.")
        return jmeno.lower(), prijmeni.lower()

    def ziskej_vek(self):
        while True:
            vek = input("Zadejte věk: ").strip()
            if vek.isdigit() and int(vek) > 0:
                return vek
            print("Neplatný vstup. Zadejte prosím celé kladné číslo.")

    def ziskej_telefon(self):
        while True:
            telefon = input("Zadejte telefonní číslo: ").strip()
            if telefon.isdigit() and len(telefon) >= 9:
                return telefon
            print("Telefon musí obsahovat alespoň 9 číslic.")

    def zobraz_pojistence(self, vysledky):
        if not vysledky:
            print("Žádní pojištěnci k zobrazení.")
            return
        print("Výpis pojištěnců:")
        for pojistenec_id, jmeno, prijmeni, vek, telefon in vysledky:
            print(f"ID: {pojistenec_id}, Jméno: {jmeno}, Příjmení: {prijmeni}, Věk: {vek}, Telefon: {telefon}")

    def pridej_pojistence(self):
        jmeno, prijmeni = self.ziskej_jmeno_a_prijmeni()
        vek = self.ziskej_vek()
        telefon = self.ziskej_telefon()
        pojistenec = Pojistenec(jmeno, prijmeni, vek, telefon)
        print(self.spravce.vloz(pojistenec))

    def uprav_pojistence(self):
        jmeno, prijmeni = self.ziskej_jmeno_a_prijmeni()
        vysledky = self.spravce.vyhledej(jmeno, prijmeni)

        if vysledky:
            self.zobraz_pojistence(vysledky)
            pojistenec_id = int(input("Zadejte ID pojištěnce, kterého chcete upravit: "))
            sloupec = input("Zadejte název sloupce (jmeno, prijmeni, vek, telefon): ").strip()
            nova_hodnota = input(f"Zadejte novou hodnotu pro '{sloupec}': ").strip()
            print(self.spravce.uprav(pojistenec_id, sloupec, nova_hodnota))
        else:
            print("Pojištěnec nebyl nalezen.")

    def smaz_pojistence(self):
        jmeno, prijmeni = self.ziskej_jmeno_a_prijmeni()
        vysledky = self.spravce.vyhledej(jmeno, prijmeni)

        if vysledky:
            self.zobraz_pojistence(vysledky)
            id_ke_smazani = int(input("Zadejte ID pojištěnce, kterého chcete smazat: "))
            print(self.spravce.smaz(id_ke_smazani))
        else:
            print("Pojištěnec nebyl nalezen.")

    def vypis_pojistence(self):
        vysledky = self.spravce.vypis()
        self.zobraz_pojistence(vysledky)

    def vyhledej_pojistence(self):
        jmeno, prijmeni = self.ziskej_jmeno_a_prijmeni()
        vysledky = self.spravce.vyhledej(jmeno, prijmeni)

        if vysledky:
            self.zobraz_pojistence(vysledky)
        else:
            print("Pojištěnec nenalezen.")



