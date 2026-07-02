import asyncio
import csv
import types
from pathlib import Path

import main
import baseline

MERGED_REVIEW = "## Review\nSolid paper.\n<score>6.5</score>\n<decision>Accept</decision>"


def fake_usage():
    return types.SimpleNamespace(input_tokens=100, output_tokens=50, total_tokens=150, requests=2)


def make_data_dir(tmp_path):
    data_dir = tmp_path / "data"
    papers_dir = data_dir / "papers"
    papers_dir.mkdir(parents=True)
    with open(data_dir / "ratings.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["paper_id", "title", "score_0", "score_1", "avg_score", "decision", "gt_binary"])
        writer.writerow(["p1", "Paper One", "6", "8", "7.0", "Accept (poster)", "Accept"])
        writer.writerow(["p2", "Paper Two", "3", "3", "3.0", "Reject", "Reject"])
    (papers_dir / "p1.txt").write_text("Paper one content.")
    (papers_dir / "p2.txt").write_text("Paper two content.")
    return data_dir


CSV_HEADER = ["paper_id", "pred_score", "pred_decision", "gt_avg_score", "gt_decision", "gt_binary", "match", "cost", "sdk_savings",
              "gt_score_0", "gt_score_1", "gt_score_2", "gt_score_3", "gt_score_4", "gt_score_5", "gt_score_6"]


# ── main.py pipeline ─────────────────────────────────────────────────

def test_run_pipeline_shape(tmp_path, monkeypatch):
    async def fake_run_agent_with_retry(agent, prompt, max_turns=30):
        # nonzero duration_ms, else the tokens/s log line in run_pipeline divides by zero
        await asyncio.sleep(0.01)
        return MERGED_REVIEW, fake_usage()

    monkeypatch.setattr(main, "run_agent_with_retry", fake_run_agent_with_retry)
    monkeypatch.setenv("MERGE_LOG", str(tmp_path / "pipeline.log"))
    paper = tmp_path / "paper.txt"
    paper.write_text("content")

    result = asyncio.run(main.run_pipeline(str(paper)))

    assert set(result.keys()) == {"merged_review", "scorer_output", "decision", "sdk_usages"}
    assert isinstance(result["merged_review"], str) and result["merged_review"].strip()
    assert isinstance(result["scorer_output"], float) and result["scorer_output"] == 6.5
    assert result["decision"] == "Accept"
    assert isinstance(result["sdk_usages"], dict)
    log_text = (tmp_path / "pipeline.log").read_text()
    for section in ["--- Token Usage ---", "--- Merged Inputs ---", "--- Merged Review ---", "--- Scorer Output ---", "--- Decision ---"]:
        assert section in log_text


def test_run_pipeline_extractor_fallback(tmp_path, monkeypatch):
    async def fake_run_agent_with_retry(agent, prompt, max_turns=30):
        await asyncio.sleep(0.01)
        return "A review with no tags at all. Score: 4 out of 10, leaning reject.", fake_usage()

    async def fake_extractor_create(*args, **kwargs):
        message = types.SimpleNamespace(content="<score>4</score><decision>Reject</decision>")
        return types.SimpleNamespace(choices=[types.SimpleNamespace(message=message)], usage=None)

    monkeypatch.setattr(main, "run_agent_with_retry", fake_run_agent_with_retry)
    monkeypatch.setattr(main.custom_client.chat.completions, "create", fake_extractor_create)
    monkeypatch.setenv("MERGE_LOG", str(tmp_path / "pipeline.log"))
    paper = tmp_path / "paper.txt"
    paper.write_text("content")

    result = asyncio.run(main.run_pipeline(str(paper)))

    assert result["scorer_output"] == 4.0
    assert result["decision"] == "Reject"


def test_process_papers_callback_and_skip(tmp_path, monkeypatch):
    data_dir = make_data_dir(tmp_path)
    papers, papers_dir = main.load_ground_truth(data_dir)

    async def fake_run_pipeline(paper_path, skip_scoring=False, no_cal=False):
        if "p2" in paper_path:
            raise RuntimeError("boom")
        return {"merged_review": MERGED_REVIEW, "scorer_output": 6.5, "decision": "Accept", "sdk_usages": {}}

    monkeypatch.setattr(main, "run_pipeline", fake_run_pipeline)
    collected = []
    asyncio.run(main.process_papers(papers, papers_dir, skip_scoring=False, callback=lambda info, res: collected.append((info, res))))

    assert len(collected) == 1
    info, res = collected[0]
    assert info["paper_id"] == "p1"
    assert res["scorer_output"] == 6.5


def test_run_benchmark_csv_shape(tmp_path, monkeypatch):
    data_dir = make_data_dir(tmp_path)

    async def fake_run_pipeline(paper_path, skip_scoring=False, no_cal=False):
        return {"merged_review": MERGED_REVIEW, "scorer_output": 6.5, "decision": "Accept", "sdk_usages": {}}

    monkeypatch.setattr(main, "run_pipeline", fake_run_pipeline)
    out_csv = tmp_path / "bench_scores.csv"
    reviews_dir = tmp_path / "bench_reviews"
    monkeypatch.setenv("OUTPUT_CSV", str(out_csv))

    asyncio.run(main.run_benchmark(str(data_dir), n_samples=2, seed=42, reviews_dir=str(reviews_dir)))

    with open(out_csv, newline="") as f:
        rows = list(csv.reader(f))
    assert rows[0] == CSV_HEADER
    assert len(rows) == 3
    for row in rows[1:]:
        assert len(row) == len(CSV_HEADER)
        assert float(row[1]) == 6.5
        assert row[2] == "Accept"
        assert row[6] in ("YES", "NO", "N/A")
    written_ids = {row[0] for row in rows[1:]}
    assert written_ids == {"p1", "p2"}
    assert {p.name for p in reviews_dir.iterdir()} == {"p1.md", "p2.md"}
    assert (reviews_dir / "p1.md").read_text() == MERGED_REVIEW


# ── baseline.py pipeline ─────────────────────────────────────────────

def fake_or_response(content, cost=0.01):
    message = types.SimpleNamespace(content=content)
    usage = types.SimpleNamespace(cost=cost)
    return types.SimpleNamespace(choices=[types.SimpleNamespace(message=message)], usage=usage)


def test_baseline_review_paper_shape(tmp_path, monkeypatch):
    review_body = "## Summary\nGood.\nMY FINAL SCORE: <score>8</score>\nMY FINAL DECISION: <decision>Accept</decision>"
    monkeypatch.setattr(baseline.client.chat.completions, "create", lambda *a, **k: fake_or_response(review_body))
    paper = tmp_path / "p1.txt"
    paper.write_text("Paper content.")

    review_text, score, decision, cost = baseline.review_paper(paper, "fake-model", baseline.BASELINE_PROMPT)

    assert review_text == review_body
    assert isinstance(score, float) and score == 8.0
    assert decision == "Accept"
    assert isinstance(cost, float) and cost == 0.01


def test_baseline_parse_review_extractor_fallback(monkeypatch):
    monkeypatch.setattr(
        baseline.client.chat.completions, "create",
        lambda *a, **k: fake_or_response("<score>3.5</score><decision>Reject</decision>", cost=0.001),
    )
    score, decision, extractor_cost = baseline.parse_review("A rambling review that never uses the tags.")
    assert score == 3.5
    assert decision == "Reject"
    assert extractor_cost == 0.001


def test_baseline_run_benchmark_csv_shape(tmp_path, monkeypatch):
    data_dir = make_data_dir(tmp_path)

    def fake_review_paper(paper_path, model, system_prompt):
        if paper_path.stem == "p2":
            raise RuntimeError("boom")
        return "review text", 7.0, "Accept", 0.02

    monkeypatch.setattr(baseline, "review_paper", fake_review_paper)
    out_csv = tmp_path / "baseline_scores.csv"
    reviews_dir = tmp_path / "baseline_reviews"
    monkeypatch.setenv("OUTPUT_CSV", str(out_csv))

    baseline.run_benchmark(str(data_dir), "fake-model", n_samples=2, seed=42, balanced=False, reviews_dir=str(reviews_dir))

    with open(out_csv, newline="") as f:
        rows = list(csv.reader(f))
    assert rows[0] == CSV_HEADER
    assert len(rows) == 3
    by_id = {row[0]: row for row in rows[1:]}
    assert set(by_id) == {"p1", "p2"}
    for row in rows[1:]:
        assert len(row) == len(CSV_HEADER)
    assert float(by_id["p1"][1]) == 7.0
    assert by_id["p1"][2] == "Accept"
    assert by_id["p1"][6] == "YES"
    assert float(by_id["p2"][1]) == -100
    assert by_id["p2"][2] == "Error"
    assert by_id["p2"][6] == "N/A"
    assert {p.name for p in reviews_dir.iterdir()} == {"p1.md", "p2.md"}
    assert (reviews_dir / "p2.md").read_text().startswith("# Error")
