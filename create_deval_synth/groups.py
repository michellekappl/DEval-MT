from declensions import Noun

# not finished
groups = {
    "generic": [
        Noun("m", "Mann", "Mannes", nom_pl="Männer", dat_pl="Männern"),
        Noun("f", "Frau", nom_pl="Frauen"),
        Noun("f", "Person", nom_pl="Personen", neopronouns=True),
    ],
    "Textil/Bekleidung": [
        Noun("m", "Schneider", "Schneiders", dat_pl="Schneidern"),
        Noun("f", "Schneiderin", nom_pl="Schneiderinnen"),
    ],
    "Chemie": [
        Noun("m", "Chemiker", "Chemikers", dat_pl="Chemikern"),
        Noun("f", "Laborhilfe", nom_pl="Laborhilfen"),
    ],
    "Nahrungs-/Genussmittel": [
        Noun("m", "Bäcker", "Bäckers", dat_pl="Bäckern"),
        Noun("f", "Bäckerin", nom_pl="Bäckerinnen"),
    ],
    "Handel": [
        Noun("m", "Kaufmann", "Kaufmanns", nom_pl="Kaufleute", dat_pl="Kaufleuten"),
        Noun("f", "Kauffrau", nom_pl="Kauffrauen"),
    ],
    "Dienstleistung": [
        Noun("m", "Dienstleister", "Dienstleisters", dat_pl="Dienstleistern"),
        Noun("f", "Dienstleisterin", nom_pl="Dienstleisterinnen"),
    ],
    "Werbung": [
        Noun("m", "Marketingmanager", "Marketingmanagers", dat_pl="Marketingmanagern"),
        Noun("f", "Marketingmanagerin", nom_pl="Marketingmanagerinnen"),
    ],
    "Landwirtschaft": [
        Noun("m", "Landwirt", "Landwirts", dat_pl="Landwirten"),
        Noun("f", "Bäuerin", nom_pl="Bäuerinnen"),
    ],
    "Medizin": [
        Noun("m", "Pfleger", "Pflegers", dat_pl="Pflegern"),
        Noun("f", "Ärztin", nom_pl="Ärztinnen"),
    ],
    "Mode": [
        Noun("m", "Designer", "Designers", dat_pl="Designern"),
        Noun("f", "Modedesignerin", nom_pl="Modedesignerinnen"),
    ],
}
