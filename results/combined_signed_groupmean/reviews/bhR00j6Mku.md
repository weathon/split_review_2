Now I'll write the final review.

## Summary

This paper presents the first systematic study of benchmark contamination detection in large reasoning models (LRMs), identifying two realistic contamination scenarios and demonstrating that existing detection methods systematically fail under both. **Stage I (pre-LRM):** contamination introduced during SFT is initially detectable but is reliably concealed by subsequent GRPO/RL training — even very short RL training (64–156 steps) drives AUROC from ~75–89% toward near-random. Through controlled ablations (Table 3) and theoretical analysis (Theorem 3.1), the paper isolates the root cause to PPO-style importance sampling and clipping, showing that removing these terms restores detectability. **Stage II (post-LRM):** extensive SFT contamination with CoT on advanced LRMs produces large performance gains while leaving detection methods near random guessing, because LRMs generalize to distributionally similar unseen samples rather than memorizing specific sequences.

---

## Strengths

- **Problem significance and timeliness.** The paper identifies a critical and timely vulnerability — as the field shifts from standard LLMs to LRMs, existing benchmark contamination detection methods systematically fail. The two-scenario framing covers realistic pathways for inflating leaderboard performance. The findings directly threaten the integrity of current LRM leaderboards.

- **Comprehensive and well-structured experimental design.** The evaluation spans 10 detection methods (generation-based, perturbation-based, reference-based, reference-free), 6 reasoning benchmarks (OlympiadBench, GPQA, AIME25, AIME24, Minerva, AMC23), and multiple base models (Qwen2.5-7B-Instruct, Llama-3.1-8B-Instruct for Stage I; DeepSeek-R1-Distill-8B/7B/14B, OpenThinker-7B for Stage II). This breadth makes the findings robust rather than method- or benchmark-specific.

- **Causal isolation of the concealment mechanism.** The ablation in Table 3 cleanly separates the contributions of different RL objective components. RAFT (no importance sampling/clipping) preserves detectability; RAFT++ and GRPO (which include it) sharply reduce it; removing clipping from RAFT++ and GRPO restores detectability. The theoretical analysis (Theorem 3.1) provides a mechanistic explanation rooted in the covariance term, showing that the importance-sampling/clipping gate differentially suppresses the NLL gap for non-members. The fact that the theory predicts the ablation results gives it real weight.

- **Ruling out alternative explanations.** The paper explicitly tests whether "the model simply forgets contamination" by continuing SFT on clean data (which does not conceal) and by training with GRPO on clean+contaminated data (which does conceal). This eliminates the most obvious confound. The monotonic AUROC decline with more GRPO steps (Figure 2) while pass@1 stays elevated is clean evidence that concealment is driven by the optimization objective, not by forgetting.

---

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Stage II claims could be more precisely scoped to the experimental setup.** The Stage II experiment evaluates *within-benchmark membership inference* (half the questions are contaminated members, half are held-out non-members). The paper's claim that "model developers could extensively contaminate their LRMs in the final stage while leaving little detectable evidence" is a reasonable extrapolation — if detectors cannot distinguish contaminated from uncontaminated items within the same benchmark, the detection task is fundamentally undermined — but the experiment does not directly test the fully-contaminated scenario (all benchmark items seen). The paper uses the standard membership-inference framing common in the literature, and the log-prob analysis (Figure 4) convincingly shows why detectors fail (generalization to distributionally similar questions). Still, acknowledging this scope distinction would strengthen precision.

- **Absence of uncertainty quantification for AUROC values.** All AUROC values are reported as point estimates without confidence intervals, standard deviations, or bootstrap estimates. For claims that detection methods are "performing near random guessing" (AUROC ≈ 50%), it would sharpen the evidence to know whether a value like 55% is statistically distinguishable from 50% given the sample size. The consistency of the pattern across 10 methods, 6 benchmarks, and multiple models strongly mitigates this concern, but it remains a precision gap.

- **No dedicated limitations section.** The paper does not explicitly discuss limitations such as: (a) the theoretical analysis uses a tabular/idealized setting with a first-order expansion, (b) experiments use relatively small base models (7B–14B), (c) RL training is short (up to 156 steps vs. the thousands used in production), and (d) only open-weight models are tested. These are reasonable scope boundaries, but stating them explicitly would improve credibility.

### Trivial
None.

---

## Nice-to-Haves

- **Cross-benchmark detection experiment for Stage II.** Adding a comparison of log-prob distributions on the contaminated benchmark vs. a held-out distribution would directly test the fully-contaminated scenario and strengthen the "barely leaves evidence" claim.
- **Cost-benefit discussion for Stage I.** The paper shows that GRPO on *clean* data conceals SFT contamination. A brief discussion of whether this is practically attractive for a malicious developer (given the cost of RL training) would add context.

---

## Removed Points

These points were raised in the input review but removed after verification:

- **"Stage II scenario is mismatched to realistic contamination incentives (structural concern)"** — The paper uses the standard membership-inference framing for contamination detection. The within-benchmark setup is the norm in this literature, and the paper's conclusion follows naturally from the evidence. Retained as a minor precision note rather than a structural concern.
- **"Practical feasibility of Stage I is underspecified"** — This is a nice-to-have suggestion about cost-benefit analysis, not a genuine weakness of the scientific contribution.
- **"Related works brief / reads as taxonomy"** — Subjective; the paper adequately cites relevant work and frames it relative to the LRM setting.
- **"No discussion of limitations"** — Moved to Minor; it is a presentation gap but the content limitations are implicitly scoped.
- **"Table 1 anomaly (higher pass@1 with SFT alone than SFT+RL)"** — Minor curiosity; the pattern is model-specific (only Qwen, not Llama) and likely reflects short RL training. Not a weakness.

---

## Novel Insights

None beyond the paper's own contributions. The Harsh Critic perceptively notes that the Stage II discussion (lines 330–331) — that LRMs internalize knowledge rather than memorize sequences, enabling generalization to distributionally similar questions — is the paper's most insightful paragraph and could be elevated.

---

## Suggestions

1. Add a limitations section acknowledging the idealized theoretical setting, model scale, limited RL steps, and open-weight-only testing.
2. Add bootstrap confidence intervals for key AUROC values in Tables 2 and 5 to sharpen the "near random guessing" claims.
3. Reframe Stage II claims slightly to reflect the within-benchmark membership inference framing used, noting the natural extension to the fully-contaminated scenario.

---

## Score and Decision

**Calibration summary (all anchors retrieved):**

| Path | Avg | Round | Itemized? | Comparison |
|------|-----|-------|-----------|------------|
| `5kMwiMnUip` (jailbreaking) | 1.40 | R1 | No | Irrelevant topic; very weak paper |
| `8QTpYC4smR` (LLM survey) | 1.00 | R1 | No | Literature review; no comparison |
| `nSDOkm0SKo` (financial NN) | 1.00 | R1 | No | Irrelevant topic |
| `gwZ90hFSL2` (humanoid robots) | 1.00 | R1 | No | Irrelevant topic |
| `ly10tMV6cD` (structure-rich text bench) | 3.25 | R1 | No | Weak benchmark paper, minimal overlap |
| `JQbqaQjV7D` (traffic LLM bench) | 3.00 | R1 | No | Unrelated domain |
| `NlY3XppPt3` (computational models) | 2.00 | R1 | No | Unrelated |
| `koza5fePTs` (planning benchmark) | 2.00 | R1 | No | Unrelated |
| **`Nk1MegaPuG` (Evading Detection)** | **4.25** | **R1** | **Yes** | **Most directly comparable; this paper is far stronger in rigor, theory, and presentation** |
| `aRqyX0DsmW` (lab safety bench) | 4.00 | R1 | No | Unrelated domain |
| `rAylWUIKtu` (Benchmark Inflation) | 4.25 | R1 | No | Related topic but different methodology |
| `QiyQJqpcYe` (linguistic reasoning) | 4.75 | R1 | No | Unrelated |
| **`m2NVG4Htxs` (Cutoff longitudinal)** | **6.75** | **R1/R2** | **Yes** | **Comparable quality; this paper adds theoretical mechanism** |
| **`zWqr3MQuNs` (Detecting Pretraining)** | **6.25** | **R1** | **Yes** | **Comparable; this paper has broader experimental scope** |
| **`Nsms7NeU2x` (Forget Contamination)** | **6.75** | **R1/R2** | **Yes** | **Comparable; this paper's theoretical analysis is more directly validated** |
| `hpeyWG1PP6` (TDDBench) | 5.75 | R2 | No | Related topic (MIA benchmark) but narrower scope |
| `dRel8fuUK4` (RMIA membership) | 6.00 | R2 | No | Related (membership inference) but different focus |
| `86zAUE80pP` (CPPO RLHF) | 6.25 | R2 | No | RL alignment, not contamination |
| `Wf2ndb8nhf` (Manipulation in RL) | 6.33 | R2 | No | RL safety, tangential |
| `gkfUvn0fLU` (Constrained RLHF) | 7.00 | R2 | No | RLHF overoptimization, tangential |

**Round 1 bracket:** The paper sits between the 4.25 "Evading Detection" anchor (where it clearly dominates on every dimension) and the 6.25–6.75 contamination anchors. The strongest comparators — "To the Cutoff" (6.75), "Detecting Pretraining Data" (6.25), "How much can we Forget" (6.75) — all have comparable experimental rigor but none provide a theoretically grounded causal mechanism identifying *why* detection fails. The paper under review's Theorem 3.1 and Table 3 ablations, combined with broader benchmark coverage, place it above these anchors. **Bracket: 6.5–7.5.**

**Narrowing:** Compared to "How much can we Forget" (6.75, rejected despite high raw scores due to its theoretical bounds being loose and questions about practical applicability), the current paper's theory is directly validated by ablations (Table 3) and its practical implications are clear and immediately actionable for the LRM evaluation community. Compared to "Detecting Pretraining Data" (6.25, accepted), the current paper has broader experimental scope (10 methods × 6 benchmarks × multiple models vs. a single Wikipedia dataset) and a deeper scientific contribution (mechanistic explanation, not just a new detection heuristic). This places the paper solidly in the **6.5–7.5 bracket**, leaning toward the upper end.

**Final score: 7.0** — The paper makes a well-supported, important contribution that should influence how the community evaluates contamination detection in the LRM era. The core finding (RL with PPO-style importance sampling/clipping systematically erodes detection signals) is convincingly demonstrated through broad benchmarking, controlled ablations, and supporting theory. The Stage II finding is also significant. The minor weaknesses (scope precision, missing uncertainty quantification, no limitations section) do not threaten the core contribution.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>