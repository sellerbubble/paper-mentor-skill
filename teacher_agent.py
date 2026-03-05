"""
Teacher Agent

Responsible for:
1. Generating learning questions (Bloom taxonomy)
2. Managing interactive Q&A session
3. Adapting question difficulty based on user level
"""

from typing import List, Dict, Optional
import asyncio


class QuestionGenerator:
    """Generate learning questions based on Bloom's taxonomy."""

    BLOOM_LEVELS = {
        "remember": "记忆 - Recall facts and basic concepts",
        "understand": "理解 - Explain ideas and concepts",
        "apply": "应用 - Use information in new situations",
        "analyze": "分析 - Draw connections among ideas",
        "evaluate": "评价 - Justify a stand or decision",
        "create": "综合/创造 - Produce new or original work"
    }

    def __init__(self):
        self.difficulty_templates = {
            "beginner": self._get_beginner_template(),
            "intermediate": self._get_intermediate_template(),
            "advanced": self._get_advanced_template()
        }

    async def generate_questions(
        self,
        main_paper: Dict,
        similar_papers: List[Dict],
        domain_analysis: Dict,
        difficulty: str = "intermediate",
        num_questions: int = 10
    ) -> List[Dict]:
        """
        Generate learning questions.

        Args:
            main_paper: The input paper
            similar_papers: List of similar papers
            domain_analysis: Domain analysis report
            difficulty: User's knowledge level (beginner/intermediate/advanced)
            num_questions: Number of questions to generate

        Returns:
            List of question dictionaries
        """
        # Use LLM to generate questions
        template = self.difficulty_templates.get(difficulty, self.difficulty_templates["intermediate"])

        prompt = self._build_prompt(
            main_paper=main_paper,
            similar_papers=similar_papers,
            domain_analysis=domain_analysis,
            template=template,
            num_questions=num_questions
        )

        # In production: Call LLM with prompt
        # For now, return placeholder questions
        return self._generate_placeholder_questions(num_questions, difficulty)

    def _build_prompt(
        self,
        main_paper: Dict,
        similar_papers: List[Dict],
        domain_analysis: Dict,
        template: str,
        num_questions: int
    ) -> str:
        """Build the LLM prompt for question generation."""
        return f"""
        Generate {num_questions} learning questions based on the following paper and domain analysis.

        Main Paper:
        Title: {main_paper.get('title', 'N/A')}
        Abstract: {main_paper.get('abstract', 'N/A')[:500]}...

        Domain Analysis:
        Research Direction: {domain_analysis.get('research_direction', 'N/A')}
        Key Concepts: {', '.join(domain_analysis.get('key_concepts', []))}

        Generate questions across Bloom's taxonomy levels:
        - 2 Remember questions
        - 2 Understand questions
        - 2 Apply questions
        - 2 Analyze questions
        - 1 Evaluate question
        - 1 Create question

        {template}

        Return format (JSON):
        [
            {{"level": "remember", "question": "...", "expected_answer": "..."}},
            ...
        ]
        """

    def _get_beginner_template(self) -> str:
        return """
        For BEGINNER level:
        - Use simpler language
        - Focus on understanding basic concepts
        - Provide hints in questions
        - Avoid technical jargon when possible
        """

    def _get_intermediate_template(self) -> str:
        return """
        For INTERMEDIATE level:
        - Use standard technical language
        - Balance concept understanding with application
        - Expect familiarity with domain basics
        """

    def _get_advanced_template(self) -> str:
        return """
        For ADVANCED level:
        - Use advanced technical language
        - Focus on analysis, evaluation, and creation
        - Ask about trade-offs and limitations
        - Include comparison with alternative approaches
        """

    def _generate_placeholder_questions(self, num_questions: int, difficulty: str) -> List[Dict]:
        """Generate placeholder questions (for testing)."""
        return [
            {
                "level": "remember",
                "question": "What is the main contribution of this paper?",
                "expected_answer": "Key contribution..."
            },
            {
                "level": "understand",
                "question": "Explain the core mechanism proposed in this paper.",
                "expected_answer": "Core mechanism explanation..."
            },
            {
                "level": "apply",
                "question": "How would you apply this technique to a different domain?",
                "expected_answer": "Application scenario..."
            },
            {
                "level": "analyze",
                "question": "What are the key differences between this approach and prior work?",
                "expected_answer": "Comparative analysis..."
            },
            {
                "level": "evaluate",
                "question": "What are the main limitations of this approach?",
                "expected_answer": "Limitation analysis..."
            },
            {
                "level": "create",
                "question": "How would you extend this work for future research?",
                "expected_answer": "Extension proposal..."
            }
        ][:num_questions]


class InteractiveSession:
    """Manage interactive Q&A session with user."""

    def __init__(self, questions: List[Dict]):
        self.questions = questions
        self.user_answers: Dict[int, str] = {}
        self.feedback_history: List[Dict] = []

    async def start(self):
        """Start the interactive session."""
        print("\n📚 Learning Questions:")
        for i, q in enumerate(self.questions, 1):
            print(f"  {i}. [{q['level'].upper()}] {q['question']}")

        print("\n💡 Answer questions by typing 'Q<number>: <your answer>'")
        print("   Type 'hint <number>' for a hint, or 'quit' to exit.\n")

    async def process_answer(self, question_num: int, answer: str) -> Dict:
        """
        Process user's answer and provide feedback.

        Args:
            question_num: Question number (1-indexed)
            answer: User's answer

        Returns:
            Feedback dictionary
        """
        if question_num < 1 or question_num > len(self.questions):
            return {"error": "Invalid question number"}

        self.user_answers[question_num] = answer

        # Get expected answer
        expected = self.questions[question_num - 1].get("expected_answer", "")

        # Evaluate answer (would use Evaluator Agent in production)
        feedback = {
            "question": self.questions[question_num - 1],
            "user_answer": answer,
            "accuracy": 0.8,  # Placeholder
            "completeness": 0.7,  # Placeholder
            "feedback": "Good answer! Consider also mentioning..."
        }

        self.feedback_history.append(feedback)
        return feedback


class TeacherAgent:
    """
    Main Teacher Agent.

    Coordinates:
    1. Question generation
    2. Interactive session management
    3. User difficulty adaptation
    """

    def __init__(self):
        self.question_generator = QuestionGenerator()
        self.session: Optional[InteractiveSession] = None
        self.user_difficulty: str = "intermediate"

    async def generate_questions(
        self,
        main_paper: Dict,
        similar_papers: List[Dict],
        domain_analysis: Dict,
        difficulty: str = "intermediate",
        num_questions: int = 10
    ) -> List[Dict]:
        """Generate questions and initialize session."""
        self.user_difficulty = difficulty
        questions = await self.question_generator.generate_questions(
            main_paper=main_paper,
            similar_papers=similar_papers,
            domain_analysis=domain_analysis,
            difficulty=difficulty,
            num_questions=num_questions
        )
        self.session = InteractiveSession(questions)
        return questions

    async def start_session(self):
        """Start the interactive Q&A session."""
        if self.session:
            await self.session.start()
        else:
            print("⚠️ No questions generated yet. Call generate_questions first.")

    async def process_user_input(self, user_input: str) -> Dict:
        """
        Process user input and return feedback.

        Args:
            user_input: User's message

        Returns:
            Response dictionary
        """
        # Parse user input
        if user_input.lower().startswith("q"):
            # Format: Q1: answer
            parts = user_input.split(":", 1)
            if len(parts) == 2:
                try:
                    q_num = int(parts[0][1:])
                    answer = parts[1].strip()
                    return await self.session.process_answer(q_num, answer)
                except ValueError:
                    return {"error": "Invalid format. Use 'Q1: answer'"}

        elif user_input.lower().startswith("hint"):
            # Provide hint for a question
            parts = user_input.split()
            if len(parts) > 1:
                try:
                    q_num = int(parts[1])
                    return {"hint": f"Hint for question {q_num}..."}
                except ValueError:
                    return {"error": "Invalid hint request"}

        return {"error": "Unknown command"}


if __name__ == "__main__":
    print("Teacher Agent module loaded successfully")
