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
            Noun("n", "Date", "Dates", nom_pl="Dates", dat_pl="Dates", pronouns="er"),
            Noun("n", "Date", "Dates", nom_pl="Dates", dat_pl="Dates", pronouns="sie"),
            Noun("n", "Date", "Dates", nom_pl="Dates", dat_pl="Dates", pronouns="dey"),
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
                "Agrarökonom",
                "Agrarökonomen",
                "Agrarökonomen",
                "Agrarökonomen",
                nom_pl="Agrarökonomen",
                status="Experten",
            ),
            Noun("f", "Agrarökonomin", nom_pl="Agrarökonominnen", status="Experten"),
        ],
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
            Noun(
                "f", "Erntehilfe", nom_pl="Erntehilfen", status="Helfer", pronouns="dey"
            ),
        ],
        [
            Noun(
                "m",
                "Landwirt",
                "Landwirts",
                nom_pl="Landwirte",
                dat_pl="Landwirten",
                acc_pl="Landwirte",
                status="Spezialisten",
            ),
            Noun("f", "Landwirtin", nom_pl="Landwirtinnen", status="Spezialisten"),
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
        [
            Noun(
                "m",
                "Hirte",
                "Hirten",
                "Hirten",
                "Hirten",
                nom_pl="Hirten",
                status="Fachkraefte",
            ),
            Noun("f", "Hirtin", nom_pl="Hirtinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Schäfer",
                "Schäfer",
                "Schäfer",
                "Schäfer",
                nom_pl="Schäfer",
                status="Fachkraefte",
            ),
            Noun("f", "Schäferin", nom_pl="Schäferinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Viehtreiber",
                "Viehtreibers",
                nom_pl="Viehtreiber",
                dat_pl="Viehtreibern",
                status="Helfer",
            ),
            Noun("f", "Viehtreiberin", nom_pl="Viehtreiberinnen", status="Helfer"),
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
        [
            Noun(
                "m",
                "Hufschmied",
                "Hufschmieds",
                nom_pl="Hufschmiede",
                dat_pl="Hufschmieden",
                acc_pl="Hufschmiede",
                status="Spezialisten",
            ),
            Noun("f", "Hufschmiedin", nom_pl="Hufschmiedinnen", status="Spezialisten"),
        ],
        [
            Noun(
                "m",
                "Pferdepfleger",
                "Pferdepflegers",
                nom_pl="Pferdepfleger",
                dat_pl="Pferdepflegern",
                status="Fachkraefte",
            ),
            Noun(
                "f", "Pferdepflegerin", nom_pl="Pferdepflegerinnen", status="Fachkraefte"
            ),
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
        [
            Noun(
                "m",
                "Fischzüchter",
                "Fischzüchters",
                nom_pl="Fischzüchter",
                dat_pl="Fischzüchtern",
                status="Fachkraefte",
            ),
            Noun(
                "f", "Fischzüchterin", nom_pl="Fischzüchterinnen", status="Fachkraefte"
            ),
        ],
    ],
    115: [
        [
            Noun(
                "m",
                "Falkner",
                "Falkners",
                nom_pl="Falkner",
                dat_pl="Falknern",
                status="Fachkraefte",
            ),
            Noun("f", "Falknerin", nom_pl="Falknerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Zoowärter",
                "Zoowärters",
                nom_pl="Zoowärter",
                dat_pl="Zoowärtern",
                status="Fachkraefte",
            ),
            Noun("f", "Zoowärterin", nom_pl="Zoowärterinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Hundetrainer",
                "Hundetrainers",
                nom_pl="Hundetrainer",
                dat_pl="Hundetrainern",
                status="Fachkraefte",
            ),
            Noun(
                "f", "Hundetrainerin", nom_pl="Hundetrainerinnen", status="Fachkraefte"
            ),
        ],
        [
            Noun(
                "m",
                "Tiertrainer",
                "Tiertrainers",
                nom_pl="Tiertrainer",
                dat_pl="Tiertrainern",
                status="Fachkraefte",
            ),
            Noun(
                "f", "Tiertrainerin", nom_pl="Tiertrainerinnen", status="Fachkraefte"
            ),
        ],
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
                "Forstwissenschaftler",
                "Forstwissenschaftlers",
                nom_pl="Forstwissenschaftler",
                dat_pl="Forstwissenschaftlern",
                status="Experten",
            ),
            Noun("f", "Forstwissenschaftlerin", nom_pl="Forstwissenschaftlerinnen", status="Experten"),
        ],
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
        [
            Noun(
                "m",
                "Waldarbeiter",
                "Waldarbeiters",
                nom_pl="Waldarbeiter",
                dat_pl="Waldarbeitern",
                status="Helfer",
            ),
            Noun("f", "Waldarbeiterin", nom_pl="Waldarbeiterinnen", status="Helfer"),
        ],
    ],
    121: [
        [
            Noun(
                "m",
                "Gartenarchitekt",
                "Gartenarchitekten",
                "Gartenarchitekten",
                "Gartenarchitekten",
                nom_pl="Gartenarchitekten",
                status="Experten",
            ),
            Noun(
                "f",
                "Gartenarchitektin",
                nom_pl="Gartenarchitektinnen",
                status="Experten",
            ),
        ],
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
            Noun(
                "f", "Gartenarbeiterin", nom_pl="Gartenarbeiterinnen", status="Helfer"
            ),
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
                status="Fachkräfte",
            ),
            Noun("f", "Floristin", nom_pl="Floristinnen", status="Fachkräfte"),
        ],
        [
            Noun(
                "m",
                "Blumenhändler",
                "Blumenhändlers",
                "Blumenhändler",
                "Blumenhändler",
                nom_pl="Blumenhändler",
                status="Fachkraefte",
            ),
            Noun("f", "Blumenhändlerin", nom_pl="Blumenhändlerinnen", status="Fachkraefte"),
        ],
    ],
    211: [
        [
            Noun(
                "m",
                "Bergbauingenieur",
                "Bergbauingenieurs",
                nom_pl="Bergbauingenieure",
                status="Experten",
            ),
            Noun(
                "f",
                "Bergbauingenieurin",
                nom_pl="Bergbauingenieurinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m",
                "Sprengtechniker",
                "Sprengtechnikers",
                nom_pl="Sprengtechniker",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Sprengtechnikerin",
                nom_pl="Sprengtechnikerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    212: [
        [
            Noun(
                "m",
                "Baustoffingenieur",
                "Baustoffingenieurs",
                nom_pl="Baustoffingenieure",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Baustoffingenieurin",
                nom_pl="Baustoffingenieurinnen",
                status="Spezialisten",
            ),
        ],
        [
            Noun(
                "m",
                "Ziegeleiarbeiter",
                "Ziegeleiarbeiters",
                nom_pl="Ziegeleiarbeiter",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Ziegeleiarbeiterin",
                nom_pl="Ziegeleiarbeiterinnen",
                status="Spezialisten",
            ),
        ],
        [
            Noun(
                "m",
                "Steinmetz",
                "Steinmetzes",
                nom_pl="Steinmetze",
                status="Fachkraefte",
            ),
            Noun(
                "f", "Steinmetzin", nom_pl="Steinmetzinnen", status="Fachkraefte"
            ),
        ],
    ],
    213: [
        [
            Noun(
                "m",
                "Fensterbautechniker",
                "Fensterbautechnikers",
                nom_pl="Fensterbautechniker",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Fensterbautechnikerin",
                nom_pl="Fensterbautechnikerinnen",
                status="Spezialisten",
            ),
        ],
        [
            Noun(
                "m",
                "Glasmacher",
                "Glasmachers",
                nom_pl="Glasmacher",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Glasmacherin",
                nom_pl="Glasmacherinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    214: [
        [
            Noun(
                "m",
                "Fliesenmacher",
                "Fliesenmachers",
                nom_pl="Fliesenmacher",
                status="Fachkraefte",
            ),
            Noun(
                "f", "Fliesenmacherin", nom_pl="Fliesenmacherinnen", status="Fachkraefte"
            ),
        ],
        [
            Noun(
                "m",
                "Keramikarbeiter",
                "Keramikarbeiters",
                nom_pl="Keramikarbeiter",
                status="Helfer",
            ),
            Noun(
                "f", "Keramikarbeiterin", nom_pl="Keramikarbeiterinnen", status="Helfer"
            ),
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
    ],
    222: [
        [
            Noun(
                "m",
                "Beschichtungstechniker",
                "Beschichtungstechnikers",
                nom_pl="Beschichtungstechniker",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Beschichtungstechnikerin",
                nom_pl="Beschichtungstechnikerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    223: [
        [
            Noun(
                "m",
                "Holzingenieur",
                "Holzingenieurs",
                nom_pl="Holzingenieure",
                status="Experten",
            ),
            Noun(
                "f", "Holzingenieurin", nom_pl="Holzingenieurinnen", status="Experten"
            ),
        ],
        [
            Noun(
                "m", "Möbeltischler", "Möbeltischlers", nom_pl="Möbeltischler", status="Fachkraefte"
            ),
            Noun("f", "Möbeltischlerin", nom_pl="Möbeltischlerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m", "Holzkitter", "Holzkitters", nom_pl="Holzkitter", status="Helfer"
            ),
            Noun("f", "Holzkitterin", nom_pl="Holzkitterinnen", status="Helfer"),
        ],
        [
            Noun(
                "m",
                "Möbelrestaurator",
                "Möbelrestaurators",
                acc_sg="Möbelrestaurator",
                dat_sg="Möbelrestaurator",
                nom_pl="Möbelrestauratoren",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Möbelrestauratorin",
                nom_pl="Möbelrestauratorinnen",
                status="Spezialisten",
            ),
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
            Noun(
                "f", "Papierfärberin", nom_pl="Papierfärberinnen", status="Fachkraefte"
            ),
        ],
        [
            Noun(
                "m",
                "Papiersortierer",
                "Papiersortierers",
                nom_pl="Papiersortierer",
                status="Helfer",
            ),
            Noun(
                "f", "Papiersortiererin", nom_pl="Papiersortiererinnen", status="Helfer"
            ),
        ],
        [
            Noun(
                "m",
                "Verpackungsdesigner",
                "Verpackungsdesigners",
                nom_pl="Verpackungsdesigner",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Verpackungsdesignerin",
                nom_pl="Verpackungsdesignerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    232: [
        [
            Noun(
                "m",
                "Grafikdesigner",
                "Grafikdesigners",
                nom_pl="Grafikdesigner",
                status="Experten",
            ),
            Noun(
                "f", "Grafikdesignerin", nom_pl="Grafikdesignerinnen", status="Experten"
            ),
        ],
        [
            Noun(
                "m",
                "Werbezeichner",
                "Werbezeichners",
                nom_pl="Werbezeichner",
                status="Fachkraefte",
            ),
            Noun(
                "f", "Werbezeichnerin", nom_pl="Werbezeichnerinnen", status="Fachkraefte"
            ),
        ],
        [
            Noun(
                "m",
                "Werbegrafiker",
                "Werbegrafikers",
                nom_pl="Werbegrafiker",
                status="Spezialisten",
            ),
            Noun(
                "f", "Werbegrafikerin", nom_pl="Werbegrafikerinnen", status="Spezialisten"
            ),
        ],
        [
            Noun(
                "m",
                "Modezeichner",
                "Modezeichners",
                nom_pl="Modezeichner",
                status="Spezialisten",
            ),
            Noun(
                "f", "Modezeichnerin", nom_pl="Modezeichnerinnen", status="Spezialisten"
            ),
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
        [
            Noun(
                "m",
                "Fotojournalist",
                "Fotojournalisten",
                nom_pl="Fotojournalisten",
                status="Spezialisten",
            ),
            Noun(
                "f", "Fotojournalistin", nom_pl="Fotojournalistinnen", status="Spezialisten"
            ),
        ],
    ],
    234: [
        [
            Noun(
                "m",
                "Medieningenieur",
                "Medieningenieurs",
                nom_pl="Medieningenieure",
                status="Experten",
            ),
            Noun(
                "f",
                "Medieningenieurin",
                nom_pl="Medieningenieurinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m",
                "Druckereiarbeiter",
                "Druckereiarbeiters",
                nom_pl="Druckereiarbeiter",
                status="Helfer",
            ),
            Noun(
                "f",
                "Druckereiarbeiterin",
                nom_pl="Druckereiarbeiterinnen",
                status="Helfer",
            ),
        ],
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
        [
            Noun(
                "m",
                "Buchrestaurator",
                "Buchrestaurators",
                nom_pl="Buchrestauratoren",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Buchrestauratorin",
                nom_pl="Buchrestauratorinnen",
                status="Spezialisten",
            ),
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
            Noun(
                "f", "Stahlarbeiterin", nom_pl="Stahlarbeiterinnen", status="Fachkraefte"
            ),
        ],
        [
            Noun(
                "m",
                "Gusstechniker",
                "Gusstechnikers",
                nom_pl="Gusstechniker",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Gusstechnikerin",
                nom_pl="Gusstechnikerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    242: [
        [
            Noun(
                "m",
                "Zerspanungsmechaniker",
                "Zerspanungsmechanikers",
                nom_pl="Zerspanungsmechaniker",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Zerspanungsmechanikerin",
                nom_pl="Zerspanungsmechanikerinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "m",
                "Metallarbeiter",
                "Metallarbeiters",
                nom_pl="Metallarbeiter",
                status="Helfer",
            ),
            Noun(
                "f", "Metallarbeiterin", nom_pl="Metallarbeiterinnen", status="Helfer"
            ),
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
            Noun(
                "f", "Metallfärberin", nom_pl="Metallfärberinnen", status="Fachkraefte"
            ),
        ],
    ],
    244: [
        [
            Noun(
                "m",
                "Stahlbauingenieur",
                "Stahlbauingenieurs",
                nom_pl="Stahlbauingenieure",
                status="Experten",
            ),
            Noun(
                "f",
                "Stahlbauingenieurin",
                nom_pl="Stahlbauingenieurinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m", "Schlosser", "Schlossers", nom_pl="Schlosser", status="Fachkraefte"
            ),
            Noun("f", "Schlosserin", nom_pl="Schlosserinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m", "Schmied", "Schmiedes", nom_pl="Schmiede", status="Fachkraefte"
            ),
            Noun("f", "Schmiedin", nom_pl="Schmiedinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m", "Stahlbauer", "Stahlbauers", nom_pl="Stahlbauer", status="Fachkraefte"
            ),
            Noun("f", "Stahlbauerin", nom_pl="Stahlbauerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Dockarbeiter",
                "Dockarbeiters",
                nom_pl="Dockarbeiter",
                status="Helfer",
            ),
            Noun("f", "Dockarbeiterin", nom_pl="Dockarbeiterinnen", status="Helfer"),
        ],
        [
            Noun(
                "m",
                "Schweißfachmann",
                "Schweißfachmanns",
                nom_pl="Schweißfachmänner",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Schweißfachfrau",
                nom_pl="Schweißfachfrauen",
                status="Spezialisten",
            ),
            Noun("f", "Schweißfachkraft", status="Spezialisten", pronouns="dey"),
        ],
    ],
    245: [
        [
            Noun(
                "m",
                "Waffeningenieur",
                "Waffeningenieurs",
                nom_pl="Waffeningenieure",
                status="Experten",
            ),
            Noun(
                "f",
                "Waffeningenieurin",
                nom_pl="Waffeningenieurinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m",
                "Werkzeugmechaniker",
                "Werkzeugmechanikers",
                nom_pl="Werkzeugmechaniker",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Werkzeugmechanikerin",
                nom_pl="Werkzeugmechanikerinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "m",
                "Gerätetechniker",
                "Gerätetechnikers",
                nom_pl="Gerätetechniker",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Gerätetechnikerin",
                nom_pl="Gerätetechnikerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    251: [
        [
            Noun(
                "m",
                "Serviceingenieur",
                "Serviceingenieurs",
                nom_pl="Serviceingenieure",
                status="Experten",
            ),
            Noun(
                "f",
                "Serviceingenieurin",
                nom_pl="Serviceingenieurinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m",
                "Industriemechaniker",
                "Industriemechanikers",
                nom_pl="Industriemechaniker",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Industriemechanikerin",
                nom_pl="Industriemechanikerinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "m",
                "Betriebstechniker",
                "Betriebstechnikers",
                nom_pl="Betriebstechniker",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Betriebstechnikerin",
                nom_pl="Betriebstechnikerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    252: [
        [
            Noun(
                "m",
                "Luftfahrtingenieur",
                "Luftfahrtingenieurs",
                nom_pl="Luftfahrtingenieure",
                status="Experten",
            ),
            Noun(
                "f",
                "Luftfahrtingenieurin",
                nom_pl="Luftfahrtingenieurinnen",
                status="Experten",
            ),
        ],
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
                "Fahrzeugtechniker",
                "Fahrzeugtechnikers",
                nom_pl="Fahrzeugtechniker",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Fahrzeugtechnikerin",
                nom_pl="Fahrzeugtechnikerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    261: [
        [
            Noun(
                "m",
                "Messingenieur",
                "Messingenieurs",
                nom_pl="Messingenieure",
                status="Experten",
            ),
            Noun(
                "f", "Messingenieurin", nom_pl="Messingenieurinnen", status="Experten"
            ),
        ],
        [
            Noun(
                "m",
                "Mechatroniker",
                "Mechatronikers",
                nom_pl="Mechatroniker",
                status="Fachkraefte",
            ),
            Noun(
                "f", "Mechatronikerin", nom_pl="Mechatronikerinnen", status="Fachkraefte"
            ),
        ],
        [
            Noun(
                "m",
                "Roboterprogrammierer",
                "Roboterprogrammierers",
                nom_pl="Roboterprogrammierer",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Roboterprogrammiererin",
                nom_pl="Roboterprogrammiererinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "m",
                "Schalttechniker",
                "Schalttechnikers",
                nom_pl="Schalttechniker",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Schalttechnikerin",
                nom_pl="Schalttechnikerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    262: [
        [
            Noun(
                "m",
                "Windparkmanager",
                "Windparkmanagers",
                nom_pl="Windparkmanager",
                status="Experten",
            ),
            Noun(
                "f",
                "Windparkmanagerin",
                nom_pl="Windparkmanagerinnen",
                status="Experten",
            ),
        ],
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
                "Kabelleger",
                "Kabellegers",
                nom_pl="Kabelleger",
                status="Fachkraefte",
            ),
            Noun("f", "Kabellegerin", nom_pl="Kabellegerinnen", status="Fachkraefte"),
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
                "Chipentwickler",
                "Chipentwicklers",
                nom_pl="Chipentwickler",
                status="Experten",
            ),
            Noun(
                "f",
                "Chipentwicklerin",
                nom_pl="Chipentwicklerinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m",
                "PC-Techniker",
                "PC-Technikers",
                nom_pl="PC-Techniker",
                status="Fachkraefte",
            ),
            Noun(
                "f", "PC-Technikerin", nom_pl="PC-Technikerinnen", status="Fachkraefte"
            ),
        ],
        [
            Noun(
                "m",
                "Elektroniktechniker",
                "Elektroniktechnikers",
                nom_pl="Elektroniktechniker",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Elektroniktechnikerin",
                nom_pl="Elektroniktechnikerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    271: [
        [
            Noun(
                "m",
                "Forschungsgruppenleiter",
                "Forschungsgruppenleiters",
                nom_pl="Forschungsgruppenleiter",
                status="Experten",
            ),
            Noun(
                "f",
                "Forschungsgruppenleiterin",
                nom_pl="Forschungsgruppenleiterinnen",
                status="Experten",
            ),
            Noun("f", "Forschungsgruppenleitung", status="Experten", pronouns="dey"),
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
        [
            Noun(
                "m",
                "Entwickler",
                "Entwicklers",
                nom_pl="Entwickler",
                status="Spezialisten",
            ),
            Noun("f", "Entwicklerin", nom_pl="Entwicklerinnen", status="Spezialisten"),
        ],
    ],
    272: [
        [
            Noun(
                "m",
                "Sportingenieur",
                "Sportingenieurs",
                nom_pl="Sportingenieure",
                status="Experten",
            ),
            Noun(
                "f", "Sportingenieurin", nom_pl="Sportingenieurinnen", status="Experten"
            ),
        ],
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
                "Werkzeugprüfer",
                "Werkzeugprüfers",
                nom_pl="Werkzeugprüfer",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Werkzeugprüferin",
                nom_pl="Werkzeugprüferinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "m",
                "Planungsökonom",
                "Planungsökonomen",
                "Planungsökonomen",
                "Planungsökonomen",
                nom_pl="Planungsökonomen",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Planungsökonomin",
                nom_pl="Planungsökonominnen",
                status="Spezialisten",
            ),
        ],
    ],
    281: [
        [
            Noun(
                "m",
                "Textildesigner",
                "Textildesigners",
                nom_pl="Textildesigner",
                status="Experten",
            ),
            Noun(
                "f", "Textildesignerin", nom_pl="Textildesignerinnen", status="Experten"
            ),
        ],
        [
            Noun(
                "m",
                "Teppichknüpfer",
                "Teppichknüpfers",
                nom_pl="Teppichknüpfer",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Teppichknüpferin",
                nom_pl="Teppichknüpferinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "m",
                "Textilformer",
                "Textilformers",
                nom_pl="Textilformer",
                status="Helfer",
            ),
            Noun("f", "Textilformerin", nom_pl="Textilformerinnen", status="Helfer"),
        ],
    ],
    282: [
        [
            Noun(
                "m",
                "Modedesigner",
                "Modedesigners",
                nom_pl="Modedesigner",
                status="Experten",
            ),
            Noun(
                "f",
                "Modedesignerin",
                nom_pl="Modedesignerinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m",
                "Modeschneider",
                "Modeschneiders",
                nom_pl="Modeschneider",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Modeschneiderin",
                nom_pl="Modeschneiderinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "m", "Hutmacher", "Hutmachers", nom_pl="Hutmacher", status="Fachkraefte"
            ),
            Noun("f", "Hutmacherin", nom_pl="Hutmacherinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Stylist",
                "Stylisten",
                "Stylisten",
                "Stylisten",
                nom_pl="Stylisten",
                status="Spezialisten",
            ),
            Noun("f", "Stylistin", nom_pl="Stylistinnen", status="Spezialisten"),
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
                "Lebensmittelingenieur",
                "Lebensmittelingenieurs",
                nom_pl="Lebensmittelingenieure",
                status="Experten",
            ),
            Noun(
                "f",
                "Lebensmittelingenieurin",
                nom_pl="Lebensmittelingenieurinnen",
                status="Experten",
            ),
        ],
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
    ],
    293: [
        [
            Noun("m", "Koch", "Kochs", nom_pl="Köche", status="Fachkraefte"),
            Noun("f", "Köchin", nom_pl="Köchinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "f",
                "Küchenhilfe",
                nom_pl="Küchenhilfen",
                pronouns="er",
                status="Helfer",
            ),
            Noun(
                "f",
                "Küchenhilfe",
                nom_pl="Küchenhilfen",
                pronouns="sie",
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
            Noun(
                "m", "Raumplaner", "Raumplaners", nom_pl="Raumplaner", status="Experten"
            ),
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
                "Dackdeckers",
                nom_pl="Dachdecker",
                dat_pl="Dachdeckern",
                status="Fachkraefte",
            ),
            Noun("f", "Dachdeckerin", nom_pl="Dachdeckerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Bauwerker",
                "Bauwerkers",
                nom_pl="Bauwerker",
                dat_pl="Bauwerkern",
                status="Helfer",
            ),
            Noun("f", "Bauwerkerin", nom_pl="Bauwerkerinnen", status="Helfer"),
        ],
    ],
    322: [
        [
            Noun(
                "m",
                "Straßenbauingenieur",
                "Straßenbauingenieurs",
                nom_pl="Straßenbauingenieure",
                dat_pl="Straßenbauingenieuren",
                status="Experten",
            ),
            Noun(
                "f",
                "Straßenbauingenieurin",
                nom_pl="Straßenbauingenieurinnen",
                status="Experten",
            ),
        ],
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
                "Straßenarbeiter",
                "Straßenarbeiters",
                nom_pl="Straßenarbeiter",
                dat_pl="Straßenarbeitern",
                status="Helfer",
            ),
            Noun(
                "f", "Straßenarbeiterin", nom_pl="Straßenarbeiterinnen", status="Helfer"
            ),
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
            Noun(
                "f", "Fliesenlegerin", nom_pl="Fliesenlegerinnen", status="Fachkraefte"
            ),
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
                "Stuckateur",
                "Stuckateurs",
                nom_pl="Stuckateure",
                dat_pl="Stuckateuren",
                status="Spezialisten",
            ),
            Noun("f", "Stuckateurin", nom_pl="Stuckateurinnen", status="Spezialisten"),
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
        [
            Noun(
                "m",
                "Zimmerer",
                "Zimmerers",
                nom_pl="Zimmerer",
                dat_pl="Zimmerern",
                status="Fachkraefte",
            ),
            Noun("f", "Zimmerin", nom_pl="Zimmerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Restaurator",
                "Restaurators",
                nom_pl="Restauratoren",
                dat_pl="Restauratoren",
                status="Spezialisten",
            ),
            Noun(
                "f", "Restauratorin", nom_pl="Restauratorinnen", status="Spezialisten"
            ),
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
                "Gebäudetechniker",
                "Gebäudetechnikers",
                nom_pl="Gebäudetechniker",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Gebäudetechnikerin",
                nom_pl="Gebäudetechnikerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    342: [
        [
            Noun(
                "m",
                "Klimaingenieur",
                "Klimaingenieurs",
                nom_pl="Klimaingenieure",
                dat_pl="Klimaingenieuren",
                status="Experten",
            ),
            Noun(
                "f", "Klimaingenieurin", nom_pl="Klimaingenieurinnen", status="Experten"
            ),
        ],
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
            Noun(
                "m",
                "Sanitäringenieur",
                "Sanitäringenieurs",
                nom_pl="Sanitäringenieure",
                dat_pl="Sanitäringenieuren",
                status="Experten",
            ),
            Noun(
                "f",
                "Sanitäringenieurin",
                nom_pl="Sanitäringenieurinnen",
                status="Experten",
            ),
        ],
        [
            Noun("m", "Rohrbauer", "Rohrbauers", nom_pl="Rohrbauer", status="Fachkraefte"),
            Noun("f", "Rohrbauerin", nom_pl="Rohrbauerinnen", status="Fachkraefte"),
        ],
        [
            Noun("m", "Müllmann", "Müllmanns", nom_pl="Müllmänner", status="Helfer"),
            Noun("f", "Müllfrau", nom_pl="Müllfrauen", status="Helfer"),
        ],
        [
            Noun(
                "m",
                "Anlagentechniker",
                "Anlagentechnikers",
                nom_pl="Anlagentechniker",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Anlagentechnikerin",
                nom_pl="Anlagentechnikerinnen",
                status="Spezialisten",
            ),
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
        [
            Noun(
                "m",
                "Statistiker",
                "Statistikers",
                nom_pl="Statistiker",
                status="Experten",
            ),
            Noun("f", "Statistikerin", nom_pl="Statistikerinnen", status="Experten"),
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
                "Biologielaborant",
                "Biologielaboranten",
                "Biologielaboranten",
                "Biologielaboranten",
                nom_pl="Biologielaboranten",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Biologielaborantin",
                nom_pl="Biologielaborantinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "m",
                "Biotechniker",
                "Biotechnikers",
                nom_pl="Biotechniker",
                status="Spezialisten",
            ),
            Noun(
                "f", "Biotechnikerin", nom_pl="Biotechnikerinnen", status="Spezialisten"
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
                "Astronom",
                "Astronomen",
                "Astronomen",
                "Astronomen",
                nom_pl="Astronomen",
                status="Experten",
            ),
            Noun("f", "Astronomin", nom_pl="Astronominnen", status="Experten"),
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
        ],
    ],
    433: [
        [
            Noun(
                "m", "Netzplaner", "Netzplaners", nom_pl="Netzplaner", status="Experten"
            ),
            Noun("f", "Netzplanerin", nom_pl="Netzplanerinnen", status="Experten"),
        ],
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
        [
            Noun(
                "m",
                "Data-Analyst",
                "Data-Analysten",
                "Data-Analysten",
                "Data-Analysten",
                nom_pl="Data-Analysten",
                status="Spezialisten",
            ),
            Noun(
                "f", "Data-Analystin", nom_pl="Data-Analystinnen", status="Spezialisten"
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
                "Fachinformatiker",
                "Fachinformatikers",
                nom_pl="Fachinformatiker",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Fachinformatikerin",
                nom_pl="Fachinformatikerinnen",
                status="Fachkraefte",
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
                "Schiffsoffizier",
                "Schiffsoffiziers",
                nom_pl="Schiffsoffiziere",
                status="Experten",
            ),
            Noun(
                "f",
                "Schiffsoffizierin",
                nom_pl="Schiffsoffizierinnen",
                status="Experten",
            ),
        ],
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
        [
            Noun("m", "Funker", "Funkers", nom_pl="Funker", status="Fachkraefte"),
            Noun("f", "Funkerin", nom_pl="Funkerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Funkmeister",
                "Funkmeisters",
                nom_pl="Funkmeister",
                status="Spezialisten",
            ),
            Noun(
                "f", "Funkmeisterin", nom_pl="Funkmeisterinnen", status="Spezialisten"
            ),
        ],
    ],
    512: [
        [
            Noun(
                "m",
                "Streckenwärter",
                "Streckenwärters",
                nom_pl="Streckenwärter",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Streckenwärterin",
                nom_pl="Streckenwärterinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "m",
                "Sicherungsposten",
                nom_pl="Sicherungsposten",
                pronouns="er",
                status="Fachkraefte",
            ),
            Noun(
                "m",
                "Sicherungsposten",
                nom_pl="Sicherungsposten",
                pronouns="sie",
                status="Fachkraefte",
            ),
            Noun(
                "m",
                "Sicherungsposten",
                nom_pl="Sicherungsposten",
                pronouns="dey",
                status="Fachkraefte",
            ),
        ],
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
                "Briefträger",
                "Briefträgers",
                nom_pl="Briefträger",
                status="Fachkraefte",
            ),
            Noun("f", "Briefträgerin", nom_pl="Briefträgerinnen", status="Fachkraefte"),
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
    ],
    514: [
        [
            Noun(
                "m", "Schaffner", "Schaffners", nom_pl="Schaffner", status="Fachkraefte"
            ),
            Noun("f", "Schaffnerin", nom_pl="Schaffnerinnen", status="Fachkraefte"),
        ],
        [
            Noun("m", "Steward", "Stewards", nom_pl="Stewards", status="Fachkraefte"),
            Noun("f", "Stewardess", nom_pl="Stewardessen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Flugbegleiter",
                "Flugbegleiters",
                nom_pl="Flugbegleiter",
                status="Helfer",
            ),
            Noun("f", "Flugbegleiterin", nom_pl="Flugbegleiterinnen", status="Helfer"),
            Noun(
                "f",
                "Flugbegleitung",
                nom_pl="Flugbegleitungen",
                status="Helfer",
                pronouns="dey",
            ),
        ],
    ],
    515: [
        [
            Noun(
                "m",
                "Verkehrsplaner",
                "Verkehrsplaners",
                nom_pl="Verkehrsplaner",
                status="Experten",
            ),
            Noun(
                "f", "Verkehrsplanerin", nom_pl="Verkehrsplanerinnen", status="Experten"
            ),
        ],
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
            Noun(
                "m", "Logistiker", "Logistikers", nom_pl="Logistiker", status="Experten"
            ),
            Noun("f", "Logistikerin", nom_pl="Logistikerinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Spediteur",
                "Spediteurs",
                nom_pl="Spediteure",
                status="Spezialisten",
            ),
            Noun("f", "Spediteurin", nom_pl="Spediteurinnen", status="Spezialisten"),
        ],
    ],
    521: [
        [
            Noun(
                "m", "Chauffeur", "Chauffeurs", nom_pl="Chauffeure", status="Fachkraefte"
            ),
            Noun("f", "Chauffeurin", nom_pl="Chauffeurinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m", "Busfahrer", "Busfahrers", nom_pl="Busfahrer", status="Fachkraefte"
            ),
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
                "Fahrradkurier",
                "Fahrradkuriers",
                nom_pl="Fahrradkuriere",
                status="Fachkraefte",
            ),
            Noun(
                "f", "Fahrradkurierin", nom_pl="Fahrradkurierinnen", status="Fachkraefte"
            ),
        ],
    ],
    522: [
        [
            Noun(
                "m", "Lokführer", "Lokführers", nom_pl="Lokführer", status="Fachkraefte"
            ),
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
            Noun(
                "f", "Ballonfahrerin", nom_pl="Ballonfahrerinnen", status="Spezialisten"
            ),
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
                "Binnenschiffer",
                "Binnenschiffers",
                nom_pl="Binnenschiffer",
                status="Fachkraefte",
            ),
            Noun("f", "Binnenschifferin", nom_pl="Binnenschifferin", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Bootsführer",
                "Bootsführers",
                nom_pl="Bootsführer",
                status="Spezialisten",
            ),
            Noun(
                "f", "Bootsführerin", nom_pl="Bootsführerinnen", status="Spezialisten"
            ),
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
            Noun(
                "m", "Fahrprüfer", "Fahrprüfers", nom_pl="Fahrprüfer", status="Experten"
            ),
            Noun("f", "Fahrprüferin", nom_pl="Fahrprüferinnen", status="Experten"),
        ],
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
            Noun(
                "m",
                "Rettungsschwimmer",
                "Rettungsschwimmers",
                nom_pl="Rettungsschwimmer",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Rettungsschwimmerin",
                nom_pl="Rettungsschwimmerinnen",
                status="Fachkraefte",
            ),
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
            Noun(
                "m",
                "Museumswärter",
                "Museumswärters",
                nom_pl="Museumswärter",
                status="Helfer",
            ),
            Noun("f", "Museumswärterin", nom_pl="Museumswärterinnen", status="Helfer"),
        ],
        [
            Noun("m", "Türsteher", "Türstehers", nom_pl="Türsteher", status="Helfer"),
            Noun("f", "Türsteherin", nom_pl="Türsteherinnen", status="Helfer"),
        ],
        [
            Noun(
                "m",
                "Brandschutztechniker",
                "Brandschutztechnikers",
                nom_pl="Brandschutztechniker",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Brandschutztechnikerin",
                nom_pl="Brandschutztechnikerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    532: [
        [
            Noun(
                "m",
                "Kriminalpolizist",
                "Kriminalpolizisten",
                "Kriminalpolizisten",
                "Kriminalpolizisten",
                nom_pl="Kriminalpolizisten",
                status="Experten",
            ),
            Noun(
                "f",
                "Kriminalpolizistin",
                nom_pl="Kriminalpolizistinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m",
                "Verkehrspolizist",
                "Verkehrspolizisten",
                "Verkehrspolizisten",
                "Verkehrspolizisten",
                nom_pl="Verkehrspolizisten",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Verkehrspolizistin",
                nom_pl="Verkehrspolizistinnen",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "m",
                "Justizwachtmeister",
                "Justizwachtmeisters",
                nom_pl="Justizwachtmeister",
                status="Helfer",
            ),
            Noun(
                "f",
                "Justizwachtmeisterin",
                nom_pl="Justizwachtmeisterinnen",
                status="Helfer",
            ),
        ],
        [
            Noun(
                "m",
                "Gerichtsvollzieher",
                "Gerichtsvollziehers",
                nom_pl="Gerichtsvollzieher",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Gerichtsvollzieherin",
                nom_pl="Gerichtsvollzieherinnen",
                status="Spezialisten",
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
        [
            Noun(
                "m",
                "Hygieneinspektor",
                "Hygieneinspektors",
                nom_pl="Hygieneinspektoren",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Hygieneinspektorin",
                nom_pl="Hygieneinspektorinnen",
                status="Spezialisten",
            ),
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
            Noun("f", "Putzhilfe", nom_pl="Putzhilfen", pronouns="er", status="Helfer"),
            Noun(
                "f", "Putzhilfe", nom_pl="Putzhilfen", pronouns="sie", status="Helfer"
            ),
            Noun(
                "f", "Putzhilfe", nom_pl="Putzhilfen", pronouns="dey", status="Helfer"
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
        ],
    ],
    611: [
        [
            Noun("m", "Pfandleiher", "Pfandleihers", nom_pl="Pfandleiher", status="Fachkraefte"),
            Noun("f", "Pfandleiherin", nom_pl="Pfandleiherinnen", status="Fachkraefte"),
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
    ],
    621: [
        [
            Noun(
                "m", "Verkäufer", "Verkäufers", nom_pl="Verkäufer", status="Fachkraefte"
            ),
            Noun("f", "Verkäuferin", nom_pl="Verkäuferinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m", "Kassierer", "Kassierers", nom_pl="Kassierer", status="Fachkraefte"
            ),
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
            Noun(
                "f", "Regalauffüllerin", nom_pl="Regalauffüllerinnen", status="Helfer"
            ),
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
            Noun(
                "f", "Gemüsehändlerin", nom_pl="Gemüsehändlerinnen", status="Fachkraefte"
            ),
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
                "Drogist",
                "Drogisten",
                "Drogisten",
                "Drogisten",
                nom_pl="Drogisten",
                status="Fachkraefte",
            ),
            Noun("f", "Drogistin", nom_pl="Drogistinnen", status="Fachkraefte"),
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
        [
            Noun(
                "m",
                "Galerist",
                "Galeristen",
                "Galeristen",
                "Galeristen",
                nom_pl="Galeristen",
                status="Fachkraefte",
            ),
            Noun("f", "Galeristin", nom_pl="Galeristinnen", status="Fachkraefte"),
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
        [
            Noun(
                "m",
                "Fremdenführer",
                "Fremdenführers",
                nom_pl="Fremdenführer",
                status="Spezialisten",
            ),
            Noun(
                "f", "Fremdenführerin", nom_pl="Fremdenführinnen", status="Spezialisten"
            ),
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
            Noun(
                "f", "Rezeptionistin", nom_pl="Rezeptionistinnen", status="Fachkraefte"
            ),
        ],
        [
            Noun("f", "Empfangskraft", nom_pl="Empfangskräfte", pronouns="er", status="Helfer"),
            Noun(
                "f", "Empfangskraft", nom_pl="Empfangskräfte", pronouns="sie", status="Helfer"
            ),
            Noun(
                "f", "Empfangskraft", nom_pl="Empfangskräfte", pronouns="dey", status="Helfer"
            ),
        ],
        [
            Noun(
                "m",
                "Hotelbetriebswirt",
                "Hotelbetriebswirts",
                nom_pl="Hotelbetriebswirte",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Hotelbetriebswirtin",
                nom_pl="Hotelbetriebswirtinnen",
                status="Spezialisten",
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
                "m", "Barkeeper", "Barkeepers", nom_pl="Barkeeper", status="Fachkraefte"
            ),
            Noun("f", "Barkeeperin", nom_pl="Barkeeperinnen", status="Fachkraefte"),
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
        [
            Noun(
                "m",
                "Weinkellner",
                "Weinkellners",
                nom_pl="Weinkellner",
                status="Spezialisten",
            ),
            Noun(
                "f", "Weinkellnerin", nom_pl="Weinkellnerinnen", status="Spezialisten"
            ),
        ],
    ],
    634: [
        [
            Noun(
                "m",
                "Kulturmanager",
                "Kulturmanagers",
                nom_pl="Kulturmanager",
                status="Experten",
            ),
            Noun(
                "f", "Kulturmanagerin", nom_pl="Kulturmanagerinnen", status="Experten"
            ),
        ],
        [
            Noun(
                "m",
                "Veranstaltungskaufmann",
                "Veranstaltungskaufmanns",
                nom_pl="Veranstaltungskaufmänner",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Veranstaltungskauffrau",
                nom_pl="Veranstaltungskauffrauen",
                status="Fachkraefte",
            ),
        ],
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
            Noun(
                "f", "Eventmanagerin", nom_pl="Eventmanagerinnen", status="Spezialisten"
            ),
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
            Noun(
                "f", "Bürgermeisterin", nom_pl="Bürgermeisterinnen", status="Experten"
            ),
            Noun("n", "Stadtoberhaupt", status="Experten", pronouns="dey"),
        ],
    ],
    713: [
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
            Noun(
                "m",
                "Dolmetscher",
                "Dolmetschers",
                nom_pl="Dolmetscher",
                status="Experten",
            ),
            Noun("f", "Dolmetscherin", nom_pl="Dolmetscherinnen", status="Experten"),
        ],
        [
            Noun("m", "Sekretär", "Sekretärs", nom_pl="Sekretäre", status="Fachkraefte"),
            Noun("f", "Sekretärin", nom_pl="Sekretärinnen", status="Fachkraefte"),
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
            Noun(
                "f", "Chefsekretärin", nom_pl="Chefsekretärinnen", status="Spezialisten"
            ),
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
        [
            Noun(
                "m",
                "Recruiter",
                "Recruiters",
                nom_pl="Recruiter",
                status="Spezialisten",
            ),
            Noun("f", "Recruiterin", nom_pl="Recruiterinnen", status="Spezialisten"),
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
                "Bankangestellter",
                "Bankangestellten",
                "Bankangestellten",
                "Bankangestellten",
                nom_pl="Bankangestellte",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Bankangestellte",
                "Bankangestellten",
                nom_pl="Bankangestellten",
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
            Noun(
                "f", "Börsenmaklerin", nom_pl="Börsenmaklerinnen", status="Spezialisten"
            ),
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
            Noun(
                "f", "Steuerberaterin", nom_pl="Steuerberaterinnen", status="Experten"
            ),
        ],
        [
            Noun(
                "m",
                "Steuerfachangestellter",
                "Steuerfachangestellten",
                "Steuerfachangestellten",
                "Steuerfachangestellten",
                nom_pl="Steuerfachangestellte",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Steuerfachangestellte",
                "Steuerfachangestellten",
                nom_pl="Steuerfachangestellten",
                status="Fachkraefte",
            ),
        ],
        [
            Noun(
                "m",
                "Steuerfachmann",
                "Steuerfachmanns",
                acc_sg="Steuerfachmann",
                dat_sg="Steuerfachmann",
                nom_pl="Steuerfachmänner",
                status="Spezialisten",
            ),
            Noun(
                "f", "Steuerfachfrau", nom_pl="Steuerfachfrauen", status="Spezialisten"
            ),
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
        [
            Noun(
                "m",
                "Datenschutzbeauftragter",
                "Datenschutzbeauftragten",
                "Datenschutzbeauftragten",
                "Datenschutzbeauftragten",
                nom_pl="Datenschutzbeauftragte",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Datenschutzbeauftragte",
                "Datenschutzbeauftragten",
                "Datenschutzbeauftragten",
                "Datenschutzbeauftragte",
                nom_pl="Datenschutzbeauftragten",
                status="Spezialisten",
            ),
        ],
    ],
    732: [
        [
            Noun(
                "m",
                "Kulturreferent",
                "Kulturreferenten",
                "Kulturreferenten",
                "Kulturreferenten",
                nom_pl="Kulturreferenten",
                status="Experten",
            ),
            Noun("f", "Kulturreferentin", nom_pl="Kulturreferentinnen", status="Experten"),
        ],
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
                "Gemeindediener",
                "Gemeindedieners",
                nom_pl="Gemeindediener",
                status="Helfer",
            ),
            Noun(
                "f", "Gemeindedienerin", nom_pl="Gemeindedienerinnen", status="Helfer"
            ),
        ],
        [
            Noun(
                "m",
                "Rechtspfleger",
                "Rechtspflegers",
                nom_pl="Rechtspfleger",
                status="Spezialisten",
            ),
            Noun(
                "f", "Rechtspflegerin", nom_pl="Rechtspflegerinnen", status="Spezialisten"
            ),
        ],
    ],
    733: [
        [
            Noun(
                "m",
                "Aktenverwalter",
                "Aktenverwalters",
                dat_sg="Aktenverwalter",
                acc_sg="Aktenverwalter",
                nom_pl="Aktenverwalter",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Aktenverwalterin",
                nom_pl="Aktenverwalterinnen",
                status="Fachkraefte",
            ),
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
    ],
    812: [
        [
            Noun(
                "m",
                "Infektologe",
                "Infektologen",
                "Infektologen",
                "Infektologen",
                nom_pl="Infektologen",
                status="Experten",
            ),
            Noun("f", "Infektologin", nom_pl="Infektologinnen", status="Experten"),
        ],
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
            Noun(
                "f", "Pflegeassistentin", nom_pl="Pflegeassistentinnen", status="Helfer"
            ),
            Noun("f", "Pflegeassistenz", status="Helfer", pronouns="dey"),
        ],
        [
            Noun(
                "f", "Hebamme", nom_pl="Hebammen", status="Spezialisten", pronouns="er"
            ),
            Noun(
                "f", "Hebamme", nom_pl="Hebammen", status="Spezialisten", pronouns="sie"
            ),
            Noun(
                "f", "Hebamme", nom_pl="Hebammen", status="Spezialisten", pronouns="dey"
            ),
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
                "Notfallsanitäter",
                "Notfallsanitäters",
                nom_pl="Notfallsanitäter",
                dat_pl="Notfallsanitätern",
                status="Fachkraefte",
            ),
            Noun(
                "f",
                "Notfallsanitäterin",
                nom_pl="Notfallsanitäterinnen",
                status="Fachkraefte",
            ),
        ],
    ],
    814: [
        [
            Noun(
                "m",
                "Hausarzt",
                "Hausarztes",
                nom_pl="Hausärzte",
                dat_pl="Hausärzten",
                acc_pl="Hausärzte",
                status="Experten",
            ),
            Noun("f", "Hausärztin", nom_pl="Hausärztinnen", status="Experten"),
        ],
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
            Noun(
                "f", "Suchttherapeutin", nom_pl="Suchttherapeutinnen", status="Experten"
            ),
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
                status="Experten",
            ),
            Noun(
                "f",
                "Physiotherapeutin",
                nom_pl="Physiotherapeutinnen",
                status="Experten",
            ),
        ],
        [
            Noun(
                "m",
                "Musiktherapeut",
                "Musiktherapeuten",
                "Musiktherapeuten",
                "Musiktherapeuten",
                nom_pl="Musiktherapeuten",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Musiktherapeutin",
                nom_pl="Musiktherapeutinnen",
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
            Noun(
                "f", "Altenpflegerin", nom_pl="Altenpflegerinnen", status="Fachkraefte"
            ),
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
                "Gesundheitscoach",
                "Gesundheitscoachs",
                nom_pl="Gesundheitscoachs",
                dat_pl="Gesundheitscoachs",
                status="Fachkraefte",
                pronouns="er",
            ),
            Noun(
                "m",
                "Gesundheitscoach",
                "Gesundheitscoachs",
                nom_pl="Gesundheitscoachs",
                dat_pl="Gesundheitscoachs",
                status="Fachkraefte",
                pronouns="sie",
            ),
            Noun(
                "m",
                "Gesundheitscoach",
                "Gesundheitscoachs",
                nom_pl="Gesundheitscoachs",
                dat_pl="Gesundheitscoachs",
                status="Fachkraefte",
                pronouns="dey",
            ),
        ],
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
                "Totengräber",
                "Totengräbers",
                nom_pl="Totengräber",
                dat_pl="Totengräbern",
                status="Helfer",
            ),
            Noun("f", "Totengräberin", nom_pl="Totengräberinnen", status="Helfer"),
        ],
        [
            Noun(
                "m",
                "Bestatter",
                "Bestatters",
                nom_pl="Bestatter",
                dat_pl="Bestattern",
                status="Spezialisten",
            ),
            Noun("f", "Bestatterin", nom_pl="Bestatterinnen", status="Spezialisten"),
        ],
    ],
    825: [
        [
            Noun(
                "m",
                "Augenoptiker",
                "Augenoptikers",
                nom_pl="Augenoptiker",
                dat_pl="Augenoptikern",
                status="Fachkraefte",
            ),
            Noun("f", "Augenoptikerin", nom_pl="Augenoptikerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Zahntechniker",
                "Zahntechnikers",
                nom_pl="Zahntechniker",
                dat_pl="Zahntechnikern",
                status="Fachkraefte",
            ),
            Noun(
                "f", "Zahntechnikerin", nom_pl="Zahntechnikerinnen", status="Fachkraefte"
            ),
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
            Noun(
                "f", "Jugendberaterin", nom_pl="Jugendberaterinnen", status="Experten"
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
                "m",
                "Tagesvater",
                "Tagesvaters",
                nom_pl="Tagesväter",
                dat_pl="Tagesvätern",
                status="Helfer",
            ),
            Noun(
                "f", "Tagesmutter", nom_pl="Tagesmütter", status="Helfer"
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
            Noun("f", "Haushaltshilfe", nom_pl="Haushaltshilfen", pronouns="er", status="Helfer"),
            Noun(
                "f", "Haushaltshilfe", nom_pl="Haushaltshilfen", pronouns="sie", status="Helfer"
            ),
            Noun(
                "f", "Haushaltshilfe", nom_pl="Haushaltshilfen", pronouns="dey", status="Helfer"
            ),
        ],
    ],
    833: [
        [
            Noun(
                "m",
                "Priester",
                "Priesters",
                nom_pl="Priester",
                dat_pl="Priestern",
                status="Experten",
            ),
            Noun("f", "Priesterin", nom_pl="Priesterinnen", status="Experten"),
        ],
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
            Noun(
                "f", "Gitarrenlehrerin", nom_pl="Gitarrenlehrerinnen", status="Experten"
            ),
        ],
        [
            Noun(
                "m",
                "Musiklehrer",
                "Musiklehrers",
                nom_pl="Musiklehrer",
                dat_pl="Musiklehrern",
                status="Fachkraefte",
            ),
            Noun("f", "Musiklehrerin", nom_pl="Musiklehrerinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Nachhilfelehrer",
                "Nachhilfelehrers",
                nom_pl="Nachhilfelehrer",
                dat_pl="Nachhilfelehrern",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Nachhilfelehrerin",
                nom_pl="Nachhilfelehrerinnen",
                status="Spezialisten",
            ),
        ],
    ],
    845: [
        [
            Noun(
                "m",
                "Sportwissenschaftler",
                "Sportwissenschaftlers",
                nom_pl="Sportwissenschaftler",
                dat_pl="Sportwissenschaftlern",
                status="Experten",
            ),
            Noun(
                "f",
                "Sportwissenschaftlerin",
                nom_pl="Sportwissenschaftlerinnen",
                status="Experten",
            ),
        ],
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
                "Literaturwissenschaftler",
                "Literaturwissenschaftlers",
                nom_pl="Literaturwissenschaftler",
                status="Experten",
            ),
            Noun(
                "f",
                "Literaturwissenschaftlerin",
                nom_pl="Literaturwissenschaftlerinnen",
                status="Experten",
            ),
        ],
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
            Noun(
                "m",
                "Archäologe",
                "Archäologen",
                "Archäologen",
                "Archäologen",
                nom_pl="Archäologen",
                status="Experten",
            ),
            Noun("f", "Archäologin", nom_pl="Archäologinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Philosoph",
                "Philosophen",
                "Philosophen",
                "Philosophen",
                nom_pl="Philosophen",
                status="Experten",
            ),
            Noun("f", "Philosophin", nom_pl="Philosophinnen", status="Experten"),
        ],
        [
            Noun(
                "m", "Historiker", "Historikers", nom_pl="Historiker", status="Experten"
            ),
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
            Noun(
                "f", "Marktforscherin", nom_pl="Marktforscherinnen", status="Experten"
            ),
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
                "Werbemanager",
                "Werbemanagers",
                nom_pl="Werbemanager",
                status="Experten",
            ),
            Noun("f", "Werbemanagerin", nom_pl="Werbemanagerinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Werbetexter",
                "Werbetexters",
                nom_pl="Werbetexter",
                status="Spezialisten",
            ),
            Noun(
                "f", "Werbetexterin", nom_pl="Werbetexterinnen", status="Spezialisten"
            ),
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
            Noun(
                "f", "Pressesprecherin", nom_pl="Pressesprecherinnen", status="Experten"
            ),
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
            Noun(
                "f", "Literaturagentin", nom_pl="Literaturagentinnen", status="Experten"
            ),
        ],
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
        [
            Noun(
                "m",
                "Verlagsvertreter",
                "Verlagsvertreters",
                nom_pl="Verlagsvertreter",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Verlagsvertreterin",
                nom_pl="Verlagsvertreterinnen",
                status="Spezialisten",
            ),
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
        [
            Noun(
                "m",
                "Karikaturist",
                "Karikaturisten",
                "Karikaturisten",
                "Karikaturisten",
                nom_pl="Karikaturisten",
                acc_pl="Karikaturisten",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Karikaturistin",
                nom_pl="Karikaturistinnen",
                acc_pl="Karikaturistinnen",
                status="Spezialisten",
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
                status="Spezialisten",
            ),
            Noun(
                "f", "Goldschmiedin", nom_pl="Goldschmiedinnen", status="Spezialisten"
            ),
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
            Noun(
                "f", "Klaviespielerin", nom_pl="Klaviespielerinnen", status="Experten"
            ),
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
                "Akrobat",
                "Akrobaten",
                "Akrobaten",
                "Akrobaten",
                nom_pl="Akrobaten",
                status="Spezialisten",
            ),
            Noun("f", "Akrobatin", nom_pl="Akrobatinnen", status="Spezialisten"),
        ],
        [
            Noun(
                "n",
                "Model",
                "Models",
                nom_pl="Models",
                status="Fachkräfte",
                pronouns="er",
            ),
            Noun(
                "n",
                "Model",
                "Models",
                nom_pl="Models",
                status="Fachkräfte",
                pronouns="sie",
            ),
            Noun(
                "n",
                "Model",
                "Models",
                nom_pl="Models",
                status="Fachkräfte",
                pronouns="dey",
            ),
        ],
    ],
    943: [
        [
            Noun(
                "m",
                "Radiomoderator",
                "Radiomoderators",
                nom_pl="Radiomoderatoren",
                status="Experten",
            ),
            Noun(
                "f", "Radiomoderatorin", nom_pl="Radiomoderatorinnen", status="Experten"
            ),
        ],
        [
            Noun(
                "m", "Hellseher", "Hellsehers", nom_pl="Hellseher", status="Fachkraefte"
            ),
            Noun("f", "Hellseherin", nom_pl="Hellseherinnen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m", "Wahrsager", "Wahrsagers", nom_pl="Wahrsager", status="Fachkraefte"
            ),
            Noun("f", "Wahrsagerin", nom_pl="Wahrsagerinnen", status="Fachkraefte"),
        ],
    ],
    944: [
        [
            Noun(
                "m", "Souffleur", "Souffleurs", nom_pl="Souffleure", status="Fachkraefte"
            ),
            Noun("f", "Souffleuse", nom_pl="Souffleusen", status="Fachkraefte"),
        ],
        [
            Noun(
                "m",
                "Regieassistent",
                "Regieassistenten",
                "Regieassistenten",
                "Regieassistenten",
                nom_pl="Regieassistenten",
                status="Spezialisten",
            ),
            Noun(
                "f",
                "Regieassistentin",
                nom_pl="Regieassistentinnen",
                status="Spezialisten",
            ),
            Noun("f", "Regieassistenz", status="Spezialisten", pronouns="dey"),
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
                "m", "Tonmeister", "Tonmeisters", nom_pl="Tonmeister", status="Experten"
            ),
            Noun("f", "Tonmeisterin", nom_pl="Tonmeisterinnen", status="Experten"),
        ],
        [
            Noun(
                "m",
                "Pyrotechniker",
                "Pyrotechnikers",
                nom_pl="Pyrotechniker",
                status="Fachkraefte",
            ),
            Noun(
                "f", "Pyrotechnikerin", nom_pl="Pyrotechnikerinnen", status="Fachkraefte"
            ),
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
                "Kostümbildner",
                "Kostümbildners",
                nom_pl="Kostümbildner",
                status="Experten",
            ),
            Noun(
                "f", "Kostümbildnerin", nom_pl="Kostümbildnerinnen", status="Experten"
            ),
        ],
        [
            Noun(
                "m",
                "Requisiteur",
                "Requisiteurs",
                nom_pl="Requisiteure",
                status="Spezialisten",
            ),
            Noun(
                "f", "Requisiteurin", nom_pl="Requisiteurinnen", status="Spezialisten"
            ),
        ],
    ],
    947: [
        [
            Noun("m", "Kurator", "Kurators", nom_pl="Kuratoren", status="Experten"),
            Noun("f", "Kuratorin", nom_pl="Kuratorinnen", status="Experten"),
        ],
    ],
}
