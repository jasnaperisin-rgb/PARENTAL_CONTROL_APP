#  PARENTAL CONTROL App


## Opis projekta

Ova aplikacija omogućuje roditelju da kontrolira vrijeme korištenja računala za dijete.

Ako dijete koristi računalo izvan dozvoljenog vremena : aplikacija automatski zaključava ekran u fullscreen modu.



##  Namjena

- roditelji
- učenici ( ograničenje korištenja računala)
- edukacijski projekt


## Pokretanje

### ADMIN (roditelj)

main.exe admin

PIN 1234

#Client (automatski)
main.exe


## Funkcionalnosti

-  unos rasporeda korištenja računala
- prikaz rasporeda
- brisanje rasporeda
- fullscreen zaključavanje računala
- PIN zaštita za admin pristup
- automatsko pokretanje uz Windows
- pozadinski nadzor vremena



## Instalacija


# 1. Instaliraj PyInstaller:

pip install pyinstaller

# 2. Napravi .exe:

pyinstaller --noconsole --onefile main.py




# 3. Pokreni aplikaciju

i kopiraj `.exe` na drugo računalo



#  Autostart

1. Pritisni:

Win + R

2. Upiši:

shell:startup

3. Ubaci `.exe` ili shortcut



##  Konfiguracija

Aplikacija koristi `config.json` datoteku za spremanje rasporeda.

Primjer:
```json
{
  "allowed_times": []
}

## Screenshot

-Admin GUI
- Lock screen





## Ograničenja 

- aplikacija nije potpuno otporna na napredne korisnike
- koristi sistemski sat
- nema zaštitu od Task Manager-a


## Plan razvoja (TODO)

- promjena PIN-a
- bolji GUI (modern design)
- cloud sync
- višekorisnička podrška
- watchdog proces



 ## Licenca

  MIT



## Autor

JASNA  PERIŠIN





