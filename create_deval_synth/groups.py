from declensions import Noun

# not finished
groups = {
    # "generic": [
    #     Noun("m", "Mann", "Mannes", nom_pl="Männer", dat_pl="Männern"),
    #     Noun("f", "Frau", nom_pl="Frauen"),
    #     Noun("n", "Person", nom_pl="Personen", pronouns="dey"),
    # ],
    "romantic": [
        [
            Noun(
                "m",
                "Partner",
                "Partners",
                nom_pl="Partner",
                dat_pl="Partnern",
            ),
            Noun("f", "Partnerin", nom_pl="Partnerinnen"),
        ],
        [
            Noun(
                "m",
                "Freund",
                "Freundes",
                nom_pl="Freunde",
                dat_pl="Freunden",
            ),
            Noun("f", "Freundin", nom_pl="Freundinnen"),
        ],
        [
            Noun(
                "m",
                "Ehemann",
                "Ehemannes",
                nom_pl="Ehemänner",
                dat_pl="Ehemännern",
            ),
            Noun("f", "Ehefrau", nom_pl="Ehefrauen"),
        ],
        [
            Noun(
                "m",
                "Liebhaber",
                "Liebhabers",
                nom_pl="Liebhaber",
                dat_pl="Liebhabern",
            ),
            Noun("f", "Liebhaberin", nom_pl="Liebhaberinnen"),
        ],
        [
            Noun("n", "Date", "Dates", nom_pl="Dates", dat_pl="Dates"),
        ],
    ],
    # "other": [
    #     Noun("m", "Juror"),
    #     Noun("f", "Jurorin"),
    #     Noun("n", "Jurymitglied", neopronouns=True),
    #     Noun("n", "Multitalent", neopronouns=True),
    #     Noun("m", "Gesprächspartner"),
    #     Noun("f", "Gesprächspartnerin"),
    #     Noun("n", "Gesprächsperson"),
    #     Noun("m", "Bruder"),
    #     Noun("f", "Schwester"),
    #     Noun("n", "Geschwisterkind", neopronouns=True),
    #     Noun("m", "Enkel"),
    #     Noun("f", "Enkelin"),
    #     Noun("n", "Enkelkind", neopronouns=True),
    #     Noun("m", "Doppelgänger"),
    #     Noun("f", "Doppelgängerin"),
    #     Noun("n", "Double", neopronouns=True),
    #     Noun("m", "Schüler"),
    #     Noun("f", "Schülerin"),
    #     Noun("n", "Schulkind", neopronouns=True),
    #     Noun("m", "Held"),
    #     Noun("f", "Heldin"),
    #     Noun("n", "Vorbild", neopronouns=True),
    #     Noun("n", "Ombudsperson", neopronouns=True),
    #     Noun("m", "Praktikant", status="Helfer"),
    #     Noun("f", "Praktikantin", status="Helfer"),
    #     Noun(
    #         "f", "Praktikumskraft", status="Helfer", neopronouns=True
    #     ),  # im Österreichischen anscheinend gebräuchlich
    # ],
    111: [
        [
            Noun(
                "m",
                "Bauer",
                "Bauern",
                "Bauern",
                "Bauern",
                nom_pl="Bauern",
                status="Fachkraefte",
            ),
            Noun("f", "Bäuerin", nom_pl="Bäuerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Erntehelfer",
                "Erntehelfers",
                nom_pl="Erntehelfer",
                dat_pl="Erntehelfern",
                status="Helfer",
            ),
            Noun("f", "Erntehelferin", nom_pl="Erntehelferinnen", status="Helfer"),
            Noun("f", "Erntehilfe", nom_pl="Erntehilfen", status="Helfer", pronouns="dey"),
        ],
    ],
    112: [
        [
            Noun(
                "m",
                "Imker",
                "Imkers",
                nom_pl="Imker",
                dat_pl="Imkern",
                status="Fachkraefte",
            ),
            Noun("f", "Imkerin", nom_pl="Imkerinnen", status="Fachkraefte"),
        ],
    ],
    113: [
        [
            Noun(
                "m",
                "Kutscher",
                "Kutschers",
                nom_pl="Kutscher",
                dat_pl="Kutschern",
                status="Fachkraefte",
            ),
            Noun("f", "Kutscherin", nom_pl="Kutscherinnen", status="Fachkraefte"),
        ],
    ],
    114: [
        [
            Noun(
                "m",
                "Fischer",
                "Fischers",
                nom_pl="Fischer",
                dat_pl="Fischern",
                status="Fachkraefte",
            ),
            Noun("f", "Fischerin", nom_pl="Fischerinnen", status="Fachkraefte"),
        ],
    ],
    115: [
        [
            Noun(
                "m",
                "Tierpfleger",
                "Tierpflegers",
                nom_pl="Tierpfleger",
                dat_pl="Tierpflegern",
                status="Fachkraefte",
            ),
            Noun("f", "Tierpflegerin", nom_pl="Tierpflegerinnen", status="Fachkraefte"),
        ],
    ],
    116: [
        [
            Noun(
                "m",
                "Winzer",
                "Winzers",
                nom_pl="Winzer",
                dat_pl="Winzern",
                status="Fachkraefte",
            ),
            Noun("f", "Winzerin", nom_pl="Winzerinnen", status="Fachkraefte"),
        ],
    ],
    117: [
        [
            Noun(
                "m",
                "Jäger",
                "Jägers",
                nom_pl="Jäger",
                dat_pl="Jägern",
                status="Fachkraefte",
            ),
            Noun("f", "Jägerin", nom_pl="Jägerinnen", status="Fachkraefte"),
        ],
    ],
    121: [
        [
            Noun(
                "m",
                "Landschaftsgärtner",
                "Landschaftsgärtners",
                nom_pl="Landschaftsgärtner",
                dat_pl="Landschaftsgärtnern",
                status="Fachkraefte",
            ),
            Noun(
                "f", "Landschaftsgärtnerin", nom_pl="Landschaftsgärtnerinnen", status="Fachkraefte"
            ),
        ],
        [
            Noun(
                "m",
                "Gartenarbeiter",
                "Gartenarbeiters",
                nom_pl="Gartenarbeiter",
                dat_pl="Gartenarbeitern",
                status="Helfer",
            ),
            Noun("f", "Gartenarbeiterin", nom_pl="Gartenarbeiterinnen", status="Helfer"),
        ],
    ],
    122: [
        [
            Noun(
                "m",
                "Florist",
                "Floristen",
                "Floristen",
                "Floristen",
                nom_pl="Floristen",
                status="Fachkraefte",
            ),
            Noun("f", "Floristin", nom_pl="Floristinnen", status="Fachkraefte"),
        ],
    ],
    211: [
        [
            Noun(
                "m",
                "Bergarbeiter",
                "Bergarbeiters",
                nom_pl="Bergarbeiter",
                status="Fachkraefte",
            ),
            Noun("f", "Bergarbeiterin", nom_pl="Bergarbeiterinnen", status="Fachkraefte"),
        ]
    ],
    212: [
        [
            Noun(
                "m",
                "Steinmetz",
                "Steinmetzes",
                nom_pl="Steinmetze",
                status="Fachkraefte",
            ),
            Noun("f", "Steinmetzin", nom_pl="Steinmetzinnen", status="Fachkraefte"),
        ],
    ],
    213: [
        [
            Noun(
                "m",
                "Glasbläser",
                "Glasbläsers",
                nom_pl="Glasbläser",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Glasbläserin",
                nom_pl="Glasbläserinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    214: [
        [
            Noun(
                "m",
                "Keramikarbeiter",
                "Keramikarbeiters",
                nom_pl="Keramikarbeiter",
                status="Helfer",
            ),
            Noun("f", "Keramikarbeiterin", nom_pl="Keramikarbeiterinnen", status="Helfer"),
        ],
    ],
    221: [
        [
            Noun(
                "m",
                "Gummiarbeiter",
                "Gummiarbeiters",
                nom_pl="Gummiarbeiter",
                status="Helfer",
            ),
            Noun("f", "Gummiarbeiterin", nom_pl="Gummiarbeiterinnen", status="Helfer"),
        ],
        [
            Noun(
                "m",
                "Reifenbauer",
                "Reifenbauers",
                nom_pl="Reifenbauer",
                status="Fachkraefte",
            ),
            Noun("f", "Reifenbauerin", nom_pl="Reifenbauerinnen", status="Fachkraefte"),
        ],
    ],
    222: [
        [
            Noun(
                "m",
                "Autolackierer",
                "Autolackierers",
                nom_pl="Autolackierer",
                status="Fachkraefte",
            ),
            Noun("f", "Autolackiererin", nom_pl="Autolackiererinnen", status="Fachkraefte"),
        ],
    ],
    223: [
        [
            Noun("m", "Schreiner", "Schreiners", nom_pl="Schreiner", status="Fachkraefte"),
            Noun("f", "Schreinerin", nom_pl="Schreinerinnen", status="Fachkraefte"),
        ],
        [
            Noun("m", "Tischler", "Tischlers", nom_pl="Tischler", status="Fachkraefte"),
            Noun("f", "Tischlerin", nom_pl="Tischlerinnen", status="Fachkraefte"),
        ],
    ],
    231: [
        [
            Noun(
                "m",
                "Papierfärber",
                "Papierfärbers",
                nom_pl="Papierfärber",
                status="Fachkraefte",
            ),
            Noun("f", "Papierfärberin", nom_pl="Papierfärberinnen", status="Fachkraefte"),
        ],
    ],
    232: [
        [
            Noun(
                "m",
                "Werbegrafiker",
                "Werbegrafikers",
                nom_pl="Werbegrafiker",
                status="Spezialisten",
            ),
            Noun("f", "Werbegrafikerin", nom_pl="Werbegrafikerinnen", status="Spezialisten"),
        ],
    ],
    233: [
        [
            Noun(
                "m",
                "Fotograf",
                "Fotografen",
                "Fotografen",
                "Fotografen",
                nom_pl="Fotografen",
                status="Fachkraefte",
            ),
            Noun("f", "Fotografin", nom_pl="Fotografinnen", status="Fachkraefte"),
        ],
    ],
    234: [
        [
            Noun(
                "m",
                "Buchdrucker",
                "Buchdruckers",
                nom_pl="Buchdrucker",
                status="Fachkraefte",
            ),
            Noun("f", "Buchdruckerin", nom_pl="Buchdruckerinnen", status="Fachkraefte"),
        ],
    ],
    241: [
        [
            Noun(
                "m",
                "Stahlarbeiter",
                "Stahlarbeiters",
                nom_pl="Stahlarbeiter",
                status="Fachkraefte",
            ),
            Noun("f", "Stahlarbeiterin", nom_pl="Stahlarbeiterinnen", status="Fachkraefte"),
        ],
    ],
    242: [
        [
            Noun(
                "m",
                "Münzpräger",
                "Münzprägers",
                nom_pl="Münzpräger",
                status="Fachkraefte",
            ),
            Noun("f", "Münzprägerin", nom_pl="Münzprägerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Schleifer",
                "Schleifers",
                nom_pl="Schleifer",
                status="Fachkraefte",
            ),
            Noun("f", "Schleiferin", nom_pl="Schleiferinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Metallarbeiter",
                "Metallarbeiters",
                nom_pl="Metallarbeiter",
                status="Helfer",
            ),
            Noun("f", "Metallarbeiterin", nom_pl="Metallarbeiterinnen", status="Helfer"),
        ],
    ],
    243: [
        [
            Noun(
                "m",
                "Metallfärber",
                "Metallfärbers",
                nom_pl="Metallfärber",
                status="Fachkraefte",
            ),
            Noun("f", "Metallfärberin", nom_pl="Metallfärberinnen", status="Fachkraefte"),
        ],
    ],
    244: [
        [
            Noun("m", "Schlosser", "Schlossers", nom_pl="Schlosser", status="Fachkraefte"),
            Noun("f", "Schlosserin", nom_pl="Schlosserinnen", status="Fachkraefte"),
        ],
        [
            Noun("m", "Schmied", "Schmiedes", nom_pl="Schmiede", status="Fachkraefte"),
            Noun("f", "Schmiedin", nom_pl="Schmiedinnen", status="Fachkraefte"),
        ],
    ],
    245: [
        [
            Noun(
                "m",
                "Uhrmacher",
                "Uhrmachers",
                nom_pl="Uhrmacher",
                status="Fachkraefte",
            ),
            Noun("f", "Uhrmacherin", nom_pl="Uhrmacherinnen", status="Fachkraefte"),
        ],
    ],
    251: [
        [
            Noun(
                "m",
                "Maschinenbauer",
                "Maschinenbauers",
                nom_pl="Maschinenbauer",
                status="Fachkraefte",
            ),
            Noun("f", "Maschinenbauerin", nom_pl="Maschinenbauerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Mechaniker",
                "Mechanikers",
                nom_pl="Mechaniker",
                status="Fachkraefte",
            ),
            Noun("f", "Mechanikerin", nom_pl="Mechanikerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Stromableser",
                "Stromablesers",
                nom_pl="Stromableser",
                status="Helfer",
            ),
            Noun("f", "Stromableserin", nom_pl="Stromableserinnen", status="Helfer"),
        ],
    ],
    252: [
        [
            Noun(
                "m",
                "Automechaniker",
                "Automechanikers",
                nom_pl="Automechaniker",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Automechanikerin",
                nom_pl="Automechanikerinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "m",
                "Schiffbauer",
                "Schiffbauers",
                nom_pl="Schiffbauer",
                status="Fachkraefte",
            ),
            Noun("f", "Schiffbauerin", nom_pl="Schiffbauerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Flugingenieur",
                "Flugingenieurs",
                nom_pl="Flugingenieure",
                status="Experten",
            ),
            Noun(
                "f",
                "Flugingenieurin",
                nom_pl="Flugingenieurinnen",
                status="Experten",
            ),
        ],
    ],
    261: [
        [
            Noun(
                "m",
                "Mechatroniker",
                "Mechatronikers",
                nom_pl="Mechatroniker",
                status="Fachkraefte",
            ),
            Noun("f", "Mechatronikerin", nom_pl="Mechatronikerinnen", status="Fachkraefte"),
        ],
    ],
    262: [
        [
            Noun(
                "m",
                "Elektriker",
                "Elektrikers",
                nom_pl="Elektriker",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Elektrikerin",
                nom_pl="Elektrikerinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "m",
                "Lichtinstallateur",
                "Lichtinstallateurs",
                nom_pl="Lichtinstallateure",
                status="Fachkraefte",
            ),
            Noun("f", "Lichtinstallateurin", nom_pl="Lichtinstallateurinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Solartechniker",
                "Solartechnikers",
                nom_pl="Solartechniker",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Solartechnikerin",
                nom_pl="Solartechnikerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    263: [
        [
            Noun(
                "m",
                "PC-Techniker",
                "PC-Technikers",
                nom_pl="PC-Techniker",
                status="Fachkraefte",
            ),
            Noun("f", "PC-Technikerin", nom_pl="PC-Technikerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Elektrotechniker",
                "Elektrotechnikers",
                nom_pl="Elektrotechniker",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Elektrotechnikerin",
                nom_pl="Elektrotechnikerinnen",
                status="Spezialisten",
            ),
        ],
        [
            Noun(
                "m",
                "Batteriehersteller",
                "Batterieherstellers",
                nom_pl="Batteriehersteller",
                status="Helfer",
            ),
            Noun(
                "f",
                "Batterieherstellerin",
                nom_pl="Batterieherstellerinnen",
                status="Helfer",
            ),
        ],
    ],
    271: [
        [
            Noun(
                "m",
                "Produktentwickler",
                "Produktentwicklers",
                nom_pl="Produktentwickler",
                status="Experten",
            ),
            Noun(
                "f",
                "Produktentwicklerin",
                nom_pl="Produktentwicklerinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m",
                "Patentprüfer",
                "Patentprüfers",
                nom_pl="Patentprüfer",
                status="Experten",
            ),
            Noun("f", "Patentprüferin", nom_pl="Patentprüferinnen", status="Experten"),
        ],
    ],
    272: [
        [
            Noun(
                "m",
                "Bauzeichner",
                "Bauzeichners",
                nom_pl="Bauzeichner",
                status="Fachkraefte",
            ),
            Noun("f", "Bauzeichnerin", nom_pl="Bauzeichnerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Anlagenplaner",
                "Anlagenplaners",
                nom_pl="Anlagenplaner",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Anlagenplanerin",
                nom_pl="Anlagenplanerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    273: [
        [
            Noun(
                "m",
                "Wirtschaftsingenieur",
                "Wirtschaftsingenieurs",
                nom_pl="Wirtschaftsingenieure",
                status="Experten",
            ),
            Noun(
                "f",
                "Wirtschaftsingenieurin",
                nom_pl="Wirtschaftsingenieurinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m",
                "Qualitätsprüfer",
                "Qualitätsprüfers",
                nom_pl="Qualitätsprüfer",
                status="Fachkraefte",
            ),
            Noun("f", "Qualitätsprüferin", nom_pl="Qualitätsprüferinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Geräteprüfer",
                "Geräteprüfers",
                nom_pl="Geräteprüfer",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Geräteprüferin",
                nom_pl="Geräteprüferinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "m",
                "Materialplaner",
                "Materialplaners",
                nom_pl="Materialplaner",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Materialplanerin",
                nom_pl="Materialplanerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    281: [
        [
            Noun(
                "m",
                "Stricker",
                "Strickers",
                nom_pl="Stricker",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Strickerin",
                nom_pl="Strickerinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    282: [
        [
            Noun(
                "m",
                "Schneider",
                "Schneiders",
                nom_pl="Schneider",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Schneiderin",
                nom_pl="Schneiderinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun("m", "Hutmacher", "Hutmachers", nom_pl="Hutmacher", status="Fachkraefte"),
            Noun("f", "Hutmacherin", nom_pl="Hutmacherinnen", status="Fachkraefte"),
        ],
    ],
    283: [
        [
            Noun(
                "m",
                "Schuhmacher",
                "Schuhmachers",
                nom_pl="Schuhmacher",
                status="Fachkraefte",
            ),
            Noun("f", "Schuhmacherin", nom_pl="Schuhmacherinnen", status="Fachkraefte"),
        ],
    ],
    291: [
        [
            Noun("m", "Brauer", "Brauers", nom_pl="Brauer", status="Fachkraefte"),
            Noun("f", "Brauerin", nom_pl="Brauerinnen", status="Fachkraefte"),
        ],
    ],
    292: [
        [
            Noun(
                "m",
                "Bäcker",
                "Bäckers",
                nom_pl="Bäcker",
                status="Fachkraefte",
            ),
            Noun("f", "Bäckerin", nom_pl="Bäckerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Konditor",
                "Konditors",
                nom_pl="Konditoren",
                status="Fachkraefte",
            ),
            Noun("f", "Konditorin", nom_pl="Konditorinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Molkereiarbeiter",
                "Molkereiarbeiters",
                nom_pl="Molkereiarbeiter",
                status="Helfer",
            ),
            Noun(
                "f",
                "Molkereiarbeiterin",
                nom_pl="Molkereiarbeiterinnen",
                status="Helfer",
            ),
        ],
    ],
    293: [
        [
            Noun("m", "Koch", "Kochs", nom_pl="Köche", status="Fachkraefte"),
            Noun("f", "Köchin", nom_pl="Köchinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Küchenhelfer",
                "Küchenhelfers",
                status="Helfer",
            ),
            Noun(
                "f",
                "Küchenhelferin",
                nom_pl="Küchenhelferinnen",
                status="Helfer",
            ),
            Noun(
                "f",
                "Küchenhilfe",
                nom_pl="Küchenhilfen",
                pronouns="dey",
                status="Helfer",
            ),
        ],
        [
            Noun(
                "m",
                "Pizzabäcker",
                "Pizzabäckers",
                nom_pl="Pizzabäcker",
                status="Fachkraefte",
            ),
            Noun("f", "Pizzabäckerin", nom_pl="Pizzabäckerinnen", status="Fachkraefte"),
        ],
    ],
    311: [
        [
            Noun(
                "m",
                "Architekt",
                "Architekten",
                nom_pl="Architekten",
                dat_pl="Architekten",
                status="Experten",
            ),
            Noun("f", "Architektin", nom_pl="Architektinnen", status="Experten"),
        ],
        [
            Noun("m", "Raumplaner", "Raumplaners", nom_pl="Raumplaner", status="Experten"),
            Noun("f", "Raumplanerin", nom_pl="Raumplanerinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Baustellenprüfer",
                "Baustellenprüfers",
                nom_pl="Baustellenprüfer",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Baustellenprüferin",
                nom_pl="Baustellenprüferinnen",
                status="Spezialisten",
            ),
        ],
    ],
    312: [
        [
            Noun(
                "m",
                "Kartograf",
                "Kartografen",
                "Kartografen",
                "Kartografen",
                "Kartografen",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Kartografin",
                nom_pl="Kartografinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    321: [
        [
            Noun(
                "m",
                "Maurer",
                "Maurers",
                nom_pl="Maurer",
                dat_pl="Maurern",
                status="Fachkraefte",
            ),
            Noun("f", "Maurerin", nom_pl="Maurerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Dachdecker",
                "Dachdeckers",
                nom_pl="Dachdecker",
                dat_pl="Dachdeckern",
                status="Fachkraefte",
            ),
            Noun("f", "Dachdeckerin", nom_pl="Dachdeckerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Bauarbeiter",
                "Bauarbeiters",
                nom_pl="Bauarbeiter",
                dat_pl="Bauarbeitern",
                status="Helfer",
            ),
            Noun("f", "Bauarbeiterin", nom_pl="Bauarbeiterinnen", status="Helfer"),
        ],
    ],
    322: [
        [
            Noun(
                "m",
                "Kanalbauer",
                "Kanalbauers",
                nom_pl="Kanalbauer",
                dat_pl="Kanalbauern",
                status="Fachkraefte",
            ),
            Noun("f", "Kanalbauerin", nom_pl="Kanalbauerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Teerer",
                "Teerers",
                status="Helfer",
            ),
            Noun("f", "Teererin", nom_pl="Teererinnen", status="Helfer"),
        ],
    ],
    331: [
        [
            Noun(
                "m",
                "Fliesenleger",
                "Fliesenlegers",
                nom_pl="Fliesenleger",
                dat_pl="Fliesenlegern",
                status="Fachkraefte",
            ),
            Noun("f", "Fliesenlegerin", nom_pl="Fliesenlegerinnen", status="Fachkraefte"),
        ],
    ],
    332: [
        [
            Noun(
                "m",
                "Maler",
                "Malers",
                nom_pl="Maler",
                dat_pl="Malern",
                status="Fachkraefte",
            ),
            Noun("f", "Malerin", nom_pl="Malerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Malerhelfer",
                "Malerhelfers",
                status="Helfer",
            ),
            Noun("f", "Malerhelferin", nom_pl="Malerhelferinnen", status="Helfer"),
            Noun("f", "Malerhilfe", status="Helfer", pronouns="dey"),
        ],
    ],
    333: [
        [
            Noun(
                "m",
                "Autoglaser",
                "Autoglasers",
                nom_pl="Autoglaser",
                dat_pl="Autoglasern",
                status="Fachkraefte",
            ),
            Noun("f", "Autoglaserin", nom_pl="Autoglaserinnen", status="Fachkraefte"),
        ],
    ],
    341: [
        [
            Noun(
                "m",
                "Hausmeister",
                "Hausmeisters",
                nom_pl="Hausmeister",
                status="Fachkraefte",
            ),
            Noun("f", "Hausmeisterin", nom_pl="Hausmeisterinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Platzwart",
                "Platzwarts",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Platzwartin",
                nom_pl="Platzwartinnen",
                status="Spezialisten",
            ),
        ],
    ],
    342: [
        [
            Noun("m", "Klempner", "Klempners", nom_pl="Klempner", status="Fachkraefte"),
            Noun("f", "Klempnerin", nom_pl="Klempnerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Wärmetechniker",
                "Wärmetechnikers",
                nom_pl="Wärmetechniker",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Wärmetechnikerin",
                nom_pl="Wärmetechnikerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    343: [
        [
            Noun("m", "Rohrbauer", "Rohrbauers", nom_pl="Rohrbauer", status="Fachkraefte"),
            Noun("f", "Rohrbauerin", nom_pl="Rohrbauerinnen", status="Fachkraefte"),
        ],
        [
            Noun("m", "Müllmann", "Müllmanns", nom_pl="Müllmänner", status="Helfer"),
            Noun("f", "Müllfrau", nom_pl="Müllfrauen", status="Helfer"),
        ],
    ],
    411: [
        [
            Noun(
                "m",
                "Mathematiker",
                "Mathematikers",
                nom_pl="Mathematiker",
                status="Experten",
            ),
            Noun("f", "Mathematikerin", nom_pl="Mathematikerinnen", status="Experten"),
        ],
    ],
    412: [
        [
            Noun(
                "m",
                "Biologe",
                "Biologen",
                "Biologen",
                "Biologen",
                nom_pl="Biologen",
                status="Experten",
            ),
            Noun("f", "Biologin", nom_pl="Biologinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Biolaborant",
                "Biolaboranten",
                "Biolaboranten",
                "Biolaboranten",
                nom_pl="Biolaboranten",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Biolaborantin",
                nom_pl="Biolaborantinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    413: [
        [
            Noun("m", "Chemiker", "Chemikers", nom_pl="Chemiker", status="Experten"),
            Noun("f", "Chemikerin", nom_pl="Chemikerinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Chemielaborant",
                "Chemielaboranten",
                "Chemielaboranten",
                "Chemielaboranten",
                nom_pl="Chemielaboranten",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Chemielaborantin",
                nom_pl="Chemielaborantinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    414: [
        [
            Noun("m", "Physiker", "Physikers", nom_pl="Physiker", status="Experten"),
            Noun("f", "Physikerin", nom_pl="Physikerinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Materialprüfer",
                "Materialprüfers",
                nom_pl="Materialprüfer",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Materialprüferin",
                nom_pl="Materialprüferinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    421: [
        [
            Noun(
                "m",
                "Meteorologe",
                "Meteorologen",
                "Meteorologen",
                "Meteorologen",
                nom_pl="Meteorologen",
                status="Experten",
            ),
            Noun("f", "Meteorologin", nom_pl="Meteorologinnen", status="Experten"),
        ],
    ],
    422: [
        [
            Noun(
                "m",
                "Schornsteinfeger",
                "Schornsteinfegers",
                nom_pl="Schornsteinfeger",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Schornsteinfegerin",
                nom_pl="Schornsteinfegerinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    423: [
        [
            Noun(
                "m",
                "Umweltbeauftragter",
                "Umweltbeauftragten",
                "Umweltbeauftragten",
                "Umweltbeauftragten",
                nom_pl="Umweltbeauftragte",
                acc_pl="Umweltbeauftragte",
                status="Experten",
            ),
            Noun(
                "f",
                "Umweltbeauftragte",
                "Umweltbeauftragten",
                "Umweltbeauftragten",
                nom_pl="Umweltbeauftragte",
                acc_pl="Umweltbeauftragte",
                status="Experten",
            ),
        ],
    ],
    431: [
        [
            Noun(
                "m",
                "Informatiker",
                "Informatikers",
                nom_pl="Informatiker",
                status="Experten",
            ),
            Noun("f", "Informatikerin", nom_pl="Informatikerinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Webentwickler",
                "Webentwicklers",
                nom_pl="Webentwickler",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Webentwicklerin",
                nom_pl="Webentwicklerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    432: [
        [
            Noun(
                "m",
                "Systemanalytiker",
                "Systemanalytikers",
                nom_pl="Systemanalytiker",
                status="Experten",
            ),
            Noun(
                "f",
                "Systemanalytikerin",
                nom_pl="Systemanalytikerinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m",
                "IT-Berater",
                "IT-Beraters",
                nom_pl="IT-Berater",
                status="Spezialisten",
            ),
            Noun("f", "IT-Beraterin", nom_pl="IT-Beraterinnen", status="Spezialisten"),
            Noun(
                "f",
                "IT-Beratungs",
                nom_pl="IT-Beratungen",
                pronouns="dey",
                status="Spezialisten",
            ),
        ],
    ],
    433: [
        [
            Noun(
                "m",
                "Softwaretester",
                "Softwaretesters",
                nom_pl="Softwaretester",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Softwaretesterin",
                nom_pl="Softwaretesterinnen",
                status="Spezialisten",
            ),
        ],
    ],
    434: [
        [
            Noun(
                "m",
                "Softwareentwickler",
                "Softwareentwicklers",
                nom_pl="Softwareentwickler",
                status="Experten",
            ),
            Noun(
                "f",
                "Softwareentwicklerin",
                nom_pl="Softwareentwicklerinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m",
                "Systemprogrammierer",
                "Systemprogrammierers",
                nom_pl="Systemprogrammierer",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Systemprogrammiererin",
                nom_pl="Systemprogrammiererinnen",
                status="Spezialisten",
            ),
        ],
    ],
    511: [
        [
            Noun(
                "m",
                "Matrose",
                "Matrosen",
                "Matrosen",
                "Matrosen",
                nom_pl="Matrosen",
                status="Fachkraefte",
            ),
            Noun("f", "Matrosin", nom_pl="Matrosinnen", status="Fachkraefte"),
        ],
    ],
    512: [
        [
            Noun(
                "m",
                "Hafenaufseher",
                "Hafenaufsehers",
                nom_pl="Hafenaufseher",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Hafenaufseherin",
                nom_pl="Hafenaufseherinnen",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Hafenaufsicht",
                nom_pl="Hafenaufsichten",
                pronouns="dey",
                status="Fachkraefte",
            ),
        ],
    ],
    513: [
        [
            Noun(
                "m",
                "Postbote",
                "Postboten",
                "Postboten",
                "Postboten",
                nom_pl="Postboten",
                status="Fachkraefte",
            ),
            Noun("f", "Postbotin", nom_pl="Postbotinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Möbelpacker",
                "Möbelpackers",
                nom_pl="Möbelpacker",
                status="Helfer",
            ),
            Noun("f", "Möbelpackerin", nom_pl="Möbelpackerinnen", status="Helfer"),
        ],
        [
            Noun(
                "m",
                "Zeitungsausträger",
                "Zeitungsausträgers",
                nom_pl="Zeitungsausträger",
                status="Helfer",
            ),
            Noun("f", "Zeitungsausträgerin", nom_pl="Zeitungsausträgerinnen", status="Helfer"),
        ],
    ],
    514: [
        [
            Noun(
                "m",
                "Zugbegleiter",
                "Zugbegleiters",
                nom_pl="Zugbegleiter",
                status="Fachkraefte",
            ),
            Noun("f", "Zugbegleiterin", nom_pl="Zugbegleiterinnen", status="Fachkraefte"),
            Noun(
                "f",
                "Zugbegleitung",
                nom_pl="Zugbegleitungen",
                status="Fachkraefte",
                pronouns="dey",
            ),
        ],
    ],
    515: [
        [
            Noun(
                "m",
                "Fahrdienstleiter",
                "Fahrdienstleiters",
                nom_pl="Fahrdienstleiter",
                status="Fachkraefte",
            ),
            Noun("f", "Fahrdienstleiterin", nom_pl="Fahrdienstleiterin", status="Fachkraefte"),
            Noun(
                "f",
                "Fahrdienstleitung",
                nom_pl="Fahrdienstleitung",
                status="Fachkraefte",
                pronouns="dey",
            ),
        ],
        [
            Noun(
                "m",
                "Lotse",
                "Lotsen",
                "Lotsen",
                "Lotsen",
                nom_pl="Lotsen",
                status="Spezialisten",
            ),
            Noun("f", "Lotsin", nom_pl="Lotsinnen", status="Spezialisten"),
        ],
    ],
    516: [
        [
            Noun("m", "Logistiker", "Logistikers", nom_pl="Logistiker", status="Experten"),
            Noun("f", "Logistikerin", nom_pl="Logistikerinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Postbeamte",
                "Postbeamten",
                nom_pl="Postbeamte",
                status="Fachkraefte",
            ),
            Noun("f", "Postbeamtin", nom_pl="Postbeamtinnen", status="Fachkraefte"),
        ],
    ],
    521: [
        [
            Noun("m", "Busfahrer", "Busfahrers", nom_pl="Busfahrer", status="Fachkraefte"),
            Noun("f", "Busfahrerin", nom_pl="Busfahrerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Taxifahrer",
                "Taxifahrers",
                nom_pl="Taxifahrer",
                status="Fachkraefte",
            ),
            Noun("f", "Taxifahrerin", nom_pl="Taxifahrerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "LKW-Fahrer",
                "LKW-Fahrers",
                nom_pl="LKW-Fahrer",
                status="Fachkraefte",
            ),
            Noun("f", "LKW-Fahrerin", nom_pl="LKW-Fahrerinnen", status="Fachkraefte"),
        ],
    ],
    522: [
        [
            Noun("m", "Lokführer", "Lokführers", nom_pl="Lokführer", status="Fachkraefte"),
            Noun("f", "Lokführerin", nom_pl="Lokführerinnen", status="Fachkraefte"),
        ],
    ],
    523: [
        [
            Noun(
                "m",
                "Pilot",
                "Piloten",
                "Piloten",
                "Piloten",
                nom_pl="Piloten",
                status="Experten",
            ),
            Noun("f", "Pilotin", nom_pl="Pilotinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Ballonfahrer",
                "Ballonfahrers",
                nom_pl="Ballonfahrer",
                status="Spezialisten",
            ),
            Noun("f", "Ballonfahrerin", nom_pl="Ballonfahrerinnen", status="Spezialisten"),
        ],
    ],
    524: [
        [
            Noun("m", "Kapitän", "Kapitäns", nom_pl="Kapitäne", status="Experten"),
            Noun("f", "Kapitänin", nom_pl="Kapitäninnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Bootsführer",
                "Bootsführers",
                nom_pl="Bootsführer",
                status="Spezialisten",
            ),
            Noun("f", "Bootsführerin", nom_pl="Bootsführerinnen", status="Spezialisten"),
        ],
    ],
    525: [
        [
            Noun(
                "m",
                "Kranführer",
                "Kranführers",
                nom_pl="Kranführer",
                status="Fachkraefte",
            ),
            Noun("f", "Kranführerin", nom_pl="Kranführerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Staplerfahrer",
                "Staplerfahrers",
                nom_pl="Staplerfahrer",
                status="Helfer",
            ),
            Noun(
                "f",
                "Staplerfahrerin",
                nom_pl="Staplerfahrerinnen",
                status="Helfer",
            ),
        ],
    ],
    531: [
        [
            Noun("m", "Detektiv", "Detektivs", nom_pl="Detektive", status="Fachkraefte"),
            Noun("f", "Detektivin", nom_pl="Detektivinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Feuerwehrmann",
                "Feuerwehrmanns",
                nom_pl="Feuerwehrmänner",
                status="Fachkraefte",
            ),
            Noun("f", "Feuerwehrfrau", nom_pl="Feuerwehrfrauen", status="Fachkraefte"),
        ],
        [
            Noun("m", "Bademeister", status="Fachkraefte"),
            Noun("f", "Bademeisterin", status="Fachkraefte"),
            Noun("f", "Badeaufsicht", status="Fachkraefte", pronouns="dey"),
        ],
        [
            Noun("m", "Pförtner", "Pförtners", nom_pl="Pförtner", status="Helfer"),
            Noun("f", "Pförtnerin", nom_pl="Pförtnerinnen", status="Helfer"),
        ],
        [
            Noun("m", "Türsteher", "Türstehers", nom_pl="Türsteher", status="Helfer"),
            Noun("f", "Türsteherin", nom_pl="Türsteherinnen", status="Helfer"),
        ],
    ],
    532: [
        [
            Noun(
                "m",
                "Polizist",
                "Polizisten",
                nom_pl="Polizisten",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Polizistin",
                nom_pl="Polizistinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    533: [
        [
            Noun(
                "m",
                "Kammerjäger",
                "Kammerjägers",
                nom_pl="Kammerjäger",
                status="Fachkraefte",
            ),
            Noun("f", "Kammerjägerin", nom_pl="Kammerjägerinnen", status="Fachkraefte"),
        ],
    ],
    541: [
        [
            Noun(
                "f",
                "Reinigungskraft",
                nom_pl="Reinigungskräfte",
                pronouns="er",
                status="Helfer",
            ),
            Noun(
                "f",
                "Reinigungskraft",
                nom_pl="Reinigungskräfte",
                pronouns="sie",
                status="Helfer",
            ),
            Noun(
                "f",
                "Reinigungskraft",
                nom_pl="Reinigungskräfte",
                pronouns="dey",
                status="Helfer",
            ),
        ],
        [
            Noun(
                "m",
                "Putzmann",
                "Putzmannes",
                nom_pl="Putzmänner",
                status="Helfer",
            ),
            Noun("f", "Putzfrau", nom_pl="Putzfrauen", status="Helfer"),
            Noun("f", "Putzhilfe", nom_pl="Putzhilfen", pronouns="dey", status="Helfer"),
        ],
    ],
    611: [
        [
            Noun("m", "Videothekar", "Videothekars", nom_pl="Videothekare", status="Fachkraefte"),
            Noun("f", "Videothekarin", nom_pl="Videothekarinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Handelsvertreter",
                "Handelsvertreters",
                nom_pl="Handelsvertreter",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Handelsvertreterin",
                nom_pl="Handelsvertreterinnen",
                status="Spezialisten",
            ),
        ],
    ],
    612: [
        [
            Noun(
                "m",
                "Großhändler",
                "Großhändlers",
                nom_pl="Großhändler",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Großhändlerin",
                nom_pl="Großhändlerinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    613: [
        [
            Noun(
                "m",
                "Immobilienmakler",
                "Immobilienmaklers",
                nom_pl="Immobilienmakler",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Immobilienmaklerin",
                nom_pl="Immobilienmaklerinnen",
                status="Spezialisten",
            ),
        ],
        [
            Noun(
                "m",
                "Hausverwalter",
                "Hausverwalters",
                nom_pl="Hausverwalter",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Hausverwalterin",
                nom_pl="Hausverwalterinnen",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Hausverwaltung",
                nom_pl="Hausverwaltungen",
                status="Spezialisten",
                pronouns="dey",
            ),
        ],
    ],
    621: [
        [
            Noun("m", "Verkäufer", "Verkäufers", nom_pl="Verkäufer", status="Fachkraefte"),
            Noun("f", "Verkäuferin", nom_pl="Verkäuferinnen", status="Fachkraefte"),
        ],
        [
            Noun("m", "Kassierer", "Kassierers", nom_pl="Kassierer", status="Fachkraefte"),
            Noun("f", "Kassiererin", nom_pl="Kassiererinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Regalauffüller",
                "Regalauffüllers",
                nom_pl="Regalauffüller",
                status="Helfer",
            ),
            Noun("f", "Regalauffüllerin", nom_pl="Regalauffüllerinnen", status="Helfer"),
        ],
    ],
    622: [
        [
            Noun(
                "m",
                "Juwelier",
                "Juweliers",
                nom_pl="Juwelier",
                status="Fachkraefte",
            ),
            Noun("f", "Juwelierin", nom_pl="Juwelierinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Autohändler",
                "Autohändlers",
                nom_pl="Autohändler",
                status="Fachkraefte",
            ),
            Noun("f", "Autohändlerin", nom_pl="Autohändlerinnen", status="Fachkraefte"),
        ],
    ],
    623: [
        [
            Noun(
                "m",
                "Gemüsehändler",
                "Gemüsehändlers",
                nom_pl="Gemüsehändler",
                status="Fachkraefte",
            ),
            Noun("f", "Gemüsehändlerin", nom_pl="Gemüsehändlerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Fischverkäufer",
                "Fischverkäufers",
                nom_pl="Fischverkäufer",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Fischverkäuferin",
                nom_pl="Fischverkäuferinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "m",
                "Eisverkäufer",
                "Eisverkäufers",
                nom_pl="Eisverkäufer",
                status="Helfer",
            ),
            Noun("f", "Eisverkäuferin", nom_pl="Eisverkäuferinnen", status="Helfer"),
        ],
    ],
    624: [
        [
            Noun(
                "m",
                "Drogerieverkäufer",
                "Drogerieverkäufers",
                nom_pl="Drogerieverkäufer",
                status="Fachkraefte",
            ),
            Noun("f", "Drogerieverkäuferin", nom_pl="Drogerieverkäuferinnen", status="Fachkraefte"),
        ],
    ],
    625: [
        [
            Noun(
                "m",
                "Buchhändler",
                "Buchhändlers",
                nom_pl="Buchhändler",
                status="Fachkraefte",
            ),
            Noun("f", "Buchhändlerin", nom_pl="Buchhändlerinnen", status="Fachkraefte"),
        ],
    ],
    631: [
        [
            Noun(
                "m",
                "Reiseleiter",
                "Reiseleiters",
                nom_pl="Reiseleiter",
                status="Fachkraefte",
            ),
            Noun("f", "Reiseleiterin", nom_pl="Reiseleiterinnen", status="Fachkraefte"),
            Noun("f", "Reiseleitung", status="Fachkraefte", pronouns="dey"),
        ],
    ],
    632: [
        [
            Noun(
                "m",
                "Rezeptionist",
                "Rezeptionisten",
                "Rezeptionisten",
                "Rezeptionisten",
                nom_pl="Rezeptionisten",
                status="Fachkraefte",
            ),
            Noun("f", "Rezeptionistin", nom_pl="Rezeptionistinnen", status="Fachkraefte"),
        ],
        [
            Noun("m", "Roomboy", "Roomboys", nom_pl="Roomboys", status="Helfer"),
            Noun(
                "n",
                "Zimmermädchen",
                "Zimmermädchens",
                nom_pl="Zimmermädchen",
                status="Helfer",
                pronouns="sie",
            ),
        ],
    ],
    633: [
        [
            Noun("m", "Kellner", "Kellners", nom_pl="Kellner", status="Fachkraefte"),
            Noun("f", "Kellnerin", nom_pl="Kellnerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m", "Barista", "Baristas", nom_pl="Baristas", status="Fachkraefte", pronouns="er"
            ),
            Noun("f", "Barista", nom_pl="Baristas", status="Fachkraefte"),
            Noun(
                "m", "Barista", "Baristas", nom_pl="Baristas", status="Fachkraefte", pronouns="dey"
            ),
        ],
        [
            Noun(
                "m",
                "Tellerwäscher",
                "Tellerwäschers",
                nom_pl="Tellerwäscher",
                status="Helfer",
            ),
            Noun("f", "Tellerwäscherin", nom_pl="Tellerwäscherinnen", status="Helfer"),
        ],
    ],
    634: [
        [
            Noun("m", "Host", "Hosts", nom_pl="Hosts", status="Helfer"),
            Noun("f", "Hostess", nom_pl="Hostessen", status="Helfer"),
        ],
        [
            Noun(
                "m",
                "Eventmanager",
                "Eventmanagers",
                nom_pl="Eventmanager",
                status="Spezialisten",
            ),
            Noun("f", "Eventmanagerin", nom_pl="Eventmanagerinnen", status="Spezialisten"),
        ],
    ],
    711: [
        [
            Noun(
                "m",
                "Geschäftsführer",
                "Geschäftsführers",
                nom_pl="Geschäftsführer",
                status="Experten",
            ),
            Noun(
                "f",
                "Geschäftsführerin",
                nom_pl="Geschäftsführerinnen",
                status="Experten",
            ),
            Noun("f", "Geschäftsführung", status="Experten", pronouns="dey"),
        ],
    ],
    712: [
        [
            Noun(
                "m",
                "Abgeordneter",
                "Abgeordneten",
                "Abgeordneten",
                "Abgeordneten",
                nom_pl="Abgeordnete",
                status="Experten",
            ),
            Noun(
                "f",
                "Abgeordnete",
                "Abgeordneten",
                "Abgeordneten",
                "Abgeordneten",
                nom_pl="Abgeordneten",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m",
                "Bürgermeister",
                "Bürgermeisters",
                nom_pl="Bürgermeister",
                status="Experten",
            ),
            Noun("f", "Bürgermeisterin", nom_pl="Bürgermeisterinnen", status="Experten"),
            Noun("n", "Stadtoberhaupt", status="Experten", pronouns="dey"),
        ],
    ],
    713: [
        [
            Noun(
                "m",
                "Organisator",
                "Organisators",
                acc_sg="Organisator",
                dat_sg="Organisator",
                nom_pl="Organisatoren",
                status="Experten",
            ),
            Noun("f", "Organisatorin", nom_pl="Organisatorinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Betriebsassistent",
                "Betriebsassistenten",
                "Betriebsassistenten",
                "Betriebsassistenten",
                nom_pl="Betriebsassistenten",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Betriebsassistentin",
                nom_pl="Betriebsassistentinnen",
                status="Fachkraefte",
            ),
            Noun("f", "Betriebsassistenz", status="Fachkraefte", pronouns="dey"),
        ],
    ],
    714: [
        [
            Noun("m", "Sekretär", "Sekretärs", nom_pl="Sekretäre", status="Fachkraefte"),
            Noun("f", "Sekretärin", nom_pl="Sekretärinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Büroassistent",
                "Büroassistenten",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Büroassistentin",
                nom_pl="Büroassistentinnen",
                status="Fachkraefte",
            ),
            Noun("f", "Büroassistenz", status="Fachkraefte", pronouns="dey"),
        ],
        [
            Noun(
                "m",
                "Telefonist",
                "Telefonisten",
                "Telefonisten",
                "Telefonisten",
                nom_pl="Telefonisten",
                status="Helfer",
            ),
            Noun("f", "Telefonistin", nom_pl="Telefonistinnen", status="Helfer"),
        ],
        [
            Noun(
                "m",
                "Chefsekretär",
                "Chefsekretärs",
                nom_pl="Chefsekretäre",
                status="Spezialisten",
            ),
            Noun("f", "Chefsekretärin", nom_pl="Chefsekretärinnen", status="Spezialisten"),
        ],
    ],
    715: [
        [
            Noun(
                "m",
                "Ausbildungsleiter",
                "Ausbildungsleiters",
                nom_pl="Ausbildungsleiter",
                status="Experten",
            ),
            Noun(
                "f",
                "Ausbildungsleiterin",
                nom_pl="Ausbildungsleiterinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m",
                "Arbeitsvermittler",
                "Arbeitsvermittlers",
                nom_pl="Arbeitsvermittler",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Arbeitsvermittlerin",
                nom_pl="Arbeitsvermittlerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    721: [
        [
            Noun(
                "m",
                "Vermögensberater",
                "Vermögensberaters",
                nom_pl="Vermögensberater",
                status="Experten",
            ),
            Noun(
                "f",
                "Vermögensberaterin",
                nom_pl="Vermögensberaterinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m",
                "Bankmitarbeiter",
                "Bankmitarbeiters",
                nom_pl="Bankmitarbeiter",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Bankmitarbeiterin",
                nom_pl="Bankmitarbeiterinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "m",
                "Börsenmakler",
                "Börsenmaklers",
                nom_pl="Börsenmakler",
                status="Spezialisten",
            ),
            Noun("f", "Börsenmaklerin", nom_pl="Börsenmaklerinnen", status="Spezialisten"),
        ],
    ],
    722: [
        [
            Noun(
                "m",
                "Wirtschaftsprüfer",
                "Wirtschaftsprüfers",
                nom_pl="Wirtschaftsprüfer",
                status="Experten",
            ),
            Noun(
                "f",
                "Wirtschaftsprüferin",
                nom_pl="Wirtschaftsprüferinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m",
                "Buchhalter",
                "Buchhalters",
                nom_pl="Buchhalter",
                status="Spezialisten",
            ),
            Noun("f", "Buchhalterin", nom_pl="Buchhalterinnen", status="Spezialisten"),
        ],
    ],
    723: [
        [
            Noun(
                "m",
                "Steuerberater",
                "Steuerberaters",
                nom_pl="Steuerberater",
                status="Experten",
            ),
            Noun("f", "Steuerberaterin", nom_pl="Steuerberaterinnen", status="Experten"),
        ],
    ],
    731: [
        [
            Noun("m", "Richter", "Richters", nom_pl="Richter", status="Experten"),
            Noun("f", "Richterin", nom_pl="Richterinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Jurist",
                "Juristen",
                "Juristen",
                "Juristen",
                nom_pl="Juristen",
                status="Experten",
            ),
            Noun("f", "Juristin", nom_pl="Juristinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Anwaltssekretär",
                "Anwaltssekretärs",
                nom_pl="Anwaltssekretäre",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Anwaltssekretärin",
                nom_pl="Anwaltssekretärinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    732: [
        [
            Noun(
                "m",
                "Arztsekretär",
                "Arztsekretärs",
                nom_pl="Arztsekretäre",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Arztsekretärin",
                nom_pl="Arztsekretärinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "m",
                "Verwaltungsangestellte",
                "Verwaltungsangestellten",
                nom_pl="Verwaltungsangestellte",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Verwaltungsangestellte",
                "Verwaltungsangestellten",
                nom_pl="Verwaltungsangestellten",
                status="Fachkraefte",
            ),
        ],
    ],
    733: [
        [
            Noun(
                "m",
                "Büchereiangestellte",
                "Büchereiangestellten",
                nom_pl="Büchereiangestellten",
                status="Experten",
            ),
            Noun("f", "Büchereiangestellte", nom_pl="Büchereiangestellten", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Archivar",
                "Archivars",
                acc_sg="Archivar",
                dat_sg="Archivar",
                nom_pl="Archivare",
                status="Spezialisten",
            ),
            Noun("f", "Archivarin", nom_pl="Archivarinnen", status="Spezialisten"),
        ],
    ],
    811: [
        [
            Noun(
                "m",
                "Arzthelfer",
                "Arzthelfers",
                nom_pl="Arzthelfer",
                dat_pl="Arzthelfern",
                status="Fachkraefte",
            ),
            Noun("f", "Arzthelferin", nom_pl="Arzthelferinnen", status="Fachkraefte"),
            Noun(
                "f",
                "Arzthilfe",
                nom_pl="Arzthilfen",
                status="Fachkraefte",
                pronouns="dey",
            ),
        ],
        [
            Noun(
                "m",
                "Coronatester",
                "Coronatesters",
                status="Fachkraefte",
            ),
            Noun("f", "Coronatesterin", nom_pl="Coronatesterinnen", status="Fachkraefte"),
        ],
    ],
    812: [
        [
            Noun(
                "m",
                "Pathologe",
                "Pathologen",
                "Pathologen",
                "Pathologen",
                nom_pl="Pathologen",
                status="Experten",
            ),
            Noun("f", "Pathologin", nom_pl="Pathologinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Radiologieassistent",
                "Radiologieassistenten",
                "Radiologieassistenten",
                "Radiologieassistenten",
                nom_pl="Radiologieassistenten",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Radiologieassistentin",
                nom_pl="Radiologieassistentinnen",
                status="Fachkraefte",
            ),
            Noun("f", "Radiologieassistenz", status="Fachkraefte", pronouns="dey"),
        ],
    ],
    813: [
        [
            Noun(
                "m",
                "Pflegeassistent",
                "Pflegeassistenten",
                "Pflegeassistenten",
                "Pflegeassistenten",
                nom_pl="Pflegeassistenten",
                status="Helfer",
            ),
            Noun("f", "Pflegeassistentin", nom_pl="Pflegeassistentinnen", status="Helfer"),
            Noun("f", "Pflegeassistenz", status="Helfer", pronouns="dey"),
        ],
        [
            Noun("f", "Hebamme", nom_pl="Hebammen", status="Spezialisten", pronouns="er"),
            Noun("f", "Hebamme", nom_pl="Hebammen", status="Spezialisten", pronouns="sie"),
            Noun("f", "Hebamme", nom_pl="Hebammen", status="Spezialisten", pronouns="dey"),
        ],
        [
            Noun(
                "m",
                "Krankenpfleger",
                "Krankenpflegers",
                nom_pl="Krankenpfleger",
                dat_pl="Krankenpflegern",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Krankenpflegerin",
                nom_pl="Krankenpflegerinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "m",
                "Rettungssanitäter",
                "Rettungssanitäters",
                nom_pl="Rettungssanitäter",
                dat_pl="Rettungssanitätern",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Rettungssanitäterin",
                nom_pl="Rettungssanitäterinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    814: [
        [
            Noun(
                "m",
                "Arzt",
                "Arztes",
                nom_pl="Ärzte",
                dat_pl="Ärzten",
                acc_pl="Ärzte",
                status="Experten",
            ),
            Noun("f", "Ärztin", nom_pl="Ärztinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Zahnarzt",
                "Zahnarztes",
                nom_pl="Zahnärzte",
                dat_pl="Zahnärzten",
                acc_pl="Zahnärzte",
                status="Experten",
            ),
            Noun("f", "Zahnärztin", nom_pl="Zahnärztinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Chirurg",
                "Chirurgen",
                "Chirurgen",
                "Chirurgen",
                nom_pl="Chirurgen",
                status="Experten",
            ),
            Noun("f", "Chirurgin", nom_pl="Chirurginnen", status="Experten"),
        ],
    ],
    815: [
        [
            Noun(
                "m",
                "Tierarzt",
                "Tierarztes",
                nom_pl="Tierärzte",
                dat_pl="Tierärzten",
                acc_pl="Tierärzte",
                status="Experten",
            ),
            Noun("f", "Tierärztin", nom_pl="Tierärztinnen", status="Experten"),
        ],
    ],
    816: [
        [
            Noun(
                "m",
                "Psychotherapeut",
                "Psychotherapeuten",
                "Psychotherapeuten",
                "Psychotherapeuten",
                nom_pl="Psychotherapeuten",
                status="Experten",
            ),
            Noun(
                "f",
                "Psychotherapeutin",
                nom_pl="Psychotherapeutinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m",
                "Suchttherapeut",
                "Suchttherapeuten",
                "Suchttherapeuten",
                "Suchttherapeuten",
                nom_pl="Suchttherapeuten",
                status="Experten",
            ),
            Noun("f", "Suchttherapeutin", nom_pl="Suchttherapeutinnen", status="Experten"),
        ],
    ],
    817: [
        [
            Noun(
                "m",
                "Physiotherapeut",
                "Physiotherapeuten",
                "Physiotherapeuten",
                "Physiotherapeuten",
                nom_pl="Physiotherapeuten",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Physiotherapeutin",
                nom_pl="Physiotherapeutinnen",
                status="Spezialisten",
            ),
        ],
        [
            Noun(
                "m",
                "Logopäde",
                "Logopäden",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Logopädin",
                nom_pl="Logopädinnen",
                status="Spezialisten",
            ),
        ],
        [
            Noun(
                "m",
                "Masseur",
                "Masseurs",
                nom_pl="Masseure",
                dat_pl="Masseuren",
                acc_pl="Masseure",
                status="Fachkraefte",
            ),
            Noun("f", "Masseurin", nom_pl="Masseurinnen", status="Fachkraefte"),
        ],
    ],
    818: [
        [
            Noun(
                "m",
                "Apotheker",
                "Apothekers",
                nom_pl="Apotheker",
                dat_pl="Apothekern",
                status="Experten",
            ),
            Noun("f", "Apothekerin", nom_pl="Apothekerinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Pharmalaborant",
                "Pharmalaboranten",
                "Pharmalaboranten",
                "Pharmalaboranten",
                nom_pl="Pharmalaboranten",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Pharmalaborantin",
                nom_pl="Pharmalaborantinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "m",
                "Pharmazeut",
                "Pharmazeuten",
                "Pharmazeuten",
                "Pharmazeuten",
                nom_pl="Pharmazeuten",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Pharmazeutin",
                nom_pl="Pharmazeutinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    821: [
        [
            Noun(
                "m",
                "Altenpfleger",
                "Altenpflegers",
                nom_pl="Altenpfleger",
                dat_pl="Altenpflegern",
                status="Fachkraefte",
            ),
            Noun("f", "Altenpflegerin", nom_pl="Altenpflegerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Pflegehelfer",
                "Pflegehelfers",
                nom_pl="Pflegehelfer",
                dat_pl="Pflegehelfern",
                status="Helfer",
            ),
            Noun(
                "f",
                "Pflegehilfe",
                nom_pl="Pflegehilfen",
                status="Helfer",
                pronouns="dey",
            ),
            Noun("f", "Pflegehelferin", nom_pl="Pflegehelferinnen", status="Helfer"),
        ],
    ],
    822: [
        [
            Noun(
                "m",
                "Ernährungsberater",
                "Ernährungsberaters",
                nom_pl="Ernährungsberater",
                dat_pl="Ernährungsberatern",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Ernährungsberaterin",
                nom_pl="Ernährungsberaterinnen",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Ernährungsberatung",
                nom_pl="Ernährungsberatungen",
                status="Spezialisten",
                pronouns="dey",
            ),
        ],
    ],
    823: [
        [
            Noun(
                "m",
                "Friseur",
                "Friseurs",
                nom_pl="Friseure",
                dat_pl="Friseuren",
                acc_pl="Friseure",
                status="Fachkraefte",
            ),
            Noun("f", "Friseurin", nom_pl="Friseurinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Tätowierer",
                "Tätowierers",
                nom_pl="Tätowierer",
                dat_pl="Tätowierern",
                status="Fachkraefte",
            ),
            Noun("f", "Tätowiererin", nom_pl="Tätowiererinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Maskenbildner",
                "Maskenbildners",
                nom_pl="Maskenbildner",
                dat_pl="Maskenbildnern",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Maskenbildnerin",
                nom_pl="Maskenbildnerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    824: [
        [
            Noun(
                "m",
                "Bestatter",
                "Bestatters",
                nom_pl="Bestatter",
                dat_pl="Bestattern",
                status="Fachkraefte",
            ),
            Noun("f", "Bestatterin", nom_pl="Bestatterinnen", status="Fachkraefte"),
        ],
    ],
    825: [
        [
            Noun(
                "m",
                "Optiker",
                "Optikers",
                nom_pl="Optiker",
                dat_pl="Optikern",
                status="Fachkraefte",
            ),
            Noun("f", "Optikerin", nom_pl="Optikerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Hörakustiker",
                "Hörakustikers",
                nom_pl="Hörakustiker",
                status="Fachkraefte",
            ),
            Noun("f", "Hörakustikerin", nom_pl="Hörakustikerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Medizintechniker",
                "Medizintechnikers",
                nom_pl="Medizintechniker",
                dat_pl="Medizintechnikern",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Medizintechnikerin",
                nom_pl="Medizintechnikerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    831: [
        [
            Noun(
                "m",
                "Jugendberater",
                "Jugendberaters",
                nom_pl="Jugendberater",
                dat_pl="Jugendberatern",
                status="Experten",
            ),
            Noun("f", "Jugendberaterin", nom_pl="Jugendberaterinnen", status="Experten"),
            Noun(
                "f",
                "Jugendberatung",
                nom_pl="Jugendberatungen",
                status="Experten",
                pronouns="dey",
            ),
        ],
        [
            Noun(
                "m",
                "Sozialarbeiter",
                "Sozialarbeiters",
                nom_pl="Sozialarbeiter",
                dat_pl="Sozialarbeitern",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Sozialarbeiterin",
                nom_pl="Sozialarbeiterinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "f",
                "Integrationsfachkraft",
                nom_pl="Integrationsfachkräfte",
                status="Fachkraefte",
                pronouns="er",
            ),
            Noun(
                "f",
                "Integrationsfachkraft",
                nom_pl="Integrationsfachkräfte",
                status="Fachkraefte",
                pronouns="sie",
            ),
            Noun(
                "f",
                "Integrationsfachkraft",
                nom_pl="Integrationsfachkräfte",
                status="Fachkraefte",
                pronouns="dey",
            ),
        ],
        [
            Noun(
                "m",
                "Betreuer",
                "Betreuers",
                nom_pl="Betreuer",
                dat_pl="Betreuern",
                status="Helfer",
            ),
            Noun("f", "Betreuerin", nom_pl="Betreuerinnen", status="Helfer"),
        ],
        [
            Noun(
                "m",
                "Erzieher",
                "Erziehers",
                nom_pl="Erzieher",
                dat_pl="Erziehern",
                status="Spezialisten",
            ),
            Noun("f", "Erzieherin", nom_pl="Erzieherinnen", status="Spezialisten"),
        ],
        [
            Noun(
                "m",
                "Kindergärtner",
                "Kindergärtners",
                nom_pl="Kindergärtner",
                dat_pl="Kindergärtnern",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Kindergärtnerin",
                nom_pl="Kindergärtnerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    832: [
        [
            Noun(
                "m",
                "Haushälter",
                "Haushälters",
                nom_pl="Haushälter",
                dat_pl="Haushältern",
                status="Fachkraefte",
            ),
            Noun("f", "Haushälterin", nom_pl="Haushälterinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Haushaltshelfer",
                "Haushaltshelfers",
                nom_pl="Haushaltshelfer",
                status="Helfer",
            ),
            Noun("f", "Haushaltshelferin", nom_pl="Haushaltshelferinnen", status="Helfer"),
        ],
        [
            Noun("f", "Haushaltshilfe", nom_pl="Haushaltshilfen", pronouns="dey", status="Helfer"),
        ],
    ],
    833: [
        [
            Noun(
                "m",
                "Pfarrer",
                "Pfarrers",
                nom_pl="Pfarrer",
                dat_pl="Pfarrern",
                status="Experten",
            ),
            Noun("f", "Pfarrerin", nom_pl="Pfarrerinnen", status="Experten"),
        ],
    ],
    841: [
        [
            Noun(
                "m",
                "Lehrer",
                "Lehrers",
                nom_pl="Lehrer",
                dat_pl="Lehrern",
                status="Experten",
            ),
            Noun("f", "Lehrerin", nom_pl="Lehrerinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Grundschullehrer",
                "Grundschullehrers",
                nom_pl="Grundschullehrer",
                dat_pl="Grundschullehrern",
                status="Experten",
            ),
            Noun("f", "Grundschullehrerin", nom_pl="Grundschullehrerinnen", status="Experten"),
        ],
    ],
    842: [
        [
            Noun(
                "m",
                "Werklehrer",
                "Werklehrers",
                nom_pl="Werklehrer",
                status="Spezialisten",
            ),
            Noun("f", "Werklehrerin", nom_pl="Werklehrerinnen", status="Spezialisten"),
        ],
        [
            Noun(
                "m",
                "Berufsschullehrer",
                "Berufsschullehrers",
                nom_pl="Berufsschullehrer",
                dat_pl="Berufsschullehrern",
                status="Experten",
            ),
            Noun(
                "f",
                "Berufsschullehrerin",
                nom_pl="Berufsschullehrerinnen",
                status="Experten",
            ),
        ],
    ],
    843: [
        [
            Noun(
                "m",
                "Dozent",
                "Dozenten",
                "Dozenten",
                "Dozenten",
                nom_pl="Dozenten",
                status="Experten",
            ),
            Noun("f", "Dozentin", nom_pl="Dozentinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Professor",
                "Professors",
                nom_pl="Professoren",
                dat_pl="Professoren",
                acc_pl="Professoren",
                status="Experten",
            ),
            Noun("f", "Professorin", nom_pl="Professorinnen", status="Experten"),
        ],
    ],
    844: [
        [
            Noun(
                "m",
                "Gitarrenlehrer",
                "Gitarrenlehrers",
                nom_pl="Gitarrenlehrer",
                dat_pl="Gitarrenlehrern",
                status="Experten",
            ),
            Noun("f", "Gitarrenlehrerin", nom_pl="Gitarrenlehrerinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Gesangslehrer",
                "Gesangslehrers",
                status="Experten",
            ),
            Noun("f", "Gesangslehrerin", nom_pl="Gesangslehrerinnen", status="Experten"),
        ],
    ],
    845: [
        [
            Noun(
                "m",
                "Fahrlehrer",
                "Fahrlehrers",
                nom_pl="Fahrlehrer",
                dat_pl="Fahrlehrern",
                status="Spezialisten",
            ),
            Noun("f", "Fahrlehrerin", nom_pl="Fahrlehrerinnen", status="Spezialisten"),
        ],
        [
            Noun(
                "m",
                "Trainer",
                "Trainers",
                nom_pl="Trainer",
                dat_pl="Trainern",
                status="Spezialisten",
            ),
            Noun("f", "Trainerin", nom_pl="Trainerinnen", status="Spezialisten"),
        ],
    ],
    911: [
        [
            Noun(
                "m",
                "Linguist",
                "Linguisten",
                "Linguisten",
                "Linguisten",
                nom_pl="Linguisten",
                status="Experten",
            ),
            Noun("f", "Linguistin", nom_pl="Linguistinnen", status="Experten"),
        ],
    ],
    912: [
        [
            Noun("m", "Historiker", "Historikers", nom_pl="Historiker", status="Experten"),
            Noun("f", "Historikerin", nom_pl="Historikerinnen", status="Experten"),
        ],
    ],
    913: [
        [
            Noun(
                "m",
                "Marktforscher",
                "Marktforschers",
                nom_pl="Marktforscher",
                status="Experten",
            ),
            Noun("f", "Marktforscherin", nom_pl="Marktforscherinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Soziologe",
                "Soziologen",
                "Soziologen",
                "Soziologen",
                nom_pl="Soziologen",
                status="Experten",
            ),
            Noun("f", "Soziologin", nom_pl="Soziologinnen", status="Experten"),
        ],
    ],
    914: [
        [
            Noun(
                "m",
                "Ökonom",
                "Ökonomen",
                "Ökonomen",
                "Ökonomen",
                nom_pl="Ökonomen",
                status="Experten",
            ),
            Noun("f", "Ökonomin", nom_pl="Ökonominnen", status="Experten"),
        ],
    ],
    921: [
        [
            Noun(
                "m",
                "Callcenteragent",
                "Callcenteragenten",
                nom_pl="Callcenteragenten",
                status="Fachkraefte",
            ),
            Noun("f", "Callcenteragentin", nom_pl="Callcenteragentinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Werbetexter",
                "Werbetexters",
                nom_pl="Werbetexter",
                status="Spezialisten",
            ),
            Noun("f", "Werbetexterin", nom_pl="Werbetexterinnen", status="Spezialisten"),
        ],
    ],
    922: [
        [
            Noun(
                "m",
                "Pressesprecher",
                "Pressesprechers",
                nom_pl="Pressesprecher",
                status="Experten",
            ),
            Noun("f", "Pressesprecherin", nom_pl="Pressesprecherinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Lobbyist",
                "Lobbyisten",
                "Lobbyisten",
                "Lobbyisten",
                nom_pl="Lobbyisten",
                status="Spezialisten",
            ),
            Noun("f", "Lobbyistin", nom_pl="Lobbyistinnen", status="Spezialisten"),
        ],
    ],
    923: [
        [
            Noun(
                "m",
                "Literaturagent",
                "Literaturagenten",
                "Literaturagenten",
                "Literaturagenten",
                nom_pl="Literaturagenten",
                status="Experten",
            ),
            Noun("f", "Literaturagentin", nom_pl="Literaturagentinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Anzeigenagent",
                "Anzeigenagents",
                nom_pl="Anzeigenagenten",
                status="Fachkraefte",
            ),
            Noun("f", "Anzeigenagentin", nom_pl="Anzeigenagentinnen", status="Fachkraefte"),
        ],
    ],
    924: [
        [
            Noun("m", "Reporter", "Reporters", nom_pl="Reporter", status="Experten"),
            Noun("f", "Reporterin", nom_pl="Reporterinnen", status="Experten"),
        ],
        [
            Noun("m", "Dichter", "Dichters", nom_pl="Dichter", status="Experten"),
            Noun("f", "Dichterin", nom_pl="Dichterinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Journalist",
                "Journalisten",
                "Journalisten",
                "Journalisten",
                nom_pl="Journalisten",
                status="Experten",
            ),
            Noun("f", "Journalistin", nom_pl="Journalistinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Redaktionsassistent",
                "Redaktionsassistenten",
                "Redaktionsassistenten",
                "Redaktionsassistenten",
                nom_pl="Redaktionsassistenten",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Redaktionsassistentin",
                nom_pl="Redaktionsassistentinnen",
                status="Fachkraefte",
            ),
            Noun("f", "Redaktionsassistenz", status="Experten", pronouns="dey"),
        ],
        [
            Noun(
                "m",
                "Redakteur",
                "Redakteurs",
                nom_pl="Redakteure",
                status="Spezialisten",
            ),
            Noun("f", "Redakteurin", nom_pl="Redakteurinnen", status="Spezialisten"),
        ],
    ],
    931: [
        [
            Noun(
                "m",
                "Möbeldesigner",
                "Möbeldesigners",
                dat_sg="Möbeldesigner",
                acc_sg="Möbeldesigner",
                nom_pl="Möbeldesigner",
                acc_pl="Möbeldesigner",
                status="Experten",
            ),
            Noun(
                "f",
                "Möbeldesignerin",
                nom_pl="Möbeldesignerinnen",
                acc_pl="Möbeldesignerinnen",
                status="Experten",
            ),
        ],
    ],
    932: [
        [
            Noun(
                "m",
                "Innenarchitekt",
                "Innenarchitekten",
                "Innenarchitekten",
                "Innenarchitekten",
                nom_pl="Innenarchitekten",
                acc_pl="Innenarchitekten",
                status="Experten",
            ),
            Noun(
                "f",
                "Innenarchitektin",
                nom_pl="Innenarchitektinnen",
                acc_pl="Innenarchitektinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m",
                "Innenausstatter",
                "Innenausstatters",
                dat_sg="Innenausstatter",
                acc_sg="Innenausstatter",
                nom_pl="Innenausstatter",
                acc_pl="Innenausstatter",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Innenausstatterin",
                nom_pl="Innenausstatterinnen",
                acc_pl="Innenausstatterinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    933: [
        [
            Noun(
                "m",
                "Restaurator",
                "Restaurators",
                dat_sg="Restaurator",
                acc_sg="Restaurator",
                nom_pl="Restauratoren",
                acc_pl="Restauratoren",
                status="Experten",
            ),
            Noun(
                "f",
                "Restauratorin",
                nom_pl="Restauratorinnen",
                acc_pl="Restauratorinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m",
                "Bildhauer",
                "Bildhauers",
                dat_sg="Bildhauer",
                acc_sg="Bildhauer",
                nom_pl="Bildhauer",
                acc_pl="Bildhauer",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Bildhauerin",
                nom_pl="Bildhauerinnen",
                acc_pl="Bildhauerinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    934: [
        [
            Noun(
                "m",
                "Töpfer",
                "Töpfers",
                dat_sg="Töpfer",
                acc_sg="Töpfer",
                nom_pl="Töpfer",
                acc_pl="Töpfer",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Töpferin",
                nom_pl="Töpferinnen",
                acc_pl="Töpferinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    935: [
        [
            Noun(
                "m",
                "Goldschmied",
                "Goldschmieds",
                nom_pl="Goldschmiede",
                status="Fachkraefte",
            ),
            Noun("f", "Goldschmiedin", nom_pl="Goldschmiedinnen", status="Fachkraefte"),
        ],
    ],
    936: [
        [
            Noun(
                "m",
                "Geigenbauer",
                "Geigenbauers",
                nom_pl="Geigenbauer",
                status="Fachkraefte",
            ),
            Noun("f", "Geigenbauerin", nom_pl="Geigenbauerinnen", status="Fachkraefte"),
        ],
    ],
    941: [
        [
            Noun("m", "Sänger", "Sängers", nom_pl="Sänger", status="Experten"),
            Noun("f", "Sängerin", nom_pl="Sängerinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Klaviespieler",
                "Klaviespielers",
                nom_pl="Klaviespieler",
                status="Experten",
            ),
            Noun("f", "Klaviespielerin", nom_pl="Klaviespielerinnen", status="Experten"),
        ],
    ],
    942: [
        [
            Noun(
                "m",
                "Schauspieler",
                "Schauspielers",
                nom_pl="Schauspieler",
                status="Experten",
            ),
            Noun("f", "Schauspielerin", nom_pl="Schauspielerinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Prostituierter",
                "Prostituierten",
                "Prostituierten",
                "Prostituierten",
                nom_pl="Prostituierten",
                status="Fachkraefte",
            ),
            Noun("f", "Prostituierte", nom_pl="Prostituierten", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Fußballer",
                "Fußballers",
                nom_pl="Fußballer",
                status="Spezialisten",
            ),
            Noun("f", "Fußballerin", nom_pl="Fußballerinnen", status="Spezialisten"),
        ],
        [
            Noun(
                "n",
                "Model",
                "Models",
                nom_pl="Models",
                status="Fachkraefte",
                pronouns="er",
            ),
            Noun(
                "n",
                "Model",
                "Models",
                nom_pl="Models",
                status="Fachkraefte",
                pronouns="sie",
            ),
            Noun(
                "n",
                "Model",
                "Models",
                nom_pl="Models",
                status="Fachkraefte",
                pronouns="dey",
            ),
        ],
    ],
    943: [
        [
            Noun("m", "Hellseher", "Hellsehers", nom_pl="Hellseher", status="Fachkraefte"),
            Noun("f", "Hellseherin", nom_pl="Hellseherinnen", status="Fachkraefte"),
        ],
        [
            Noun("m", "Wahrsager", "Wahrsagers", nom_pl="Wahrsager", status="Fachkraefte"),
            Noun("f", "Wahrsagerin", nom_pl="Wahrsagerinnen", status="Fachkraefte"),
        ],
    ],
    944: [
        [
            Noun("m", "Souffleur", "Souffleurs", nom_pl="Souffleure", status="Fachkraefte"),
            Noun("f", "Souffleuse", nom_pl="Souffleusen", status="Fachkraefte"),
        ],
        [
            Noun("m", "Filmregisseur", status="Experten"),
            Noun("f", "Filmregisseurin", status="Experten"),
            Noun("f", "Filmregie", status="Experten", pronouns="dey"),
        ],
        [
            Noun(
                "m",
                "Produzent",
                "Produzenten",
                "Produzenten",
                "Produzenten",
                nom_pl="Produzenten",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Produzentin",
                nom_pl="Produzentinnen",
                status="Spezialisten",
            ),
        ],
    ],
    945: [
        [
            Noun(
                "m",
                "Pyrotechniker",
                "Pyrotechnikers",
                nom_pl="Pyrotechniker",
                status="Fachkraefte",
            ),
            Noun("f", "Pyrotechnikerin", nom_pl="Pyrotechnikerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Kameramann",
                "Kameramanns",
                nom_pl="Kameramänner",
                status="Spezialisten",
            ),
            Noun("f", "Kamerafrau", nom_pl="Kamerafrauen", status="Spezialisten"),
        ],
    ],
    946: [
        [
            Noun(
                "m",
                "Bühnenbildner",
                "Bühnenbildners",
                nom_pl="Bühnenbildner",
                status="Experten",
            ),
            Noun("f", "Bühnenbildnerin", nom_pl="Bühnenbildnerinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Requisiteur",
                "Requisiteurs",
                nom_pl="Requisiteure",
                status="Spezialisten",
            ),
            Noun("f", "Requisiteurin", nom_pl="Requisiteurinnen", status="Spezialisten"),
        ],
    ],
    947: [
        [
            Noun("m", "Kurator", "Kurators", nom_pl="Kuratoren", status="Experten"),
            Noun("f", "Kuratorin", nom_pl="Kuratorinnen", status="Experten"),
        ],
    ],
}
