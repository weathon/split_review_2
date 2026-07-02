import csv

import matplotlib
matplotlib.use("Agg")
import numpy as np
import pandas as pd

import metric


def make_df():
    return pd.DataFrame([
        {"pred_score": 6.0, "gt_avg_score": 7.0, "gt_binary": "Accept", "gt_score_0": 6.0, "gt_score_1": 8.0},
        {"pred_score": 4.0, "gt_avg_score": 4.0, "gt_binary": "Reject", "gt_score_0": 3.0, "gt_score_1": 5.0},
    ])


GT_COLS = ["gt_score_0", "gt_score_1"]


def test_round_to_scale():
    assert metric.round_to_scale(6.4) == 6
    assert metric.round_to_scale(7.1) == 8
    assert metric.round_to_scale(0.0) == 1
    assert metric.round_to_scale(11.0) == 10


def test_spearman_and_pearson_ci():
    lo, hi = metric.spearman_ci(0.8, 50)
    assert lo < 0.8 < hi
    assert -1 <= lo and hi <= 1
    assert metric.pearson_ci(0.8, 50) == (lo, hi)


def test_mae_ci():
    errors = [1.0, 2.0, 3.0, 4.0]
    lo, hi = metric.mae_ci(errors)
    assert lo < 2.5 < hi


def test_auroc_ci():
    lo, hi = metric.auroc_ci(0.8, 20, 30)
    assert 0 <= lo < 0.8 < hi <= 1


def test_max_f1_at_threshold():
    f1, threshold = metric.max_f1_at_threshold([0, 0, 1, 1], [1.0, 2.0, 3.0, 4.0])
    assert f1 == 1.0
    assert threshold == 3.0


def test_paired_bootstrap_ci_and_pvalue():
    values = list(np.linspace(1, 2, 100))
    lo, hi = metric.paired_bootstrap_ci(values)
    assert 1 <= lo < hi <= 2
    assert metric.paired_bootstrap_pvalue(values) == 0.0
    assert metric.paired_bootstrap_pvalue([-1, 1]) == 1.0


def test_build_one_vs_rest_arrays_by_paper():
    out = metric.build_one_vs_rest_arrays_by_paper(make_df(), GT_COLS)
    assert out["pred"].shape == (2,)
    assert out["gt_avg"].shape == (2,)
    assert len(out["rest_means_by_paper"]) == 2
    np.testing.assert_array_equal(out["rest_means_by_paper"][0], [8.0, 6.0])
    np.testing.assert_array_equal(out["heldout_scores_by_paper"][0], [6.0, 8.0])
    single = pd.DataFrame([{"pred_score": 5, "gt_avg_score": 5, "gt_score_0": 5, "gt_score_1": None}])
    assert metric.build_one_vs_rest_arrays_by_paper(single, GT_COLS) is None


def test_one_vs_rest_baseline():
    out = metric.one_vs_rest_baseline(make_df(), GT_COLS)
    assert out["n_pairs"] == 4
    assert out["n_papers"] == 2
    assert out["mae"] == 2.0
    assert out["rest_means"] == [8.0, 6.0, 5.0, 3.0]
    assert out["heldout_scores"] == [6.0, 8.0, 3.0, 5.0]
    assert out["paper_decisions"] == ["accept", "accept", "reject", "reject"]


def test_one_vs_one_baseline():
    out = metric.one_vs_one_baseline(make_df(), GT_COLS)
    assert out["n_pairs"] == 2
    assert out["n_papers"] == 2
    assert out["mae"] == 2.0
    assert out["a_scores"] == [6.0, 3.0]
    assert out["b_scores"] == [8.0, 5.0]


def test_split_half_baseline():
    out = metric.split_half_baseline(make_df(), GT_COLS)
    assert out["n_pairs"] == 2
    assert out["half_a"] == [6.0, 3.0]
    assert out["half_b"] == [8.0, 5.0]
    assert out["mae"] == 2.0
    assert out["pearson"] == 1.0


def bigger_df(n=12):
    rng = np.random.default_rng(0)
    rows = []
    for i in range(n):
        gt = float(rng.uniform(2, 9))
        s0 = round(min(10, max(1, gt + rng.normal(0, 1))))
        s1 = round(min(10, max(1, gt + rng.normal(0, 1))))
        s2 = round(min(10, max(1, gt + rng.normal(0, 1))))
        avg = (s0 + s1 + s2) / 3
        rows.append({
            "paper_id": f"paper{i}",
            "pred_score": float(min(10, max(1, gt + rng.normal(0, 1.5)))),
            "pred_decision": "Accept" if gt >= 5.5 else "Reject",
            "gt_avg_score": avg,
            "gt_decision": "Accept (poster)" if avg >= 5.5 else "Reject",
            "gt_binary": "Accept" if avg >= 5.5 else "Reject",
            "match": "YES",
            "cost": 0.0,
            "sdk_savings": 0.0,
            "gt_score_0": float(s0),
            "gt_score_1": float(s1),
            "gt_score_2": float(s2),
            "gt_score_3": None, "gt_score_4": None, "gt_score_5": None, "gt_score_6": None,
        })
    return pd.DataFrame(rows)


def test_ai_vs_one_vs_rest_shape():
    out = metric.ai_vs_one_vs_rest(bigger_df(), [f"gt_score_{i}" for i in range(7)], n_boot=50)
    for key in ["spearman", "pearson", "mae", "slope", "intercept"]:
        assert np.isfinite(out[f"{key}_diff"])
        lo, hi = out[f"{key}_ci"]
        assert lo <= hi
        assert 0 <= out[f"{key}_p"] <= 1
    assert out["n_boot"] == 50


def test_ai_vs_one_vs_one_shape():
    out = metric.ai_vs_one_vs_one(bigger_df(), [f"gt_score_{i}" for i in range(7)], n_boot=50)
    for key in ["spearman", "pearson", "mae"]:
        assert np.isfinite(out[f"{key}_diff"])
        lo, hi = out[f"{key}_ci"]
        assert lo <= hi
        assert 0 <= out[f"{key}_p"] <= 1


def test_analyze_and_plot_end_to_end(tmp_path, capsys):
    df = bigger_df(20)
    # missing prediction row and a blacklisted paper must both be dropped
    df.loc[0, "pred_score"] = -1
    df.loc[1, "paper_id"] = "rzGEfYr2ZC"
    csv_path = tmp_path / "fake_bench.csv"
    df.to_csv(csv_path, index=False)

    metric.analyze_and_plot(str(csv_path))

    out = capsys.readouterr().out
    assert "Dropped 1/20 papers" in out
    assert "Excluded 1 admin-rejected papers" in out
    assert "Papers: 18" in out
    assert "Spearman (raw):" in out
    assert "AUROC (score→A/R):" in out
    assert (tmp_path / "fake_bench_scatter.png").exists()
