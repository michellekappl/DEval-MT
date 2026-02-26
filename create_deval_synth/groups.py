from declensions import Noun

# not finished
groups = {
    # "generic": [
    #     Noun("MASCULINE", "Mann", "Mannes", nom_pl="Männer", dat_pl="Männern"),
    #     Noun("FEMININE", "Frau", nom_pl="Frauen"),
    #     Noun("NEUTRAL", "Person", nom_pl="Personen", pronouns="dey"),
    # ],
    "romantic": [
        [
            Noun(
                "MASCULINE",
                "Partner",
                "Partners",
                nom_pl="Partner",
                dat_pl="Partnern",
            ),
            Noun("FEMININE", "Partnerin", nom_pl="Partnerinnen"),
        ],
        [
            Noun(
                "MASCULINE",
                "Freund",
                "Freundes",
                nom_pl="Freunde",
                dat_pl="Freunden",
            ),
            Noun("FEMININE", "Freundin", nom_pl="Freundinnen"),
        ],
        [
            Noun(
                "MASCULINE",
                "Ehemann",
                "Ehemannes",
                nom_pl="Ehemänner",
                dat_pl="Ehemännern",
            ),
            Noun("FEMININE", "Ehefrau", nom_pl="Ehefrauen"),
        ],
        [
            Noun(
                "MASCULINE",
                "Liebhaber",
                "Liebhabers",
                nom_pl="Liebhaber",
                dat_pl="Liebhabern",
            ),
            Noun("FEMININE", "Liebhaberin", nom_pl="Liebhaberinnen"),
        ],
        [
            Noun("NEUTRAL", "Date", "Dates", nom_pl="Dates", dat_pl="Dates"),
        ],
    ],
    # "other": [
    #     Noun("MASCULINE", "Juror"),
    #     Noun("FEMININE", "Jurorin"),
    #     Noun("NEUTRAL", "Jurymitglied", neopronouns=True),
    #     Noun("NEUTRAL", "Multitalent", neopronouns=True),
    #     Noun("MASCULINE", "Gesprächspartner"),
    #     Noun("FEMININE", "Gesprächspartnerin"),
    #     Noun("NEUTRAL", "Gesprächsperson"),
    #     Noun("MASCULINE", "Bruder"),
    #     Noun("FEMININE", "Schwester"),
    #     Noun("NEUTRAL", "Geschwisterkind", neopronouns=True),
    #     Noun("MASCULINE", "Enkel"),
    #     Noun("FEMININE", "Enkelin"),
    #     Noun("NEUTRAL", "Enkelkind", neopronouns=True),
    #     Noun("MASCULINE", "Doppelgänger"),
    #     Noun("FEMININE", "Doppelgängerin"),
    #     Noun("NEUTRAL", "Double", neopronouns=True),
    #     Noun("MASCULINE", "Schüler"),
    #     Noun("FEMININE", "Schülerin"),
    #     Noun("NEUTRAL", "Schulkind", neopronouns=True),
    #     Noun("MASCULINE", "Held"),
    #     Noun("FEMININE", "Heldin"),
    #     Noun("NEUTRAL", "Vorbild", neopronouns=True),
    #     Noun("NEUTRAL", "Ombudsperson", neopronouns=True),
    #     Noun("MASCULINE", "Praktikant", status="Helfer"),
    #     Noun("FEMININE", "Praktikantin", status="Helfer"),
    #     Noun(
    #         "FEMININE", "Praktikumskraft", status="Helfer", neopronouns=True
    #     ),  # im Österreichischen anscheinend gebräuchlich
    # ],
    111: [
        [
            Noun(
                "MASCULINE",
                "Bauer",
                "Bauern",
                "Bauern",
                "Bauern",
                nom_pl="Bauern",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Bäuerin", nom_pl="Bäuerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Erntehelfer",
                "Erntehelfers",
                nom_pl="Erntehelfer",
                dat_pl="Erntehelfern",
                status="Helfer",
            ),
            Noun("FEMININE", "Erntehelferin", nom_pl="Erntehelferinnen", status="Helfer"),
            Noun("FEMININE", "Erntehilfe", nom_pl="Erntehilfen", status="Helfer", pronouns="dey"),
        ],
    ],
    112: [
        [
            Noun(
                "MASCULINE",
                "Imker",
                "Imkers",
                nom_pl="Imker",
                dat_pl="Imkern",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Imkerin", nom_pl="Imkerinnen", status="Fachkraefte"),
        ],
    ],
    113: [
        [
            Noun(
                "MASCULINE",
                "Kutscher",
                "Kutschers",
                nom_pl="Kutscher",
                dat_pl="Kutschern",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Kutscherin", nom_pl="Kutscherinnen", status="Fachkraefte"),
        ],
    ],
    114: [
        [
            Noun(
                "MASCULINE",
                "Fischer",
                "Fischers",
                nom_pl="Fischer",
                dat_pl="Fischern",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Fischerin", nom_pl="Fischerinnen", status="Fachkraefte"),
        ],
    ],
    115: [
        [
            Noun(
                "MASCULINE",
                "Tierpfleger",
                "Tierpflegers",
                nom_pl="Tierpfleger",
                dat_pl="Tierpflegern",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Tierpflegerin", nom_pl="Tierpflegerinnen", status="Fachkraefte"),
        ],
    ],
    116: [
        [
            Noun(
                "MASCULINE",
                "Winzer",
                "Winzers",
                nom_pl="Winzer",
                dat_pl="Winzern",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Winzerin", nom_pl="Winzerinnen", status="Fachkraefte"),
        ],
    ],
    117: [
        [
            Noun(
                "MASCULINE",
                "Jäger",
                "Jägers",
                nom_pl="Jäger",
                dat_pl="Jägern",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Jägerin", nom_pl="Jägerinnen", status="Fachkraefte"),
        ],
    ],
    121: [
        [
            Noun(
                "MASCULINE",
                "Landschaftsgärtner",
                "Landschaftsgärtners",
                nom_pl="Landschaftsgärtner",
                dat_pl="Landschaftsgärtnern",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE", "Landschaftsgärtnerin", nom_pl="Landschaftsgärtnerinnen", status="Fachkraefte"
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Gartenarbeiter",
                "Gartenarbeiters",
                nom_pl="Gartenarbeiter",
                dat_pl="Gartenarbeitern",
                status="Helfer",
            ),
            Noun("FEMININE", "Gartenarbeiterin", nom_pl="Gartenarbeiterinnen", status="Helfer"),
        ],
    ],
    122: [
        [
            Noun(
                "MASCULINE",
                "Florist",
                "Floristen",
                "Floristen",
                "Floristen",
                nom_pl="Floristen",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Floristin", nom_pl="Floristinnen", status="Fachkraefte"),
        ],
    ],
    211: [
        [
            Noun(
                "MASCULINE",
                "Bergarbeiter",
                "Bergarbeiters",
                nom_pl="Bergarbeiter",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Bergarbeiterin", nom_pl="Bergarbeiterinnen", status="Fachkraefte"),
        ]
    ],
    212: [
        [
            Noun(
                "MASCULINE",
                "Steinmetz",
                "Steinmetzes",
                nom_pl="Steinmetze",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Steinmetzin", nom_pl="Steinmetzinnen", status="Fachkraefte"),
        ],
    ],
    213: [
        [
            Noun(
                "MASCULINE",
                "Glasbläser",
                "Glasbläsers",
                nom_pl="Glasbläser",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Glasbläserin",
                nom_pl="Glasbläserinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    214: [
        [
            Noun(
                "MASCULINE",
                "Keramikarbeiter",
                "Keramikarbeiters",
                nom_pl="Keramikarbeiter",
                status="Helfer",
            ),
            Noun("FEMININE", "Keramikarbeiterin", nom_pl="Keramikarbeiterinnen", status="Helfer"),
        ],
    ],
    221: [
        [
            Noun(
                "MASCULINE",
                "Gummiarbeiter",
                "Gummiarbeiters",
                nom_pl="Gummiarbeiter",
                status="Helfer",
            ),
            Noun("FEMININE", "Gummiarbeiterin", nom_pl="Gummiarbeiterinnen", status="Helfer"),
        ],
        [
            Noun(
                "MASCULINE",
                "Reifenbauer",
                "Reifenbauers",
                nom_pl="Reifenbauer",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Reifenbauerin", nom_pl="Reifenbauerinnen", status="Fachkraefte"),
        ],
    ],
    222: [
        [
            Noun(
                "MASCULINE",
                "Autolackierer",
                "Autolackierers",
                nom_pl="Autolackierer",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Autolackiererin", nom_pl="Autolackiererinnen", status="Fachkraefte"),
        ],
    ],
    223: [
        [
            Noun("MASCULINE", "Schreiner", "Schreiners", nom_pl="Schreiner", status="Fachkraefte"),
            Noun("FEMININE", "Schreinerin", nom_pl="Schreinerinnen", status="Fachkraefte"),
        ],
        [
            Noun("MASCULINE", "Tischler", "Tischlers", nom_pl="Tischler", status="Fachkraefte"),
            Noun("FEMININE", "Tischlerin", nom_pl="Tischlerinnen", status="Fachkraefte"),
        ],
    ],
    231: [
        [
            Noun(
                "MASCULINE",
                "Papierfärber",
                "Papierfärbers",
                nom_pl="Papierfärber",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Papierfärberin", nom_pl="Papierfärberinnen", status="Fachkraefte"),
        ],
    ],
    232: [
        [
            Noun(
                "MASCULINE",
                "Werbegrafiker",
                "Werbegrafikers",
                nom_pl="Werbegrafiker",
                status="Spezialisten",
            ),
            Noun("FEMININE", "Werbegrafikerin", nom_pl="Werbegrafikerinnen", status="Spezialisten"),
        ],
    ],
    233: [
        [
            Noun(
                "MASCULINE",
                "Fotograf",
                "Fotografen",
                "Fotografen",
                "Fotografen",
                nom_pl="Fotografen",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Fotografin", nom_pl="Fotografinnen", status="Fachkraefte"),
        ],
    ],
    234: [
        [
            Noun(
                "MASCULINE",
                "Buchdrucker",
                "Buchdruckers",
                nom_pl="Buchdrucker",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Buchdruckerin", nom_pl="Buchdruckerinnen", status="Fachkraefte"),
        ],
    ],
    241: [
        [
            Noun(
                "MASCULINE",
                "Stahlarbeiter",
                "Stahlarbeiters",
                nom_pl="Stahlarbeiter",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Stahlarbeiterin", nom_pl="Stahlarbeiterinnen", status="Fachkraefte"),
        ],
    ],
    242: [
        [
            Noun(
                "MASCULINE",
                "Münzpräger",
                "Münzprägers",
                nom_pl="Münzpräger",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Münzprägerin", nom_pl="Münzprägerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Schleifer",
                "Schleifers",
                nom_pl="Schleifer",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Schleiferin", nom_pl="Schleiferinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Metallarbeiter",
                "Metallarbeiters",
                nom_pl="Metallarbeiter",
                status="Helfer",
            ),
            Noun("FEMININE", "Metallarbeiterin", nom_pl="Metallarbeiterinnen", status="Helfer"),
        ],
    ],
    243: [
        [
            Noun(
                "MASCULINE",
                "Metallfärber",
                "Metallfärbers",
                nom_pl="Metallfärber",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Metallfärberin", nom_pl="Metallfärberinnen", status="Fachkraefte"),
        ],
    ],
    244: [
        [
            Noun("MASCULINE", "Schlosser", "Schlossers", nom_pl="Schlosser", status="Fachkraefte"),
            Noun("FEMININE", "Schlosserin", nom_pl="Schlosserinnen", status="Fachkraefte"),
        ],
        [
            Noun("MASCULINE", "Schmied", "Schmiedes", nom_pl="Schmiede", status="Fachkraefte"),
            Noun("FEMININE", "Schmiedin", nom_pl="Schmiedinnen", status="Fachkraefte"),
        ],
    ],
    245: [
        [
            Noun(
                "MASCULINE",
                "Uhrmacher",
                "Uhrmachers",
                nom_pl="Uhrmacher",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Uhrmacherin", nom_pl="Uhrmacherinnen", status="Fachkraefte"),
        ],
    ],
    251: [
        [
            Noun(
                "MASCULINE",
                "Maschinenbauer",
                "Maschinenbauers",
                nom_pl="Maschinenbauer",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Maschinenbauerin", nom_pl="Maschinenbauerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Mechaniker",
                "Mechanikers",
                nom_pl="Mechaniker",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Mechanikerin", nom_pl="Mechanikerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Stromableser",
                "Stromablesers",
                nom_pl="Stromableser",
                status="Helfer",
            ),
            Noun("FEMININE", "Stromableserin", nom_pl="Stromableserinnen", status="Helfer"),
        ],
    ],
    252: [
        [
            Noun(
                "MASCULINE",
                "Automechaniker",
                "Automechanikers",
                nom_pl="Automechaniker",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Automechanikerin",
                nom_pl="Automechanikerinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Schiffbauer",
                "Schiffbauers",
                nom_pl="Schiffbauer",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Schiffbauerin", nom_pl="Schiffbauerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Flugingenieur",
                "Flugingenieurs",
                nom_pl="Flugingenieure",
                status="Experten",
            ),
            Noun(
                "FEMININE",
                "Flugingenieurin",
                nom_pl="Flugingenieurinnen",
                status="Experten",
            ),
        ],
    ],
    261: [
        [
            Noun(
                "MASCULINE",
                "Mechatroniker",
                "Mechatronikers",
                nom_pl="Mechatroniker",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Mechatronikerin", nom_pl="Mechatronikerinnen", status="Fachkraefte"),
        ],
    ],
    262: [
        [
            Noun(
                "MASCULINE",
                "Elektriker",
                "Elektrikers",
                nom_pl="Elektriker",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Elektrikerin",
                nom_pl="Elektrikerinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Lichtinstallateur",
                "Lichtinstallateurs",
                nom_pl="Lichtinstallateure",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Lichtinstallateurin", nom_pl="Lichtinstallateurinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Solartechniker",
                "Solartechnikers",
                nom_pl="Solartechniker",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Solartechnikerin",
                nom_pl="Solartechnikerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    263: [
        [
            Noun(
                "MASCULINE",
                "PC-Techniker",
                "PC-Technikers",
                nom_pl="PC-Techniker",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "PC-Technikerin", nom_pl="PC-Technikerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Elektrotechniker",
                "Elektrotechnikers",
                nom_pl="Elektrotechniker",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Elektrotechnikerin",
                nom_pl="Elektrotechnikerinnen",
                status="Spezialisten",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Batteriehersteller",
                "Batterieherstellers",
                nom_pl="Batteriehersteller",
                status="Helfer",
            ),
            Noun(
                "FEMININE",
                "Batterieherstellerin",
                nom_pl="Batterieherstellerinnen",
                status="Helfer",
            ),
        ],
    ],
    271: [
        [
            Noun(
                "MASCULINE",
                "Produktentwickler",
                "Produktentwicklers",
                nom_pl="Produktentwickler",
                status="Experten",
            ),
            Noun(
                "FEMININE",
                "Produktentwicklerin",
                nom_pl="Produktentwicklerinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Patentprüfer",
                "Patentprüfers",
                nom_pl="Patentprüfer",
                status="Experten",
            ),
            Noun("FEMININE", "Patentprüferin", nom_pl="Patentprüferinnen", status="Experten"),
        ],
    ],
    272: [
        [
            Noun(
                "MASCULINE",
                "Bauzeichner",
                "Bauzeichners",
                nom_pl="Bauzeichner",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Bauzeichnerin", nom_pl="Bauzeichnerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Anlagenplaner",
                "Anlagenplaners",
                nom_pl="Anlagenplaner",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Anlagenplanerin",
                nom_pl="Anlagenplanerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    273: [
        [
            Noun(
                "MASCULINE",
                "Wirtschaftsingenieur",
                "Wirtschaftsingenieurs",
                nom_pl="Wirtschaftsingenieure",
                status="Experten",
            ),
            Noun(
                "FEMININE",
                "Wirtschaftsingenieurin",
                nom_pl="Wirtschaftsingenieurinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Qualitätsprüfer",
                "Qualitätsprüfers",
                nom_pl="Qualitätsprüfer",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Qualitätsprüferin", nom_pl="Qualitätsprüferinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Geräteprüfer",
                "Geräteprüfers",
                nom_pl="Geräteprüfer",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Geräteprüferin",
                nom_pl="Geräteprüferinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Materialplaner",
                "Materialplaners",
                nom_pl="Materialplaner",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Materialplanerin",
                nom_pl="Materialplanerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    281: [
        [
            Noun(
                "MASCULINE",
                "Stricker",
                "Strickers",
                nom_pl="Stricker",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Strickerin",
                nom_pl="Strickerinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    282: [
        [
            Noun(
                "MASCULINE",
                "Schneider",
                "Schneiders",
                nom_pl="Schneider",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Schneiderin",
                nom_pl="Schneiderinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun("MASCULINE", "Hutmacher", "Hutmachers", nom_pl="Hutmacher", status="Fachkraefte"),
            Noun("FEMININE", "Hutmacherin", nom_pl="Hutmacherinnen", status="Fachkraefte"),
        ],
    ],
    283: [
        [
            Noun(
                "MASCULINE",
                "Schuhmacher",
                "Schuhmachers",
                nom_pl="Schuhmacher",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Schuhmacherin", nom_pl="Schuhmacherinnen", status="Fachkraefte"),
        ],
    ],
    291: [
        [
            Noun("MASCULINE", "Brauer", "Brauers", nom_pl="Brauer", status="Fachkraefte"),
            Noun("FEMININE", "Brauerin", nom_pl="Brauerinnen", status="Fachkraefte"),
        ],
    ],
    292: [
        [
            Noun(
                "MASCULINE",
                "Bäcker",
                "Bäckers",
                nom_pl="Bäcker",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Bäckerin", nom_pl="Bäckerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Konditor",
                "Konditors",
                nom_pl="Konditoren",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Konditorin", nom_pl="Konditorinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Molkereiarbeiter",
                "Molkereiarbeiters",
                nom_pl="Molkereiarbeiter",
                status="Helfer",
            ),
            Noun(
                "FEMININE",
                "Molkereiarbeiterin",
                nom_pl="Molkereiarbeiterinnen",
                status="Helfer",
            ),
        ],
    ],
    293: [
        [
            Noun("MASCULINE", "Koch", "Kochs", nom_pl="Köche", status="Fachkraefte"),
            Noun("FEMININE", "Köchin", nom_pl="Köchinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Küchenhelfer",
                "Küchenhelfers",
                status="Helfer",
            ),
            Noun(
                "FEMININE",
                "Küchenhelferin",
                nom_pl="Küchenhelferinnen",
                status="Helfer",
            ),
            Noun(
                "FEMININE",
                "Küchenhilfe",
                nom_pl="Küchenhilfen",
                pronouns="dey",
                status="Helfer",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Pizzabäcker",
                "Pizzabäckers",
                nom_pl="Pizzabäcker",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Pizzabäckerin", nom_pl="Pizzabäckerinnen", status="Fachkraefte"),
        ],
    ],
    311: [
        [
            Noun(
                "MASCULINE",
                "Architekt",
                "Architekten",
                nom_pl="Architekten",
                dat_pl="Architekten",
                status="Experten",
            ),
            Noun("FEMININE", "Architektin", nom_pl="Architektinnen", status="Experten"),
        ],
        [
            Noun("MASCULINE", "Raumplaner", "Raumplaners", nom_pl="Raumplaner", status="Experten"),
            Noun("FEMININE", "Raumplanerin", nom_pl="Raumplanerinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Baustellenprüfer",
                "Baustellenprüfers",
                nom_pl="Baustellenprüfer",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Baustellenprüferin",
                nom_pl="Baustellenprüferinnen",
                status="Spezialisten",
            ),
        ],
    ],
    312: [
        [
            Noun(
                "MASCULINE",
                "Kartograf",
                "Kartografen",
                "Kartografen",
                "Kartografen",
                "Kartografen",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Kartografin",
                nom_pl="Kartografinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    321: [
        [
            Noun(
                "MASCULINE",
                "Maurer",
                "Maurers",
                nom_pl="Maurer",
                dat_pl="Maurern",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Maurerin", nom_pl="Maurerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Dachdecker",
                "Dachdeckers",
                nom_pl="Dachdecker",
                dat_pl="Dachdeckern",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Dachdeckerin", nom_pl="Dachdeckerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Bauarbeiter",
                "Bauarbeiters",
                nom_pl="Bauarbeiter",
                dat_pl="Bauarbeitern",
                status="Helfer",
            ),
            Noun("FEMININE", "Bauarbeiterin", nom_pl="Bauarbeiterinnen", status="Helfer"),
        ],
    ],
    322: [
        [
            Noun(
                "MASCULINE",
                "Kanalbauer",
                "Kanalbauers",
                nom_pl="Kanalbauer",
                dat_pl="Kanalbauern",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Kanalbauerin", nom_pl="Kanalbauerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Teerer",
                "Teerers",
                status="Helfer",
            ),
            Noun("FEMININE", "Teererin", nom_pl="Teererinnen", status="Helfer"),
        ],
    ],
    331: [
        [
            Noun(
                "MASCULINE",
                "Fliesenleger",
                "Fliesenlegers",
                nom_pl="Fliesenleger",
                dat_pl="Fliesenlegern",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Fliesenlegerin", nom_pl="Fliesenlegerinnen", status="Fachkraefte"),
        ],
    ],
    332: [
        [
            Noun(
                "MASCULINE",
                "Maler",
                "Malers",
                nom_pl="Maler",
                dat_pl="Malern",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Malerin", nom_pl="Malerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Malerhelfer",
                "Malerhelfers",
                status="Helfer",
            ),
            Noun("FEMININE", "Malerhelferin", nom_pl="Malerhelferinnen", status="Helfer"),
            Noun("FEMININE", "Malerhilfe", status="Helfer", pronouns="dey"),
        ],
    ],
    333: [
        [
            Noun(
                "MASCULINE",
                "Autoglaser",
                "Autoglasers",
                nom_pl="Autoglaser",
                dat_pl="Autoglasern",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Autoglaserin", nom_pl="Autoglaserinnen", status="Fachkraefte"),
        ],
    ],
    341: [
        [
            Noun(
                "MASCULINE",
                "Hausmeister",
                "Hausmeisters",
                nom_pl="Hausmeister",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Hausmeisterin", nom_pl="Hausmeisterinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Platzwart",
                "Platzwarts",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Platzwartin",
                nom_pl="Platzwartinnen",
                status="Spezialisten",
            ),
        ],
    ],
    342: [
        [
            Noun("MASCULINE", "Klempner", "Klempners", nom_pl="Klempner", status="Fachkraefte"),
            Noun("FEMININE", "Klempnerin", nom_pl="Klempnerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Wärmetechniker",
                "Wärmetechnikers",
                nom_pl="Wärmetechniker",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Wärmetechnikerin",
                nom_pl="Wärmetechnikerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    343: [
        [
            Noun("MASCULINE", "Rohrbauer", "Rohrbauers", nom_pl="Rohrbauer", status="Fachkraefte"),
            Noun("FEMININE", "Rohrbauerin", nom_pl="Rohrbauerinnen", status="Fachkraefte"),
        ],
        [
            Noun("MASCULINE", "Müllmann", "Müllmanns", nom_pl="Müllmänner", status="Helfer"),
            Noun("FEMININE", "Müllfrau", nom_pl="Müllfrauen", status="Helfer"),
        ],
    ],
    411: [
        [
            Noun(
                "MASCULINE",
                "Mathematiker",
                "Mathematikers",
                nom_pl="Mathematiker",
                status="Experten",
            ),
            Noun("FEMININE", "Mathematikerin", nom_pl="Mathematikerinnen", status="Experten"),
        ],
    ],
    412: [
        [
            Noun(
                "MASCULINE",
                "Biologe",
                "Biologen",
                "Biologen",
                "Biologen",
                nom_pl="Biologen",
                status="Experten",
            ),
            Noun("FEMININE", "Biologin", nom_pl="Biologinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Biolaborant",
                "Biolaboranten",
                "Biolaboranten",
                "Biolaboranten",
                nom_pl="Biolaboranten",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Biolaborantin",
                nom_pl="Biolaborantinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    413: [
        [
            Noun("MASCULINE", "Chemiker", "Chemikers", nom_pl="Chemiker", status="Experten"),
            Noun("FEMININE", "Chemikerin", nom_pl="Chemikerinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Chemielaborant",
                "Chemielaboranten",
                "Chemielaboranten",
                "Chemielaboranten",
                nom_pl="Chemielaboranten",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Chemielaborantin",
                nom_pl="Chemielaborantinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    414: [
        [
            Noun("MASCULINE", "Physiker", "Physikers", nom_pl="Physiker", status="Experten"),
            Noun("FEMININE", "Physikerin", nom_pl="Physikerinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Materialprüfer",
                "Materialprüfers",
                nom_pl="Materialprüfer",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Materialprüferin",
                nom_pl="Materialprüferinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    421: [
        [
            Noun(
                "MASCULINE",
                "Meteorologe",
                "Meteorologen",
                "Meteorologen",
                "Meteorologen",
                nom_pl="Meteorologen",
                status="Experten",
            ),
            Noun("FEMININE", "Meteorologin", nom_pl="Meteorologinnen", status="Experten"),
        ],
    ],
    422: [
        [
            Noun(
                "MASCULINE",
                "Schornsteinfeger",
                "Schornsteinfegers",
                nom_pl="Schornsteinfeger",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Schornsteinfegerin",
                nom_pl="Schornsteinfegerinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    423: [
        [
            Noun(
                "MASCULINE",
                "Umweltbeauftragter",
                "Umweltbeauftragten",
                "Umweltbeauftragten",
                "Umweltbeauftragten",
                nom_pl="Umweltbeauftragte",
                acc_pl="Umweltbeauftragte",
                status="Experten",
            ),
            Noun(
                "FEMININE",
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
                "MASCULINE",
                "Informatiker",
                "Informatikers",
                nom_pl="Informatiker",
                status="Experten",
            ),
            Noun("FEMININE", "Informatikerin", nom_pl="Informatikerinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Webentwickler",
                "Webentwicklers",
                nom_pl="Webentwickler",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Webentwicklerin",
                nom_pl="Webentwicklerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    432: [
        [
            Noun(
                "MASCULINE",
                "Systemanalytiker",
                "Systemanalytikers",
                nom_pl="Systemanalytiker",
                status="Experten",
            ),
            Noun(
                "FEMININE",
                "Systemanalytikerin",
                nom_pl="Systemanalytikerinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "IT-Berater",
                "IT-Beraters",
                nom_pl="IT-Berater",
                status="Spezialisten",
            ),
            Noun("FEMININE", "IT-Beraterin", nom_pl="IT-Beraterinnen", status="Spezialisten"),
            Noun(
                "FEMININE",
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
                "MASCULINE",
                "Softwaretester",
                "Softwaretesters",
                nom_pl="Softwaretester",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Softwaretesterin",
                nom_pl="Softwaretesterinnen",
                status="Spezialisten",
            ),
        ],
    ],
    434: [
        [
            Noun(
                "MASCULINE",
                "Softwareentwickler",
                "Softwareentwicklers",
                nom_pl="Softwareentwickler",
                status="Experten",
            ),
            Noun(
                "FEMININE",
                "Softwareentwicklerin",
                nom_pl="Softwareentwicklerinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Systemprogrammierer",
                "Systemprogrammierers",
                nom_pl="Systemprogrammierer",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Systemprogrammiererin",
                nom_pl="Systemprogrammiererinnen",
                status="Spezialisten",
            ),
        ],
    ],
    511: [
        [
            Noun(
                "MASCULINE",
                "Matrose",
                "Matrosen",
                "Matrosen",
                "Matrosen",
                nom_pl="Matrosen",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Matrosin", nom_pl="Matrosinnen", status="Fachkraefte"),
        ],
    ],
    512: [
        [
            Noun(
                "MASCULINE",
                "Hafenaufseher",
                "Hafenaufsehers",
                nom_pl="Hafenaufseher",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Hafenaufseherin",
                nom_pl="Hafenaufseherinnen",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
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
                "MASCULINE",
                "Postbote",
                "Postboten",
                "Postboten",
                "Postboten",
                nom_pl="Postboten",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Postbotin", nom_pl="Postbotinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Möbelpacker",
                "Möbelpackers",
                nom_pl="Möbelpacker",
                status="Helfer",
            ),
            Noun("FEMININE", "Möbelpackerin", nom_pl="Möbelpackerinnen", status="Helfer"),
        ],
        [
            Noun(
                "MASCULINE",
                "Zeitungsausträger",
                "Zeitungsausträgers",
                nom_pl="Zeitungsausträger",
                status="Helfer",
            ),
            Noun("FEMININE", "Zeitungsausträgerin", nom_pl="Zeitungsausträgerinnen", status="Helfer"),
        ],
    ],
    514: [
        [
            Noun(
                "MASCULINE",
                "Zugbegleiter",
                "Zugbegleiters",
                nom_pl="Zugbegleiter",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Zugbegleiterin", nom_pl="Zugbegleiterinnen", status="Fachkraefte"),
            Noun(
                "FEMININE",
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
                "MASCULINE",
                "Fahrdienstleiter",
                "Fahrdienstleiters",
                nom_pl="Fahrdienstleiter",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Fahrdienstleiterin", nom_pl="Fahrdienstleiterin", status="Fachkraefte"),
            Noun(
                "FEMININE",
                "Fahrdienstleitung",
                nom_pl="Fahrdienstleitung",
                status="Fachkraefte",
                pronouns="dey",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Lotse",
                "Lotsen",
                "Lotsen",
                "Lotsen",
                nom_pl="Lotsen",
                status="Spezialisten",
            ),
            Noun("FEMININE", "Lotsin", nom_pl="Lotsinnen", status="Spezialisten"),
        ],
    ],
    516: [
        [
            Noun("MASCULINE", "Logistiker", "Logistikers", nom_pl="Logistiker", status="Experten"),
            Noun("FEMININE", "Logistikerin", nom_pl="Logistikerinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Postbeamte",
                "Postbeamten",
                nom_pl="Postbeamte",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Postbeamtin", nom_pl="Postbeamtinnen", status="Fachkraefte"),
        ],
    ],
    521: [
        [
            Noun("MASCULINE", "Busfahrer", "Busfahrers", nom_pl="Busfahrer", status="Fachkraefte"),
            Noun("FEMININE", "Busfahrerin", nom_pl="Busfahrerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Taxifahrer",
                "Taxifahrers",
                nom_pl="Taxifahrer",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Taxifahrerin", nom_pl="Taxifahrerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "LKW-Fahrer",
                "LKW-Fahrers",
                nom_pl="LKW-Fahrer",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "LKW-Fahrerin", nom_pl="LKW-Fahrerinnen", status="Fachkraefte"),
        ],
    ],
    522: [
        [
            Noun("MASCULINE", "Lokführer", "Lokführers", nom_pl="Lokführer", status="Fachkraefte"),
            Noun("FEMININE", "Lokführerin", nom_pl="Lokführerinnen", status="Fachkraefte"),
        ],
    ],
    523: [
        [
            Noun(
                "MASCULINE",
                "Pilot",
                "Piloten",
                "Piloten",
                "Piloten",
                nom_pl="Piloten",
                status="Experten",
            ),
            Noun("FEMININE", "Pilotin", nom_pl="Pilotinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Ballonfahrer",
                "Ballonfahrers",
                nom_pl="Ballonfahrer",
                status="Spezialisten",
            ),
            Noun("FEMININE", "Ballonfahrerin", nom_pl="Ballonfahrerinnen", status="Spezialisten"),
        ],
    ],
    524: [
        [
            Noun("MASCULINE", "Kapitän", "Kapitäns", nom_pl="Kapitäne", status="Experten"),
            Noun("FEMININE", "Kapitänin", nom_pl="Kapitäninnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Bootsführer",
                "Bootsführers",
                nom_pl="Bootsführer",
                status="Spezialisten",
            ),
            Noun("FEMININE", "Bootsführerin", nom_pl="Bootsführerinnen", status="Spezialisten"),
        ],
    ],
    525: [
        [
            Noun(
                "MASCULINE",
                "Kranführer",
                "Kranführers",
                nom_pl="Kranführer",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Kranführerin", nom_pl="Kranführerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Staplerfahrer",
                "Staplerfahrers",
                nom_pl="Staplerfahrer",
                status="Helfer",
            ),
            Noun(
                "FEMININE",
                "Staplerfahrerin",
                nom_pl="Staplerfahrerinnen",
                status="Helfer",
            ),
        ],
    ],
    531: [
        [
            Noun("MASCULINE", "Detektiv", "Detektivs", nom_pl="Detektive", status="Fachkraefte"),
            Noun("FEMININE", "Detektivin", nom_pl="Detektivinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Feuerwehrmann",
                "Feuerwehrmanns",
                nom_pl="Feuerwehrmänner",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Feuerwehrfrau", nom_pl="Feuerwehrfrauen", status="Fachkraefte"),
        ],
        [
            Noun("MASCULINE", "Bademeister", status="Fachkraefte"),
            Noun("FEMININE", "Bademeisterin", status="Fachkraefte"),
            Noun("FEMININE", "Badeaufsicht", status="Fachkraefte", pronouns="dey"),
        ],
        [
            Noun("MASCULINE", "Pförtner", "Pförtners", nom_pl="Pförtner", status="Helfer"),
            Noun("FEMININE", "Pförtnerin", nom_pl="Pförtnerinnen", status="Helfer"),
        ],
        [
            Noun("MASCULINE", "Türsteher", "Türstehers", nom_pl="Türsteher", status="Helfer"),
            Noun("FEMININE", "Türsteherin", nom_pl="Türsteherinnen", status="Helfer"),
        ],
    ],
    532: [
        [
            Noun(
                "MASCULINE",
                "Polizist",
                "Polizisten",
                nom_pl="Polizisten",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Polizistin",
                nom_pl="Polizistinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    533: [
        [
            Noun(
                "MASCULINE",
                "Kammerjäger",
                "Kammerjägers",
                nom_pl="Kammerjäger",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Kammerjägerin", nom_pl="Kammerjägerinnen", status="Fachkraefte"),
        ],
    ],
    541: [
        [
            Noun(
                "FEMININE",
                "Reinigungskraft",
                nom_pl="Reinigungskräfte",
                pronouns="er",
                status="Helfer",
            ),
            Noun(
                "FEMININE",
                "Reinigungskraft",
                nom_pl="Reinigungskräfte",
                pronouns="sie",
                status="Helfer",
            ),
            Noun(
                "FEMININE",
                "Reinigungskraft",
                nom_pl="Reinigungskräfte",
                pronouns="dey",
                status="Helfer",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Putzmann",
                "Putzmannes",
                nom_pl="Putzmänner",
                status="Helfer",
            ),
            Noun("FEMININE", "Putzfrau", nom_pl="Putzfrauen", status="Helfer"),
            Noun("FEMININE", "Putzhilfe", nom_pl="Putzhilfen", pronouns="dey", status="Helfer"),
        ],
    ],
    611: [
        [
            Noun("MASCULINE", "Videothekar", "Videothekars", nom_pl="Videothekare", status="Fachkraefte"),
            Noun("FEMININE", "Videothekarin", nom_pl="Videothekarinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Handelsvertreter",
                "Handelsvertreters",
                nom_pl="Handelsvertreter",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Handelsvertreterin",
                nom_pl="Handelsvertreterinnen",
                status="Spezialisten",
            ),
        ],
    ],
    612: [
        [
            Noun(
                "MASCULINE",
                "Großhändler",
                "Großhändlers",
                nom_pl="Großhändler",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Großhändlerin",
                nom_pl="Großhändlerinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    613: [
        [
            Noun(
                "MASCULINE",
                "Immobilienmakler",
                "Immobilienmaklers",
                nom_pl="Immobilienmakler",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Immobilienmaklerin",
                nom_pl="Immobilienmaklerinnen",
                status="Spezialisten",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Hausverwalter",
                "Hausverwalters",
                nom_pl="Hausverwalter",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Hausverwalterin",
                nom_pl="Hausverwalterinnen",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Hausverwaltung",
                nom_pl="Hausverwaltungen",
                status="Spezialisten",
                pronouns="dey",
            ),
        ],
    ],
    621: [
        [
            Noun("MASCULINE", "Verkäufer", "Verkäufers", nom_pl="Verkäufer", status="Fachkraefte"),
            Noun("FEMININE", "Verkäuferin", nom_pl="Verkäuferinnen", status="Fachkraefte"),
        ],
        [
            Noun("MASCULINE", "Kassierer", "Kassierers", nom_pl="Kassierer", status="Fachkraefte"),
            Noun("FEMININE", "Kassiererin", nom_pl="Kassiererinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Regalauffüller",
                "Regalauffüllers",
                nom_pl="Regalauffüller",
                status="Helfer",
            ),
            Noun("FEMININE", "Regalauffüllerin", nom_pl="Regalauffüllerinnen", status="Helfer"),
        ],
    ],
    622: [
        [
            Noun(
                "MASCULINE",
                "Juwelier",
                "Juweliers",
                nom_pl="Juwelier",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Juwelierin", nom_pl="Juwelierinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Autohändler",
                "Autohändlers",
                nom_pl="Autohändler",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Autohändlerin", nom_pl="Autohändlerinnen", status="Fachkraefte"),
        ],
    ],
    623: [
        [
            Noun(
                "MASCULINE",
                "Gemüsehändler",
                "Gemüsehändlers",
                nom_pl="Gemüsehändler",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Gemüsehändlerin", nom_pl="Gemüsehändlerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Fischverkäufer",
                "Fischverkäufers",
                nom_pl="Fischverkäufer",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Fischverkäuferin",
                nom_pl="Fischverkäuferinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Eisverkäufer",
                "Eisverkäufers",
                nom_pl="Eisverkäufer",
                status="Helfer",
            ),
            Noun("FEMININE", "Eisverkäuferin", nom_pl="Eisverkäuferinnen", status="Helfer"),
        ],
    ],
    624: [
        [
            Noun(
                "MASCULINE",
                "Drogerieverkäufer",
                "Drogerieverkäufers",
                nom_pl="Drogerieverkäufer",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Drogerieverkäuferin", nom_pl="Drogerieverkäuferinnen", status="Fachkraefte"),
        ],
    ],
    625: [
        [
            Noun(
                "MASCULINE",
                "Buchhändler",
                "Buchhändlers",
                nom_pl="Buchhändler",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Buchhändlerin", nom_pl="Buchhändlerinnen", status="Fachkraefte"),
        ],
    ],
    631: [
        [
            Noun(
                "MASCULINE",
                "Reiseleiter",
                "Reiseleiters",
                nom_pl="Reiseleiter",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Reiseleiterin", nom_pl="Reiseleiterinnen", status="Fachkraefte"),
            Noun("FEMININE", "Reiseleitung", status="Fachkraefte", pronouns="dey"),
        ],
    ],
    632: [
        [
            Noun(
                "MASCULINE",
                "Rezeptionist",
                "Rezeptionisten",
                "Rezeptionisten",
                "Rezeptionisten",
                nom_pl="Rezeptionisten",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Rezeptionistin", nom_pl="Rezeptionistinnen", status="Fachkraefte"),
        ],
        [
            Noun("MASCULINE", "Roomboy", "Roomboys", nom_pl="Roomboys", status="Helfer"),
            Noun(
                "NEUTRAL",
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
            Noun("MASCULINE", "Kellner", "Kellners", nom_pl="Kellner", status="Fachkraefte"),
            Noun("FEMININE", "Kellnerin", nom_pl="Kellnerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE", "Barista", "Baristas", nom_pl="Baristas", status="Fachkraefte", pronouns="er"
            ),
            Noun("FEMININE", "Barista", nom_pl="Baristas", status="Fachkraefte"),
            Noun(
                "MASCULINE", "Barista", "Baristas", nom_pl="Baristas", status="Fachkraefte", pronouns="dey"
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Tellerwäscher",
                "Tellerwäschers",
                nom_pl="Tellerwäscher",
                status="Helfer",
            ),
            Noun("FEMININE", "Tellerwäscherin", nom_pl="Tellerwäscherinnen", status="Helfer"),
        ],
    ],
    634: [
        [
            Noun("MASCULINE", "Host", "Hosts", nom_pl="Hosts", status="Helfer"),
            Noun("FEMININE", "Hostess", nom_pl="Hostessen", status="Helfer"),
        ],
        [
            Noun(
                "MASCULINE",
                "Eventmanager",
                "Eventmanagers",
                nom_pl="Eventmanager",
                status="Spezialisten",
            ),
            Noun("FEMININE", "Eventmanagerin", nom_pl="Eventmanagerinnen", status="Spezialisten"),
        ],
    ],
    711: [
        [
            Noun(
                "MASCULINE",
                "Geschäftsführer",
                "Geschäftsführers",
                nom_pl="Geschäftsführer",
                status="Experten",
            ),
            Noun(
                "FEMININE",
                "Geschäftsführerin",
                nom_pl="Geschäftsführerinnen",
                status="Experten",
            ),
            Noun("FEMININE", "Geschäftsführung", status="Experten", pronouns="dey"),
        ],
    ],
    712: [
        [
            Noun(
                "MASCULINE",
                "Abgeordneter",
                "Abgeordneten",
                "Abgeordneten",
                "Abgeordneten",
                nom_pl="Abgeordnete",
                status="Experten",
            ),
            Noun(
                "FEMININE",
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
                "MASCULINE",
                "Bürgermeister",
                "Bürgermeisters",
                nom_pl="Bürgermeister",
                status="Experten",
            ),
            Noun("FEMININE", "Bürgermeisterin", nom_pl="Bürgermeisterinnen", status="Experten"),
            Noun("NEUTRAL", "Stadtoberhaupt", status="Experten", pronouns="dey"),
        ],
    ],
    713: [
        [
            Noun(
                "MASCULINE",
                "Organisator",
                "Organisators",
                acc_sg="Organisator",
                dat_sg="Organisator",
                nom_pl="Organisatoren",
                status="Experten",
            ),
            Noun("FEMININE", "Organisatorin", nom_pl="Organisatorinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Betriebsassistent",
                "Betriebsassistenten",
                "Betriebsassistenten",
                "Betriebsassistenten",
                nom_pl="Betriebsassistenten",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Betriebsassistentin",
                nom_pl="Betriebsassistentinnen",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Betriebsassistenz", status="Fachkraefte", pronouns="dey"),
        ],
    ],
    714: [
        [
            Noun("MASCULINE", "Sekretär", "Sekretärs", nom_pl="Sekretäre", status="Fachkraefte"),
            Noun("FEMININE", "Sekretärin", nom_pl="Sekretärinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Büroassistent",
                "Büroassistenten",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Büroassistentin",
                nom_pl="Büroassistentinnen",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Büroassistenz", status="Fachkraefte", pronouns="dey"),
        ],
        [
            Noun(
                "MASCULINE",
                "Telefonist",
                "Telefonisten",
                "Telefonisten",
                "Telefonisten",
                nom_pl="Telefonisten",
                status="Helfer",
            ),
            Noun("FEMININE", "Telefonistin", nom_pl="Telefonistinnen", status="Helfer"),
        ],
        [
            Noun(
                "MASCULINE",
                "Chefsekretär",
                "Chefsekretärs",
                nom_pl="Chefsekretäre",
                status="Spezialisten",
            ),
            Noun("FEMININE", "Chefsekretärin", nom_pl="Chefsekretärinnen", status="Spezialisten"),
        ],
    ],
    715: [
        [
            Noun(
                "MASCULINE",
                "Ausbildungsleiter",
                "Ausbildungsleiters",
                nom_pl="Ausbildungsleiter",
                status="Experten",
            ),
            Noun(
                "FEMININE",
                "Ausbildungsleiterin",
                nom_pl="Ausbildungsleiterinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Arbeitsvermittler",
                "Arbeitsvermittlers",
                nom_pl="Arbeitsvermittler",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Arbeitsvermittlerin",
                nom_pl="Arbeitsvermittlerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    721: [
        [
            Noun(
                "MASCULINE",
                "Vermögensberater",
                "Vermögensberaters",
                nom_pl="Vermögensberater",
                status="Experten",
            ),
            Noun(
                "FEMININE",
                "Vermögensberaterin",
                nom_pl="Vermögensberaterinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Bankmitarbeiter",
                "Bankmitarbeiters",
                nom_pl="Bankmitarbeiter",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Bankmitarbeiterin",
                nom_pl="Bankmitarbeiterinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Börsenmakler",
                "Börsenmaklers",
                nom_pl="Börsenmakler",
                status="Spezialisten",
            ),
            Noun("FEMININE", "Börsenmaklerin", nom_pl="Börsenmaklerinnen", status="Spezialisten"),
        ],
    ],
    722: [
        [
            Noun(
                "MASCULINE",
                "Wirtschaftsprüfer",
                "Wirtschaftsprüfers",
                nom_pl="Wirtschaftsprüfer",
                status="Experten",
            ),
            Noun(
                "FEMININE",
                "Wirtschaftsprüferin",
                nom_pl="Wirtschaftsprüferinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Buchhalter",
                "Buchhalters",
                nom_pl="Buchhalter",
                status="Spezialisten",
            ),
            Noun("FEMININE", "Buchhalterin", nom_pl="Buchhalterinnen", status="Spezialisten"),
        ],
    ],
    723: [
        [
            Noun(
                "MASCULINE",
                "Steuerberater",
                "Steuerberaters",
                nom_pl="Steuerberater",
                status="Experten",
            ),
            Noun("FEMININE", "Steuerberaterin", nom_pl="Steuerberaterinnen", status="Experten"),
        ],
    ],
    731: [
        [
            Noun("MASCULINE", "Richter", "Richters", nom_pl="Richter", status="Experten"),
            Noun("FEMININE", "Richterin", nom_pl="Richterinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Jurist",
                "Juristen",
                "Juristen",
                "Juristen",
                nom_pl="Juristen",
                status="Experten",
            ),
            Noun("FEMININE", "Juristin", nom_pl="Juristinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Anwaltssekretär",
                "Anwaltssekretärs",
                nom_pl="Anwaltssekretäre",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Anwaltssekretärin",
                nom_pl="Anwaltssekretärinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    732: [
        [
            Noun(
                "MASCULINE",
                "Arztsekretär",
                "Arztsekretärs",
                nom_pl="Arztsekretäre",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Arztsekretärin",
                nom_pl="Arztsekretärinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Verwaltungsangestellte",
                "Verwaltungsangestellten",
                nom_pl="Verwaltungsangestellte",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
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
                "MASCULINE",
                "Büchereiangestellte",
                "Büchereiangestellten",
                nom_pl="Büchereiangestellten",
                status="Experten",
            ),
            Noun("FEMININE", "Büchereiangestellte", nom_pl="Büchereiangestellten", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Archivar",
                "Archivars",
                acc_sg="Archivar",
                dat_sg="Archivar",
                nom_pl="Archivare",
                status="Spezialisten",
            ),
            Noun("FEMININE", "Archivarin", nom_pl="Archivarinnen", status="Spezialisten"),
        ],
    ],
    811: [
        [
            Noun(
                "MASCULINE",
                "Arzthelfer",
                "Arzthelfers",
                nom_pl="Arzthelfer",
                dat_pl="Arzthelfern",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Arzthelferin", nom_pl="Arzthelferinnen", status="Fachkraefte"),
            Noun(
                "FEMININE",
                "Arzthilfe",
                nom_pl="Arzthilfen",
                status="Fachkraefte",
                pronouns="dey",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Coronatester",
                "Coronatesters",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Coronatesterin", nom_pl="Coronatesterinnen", status="Fachkraefte"),
        ],
    ],
    812: [
        [
            Noun(
                "MASCULINE",
                "Pathologe",
                "Pathologen",
                "Pathologen",
                "Pathologen",
                nom_pl="Pathologen",
                status="Experten",
            ),
            Noun("FEMININE", "Pathologin", nom_pl="Pathologinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Radiologieassistent",
                "Radiologieassistenten",
                "Radiologieassistenten",
                "Radiologieassistenten",
                nom_pl="Radiologieassistenten",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Radiologieassistentin",
                nom_pl="Radiologieassistentinnen",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Radiologieassistenz", status="Fachkraefte", pronouns="dey"),
        ],
    ],
    813: [
        [
            Noun(
                "MASCULINE",
                "Pflegeassistent",
                "Pflegeassistenten",
                "Pflegeassistenten",
                "Pflegeassistenten",
                nom_pl="Pflegeassistenten",
                status="Helfer",
            ),
            Noun("FEMININE", "Pflegeassistentin", nom_pl="Pflegeassistentinnen", status="Helfer"),
            Noun("FEMININE", "Pflegeassistenz", status="Helfer", pronouns="dey"),
        ],
        [
            Noun("FEMININE", "Hebamme", nom_pl="Hebammen", status="Spezialisten", pronouns="er"),
            Noun("FEMININE", "Hebamme", nom_pl="Hebammen", status="Spezialisten", pronouns="sie"),
            Noun("FEMININE", "Hebamme", nom_pl="Hebammen", status="Spezialisten", pronouns="dey"),
        ],
        [
            Noun(
                "MASCULINE",
                "Krankenpfleger",
                "Krankenpflegers",
                nom_pl="Krankenpfleger",
                dat_pl="Krankenpflegern",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Krankenpflegerin",
                nom_pl="Krankenpflegerinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Rettungssanitäter",
                "Rettungssanitäters",
                nom_pl="Rettungssanitäter",
                dat_pl="Rettungssanitätern",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Rettungssanitäterin",
                nom_pl="Rettungssanitäterinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    814: [
        [
            Noun(
                "MASCULINE",
                "Arzt",
                "Arztes",
                nom_pl="Ärzte",
                dat_pl="Ärzten",
                acc_pl="Ärzte",
                status="Experten",
            ),
            Noun("FEMININE", "Ärztin", nom_pl="Ärztinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Zahnarzt",
                "Zahnarztes",
                nom_pl="Zahnärzte",
                dat_pl="Zahnärzten",
                acc_pl="Zahnärzte",
                status="Experten",
            ),
            Noun("FEMININE", "Zahnärztin", nom_pl="Zahnärztinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Chirurg",
                "Chirurgen",
                "Chirurgen",
                "Chirurgen",
                nom_pl="Chirurgen",
                status="Experten",
            ),
            Noun("FEMININE", "Chirurgin", nom_pl="Chirurginnen", status="Experten"),
        ],
    ],
    815: [
        [
            Noun(
                "MASCULINE",
                "Tierarzt",
                "Tierarztes",
                nom_pl="Tierärzte",
                dat_pl="Tierärzten",
                acc_pl="Tierärzte",
                status="Experten",
            ),
            Noun("FEMININE", "Tierärztin", nom_pl="Tierärztinnen", status="Experten"),
        ],
    ],
    816: [
        [
            Noun(
                "MASCULINE",
                "Psychotherapeut",
                "Psychotherapeuten",
                "Psychotherapeuten",
                "Psychotherapeuten",
                nom_pl="Psychotherapeuten",
                status="Experten",
            ),
            Noun(
                "FEMININE",
                "Psychotherapeutin",
                nom_pl="Psychotherapeutinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Suchttherapeut",
                "Suchttherapeuten",
                "Suchttherapeuten",
                "Suchttherapeuten",
                nom_pl="Suchttherapeuten",
                status="Experten",
            ),
            Noun("FEMININE", "Suchttherapeutin", nom_pl="Suchttherapeutinnen", status="Experten"),
        ],
    ],
    817: [
        [
            Noun(
                "MASCULINE",
                "Physiotherapeut",
                "Physiotherapeuten",
                "Physiotherapeuten",
                "Physiotherapeuten",
                nom_pl="Physiotherapeuten",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Physiotherapeutin",
                nom_pl="Physiotherapeutinnen",
                status="Spezialisten",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Logopäde",
                "Logopäden",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Logopädin",
                nom_pl="Logopädinnen",
                status="Spezialisten",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Masseur",
                "Masseurs",
                nom_pl="Masseure",
                dat_pl="Masseuren",
                acc_pl="Masseure",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Masseurin", nom_pl="Masseurinnen", status="Fachkraefte"),
        ],
    ],
    818: [
        [
            Noun(
                "MASCULINE",
                "Apotheker",
                "Apothekers",
                nom_pl="Apotheker",
                dat_pl="Apothekern",
                status="Experten",
            ),
            Noun("FEMININE", "Apothekerin", nom_pl="Apothekerinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Pharmalaborant",
                "Pharmalaboranten",
                "Pharmalaboranten",
                "Pharmalaboranten",
                nom_pl="Pharmalaboranten",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Pharmalaborantin",
                nom_pl="Pharmalaborantinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Pharmazeut",
                "Pharmazeuten",
                "Pharmazeuten",
                "Pharmazeuten",
                nom_pl="Pharmazeuten",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Pharmazeutin",
                nom_pl="Pharmazeutinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    821: [
        [
            Noun(
                "MASCULINE",
                "Altenpfleger",
                "Altenpflegers",
                nom_pl="Altenpfleger",
                dat_pl="Altenpflegern",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Altenpflegerin", nom_pl="Altenpflegerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Pflegehelfer",
                "Pflegehelfers",
                nom_pl="Pflegehelfer",
                dat_pl="Pflegehelfern",
                status="Helfer",
            ),
            Noun(
                "FEMININE",
                "Pflegehilfe",
                nom_pl="Pflegehilfen",
                status="Helfer",
                pronouns="dey",
            ),
            Noun("FEMININE", "Pflegehelferin", nom_pl="Pflegehelferinnen", status="Helfer"),
        ],
    ],
    822: [
        [
            Noun(
                "MASCULINE",
                "Ernährungsberater",
                "Ernährungsberaters",
                nom_pl="Ernährungsberater",
                dat_pl="Ernährungsberatern",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Ernährungsberaterin",
                nom_pl="Ernährungsberaterinnen",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
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
                "MASCULINE",
                "Friseur",
                "Friseurs",
                nom_pl="Friseure",
                dat_pl="Friseuren",
                acc_pl="Friseure",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Friseurin", nom_pl="Friseurinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Tätowierer",
                "Tätowierers",
                nom_pl="Tätowierer",
                dat_pl="Tätowierern",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Tätowiererin", nom_pl="Tätowiererinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Maskenbildner",
                "Maskenbildners",
                nom_pl="Maskenbildner",
                dat_pl="Maskenbildnern",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Maskenbildnerin",
                nom_pl="Maskenbildnerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    824: [
        [
            Noun(
                "MASCULINE",
                "Bestatter",
                "Bestatters",
                nom_pl="Bestatter",
                dat_pl="Bestattern",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Bestatterin", nom_pl="Bestatterinnen", status="Fachkraefte"),
        ],
    ],
    825: [
        [
            Noun(
                "MASCULINE",
                "Optiker",
                "Optikers",
                nom_pl="Optiker",
                dat_pl="Optikern",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Optikerin", nom_pl="Optikerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Hörakustiker",
                "Hörakustikers",
                nom_pl="Hörakustiker",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Hörakustikerin", nom_pl="Hörakustikerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Medizintechniker",
                "Medizintechnikers",
                nom_pl="Medizintechniker",
                dat_pl="Medizintechnikern",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Medizintechnikerin",
                nom_pl="Medizintechnikerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    831: [
        [
            Noun(
                "MASCULINE",
                "Jugendberater",
                "Jugendberaters",
                nom_pl="Jugendberater",
                dat_pl="Jugendberatern",
                status="Experten",
            ),
            Noun("FEMININE", "Jugendberaterin", nom_pl="Jugendberaterinnen", status="Experten"),
            Noun(
                "FEMININE",
                "Jugendberatung",
                nom_pl="Jugendberatungen",
                status="Experten",
                pronouns="dey",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Sozialarbeiter",
                "Sozialarbeiters",
                nom_pl="Sozialarbeiter",
                dat_pl="Sozialarbeitern",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Sozialarbeiterin",
                nom_pl="Sozialarbeiterinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "FEMININE",
                "Integrationsfachkraft",
                nom_pl="Integrationsfachkräfte",
                status="Fachkraefte",
                pronouns="er",
            ),
            Noun(
                "FEMININE",
                "Integrationsfachkraft",
                nom_pl="Integrationsfachkräfte",
                status="Fachkraefte",
                pronouns="sie",
            ),
            Noun(
                "FEMININE",
                "Integrationsfachkraft",
                nom_pl="Integrationsfachkräfte",
                status="Fachkraefte",
                pronouns="dey",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Betreuer",
                "Betreuers",
                nom_pl="Betreuer",
                dat_pl="Betreuern",
                status="Helfer",
            ),
            Noun("FEMININE", "Betreuerin", nom_pl="Betreuerinnen", status="Helfer"),
        ],
        [
            Noun(
                "MASCULINE",
                "Erzieher",
                "Erziehers",
                nom_pl="Erzieher",
                dat_pl="Erziehern",
                status="Spezialisten",
            ),
            Noun("FEMININE", "Erzieherin", nom_pl="Erzieherinnen", status="Spezialisten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Kindergärtner",
                "Kindergärtners",
                nom_pl="Kindergärtner",
                dat_pl="Kindergärtnern",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Kindergärtnerin",
                nom_pl="Kindergärtnerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    832: [
        [
            Noun(
                "MASCULINE",
                "Haushälter",
                "Haushälters",
                nom_pl="Haushälter",
                dat_pl="Haushältern",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Haushälterin", nom_pl="Haushälterinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Haushaltshelfer",
                "Haushaltshelfers",
                nom_pl="Haushaltshelfer",
                status="Helfer",
            ),
            Noun("FEMININE", "Haushaltshelferin", nom_pl="Haushaltshelferinnen", status="Helfer"),
        ],
        [
            Noun("FEMININE", "Haushaltshilfe", nom_pl="Haushaltshilfen", pronouns="dey", status="Helfer"),
        ],
    ],
    833: [
        [
            Noun(
                "MASCULINE",
                "Pfarrer",
                "Pfarrers",
                nom_pl="Pfarrer",
                dat_pl="Pfarrern",
                status="Experten",
            ),
            Noun("FEMININE", "Pfarrerin", nom_pl="Pfarrerinnen", status="Experten"),
        ],
    ],
    841: [
        [
            Noun(
                "MASCULINE",
                "Lehrer",
                "Lehrers",
                nom_pl="Lehrer",
                dat_pl="Lehrern",
                status="Experten",
            ),
            Noun("FEMININE", "Lehrerin", nom_pl="Lehrerinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Grundschullehrer",
                "Grundschullehrers",
                nom_pl="Grundschullehrer",
                dat_pl="Grundschullehrern",
                status="Experten",
            ),
            Noun("FEMININE", "Grundschullehrerin", nom_pl="Grundschullehrerinnen", status="Experten"),
        ],
    ],
    842: [
        [
            Noun(
                "MASCULINE",
                "Werklehrer",
                "Werklehrers",
                nom_pl="Werklehrer",
                status="Spezialisten",
            ),
            Noun("FEMININE", "Werklehrerin", nom_pl="Werklehrerinnen", status="Spezialisten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Berufsschullehrer",
                "Berufsschullehrers",
                nom_pl="Berufsschullehrer",
                dat_pl="Berufsschullehrern",
                status="Experten",
            ),
            Noun(
                "FEMININE",
                "Berufsschullehrerin",
                nom_pl="Berufsschullehrerinnen",
                status="Experten",
            ),
        ],
    ],
    843: [
        [
            Noun(
                "MASCULINE",
                "Dozent",
                "Dozenten",
                "Dozenten",
                "Dozenten",
                nom_pl="Dozenten",
                status="Experten",
            ),
            Noun("FEMININE", "Dozentin", nom_pl="Dozentinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Professor",
                "Professors",
                nom_pl="Professoren",
                dat_pl="Professoren",
                acc_pl="Professoren",
                status="Experten",
            ),
            Noun("FEMININE", "Professorin", nom_pl="Professorinnen", status="Experten"),
        ],
    ],
    844: [
        [
            Noun(
                "MASCULINE",
                "Gitarrenlehrer",
                "Gitarrenlehrers",
                nom_pl="Gitarrenlehrer",
                dat_pl="Gitarrenlehrern",
                status="Experten",
            ),
            Noun("FEMININE", "Gitarrenlehrerin", nom_pl="Gitarrenlehrerinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Gesangslehrer",
                "Gesangslehrers",
                status="Experten",
            ),
            Noun("FEMININE", "Gesangslehrerin", nom_pl="Gesangslehrerinnen", status="Experten"),
        ],
    ],
    845: [
        [
            Noun(
                "MASCULINE",
                "Fahrlehrer",
                "Fahrlehrers",
                nom_pl="Fahrlehrer",
                dat_pl="Fahrlehrern",
                status="Spezialisten",
            ),
            Noun("FEMININE", "Fahrlehrerin", nom_pl="Fahrlehrerinnen", status="Spezialisten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Trainer",
                "Trainers",
                nom_pl="Trainer",
                dat_pl="Trainern",
                status="Spezialisten",
            ),
            Noun("FEMININE", "Trainerin", nom_pl="Trainerinnen", status="Spezialisten"),
        ],
    ],
    911: [
        [
            Noun(
                "MASCULINE",
                "Linguist",
                "Linguisten",
                "Linguisten",
                "Linguisten",
                nom_pl="Linguisten",
                status="Experten",
            ),
            Noun("FEMININE", "Linguistin", nom_pl="Linguistinnen", status="Experten"),
        ],
    ],
    912: [
        [
            Noun("MASCULINE", "Historiker", "Historikers", nom_pl="Historiker", status="Experten"),
            Noun("FEMININE", "Historikerin", nom_pl="Historikerinnen", status="Experten"),
        ],
    ],
    913: [
        [
            Noun(
                "MASCULINE",
                "Marktforscher",
                "Marktforschers",
                nom_pl="Marktforscher",
                status="Experten",
            ),
            Noun("FEMININE", "Marktforscherin", nom_pl="Marktforscherinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Soziologe",
                "Soziologen",
                "Soziologen",
                "Soziologen",
                nom_pl="Soziologen",
                status="Experten",
            ),
            Noun("FEMININE", "Soziologin", nom_pl="Soziologinnen", status="Experten"),
        ],
    ],
    914: [
        [
            Noun(
                "MASCULINE",
                "Ökonom",
                "Ökonomen",
                "Ökonomen",
                "Ökonomen",
                nom_pl="Ökonomen",
                status="Experten",
            ),
            Noun("FEMININE", "Ökonomin", nom_pl="Ökonominnen", status="Experten"),
        ],
    ],
    921: [
        [
            Noun(
                "MASCULINE",
                "Callcenteragent",
                "Callcenteragenten",
                nom_pl="Callcenteragenten",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Callcenteragentin", nom_pl="Callcenteragentinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Werbetexter",
                "Werbetexters",
                nom_pl="Werbetexter",
                status="Spezialisten",
            ),
            Noun("FEMININE", "Werbetexterin", nom_pl="Werbetexterinnen", status="Spezialisten"),
        ],
    ],
    922: [
        [
            Noun(
                "MASCULINE",
                "Pressesprecher",
                "Pressesprechers",
                nom_pl="Pressesprecher",
                status="Experten",
            ),
            Noun("FEMININE", "Pressesprecherin", nom_pl="Pressesprecherinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Lobbyist",
                "Lobbyisten",
                "Lobbyisten",
                "Lobbyisten",
                nom_pl="Lobbyisten",
                status="Spezialisten",
            ),
            Noun("FEMININE", "Lobbyistin", nom_pl="Lobbyistinnen", status="Spezialisten"),
        ],
    ],
    923: [
        [
            Noun(
                "MASCULINE",
                "Literaturagent",
                "Literaturagenten",
                "Literaturagenten",
                "Literaturagenten",
                nom_pl="Literaturagenten",
                status="Experten",
            ),
            Noun("FEMININE", "Literaturagentin", nom_pl="Literaturagentinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Anzeigenagent",
                "Anzeigenagents",
                nom_pl="Anzeigenagenten",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Anzeigenagentin", nom_pl="Anzeigenagentinnen", status="Fachkraefte"),
        ],
    ],
    924: [
        [
            Noun("MASCULINE", "Reporter", "Reporters", nom_pl="Reporter", status="Experten"),
            Noun("FEMININE", "Reporterin", nom_pl="Reporterinnen", status="Experten"),
        ],
        [
            Noun("MASCULINE", "Dichter", "Dichters", nom_pl="Dichter", status="Experten"),
            Noun("FEMININE", "Dichterin", nom_pl="Dichterinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Journalist",
                "Journalisten",
                "Journalisten",
                "Journalisten",
                nom_pl="Journalisten",
                status="Experten",
            ),
            Noun("FEMININE", "Journalistin", nom_pl="Journalistinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Redaktionsassistent",
                "Redaktionsassistenten",
                "Redaktionsassistenten",
                "Redaktionsassistenten",
                nom_pl="Redaktionsassistenten",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
                "Redaktionsassistentin",
                nom_pl="Redaktionsassistentinnen",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Redaktionsassistenz", status="Experten", pronouns="dey"),
        ],
        [
            Noun(
                "MASCULINE",
                "Redakteur",
                "Redakteurs",
                nom_pl="Redakteure",
                status="Spezialisten",
            ),
            Noun("FEMININE", "Redakteurin", nom_pl="Redakteurinnen", status="Spezialisten"),
        ],
    ],
    931: [
        [
            Noun(
                "MASCULINE",
                "Möbeldesigner",
                "Möbeldesigners",
                dat_sg="Möbeldesigner",
                acc_sg="Möbeldesigner",
                nom_pl="Möbeldesigner",
                acc_pl="Möbeldesigner",
                status="Experten",
            ),
            Noun(
                "FEMININE",
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
                "MASCULINE",
                "Innenarchitekt",
                "Innenarchitekten",
                "Innenarchitekten",
                "Innenarchitekten",
                nom_pl="Innenarchitekten",
                acc_pl="Innenarchitekten",
                status="Experten",
            ),
            Noun(
                "FEMININE",
                "Innenarchitektin",
                nom_pl="Innenarchitektinnen",
                acc_pl="Innenarchitektinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Innenausstatter",
                "Innenausstatters",
                dat_sg="Innenausstatter",
                acc_sg="Innenausstatter",
                nom_pl="Innenausstatter",
                acc_pl="Innenausstatter",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
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
                "MASCULINE",
                "Restaurator",
                "Restaurators",
                dat_sg="Restaurator",
                acc_sg="Restaurator",
                nom_pl="Restauratoren",
                acc_pl="Restauratoren",
                status="Experten",
            ),
            Noun(
                "FEMININE",
                "Restauratorin",
                nom_pl="Restauratorinnen",
                acc_pl="Restauratorinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "MASCULINE",
                "Bildhauer",
                "Bildhauers",
                dat_sg="Bildhauer",
                acc_sg="Bildhauer",
                nom_pl="Bildhauer",
                acc_pl="Bildhauer",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
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
                "MASCULINE",
                "Töpfer",
                "Töpfers",
                dat_sg="Töpfer",
                acc_sg="Töpfer",
                nom_pl="Töpfer",
                acc_pl="Töpfer",
                status="Fachkraefte",
            ),
            Noun(
                "FEMININE",
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
                "MASCULINE",
                "Goldschmied",
                "Goldschmieds",
                nom_pl="Goldschmiede",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Goldschmiedin", nom_pl="Goldschmiedinnen", status="Fachkraefte"),
        ],
    ],
    936: [
        [
            Noun(
                "MASCULINE",
                "Geigenbauer",
                "Geigenbauers",
                nom_pl="Geigenbauer",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Geigenbauerin", nom_pl="Geigenbauerinnen", status="Fachkraefte"),
        ],
    ],
    941: [
        [
            Noun("MASCULINE", "Sänger", "Sängers", nom_pl="Sänger", status="Experten"),
            Noun("FEMININE", "Sängerin", nom_pl="Sängerinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Klaviespieler",
                "Klaviespielers",
                nom_pl="Klaviespieler",
                status="Experten",
            ),
            Noun("FEMININE", "Klaviespielerin", nom_pl="Klaviespielerinnen", status="Experten"),
        ],
    ],
    942: [
        [
            Noun(
                "MASCULINE",
                "Schauspieler",
                "Schauspielers",
                nom_pl="Schauspieler",
                status="Experten",
            ),
            Noun("FEMININE", "Schauspielerin", nom_pl="Schauspielerinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Prostituierter",
                "Prostituierten",
                "Prostituierten",
                "Prostituierten",
                nom_pl="Prostituierten",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Prostituierte", nom_pl="Prostituierten", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Fußballer",
                "Fußballers",
                nom_pl="Fußballer",
                status="Spezialisten",
            ),
            Noun("FEMININE", "Fußballerin", nom_pl="Fußballerinnen", status="Spezialisten"),
        ],
        [
            Noun(
                "NEUTRAL",
                "Model",
                "Models",
                nom_pl="Models",
                status="Fachkraefte",
                pronouns="er",
            ),
            Noun(
                "NEUTRAL",
                "Model",
                "Models",
                nom_pl="Models",
                status="Fachkraefte",
                pronouns="sie",
            ),
            Noun(
                "NEUTRAL",
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
            Noun("MASCULINE", "Hellseher", "Hellsehers", nom_pl="Hellseher", status="Fachkraefte"),
            Noun("FEMININE", "Hellseherin", nom_pl="Hellseherinnen", status="Fachkraefte"),
        ],
        [
            Noun("MASCULINE", "Wahrsager", "Wahrsagers", nom_pl="Wahrsager", status="Fachkraefte"),
            Noun("FEMININE", "Wahrsagerin", nom_pl="Wahrsagerinnen", status="Fachkraefte"),
        ],
    ],
    944: [
        [
            Noun("MASCULINE", "Souffleur", "Souffleurs", nom_pl="Souffleure", status="Fachkraefte"),
            Noun("FEMININE", "Souffleuse", nom_pl="Souffleusen", status="Fachkraefte"),
        ],
        [
            Noun("MASCULINE", "Filmregisseur", status="Experten"),
            Noun("FEMININE", "Filmregisseurin", status="Experten"),
            Noun("FEMININE", "Filmregie", status="Experten", pronouns="dey"),
        ],
        [
            Noun(
                "MASCULINE",
                "Produzent",
                "Produzenten",
                "Produzenten",
                "Produzenten",
                nom_pl="Produzenten",
                status="Spezialisten",
            ),
            Noun(
                "FEMININE",
                "Produzentin",
                nom_pl="Produzentinnen",
                status="Spezialisten",
            ),
        ],
    ],
    945: [
        [
            Noun(
                "MASCULINE",
                "Pyrotechniker",
                "Pyrotechnikers",
                nom_pl="Pyrotechniker",
                status="Fachkraefte",
            ),
            Noun("FEMININE", "Pyrotechnikerin", nom_pl="Pyrotechnikerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "MASCULINE",
                "Kameramann",
                "Kameramanns",
                nom_pl="Kameramänner",
                status="Spezialisten",
            ),
            Noun("FEMININE", "Kamerafrau", nom_pl="Kamerafrauen", status="Spezialisten"),
        ],
    ],
    946: [
        [
            Noun(
                "MASCULINE",
                "Bühnenbildner",
                "Bühnenbildners",
                nom_pl="Bühnenbildner",
                status="Experten",
            ),
            Noun("FEMININE", "Bühnenbildnerin", nom_pl="Bühnenbildnerinnen", status="Experten"),
        ],
        [
            Noun(
                "MASCULINE",
                "Requisiteur",
                "Requisiteurs",
                nom_pl="Requisiteure",
                status="Spezialisten",
            ),
            Noun("FEMININE", "Requisiteurin", nom_pl="Requisiteurinnen", status="Spezialisten"),
        ],
    ],
    947: [
        [
            Noun("MASCULINE", "Kurator", "Kurators", nom_pl="Kuratoren", status="Experten"),
            Noun("FEMININE", "Kuratorin", nom_pl="Kuratorinnen", status="Experten"),
        ],
    ],
}
