"""Coordinate learner agents into reusable learning workflows."""

from backend.agents.adaptive_agent import AdaptiveAgent
from backend.agents.assessment_agent import AssessmentAgent
from backend.agents.planner_agent import PlannerAgent
from backend.agents.profile_agent import ProfileAgent
from backend.agents.tutor_agent import TutorAgent
from backend.models.learner_profile import LearnerProfile


class LearningWorkflow:
    """Coordinate profile, assessment, planning, tutoring, and adaptation."""

    def __init__(
        self,
        profile_agent: ProfileAgent,
        assessment_agent: AssessmentAgent,
        planner_agent: PlannerAgent,
        tutor_agent: TutorAgent,
        adaptive_agent: AdaptiveAgent,
    ) -> None:
        self._profile_agent = profile_agent
        self._assessment_agent = assessment_agent
        self._planner_agent = planner_agent
        self._tutor_agent = tutor_agent
        self._adaptive_agent = adaptive_agent

    def create_learner_profile(
        self,
        learner_id: str,
        learner_information: str,
    ) -> LearnerProfile:
        """Generate and return a profile from learner-provided information."""
        summary = self._profile_agent.create_profile(learner_information)
        return LearnerProfile(learner_id=learner_id, profile_summary=summary)

    def create_assessment(
        self,
        profile: LearnerProfile,
        topic: str,
        question_count: int = 5,
    ) -> str:
        """Generate a topic assessment tailored to the learner."""
        return self._assessment_agent.create_assessment(
            topic=topic,
            learner_profile=profile.profile_summary,
            question_count=question_count,
        )

    def create_learning_plan(
        self,
        profile: LearnerProfile,
        assessment_results: str,
    ) -> str:
        """Create a study plan using the learner profile and results."""
        return self._planner_agent.create_plan(
            learner_profile=profile.profile_summary,
            assessment_results=assessment_results,
        )

    def answer_question(
        self,
        profile: LearnerProfile,
        question: str,
        learning_context: str = "",
    ) -> str:
        """Get a context-aware tutoring response for the learner."""
        return self._tutor_agent.answer_question(
            question=question,
            learner_profile=profile.profile_summary,
            learning_context=learning_context,
        )

    def adapt_learning_plan(
        self,
        current_plan: str,
        learner_progress: str,
        learner_feedback: str = "",
    ) -> str:
        """Update a study plan using progress and learner feedback."""
        return self._adaptive_agent.adapt_plan(
            current_plan=current_plan,
            learner_progress=learner_progress,
            learner_feedback=learner_feedback,
        )
