# Book Choices
READ = "R"
UNREAD = "U"
TRASH = "T"
READ_CHOICES = [
    (READ, "Read"),
    (UNREAD, "Unread"),
    (TRASH, "Trash"),
]

# Profile - Gender Choices
FEMALE = "F"
MALE = "M"
NONBINARY = "NB"
GENDER_CHOICES = [
    (MALE, "Male"),
    (FEMALE, "Female"),
    (NONBINARY, "Non-Binary"),
]

# Profile - Ethnicity Choices
# In alphabetical order, list shamelessly borrowed from Hinge, noted when changed
AM_IN_FN = "AIFN"
AFRICAN_DESCENT = "BLAD"
EAST_ASIAN = "EA"
HISPANIC = "HL"
MIDDLE_EASTERN = "ME"
PACIFIC_ISLANDER = "PI"
SOUTH_ASIAN = "SA"
SOUTHEAST_ASIAN = "SEA"
WHITE_CAUCASIAN = "WC"
OTHER = "O"
ETHNICITY_CHOICES = [
    (AM_IN_FN, "American Indian/First Nations"), # added First Nations to make the descriptor more inclusive
    (AFRICAN_DESCENT, "Black/African Descent"),
    (EAST_ASIAN, "East Asian")
    (HISPANIC, "Hispanic/Latino"),
    (MIDDLE_EASTERN, "Middle Eastern")
    (PACIFIC_ISLANDER, "Pacific Islander"),
    (SOUTH_ASIAN, "South Asian"),
    (SOUTHEAST_ASIAN, "Southeast Asian"),
    (WHITE_CAUCASIAN, "White/Caucasian"),
    (OTHER, "Other"),
]

# Profile - Religion Choices
# Also shamelessly stolen from Hinge, noted when changed
AGNOSTIC = "AG"
ATHEIST = "A"
BUDDHIST = "B"
CATHOLIC = "CA"
CHRISTIAN = "C"
HINDU = "H"
JEWISH = "J"
MUSLIM = "M"
SIKH = "SK"
SPIRITUAL = "SP"
OTHER = "O"
RELIGION_CHOICES = [
    (AGNOSTIC, "Agnostic"),
    (ATHEIST, "Atheist/None"), #added None to better describe the option
    (BUDDHIST, "Buddhist"),
    (CATHOLIC, "Catholic"),
    (CHRISTIAN, "Christian"),
    (HINDU, "Hindu"),
    (JEWISH, "Jewish"),
    (MUSLIM, "Muslim"),
    (SIKH, "Sikh"),
    (SPIRITUAL, "Spiritual"),
    (OTHER, "Other"),
]