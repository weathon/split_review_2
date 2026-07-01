Now I have all the information I need. Let me produce the final consolidated review.

---

## Summary

This paper proposes **Steady Thought (ST)**, a training-time framework that operates at the granularity of individual reasoning "thoughts" (rather than entire responses) to mitigate the "under-thinking" phenomenon in Large Reasoning Models (LRMs) — where models prematurely abandon promising reasoning trajectories. ST consists of three stages: entropy-based thought segmentation, forced-completion of each thought via logit suppression, and thought-level preference optimization (STPO) that teaches the model to commit to promising thoughts while preserving exploration ability. Experiments across three model scales (1.5B–14B) and four benchmarks show consistent accuracy improvements (up to 5.3%) alongside substantial token reductions (19%–39.3%), including on out-of-distribution code tasks.

---

## Strengths

1. **Well-motivated problem with concrete evidence.** The paper demonstrates the under-thinking phenomenon empirically (Figures 1a, 1b) by showing that models often identify the correct path early yet continue switching — a genuine, practically relevant failure mode that practitioners observe.

2. **Novel and principled technical approach.** Operating preference optimization at the *thought level* (rather than token-level suppression as in NOWAIT or representation-level steering as in SEAL) is a legitimate advance. The three-stage pipeline (segment → complete → optimize) is coherent and directly targets the identified problem: teaching the model *when* to commit versus *when* to explore.

3. **Consistently positive results across diverse settings.** ST improves accuracy while reducing tokens across nearly all model/dataset combinations. The OOD generalization on LiveCode (e.g., Qwen3-8B: 71.8% → 77.1%) is a meaningful signal that the method learns a generalizable pattern. The AIME 2024 improvements (e.g., 60.4% → 65.4% on 14B) are practically meaningful.

4. **Informative ablation study.** Table 4 cleanly demonstrates that STPO's length-normalized, thought-conditional design outperforms both SFT and DPO on the same data, strengthening the case for the specific algorithmic choices.

---

## Weaknesses

### Fatal
None.

### Major

1. **The NOWAIT baseline on Qwen3-8B appears broken, inflating ST's relative advantage.** On Qwen3-8B, NOWAIT's accuracy collapses to 61.0% on MATH500 (from 91.4% vanilla) and 26.3% on AIME2024 (from 62.1% vanilla), while token count *increases* by 84.6% on MATH500. This is far worse than vanilla — the opposite of what an under-thinking mitigation method should produce. The most plausible explanation is that NOWAIT's logit-suppression hyperparameters were not tuned for this model. Including this configuration without tuning compromises the fairness of the comparison. The paper should either tune NOWAIT per model and report best-case results, or explicitly acknowledge the tuning gap and qualify the comparison.

2. **No statistical variance is reported, making it impossible to assess whether improvements are reliable.** The paper states only that AIME2024 results are averaged over 8 runs and LiveCode over 2 runs, but no standard deviations, confidence intervals, or error bars appear anywhere. For AIME 2024 (30 problems), a difference of 3.7 percentage points (e.g., 27.5% → 31.2% on 1.5B) represents roughly 1 additional correct problem — easily within noise without variance estimates. For MATH500 and GSM8K, no run count is mentioned at all. Given that the headline "up to 5.3%" improvement is emphasized in the abstract, this evidential gap is significant.

### Minor

3. **The paper's own data contains a clear counterexample to its central narrative that is explained away rather than analyzed.** On DeepSeek-R1-Distill-Qwen-1.5B for AIME2024 (Figure 2), the average thought count *increases* by 41% (12.87 → 18.21) and the proportion of last thought *decreases* (18.96% → 15.66%). The paper acknowledges this but frames it positively without rigor. More problematically, the paper claims "the final thought consistently accounted for a larger proportion of the total response" — this is factually contradicted by the paper's own data for this setting. A careful analysis of *when* the model switches more and why that improves accuracy would strengthen rather than weaken the paper.

4. **The formalization in Section 2.1 (Steadiness Score, Bradley-Terry model) is decorative.** The paper introduces an abstract scoring function and Bradley-Terry preference formulation, claiming it "provides a powerful new lens," but this framework is never operationalized. The actual method (STPO, Equation 7) is simply SimPO applied at the thought level — using average log-probability as the implicit reward. The formal apparatus in Section 2.1 could be removed without affecting the technical contribution. The paper should either instantiate the Steadiness Score directly or present the method without the mismatched framing.

5. **The method's dependence on ground-truth answers is not discussed as a limitation.** The Thought Completion stage determines correctness by checking against ground-truth labels (Section 3.2). This means ST cannot be applied to open-ended reasoning or generation tasks without verifiable outcomes. The paper should acknowledge this scope limitation.

6. **The PCT metric's underlying assumption conflates outcome with process.** Section 4.4.2 equates all abandoned correct intermediate thoughts with "Invalid Switches." However, a correct thought that is abandoned might be abandoned because the model correctly detects an error or dead end — the metric cannot distinguish between wasteful switching and justified re-exploration. This ambiguity weakens the PCT result as evidence.

### Trivial
None.

---

## Nice-to-Haves

- **Hyperparameter-tuned baselines.** If NOWAIT is sensitive to suppression strength or keyword choice, tuning it per model and reporting the best configuration would provide a fairer comparison.
- **Statistical variance reporting.** Adding standard deviations or confidence intervals — especially for the small AIME 2024 set — would resolve the most significant evidential gap.
- **Training compute cost.** The pipeline involves multiple inference passes (generation, segmentation, forced completion, preference training). A brief summary of the computational overhead in the main text would help practitioners assess practicality.
- **Failure case analysis.** GSM8K improvements are marginal; understanding when ST does not help (e.g., simpler problems? problems where the first correct thought appears very late?) would sharpen the contribution.

---

## Removed Points

These points were identified in the input review but are removed with justification:

- **"NoThink is a strawman"** — NoThink is a published baseline from the literature (Ma et al., 2025). It is clearly a lower-bound reference (skipping thinking entirely), not positioned as a competitive method. The critic over-characterizes this.
- **"Acc[%]↓ arrow direction is confusing"** — Formatting artifact from the PDF parser; not present in the original submission.
- **"SEAL's improvements are modest"/"SEAL is an easy target"** — Generic criticism that does not identify a specific flaw; the reported results are what they are.
- **"No discussion of training compute cost"** — The paper references Appendix E for this detail. Per instructions, missing appendix content cannot be penalized.
- **"The 'Overall' column averages across datasets of different difficulties"** — All per-dataset results are individually reported in the same table. The average column is auxiliary and not misleading when the full data is visible.

---

## Novel Insights

None beyond the paper's own contributions. The input review did not surface genuinely novel observations about the paper that the authors themselves missed. The counterexample in Figure 2 (1.5B/AIME2024) is noted in the paper but insufficiently analyzed; this is a gap to address rather than a novel insight.

---

## Suggestions

1. **Report variance for all main results.** Run each condition with at least 3–5 seeds and include standard deviations or confidence intervals. This is the single highest-leverage improvement.
2. **Tune baselines per model or qualify the comparison.** If NOWAIT is sensitive to its hyperparameters, either find the best configuration for each model or clearly state that the reported results reflect default settings and may understate the baseline's performance.
3. **Correct the overclaim in Section 4.4.1** — the final-thought proportion does *not* increase on the 1.5B/AIME2024 setting; the text should not claim "consistently."
4. **Either operationalize the Steadiness Score or remove the formal apparatus** from Section 2.1 to match what the method actually does.
5. **Acknowledge the ground-truth limitation** explicitly in a "Limitations" paragraph.
6. **Clarify the PCT metric** by discussing the assumption that all abandoned correct thoughts represent invalid switches, and what scenarios this might misclassify.

---

## Score and Decision

The paper presents a genuinely novel idea — thought-level preference optimization for mitigating under-thinking — supported by a coherent pipeline and consistently positive results across multiple models and benchmarks. However, two significant evidential weaknesses prevent full confidence in the reported improvements: (a) a baseline (NOWAIT on Qwen3-8B) appears to be configured in a way that produces pathologically poor results, inflating ST's apparent advantage, and (b) the complete absence of statistical variance reporting makes it impossible to assess whether the often modest accuracy gains (1–4 pp) are reliable or within noise. These are addressable issues, not structural flaws. The core method is sound and the direction is worthwhile.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>