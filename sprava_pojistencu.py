import sqlite3

class Pojistenec:
    def __init__(self, jmeno, prijmeni, vek, telefon):
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.vek = vek
        self.telefon = telefon

    def __str__(self):
        return f"{self.jmeno} {self.prijmeni}, Věk:{self.vek}, Telefon {self.telefon}"

    @staticmethod
    def pripoj_se_k_databazi():
        pripojeni = sqlite3.connect('databazepojistenych.db')
        komunikace_s_databazi = pripojeni.cursor()
        return pripojeni, komunikace_s_databazi

    @staticmethod
    def zavri_databazi(pripojeni, komunikace_s_databazi):
        if komunikace_s_databazi:
            komunikace_s_databazi.close()
        if pripojeni:
            pripojeni.close()

    def vloz(self):
        try:
            #otevření a připojení k databázi
            pripojeni, komunikace_s_databazi = Pojistenec.pripoj_se_k_databazi()

            #vykonání SQL INSERT
            komunikace_s_databazi.execute('INSERT INTO pojistenci (jmeno, prijmeni, vek, telefon) VALUES (?, ?, ?, ?)',
                          (self.jmeno, self.prijmeni, self.vek, self.telefon))
            #ulozeni zmen
            pripojeni.commit()

            #uzavření komunikace a připojení
            Pojistenec.zavri_databazi(pripojeni, komunikace_s_databazi)
            return f"Pojištěnec {self.jmeno.capitalize()} {self.prijmeni.capitalize()},{self.vek}, {self.telefon} úspěšně přidán do databáze"
        except Exception as e:
            return f"Nepodařilo se přidat pojištěného: {e}"

    @staticmethod
    def uprav(pojistenec_id, sloupec, nova_hodnota):
        povolene_sloupce = {"jmeno", "prijmeni", "vek", "telefon"}

        if sloupec not in povolene_sloupce:
            return f"Chyba: Sloupec '{sloupec}' není platný. Můžeš upravit pouze: {', '.join(povolene_sloupce)}."

        pripojeni = None
        komunikace_s_databazi = None
        try:
            # Připojení a komunikace s databází
            pripojeni, komunikace_s_databazi = Pojistenec.pripoj_se_k_databazi()

            # Dotaz pro aktualizaci
            uprav_tabulku = f'UPDATE pojistenci SET {sloupec} = ? WHERE pojistenec_id = ?'
            komunikace_s_databazi.execute(uprav_tabulku, (nova_hodnota, pojistenec_id))

            # Uložení změn
            pripojeni.commit()

            return f"Úspěšně bylo upraveno '{sloupec}' na '{nova_hodnota}' pro pojištěnce s ID {pojistenec_id}."
        except Exception as e:
            return f"Nepodařilo se upravit pojištěného: {e}"
        finally:
            Pojistenec.zavri_databazi(pripojeni, komunikace_s_databazi)

    @staticmethod
    def vyhledej(jmeno=None, prijmeni=None):
        pripojeni = None
        komunikace_s_databazi = None
        try:
            # Připojení k databázi
            pripojeni, komunikace_s_databazi = Pojistenec.pripoj_se_k_databazi()

            # Příprava SQL dotazu
            vyhledani_pojistence = 'SELECT pojistenec_id, jmeno, prijmeni, vek, telefon FROM pojistenci WHERE 1=1'
            parameters = []

            if jmeno:
                vyhledani_pojistence += ' AND jmeno LIKE ?'
                parameters.append('%' + jmeno + '%')
            if prijmeni:
                vyhledani_pojistence += ' AND prijmeni LIKE ?'
                parameters.append('%' + prijmeni + '%')

            komunikace_s_databazi.execute(vyhledani_pojistence, parameters)
            return komunikace_s_databazi.fetchall()
        except Exception as e:
            return f"Nepodařilo se vyhledat pojištěného: {e}"
        finally:
            Pojistenec.zavri_databazi(pripojeni, komunikace_s_databazi)

    @staticmethod
    def smaz(pojistenec_id):
        pripojeni = None
        komunikace_s_databazi = None
        try:
            pripojeni, komunikace_s_databazi = Pojistenec.pripoj_se_k_databazi()
            smazani_radku = 'DELETE FROM pojistenci WHERE pojistenec_id = ?'
            komunikace_s_databazi.execute(smazani_radku, (pojistenec_id,))
            pripojeni.commit()
            # Vrátíme zprávu s ID, které bylo smazáno

            return f"Pojištěnec byl úspěšně smazán. ID: {pojistenec_id}"

        except Exception as e:
                return f"Nepodařilo se smazat pojištěného: {e}"

        finally:
            Pojistenec.zavri_databazi(pripojeni, komunikace_s_databazi)

    @staticmethod
    def vypis():
        pripojeni = None
        komunikace_s_databazi = None

        try:
            pripojeni, komunikace_s_databazi = Pojistenec.pripoj_se_k_databazi()
            komunikace_s_databazi.execute('SELECT * FROM pojistenci')
            vysledky = komunikace_s_databazi.fetchall()  # Získání všech výsledků

            # Formátování výsledků do řetězce
            if vysledky:
                vypis = "\n".join(
                    [f"ID: {row[0]}, Jméno: {row[1]}, Příjmení: {row[2]}, Věk: {row[3]}, Telefon: {row[4]}" for row
                        in vysledky])
                return f"Výpis pojištěnců:\n{vypis}"
            else:
                return "Nebyl nalezen žádný pojištěnec."

        except Exception as e:
            return f"Nepodařilo se načíst pojištěnce: {e}"

        finally:
            Pojistenec.zavri_databazi(pripojeni, komunikace_s_databazi)

