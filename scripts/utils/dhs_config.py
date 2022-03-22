# Column names for personnal informations
COLUMN_PERSON = [
    "scholing",  # Highest level of education
    "gez1",  # Height (cm)
    "gez3",  # Subjective health (1 - Excellent, 5 - Poor)
    "bmi",  # BMI
]

# Column names for risk questions
COLUMN_RISK = [f"spaar{i+1}" for i in range(6)]

# Column names for psycological questions
COLUMN_PSY = [f"teg{i+1}" for i in range(16)]

# Columns names for other useful information
COLUMN_OTHERS = [
    "nohhold",
    "nomem",
    "year",
    "geslacht",
    "positie",  # Position in the houshold (1 - Head, 2 - Spouse, 3 - Permanent partner)
]  


def get_columns():
    """Returns two sets of columns names (variables, others)
    
    inputs:
        None
    outpus:
        column_variables (list(str)): column names corresponding to
        the features of each person.
        columns_others (list(str)): column names corresponding to other
        important features that would not be use for the model.
    """
    
    column_variables = COLUMN_PERSON + COLUMN_RISK + COLUMN_PSY
    column_others = COLUMN_OTHERS
    
    return column_variables, column_others