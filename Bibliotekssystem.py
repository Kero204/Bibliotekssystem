# =================================================================
# KLASSE: Book
# Denne klasse fungerer som en skabelon for alle bøger i systemet.
# Den indeholder data (attributter) om den enkelte bog.
# =================================================================
class Book:
    def __init__(self, book_id, title, author, copies):
        # Initialisering af bogens egenskaber
        self.book_id = book_id    # Unikt ID til at identificere bogen
        self.title = title        # Bogens titel
        self.author = author      # Forfatterens navn
        self.copies = copies      # Antal eksemplarer på hylden

    # Metoden display_info viser bogens detaljer.
    # Dette er et eksempel på Polymorfisme, da Member-klassen har en metode med samme navn.
    def display_info(self):
        print(f"BOG [ID: {self.book_id}] | Titel: {self.title} | Forfatter: {self.author} | Lager: {self.copies}")


# =================================================================
# KLASSE: Member
# Denne klasse håndterer bibliotekets brugere og deres lån.
# Her ser vi 'Composition', da klassen indeholder en liste over bogtitler.
# =================================================================
class Member:
    def __init__(self, member_id, name):
        # Initialisering af medlemmets data
        self.member_id = member_id  # Unikt medlemsnummer
        self.name = name            # Medlemmets fulde navn
        self.borrowed_books = []    # Liste over titler som medlemmet har lånt lige nu

    # Tilføjer en bogtitel til medlemmets private liste
    def borrow_book(self, book_title):
        self.borrowed_books.append(book_title)

    # Fjerner en bogtitel fra listen, hvis medlemmet har den.
    # Returnerer True/False så Library-klassen ved, om afleveringen lykkedes.
    def return_book(self, book_title):
        if book_title in self.borrowed_books:
            self.borrowed_books.remove(book_title)
            return True
        return False

    # Viser medlemmets info og deres aktuelle lån.
    def display_info(self):
        lån_tekst = ", ".join(self.borrowed_books) if self.borrowed_books else "Ingen aktive lån"
        print(f"MEDLEM [ID: {self.member_id}] | Navn: {self.name} | Lånte bøger: {lån_tekst}")


# =================================================================
# KLASSE: Library
# Dette er 'hjernen' i systemet. Klassen styrer interaktionen mellem 
# bøger og medlemmer og holder styr på de overordnede lister.
# =================================================================
class Library:
    def __init__(self):
        # Listerne her gemmer selve objekterne (Book og Member instanser)
        self.books = []   # Database over alle bøger
        self.members = [] # Database over alle medlemmer

    # --- BOGSTYRING ---
    def add_book(self, book):
        # Fejlhåndtering: Tjekker om en bog med samme ID allerede findes
        if any(b.book_id == book.book_id for b in self.books):
            print(f"!!! FEJL: Bog-ID {book.book_id} er allerede i brug.")
            return
        self.books.append(book)
        print(f"> System: Bogen '{book.title}' er registreret.")

    def remove_book(self, book_id):
        # Bruger 'list comprehension' til at skabe en ny liste uden den valgte bog
        oprindelig_længde = len(self.books)
        self.books = [b for b in self.books if b.book_id != book_id]
        if len(self.books) < oprindelig_længde:
            print(f"> System: Bog med ID {book_id} er slettet.")
        else:
            print(f"!!! FEJL: Kunne ikke finde bog med ID {book_id}.")

    def update_book(self, book_id, title=None, copies=None):
        # Leder efter bogen og opdaterer kun de felter, der er udfyldt (ikke None)
        for b in self.books:
            if b.book_id == book_id:
                if title: b.title = title
                if copies is not None: b.copies = copies
                print(f"> System: Bog {book_id} er blevet opdateret.")
                return
        print("!!! FEJL: Bog blev ikke fundet.")

    # --- MEDLEMSSTYRING ---
    def add_member(self, member):
        self.members.append(member)
        print(f"> System: Medlem '{member.name}' er oprettet.")

    def remove_member(self, member_id):
        self.members = [m for m in self.members if m.member_id != member_id]
        print(f"> System: Medlem {member_id} er slettet fra systemet.")

    # --- UDLÅN OG AFLEVERING (LOGIKKEN) ---
    def issue_book(self, m_id, b_id):
        # Finder det specifikke medlem og bogen i listerne via deres ID
        member = next((m for m in self.members if m.member_id == m_id), None)
        book = next((b for b in self.books if b.book_id == b_id), None)

        # Tjekker om begge eksisterer og om der er bøger nok på lager
        if member and book:
            if book.copies > 0:
                book.copies -= 1             # Trækker 1 fra lageret
                member.borrow_book(book.title) # Tilføjer til medlemmets liste
                print(f"SUCCES: '{book.title}' er udlånt til {member.name}.")
            else:
                print(f"FEJL: '{book.title}' er desværre udsolgt.")
        else:
            print("FEJL: Ugyldigt medlems-ID eller bog-ID.")

    def return_book(self, m_id, b_id):
        member = next((m for m in self.members if m.member_id == m_id), None)
        book = next((b for b in self.books if b.book_id == b_id), None)

        if member and book:
            # Hvis medlemmets return_book returnerer True, lægger vi 1 til lageret
            if member.return_book(book.title):
                book.copies += 1
                print(f"SUCCES: '{book.title}' er afleveret korrekt.")
            else:
                print(f"FEJL: {member.name} står ikke som låner af denne bog.")

    def search_book(self, query):
        # Søger i alle bogtitler (gør alt til små bogstaver for at gøre søgningen nemmere)
        print(f"\n--- SØGERESULTATER FOR: '{query}' ---")
        found = [b for b in self.books if query.lower() in b.title.lower()]
        if not found:
            print("Ingen bøger matchede din søgning.")
        for b in found:
            b.display_info()

    def display_status(self):
        # Viser en komplet oversigt over hele biblioteket
        print("\n" + "="*40)
        print("      BIBLIOTEKETS AKTUELLE STATUS")
        print("="*40)
        print("BØGER PÅ LAGER:")
        for b in self.books: b.display_info()
        print("\nREGISTREREDE MEDLEMMER:")
        for m in self.members: m.display_info()
        print("="*40)


# =================================================================
# MAIN: Brugerflade (CLI Menu)
# Her kører selve løkken, som brugeren interagerer med.
# =================================================================
def main():
    bib = Library()
    
    while True:
        print("\n--- HOVEDMENU ---")
        print("\n 1: Tilføj bog\n 2: Fjern bog\n 3: Opdater bog\n 4: Søg bog\n 5: Opret medlem\n 6: Slet medlem\n 7: Udlån bog\n 8: Aflever bog\n 9: Vis status\n 0: Afslut") 
        valg = input("\nVælg handling: ")
        try:
            if valg == "1":
                id_v = int(input("Indtast bog-ID: "))
                tit = input("Indtast titel: ")
                forf = input("Indtast forfatter: ")
                ant = int(input("Antal eksemplarer: "))
                bib.add_book(Book(id_v, tit, forf, ant))

            elif valg == "2":
                bib.remove_book(int(input("Indtast ID på bog der skal fjernes: ")))

            elif valg == "3":
                id_v = int(input("Indtast ID på bogen der skal opdateres: "))
                tit = input("Ny titel (tryk enter for at springe over): ")
                ant = input("Nyt antal (tryk enter for at springe over): ")
                # Hvis 'ant' ikke er tom, konverter til int, ellers behold None
                ant_val = int(ant) if ant.strip() else None
                bib.update_book(id_v, tit if tit.strip() else None, ant_val)

            elif valg == "4":
                bib.search_book(input("Indtast søgeord (titel): "))

            elif valg == "5":
                id_m = int(input("Indtast medlems-ID: "))
                navn = input("Indtast navn: ")
                bib.add_member(Member(id_m, navn))

            elif valg == "6":
                bib.remove_member(int(input("Indtast medlems-ID der skal slettes: ")))

            elif valg == "7":
                mid = int(input("Medlems-ID: "))
                bid = int(input("Bog-ID: "))
                bib.issue_book(mid, bid)

            elif valg == "8":
                mid = int(input("Medlems-ID: "))
                bid = int(input("Bog-ID: "))
                bib.return_book(mid, bid)

            elif valg == "9":
                bib.display_status()

            elif valg == "0":
                print("Programmet afsluttes. Hav en god dag!")
                break
            
            else:
                print("!!! Ugyldigt valg, prøv igen (0-9).")

        except ValueError:
            # Dette fanger fejl hvis brugeren skriver bogstaver hvor der skal stå tal
            print("!!! FEJL: Du skal indtaste et tal i dette felt.")

if __name__ == "__main__":
    main()