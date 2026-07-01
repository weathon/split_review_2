Now I'll produce the final consolidated review.

## Summary

The paper proposes WeCAN, an end-to-end RL framework for heterogeneous DAG scheduling with task-pool compatibility coefficients. It introduces a weighted cross-attention (WeCA) encoder that processes compatibility coefficients outside the softmax normalization (preserving size-adaptability), a longest-directed-distance GNN (LDDGNN) for task dependency encoding, a non-autoregressive decoder, and a skip-action mechanism integrated into the single-pass generation pipeline. A theoretical analysis formalizes the optimality gap of list-scheduling-based generation maps. Empirical results on TPC-H and Computation Graphs benchmarks show consistent makespan improvements over heuristic and neural baselines.

## Strengths

1. **The weighted cross-attention mechanism (Section 3.1, Eq. 2) is a well-motivated architectural contribution.** Placing compatibility coefficients outside the softmax (rather than adding them in log form inside) is a nuanced design choice, and the two-pool, two-task example convincingly shows why the two placements can produce different embeddings. This directly addresses the limitation of fixed-size embeddings in prior heterogeneous scheduling work.

2. **Empirical results on TPC-H (Table 1) and Computation Graphs (Table 2) are strong and consistent.** WeCAN-S(256) outperforms One-Shot-S(256) by ~5–7% on TPC-H and ~9–12% on Computation Graphs. The greedy variant (WeCAN-Greedy) also beats both heuristic and neural baselines at comparable or better runtime. The gains are visible across multiple dataset sizes and graph types.

3. **The generalization experiments (Figure 2) go beyond what many scheduling papers provide.** Testing under varying pool counts, pool types, task counts, and task types while training on a fixed environment demonstrates that the weighted cross-attention mechanism's adaptability to variable-sized environments is real rather than merely claimed.

4. **The theoretical framing of the list-scheduling optimality gap (Section 4) is a genuine conceptual contribution.** The use of T and S maps to formalize when a generation map can represent optimal solutions is clean, and the distinction between the list scheduling map S_list and the proposed skip-augmented map is clearly drawn. The framework for analyzing generation maps is well-structured.

## Weaknesses

### Major

1. **PRO-BALM appears in the heavy-task ablation (Figure 3) without definition or citation.** This baseline is neither listed in Section 5.1 (Baselines) nor defined anywhere in the main text. The reader cannot evaluate what method is being compared against. Additionally, the figure caption lists "WeCAN-S(256)" twice (once blue, once green), suggesting a labeling error where one entry is likely a variant (e.g., WeCAN without skip). These two issues together make a key experiment difficult to interpret. This needs to be corrected — either define and cite PRO-BALM, or replace it with a properly described baseline.

### Minor

2. **The skip score formula (Section 3.2, line 145) is presented without ablation against alternatives.** The formula \(u_a(1 - k/(2n))^{u_b} + u_c\) is introduced with the rationale that it prevents endless idling while maintaining single-pass efficiency. However, no comparison is provided against other plausible schedules (e.g., linear decay, exponential decay, a learned per-step MLP). Theorem 1(iv) guarantees existence of scores enabling optimality, but whether this specific functional form is necessary or merely sufficient is not tested. An ablation study comparing 2–3 alternatives on the heavy-task datasets would strengthen the paper, though this does not invalidate the core contributions.

3. **The evaluation protocol for the main results (Tables 1–2) is underspecified.** The table caption states "standard deviation among random seed," but the number of random seeds and the number of test instances are not reported. The ablation section (line 308) mentions "10 test problems" — it is unclear whether the same holds for the main tables. This should be stated explicitly for reproducibility.

### Trivial

4. **The "three pool-selection rules" used for heuristic baselines (Section 5.1) are not described.** This is a reproducibility detail that should be clarified.

5. **The "signed length of the longest directed path" (d_c, line 129) could be more precisely defined.** The meaning of "signed" in this context is not explained in the main text.

## Nice-to-Haves

- An ablation of the skip score formula against alternatives (linear decay, exponential decay, constant skip score) on the heavy-task datasets would strengthen the empirical validation of the skip mechanism.
- Clarifying whether the WeCA layer uses multi-head attention (the equation shows a single-head formulation, while LDDGNN explicitly uses multi-head).

## Removed Points

These points were flagged by the reviewer but are removed with justification:

- **PPO-BiHyb comparison conflates method and compute budget:** Removed. Comparing against a published SOTA method as-is is standard practice. The runtime advantage stems from the single-pass paradigm, which is an explicit contribution of the paper. Modifying the baseline's algorithm (e.g., limiting its beam search) is not a standard expectation.
- **Suspiciously tight standard deviations (strong form):** The table caption (line 228) explicitly states "standard deviation among random seed," not across problem instances. Different methods can exhibit different training stability across seeds, so the claim that the tight std is "suspicious" is unfounded. The valid sub-concern about underspecified test instance count is retained in Minor weakness #3.
- **Duplicate WeCAN-S(256) label in Figure 3:** This may be a parser/formatting artifact from PDF extraction. The substantive issue of PRO-BALM being undefined is retained in Major weakness #1.
- **Resource constraint vector inequality notation:** This is standard component-wise vector inequality. Not a real issue.
- **WeCA layer multi-head attention not discussed:** This is a minor implementation detail, not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Define or properly cite the PRO-BALM baseline in Figure 3, and fix the apparent duplicate label (the green bar likely corresponds to a variant such as WeCAN without skip).
2. Report the number of test instances and random seeds used for the main results (Tables 1–2).
3. Add an ablation comparing the proposed skip-score formula against 2–3 alternatives on the heavy-task datasets, or justify the current choice more thoroughly.
4. Describe the three pool-selection rules used for heuristic baselines.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>