# hello.py
from collections import Counter
import re
import sys
from pathlib import Path


def top_words(text: str, topk: int = 10):
    # 只保留英文/数字/下划线单词；中文我们后面再升级处理
    words = re.findall(r"\b\w+\b", text.lower())
    return Counter(words).most_common(topk)


def main():
    if len(sys.argv) < 2:
        print("Usage: python hello.py <path_to_txt> [topk]")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    topk = int(sys.argv[2]) if len(sys.argv) >= 3 else 10

    if not file_path.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    text = file_path.read_text(encoding="utf-8", errors="ignore")
    results = top_words(text, topk=topk)

    for word, cnt in results:
        print(f"{word}\t{cnt}")


if __name__ == "__main__":
    main()
