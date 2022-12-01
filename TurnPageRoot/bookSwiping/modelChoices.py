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

# Book Report - Categories:
ADULT = "A"
INFO = "I"
PIC = "P"
BR_CATEGORY_CHOICES = [
    (ADULT, "Adult Content Visible to Children"),
    (INFO, "Information Missing"),
    (PIC, "Picture Missing"),
]

OPEN = "O"
RESOLVED = "R"
NO_ACTION = "N"
BR_STATUS_CHOICES = [
    (OPEN, "Open"),
    (RESOLVED, "Closed - Resolved"),
    (NO_ACTION, "Closed - No Action Taken"),
]
