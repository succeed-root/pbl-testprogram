# Utility functions for measuring similarity between code snippets
from difflib import SequenceMatcher
import re


def _clean_lines(code: str) -> list[str]:
    """Return a list of code lines with comments and empty lines removed."""
    cleaned = []
    for line in code.splitlines():
        # remove comments starting with // or ;
        comment_pos = len(line)
        for marker in ("//", ";"):
            pos = line.find(marker)
            if pos != -1:
                comment_pos = min(comment_pos, pos)
        line = line[:comment_pos].strip()
        if line:
            cleaned.append(line)
    return cleaned




def levenshtein_distance(s1: str, s2: str) -> int:
    """Compute the Levenshtein edit distance between two strings."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost,
            )
    return dp[m][n]


def char_similarity(s1: str, s2: str) -> float:
    """Return similarity ratio between 0 and 1 ignoring whitespace and comments."""
    lines1 = _clean_lines(s1)
    lines2 = _clean_lines(s2)
    text1 = "".join(lines1)
    text2 = "".join(lines2)
    # remove all whitespace characters
    text1 = re.sub(r"\s+", "", text1)
    text2 = re.sub(r"\s+", "", text2)
    if not text1 and not text2:
        return 1.0
    distance = levenshtein_distance(text1, text2)
    max_len = max(len(text1), len(text2))
    return 1 - distance / max_len


def line_similarity(s1: str, s2: str) -> float:
    """Compare two strings line by line ignoring whitespace and comments."""
    lines1 = [re.sub(r"\s+", "", l) for l in _clean_lines(s1)]
    lines2 = [re.sub(r"\s+", "", l) for l in _clean_lines(s2)]
    return SequenceMatcher(None, lines1, lines2).ratio()

def compare_files(original_path: str, converted_path: str) -> tuple[float, float]:
    """Return similarity scores for two files."""
    with open(original_path, "r", encoding="utf-8") as f:
        original_code = f.read()
    with open(converted_path, "r", encoding="utf-8") as f:
        converted_code = f.read()
    char_score = char_similarity(original_code, converted_code)
    line_score = line_similarity(original_code, converted_code)
    return char_score, line_score


def main(argv: list[str] | None = None) -> int:
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Compute similarity metrics between two files"
    )
    parser.add_argument("original", help="Original code file path")
    parser.add_argument("converted", help="Converted/generated code file path")

    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 2:
        parser.print_usage()
        return 1

    args = parser.parse_args(argv)

    char_score, line_score = compare_files(args.original, args.converted)

    print(f"Character similarity: {char_score:.4f}")
    print(f"Line similarity: {line_score:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

