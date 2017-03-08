from risk_models.claus.claus_tables import (
    ONE_FIRST_DEG_TABLE,
    ONE_SECOND_DEG_TABLE,
    TWO_FIRST_DEG_TABLE,
    MOTHER_MATERNAL_AUNT,
    MOTHER_PATERNAL_AUNT,
    TWO_SEC_DEG_DIFF_SIDE_TABLE,
    TWO_SEC_DEG_SAME_SIDE_TABLE,
)

VALID_MIN_AGE = 20
VALID_MAX_AGE = 79


def calculate_risk(
        patient_age,
        mother_onset_age=None,
        daughter_onset_ages=None,
        full_sister_onset_ages=None,
        maternal_aunt_onset_ages=None,
        paternal_aunt_onset_ages=None,
        maternal_grandmother_onset_ages=None,
        paternal_grandmother_onset_ages=None,
        maternal_half_sister_onset_ages=None,
        paternal_half_sister_onset_ages=None):
    """
    Calculates the lifteime claus risk score based on age of relatives' breast cancer onset and
    the patient's current cancer-free age.
    """
    first_degree_indices = collect_and_map_ages_to_indices([mother_onset_age], full_sister_onset_ages, daughter_onset_ages)
    second_degree_indices = collect_and_map_ages_to_indices(
        maternal_aunt_onset_ages,
        paternal_aunt_onset_ages,
        maternal_grandmother_onset_ages,
        paternal_grandmother_onset_ages,
        maternal_half_sister_onset_ages,
        paternal_half_sister_onset_ages
    )

    maternal_aunt_indices = map_ages_to_indices(maternal_aunt_onset_ages)
    paternal_aunt_indices = map_ages_to_indices(paternal_aunt_onset_ages)

    maternal_second_degree_indices = collect_and_map_ages_to_indices(
        maternal_aunt_onset_ages,
        maternal_grandmother_onset_ages,
        maternal_half_sister_onset_ages
    )
    paternal_second_degree_indices = collect_and_map_ages_to_indices(
        paternal_aunt_onset_ages,
        paternal_grandmother_onset_ages,
        paternal_half_sister_onset_ages
    )
    mother_index = None

    if mother_onset_age and VALID_MIN_AGE <= mother_onset_age <= VALID_MAX_AGE:
        mother_index = _bin_age_to_index(mother_onset_age)

    # List of scores that match a claus table criteria. We consider lifetime risk to be the maximum value
    risk_scores = [None]

    if len(first_degree_indices) >= 1:
        risk_scores.append(get_lifetime_risk(ONE_FIRST_DEG_TABLE, patient_age, first_degree_indices[0]))

    if len(second_degree_indices) >= 1:
        risk_scores.append(get_lifetime_risk(ONE_SECOND_DEG_TABLE, patient_age, second_degree_indices[0]))

    if len(first_degree_indices) >= 2:
        risk_scores.append(get_lifetime_risk(TWO_FIRST_DEG_TABLE, patient_age, first_degree_indices[0], first_degree_indices[1]))

    if mother_index is not None:
        if len(maternal_aunt_indices) >= 1:
            risk_scores.append(get_lifetime_risk(MOTHER_MATERNAL_AUNT, patient_age, mother_index, maternal_aunt_indices[0]))
        if len(paternal_aunt_indices) >= 1:
            risk_scores.append(get_lifetime_risk(MOTHER_PATERNAL_AUNT, patient_age, mother_index, paternal_aunt_indices[0]))

    if len(maternal_second_degree_indices) >= 2:
        risk_scores.append(get_lifetime_risk(TWO_SEC_DEG_SAME_SIDE_TABLE, patient_age, maternal_second_degree_indices[0], maternal_second_degree_indices[1]))

    if len(paternal_second_degree_indices) >= 2:
        risk_scores.append(get_lifetime_risk(TWO_SEC_DEG_SAME_SIDE_TABLE, patient_age, paternal_second_degree_indices[0], paternal_second_degree_indices[1]))

    if len(maternal_second_degree_indices) >= 1 and len(paternal_second_degree_indices) >= 1:
        risk_scores.append(get_lifetime_risk(TWO_SEC_DEG_DIFF_SIDE_TABLE, patient_age, maternal_second_degree_indices[0], paternal_second_degree_indices[0]))

    return max(risk_scores)


def get_lifetime_risk(table, patient_age, relative1_index, relative2_index=None):
    """
    Computes the conditional risk of patient getting cancer by age 79 given that the patient
    has been cancer free until current age. Inputs are the correct claus table to use and the
    relatives's age index into the table.

    Calculates from lifetime expected risk and the expected risk of patient's current age.
    For patients current age, we look at the claus table of age range below and above the current age.
    Then take a linear interpolation to estimate the current value.

    EX: for age 33. We look up risk at 29 and 39. then estimate assuming risk at age 33 assuming linear change
    between those 10 years.
    """
    LIFETIME_AGE_INDEX = 5
    lifetime_risk = _lookup_claus_table(table, LIFETIME_AGE_INDEX, relative1_index, relative2_index)

    # Get lower age bin index on table as well number years over that lower bin
    patient_age_lower_bin_index, patient_age_over_bin = divmod(patient_age - 29, 10)

    current_age_risk = _lookup_claus_table(table, patient_age_lower_bin_index, relative1_index, relative2_index)

    if patient_age_over_bin:
        patient_age_upper_bin_risk = _lookup_claus_table(table, patient_age_lower_bin_index + 1, relative1_index, relative2_index)
        current_age_risk += (patient_age_upper_bin_risk - current_age_risk) * patient_age_over_bin / 10

    return round((lifetime_risk - current_age_risk) / (1 - current_age_risk), 3)


def _lookup_claus_table(table, patient_index, relative1_index, relative2_index=None):
    if relative2_index is None:
        return table[patient_index][relative1_index]
    return table[patient_index][relative1_index][relative2_index]


def collect_and_map_ages_to_indices(*age_groups):
    collected_ages = []
    for ages in age_groups:
        if ages:
            collected_ages.extend(ages)
    return map_ages_to_indices(collected_ages)


def map_ages_to_indices(ages):
    if ages:
        return sorted([_bin_age_to_index(age) for age in ages if age >= VALID_MIN_AGE and age <= VALID_MAX_AGE])
    return []


def _bin_age_to_index(age):
    return (age - 20) / 10
