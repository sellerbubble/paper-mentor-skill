"""
Paper Explorer Agent

Responsible for:
1. Downloading and parsing papers
2. Extracting keywords
3. Searching HuggingFace Papers
4. Scoring and ranking papers
5. Domain analysis
"""

import asyncio
import aiohttp
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta


class PaperDownloader:
    """Download and parse papers from arXiv."""

    async def download_and_parse(self, arxiv_id: str) -> Dict:
        """
        Download paper from arXiv and extract title, abstract, authors.

        Args:
            arxiv_id: arXiv ID (e.g., '1706.03762')

        Returns:
            Dictionary with title, abstract, authors, etc.
        """
        # Use arXiv API to get metadata
        api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                xml_content = await response.text()

        # Parse XML to extract metadata
        return self._parse_arxiv_xml(xml_content)

    def _parse_arxiv_xml(self, xml_content: str) -> Dict:
        """Parse arXiv XML response."""
        # Simplified parsing - in production use xml.etree.ElementTree
        import re

        title_match = re.search(r'<title>([^<]+)</title>', xml_content)
        summary_match = re.search(r'<summary>([^<]+)</summary>', xml_content)

        return {
            "title": title_match.group(1).strip() if title_match else "",
            "abstract": summary_match.group(1).strip() if summary_match else "",
            "arxiv_id": self._extract_arxiv_id(xml_content)
        }

    def _extract_arxiv_id(self, xml_content: str) -> str:
        """Extract arXiv ID from XML."""
        import re
        match = re.search(r'arxiv\.org/abs/(\d+\.\d+)', xml_content)
        return match.group(1) if match else ""


class KeywordExtractor:
    """Extract keywords from paper abstract using LLM."""

    async def extract(self, title: str, abstract: str, num_keywords: int = 5) -> List[str]:
        """
        Extract keywords using LLM.

        Args:
            title: Paper title
            abstract: Paper abstract
            num_keywords: Number of keywords to extract

        Returns:
            List of keywords
        """
        # The actual implementation would call an LLM
        # For now, return placeholder
        # In production: Use Claude to extract keywords

        prompt = f"""
        Extract {num_keywords} key technical terms from this paper:

        Title: {title}

        Abstract: {abstract}

        Return only the keywords, one per line.
        """

        # Placeholder - actual implementation calls LLM
        return self._extract_simple_keywords(title, abstract, num_keywords)

    def _extract_simple_keywords(self, title: str, abstract: str, num_keywords: int) -> List[str]:
        """Simple keyword extraction (fallback)."""
        text = (title + " " + abstract).lower()
        # Remove common words
        stop_words = {'the', 'a', 'an', 'of', 'in', 'on', 'for', 'with', 'and', 'to', 'is', 'are'}
        words = [w for w in text.split() if w not in stop_words and len(w) > 3]

        # Simple frequency-based extraction
        from collections import Counter
        return [word for word, _ in Counter(words).most_common(num_keywords)]


class HuggingFaceSearcher:
    """Search HuggingFace Papers for similar papers."""

    BASE_URL = "https://huggingface.co/papers"

    def __init__(self, weeks: int = 20):
        self.weeks = weeks
        self.all_papers: List[Dict] = []

    async def search(self, keywords: List[str]) -> List[Dict]:
        """
        Search for papers matching keywords.

        Args:
            keywords: List of keywords to search for

        Returns:
            List of matching papers with scores
        """
        # Fetch papers from recent weeks
        await self._fetch_recent_papers()

        # Score and filter papers
        scored_papers = self._score_papers(keywords)

        # Return top papers
        return scored_papers[:20]  # Return extra for deduplication

    async def _fetch_recent_papers(self):
        """
        Fetch papers from recent weeks using HuggingFace Papers weekly collections.

        Uses the HuggingFace Papers format: https://huggingface.co/papers?week=YYYY-Www
        """
        from utils import get_recent_weeks

        week_ids = get_recent_weeks(self.weeks)
        all_papers = []

        for week_id in week_ids:
            papers = await self._fetch_week_papers(week_id)
            all_papers.extend(papers)

        self.all_papers = all_papers
        return all_papers

    async def _fetch_week_papers(self, week_id: str) -> List[Dict]:
        """
        Fetch papers for a specific week.

        Args:
            week_id: Week identifier (e.g., '2026-W09')

        Returns:
            List of paper dictionaries
        """
        # In production: Use WebFetch tool via Claude Code
        # URL format: https://huggingface.co/papers?week={week_id}
        # For now, return empty list - actual implementation would:
        # 1. Fetch the page HTML
        # 2. Parse paper titles and metadata
        # 3. Return list of paper dicts

        # Placeholder for now
        return []

    def _score_papers(self, keywords: List[str]) -> List[Tuple[Dict, float]]:
        """Score papers based on keyword matching."""
        scored = []

        for paper in self.all_papers:
            title = paper.get("title", "").lower()
            score = 0.0

            for keyword in keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in title:
                    # Weight by keyword importance
                    score += 1.0

            if score > 0:
                scored.append((paper, score))

        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored


class PaperScorer:
    """Score papers using keyword weighting matrix."""

    # Keyword weight matrix (customizable per domain)
    WEIGHT_MATRIX = {
        3.0: [  # High weight keywords
            "transformer", "attention", "self-attention",
            "bert", "gpt", "language model"
        ],
        2.0: [  # Medium weight
            "neural network", "deep learning", "representation"
        ],
        1.0: [  # Low weight
            "learning", "model", "training"
        ]
    }

    def score(self, title: str, abstract: str, keywords: List[str]) -> float:
        """
        Calculate relevance score for a paper.

        Args:
            title: Paper title
            abstract: Paper abstract
            keywords: Search keywords

        Returns:
            Relevance score
        """
        text = (title + " " + abstract).lower()
        score = 0.0

        for weight, kw_list in self.WEIGHT_MATRIX.items():
            for kw in kw_list:
                if kw in text:
                    score += weight

        # Add base keyword match score
        for kw in keywords:
            if kw.lower() in text:
                score += 1.0

        return score


class DomainAnalyzer:
    """Analyze research domain from paper collection."""

    async def analyze(
        self,
        main_paper: Dict,
        similar_papers: List[Dict]
    ) -> Dict:
        """
        Generate domain analysis report.

        Args:
            main_paper: The input paper
            similar_papers: List of similar papers

        Returns:
            Domain analysis report
        """
        # Use LLM to generate analysis
        report = {
            "research_direction": self._extract_research_direction(main_paper, similar_papers),
            "evolution": self._extract_evolution(similar_papers),
            "key_concepts": self._extract_key_concepts(similar_papers),
            "core_value": self._extract_core_value(main_paper)
        }
        return report

    def _extract_research_direction(self, main_paper: Dict, similar_papers: List[Dict]) -> str:
        """Extract research direction from papers using LLM."""
        # In production: Call LLM with paper information
        # For now, return a template that will be filled by actual LLM calls
        return self._generate_llm_analysis(
            main_paper=main_paper,
            similar_papers=similar_papers,
            analysis_type="research_direction"
        )

    def _extract_evolution(self, similar_papers: List[Dict]) -> str:
        """Extract field evolution from similar papers using LLM."""
        return self._generate_llm_analysis(
            similar_papers=similar_papers,
            analysis_type="evolution"
        )

    def _extract_key_concepts(self, similar_papers: List[Dict]) -> List[str]:
        """Extract key concepts from paper collection using LLM."""
        concepts = self._generate_llm_analysis(
            similar_papers=similar_papers,
            analysis_type="key_concepts"
        )
        # Parse concepts from LLM response
        if isinstance(concepts, str):
            return [c.strip() for c in concepts.split(",") if c.strip()]
        return concepts if concepts else ["concept1", "concept2"]

    def _extract_core_value(self, main_paper: Dict) -> str:
        """Extract core value from main paper using LLM."""
        return self._generate_llm_analysis(
            main_paper=main_paper,
            analysis_type="core_value"
        )

    def _generate_llm_analysis(
        self,
        main_paper: Dict = None,
        similar_papers: List[Dict] = None,
        analysis_type: str = "research_direction"
    ) -> str:
        """
        Generate analysis using LLM.

        This method will be called by the actual skill implementation
        through Claude Code's LLM capabilities.
        """
        # Build prompt for LLM
        analysis_prompts = {
            "research_direction": """
Based on the following papers, describe the main research direction:

Main Paper: {main_title}
Similar Papers: {similar_titles}

Provide a 2-3 sentence description of what researchers in this field are trying to solve.
""",
            "evolution": """
Based on these similar papers, describe how the field has evolved:

Papers: {similar_titles}

Provide a 2-3 sentence description of the field evolution.
""",
            "key_concepts": """
Extract key concepts from these papers as a comma-separated list:

Papers: {similar_titles}

Return only the concepts, no explanation.
""",
            "core_value": """
What is the core value/contribution of this paper?

Title: {main_title}
Abstract: {main_abstract}

Provide a 1-2 sentence summary of the core contribution.
"""
        }

        # In production: Actually call LLM with the prompt
        # For now, return placeholder based on analysis type
        prompts = analysis_prompts.get(analysis_type, "")

        # Placeholder values
        placeholders = {
            "research_direction": "Research direction analysis - to be filled by LLM",
            "evolution": "Field evolution analysis - to be filled by LLM",
            "key_concepts": ["concept1", "concept2", "concept3"],
            "core_value": "Core value analysis - to be filled by LLM"
        }

        return placeholders.get(analysis_type, "")


class PaperExplorer:
    """
    Main Paper Explorer Agent.

    Coordinates:
    1. Keyword extraction
    2. Paper search
    3. Domain analysis
    """

    def __init__(self):
        self.downloader = PaperDownloader()
        self.keyword_extractor = KeywordExtractor()
        self.searcher = HuggingFaceSearcher()
        self.domain_analyzer = DomainAnalyzer()

    async def search(
        self,
        title: str,
        abstract: str,
        num_papers: int = 10
    ) -> Dict:
        """
        Search for similar papers and generate domain analysis.

        Args:
            title: Input paper title
            abstract: Input paper abstract
            num_papers: Number of similar papers to find

        Returns:
            Dictionary with papers and domain analysis
        """
        # Step 1: Extract keywords
        keywords = await self.keyword_extractor.extract(title, abstract)
        print(f"  Extracted keywords: {keywords}")

        # Step 2: Search HuggingFace
        papers = await self.searcher.search(keywords)
        print(f"  Found {len(papers)} papers")

        # Step 3: Generate domain analysis
        domain_analysis = await self.domain_analyzer.analyze(
            {"title": title, "abstract": abstract},
            papers[:num_papers]
        )

        return {
            "keywords": keywords,
            "papers": papers[:num_papers],
            "domain_analysis": domain_analysis
        }


if __name__ == "__main__":
    # Test the Paper Explorer
    async def test():
        explorer = PaperExplorer()
        result = await explorer.search(
            title="Attention Is All You Need",
            abstract="We propose a new simple network architecture, the Transformer, based solely on attention mechanisms...",
            num_papers=10
        )
        print(f"Result: {result}")

    # asyncio.run(test())
    print("Paper Explorer module loaded successfully")
