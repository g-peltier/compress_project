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


# Values for the risk questions
SPAAR_VALUES = {'Agree strongly': 7,
              'totally agree': 7,
              '6': 6,
              '5': 5,
              '4': 4,
              '3': 3,
              '2': 2,
              'Disagree strongly': 1,
              'totally disagree': 1}

# High and low values for each psycological question
TEG_QUALITY_LOW = [['oriented towards people'], 
                   ['quick thinker'], 
                   ['easly get worried'], 
                   ['ready to adapt myself, flexible', 'flexible, ready to adapt myself'],
                   ['quiet, calm'],
                   ['lighthearted, carefree', 'carefree'],
                   ['shy'],
                   ['not easily hurt/offended'],
                   ['trusting, credulous'],
                   ['oriented towards reality, down-to-earth', 'oriented towards reality'],
                   ['direct, straightforward'],
                   ['happy with myself'],
                   ['creature of habit'],
                   ['need to be supported by other people', 'need to be supported'],
                   ['little self-control'],
                   ['well-balanced, stable']]

TEG_QUALITY_HIGH = [['oriented towards things'], 
                    ['slow thinker'], 
                    ['not easaly get worried'], 
                    ['stubborn, persistent'],
                    ['lively, vivacious', 'vivid, vivacious'],
                    ['meticulous'],
                    ['dominant'],
                    ['easily hurt/offended, sensitive', 'sensitive, easily hurt/offended'],
                    ['suspicious', "don't trust people easily, suspicious"],
                    ['dreamer'],
                    ['tactful, diplomatic', 'diplomatic, tactful'],
                    ['doubts about myself'],
                    ['open to changes'],
                    ['self-reliant, independent', 'independent, self-reliant'],
                    ['disciplined'],
                    ['irritable, quick-tempered']]


def get_dict():
    """Get the renaming dict for TEG and SPAAR variables
    
    input:
        None
    output:
        teg_dict (dict): the renaming for TEG variables
        spaar_dict (dict): the renaming for SPAAR variables
    """
    
    teg_dict = {}
    for i in range(16):
        teg_dict[f'teg{i+1}'] = {'2': 2,
                                 '3': 3,
                                 '4': 4,
                                 '5': 5,
                                 '6': 6}
        for var in TEG_QUALITY_HIGH[i]:
            teg_dict[f'teg{i+1}'][var] = 7
        for var in TEG_QUALITY_LOW[i]:
            teg_dict[f'teg{i+1}'][var] = 1

    spaar_dict = {f'spaar{i+1}': SPAAR_VALUES for i in range(6)}
    return teg_dict, spaar_dict


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