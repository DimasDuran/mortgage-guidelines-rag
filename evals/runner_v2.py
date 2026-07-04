# ruff: noqa: E501
import os
import time

from dotenv import load_dotenv
from tqdm import tqdm

from evals.dataset import DATASET
from rag_mortgage_eeuu.retriever import search


def _build_client():
    from anthropic import Anthropic

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is required for evaluation.")
    return Anthropic(api_key=api_key)


def _build_prompt(question: str, contexts: list[str]) -> str:
    ctx = "\n\n".join(contexts) if contexts else "No relevant information found."
    return (
        "You are a mortgage assistant. Answer the question using ONLY the context below.\n\n"
        "Rules:\n"
        "- Extract facts directly from the context. If the context does not answer\n"
        "  the question fully, say what IS available and note what is missing.\n"
        "- Do NOT invent facts or use outside knowledge.\n"
        "- Cite the source document name when possible.\n"
        "- Keep the answer concise (2-4 sentences).\n\n"
        f"Context:\n{ctx}\n\n"
        f"Question: {question}"
    )


def _judge_prompt(question: str, answer: str, ground_truth: str) -> str:
    return (
        "Evaluate whether the predicted answer contains the KEY FACTS from the expected answer.\n"
        "Be FLEXIBLE: accept paraphrasing and partial coverage. Score 0.0 to 1.0.\n\n"
        "Rules:\n"
        "- 0.0 = answer is completely wrong, empty, or hallucinated\n"
        "- 0.5 = answer has some correct facts but misses important ones\n"
        "- 1.0 = answer covers all key facts (paraphrasing is fine)\n\n"
        f"Question: {question}\n\n"
        f"Expected answer: {ground_truth}\n\n"
        f"Predicted answer: {answer}\n\n"
        "Respond with ONLY the number (0.0 to 1.0)."
    )


def main() -> None:
    load_dotenv()
    client = _build_client()

    print(f"Evaluating {len(DATASET)} questions based on actual PDF content...\n")
    results = []
    for item in tqdm(DATASET):
        question = item["question"]
        ground_truth = item["ground_truth"]

        contexts = search(question)
        context_texts = [c["text"] for c in contexts]

        prompt = _build_prompt(question, context_texts)
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        answer = msg.content[0].text

        judge = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=32,
            system="You output ONLY a number like 0.0 or 0.5 or 1.0. No text, no explanation.",
            messages=[{"role": "user", "content": _judge_prompt(
                question, answer, ground_truth
            )}],
        )
        try:
            score = float(judge.content[0].text.strip())
        except ValueError:
            score = 0.0
            tqdm.write(f"  [WARN] Judge returned non-numeric: {judge.content[0].text.strip()[:80]}")

        results.append(
            {
                "question": question,
                "answer": answer,
                "ground_truth": ground_truth,
                "score": score,
                "num_contexts": len(context_texts),
            }
        )

        status = "PASS" if score >= 0.7 else "FAIL"
        tqdm.write(f"  {status} score={score:.2f} ctx={len(context_texts)} | {question[:60]}...")
        tqdm.write(f"         Answer: {answer[:150]}...")

        time.sleep(2)

    total = len(results)
    passed = sum(1 for r in results if r["score"] >= 0.7)
    avg_score = sum(r["score"] for r in results) / total

    print(f"\n{'='*50}")
    print(f"Average score: {avg_score:.2f}")
    print(f"Passed:        {passed}/{total} ({passed/total*100:.0f}%)")
    for r in sorted(results, key=lambda x: x["score"]):
        s = "PASS" if r["score"] >= 0.7 else "FAIL"
        print(f"  {s} {r['score']:.2f} | {r['question'][:70]}...")


if __name__ == "__main__":
    main()
