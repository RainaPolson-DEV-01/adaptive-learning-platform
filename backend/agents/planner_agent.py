"""Create a personalized learning plan."""

from collections.abc import Callable


class PlannerAgent:
    """Build a sequenced study plan from a profile and assessment."""

    def __init__(self, generate: Callable[[str], str]) -> None:
        self._generate = generate

    def create_plan(self, learner_profile: str, assessment_results: str) -> str:
        """Create a practical study plan based on assessment results."""
        if not learner_profile.strip():
            raise ValueError("learner_profile must not be empty")
        if not assessment_results.strip():
            raise ValueError("assessment_results must not be empty")

        prompt = (
            "Create a personalized learning plan using the learner profile "
            "and assessment results. Sequence topics from prerequisites to "
            "more advanced material. For each step, include a learning "
            "objective, a suggested activity, and a way to check progress. "
            "Do not assume a time budget that was not provided.\n\n"
            f"Learner profile:\n{learner_profile}\n\n"
            f"Assessment results:\n{assessment_results}"
        )
        return self._generate(prompt)
