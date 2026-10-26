import pytest
import grade_tracker


@pytest.fixture(autouse=True)
def reset_courses():
    grade_tracker.courses = {}


# -------------------------
# add_course tests
# -------------------------

def test_add_course(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "CPTR 2242")

    grade_tracker.add_course()

    assert "CPTR 2242" in grade_tracker.courses


def test_add_course_empty_name(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")

    grade_tracker.add_course()

    assert grade_tracker.courses == {}
    assert "Course name cannot be empty." in capsys.readouterr().out


def test_add_duplicate_course(capsys, monkeypatch):
    grade_tracker.courses = {
        "CPTR 2242": {
            "assignments": {}
        }
    }

    monkeypatch.setattr("builtins.input", lambda _: "CPTR 2242")

    grade_tracker.add_course()

    assert "Course already exists." in capsys.readouterr().out


# -------------------------
# remove_course tests
# -------------------------

def test_remove_course(monkeypatch):
    grade_tracker.courses = {
        "CPTR 2242": {
            "assignments": {}
        }
    }

    monkeypatch.setattr("builtins.input", lambda _: "CPTR 2242")

    grade_tracker.remove_course()

    assert "CPTR 2242" not in grade_tracker.courses


def test_remove_missing_course(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Missing Course")

    grade_tracker.remove_course()

    assert "Course not found." in capsys.readouterr().out


# -------------------------
# add_assignment tests
# -------------------------

def test_add_assignment(monkeypatch):
    grade_tracker.courses = {
        "CPTR 2242": {
            "assignments": {}
        }
    }

    inputs = iter(["CPTR 2242", "Lab 1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    grade_tracker.add_assignment()

    assert "Lab 1" in grade_tracker.courses["CPTR 2242"]["assignments"]


def test_add_assignment_missing_course(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Missing Course")

    grade_tracker.add_assignment()

    assert "Course not found." in capsys.readouterr().out


def test_add_assignment_empty_name(capsys, monkeypatch):
    grade_tracker.courses = {
        "CPTR 2242": {
            "assignments": {}
        }
    }

    inputs = iter(["CPTR 2242", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    grade_tracker.add_assignment()

    assert "Assignment name cannot be empty." in capsys.readouterr().out


def test_add_duplicate_assignment(capsys, monkeypatch):
    grade_tracker.courses = {
        "CPTR 2242": {
            "assignments": {
                "Lab 1": None
            }
        }
    }

    inputs = iter(["CPTR 2242", "Lab 1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    grade_tracker.add_assignment()

    assert "Assignment already exists." in capsys.readouterr().out


# -------------------------
# edit_assignment tests
# -------------------------

def test_edit_assignment(monkeypatch):
    grade_tracker.courses = {
        "CPTR 2242": {
            "assignments": {
                "Lab 1": 90
            }
        }
    }

    inputs = iter(["CPTR 2242", "Lab 1", "Lab 2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    grade_tracker.edit_assignment()

    assignments = grade_tracker.courses["CPTR 2242"]["assignments"]

    assert "Lab 1" not in assignments
    assert assignments["Lab 2"] == 90


def test_edit_missing_course(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Missing Course")

    grade_tracker.edit_assignment()

    assert "Course not found." in capsys.readouterr().out


def test_edit_missing_assignment(capsys, monkeypatch):
    grade_tracker.courses = {
        "CPTR 2242": {
            "assignments": {}
        }
    }

    inputs = iter(["CPTR 2242", "Missing Lab"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    grade_tracker.edit_assignment()

    assert "Assignment not found." in capsys.readouterr().out


def test_edit_assignment_empty_new_name(capsys, monkeypatch):
    grade_tracker.courses = {
        "CPTR 2242": {
            "assignments": {
                "Lab 1": 90
            }
        }
    }

    inputs = iter(["CPTR 2242", "Lab 1", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    grade_tracker.edit_assignment()

    assert "Assignment name cannot be empty." in capsys.readouterr().out


# -------------------------
# enter_grade tests
# -------------------------

def test_enter_grade(monkeypatch):
    grade_tracker.courses = {
        "CPTR 2242": {
            "assignments": {
                "Lab 1": None
            }
        }
    }

    inputs = iter(["CPTR 2242", "Lab 1", "95"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    grade_tracker.enter_grade()

    assert grade_tracker.courses["CPTR 2242"]["assignments"]["Lab 1"] == 95


def test_enter_grade_zero(monkeypatch):
    grade_tracker.courses = {
        "CPTR 2242": {
            "assignments": {
                "Lab 1": None
            }
        }
    }

    inputs = iter(["CPTR 2242", "Lab 1", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    grade_tracker.enter_grade()

    assert grade_tracker.courses["CPTR 2242"]["assignments"]["Lab 1"] == 0


def test_enter_grade_100(monkeypatch):
    grade_tracker.courses = {
        "CPTR 2242": {
            "assignments": {
                "Lab 1": None
            }
        }
    }

    inputs = iter(["CPTR 2242", "Lab 1", "100"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    grade_tracker.enter_grade()

    assert grade_tracker.courses["CPTR 2242"]["assignments"]["Lab 1"] == 100


def test_enter_grade_over_100(capsys, monkeypatch):
    grade_tracker.courses = {
        "CPTR 2242": {
            "assignments": {
                "Lab 1": None
            }
        }
    }

    inputs = iter(["CPTR 2242", "Lab 1", "101"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    grade_tracker.enter_grade()

    assert "Grade must be between 0 and 100." in capsys.readouterr().out


def test_enter_grade_negative(capsys, monkeypatch):
    grade_tracker.courses = {
        "CPTR 2242": {
            "assignments": {
                "Lab 1": None
            }
        }
    }

    inputs = iter(["CPTR 2242", "Lab 1", "-1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    grade_tracker.enter_grade()

    assert "Grade must be between 0 and 100." in capsys.readouterr().out


def test_enter_grade_invalid_number(capsys, monkeypatch):
    grade_tracker.courses = {
        "CPTR 2242": {
            "assignments": {
                "Lab 1": None
            }
        }
    }

    inputs = iter(["CPTR 2242", "Lab 1", "abc"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    grade_tracker.enter_grade()

    assert "Please enter a valid number." in capsys.readouterr().out


# -------------------------
# view_courses tests
# -------------------------

def test_view_courses_empty(capsys):
    grade_tracker.courses = {}

    grade_tracker.view_courses()

    assert "No courses found." in capsys.readouterr().out


def test_view_courses_no_assignments(capsys):
    grade_tracker.courses = {
        "CPTR 2242": {
            "assignments": {}
        }
    }

    grade_tracker.view_courses()

    output = capsys.readouterr().out

    assert "Course: CPTR 2242" in output
    assert "No assignments." in output


def test_view_courses_ungraded_assignment(capsys):
    grade_tracker.courses = {
        "CPTR 2242": {
            "assignments": {
                "Lab 1": None
            }
        }
    }

    grade_tracker.view_courses()

    assert "Lab 1: Not graded" in capsys.readouterr().out


def test_view_courses_graded_assignment(capsys):
    grade_tracker.courses = {
        "CPTR 2242": {
            "assignments": {
                "Lab 1": 95
            }
        }
    }

    grade_tracker.view_courses()

    assert "Lab 1: 95" in capsys.readouterr().out


def test_calculate_course_average():
    assignments = {
        "Lab 1": 80,
        "Lab 2": 90,
        "Lab 3": 100
    }

    assert grade_tracker.calculate_course_average(assignments) == 90


def test_calculate_course_average_ignores_ungraded():
    assignments = {
        "Lab 1": 80,
        "Lab 2": None,
        "Lab 3": 100
    }

    assert grade_tracker.calculate_course_average(assignments) == 90