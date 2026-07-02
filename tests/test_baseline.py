import csv

import pytest

import baseline


def test_parse_review_regex_path():
    text = "review body\nMY FINAL SCORE: <score>6.5</score>\nMY FINAL DECISION: <decision>Accept</decision>"
    score, decision, cost = baseline.parse_review(text)
    assert score == 6.5
    assert decision == "Accept"
    assert cost == 0.0


def test_parse_review_whitespace_and_negative():
    text = "<score> -100 </score> <decision> Error </decision>"
    score, decision, cost = baseline.parse_review(text)
    assert score == -100.0
    assert decision == "Error"
    assert cost == 0.0


def test_parse_review_rejects_non_decision_word():
    match = baseline.re.search(r"<decision>\s*(Accept|Reject|Error)\s*</decision>", "<decision>Maybe</decision>")
    assert match is None


def test_load_ground_truth(tmp_path):
    with open(tmp_path / "ratings.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["paper_id", "title", "score_0", "score_1", "avg_score", "decision", "gt_binary"])
        writer.writerow([" p1 ", " Paper One ", "6", "8", "7.0", "Accept (poster)", "Accept"])
        writer.writerow(["p2", "Paper Two", "3", "", "3.0", "Reject", "Reject"])
    rows, papers_dir = baseline.load_ground_truth(tmp_path)
    assert papers_dir == tmp_path / "papers"
    assert rows[0]["paper_id"] == "p1"
    assert rows[0]["title"] == "Paper One"
    assert rows[0]["scores"] == [6.0, 8.0]
    assert rows[0]["avg_score"] == 7.0
    assert rows[1]["scores"] == [3.0]


def test_load_ground_truth_missing_csv(tmp_path):
    with pytest.raises(FileNotFoundError):
        baseline.load_ground_truth(tmp_path)
