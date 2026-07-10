## Summary

This paper proposes IRIS (Intrinsic Reward Image Synthesis), the first framework to train autoregressive text-to-image (T2I) models via reinforcement learning using only an intrinsic reward signal — negative self-certainty (NSC) — without external reward models, human labels, or domain-specific verifiers. The key insight is that while maximizing self-certainty helps text-domain reasoning (as shown by prior work), minimizing self-certainty benefits T2I generation by producing more visually rich images. Applied to Janus-Pro 1B and 7B models, IRIS achieves results competitive with external-reward baselines (T2I-R1) across GenEval, T2I-CompBench, and WISE, while being more general and scalable.

## Strengths

- **Novel and well-motivated problem framing.** IRIS is the first RL-based alignment method for T2I that uses only an intrinsic reward, without any external reward model, human labeling, or domain-specific verifier. This is a genuine gap in the literature, and the idea of using the model's own output-distribution uncertainty as a training signal is clean and potentially general.

- **Non-trivial empirical finding.** The core result — that minimizing (rather than maximizing) self-certainty helps image generation — is counterintuitive given the prevailing narrative in LLM reasoning (Zhao et al. 2025b; Zhang et al. 2025a). The qualitative evidence in Figure 1 is compelling, and the contrast with text-domain findings is a useful contribution independent of the method.

- **Thorough ablation study (Section 4.3).** The paper systematically isolates each design choice: with/without CoT, maximize vs minimize image SC, maximize vs minimize text SC, forward vs backward KL, and RL vs direct optimization. Figures 5–9 cleanly demonstrate that each component of IRIS contributes positively. The optimize-without-RL ablation (Fig. 9) convincingly shows that naive direct optimization collapses, providing a solid justification for the GRPO-based approach.

- **Multi-benchmark evaluation across three diverse benchmarks (GenEval, T2I-CompBench, WISE) at two model scales (1B and 7B).** This covers object-level, compositional, and knowledge-grounded generation, which is more comprehensive than many T2I alignment papers.

- **Responsible disclosure of a baseline implementation discrepancy.** The paper identifies and corrects a chat template inconsistency in the official T2I-R1 implementation (line 120), demonstrating good scientific practice.

## Weaknesses

### Major

- **The central motivating observation (Figure 2) comparing self-certainty trajectories is confounded across multiple dimensions simultaneously.** Figure 2 compares self-certainty on *text* tokens of Qwen2.5-1.5B-Instruct (trained on math reasoning) against self-certainty on *image* tokens of Janus-Pro-1B (trained on T2I). These differ in model family, architecture, training task, training data, and token modality. The paper's claim that "self-certainty exhibits task-dependent behaviors" (Section 1, line 49) attributes the observed difference to *task type*, but the evidence does not isolate this factor — the difference could equally be due to different model initialization, token distributions, or training dynamics. This weakens a headline claim. That said, the paper's core method (IRIS) is independently validated by within-model ablation studies (Figures 6, 7) that show minimizing SC helps T2I on the *same* Janus-Pro model — so this confound affects the motivating observation, not the validity of the method itself.

### Minor

- **The training prompt dataset used for RL fine-tuning is not specified.** The paper says it "primarily follow[s] the protocol in T2I-R1" (line 110) but does not state the source, size, or distribution of training prompts, nor whether training prompts overlap with evaluation benchmarks. This is a reproducibility gap that the authors should address.

- **The claim that IRIS is "superior to" external rewards is overstated relative to the data.** In Table 1, IRIS is competitive with but generally slightly behind T2I-R1 on most metrics: GenEval 1B (0.72 vs 0.75), GenEval 7B (0.77 vs 0.78), T2I-CompBench 7B (lags on Shape, Texture, 2D-Spatial), WISE 1B (0.37 vs 0.38), WISE 7B (0.48 vs 0.50). The abstract's phrasing "competitive with or superior to" and the body's "surpasses the T2I-R1 on 1B models" are somewhat generous. The paper is strongest when it claims *competitiveness*, not superiority.

- **The main results (Table 1) report best-checkpoint performance over 8 checkpoints (steps 100–800) rather than final checkpoint performance.** This is disclosed in both the text and table caption, and applied equally to both methods, so the relative comparison is fair. However, the reported absolute improvement percentages (9.1%, 13.3%, 28.8%) reflect an optimistic selection. Reporting final-checkpoint numbers alongside would improve transparency for practitioners.

- **Standard image quality metrics (FID, CLIP score, etc.) are not reported.** The paper relies on GenEval, T2I-CompBench, and WISE which measure specific semantic/alignment capabilities. While HPSv2 (used in ablations) partially addresses aesthetic quality, a reader might ask whether NSC-based training improves perceptual quality or just alignment with certain automated metrics.

### Trivial

None.

## Nice-to-Haves

- A more mechanistic account of *why* minimizing SC improves T2I alignment (beyond "less confident models produce richer images"). For instance, analyzing the correlation between per-sample SC and per-sample quality scores, or characterizing the types of errors made by high-SC vs low-SC models.
- An ablation of the number of group samples *G* in GRPO (the paper fixes G=8 text generations per prompt).
- Reporting standard image quality metrics (FID, CLIP score) alongside the alignment benchmarks.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **Abstract phrasing criticism:** The reviewer claimed the abstract conflates "low uncertainty" with "high self-certainty." In fact, the abstract is internally consistent — "low uncertainty" = "high self-certainty," and the paper correctly states this leads to simple/uniform images. This is a misreading.
- **Ablation metrics concern:** The reviewer noted that the ablation metrics (HPSv2, DINO, GIT, ORM) are the same four reward models used to train T2I-R1. The paper explicitly addresses this (line 211), noting they are "simple and unbiased" because IRIS doesn't train on them. The reviewer acknowledged this is not a flaw.
- **Chat template criticism:** The reviewer mentioned the chat template issue means all baselines are re-implementations. The paper discloses this responsibly (line 120). Not a weakness.
- **Missing group-sample ablation / failure mode analysis / FID metrics:** These are generic nice-to-haves, not specific weaknesses.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Deconfound the Figure 2 observation (or caveat it explicitly).** The cleanest fix within the paper's own framing would be to take the *same* multimodal model (Janus-Pro) and compare SC trajectories when trained on (a) a text reasoning task and (b) a T2I task with external rewards. If this is infeasible, the paper should explicitly acknowledge the confounds (different models, token modalities, training tasks) and temper the "task-dependent behaviors" claim.
2. **Report final-checkpoint performance** alongside best-checkpoint performance in Table 1 for full transparency.
3. **Specify the training prompt distribution** (source, size, whether it overlaps with evaluation benchmarks).
4. **Tone down claims of "superiority"** over external rewards — the data consistently shows competitiveness but slight underperformance on most metrics.
5. **Add a discussion of failure modes** where IRIS underperforms T2I-R1 (e.g., Counting and Color Attribution in GenEval; Shape, Texture, and 2D-Spatial in T2I-CompBench).

---

**Calibration report.** All retrieved anchors:

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| bO31lfEdos | 5.00 | 1 | Yes | Human-free RL for LVLM hallucination mitigation. Much weaker — has severe weaknesses (-9.98, -9.34, -8.64) that IRIS lacks. |
| Let8OMe20n | 6.00 | 1 | Yes | Confidence-aware reward optimization for T2I. Similar strength but IRIS has stronger novelty (first without external rewards). |
| kIP0duasBb | 6.67 | 1 | Yes | TTA with CLIP reward. IRIS avoids the severe novelty/relevance weaknesses (-10.00, -8.40) that pulled RLCF down. |
| 4w99NAikOE | 6.80 | 1 | Yes | IterComp for compositional T2I. Strong theory (+10.00) and results (+10.00) but also severe weaknesses (-9.99, -9.31). IRIS is slightly below due to the Figure 2 confound. |
| RcANissyP4 | 5.67 | 2 | No | SelfEval for T2I evaluation. Less relevant architecturally; lower impact. |
| ITq4ZRUT4a | 6.00 | 2 | No | Davidsonian Scene Graph for T2I evaluation. Less relevant. |
| eC2ICbECNM | 6.00 | 2 | No | Ctrl-U for uncertainty-aware reward. Less relevant. |
| tmBKIecDE9 | 7.25 | 2 | Yes | Motif (intrinsic reward from LLM for RL agents). Very clean execution without the Figure 2 confound issue. IRIS is below this. |
| 5BSlakturs | 7.33 | 2 | Yes | Reliable random seeds for compositional T2I. Has severe weaknesses (-9.90, -9.17, -8.85). IRIS is roughly comparable. |
| Im2neAMlre | 7.33 | 2 | No | T2I evaluation methodology. Less relevant. |

**Round 1 bracket:** 5.5–7.0. The paper lacks the fatal weaknesses of sub-5 papers and doesn't have the theoretical depth or execution cleanness of 7.5+ papers.

**Narrowing:** Comparing scored items: IRIS's strongest items (novelty +9.59, insight +9.17, ablation +9.94, evaluation +8.15) are comparable to Let8OMe20n (+9.63, +9.09) and 4w99NAikOE (+8.54, +10.00, +10.00) but IRIS's main weakness (Figure 2 confound, -2.96) is non-trivial — it's a methodological gap in a headline claim, unlike the near-zero-impact weaknesses at 6.00–6.80 anchors. However, this weakness does not invalidate the core method (which is validated by within-model ablations), placing IRIS above the 6.00 papers but below the clean 7.25+ papers. Final score: **6.5**.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>