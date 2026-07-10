Now I have all the information. Let me compose the final consolidated review.

---

## Summary

This paper makes three contributions: (1) it identifies task ID leakage through graph-structure cues in the standard local-testing protocol for Graph Continual Learning (GCL), demonstrating that even a simple mean-pooling operation achieves 100% task ID accuracy and 0% forgetting, effectively debunking prior SOTA claims made under this protocol; (2) it introduces LLM4GCL, a benchmark evaluating 9 methods across 7 datasets under two continual learning scenarios; and (3) it proposes SimGCL, a method combining graph-prompted instruction tuning with training-free prototype classification. The task-ID-leakage critique is a concrete and convincing contribution. However, the paper's central empirical claims about SimGCL are weakened by unresolved experimental reporting gaps.

## Strengths

- **The identification of task ID leakage in local testing (Section 3.1, Table 1) is a genuine methodological contribution.** The paper shows that under the standard CGLB local testing protocol, graph-structure cues alone allow 100% task ID prediction even with a simple mean pooling operation, matching prior SOTA performance. This calls into question many published GCL results and establishes global testing as the more rigorous standard.

- **Comprehensive empirical coverage:** 9 methods spanning GNN, LLM, and GLM categories, evaluated across 7 datasets under two continual learning scenarios (NCIL and FSNCIL). This benchmark will be a useful resource for the community.

- **SimGCL achieves large performance margins on 5 of 7 datasets.** On Cora NCIL (84.6 vs. 70.8) and Photo NCIL (82.1 vs. 62.1), the improvements over the next-best method exceed 13 and 18 points respectively.

## Weaknesses

### Fatal
None.

### Major

- **[Major] The LLM backbone used for SimGCL in the primary results (Tables 2 and 3) is not specified anywhere in the main text.** Baselines explicitly name their backbones (BERT, RoBERTa, LLaMA, SimpleCIL with RoBERTa), but SimGCL's backbone remains unidentified. Figure 3 shows SimGCL with multiple backbones (B-large, B-medium, B-small, Ro-large), making it impossible to tell which model produced the headline numbers. Without this information, the central comparison conflates method design with model scale effects and is fundamentally uninterpretable. If this detail exists in the appendix, it must also be stated in the main text for a result central to the paper's claims.

- **[Major] No variance or statistical significance is reported for any result.** Grep confirms the complete absence of standard deviation, variance, random seed, multiple run, or ± notation. Given the known variability in LLM fine-tuning and prototype-based methods' sensitivity to per-session sample composition, single-run results provide insufficient evidence for the paper's claims.

- **[Major] SimGCL lacks any component ablation.** The method combines (a) graph-prompted instruction tuning with LoRA in session 1 and (b) training-free prototype classification. The paper's own Obs. ⑥ shows that SimpleCIL (frozen LLM + prototypes) already beats most baselines, raising the question of how much gain comes from instruction tuning vs. the prototype approach alone. Without ablating these components, the paper cannot attribute SimGCL's improvements to its proposed graph-prompted tuning mechanism.

### Minor

- **[Minor] The claim that SimGCL "consistently overperform[s]" (Obs. ⑧) is overstated.** SimGCL underperforms SimpleCIL on Arxiv-23 in both NCIL (Ā: 38.7 vs. 52.4, A_N: 13.6 vs. 38.8) and FSNCIL (31.8 vs. 49.8, 10.3 vs. 40.0), and on Arxiv in FSNCIL (36.3 vs. 46.4, 6.8 vs. 36.6). The paper's explanation attributing this to "sparse graph structure" is undermined by the fact that SimpleCIL is text-only and does not use graph structure at all.

- **[Minor] The scaling hyperparameter τ is introduced in Eq. (2) as controlling the weight distribution for classification, but its value and tuning procedure are never reported.**

### Trivial

- **[Trivial] Observation numbering is inconsistent:** the paper goes from ❶→❷→❸→④→⑥→⑧ (skipping ❺ and ❼), then switches to Arabic numerals "Obs. 7" and "Obs. 8" in subsequent paragraphs.

## Nice-to-Haves

- Forgetting ratios (AF) could supplement the reported average and final accuracy in the main results (Table 1 already reports AF, but Tables 2-4 do not).
- A computational cost comparison with baselines would strengthen the efficiency claim.

## Removed Points

These points from the input review were removed with justification:
1. **"Code link is #"** — Removed per rule: placeholder links are standard for double-blind review and do not indicate absence of code.
2. **"Missing hyperparameters (LoRA rank, learning rate, epochs, optimizer)"** — Removed per rule: nitpicks about undisclosed hyperparameters as trivial implementation details.
3. **"Missing forgetting ratios in main results"** — Removed: Table 1 does report AF, and Ā/A_N are standard CL metrics; this is a metric choice, not a flaw.
4. **"Missing computational cost (Appendix E)"** — Removed per rule: weaknesses about missing appendix content are excluded.
5. **"Prompt template token counts/memory"** — Removed as an overly granular implementation detail.
6. **Concern that task-incremental evaluation is also valid** — Removed: the paper's framing of global testing as more realistic for class-incremental evaluation is justified and the local testing critique remains valid.

## Novel Insights

None beyond the paper's own contributions. The input review is thorough but does not uncover an analytical pattern that the paper itself does not already articulate.

## Suggestions

1. **Specify the backbone** for SimGCL's main results in the main text and compare SimGCL against SimpleCIL using the *identical* backbone to separate the effect of instruction tuning from model scale.
2. **Add component ablations:** SimGCL w/o instruction tuning (frozen backbone + prototypes) and SimGCL w/o graph prompts (plain text instruction tuning + prototypes).
3. **Report mean ± std** over multiple runs (at least 3 seeds) for all main results.
4. **Acknowledge the two failure cases** more prominently and provide a more rigorous explanation for why SimpleCIL (text-only, no graph structure) outperforms SimGCL on those datasets.

## Score and Decision

The paper makes one solid, standalone contribution (the task-ID-leakage critique) and provides a comprehensive benchmark. These alone justify borderline acceptance. However, the SimGCL method's claims are not adequately supported due to the unresolved backbone ambiguity, missing variance, and absent ablations. The paper should not be accepted in its current form for the method claims, but the critique and benchmark are valuable enough to warrant conditional acceptance pending resolution of these evidential gaps.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>