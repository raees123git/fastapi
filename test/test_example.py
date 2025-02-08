import pytest


def test_equal_or_not_equal():
    assert 3 == 3
    # assert 3 != 3


def test_instance():
    assert isinstance('thsi is string', str)


def test_boolean():
    validate = True
    assert validate is True


def test_type():
    assert type('shelo' is str)


def test_greater_and_less_than():
    assert 7 > 3


def test_list():
    num_list = [1, 2, 3, 4, 5]
    assert 1 in num_list


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee():
    return Student('john', "Doe", "computer science", 3)


def test_person_initialization(default_employee):

    assert default_employee.first_name == "john", 'first name should be john'
    assert default_employee.last_name == 'Doe', 'last name should be doe'
    assert default_employee.major == 'computer science'
    assert default_employee.years == 3
