# pbl-testprogram

This repository contains a Python script `similarity.py` that computes how similar two code files are. The script reports both character-based and line-based scores.

The comparison ignores whitespace, line breaks and inline comments beginning with `//` or `;`. Scores range from `0` (completely different) to `1` (identical).

Run the tool with two file paths:

```bash
python3 similarity.py original.mag converted.mag
```

If the paths are omitted, the program prints a brief usage message and exits with an error code.

