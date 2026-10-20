
from app.services.skill_matcher import classify_job_skills


def test_separates_required_and_preferred_skills():
    job = """
    Required skills: Python and SQL.
    Docker is preferred.
    """

    result = classify_job_skills(job)

    assert result["required_skills"] == ["python", "sql"]
    assert result["preferred_skills"] == ["docker"]


def test_mandatory_and_nice_to_have_language():
    job = """
    Mandatory: Java.
    Nice to have: React.
    """

    result = classify_job_skills(job)

    assert result["required_skills"] == ["java"]
    assert result["preferred_skills"] == ["react"]


def test_unlabelled_skills_default_to_required():
    job = "Python, SQL, and Docker experience."

    result = classify_job_skills(job)

    assert result["required_skills"] == [
        "docker",
        "python",
        "sql",
    ]
    assert result["preferred_skills"] == []
