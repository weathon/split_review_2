import csv

import main


def test_parse_score():
    assert main.parse_score("blah <score>6.5</score> blah") == 6.5
    assert main.parse_score("<score>10</score>") == 10.0
    assert main.parse_score("no score here") is None


def test_decision_match():
    assert main.decision_match("Accept", "Accept") is True
    assert main.decision_match("Reject", "Accept") is False
    assert main.decision_match("N/A", "Accept") is None
    assert main.decision_match(None, "Accept") is None
    assert main.decision_match("", "Reject") is None


def test_match_label():
    assert main.match_label(True) == "YES"
    assert main.match_label(False) == "NO"
    assert main.match_label(None) == "N/A"


def test_shorten_title():
    assert main.shorten_title("A Simple Title") == "a_simple_title"
    assert main.shorten_title("CAPS & Punct!!") == "caps_punct"
    assert main.shorten_title("") == "untitled"
    long_title = "word " * 40
    assert len(main.shorten_title(long_title)) <= 60


def test_stratified_sample():
    papers = [{"paper_id": str(i), "avg_score": s} for i, s in enumerate([1.2, 1.4, 5.0, 5.1, 5.4, 8.9, 9.0])]
    sampled = main.stratified_sample(papers, n_per_bin=1, seed=42)
    bins = {round(p["avg_score"]) for p in sampled}
    assert bins == {1, 5, 9}
    assert len(sampled) == 3
    again = main.stratified_sample(papers, n_per_bin=1, seed=42)
    assert [p["paper_id"] for p in sampled] == [p["paper_id"] for p in again]


def test_load_ground_truth(tmp_path):
    papers_dir = tmp_path / "papers"
    papers_dir.mkdir()
    with open(tmp_path / "ratings.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["paper_id", "title", "score_0", "score_1", "score_2", "avg_score", "decision", "gt_binary"])
        writer.writerow(["p1", "Paper One", "6", "8", "", "7.0", "Accept (poster)", ""])
        writer.writerow(["p2", "Paper Two", "3", "", "", "3.0", "Reject", "Reject"])
    rows, returned_papers_dir = main.load_ground_truth(tmp_path)
    assert returned_papers_dir == papers_dir
    assert rows[0]["paper_id"] == "p1"
    assert rows[0]["scores"] == [6.0, 8.0]
    assert rows[0]["gt_binary"] == "Accept"
    assert rows[1]["scores"] == [3.0]
    assert rows[1]["gt_binary"] == "Reject"


def test_load_ground_truth_missing_csv(tmp_path):
    import pytest
    with pytest.raises(FileNotFoundError):
        main.load_ground_truth(tmp_path)


def test_predict_acceptance_rate(tmp_path):
    csv_path = tmp_path / "bench.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["paper_id", "pred_score", "gt_binary"])
        writer.writerow(["a", "6.0", "Accept"])
        writer.writerow(["b", "6.0", "Reject"])
        writer.writerow(["c", "6.5", "Accept"])
        writer.writerow(["d", "3.0", "Reject"])
        writer.writerow(["e", "bad", "Accept"])
    exact_rate, exact_n, win_rate, win_n, percentile, pct_n = main.predict_acceptance_rate(str(csv_path), 6.0)
    assert exact_n == 2 and exact_rate == 0.5
    assert win_n == 3 and win_rate == 2 / 3
    assert pct_n == 4
    assert percentile == (1 + 0.5 * 2) / 4 * 100


def test_predict_acceptance_rate_missing_file(tmp_path):
    assert main.predict_acceptance_rate(str(tmp_path / "nope.csv"), 5.0) is None


def test_score_and_decision_extraction_from_merged_review():
    merged = "review text <score>7.5</score> more <decision>Accept</decision>"
    score = float(merged.split("<score>")[1].split("</score>")[0]) if "<score>" in merged else -1
    decision = (merged.split("<decision>")[1].split("</decision>")[0]) if "<decision>" in merged else "N/A"
    assert score == 7.5
    assert decision == "Accept"
