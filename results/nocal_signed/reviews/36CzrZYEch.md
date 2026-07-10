Now I have the impact scores. Let me finalize the review and assign a score.

The key signals:
- The core observation (+9.6) and thorough ablations (+7.3 to +9.2) are very strong
- The missing temperature baseline (-8.6) is the most critical gap
- Overclaimed results (-6.8) is another significant issue
- The Fig. 2 confound (-1.8) and minor issues (-1.0, -0.2) are less impactful

The paper has a genuine contribution but needs to address the mechanism question and calibrate its claims. Let me write the final review.

## Summary
This paper proposes IRIS, a framework that uses Negative Self-Certainty (NSC) — the KL divergence between the model's output distribution and a uniform distribution — as an intrinsic reward for RL-based fine-tuning of autoregressive text-to-image models. The key insight is that while maximizing self-certainty improves LLM reasoning, minimizing self-certainty improves T2I generation. IRIS requires no external reward models, human labels, or domain-specific verifiers, yet achieves results close to those obtained with external-reward baselines on GenEval, T2I-CompBench, and WISE.

## Strengths
- **Genuine and non-trivial empirical observation (Fig. 2):** The finding that RL training with external rewards *decreases* self-certainty on image tokens in T2I models while *increasing* it on text tokens in LLM reasoning challenges the assumption that "more confident = better" generalizes across modalities. This observation is the paper's most valuable contribution and is well-supported by the data shown.
- **Clean and simple method (Sec. 3.2):** The NSC reward design — negative KL( U ∥ π_θ ) — is conceptually straightforward, requires no external models, no human labels, and no domain-specific verifiers. The simplicity is a genuine strength for practical applicability.
- **Thorough ablation study (Sec. 4.3):** The paper systematically ablates CoT vs. no CoT, maximizing vs. minimizing image/text self-certainty, forward vs. backward KL, and RL vs. direct optimization. This provides clear evidence for the design choices and is one of the more comprehensive ablation studies in this space.
- **Multi-benchmark evaluation:** Results on GenEval (object-level), T2I-CompBench (compositional), and WISE (world-knowledge) provide a broader assessment than a single benchmark.

## Weaknesses

### Major
1. **Missing control: inference-time temperature increase.** The NSC reward pushes the output distribution toward uniform. The paper never compares against simply increasing the sampling temperature of the base model at inference time. If higher temperature (which also flattens the output distribution) produces similarly rich images from the base model, then the claimed mechanism may be reducible to increased stochasticity, and the RL training may be unnecessary. This is the single most critical missing experiment. The paper shows that direct NSC optimization (without RL) collapses (Fig. 9), which partly suggests the mechanism is not *just* about flattening the distribution, but a direct temperature baseline on the three evaluation benchmarks is needed to rule out the simpler hypothesis.

2. **Headline claims are overstated relative to the data.** The abstract claims IRIS achieves performance "competitive with or superior to external rewards." Across Table 1, IRIS is consistently *slightly worse* than T2I-R1 on most aggregate metrics (GenEval 1B: 0.72 vs. 0.75; WISE 7B: 0.48 vs. 0.50; GenEval 7B: 0.77 vs. 0.78). The paper further claims advantages on "natural science" subcategories of WISE, but Table 1(c) shows ties or negligible differences (Biology: 0.36 vs. 0.36; Chemistry: 0.22 vs. 0.22; Physics: 0.45 vs. 0.43). IRIS achieving ~95% of external-reward performance with *no supervision at all* is a noteworthy and publishable finding on its own; overclaiming it as "superior" undermines the paper's credibility.

### Minor
3. **Fig. 2 compares across confounded variables.** The central observation plots text-token self-certainty from Qwen2.5-1.5B-Instruct (trained on math reasoning) against image-token self-certainty from Janus-Pro-1B (trained on T2I). Both the model architecture *and* the task differ, so the observed difference cannot be cleanly attributed to token modality. This does not invalidate the observation, but it weakens the claim that "self-certainty exhibits task-dependent behaviors" — the dependence could be on model architecture, training objective, or evaluation domain.

4. **Improvement percentages inconsistent with Table 1.** The paper claims a 28.8% improvement on WISE for the 1B model. From Table 1(c): base = 0.28, IRIS = 0.37 gives (0.37-0.28)/0.28 ≈ 32.1%, not 28.8%. The 13.3% claimed for T2I-CompBench cannot be verified from Table 1(b) as it has no "overall" column for the base model. These discrepancies need clarification.

5. **Chat template discrepancy not quantified.** The paper notes (lines 120-121) that the T2I-R1 baseline used an incorrect chat template and reports its own numbers using the correct one. However, it does not report the original T2I-R1 numbers or the magnitude of the template effect, making it hard for readers to assess comparison fairness.

### Trivial
None.

## Nice-to-Haves
- Run training beyond 800 steps on at least one setting to check for stability or collapse under continued NSC optimization.
- Explicitly state the training prompt distribution in the main text (likely deferred to the now-stripped appendix).
- Include qualitative analysis of how token-level distributions actually change during IRIS training (e.g., do individual token probabilities become more uniform?).

## Removed Points
The following points from the input review were removed:
1. **Training data not specified in main text** — Removed per hard rule: the appendix (stripped by the parser) would contain training details; the paper states it follows the T2I-R1 protocol. The criticism conflates a missing-appendix issue with a missing-main-text issue.
2. **Pure formatting/style nitpicks and section-by-section observations** — Removed per instructions; these are parser artifacts or generic observations that do not rise to the level of actionable weaknesses.

## Novel Insights
None beyond the paper's own contributions. The reviews surface the tension between the paper's genuine empirical contribution and its overclaimed framing, but do not introduce entirely new analytical angles.

## Suggestions
- Add a controlled experiment comparing IRIS-trained models against the base model at several sampling temperatures (e.g., T=0.8, 1.0, 1.2, 1.5) on all three benchmarks to rule out the "increased stochasticity" hypothesis.
- Calibrate the contribution claims: "IRIS achieves results comparable to external-reward baselines without any supervision, closing ~95% of the gap" is accurate and still compelling.
- Clarify the improvement percentages: specify which checkpoint(s) the 9.1%/13.3%/28.8% numbers refer to and reconcile with Table 1.
- Report the original (incorrect-template) T2I-R1 numbers alongside the corrected ones to quantify the template effect.

## Score and Decision

The paper makes a genuine contribution: it demonstrates that an intrinsic reward (negative self-certainty) can substitute for expensive external reward models in T2I, achieving results close to external-reward baselines. The ablation study is thorough, and the core observation about modality-dependent self-certainty behavior is interesting and worth communicating. However, the paper suffers from two significant weaknesses: the missing temperature baseline leaves the mechanism under-characterized, and the overclaimed results damage the paper's credibility. These are addressable with additional experiments and more measured framing, and they do not invalidate the core contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>