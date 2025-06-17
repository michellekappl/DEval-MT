class Declinable:
    def decline(self, case, number):
        if number == "sg":
            return getattr(self, f"{case}_sg", None)
        elif number == "pl":
            return getattr(self, f"{case}_pl", None)
        else:
            raise ValueError("Number must be 'sg' or 'pl'")


class Noun(Declinable):
    def __init__(
        self,
        gender,
        nom_sg,
        gen_sg=None,
        dat_sg=None,
        acc_sg=None,
        nom_pl=None,
        gen_pl=None,
        dat_pl=None,
        acc_pl=None,
        neopronouns=False,
    ):
        self.gender = gender
        self.nom_sg = nom_sg
        self.gen_sg = gen_sg or nom_sg
        self.dat_sg = dat_sg or nom_sg
        self.acc_sg = acc_sg or nom_sg
        self.nom_pl = nom_pl or nom_sg
        self.gen_pl = gen_pl or nom_pl
        self.dat_pl = dat_pl or nom_pl
        self.acc_pl = acc_pl or nom_pl
        self.neopronouns = neopronouns


class Definite(Declinable):
    def __init__(self, noun: Noun):
        self.noun = noun

    def declineArticle(self, case, number):
        dict = {
            "nom": {"m": "der", "f": "die", "n": "das", "pl": "die"},
            "gen": {"m": "des", "f": "der", "n": "des", "pl": "der"},
            "dat": {"m": "dem", "f": "der", "n": "dem", "pl": "den"},
            "acc": {"m": "den", "f": "die", "n": "das", "pl": "die"},
        }
        if number == "sg":
            return dict[case][self.noun.gender]
        elif number == "pl":
            return dict[case]["pl"]

    def decline(self, case, number):
        return self.declineArticle(case, number) + " " + self.noun.decline(case, number)


class Relative(Declinable):
    def __init__(self, noun: Noun):
        self.gender = noun.gender

    def decline(self, case, number):
        dict = {
            "nom": {"m": "der", "f": "die", "n": "das", "pl": "die"},
            "gen": {"m": "dessen", "f": "deren", "n": "dessen", "pl": "deren"},
            "dat": {"m": "dem", "f": "der", "n": "dem", "pl": "denen"},
            "acc": {"m": "den", "f": "die", "n": "das", "pl": "die"},
        }
        if number == "sg":
            return dict[case][self.gender]
        elif number == "pl":
            return dict[case]["pl"]


class Pronoun(Declinable):
    def __init__(self, noun: Noun):
        self.gender = noun.gender
        self.neopronouns = noun.neopronouns

    def decline(self, case, number):
        dict = {
            "nom": {"m": "er", "f": "sie", "n": "es", "neo": "dey", "pl": "sie"},
            "gen": {
                "m": "seiner",
                "f": "ihrer",
                "n": "seiner",
                "neo": "deren",
                "pl": "ihrer",
            },
            "dat": {"m": "ihm", "f": "ihr", "n": "ihm", "neo": "denen", "pl": "ihnen"},
            "acc": {"m": "ihn", "f": "sie", "n": "es", "neo": "dey", "pl": "sie"},
        }
        if number == "sg":
            if self.neopronouns:
                return dict[case]["neo"]
            else:
                return dict[case][self.gender]
        elif number == "pl":
            return dict[case]["pl"]


class Possessive(Declinable):
    def __init__(self, possessor: Noun, possessed):
        self.possessor = possessor
        self.possessed = possessed

    def decline(self, case, number):
        base = {"m": "sein", "f": "ihr", "n": "sein", "pl": "ihr"}
        endings = {
            "nom": {"m": "", "f": "e", "n": "", "pl": "e"},
            "gen": {"m": "es", "f": "er", "n": "es", "pl": "er"},
            "dat": {"m": "em", "f": "er", "n": "em", "pl": "en"},
            "acc": {"m": "en", "f": "e", "n": "", "pl": "e"},
        }

        if number == "sg":
            if self.possessor.neopronouns:
                return "deren"
            else:
                return base[self.possessor.gender] + endings[case][self.possessed]
        elif number == "pl":
            return base["pl"] + endings[case][self.possessed]


# Example usage
mann = Noun("m", "Mann", "Mannes", nom_pl="Männer", dat_pl="Männern", neopronouns=True)
definite_mann = Definite(mann)
possessive_mann = Possessive(mann, "pl")
pronoun_mann = Pronoun(mann)
relative_mann = Relative(mann)
