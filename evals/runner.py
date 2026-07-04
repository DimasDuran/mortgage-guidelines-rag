# ruff: noqa: E501
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from langsmith import traceable

from evals.config import THRESHOLDS
from evals.dataset import DATASET
from rag_mortgage_eeuu.retriever import search


RESULTS_DIR = Path("evals/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


@traceable(name="generate_answer", run_type="llm")
def generate_answer(llm, question: str, context_texts: list[str]) -> str:
    ctx = "\n\n".join(context_texts) if context_texts else "No relevant information found."
    prompt = (
        "You are a mortgage assistant. Answer the question using ONLY the context below.\n\n"
        "Rules:\n"
        "- Extract facts directly from the context.\n"
        "- Do NOT invent facts or use outside knowledge.\n"
        "- Cite the source document name when possible.\n"
        "- Keep the answer concise (2-4 sentences).\n\n"
        f"Context:\n{ctx}\n\n"
        f"Question: {question}"
    )
    msg = llm.invoke(prompt)
    return msg.content


@traceable(name="judge_score", run_type="llm")
def judge_answer(judge_llm, question: str, ground_truth: str, answer: str) -> float:
    judge_text = (
        "Compare the predicted answer to the expected answer. Score 0.0 to 1.0.\n\n"
        f"Question: {question}\n\n"
        f"Expected: {ground_truth}\n\n"
        f"Predicted: {answer}\n\n"
        "Score:"
    )
    judge = judge_llm.invoke([
        ("system", "You output ONLY a single number between 0.0 and 1.0. No text."),
        ("human", judge_text),
    ])
    try:
        return float(judge.content.strip())
    except ValueError:
        return 0.0


@traceable(name="rag_eval_row")
async def run_row(row: dict, llm, judge_llm) -> dict:
    question = row["question"]
    ground_truth = row["ground_truth"]

    contexts = search(question)
    context_texts = [c["text"] for c in contexts]

    answer = generate_answer(llm, question, context_texts)
    score = judge_answer(judge_llm, question, ground_truth, answer)

    result = {
        "question": question,
        "ground_truth": ground_truth,
        "answer": answer,
        "num_contexts": len(context_texts),
        "score": score,
        "passed": score >= 0.7,
    }
    return result


def update_metadata(result: dict) -> None:
    meta_path = RESULTS_DIR / "metadata.jsonl"
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    with open(meta_path, "a") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")


def main() -> None:
    load_dotenv()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    experiment_name = f"rag_eval_{timestamp}"

    from langchain_anthropic import ChatAnthropic

    llm = ChatAnthropic(
        model="claude-sonnet-4-6",
        max_tokens=512,
        temperature=0,
    )
    judge_llm = ChatAnthropic(
        model="claude-sonnet-4-6",
        max_tokens=32,
        temperature=0,
    )

    print(f"Running experiment '{experiment_name}' on {len(DATASET)} questions...")
    print(f"LangSmith tracing: {os.getenv('LANGSMITH_TRACING', 'not set')}")
    print(f"LangSmith project: {os.getenv('LANGSMITH_PROJECT', 'not set')}")
    print()

    async def run_all():
        tasks = [run_row(row, llm, judge_llm) for row in DATASET]
        results = []
        for i, coro in enumerate(asyncio.as_completed(tasks)):
            result = await coro
            results.append(result)
            update_metadata(result)
            p = f"{i+1}/{len(DATASET)}"
            s = "PASS" if result["passed"] else "FAIL"
            print(f"  [{p}] {s} {result['score']:.2f} | {result['question'][:60]}...")
        return results

    results = asyncio.run(run_all())

    passed = sum(1 for r in results if r.get("passed"))
    total = len(results)
    avg_score = sum(r.get("score", 0) for r in results) / total if total else 0

    print(f"\n{'='*50}")
    print(f"Results saved to {RESULTS_DIR}/")
    print(f"LangSmith project: {os.getenv('LANGSMITH_PROJECT')} "
          f"(@ https://smith.langchain.com)")
    print(f"{'='*50}")
    print(f"Average score: {avg_score:.2f}")
    print(f"Passed:        {passed}/{total} ({passed/total*100:.0f}%)")

    threshold_ok = (passed / total) >= THRESHOLDS.answer_correctness if total else False
    if not threshold_ok:
        thr = int(THRESHOLDS.answer_correctness * 100)
        print(f"\nFAIL: accuracy {passed/total*100:.0f}% < threshold {thr}%")
        raise SystemExit(1)
    else:
        print(f"\nAll thresholds met (≥{THRESHOLDS.answer_correctness:.0%}).")


if __name__ == "__main__":
    main()
