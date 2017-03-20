# Color Risk Models

Color genomics risk models

## Background

[The Claus risk model](https://www.ncbi.nlm.nih.gov/pubmed/8299086) is a model
of breast cancer risk from familial data. The paper publishes tables that map risk
percentages based on each family member's relationship and cancer onset ages

This project is a python implementation of this paper. Given a patient's family
history of cancer diagnosis, it returns the lifetime risk of the patient
developing breast cancer assuming he/she is currently cancer-free.

## Implementation details

Given the cancer onset ages of each family relationship, the function
looks at the risk scores derived from all applicable claus tables
and selects the highest one.

_Example: For a patient whose mother and two aunt's have developed cancer._
_The function looks at both the mother + aunt table as well the two second degree_
_relatives table and does each calculation. Depending on the ages of diagnosis,_
_either table can result in higher lifetime cancer risk score._

A key part of calculating remaining risk in the equation specified by the paper
is calculating the risk of developing cancer up til patient's current
age and conditionally removing that probability from lifetime risk.
(As we know the patient is currently cancer-free).
One detail of this implementation is that it does a linear
interpolation between the age buckets specified in the table.

_Example: if patient is age 34 we assume the that risk is half way between the risk,_
_specified at age 29 and age 39_
