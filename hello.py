from collections import Counter
from pathlib import Path
import argparse
import re


def load_stopwords(path: Path | None) -> set[str]:
    if path is None or (not path.exists()):
        return set()
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    return {line.strip() for line in lines if line.strip()}


def tokenize(text: str, lang: str) -> list[str]:
    text = text.strip().lower()
    if lang == "zh":
        try:
            import jieba  # type: ignore
        except ImportError:
            raise RuntimeError("缺少依赖 jieba：请先 pip install -r requirements.txt")
        return [w.strip() for w in jieba.cut(text) if w.strip()]
    return re.findall(r"\b\w+\b", text)


def top_words(text: str, topk: int, lang: str, stopwords: set[str]) -> list[tuple[str, int]]:
    tokens = [t for t in tokenize(text, lang) if t and t not in stopwords]
    return Counter(tokens).most_common(topk)


def main():
    parser = argparse.ArgumentParser(description="Word frequency counter (supports zh/en)")
    parser.add_argument("input", type=str, help="path to input txt")
    parser.add_argument("--topk", type=int, default=10, help="top k words")
    parser.add_argument("--lang", type=str, default="en", choices=["en", "zh"], help="language mode")
    parser.add_argument("--stopwords", type=str, default="stopwords.txt", help="stopwords file path")
    parser.add_argument("--out", type=str, default="", help="optional output file (tsv)")
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        raise FileNotFoundError(f"File not found: {in_path}")

    text = in_path.read_text(encoding="utf-8", errors="ignore")
    sw = load_stopwords(Path(args.stopwords) if args.stopwords else None)

    results = top_words(text, topk=args.topk, lang=args.lang, stopwords=sw)

    lines = [f"{w}\t{c}" for w, c in results]
    output = "\n".join(lines)

    print(output)
    if args.out:
        Path(args.out).write_text(output + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
