
import pytest

from app.services.skill_matcher import analyze_match, extract_skills


def test_extracts_skill_aliases():
    text = "Experienced with Python, Node.js, PostgreSQL and React."
    skills = extract_skills(text)

    assert "python" in skills
    assert "node.js" in skills
    assert "postgresql" in skills
    assert "react" in skills


def test_calculates_match_score():
    resume = "Python developer with SQL and Git experience."
    job = "Required: Python, SQL, FastAPI."

    result = analyze_match(resume, job)

    assert result["match_score"] == 66.7
    assert result["matched_skills"] == ["python", "sql"]
    assert result["missing_skills"] == ["fastapi"]


def test_empty_resume_is_rejected():
    with pytest.raises(ValueError):
        analyze_match("", "Python developer required")


def test_no_detected_job_skills_returns_zero():
    result = analyze_match(
        "Python developer",
        "Looking for a motivated team player",
    )

    assert result["match_score"] == 0.0
    assert result["required_skills"] == []


# New accuracy tests

@pytest.mark.parametrize(
    "text, expected",
    [
        ("I use NodeJS and Postgres.", ["node.js", "postgresql"]),
        ("My stack includes JS and React.js.", ["javascript", "react"]),
        ("I develop with Python programming.", ["python"]),
        ("I know C++ and TypeScript.", ["c++", "typescript"]),
    ],
)
def test_alias_variations(text, expected):
    assert extract_skills(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "I have never used Docker.",
        "I am not familiar with Docker.",
        "I have no experience with Docker.",
        "I don't know Docker.",
        "I lack knowledge of Docker.",
    ],
)
def test_negated_skills_are_not_counted(text):
    assert "docker" not in extract_skills(text)


def test_positive_mention_still_counts_if_negation_appears_elsewhere():
    text = "I have never used Docker. I later learned Docker."
    assert "docker" in extract_skills(text)


def test_not_only_does_not_count_as_negation():
    text = "I know not only Python but also SQL."
    assert extract_skills(text) == ["python", "sql"]


def test_partial_word_does_not_match_skill():
    # "javascript" must not be detected inside "notjavascript".
    assert "javascript" not in extract_skills("notjavascript")


def test_whitespace_inputs_are_rejected():
    with pytest.raises(ValueError):
        analyze_match("   ", "Python required")

    with pytest.raises(ValueError):
        analyze_match("Python developer", "   ")


def test_job_with_only_unrecognized_skills_returns_zero():
    result = analyze_match(
        "Python developer",
        "Looking for an excellent communicator with leadership skills.",
    )

    assert result["match_score"] == 0.0
    assert result["matched_skills"] == []
    assert result["missing_skills"] == []

def test_required_skills_have_more_weight_than_preferred():
    from app.services.skill_matcher import analyze_match

    resume = "Python developer."
    job = """
    Required: Python and SQL.
    Preferred: Docker.
    """

    result = analyze_match(resume, job)

    assert result["match_score"] == 40.0
    assert result["matched_skills"] == ["python"]
    assert result["missing_skills"] == ["docker", "sql"]
    assert result["missing_required_skills"] == ["sql"]
    assert result["missing_preferred_skills"] == ["docker"]
