from declensions import Noun

# not finished
groups = {
    "generic": [
        Noun("m", "Mann", "Mannes", nom_pl="Männer", dat_pl="Männern"),
        Noun("f", "Frau", nom_pl="Frauen", neopronouns=False),
    ],
    "Chemie": [
        Noun("m", "Chemiker", "Chemikers", dat_pl="Chemikern"),
        Noun("f", "Laborhilfe", nom_pl="Laborhilfen", neopronouns=True),
    ],
    "Landwirtschaft": [
        Noun("m", "Landwirt", "Landwirts", dat_pl="Landwirten"),
        Noun("f", "Bäuerin", nom_pl="Bäuerinnen", neopronouns=True),
    ],
    "Medizin": [
        Noun("m", "Pfleger", "Pflegers", dat_pl="Pflegern"),
        Noun("f", "Ärztin", nom_pl="Ärztinnen", neopronouns=True),
    ],
    "Mode": [
        Noun("m", "Designer", "Designers", dat_pl="Designern"),
        Noun("f", "Modedesignerin", nom_pl="Modedesignerinnen"),
    ],
}
