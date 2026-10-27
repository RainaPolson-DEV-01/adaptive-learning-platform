"""Generate knowledge checks tailored to a learner and topic."""

from collections.abc import Callable


class AssessmentAgent:
    """Generate an assessment with an answer key and explanations."""

    def __init__(self, generate: Callable[[str], str]) -> None:
        self._generate = generate

    def create_assessment(
        self,
        topic: str,
        learner_profile: str,
        question_count: int = 5,
    ) -> str:
        """Create an assessment for the given topic and learner."""
        if not topic.strip():
            raise ValueError("topic must not be empty")
        if not learner_profile.strip():
            raise ValueError("learner_profile must not be empty")
        if question_count < 1:
            raise ValueError("question_count must be at least 1")

        prompt = (
            f"Create exactly {question_count} assessment questions about "
            f"{topic!r}, calibrated to this learner's profile. Include a "
            "mix of recall and application where appropriate. Put the "
            "answer key and brief explanations after all questions so the "
            "learner can attempt them first.\n\n"
            f"Learner profile:\n{learner_profile}"
        )
        return self._generate(prompt)
