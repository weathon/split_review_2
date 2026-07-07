## Summary

This paper proposes WeCAN, an end-to-end reinforcement learning framework for heterogeneous DAG scheduling with task-pool compatibility coefficients. The key technical contributions are: (1) a weighted cross-attention (WeCA) mechanism that places compatibility coefficients outside the softmax to distinguish tasks with identical attributes but different compatibility profiles; (2) a longest-directed-distance GNN (LDDGNN) for encoding task dependencies; (3) a theoretical analysis of the list-scheduling optimality gap, with a skip-action mechanism adapted to single-pass inference; and (4) empirical results on TPC-H and Computation Graphs datasets showing improvements over several heuristic and neural baselines.

## Strengths

- **Weighted cross-attention design is well-motivated and architecturally sound.** The placement of compatibility coefficients outside the softmax (Section 3.1, Eq. after line 121) is clearly argued with a concrete example: two tasks with identical attribute vectors but different numbers of compatible pools would receive the same embedding under the "inside" variant but distinguishable embeddings under the proposed design. This goes beyond simply adding compatibility as features.

- **Skip-action theoretical analysis (Section 4) is a genuine contribution.** The paper formalizes the reduced space B, the generation map S_list, proves that TS_list is not surjective (so list scheduling can miss optimal solutions), and establishes conditions under which skip actions close this gap (Theorem 1-2). This is more rigorous than the typical "we add a heuristic" approach and actually characterizes the limitation.

- **Empirical results are strong and consistent against included baselines.** On both TPC-H (Table 1) and Computation Graphs (Table 2), WeCAN-Greedy outperforms all heuristic baselines (HEFT, Tetris, CP, SFT, MOPNR) and all neural baselines (PPO-BiHyb, One-Shot-S(256)). For example, on TPC-H-30, WeCAN-Greedy (makespan 19578, 0.15s) beats One-Shot-S(256) (makespan 20399, 2.26s) at under 1/15th the runtime — a genuinely impressive result for a single-pass greedy solution against a multi-sample competitor.

- **Ablation study (Table 3) is thorough and informative.** The paper systematically ablates: WeCA placement (inside vs decoder-only vs final-only), WeCA absence, and GNN architecture (GAT vs LDDGNN). The results cleanly validate the design choices — e.g., removing WeCA layers entirely drops improvement from 14.0% to 0.5%.

- **Environment fluctuation experiments (Figure 2)** demonstrate generalization from a fixed training environment to varying pool counts, pool types, task counts, and task types. The gap between WeCAN (20.4%) and One-Shot (9.2%) on "more pool" suggests the weighted cross-attention design genuinely helps in heterogeneous settings.

## Weaknesses

### Fatal
None.

### Major

- **Missing comparisons with heterogeneous scheduling baselines discussed in the paper.** The introduction (lines 36–48) specifically critiques Zhou et al. (2022), Zhadan et al. (2023), and Wang et al. (2025) for their handling of compatibility coefficients (e.g., "averaging them across pools, potentially losing fine-grained information"), yet none of these methods appear in the experimental evaluation (Section 5.1). The two neural baselines are PPO-BiHyb (Wang et al., 2021) and One-Shot (Jeon et al., 2023) — the latter was originally designed for homogeneous settings. The abstract claims "outperforming state-of-the-art methods across diverse datasets," but the strongest directly competing heterogeneous scheduling methods are not compared. This weakens the central claim and is the most significant gap in the evaluation.

- **Figure 3 has clear labeling and explanation failures.** (a) "PRO-BALM" appears as a baseline in the figure and table (line 299) but is never defined anywhere in the paper — not in the baselines section, methodology, ablation discussion, or caption. (b) "WeCAN-S(256)" appears twice in the same table row with different values (8.3% and -2.3% on TPC-H-30-heavy). One is presumably the non-skip variant, but this is not disambiguated. The paper's discussion of Figure 3 (lines 310–311) only mentions "WeCAN with the skip action, its non-skipping variant, all other approaches, and HEFT" — it does not mention PRO-BALM at all. This makes the figure partially uninterpretable and undermines the skip-action ablation.

- **One-Shot adaptation to heterogeneous settings is not specified.** The paper notes that One-Shot's architecture "does not consider compatibility coefficients or pool allocation" (lines 28–30), then uses it as a baseline on heterogeneous datasets without describing any modification. The baselines section (lines 218–220) simply lists One-Shot without saying how it handles the compatibility coefficients it was not designed for. If used as-is, the comparison is biased in favor of WeCAN (which does use this information); if modified, the modification must be described. This undermines the fairness of a key experimental comparison.

### Minor

- **The skip-action score formula's connection to the theory is not fully established.** The paper claims the specific formula $u_{\pi_{skip}} = u_a(1 - k/2n)^{u_b} + u_c$ (line 145) "fixes the optimality gap." Theorem 1(iv) asserts existence of *some* scores enabling optimal solutions, but the paper does not argue that this particular 3-parameter exponential-decay form can represent those scores. The justification in Section 4 (line 210) is informal clustering reasoning about "high-u_a, high-u_c regions" rather than a formal connection to Theorem 1(iv). The claim should be softened to "mitigates" or the connection strengthened.

- **The baseline description for REINFORCE ("average rewards," line 186) is ambiguous.** It does not specify whether this is a running average, batch average, or moving average, which affects understanding of training stability.

### Trivial
None.

## Nice-to-Haves

- The heavy-task ablation (Figure 3) tests only one proportion (1% tasks replaced). A sweep over multiple proportions would more convincingly substantiate the claim that "skip benefits more when the percentage of heavy tasks increases."

- The non-autoregressive decoder trades away adaptive re-prioritization for efficiency. While the paper notes an appendix comparison with autoregressive variants (stripped here), a brief acknowledgment of this tradeoff in the main text would improve self-containedness.

## Removed Points

These points were raised in the input reviews but are removed as invalid, speculative, or noise:
- *"List scheduling cannot yield an optimal schedule" is too broad* — removed because the paper explicitly says "in certain cases" (line 194), so the criticism misreads the paper.
- *Non-autoregressive decoder limitation not acknowledged* — removed because the paper references an autoregressive comparison in Appendix B; the design is intentionally scoped for efficiency.
- *Variance not reported for greedy results* — removed because greedy is deterministic given a trained model; std is expected to be zero.
- *Formatting nitpicks (bold math tags in Table 1)* — removed as parser artifacts.
- *WeCA being one-directional* — removed because the decoder also uses WeCA layers and the architecture is clearly described.
- *"Average rewards" ambiguity* — kept as Minor since it's a genuine vagueness, though the positive model weight (+0.96) suggests the scorer does not consider it harmful.

## Novel Insights

The most incisive observation from the input reviews is the Figure 3 labeling failure — "PRO-BALM" undefined and duplicate "WeCAN-S(256)" — which is a concrete, independently verifiable reporting error that directly harms interpretability of the skip-action ablation. This is distinct from the more common speculative or category-driven criticisms and represents actionable feedback for the authors.

## Suggestions

1. **Add the heterogeneous scheduling methods discussed in the introduction** (Zhou et al. 2022, Zhadan et al. 2023, Wang et al. 2025) as experimental baselines to directly validate the paper's central claim about their limitations. This is the highest-leverage improvement.
2. **Fix Figure 3:** define (or remove) "PRO-BALM" and disambiguate the duplicate "WeCAN-S(256)" label — one is presumably the non-skip variant.
3. **Clarify how One-Shot was adapted** to handle compatibility coefficients and pool allocation, or explicitly acknowledge the assumption if used as-is.
4. **Strengthen the connection** between the skip-action score formula and Theorem 1(iv), or soften the claim from "fixes" to "mitigates" with empirical support.

## Score and Decision

**Calibration summary:**

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| jsWCmrsHHs (DRL JSSP) | 7.50 | R1 | Yes | Stronger evaluation with broader baselines; our paper has similar strengths but a heavier negative for missing baselines (-7.18 vs max -3.70) |
| 10eQ4Cfh8p (FJSP RL) | 3.00 | R1 | Yes | Much weaker: undefined contributions, unfair comparisons, missing baselines across the board; our paper has concrete architectural novelty and theory |
| b9aCXHhdbv (Pipeline RL) | 4.50 | R1 | Yes | Lacks formal analysis (-5.47) and has insufficient evaluation (-10.20); our paper has stronger theory and more thorough evaluation |
| AloCXPpq54 (HRL SSCO) | 6.00 | R2 | Yes | Similar score range; our paper has stronger positive weights (+4.70 to +5.29) but similar magnitude negative weights (-7.18) |
| yEwakMNIex (RedCO) | 6.25 | R2 | Yes | Criticized for weak contribution (-7.99) and applicability concerns (-7.07); our paper's methodological contribution is more concrete |

**Bracketing:** Round 1 bracketed the paper between 5.5 and 7.5. Comparison with itemized anchors in Round 2 narrows to 5.5–6.5: our paper's strengths (+4.70 to +5.29 for empirical results and ablation) are comparable to the 7.50 anchor's strongest items, but the -7.18 weight for missing baselines (absent in the 7.50 anchor's review) and the -4.40 for Figure 3 errors push it down. The paper sits above the 5.0–5.75 band (papers in that range have more fundamental issues like missing formal analysis or weak contribution) and below the 7.0–7.5 band (papers with comprehensive evaluation and no major gaps).

**Final score rationale:** The paper makes a genuine contribution — the weighted cross-attention design is novel and well-motivated, the theoretical analysis of the list-scheduling optimality gap is clean, and the empirical results against included baselines are strong. However, the evaluation has a significant gap: the paper critiques specific heterogeneous scheduling methods (Zhou 2022, Zhadan 2023, Wang 2025) but does not compare against them experimentally. Combined with the Figure 3 labeling failure (undefined PRO-BALM, duplicate WeCAN-S(256)) and the unspecified One-Shot adaptation, these issues prevent a higher score. The core methodology is sound and the issues are fixable.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>