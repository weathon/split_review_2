import random

import hivemind
import human_baseline

REVIEW_1 = """## Summary
Paper A proposes a new optimizer.

## Weaknesses
- The paper does not include any ablation study of its main components.
- No statistical significance testing is reported for the main results.
- The novelty over prior optimizers is overclaimed.
"""

REVIEW_2 = """## Summary
Paper B proposes a graph neural network for molecules.

## Weaknesses
- There is no ablation isolating the contribution of the message-passing module.
- The writing has many typos and unclear sentences.
"""


def make_method_dirs(tmp_path):
    multi = tmp_path / "multi"
    single_report = tmp_path / "single_report"
    single_md = tmp_path / "single_md"
    for d in (multi, single_report, single_md):
        d.mkdir()
    (multi / "p1_reviewer1.md").write_text("multi p1 r1")
    (multi / "p1_reviewer2.md").write_text("multi p1 r2")
    (multi / "p2_reviewer1.md").write_text("multi p2 r1")
    (multi / "notes.txt").write_text("ignore me")
    (single_report / "p1_report.md").write_text("report p1")
    (single_report / "p2_report.md").write_text("report p2")
    (single_md / "p1.md").write_text("md p1")
    return {
        "fake_multi": {"dir": multi, "kind": "multi_reviewer"},
        "fake_report": {"dir": single_report, "kind": "single_report"},
        "fake_md": {"dir": single_md, "kind": "single_md"},
    }


def test_list_papers_and_load_review(tmp_path, monkeypatch):
    monkeypatch.setattr(hivemind, "METHODS", make_method_dirs(tmp_path))
    assert hivemind.list_papers("fake_multi") == {"p1", "p2"}
    assert hivemind.list_papers("fake_report") == {"p1", "p2"}
    assert hivemind.list_papers("fake_md") == {"p1"}

    rng = random.Random(0)
    assert hivemind.load_review("fake_multi", "p1", rng) in ("multi p1 r1", "multi p1 r2")
    assert hivemind.load_review("fake_report", "p1", rng) == "report p1"
    assert hivemind.load_review("fake_md", "p1", rng) == "md p1"
    assert hivemind.load_review("fake_multi", "p3", rng) is None
    assert hivemind.load_review("fake_report", "p3", rng) is None
    assert hivemind.load_review("fake_md", "p3", rng) is None


def test_split_human_reviewers():
    md = """# Paper

## Human Reviewer 1
First review body.

## Human Reviewer 2
Second review body.
"""
    reviewers = human_baseline.split_human_reviewers(md)
    assert reviewers == ["First review body.", "Second review body."]
    assert human_baseline.split_human_reviewers("no reviewer sections") == []


def test_load_human_review(tmp_path, monkeypatch):
    monkeypatch.setattr(human_baseline, "HUMAN_DIR", tmp_path)
    (tmp_path / "p1.md").write_text("## Human Reviewer 1\nOnly review.\n")
    (tmp_path / "empty.md").write_text("no sections here")
    rng = random.Random(0)
    assert human_baseline.load_human_review("p1", rng) == "Only review."
    assert human_baseline.load_human_review("empty", rng) is None
    assert human_baseline.load_human_review("missing", rng) is None


def test_judge_real_api_shape():
    rec = hivemind.judge("fake_method", "p1", "p2", REVIEW_1, REVIEW_2)

    assert set(rec.keys()) == {"method", "paper1", "paper2", "n_items_review1", "n_matched", "overlap_rate", "items", "usage"}
    assert rec["method"] == "fake_method"
    assert rec["paper1"] == "p1" and rec["paper2"] == "p2"
    assert rec["n_items_review1"] >= 1
    assert 0 <= rec["n_matched"] <= rec["n_items_review1"]
    assert rec["overlap_rate"] == rec["n_matched"] / rec["n_items_review1"]
    for item in rec["items"]:
        assert set(item.keys()) == {"text", "match_in_review2"}
        assert isinstance(item["text"], str) and item["text"].strip()
        assert item["match_in_review2"] is None or isinstance(item["match_in_review2"], str)


def test_human_baseline_judge_real_api_shape():
    rec = human_baseline.judge("p1", "p2", REVIEW_1, REVIEW_2)
    assert rec["method"] == "human"
    assert rec["n_items_review1"] >= 1
    assert 0 <= rec["n_matched"] <= rec["n_items_review1"]
    for item in rec["items"]:
        assert set(item.keys()) == {"text", "match_in_review2"}
