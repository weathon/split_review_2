The favorability scores confirm the key signals. The Figure 3 suspicious patterns and missing variance both score near 0, while the schedule selection concern is mild (0.52). Let me now write the final consolidated review.

## Summary

This paper proposes CANON (Conditional advANtage estimatiON), a method that regroups sampled responses in RLVR training by a metric (entropy or length) and computes separate inter-group and intra-group advantages. The key idea is to let the data itself reveal whether a metric trend helps performance, rather than imposing a directional prior. CANON-Inter (emphasizing inter-group advantage) improves math accuracy, CANON-Intra (emphasizing intra-group advantage) improves complex logic reasoning, and CANON-Dynamic schedules between them. The paper also extends the method to length efficiency via a weighted advantage term.

## Strengths

- **Clean and motivated formulation.** The regrouping idea is conceptually elegant. The paper correctly identifies a limitation of prior reward/advantage shaping methods (they presuppose directional priors requiring careful tuning). CANON's design — letting inter-group comparison reveal which metric trend correlates with higher reward while intra-group comparison selects better responses within the same trend — is genuinely novel. The theoretical connection showing DR.GRPO is a special case of CANON with μ=0.5 (Eq. 7) grounds the method well in prior work.

- **Theoretical grounding for selective amplification (Theorem 2).** Theorem 2 shows that CANON based on condition c₁ does not amplify the influence of an independent condition c₂, a meaningful property that distinguishes CANON from naive advantage scaling.

- **Comprehensive evaluation scope.** The paper evaluates across three model families/sizes (Qwen2.5-Math-7B, Qwen2.5-Math-1.5B, Llama3.1-8B), six math reasoning benchmarks, and a challenging logic reasoning benchmark with three difficulty tiers. The efficient reasoning experiments (Section 5.3) explore multiple α values and compare against multiple length-control baselines.

- **Training dynamics analysis.** Figures 2 and 6 provide useful insight into how inter-group vs. intra-group advantages produce different training behaviors — CANON-Inter drives rapid math improvement with decreasing entropy, while CANON-Intra fosters exploration that pays off on complex logic tasks. The reflection-gain analysis offers a mechanistic explanation for why scheduling works.

## Weaknesses

### Major

- **Figure 3 data is inconsistent with Tables 1–2 and contains unexplained synthetic patterns.** The radar chart (Figure 3) — presented as the central visual evidence for the claim that "CANON-Dynamic outperforms DR.GRPO across all models and tasks" — contains values that do not match the paper's own experimental tables:

  | Model | Source | DR.GRPO Math | DR.GRPO Logic |
  |---|---|---|---|
  | Llama-8B | Table 2 | 22.0 | 14.9 |
  | Llama-8B | **Figure 3** | **22.6** | **18.9** |
  | Qwen-7B | Tables 1-2 | 55.7 | 26.2 |
  | Qwen-7B | **Figure 3** | **57.6** | **39.2** |
  | Qwen-1.5B | Table 2 | 46.4 | 12.8 |
  | Qwen-1.5B | **Figure 3** | **46.8** | **17.0** |

  The Figure 3 DR.GRPO values systematically match *other methods* from the tables (Cosin-First-Inter-Later-Intra for Llama-8B, CANON-Inter's math score for Qwen-7B, First-Inter-Later-Intra for Qwen-1.5B). Furthermore, the CANON-Inter/Intra values in Figure 3 exhibit suspicious symmetry (e.g., 35.2/15.0 and 15.0/35.2 for Llama; 45.0/35.0 and 35.0/45.0 for Qwen-7B), and CANON-Dynamic shows equal scores across both tasks for every model — patterns inconsistent with the table data and unexplained in the paper. No normalization or transformation is described. This is a data integrity concern that undermines the paper's headline visual claim, although the per-table experimental results (Tables 1, 2, 3) remain as presented.

- **No measure of statistical reliability.** The paper reports a single run per condition with no standard deviations, confidence intervals, or multiple seeds. RL training is high-variance, and several claimed improvements are modest (e.g., 1.9 points on math average from 55.7 to 57.6). Several benchmarks (AIME 24/25, AMC) have tiny evaluation sets where the reported Avg@10 metric itself has variance. Without any indication of run-to-run variability, the reader cannot assess whether the observed differences are meaningful signal or noise.

### Minor

- **Post-hoc model-specific schedule selection for CANON-Dynamic.** The paper tests four scheduling strategies and selects a different one per model after seeing results (Cosin-First-Inter-Later-Intra for Qwen-7B/Llama-8B, First-Inter-Later-Intra for Qwen-1.5B). The paper acknowledges this ("A specifically designed strategy is acceptable for better performance in practice"), but this means CANON-Dynamic's reported performance reflects optimization over four attempts while DR.GRPO gets one. That said, Table 2 shows both scheduling strategies consistently outperform DR.GRPO, so the core finding is not entirely dependent on the choice — the concern is about potential inflation of the reported margin.

- **Tension between the "no directional prior" framing and the length-weighting experiments.** The paper's core motivation is to "amplify the impact of specific metric changes without presupposing preferences." However, CANON-Eff (Section 5.3, Eq. 9) uses α<1 to down-weight longer responses, where C⁺ is defined as the group with longer responses. This *is* a directional prior — penalizing longer responses. The paper would benefit from cleanly separating the two contributions: (a) CANON for automatic trend discovery (entropy case, no directional prior), and (b) CANON with weighted conditions for targeted efficiency (length case, explicit directional prior).

- **Theorem 1's practical relevance is not fully established.** Theorem 1 shows that |Â^inter|/|Â^DR.GRPO| > 1 only when groups are equal-sized, which the paper uses to justify equal splits. However, the theorem only shows the ratio is maximized under equal splits — it does not establish that a larger ratio is beneficial for training quality (it could amplify noise or cause instability). An ablation varying the split ratio would strengthen the argument.

- **Entropy baselines only tested on the 7B model.** The entropy-related baselines (Entropy Adv, Clip-Cov) appear only in Table 1 (Qwen-7B) and are absent for the 1.5B and 8B models in Table 2. Given the paper's claim that CANON generalizes across model sizes, these baselines should have been included for the other models.

### Trivial

None.

## Nice-to-Haves

- An ablation varying the group split ratio (e.g., 25/75, 40/60, 50/50, 60/40) to directly validate Theorem 1's practical relevance.
- A controlled experiment demonstrating a concrete failure case of directional prior methods (e.g., entropy penalty with too-large coefficient underperforming CANON).
- More granular reporting: even computing standard deviation across the six math benchmarks per condition would partially address the variance concern.

## Removed Points

These points are flagged to be removed, treat them with caution:
- The harsh critic's claim that "Table 1 | Qwen-7B | DR.GRPO | 53.8 | 17.2" is factually wrong — those values (53.8/17.2) are for GRPO, not DR.GRPO (DR.GRPO in Table 1 is 55.7/26.2). The core finding (Figure 3 mismatch) remains correct.
- Criticism about unclear Table 2 row labeling: the scheduling strategy names are clearly stated in the table header and explained in Section 5.2.
- Criticism about missing appendix content: parser-stripped content should not be flagged.
- Criticism about context-limit modification (rope theta): acknowledged in a footnote, applies equally to all conditions.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reconcile Figure 3 with Tables 1–2.** Either use the actual experimental numbers from the tables, or if the radar chart uses normalized/transformed values, clearly state the transformation and show both raw and transformed values.
2. **Run multiple seeds.** Even 3 seeds for the main comparisons (DR.GRPO vs. CANON-Inter vs. CANON-Intra on one model) with standard deviations would substantially improve evidential quality.
3. **Pre-specify one CANON-Dynamic scheduling strategy** (e.g., First-Inter-Later-Intra, the simplest and most principled) and apply it uniformly across all models; report all schedules in an ablation.
4. **Cleanly separate the two contributions** in the framing: automatic trend discovery (entropy, no directional prior) and weighted-advantage efficiency (length, explicit directional prior).
5. **Add an ablation on group split ratio** to validate Theorem 1's practical relevance.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>