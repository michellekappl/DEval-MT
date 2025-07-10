class Declinable:
    """Base class for declinable objects in German grammar."""

    def decline(self, case: str, number: str) -> str:
        """
        Decline object based on case and number (some declinable objects may need more parameters).
        Default implementation simply gets case and number as an attribute (only implemented like this for nouns).

        Parameters
        ----------
        case : str
            "nom", "gen", "dat", "acc"
        number : str
           "sg" (singular) or "pl" (plural)

        """
        if number == "sg":
            return getattr(self, f"{case}_sg")
        elif number == "pl":
            return getattr(self, f"{case}_pl")
        else:
            raise ValueError("Number must be 'sg' or 'pl'")


class Noun(Declinable):
    """
    Represents a noun.
    """

    def __init__(
        self,
        grammatical_gender: str,
        nom_sg: str,
        gen_sg: str | None = None,
        dat_sg: str | None = None,
        acc_sg: str | None = None,
        nom_pl: str | None = None,
        gen_pl: str | None = None,
        dat_pl: str | None = None,
        acc_pl: str | None = None,
        pronouns: str | None = None,  # "er" "sie" "dey"
        status: str | None = None,
    ):
        """
        Initialize a noun with its grammatical properties.

        If certain cases are not specified, they default to the nominative form of the singular or plural.
        Parameters
        ----------
        grammatical_gender : str
            "m" (masculine), "f" (feminine), "n" (neuter)
        nom_sg : str
        gen_sg : str, optional
        dat_sg : str, optional
        acc_sg : str, optional
        nom_pl : str, optional
        gen_pl : str, optional
        dat_pl : str, optional
        acc_pl : str, optional
        pronouns : str, optional
            "er", "sie", "dey"
            If not provided, defaults to grammatical gender ("er" for masculine, "sie" for feminine, "es" for neuter).
        """
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
    def gender(self) -> str:
        """
        Gender of the noun based on its pronouns, _not_ its grammatical gender.
        "m" (masculine), "f" (feminine), "d" (dey pronouns)
        """
        if self.pronouns:
            lookup = {"er": "m", "sie": "f", "dey": "d"}
            return lookup[self.pronouns]
        else:
            # return grammatical gender if pronouns are not otherwise specified
            return self.grammatical_gender


class Adjective(Declinable):
    """
    Represents an adjective that can be declined based on
    its context within a noun phrase.
    Note that adjectives in german decline not only based on case and number, but also definiteness:
    indeed, we have a tripartite system (which doesn't neatly split for any one combination of case and number)
    which differs based on whether the adjective is used with a definite article, an indefinite article, or no article at all:
        - "der schöne Platz" "ein schöner Platz" "schöner Platz" (masculine singular nominative)
        - "an dem schönen Platz" "an einem schönen Platz" "an schönem Platz" (masculine singular dative)
    """

    def __init__(self, text: str, undeclinable: bool = False):
        """
        Parameters
        ----------
        text : str
            Base form of the adjective.
        undeclinable : bool, optional
            Whether the adjective is undeclinable. Defaults to False. (examples of undeclinable adjectives are "rosa" or "trans")
        """
        self.text = text
        self.undeclinable = undeclinable

    def decline(self, case: str, gender_or_number: str, definite: bool = False) -> str:  # type: ignore
        """
        Decline the adjective based on the case and number.
        Parameters
        ----------
        case : str
            "nom", "gen", "dat", "acc
        gender_or_number : str
            "m", "f", "n" or "pl" (plural)
            Adjective endings do not only depend on number, but also gender of the noun the adjective modifies.
        definite : bool, optional
            Whether the adjective is used with a definite article. Defaults to False. Note that the case for False is unimplemented.
        """
        if definite:
            if self.undeclinable:
                # If the adjective is undeclinable, return it as is
                return self.text
            else:
                endings = {
                    "nom": {"m": "e", "f": "e", "n": "e", "pl": "en"},
                    "gen": {"m": "en", "f": "en", "n": "en", "pl": "en"},
                    "dat": {"m": "en", "f": "en", "n": "en", "pl": "en"},
                    "acc": {"m": "en", "f": "e", "n": "e", "pl": "en"},
                }
                return self.text + endings[case][gender_or_number]
        else:
            raise ValueError("Adjectives without definite article are unimplemented.")


class DefinitePhrase(Declinable):
    """
    Represents a definite noun phrase, which includes a definite article, an optional adjective, and a noun.
    """

    def __init__(self, noun: Noun, adjective: Adjective | None = None):
        """
        Parameters
        ----------
        noun : Noun
            The noun to be declined.
        adjective : Adjective, optional
            The adjective to be declined with the noun. If not provided, the phrase will only consist
            of the definite article and the noun.
        """
        self.noun = noun
        self.adjective = adjective

    def declineArticle(self, case: str, number: str) -> str:
        """
        Get the definite article for the given case and number.
        Parameters
        ----------
        case : str
            "nom", "gen", "dat", "acc"
        number : str
            "sg" (singular) or "pl" (plural)

        """
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
        else:
            raise ValueError("Number must be 'sg' or 'pl'")

    def decline(self, case: str, number: str) -> str:
        if self.adjective:
            # If there is an adjective, we need to decline it as well
            return (
                self.declineArticle(case, number)
                + " "
                + (
                    self.adjective.decline(
                        case, self.noun.grammatical_gender, definite=True
                    )
                    if number == "sg"
                    else self.adjective.decline(case, "pl", definite=True)
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
    """
    Relative pronoun for a given noun. Only depends on grammatical gender of the noun.
    """

    def __init__(self, noun: Noun):
        """
        Parameters
        ----------
        noun : Noun
            The noun for which the relative pronoun is to be formed.
        """
        self.gender = noun.grammatical_gender

    def decline(self, case: str, number: str) -> str:
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
        else:
            raise ValueError("Number must be 'sg' or 'pl'")


class Pronoun(Declinable):
    """
    Represents a personal pronoun for a given noun. Only depends on gender (not grammatical gender) of the noun.
    """

    def __init__(self, noun: Noun):
        self.gender = noun.gender

    def decline(self, case: str, number: str) -> str:
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
        else:
            raise ValueError("Number must be 'sg' or 'pl'")


class Possessive(Declinable):
    """
    Represents a possessive pronoun for a given noun (the possessor),
    taking into account the grammatical gender of the possessed noun.
    (Consider "sein Buch" vs "ihr Buch" vs "seine Zeitung" vs "ihre Zeitung")
    """

    def __init__(self, possessor: Noun, possessed_gender: str):
        """
        Parameters
        ----------
        possessor : Noun
            The noun that possesses something (the possessor).
        possessed_gender : str
            "m", "f", "n", "pl", The grammatical gender of the noun that is possessed.
        """
        self.possessor = possessor
        self.possessed_gender = possessed_gender

    def decline(self, case: str, number: str) -> str:
        """
        Decline the possessive pronoun based on the case and number of the possessed noun.
        Parameters
        ----------
        case : str
            "nom", "gen", "dat", "acc"
        number : str
            "sg" (singular) or "pl" (plural)
        """
        # base depends on the possessor
        base = {"m": "sein", "f": "ihr", "n": "sein", "pl": "ihr"}
        # endings depend on the possessed noun
        endings = {
            "nom": {"m": "", "f": "e", "n": "", "pl": "e"},
            "gen": {"m": "es", "f": "er", "n": "es", "pl": "er"},
            "dat": {"m": "em", "f": "er", "n": "em", "pl": "en"},
            "acc": {"m": "en", "f": "e", "n": "", "pl": "e"},
        }
        if number == "sg":
            if self.possessor.gender == "d":
                # If the possessor uses dey pronouns, we use "deren" for all cases
                return "deren"
            else:
                return (
                    base[self.possessor.gender] + endings[case][self.possessed_gender]
                )
        elif number == "pl":
            return base["pl"] + endings[case][self.possessed_gender]
        else:
            raise ValueError("Number must be 'sg' or 'pl'")


class Name(Declinable):
    """Represents a name that can be declined. Declension is not actually implemented."""

    def __init__(self, text, gender):
        """
        Parameters
        ----------
        text : str
            The name.
        gender : str
            The gender of the name ("m", "f", "d" or "n" for names that can be used for any gender).
        """
        self.text = text
        self.gender = gender

    def decline(self, case: str, number: str) -> str:
        # kind of a hacky solution, since names do have declensions (i.e. Anna, Annas) but this is fine for all of our cases
        # TODO add proper declensions here if needed
        return self.text


# Example usage
mann = Noun("m", "Mann", "Mannes", nom_pl="Männer", dat_pl="Männern")
schoen = Adjective("schön")
trans = Adjective("trans", undeclinable=True)  # Example of an undeclinable adjective
definite_mann = DefinitePhrase(mann)
definite_schoen_mann = DefinitePhrase(mann, schoen)
definite_trans_mann = DefinitePhrase(mann, trans)
possessive_mann = Possessive(mann, "pl")
pronoun_mann = Pronoun(mann)
relative_mann = Relative(mann)
