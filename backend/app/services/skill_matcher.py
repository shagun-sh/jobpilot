
import re


SKILL_ALIASES = {
    "python": ["python", "python programming"],
    "java": ["java", "core java"],
    "javascript": ["javascript", "js", "ecmascript"],
    "typescript": ["typescript"],
    "c++": ["c++", "cpp"],
    "sql": ["sql", "structured query language"],
    "postgresql": ["postgresql", "postgres"],
    "mysql": ["mysql"],
    "fastapi": ["fastapi"],
    "django": ["django"],
    "flask": ["flask"],
    "node.js": ["node.js", "nodejs", "node js"],
    "express.js": ["express.js", "expressjs", "express js"],
    "react": ["react", "react.js", "reactjs", "react js"],
    "html": ["html"],
    "css": ["css"],
    "git": ["git", "github"],
    "docker": ["docker"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning"],
    "natural language processing": [
        "natural language processing",
        "nlp",
    ],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "rest api": ["rest api", "restful api", "rest apis"],
}


# These patterns must end immediately before the skill mention.
NEGATION_PATTERNS = [
    r"\bnever\s+(?:used|worked with|learned|studied|tried)\s+(?:the\s+)?$",
    r"\bnot\s+(?:familiar|proficient)\s+with\s+(?:the\s+)?$",
    r"\bno\s+(?:practical\s+)?experience\s+(?:with|in)\s+(?:the\s+)?$",
    r"\b(?:lack|lacking)\s+(?:of\s+)?(?:knowledge|experience|proficiency)\s+(?:of|in|with)\s+(?:the\s+)?$",
    r"\b(?:don't|do not|doesn't|does not)\s+(?:know|use|understand)\s+(?:the\s+)?$",
    r"\bwithout\s+(?:any\s+)?(?:knowledge|experience|proficiency)\s+(?:of|in|with)\s+(?:the\s+)?$",
]


def normalize_text(text: str) -> str:
    """Normalize common spelling variations without losing technical symbols."""
    text = text.lower()
    text = re.sub(r"\bnode\s+js\b", "node.js", text)
    text = re.sub(r"\breact\s+js\b", "react.js", text)
    text = re.sub(r"\bexpress\s+js\b", "express.js", text)
    return text


def contains_term(text: str, term: str) -> bool:
    """Match a complete term rather than an arbitrary substring."""
    pattern = rf"(?<!\w){re.escape(term)}(?!\w)"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def _is_negated(text: str, start: int) -> bool:
    """Detect common negation patterns immediately before a skill."""
    prefix = text[max(0, start - 60):start]

    # A phrase like "not only Python" is affirmative, not negative.
    if re.search(r"\bnot\s+only\s+$", prefix):
        return False

    return any(
        re.search(pattern, prefix)
        for pattern in NEGATION_PATTERNS
    )


def _find_alias_occurrences(text: str, alias: str) -> list[tuple[int, int]]:
    pattern = rf"(?<!\w){re.escape(alias)}(?!\w)"
    return [
        match.span()
        for match in re.finditer(pattern, text, flags=re.IGNORECASE)
    ]


def extract_skills(text: str) -> list[str]:
    """Extract known skills while ignoring common negated mentions."""
    normalized = normalize_text(text)
    found = []

    for canonical_skill, aliases in SKILL_ALIASES.items():
        occurrences = []

        for alias in aliases:
            occurrences.extend(
                _find_alias_occurrences(normalized, alias)
            )

        # Count the skill if at least one mention is affirmative.
        if occurrences and any(
            not _is_negated(normalized, start)
            for start, _ in occurrences
        ):
            found.append(canonical_skill)

    return sorted(found)

def classify_job_skills(job_description: str) -> dict:
    """Separate explicitly required and preferred skills."""

    if not job_description or not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    normalized = normalize_text(job_description)
    required = set()
    preferred = set()

    # Split the description into sentences or lines.
    segments = re.split(r"[\n.!?;]+", normalized)

    preferred_markers = (
        "preferred",
        "nice to have",
        "nice-to-have",
        "desirable",
        "bonus",
        "a plus",
        "plus if",
        "ideally",
    )

    required_markers = (
        "required",
        "requirements",
        "mandatory",
        "essential",
        "must have",
        "must-have",
    )

    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue

        skills = set(extract_skills(segment))

        # Preferred markers take priority within a segment.
        if any(marker in segment for marker in preferred_markers):
            preferred.update(skills)
        elif any(marker in segment for marker in required_markers):
            required.update(skills)
        else:
            # Default to required when no explicit preference is stated.
            required.update(skills)

    # If a skill appears in both groups, required takes precedence.
    preferred -= required

    return {
        "required_skills": sorted(required),
        "preferred_skills": sorted(preferred),
    }


def analyze_match(
    resume_text: str,
    job_description: str,
) -> dict:
    """Compare resume skills with weighted job requirements."""

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    if not job_description or not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    resume_skills = set(extract_skills(resume_text))
    classification = classify_job_skills(job_description)

    required = set(classification["required_skills"])
    preferred = set(classification["preferred_skills"])

    matched_required = resume_skills & required
    matched_preferred = resume_skills & preferred

    missing_required = required - resume_skills
    missing_preferred = preferred - resume_skills

    denominator = (2 * len(required)) + len(preferred)
    numerator = (2 * len(matched_required)) + len(matched_preferred)

    score = round(numerator / denominator * 100, 1) if denominator else 0.0

    suggestions = [
        f"Develop or demonstrate {skill} through a relevant project."
        for skill in sorted(missing_required | missing_preferred)
    ]

    return {
        "match_score": score,
        "matched_skills": sorted(matched_required | matched_preferred),
        "missing_skills": sorted(missing_required | missing_preferred),
        "resume_skills": sorted(resume_skills),
        "required_skills": sorted(required),
        "preferred_skills": sorted(preferred),
        "missing_required_skills": sorted(missing_required),
        "missing_preferred_skills": sorted(missing_preferred),
        "suggestions": suggestions,
    }
