import os
from src.chunking import ChunkingStrategyComparator, compute_similarity
from src.embeddings import _mock_embed
from pathlib import Path

print("=== SECTION 3 BASELINE ===")
files = list(Path("data").glob("*.*"))
comparator = ChunkingStrategyComparator()
for f in files:
    if f.suffix in ['.txt', '.md']:
        content = f.read_text()
        print(f"File: {f.name}")
        res = comparator.compare(content, chunk_size=200)
        for strategy, stats in res.items():
            print(f"  {strategy}: count={stats['count']}, avg_length={stats['avg_length']:.1f}")

print("=== SECTION 5 PREDICTIONS ===")
pairs = [
    ("Machine learning uses algorithms.", "AI relies on data-driven models."),
    ("I like to eat apples.", "I enjoy consuming fruit."),
    ("The stock market crashed today.", "It is raining heavily outside."),
    ("Python is a programming language.", "Java is used for building applications."),
    ("Data science is fun.", "Data science is fun.")
]
for a, b in pairs:
    va = _mock_embed(a)
    vb = _mock_embed(b)
    score = compute_similarity(va, vb)
    print(f"Pair:\nA: {a}\nB: {b}\nScore: {score:.3f}\n")
