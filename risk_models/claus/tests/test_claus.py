from unittest import TestCase
from risk_models.claus.claus import calculate_risk, get_lifetime_risk
from risk_models.claus.claus_tables import (
    ONE_FIRST_DEG_TABLE,
    ONE_SECOND_DEG_TABLE,
    TWO_FIRST_DEG_TABLE,
    MOTHER_MATERNAL_AUNT,
    MOTHER_PATERNAL_AUNT,
    TWO_SEC_DEG_DIFF_SIDE_TABLE,
    TWO_SEC_DEG_SAME_SIDE_TABLE
)


class ClausTest(TestCase):

    def setUp(self):
        pass

    def test_one_1st_deg(self):
        score = calculate_risk(20, mother_onset_age=44)
        self.assertEqual(score, get_lifetime_risk(ONE_FIRST_DEG_TABLE, 20, 2))

        score = calculate_risk(20, daughter_onset_ages=[23])
        self.assertEqual(score, get_lifetime_risk(ONE_FIRST_DEG_TABLE, 20, 0))

        score = calculate_risk(20, full_sister_onset_ages=[32], maternal_grandmother_onset_ages=[55])
        self.assertEqual(score, get_lifetime_risk(ONE_FIRST_DEG_TABLE, 20, 1))

        score = calculate_risk(20, full_sister_onset_ages=[11, 22])
        self.assertEqual(score, get_lifetime_risk(ONE_FIRST_DEG_TABLE, 20, 0))

    def test_one_2nd_deg(self):
        score = calculate_risk(20, maternal_aunt_onset_ages=[44])
        self.assertEqual(score, get_lifetime_risk(ONE_SECOND_DEG_TABLE, 20, 2))

        score = calculate_risk(20, paternal_aunt_onset_ages=[54])
        self.assertEqual(score, get_lifetime_risk(ONE_SECOND_DEG_TABLE, 20, 3))

        score = calculate_risk(20, maternal_grandmother_onset_ages=[77])
        self.assertEqual(score, get_lifetime_risk(ONE_SECOND_DEG_TABLE, 20, 5))

        score = calculate_risk(20, maternal_grandmother_onset_ages=[67], paternal_half_sister_onset_ages=[12])
        self.assertEqual(score, get_lifetime_risk(ONE_SECOND_DEG_TABLE, 20, 4))

    def test_two_1st_deg(self):
        score = calculate_risk(
            20,
            mother_onset_age=44,
            daughter_onset_ages=[12, 22],
            maternal_aunt_onset_ages=[33]
        )
        self.assertEqual(score, get_lifetime_risk(TWO_FIRST_DEG_TABLE, 20, 0, 2))

        score = calculate_risk(
            20,
            mother_onset_age=44,
            daughter_onset_ages=[12, 22],
            maternal_aunt_onset_ages=[33],
            full_sister_onset_ages=[11, 23],
        )
        self.assertEqual(score, get_lifetime_risk(TWO_FIRST_DEG_TABLE, 20, 0, 0))

        score = calculate_risk(
            20,
            daughter_onset_ages=[12, 22],
            maternal_aunt_onset_ages=[33, 44],
            full_sister_onset_ages=[11, 34],
            paternal_half_sister_onset_ages=[55],
            paternal_aunt_onset_ages=[22, 23, 24]
        )
        self.assertEqual(score, get_lifetime_risk(TWO_FIRST_DEG_TABLE, 20, 0, 1))

    def test_mom_and_her_sis(self):
        score = calculate_risk(
            20,
            mother_onset_age=55,
            maternal_aunt_onset_ages=[66]
        )
        self.assertEqual(score, get_lifetime_risk(MOTHER_MATERNAL_AUNT, 20, 3, 4))

        score = calculate_risk(
            20,
            mother_onset_age=55,
            maternal_aunt_onset_ages=[66],
        )
        self.assertEqual(score, get_lifetime_risk(MOTHER_MATERNAL_AUNT, 20, 3, 4))

        score = calculate_risk(
            20,
            mother_onset_age=55,
            maternal_aunt_onset_ages=[66],
            paternal_aunt_onset_ages=[52, 43, 54]
        )
        self.assertEqual(score, get_lifetime_risk(MOTHER_MATERNAL_AUNT, 20, 3, 4))

        score = calculate_risk(
            20,
            mother_onset_age=45,
            maternal_aunt_onset_ages=[19, 33, 44],
            paternal_aunt_onset_ages=[22]
        )
        self.assertEqual(score, get_lifetime_risk(MOTHER_MATERNAL_AUNT, 20, 2, 1))

        score = calculate_risk(
            20,
            mother_onset_age=55,
            maternal_aunt_onset_ages=[66, 44],
            paternal_aunt_onset_ages=[22],
            paternal_grandmother_onset_ages=[88, 34]
        )
        self.assertEqual(score, get_lifetime_risk(MOTHER_MATERNAL_AUNT, 20, 3, 2))

    def test_mom_and_paternal_aunt(self):
        score = calculate_risk(
            20,
            mother_onset_age=55,
            paternal_aunt_onset_ages=[22],
        )
        self.assertEqual(score, get_lifetime_risk(MOTHER_PATERNAL_AUNT, 20, 3, 0))

        score = calculate_risk(
            20,
            mother_onset_age=45,
            maternal_aunt_onset_ages=[99],
            paternal_aunt_onset_ages=[63, 22],
        )
        self.assertEqual(score, get_lifetime_risk(MOTHER_PATERNAL_AUNT, 20, 2, 0))

        score = calculate_risk(
            20,
            mother_onset_age=25,
            maternal_aunt_onset_ages=[99],
            paternal_aunt_onset_ages=[33, 52],
            paternal_half_sister_onset_ages=[64, 53, 62]
        )
        self.assertEqual(score, get_lifetime_risk(MOTHER_PATERNAL_AUNT, 20, 0, 1))

    def test_two_sec_deg_diff_side(self):
        score = calculate_risk(
            20,
            daughter_onset_ages=[12],
            maternal_grandmother_onset_ages=[78],
            paternal_half_sister_onset_ages=[44],
        )
        self.assertEqual(score, get_lifetime_risk(TWO_SEC_DEG_DIFF_SIDE_TABLE, 20, 2, 5))

        score = calculate_risk(
            20,
            daughter_onset_ages=[12],
            maternal_aunt_onset_ages=[55, 90],
            paternal_half_sister_onset_ages=[44],
        )
        self.assertEqual(score, get_lifetime_risk(TWO_SEC_DEG_DIFF_SIDE_TABLE, 20, 2, 3))

        score = calculate_risk(
            20,
            daughter_onset_ages=[12],
            maternal_aunt_onset_ages=[55, 90],
            paternal_half_sister_onset_ages=[44],
        )
        self.assertEqual(score, get_lifetime_risk(TWO_SEC_DEG_DIFF_SIDE_TABLE, 20, 2, 3))

        score = calculate_risk(
            20,
            mother_onset_age=12,
            maternal_half_sister_onset_ages=[55],
            paternal_half_sister_onset_ages=[66],
        )
        self.assertEqual(score, get_lifetime_risk(TWO_SEC_DEG_DIFF_SIDE_TABLE, 20, 3, 4))

    def test_two_sec_deg_same_side(self):
        score = calculate_risk(
            20,
            maternal_half_sister_onset_ages=[55],
            maternal_grandmother_onset_ages=[77],
        )
        self.assertEqual(score, get_lifetime_risk(TWO_SEC_DEG_SAME_SIDE_TABLE, 20, 3, 5))

        score = calculate_risk(
            20,
            maternal_half_sister_onset_ages=[55, 12, 44],
            maternal_grandmother_onset_ages=[77],
            paternal_aunt_onset_ages=[55],
        )
        self.assertEqual(score, get_lifetime_risk(TWO_SEC_DEG_SAME_SIDE_TABLE, 20, 2, 3))

        score = calculate_risk(
            20,
            maternal_grandmother_onset_ages=[33],
            paternal_aunt_onset_ages=[55, 22],
        )
        self.assertEqual(score, get_lifetime_risk(TWO_SEC_DEG_SAME_SIDE_TABLE, 20, 0, 3))

        score = calculate_risk(
            20,
            maternal_grandmother_onset_ages=[33],
            paternal_aunt_onset_ages=[77, 22],
            paternal_grandmother_onset_ages=[55],
            paternal_half_sister_onset_ages=[44],
        )
        self.assertEqual(score, get_lifetime_risk(TWO_SEC_DEG_SAME_SIDE_TABLE, 20, 0, 2))

        score = calculate_risk(
            20,
            maternal_grandmother_onset_ages=[55, 66],
            paternal_aunt_onset_ages=[33, 44],
        )
        self.assertEqual(score, get_lifetime_risk(TWO_SEC_DEG_SAME_SIDE_TABLE, 20, 1, 2))

        score = calculate_risk(
            20,
            maternal_grandmother_onset_ages=[22, 77],
            paternal_aunt_onset_ages=[44, 55],
        )
        self.assertEqual(score, get_lifetime_risk(TWO_SEC_DEG_SAME_SIDE_TABLE, 20, 0, 5))

    def test_get_lifetime_risk_one_relative(self):
        table = ONE_FIRST_DEG_TABLE
        computed_score = get_lifetime_risk(table, 32, 3)
        current_age_risk = table[0][3] + (table[1][3] - table[0][3]) * 3 / 10
        expected_score = (table[5][3] - current_age_risk) / (1 - current_age_risk)

        self.assertEqual(computed_score, round(expected_score, 3))

    def test_get_lifetime_risk_on_two_relatives(self):
        table = TWO_SEC_DEG_DIFF_SIDE_TABLE
        computed_score = get_lifetime_risk(table, 47, 4, 1)
        current_age_risk = table[1][4][1] + (table[2][4][1] - table[1][4][1]) * 8 / 10
        expected_score = (table[5][4][1] - current_age_risk) / (1 - current_age_risk)
        self.assertEqual(computed_score, round(expected_score, 3))
