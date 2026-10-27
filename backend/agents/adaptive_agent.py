"""Adjust a learning plan using learner progress and feedback."""

from collections.abc import Callable


class AdaptiveAgent:
    """Recommend evidence-based updates to a learner's current plan."""

    def __init__(self, generate: Callable[[str], str]) -> None:
        self._generate = generate

    def adapt_plan(
        self,
        current_plan: str,
        learner_progress: str,
        learner_feedback: str = "",
    ) -> str:
        """Revise a plan while preserving completed work and useful goals."""
        if not current_plan.strip():
            raise ValueError("current_plan must not be empty")
        if not learner_progress.strip():
            raise ValueError("learner_progress must not be empty")

        prompt = (
            "Review the current learning plan in light of the learner's "
            "progress and feedback. Keep completed work marked complete, "
            "reinforce areas of difficulty, and adjust upcoming steps only "
            "where the evidence supports a change. Briefly explain each "
            "proposed adjustment.\n\n"
            f"Current plan:\n{current_plan}\n\n"
            f"Learner progress:\n{learner_progress}\n\n"
            f"Learner feedback:\n{learner_feedback or 'Not provided'}"
        )
        return self._generate(prompt)
