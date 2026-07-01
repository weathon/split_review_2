Now let me read the paper in chunks to verify the reviewer's claims.Now I have read the full paper. Let me compile my draft review based on the verified findings before calibration.Now let me run Round 1 calibration — bracketing across score bands with topic-relevant queries.Let me read a few anchor papers to calibrate my score.Now let me do a Round 2 narrowing search within my initial bracket of 6–8.Let me read the closest comparator paper — "Language models scale reliably with over-training and on downstream tasks" (score 6.5, accepted).Now I have enough calibration data to finalize. Let me write the complete review.

---

## Summary
This paper studies how to pre-train language models when data is fixed but compute is unlimited. It discovers that optimal weight decay for data-constrained pre-training is ~30× larger than standard practice (0.8–3.2 vs. 0.1), which transforms non-monotone overfitting scaling into clean power laws. The paper proposes evaluating recipes by the *asymptote* of their scaling law, shows that ensembling independently trained models yields a lower asymptote than single-model parameter scaling, and demonstrates that gains can be compressed via distillation—including a surprising self-distillation result where a 300M student matches the regularized recipe's asymptote without ever training a larger model.

## Strengths

- **The weight decay finding is surprising and practically valuable.** Figure 3 and its accompanying table show optimal weight decay of 0.8 (150M) to 3.2 (1.4B)—over 30× the standard 0.1 from Brown et al. (2020). This transforms a non-monotone scaling curve (standard recipe reverses at ~600M parameters in Figure 2) into a clean power law that decreases monotonically through 1.4B parameters. The connection to double descent theory (Nakkiran et al., 2021; Simon et al., 2024) grounds the finding theoretically. This is immediately actionable for practitioners training on constrained data.

- **Asymptote-based evaluation is a genuine conceptual contribution.** Under the paper's premise of unlimited compute, evaluating recipes by the asymptote of their scaling law (rather than performance at a fixed compute budget) is the natural metric. This provides a principled framework for ranking qualitatively different recipes, and the paper uses it consistently throughout.

- **Clean ensembling vs. parameter scaling comparison.** Figure 4 directly compares ensembles of 300M models against single models at equal total parameter counts, showing ensembles consistently achieve lower loss with a lower asymptote (3.34 vs. 3.43). The comparison is well-controlled and the result is likely robust to fit uncertainty since ensemble points are consistently below single-model points.

- **Self-distillation result is striking and well-connected to theory.** Figure 8 shows a 300M model self-distilled into a fresh 300M student matches the regularized recipe's asymptote (3.43) without ever training a larger model. The connection to Allen-Zhu and Li (2023), who show self-distillation can be viewed as implicit ensembling, provides a plausible theoretical explanation.

- **Honest downstream evaluation protocol.** Section 7 explicitly states no downstream benchmarks were consulted until the end of the project, with all recipe selection done via validation loss. The 9% improvement on PIQA, SciQ, and ARC Easy (Figure 9) provides credible evidence that validation loss improvements generalize.

- **Systematic, layered experimental design.** The paper builds logically: standard recipe → regularized → ensembling → joint scaling → data scaling → distillation → downstream. Each section addresses a natural follow-up from the previous one, making the experimental logic transparent and easy to follow.

## Weaknesses

### Fatal
None

### Major

- **Asymptote estimation from barely-identified power law fits.** The central metric—the asymptote $E_D$ of $\hat{\mathcal{L}} = A/N^\alpha + E$—requires fitting 3 free parameters to 4 data points (150M, 300M, 600M, 1.4B). The asymptote is the least identifiable parameter since it depends entirely on extrapolation. While footnote 2 addresses stochastic uncertainty (±0.02 across 3 seeds, Appendix I.1), systematic uncertainty from functional form choice is unexamined. The joint scaling recipe (Section 4.3, Figure 5) compounds this by fitting power laws in $K$ (5 points), then taking the asymptote of those asymptotes in $N$ (4 points). The qualitative ordering of recipes is likely robust, but headline numbers like "5.17×" and "asymptote = 3.17" carry substantially more uncertainty than presented.

- **Heuristic hyperparameter tuning for the headline claim.** Section 4.3 explicitly states: "we cannot fully find locally optimal hyperparameters due to experimental constraints. Instead, we use the heuristic of taking the optimal regularized hyperparameters with 2× epochs and 0.5× weight decay." Since the 5.17× data efficiency claim depends on this joint asymptote of 3.17, the paper's most prominent number rests on weaker evidence than the regularized (2.29×) or ensembling (3.03×) results, which use more carefully tuned configurations.

- **Scale gap between experiments and motivating regime.** All experiments use 200M–1.6B tokens with models up to 1.4B parameters—roughly 1000× smaller than current practice. At these scales, parameter-to-token ratios of 7:1 create severe overfitting where aggressive regularization is indispensable. At practical ratios (0.01–0.1), the regularization regime is fundamentally different—it is unclear whether weight decay of 3.2 would remain optimal. The data scaling laws (Section 5) that attempt to bridge this gap are themselves fit on only 4 token counts spanning less than one order of magnitude. The paper is mostly transparent about this (Section 5.3), but the framing sometimes elides the gap between what has been demonstrated (small scale) and what is claimed (general pre-training guidance).

### Minor

- **Limited downstream evaluation.** Only 3 benchmarks (PIQA, SciQ, ARC Easy) are used, and the 9% improvement is a simple average without per-benchmark variance. While understandable at this scale (following Thrush et al., 2025), reporting per-benchmark results in the main text would strengthen the generalization claim.

### Trivial
None

## Nice-to-Haves

- Adding 1–2 more parameter counts (e.g., 900M, 2B) to power law fits would move them from barely-identified to meaningfully constrained and improve confidence in asymptote estimates.
- A simple "practitioner recipe" relating optimal weight decay to the parameter-to-token ratio (implicit in Table 3 of Figure 3) would dramatically increase practical impact.
- Confidence intervals or bootstrap estimates for all asymptotes would let readers assess whether the ordering of recipes is robust.
- Discussion or ablation of how other regularization methods (dropout, label smoothing, data augmentation) compose with weight decay, given the paper's thesis that regularization is critical.
- Exploring whether multiple rounds of self-distillation continue to improve performance.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"The theoretical motivation via Allen-Zhu and Li (2023) is light."** The paper uses this as a plausible framing ("Allen-Zhu and Li (2023) shows that ensembling helps when..."), not a claimed verified mechanism. The paper's contribution is empirical, and the theoretical framing is appropriately cautious. Not a weakness.
- **"Missing comparison with rephrased data / data augmentation methods."** These are explicitly discussed in related work (Section 8) and operate in a different part of the design space. The paper's stated scope is classical algorithmic improvements (regularization, ensembling, distillation), and it does this well. Scope creep.
- **"The power law form is assumed rather than derived."** This is standard practice in the entire scaling law literature (Kaplan et al., 2020; Hoffmann et al., 2022). Not a weakness specific to this paper.
- **"Coordinate descent HP tuning may be hard to replicate."** This is a reproducibility nitpick about implementation details; the paper references Appendix C.1 for full details.
- **"The abstract should caveat the 5.17× number more carefully."** The abstract already states this is an asymptotic estimate ("achieves an asymptote at 200M tokens using 5.17× less data"). While more precision would help, the current framing is adequate.

## Novel Insights

The paper's most novel insight is that weight decay has been dramatically under-tuned for data-constrained pre-training—a finding that transforms qualitatively broken scaling (non-monotone overfitting at large $N$) into clean power laws, and that the optimal value increases with model size at fixed data. The complementary finding that ensembling outperforms parameter scaling in the asymptotic limit under data constraints, combined with the self-distillation result showing these gains can be recovered without ever training larger models, provides a useful practical decomposition of how to spend compute when data is the bottleneck.

## Suggestions

- Report confidence intervals on all asymptote estimates. Even simple diagnostics—e.g., how much asymptotes shift when dropping one data point—would let readers assess robustness.
- Explicitly caveat the 5.17× number in the abstract and introduction with a note about its dependence on heuristic HP tuning and double extrapolation. The 2.29× (regularized) and 3.03× (ensembling) numbers are on firmer ground and should be emphasized more.
- Provide a simple functional relationship between optimal weight decay and parameter-to-token ratio (e.g., from Table 3 in Figure 3), which would increase the paper's immediate practical impact.
- If possible, validate the weight decay finding at one additional scale (e.g., 10B tokens) to narrow the scale gap.

## Score and Decision

**Calibration anchor papers (all rounds):**

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| Scaling In-the-Wild (IC-Light) | u1cQYxRI1H | 0.50* | R1 | Unrelated topic; clear mismatch for low-score anchoring |
| Financial Markets Neural Network | nSDOkm0SKo | 1.00 | R1 | Hypothetical scenario paper, far below reviewed paper |
| LLM Survey | 8QTpYC4smR | 1.00 | R1 | Pure survey, not comparable |
| Clothing-Irrelevant L-ReID | 5lUdTogEL3 | 1.00 | R1 | Different domain, clearly weaker |
| Data Pruning Disentangling | EOPLy80bBm | 3.00 | R1 | Systematic but limited novelty; reviewed paper is clearly stronger |
| Ask Your Distribution Shift | 7LZjuA4AB2 | 3.00 | R1 | Limited empirical validation; reviewed paper has more substance |
| Activation Decay | InRaT76E2S | 2.50 | R1 | Regularization paper but weak contribution; reviewed paper much stronger |
| Projected Subnetworks | WM5G2NWSYC | 2.00 | R1 | Unclear contribution; not comparable |
| Scaling Laws for Agents | D0XpSucS3l | 4.50 | R1 | Similar spirit but limited to simulation, no downstream tasks; reviewed paper is stronger |
| Fair Language Model Paradox | Kb1bIuGuax | 4.75 | R1 | Studies weight decay effects on token-level fairness; interesting but narrower contribution |
| Hitchhiker's Guide to Scaling Laws | xGM5shdGJD | 5.20 | R1 | Useful dataset release but presentation issues; reviewed paper has more surprising findings |
| Layer-wise Pre-weight Decay | 0GZ1Bq4Tfr | 3.75 | R1 | Proposes alternative weight decay; limited empirical scale |
| Scaling Law with LR Annealing | o9YC0B6P2m | 6.75 | R1 | Novel scaling law for LR; rejected despite score. Reviewed paper has cleaner design, more surprising results |
| Scaling Laws for Downstream Tasks (MT) | vPOMTkmSiu | 6.60 | R1 | Studies scaling for downstream; accepted. Comparable quality |
| Sparse Scaling | ud8FtE1N4N | 6.67 | R1 | Studies sparse pre-training scaling laws; accepted. Comparable |
| Scaling Laws for Sparse Foundation Models | i9K2ZWkYIP | 7.00 | R1 | First sparsity scaling law across vision/language; similar quality |
| Scaling Laws for Precision | wg1PCg3CUP | 8.00 | R1+R2 | 465 runs, much more robust empirically; reviewed paper has more surprising findings but less robustness |
| Small-scale proxies for instabilities | d8w0pmvXbZ | 8.00 | R1 | Clean methodology, broadly validated; stronger empirical foundation |
| Never Train from Scratch | PdaPky8MUn | 8.00 | R1 | Insightful finding about data-driven priors; clean |
| Scaling Laws for Associative Memories | Tzh6xAJSll | 7.60 | R1+R2 | Theoretical + empirical; strong contribution |
| MiniPLM | tJHDw8XfeC | 6.40 | R2 | KD for pre-training; reviewed paper is more comprehensive and surprising |
| MEND | 2Y5kBPtU0o | 6.25 | R2 | ICL distillation; different problem, narrower contribution |
| Unsupervised Pretraining for Fact Verification | 1mjsP8RYAw | 6.00 | R2 | Narrow domain; weaker contribution |
| Emulator for Fine-tuning | Eo7kv0sllr | 6.50 | R2 | Creative idea; comparable quality |
| Combatting Dimensional Collapse | f4gF6AIHRy | 8.00 | R2 | Data selection for pre-training; strong paper with robust results |
| Synthetic Continued Pretraining | 07yvxWDSla | 8.00 | R2 | Data efficiency through synthetic data; clean, well-validated. Reviewed paper is comparable in significance |
| DEPT | vf5aUZT0Fz | 8.00 | R2 | Decoupled embeddings; clean framework. Stronger empirical coverage |
| Training on the Test Task | jOmk0uS1hl | 8.00 | R2 | Important evaluation insight; different problem |
| Language models scale reliably with over-training | iZeQBqJamf | 6.50 | R2 | Most directly comparable: scaling laws under non-standard training. 104 models but less surprising findings. Reviewed paper has stronger contributions |
| Multi-Power Law for Loss Curves | KnoS9XxIlK | 6.00 | R2 | Loss prediction across LR schedules; narrower contribution |

**Round 1 bracket:** 6–8. The paper clearly sits above the rejected/borderline-reject scaling law papers (~3–5) with its more surprising findings and better experimental design, but below the strongest 8.0 papers that have much more robust empirical foundations.

**Round 2 narrowing:** The most informative comparison is with "Language models scale reliably with over-training" (6.5, accepted) — the closest paper in spirit. Our paper has more surprising findings (weight decay 30×, ensembling > parameter scaling, self-distillation), a more creative evaluation framework (asymptotes), and stronger practical implications. However, that paper trained 104 models and validated at larger scales (up to 6.9B parameters), while our paper uses fewer data points per fit and operates at smaller scale. The reviewed paper clearly surpasses the 6.5 anchor in contribution quality. Compared to the cluster of 8.0 papers (Scaling Laws for Precision, Synthetic Continued Pretraining, DEPT), those papers generally have more robust empirical foundations (465 runs, multiple datasets) or cleaner validation. The reviewed paper's reliance on barely-identified power law fits and heuristic HP tuning for its headline claim (5.17×) prevent it from reaching that tier.

**Final assessment:** This paper makes clear, well-organized contributions with genuinely surprising findings (weight decay, ensembling asymptote, self-distillation). The weaknesses are real and meaningful — particularly the precision of quantitative claims exceeding the reliability of evidence — but they bound the strength of conclusions rather than invalidating them. The paper sits solidly between the 6.5 and 8.0 anchors.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>