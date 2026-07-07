Now I have all the information I need. Let me compile the final review.

Here is the final review.

---

## Summary

This paper introduces High-Entropy Sum (HES), a metric that scores reasoning samples by summing the entropy of only the top 0.5% highest-entropy tokens, motivated by the idea that critical "forking tokens" carry most of the signal about reasoning complexity. HES is validated across three training paradigms (SFT, RFT, RL) by using it to select training data. Key findings include: (1) training on the top 20% of HES-ranked SFT data matches or exceeds full-dataset performance, (2) small models (0.6B) can screen data for larger models via HES, and (3) in RL, selecting high-HES successful trajectories paired with random failures outperforms full-batch training.

## Strengths

- **Broad empirical validation across three training paradigms (SFT, RFT, RL).** Most data selection papers evaluate on a single paradigm. This paper tests HES on SFT (Tables 1–4), RFT (Table 5), and RL (Table 6), showing consistent positive results across paradigms. This breadth is the paper's strongest structural asset.

- **Small-to-large model transfer (Section 4.1.2, Tables 1–2).** Qwen3-0.6B screening data for Qwen3-8B achieves AVG 32.12%, comparable to the 8B's self-selection (31.14%), reducing inference cost by over 10×. This is a practical, non-obvious result showing HES captures data-intrinsic signals rather than model-specific artifacts.

- **Sensitivity analysis on the 0.5% entropy threshold (Section 4.4, Figures 3–4).** Testing four thresholds (0.5%, 5%, 50%, 100%) across math, STEM, and code domains shows smaller thresholds consistently perform better, supporting the forking-token intuition. Good empirical hygiene.

- **Clean, computationally cheap metric.** HES requires a single forward pass per sample and no trained classifier, reward model, or human annotation. This is a genuine practical advantage for large-scale data curation.

## Weaknesses

### Fatal
None.

### Major

- **Framing: HES is described as a "quality" metric, but Figure 1 shows incorrect responses have substantially higher HES (mean 0.68) than correct responses (mean 0.29).** The paper repeatedly calls HES a measure of "reasoning quality" (Abstract line 9, line 42, line 102, line 115, line 393), yet its own diagnostic figure shows the opposite polarity — incorrect responses have *more than double* the HES of correct ones. The method works because it is consistently applied within correctness-filtered pools: SFT uses assumed-correct reference data, RFT filters to correct responses before applying HES (Section 3.2), and RL selects from successful trajectories. But the paper never makes this boundary explicit. A reader who glances at Figure 1 sees that HES is higher for wrong answers while the text calls it a "quality" metric — this is confusing at best. The paper should be reframed to describe HES as a measure of reasoning *complexity* (not quality) that has training value *given that the solution is correct*, and should explain why Figure 1 is not contradictory (incorrect responses wander more, producing higher entropy, but the metric is applied within correctness-filtered pools).

- **No measures of variance or statistical significance for any experiment.** All results are reported as point estimates (average@16) without standard deviations, confidence intervals, or significance tests. Several claimed improvements are small in magnitude:

  | Setting | Gap |
  |---|---|
  | RL: Pos-High,Neg-Rand vs Full-Batch | +0.67 points |
  | RFT Per-Query k=8: HES vs Random | +0.97 points |
  | RFT Global Pool k=2: HES vs Random | +2.35 points |
  | SFT: Highest-HES-20% vs Length-20% | +0.47 points |

  With no variance estimates, the reader cannot assess whether these differences, especially the sub-1-point gaps, are reliable or reflect evaluation noise. This is particularly important for average@16 evaluation, which has inherent variance.

### Minor

- **The "unified" claim is overstated.** The paper calls HES a "unified data selection framework applicable across all major training paradigms" (line 36). However, the selection procedure differs substantially per paradigm: SFT uses HES directly on reference responses, RFT first generates then correctness-filters then applies HES, and RL separates rollouts into positive/negative pools and applies HES only to the positive pool. What is unified is the *metric* (HES computation); the selection procedure is paradigm-specific. This should be stated more precisely.

- **Table 1 formatting error: The "Medium Difficulty" row has nearly all entries bolded despite having the lowest AVG (23.29) in the table.** The stated convention (line 182) is that bold = best performance per benchmark. Medium Difficulty's entries (e.g., AIME24: 38.13 vs Full-Dataset's 50.83) are clearly not the best. This appears to be a parser error in the submitted PDF, but readers will find it confusing.

- **Forking-Only baseline (Table 1) achieves 32.51 AVG on 100% data, essentially matching Full-Dataset (32.61), without any data selection.** This baseline modifies the loss to only update high-entropy tokens rather than selecting data, so it is not a direct competitor. However, it raises the question of whether the core effect HES captures is simply that high-entropy tokens carry more learning signal — which Forking-Only exploits without discarding data. The paper should discuss this implication.

- **RL experiments (Section 4.3) use only a 1.5B model with simple heuristic baselines.** The absolute performance is low (AVG ~20-21%), and no comparison is made against existing RL-specific data selection methods (e.g., outcome-based reward models, process reward models, rejection sampling strategies). The claim that HES "surpasses existing training-free selection methods" is only tested against difficulty, length, and random heuristics.

- **SFT: Highest-HES-20% (31.14) vs Length-20% (30.67) — the gap is ~0.5 points.** With no error bars, these are essentially indistinguishable. The paper should acknowledge that improvements over simple heuristics in this setting are modest.

- **Sensitivity analysis (Section 4.4) covers only SFT.** MMLU STEM shows no variation across any threshold (all 0.855), suggesting HES may not be informative for that benchmark — this should be discussed.

### Trivial

- The GRPO KL-divergence weight β is mentioned in the objective (line 89) but its value is not reported in the experimental setup.

- The table label reads "Forcing-Only" (line 171) while the method description reads "Forking-Only" (line 155) — a minor inconsistency.

## Nice-to-Haves

- A direct test of HES discriminative power within the correct-only pool: split correct responses into high-HES and low-HES halves and compare their training value. This would directly validate the paper's core assumption.
- An interpretability analysis of what HES captures empirically (e.g., correlation with solution length, lexical diversity, number of backtracking steps, or mathematical operations).
- Cost analysis quantifying the wall-clock overhead of HES computation across different paradigms.
- RL experiments at larger scale (7B or 8B model).
- Hyperparameter value for the GRPO KL term β.

## Removed Points

- **"Critical Issue 4 (Forking-Only not controlled for data quantity)"** from the Harsh Critic: This point is kept but demoted from Major to Minor because Forking-Only uses a fundamentally different training procedure (loss modification, not data selection), so it cannot be a controlled comparison. The observation is still worth discussing.

- **"Section 4.1 Medium-Difficulty baseline"** formatting observation: Kept as a minor weakness (Table 1 formatting error) — the critic correctly identified the bold inconsistency.

- **Criticism about missing RL baselines from existing literature:** Kept but demoted from Major to Minor because the paper's scope is "training-free selection methods," which appropriately limits the baseline set. More baselines would strengthen the paper but the current set is not invalid.

- **"Section 4.4 only covers Math for full sweep"**: Kept as a minor weakness.

- **"The paper would benefit from a concrete analysis of what HES captures empirically"**: Moved to Nice-to-Haves — this is a constructive suggestion, not a weakness.

- All grammar/typo/formatting nitpicks from the Harsh Critic are removed per policy.

## Novel Insights

The Harsh Critic's most insightful observation is the framing tension: the paper presents HES as a "quality" metric, but Figure 1 shows incorrect responses have substantially higher HES. This is resolved by noting that HES is always applied within correctness-filtered pools in practice (SFT, RFT, and RL all pre-filter for correctness), but the paper never makes this boundary explicit. Reframing HES from "quality" to "complexity" would align the paper's language with its actual evidence. The Forking-Only baseline's near-identical performance to Full-Dataset also hints that high-entropy-token focusing (whether through selection or loss modification) may be the underlying mechanism — worth further investigation.

## Suggestions

1. **Reframe HES explicitly as a measure of reasoning complexity/diversity (not quality)** and clarify that it is applied within correctness-filtered pools. Revise the Abstract, Introduction, and Conclusion accordingly.
2. **Report standard deviations or confidence intervals** for all main results, especially for the smaller gaps (RL, RFT k=8).
3. **Add a direct experiment comparing high-HES vs. low-HES within the correct-only pool** to validate the core assumption that complexity among correct solutions drives training value.
4. **Add an interpretability analysis** showing what HES correlates with empirically.
5. **Fix the Table 1 formatting error** for the Medium Difficulty row.
6. **Discuss the Forking-Only baseline** and its implications for understanding what HES captures.
7. **Report the GRPO KL weight β** and add larger-scale RL experiments if feasible.

---

## Calibration

**Round 1 — Bracketing.**
Queries on data selection / entropy metrics for LLM reasoning training returned the following score-anchored papers:

| Band | Anchor | Avg Score | Comparison |
|------|--------|-----------|------------|
| Strong reject (0–1.5) | Uj0h13lVrR (GFlowNets, sim 0.69) | 1.00 | Unrelated topic; weak-quality paper |
| Low (1.5–3.5) | EOPLy80bBm (Disentangling Data Pruning, sim 0.71) | 3.00 | Similar data-pruning topic but weaker execution |
| Low (1.5–3.5) | OdoS6cH8MP (Textual Data Valuation, sim 0.72) | 2.00 | Data quality topic, weaker framing |
| Low (1.5–3.5) | SaOxhcDCM3 (Self-Consuming Loop, sim 0.72) | 3.20 | Related topic, stronger paper |
| Mid (3.5–5.5) | qUJsX3XMBH (Data Selection at Scale, sim 0.75) | 4.40 | Similar topic; its main finding is that random works well at scale — less novel than HES |
| Mid (3.5–5.5) | cijO0f8u35 (Scaling Math Reasoning, sim 0.75) | 5.25 | Similar reasoning-training topic; limited to GSM8K |
| Mid (3.5–5.5) | gdzpnRBP4F (RLSF, sim 0.75) | 4.50 | RL+reasoning, weaker results |
| High (5.5–7.5) | Fty0wTcemV — **DELIFT** (sim 0.74) | **6.00** | Most comparable: data-selection metric for fine-tuning. DELIFT has stronger experimental rigor but narrower scope (SFT only). HES has broader paradigm coverage but a framing issue and no variance estimates. |
| High (5.5–7.5) | ouRX6A8RQJ (CoT Information Theory, sim 0.74) | 6.40 | Stronger paper on reasoning evaluation; different contribution type |
| High (5.5–7.5) | SpTzsQjgxF (Rule-Based Data Selection, sim 0.74) | 5.75 | Data selection for LLMs; similar scope, slightly stronger execution |
| High (5.5–7.5) | BTKAeLqLMw (What Makes Good Data, sim 0.73) | 6.33 | Data selection for alignment; stronger ablation but narrower scope |
| High (7.5–8.5) | f4gF6AIHRy (Dimensional Collapse, sim 0.71) | 8.00 | Strong accept; pre-training data selection with rigorous analysis |
| High (7.5–8.5) | mMPMHWOdOy (WizardMath, sim 0.71) | 8.00 | Strong accept; different contribution type |

**Itemized calibration on anchors:**
- **DELIFT (6.00)**: Heavy-weight strengths: novel utility metric (+4), effective pruning (+4), clear modular design (+3). Heavy-weight weaknesses: utility based on ICL may not transfer to fine-tuning (-3), unclear if sample diversity is captured (-3), limited comparison with diversity baselines (-2).
- **This paper vs DELIFT**: HES shares DELIFT's strength of a novel, simple metric with broad validation. HES's SFT gains (5+ points over random) are larger than DELIFT's reported gains. However, HES has two problems DELIFT largely avoids: (1) the framing issue where HES is called a "quality" metric but correlates with incorrectness in Figure 1, and (2) complete absence of variance estimates. DELIFT's weaknesses are about indirect measurement; HES's weaknesses are about the accuracy of its own framing.

**Round 1 bracket**: 4.5 – 6.0.

**Narrowing (Round 2)**: Re-querying 4.5–6.5 returned "What Makes Good Data for Alignment?" (6.33), Score Range B data selection (5.75), and "LLMs are Demonstration Pre-Selectors" (5.25). HES compares favorably to the pre-selector paper (5.25) and somewhat unfavorably to "What Makes Good Data" (6.33, which has stronger ablations and framing). The framing issue is the primary factor separating HES from the 6.0+ papers.

**Final placement**: This paper sits above the 4–5 range papers (which had limited novelty or single-dataset evaluations) but below the 6+ papers (which have cleaner framing and/or stronger experimental rigor). The core contribution (HES metric, broad validation, small-to-large transfer) is genuine and useful. However, the persistent framing of HES as a "quality" metric when it is actually a complexity metric (and Figure 1 shows incorrect responses score higher) is a significant communication flaw that weakens persuasiveness. Combined with the absence of any variance estimates, the paper falls short of the 6.0 threshold for borderline accept at ICLR.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>