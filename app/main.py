import math

# KALORIENBEDARF-BERECHNUNG (HARRIS-BENEDICT REVIDIERT 1984)

# 1. GRUNDUMSATZ (BMR)

#    Männer: BMR = 66,5 + (13,75 × Körpergewicht in kg) + (5,003 × Körpergröße in cm) - (6,755 × Alter in Jahren)
#    Frauen: BMR = 655 + (9,563 × Körpergewicht in kg) + (1,850 × Körpergröße in cm) - (4,676 × Alter in Jahren)

# 2. GESAMTUMSATZ (GSU))
#    GSU = BMR × PAL-Faktor (Physical Activity Level)

#    PAL-Faktoren:
#    1,2   = Sitzend (wenig/keine Bewegung) 
#    1,375 = Leicht aktiv (leichter Sport 1-3x/Woche)
#    1,55  = Moderat aktiv (Sport 3-5x/Woche)
#    1,725 = Sehr aktiv (Sport 6-7x/Woche)
#    1,9   = Extrem aktiv (sehr intensive Arbeit/Training)

# 3. KALORIENZIEL
#    Das kaloriendefizit darf nicht mehr als 15% des Gesamtumsatzes betragen, um gesund abzunehmen.
#    Tägliches Defizit/zunahme = (kg pro Woche × 7000) ÷ 7
#    
#    7000 = ca. Kaloriengehalt von 1 kg
#    ÷ 7  = Verteilung auf 7 Tage pro Woche
#    
#    Abnehmen: GSU - Defizit
#    Zunehmen: GSU + Zunahme
#    Halten:   GSU
#    
#    Beispiel: 0,5 kg/Woche = (0,5 × 7000) ÷ 7 = 500 kcal/Tag


gewicht = float(input("Gib dein Gewicht in kg ein: "))
groesse = float(input("Gib dein Grösse in cm ein: "))
alter = int(input("Gib dein Alter in Jahren ein: "))
geschlecht = input("Gib dein Geschlecht ein (m/w): ")


def berechne_bmr(gewicht, groesse, alter, geschlecht):
    if geschlecht == "m":

        bmr = 66.5 + (13.67 * gewicht) + (5.003 * groesse) - (6.755 * alter)
    
    elif geschlecht == "w":
        bmr = 655 + (9.563 * gewicht) + (1.850 * groesse) - (4.676 * alter)

    else:
        print("Ungültige Eingabe für Geschlecht. Bitte 'm' für männlich oder 'w' für weiblich eingeben.")

    return bmr

bmr = berechne_bmr(gewicht, groesse, alter, geschlecht)
print(f"Dein Grundumsatz (BMR) beträgt: {bmr:.2f} kcal/Tag")
print()

pal_faktor_sitzend = 1.2
pal_faktor_leicht_aktiv = 1.375
pal_faktor_moderat_aktiv = 1.55
pal_faktor_sehr_aktiv = 1.725
pal_faktor_extrem_aktiv = 1.9


print("Wähle deinen Aktivitätslevel:")

print("1. Sitzend (wenig/keine Bewegung)")
print("2. Leicht aktiv (leichter Sport 1-3x/Woche)")
print("3. Moderat aktiv (Sport 3-5x/Woche)")
print("4. Sehr aktiv (Sport 6-7x/Woche)")
print("5. Extrem aktiv (sehr intensive Arbeit/Training)")

print()

aktivitaetslevel = int(input("Gib die Zahl für deinen Aktivitätslevel ein: "))

if aktivitaetslevel == 1:
    pal_faktor = pal_faktor_sitzend

elif aktivitaetslevel == 2:
    pal_faktor = pal_faktor_leicht_aktiv

elif aktivitaetslevel == 3:
    pal_faktor = pal_faktor_moderat_aktiv

elif aktivitaetslevel == 4:
    pal_faktor = pal_faktor_sehr_aktiv

elif aktivitaetslevel == 5:
    pal_faktor = pal_faktor_extrem_aktiv

else:
    print("Ungültige Eingabe.")

def berechne_gsu(bmr, pal_faktor):
    gsu = bmr * pal_faktor
    return gsu

print()


gsu = berechne_gsu(bmr, pal_faktor)
print(f"Dein Gesamtumsatz (GSU) beträgt: {gsu:.2f} kcal/Tag")

print()

defizitProTag = gsu * 0.15

taeglicherBedarf = gsu - defizitProTag

verlustDerWoche = (defizitProTag * 7) / 7000

print()

print("Wähle dein Zielgewicht ein:")

print()

gewichtsziel = float(input(" "))

GewichtVerlieren = gewicht - gewichtsziel

dauer = GewichtVerlieren / verlustDerWoche

print(f"""
Zu verlieren:                 {GewichtVerlieren} kg
Empfohlenes Defizit:          {round(defizitProTag)} kcal/Tag (15% deines GSU)
Dein tägliches Kalorienziel:  {round(taeglicherBedarf)} kcal/Tag
Verlust pro Woche:            {round(verlustDerWoche, 2)} kg
Geschätzte Dauer:             {round(dauer)} Wochen
""")
