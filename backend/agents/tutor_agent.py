"""Answer learner questions with context-aware tutoring."""

from collections.abc import Callable


class TutorAgent:
    """Provide explanations adapted to the learner's level and context."""

    def __init__(self, generate: Callable[[str], str]) -> None:
        self._generate = generate

    def answer_question(
        self,
        question: str,
        learner_profile: str,
        learning_context: str = "",
    ) -> str:
        """Answer a question in a supportive, learner-appropriate way."""
        if not question.strip():
            raise ValueError("question must not be empty")
        if not learner_profile.strip():
            raise ValueError("learner_profile must not be empty")

        prompt = (
            "Help the learner understand the answer to their question. "
            "Adapt the explanation to their profile, explain key reasoning "
            "clearly, and use a small example when useful. If the context "
            "does not support a reliable answer, say what is missing rather "
            "than guessing.\n\n"
            f"Learner profile:\n{learner_profile}\n\n"
            f"Learning context:\n{learning_context or 'Not provided'}\n\n"
            f"Question:\n{question}"
        )
        return self._generate(prompt)
