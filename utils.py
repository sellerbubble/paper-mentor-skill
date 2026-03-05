"""
Utility functions for Paper Mentor Skill
"""

import re
from typing import Optional, Dict, Any
from datetime import datetime, timedelta


def parse_arxiv_id(url_or_id: str) -> str:
    """
    Parse arXiv ID from various input formats.

    Args:
        url_or_id: arXiv URL or ID string

    Returns:
        Clean arXiv ID (e.g., '1706.03762')

    Examples:
        >>> parse_arxiv_id("https://arxiv.org/abs/1706.03762")
        '1706.03762'
        >>> parse_arxiv_id("1706.03762")
        '1706.03762'
        >>> parse_arxiv_id("arXiv:1706.03762")
        '1706.03762'
    """
    # Already a clean ID (X.XXXXX format)
    if re.match(r'^\d+\.\d+$', url_or_id.strip()):
        return url_or_id.strip()

    # Full URL
    patterns = [
        r'arxiv\.org/abs/(\d+\.\d+)',
        r'arxiv\.org/pdf/(\d+\.\d+)',
        r'arXiv[:\s]+(\d+\.\d+)',
        r'(\d+\.\d+)'
    ]

    for pattern in patterns:
        match = re.search(pattern, url_or_id, re.IGNORECASE)
        if match:
            return match.group(1)

    # Return as-is if no match (might be new format)
    return url_or_id.strip()


def validate_paper_url(url: str) -> bool:
    """
    Validate if input is a valid paper URL or ID.

    Args:
        url: Input string to validate

    Returns:
        True if valid, False otherwise
    """
    if not url or not url.strip():
        return False

    # Check for arXiv URL
    if 'arxiv.org' in url.lower():
        return True

    # Check for arXiv ID
    if parse_arxiv_id(url) != url.strip():
        return True

    # Check for PDF URL
    if url.lower().endswith('.pdf'):
        return True

    return False


def get_recent_weeks(num_weeks: int = 20) -> list:
    """
    Get list of recent week identifiers for HuggingFace Papers.

    Args:
        num_weeks: Number of weeks to go back

    Returns:
        List of week strings (e.g., ['2026-W09', '2026-W08', ...])
    """
    today = datetime.now()
    current_iso = today.isocalendar()
    current_year, current_week = current_iso[0], current_iso[1]

    weeks = []

    year, week = current_year, current_week
    for _ in range(num_weeks):
        # Format week string
        weeks.append(f"{year}-W{week:02d}")

        # Decrement week
        week -= 1
        if week < 1:
            year -= 1
            # Get last week of previous year
            dec_31 = datetime(year, 12, 31)
            week = dec_31.isocalendar()[1]
            if week == 1:  # Edge case: Dec 31 might be in week 1 of next year
                week = datetime(year, 12, 28).isocalendar()[1]

    return weeks


def format_citation(paper: Dict) -> str:
    """
    Format a paper citation from metadata.

    Args:
        paper: Paper metadata dictionary

    Returns:
        Formatted citation string
    """
    title = paper.get('title', 'Unknown title')
    authors = paper.get('authors', [])
    year = paper.get('year', 'n.d.')

    if len(authors) == 1:
        author_str = authors[0]
    elif len(authors) == 2:
        author_str = f"{authors[0]} and {authors[1]}"
    elif len(authors) > 2:
        author_str = f"{authors[0]} et al."
    else:
        author_str = "Anonymous"

    return f"{author_str} ({year}). {title}."


def truncate_text(text: str, max_length: int = 500, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_year_from_arxiv_id(arxiv_id: str) -> int:
    """
    Extract year from arXiv ID.

    Args:
        arxiv_id: arXiv ID string

    Returns:
        4-digit year
    """
    # Old format: math/0401001 -> 2004
    # New format: 1706.03762 -> 2017

    match = re.match(r'(\d{2})\.', arxiv_id)
    if match:
        year_prefix = int(match.group(1))
        # Assume 1990s for years < 90, 2000s otherwise
        if year_prefix < 90:
            return 2000 + year_prefix
        else:
            return 1900 + year_prefix

    # Try to extract from old format
    match = re.match(r'\w+/(\d{2})', arxiv_id)
    if match:
        return 2000 + int(match.group(1))

    return datetime.now().year


def score_paper_by_keywords(
    paper: Dict,
    keywords: list,
    weight_matrix: Dict[float, list] = None
) -> float:
    """
    Score a paper based on keyword matching.

    Args:
        paper: Paper metadata
        keywords: Search keywords
        weight_matrix: Optional keyword weight matrix

    Returns:
        Relevance score
    """
    if weight_matrix is None:
        weight_matrix = {
            3.0: [],  # High priority keywords
            2.0: [],  # Medium priority
            1.0: []   # Low priority
        }

    text = (paper.get('title', '') + ' ' + paper.get('abstract', '')).lower()
    score = 0.0

    # Score by weight matrix
    for weight, kw_list in weight_matrix.items():
        for kw in kw_list:
            if kw.lower() in text:
                score += weight

    # Score by search keywords
    for kw in keywords:
        if kw.lower() in text:
            score += 1.0

    return score


async def fetch_with_retry(
    url: str,
    max_retries: int = 3,
    timeout: int = 30
) -> Optional[Any]:
    """
    Fetch URL with retry logic.

    Args:
        url: URL to fetch
        max_retries: Maximum retry attempts
        timeout: Request timeout in seconds

    Returns:
        Response content or None if all retries failed
    """
    import aiohttp

    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=timeout) as response:
                    if response.status == 200:
                        return await response.text()
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Failed to fetch {url} after {max_retries} attempts: {e}")
                return None
            await asyncio.sleep(2 ** attempt)  # Exponential backoff

    return None


if __name__ == "__main__":
    # Test utilities
    print("Testing parse_arxiv_id...")
    assert parse_arxiv_id("https://arxiv.org/abs/1706.03762") == "1706.03762"
    assert parse_arxiv_id("1706.03762") == "1706.03762"
    assert parse_arxiv_id("arXiv:1706.03762") == "1706.03762"
    print("✅ All tests passed!")

    print(f"\nRecent weeks: {get_recent_weeks(5)}")
