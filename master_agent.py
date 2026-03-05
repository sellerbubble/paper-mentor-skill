"""
Paper Mentor Skill - Master Orchestrator

Manages the entire workflow:
1. Paper download and parsing
2. Paper Explorer Agent execution
3. Teacher Agent execution
4. Evaluator Agent execution
"""

from typing import Optional, List, Dict, Any
import asyncio


class MasterOrchestrator:
    """
    Main coordinator for the Paper Mentor workflow.

    Attributes:
        paper_url: The input paper URL or arXiv ID
        paper_content: Parsed paper content (title, abstract)
        similar_papers: List of 10 similar papers
        domain_analysis: Domain analysis report
        questions: Generated learning questions
    """

    def __init__(self, paper_url: str):
        self.paper_url = paper_url
        self.paper_content: Optional[Dict] = None
        self.similar_papers: List[Dict] = []
        self.domain_analysis: Optional[Dict] = None
        self.questions: List[Dict] = []
        self.user_difficulty: str = "intermediate"  # beginner/intermediate/advanced

    async def run(self) -> Dict[str, Any]:
        """
        Execute the complete workflow.

        Returns:
            Dictionary containing all results
        """
        print("🎓 Paper Mentor - Starting...")

        # Step 1: Download and parse paper
        print("📄 Step 1: Downloading paper...")
        self.paper_content = await self._download_paper()

        # Step 2: Paper Explorer - search similar papers
        print("🔍 Step 2: Searching similar papers...")
        from paper_explorer import PaperExplorer
        explorer = PaperExplorer()
        explorer_result = await explorer.search(
            title=self.paper_content.get("title", ""),
            abstract=self.paper_content.get("abstract", ""),
            num_papers=10
        )
        self.similar_papers = explorer_result.get("papers", [])
        self.domain_analysis = explorer_result.get("domain_analysis")

        # Step 3: Teacher - generate questions
        print("📝 Step 3: Generating questions...")
        from teacher_agent import TeacherAgent
        teacher = TeacherAgent()
        self.questions = await teacher.generate_questions(
            main_paper=self.paper_content,
            similar_papers=self.similar_papers,
            domain_analysis=self.domain_analysis,
            difficulty=self.user_difficulty
        )

        # Step 4: Interactive Q&A
        print("💬 Step 4: Starting interactive session...")
        await self._interactive_session()

        return {
            "paper": self.paper_content,
            "similar_papers": self.similar_papers,
            "domain_analysis": self.domain_analysis,
            "questions": self.questions
        }

    async def _download_paper(self) -> Dict:
        """Download and parse the input paper."""
        from utils import download_paper_from_url, parse_arxiv_id

        # Parse arXiv ID from URL
        arxiv_id = parse_arxiv_id(self.paper_url)

        # Download PDF and extract content
        from paper_explorer import PaperDownloader
        downloader = PaperDownloader()
        return await downloader.download_and_parse(arxiv_id)

    async def _interactive_session(self):
        """Run interactive Q&A session with user."""
        from teacher_agent import TeacherAgent
        from evaluator_agent import EvaluatorAgent

        teacher = TeacherAgent()
        evaluator = EvaluatorAgent()

        # Display questions
        print("\n📚 Learning Questions:")
        for i, q in enumerate(self.questions, 1):
            print(f"  {i}. [{q['level']}] {q['question']}")

        # Interactive loop
        print("\n💡 You can answer any question by number (e.g., 'Q1: ...') or type 'quit' to exit.")

        while True:
            user_input = input("\nYour answer: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye! Feel free to come back for more learning.")
                break

            # Process user answer
            # (Implementation for interactive session)
            print("🔄 Processing your answer...")


async def main(paper_url: str):
    """Entry point for the skill."""
    orchestrator = MasterOrchestrator(paper_url)
    return await orchestrator.run()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        paper_url = sys.argv[1]
        asyncio.run(main(paper_url))
    else:
        print("Usage: python master_agent.py <paper_url>")
