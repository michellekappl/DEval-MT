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
        grammatical_gender,
        nom_sg,
        gen_sg=None,
        dat_sg=None,
        acc_sg=None,
        nom_pl=None,
        gen_pl=None,
        dat_pl=None,
        acc_pl=None,
        pronouns=None,  # "er" "sie" "dey"
        status=None,
    ):
        self.grammatical_gender = grammatical_gender
        self.nom_sg = nom_sg
        self.gen_sg = gen_sg or nom_sg
        self.dat_sg = dat_sg or nom_sg
        self.acc_sg = acc_sg or nom_sg
        self.nom_pl = nom_pl or nom_sg
        self.gen_pl = gen_pl or nom_pl
        self.dat_pl = dat_pl or nom_pl
        self.acc_pl = acc_pl or nom_pl
        self.pronouns = pronouns
        self.status = status

    @property
    def gender(self):
        if self.pronouns:
            lookup = {"er": "m", "sie": "f", "dey": "n"}
            return lookup[self.pronouns]
        else:
            # return grammatical gender if pronouns are not otherwise specified
            return self.grammatical_gender


class Definite(Declinable):
    def __init__(self, noun: Noun, adjective=None):
        self.noun = noun
        self.adjective = adjective

    def declineArticle(self, case, number):
        dict = {
            "nom": {"m": "der", "f": "die", "n": "das", "pl": "die"},
            "gen": {"m": "des", "f": "der", "n": "des", "pl": "der"},
            "dat": {"m": "dem", "f": "der", "n": "dem", "pl": "den"},
            "acc": {"m": "den", "f": "die", "n": "das", "pl": "die"},
        }
        if number == "sg":
            return dict[case][self.noun.grammatical_gender]
        elif number == "pl":
            return dict[case]["pl"]

    def decline(self, case, number):
        if self.adjective:
            return (
                self.declineArticle(case, number)
                + " "
                + (
                    self.adjective.decline(
                        case, self.noun.grammatical_gender, definite=True
                    )
                    if number == "sg"
                    else self.adjective.decline(case, number, definite=True)
                )
                + " "
                + self.noun.decline(case, number)
            )
        else:
            return (
                self.declineArticle(case, number)
                + " "
                + self.noun.decline(case, number)
            )


class Relative(Declinable):
    def __init__(self, noun: Noun):
        self.gender = noun.grammatical_gender

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

    def decline(self, case, number):
        dict = {
            "nom": {"m": "er", "f": "sie", "n": "es", "d": "dey", "pl": "sie"},
            "gen": {
                "m": "seiner",
                "f": "ihrer",
                "n": "seiner",
                "d": "deren",
                "pl": "ihrer",
            },
            "dat": {"m": "ihm", "f": "ihr", "n": "ihm", "d": "denen", "pl": "ihnen"},
            "acc": {"m": "ihn", "f": "sie", "n": "es", "d": "dey", "pl": "sie"},
        }
        if number == "sg":
            return dict[case][self.gender]
        elif number == "pl":
            return dict[case]["pl"]


class Possessive(Declinable):
    def __init__(self, possessor: Noun, possessed_gender):
        self.possessor = possessor
        self.possessed_gender = possessed_gender

    def decline(self, case, number):
        base = {"m": "sein", "f": "ihr", "n": "sein", "pl": "ihr"}
        endings = {
            "nom": {"m": "", "f": "e", "n": "", "pl": "e"},
            "gen": {"m": "es", "f": "er", "n": "es", "pl": "er"},
            "dat": {"m": "em", "f": "er", "n": "em", "pl": "en"},
            "acc": {"m": "en", "f": "e", "n": "", "pl": "e"},
        }

        if number == "sg":
            if self.possessor.gender == "d":
                return "deren"
            else:
                return (
                    base[self.possessor.gender] + endings[case][self.possessed_gender]
                )
        elif number == "pl":
            return base["pl"] + endings[case][self.possessed_gender]


class Adjective(Declinable):
    def __init__(self, adjective, undeclinable=False):
        self.adjective = adjective
        self.undeclinable = undeclinable

    def decline(self, case, gender_or_number, definite=False):
        if definite:
            if self.undeclinable:
                return self.adjective
            else:
                endings = {
                    "nom": {"m": "e", "f": "e", "n": "e", "pl": "en"},
                    "gen": {"m": "en", "f": "en", "n": "en", "pl": "en"},
                    "dat": {"m": "en", "f": "en", "n": "en", "pl": "en"},
                    "acc": {"m": "en", "f": "e", "n": "e", "pl": "en"},
                }
                return self.adjective + endings[case][gender_or_number]
        else:
            raise ValueError("Adjectives without definite article are unimplemented.")


# Example usage
mann = Noun("m", "Mann", "Mannes", nom_pl="Männer", dat_pl="Männern")
schoen = Adjective("schön")
trans = Adjective("trans", undeclinable=True)  # Example of an undeclinable adjective
definite_mann = Definite(mann)
definite_schoen_mann = Definite(mann, schoen)
definite_trans_mann = Definite(mann, trans)
possessive_mann = Possessive(mann, "pl")
pronoun_mann = Pronoun(mann)
relative_mann = Relative(mann)
