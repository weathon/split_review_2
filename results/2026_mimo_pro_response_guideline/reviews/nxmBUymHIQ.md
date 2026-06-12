Now I have enough calibration context. Let me finalize the review.

**Calibration Analysis:**

- **Band <3.5 (Strong Reject):** ALLoRA (3.33), HoLoRA (3.0), UnoLoRA (3.0) — rejected LoRA variants with marginal/no improvement, weak theory.
- **Band 3.5-5.5:** GLoRA (4.75, reject), Singular Value Adaptation (3.75, reject), RAC-LoRA (5.00, reject), MoRA (4.75, reject) — rejected papers with theoretical claims but insufficient validation or weak contributions.
- **Band 5.5-7.5:** ReLoRA (5.75, accept), "Optimization Landscape" (6.33, accept), "Expressive Power of LoRA" (6.50, accept), AdaRankGrad (7.00, accept) — accepted papers with stronger theory and/or more convincing practical contributions.
- **Band 7.5+:** HiRA (8.00), Scaling Laws (7.60) — clearly stronger accepted papers.

**Initial bracket: 5.0–6.0.** LoLoRA is clearly stronger than the rejected band-2 papers (has genuine non-trivial theory, clean method, honest multi-domain experiments) but has narrower practical gains and less broadly impactful theory than the 6.33+ papers. It's most comparable to ReLoRA (5.75, accept) — similar borderline quality but different strength profiles (LoLoRA has stronger theory, weaker practical impact).

**Final score: 5.5** (weak accept). The theory (Theorem 4.4, 4.6) is genuine, non-trivial, and well-proven, pushing this above reject territory. The practical contribution (online vs. offline PCA for EVA initialization) is real but narrow, keeping it below strong accept.

---

## Summary
LoLoRA proposes locally updating the LoRA adapter matrix A during the forward pass using gradient-free learning rules (Hebbian PCA/SNL or symmetric autoencoder loss) while training B via backpropagation. The key theoretical contribution is proving (Theorem 4.4) that under a random regression assumption, the optimal A is any nonsingular transformation of the top-r eigenvectors of the input covariance, formalizing the empirical observation behind EVA initialization. The practical advantage over LoRA-FA with EVA is avoiding offline PCA precomputation.

## Strengths
- **Rigorous theoretical characterization (Theorems 4.4, 4.5, 4.6):** Theorem 4.4 provides a closed-form optimality result for A initialization under random regression assumptions, going beyond EVA's empirical observation. Theorem 4.5 (any full-rank B initialization is equivalent) and Theorem 4.6 (autoencoder convergence with all local minima being global) are valuable complementary results. These are genuine, non-trivial contributions.
- **Competitive performance with memory reduction (Table 3):** On LLaMA-3.1-8B-Instruct/GSM8K, LoLoRA HPCA achieves 82.9% accuracy matching LoRA-FA (EVA) while reducing peak extra memory from 30GB (standard LoRA) to 26GB (~13% reduction).
- **Comprehensive ablation (Tables 5-6):** Systematically compares four initialization strategies and five local update rules across ranks r∈{2,4,8}, providing practical guidance that PCA-converging rules (HPCA, AE) perform comparably while SoftHebb underperforms, supporting the theory.
- **Clean algorithmic design (Algorithm 1):** A minimal 7-line modification to the LoRA forward pass requiring no architectural changes.
- **Multi-domain evaluation:** Spans NLU (GLUE/RoBERTa-large), mathematical reasoning (LLaMA-3.1-8B), multimodal (LLaVA-v1.5-7B), and ablations (TinyLlama-1.1B) across 1.1B-8B parameters.
- **Honest reporting:** The paper acknowledges when HPCA does not improve over EVA initialization (LLaVA, Table 4) and admits limitations including stationarity assumptions and extra optimizer state (Section 6).

## Weaknesses

### Fatal
None

### Major
- **Practical gains over LoRA-FA are marginal and often within noise:** On GLUE (Tables 1-2), LoLoRA HPCA underperforms LoRA-FA (uniform) on 5 of 8 tasks (CoLA: 66.3 vs 67.9; RTE: 84.6 vs 86.4; MNLI: 90.3 vs 90.6; QQP: 90.6 vs 90.8; SST-2: 96.4 vs 96.7). On GSM8K (Table 3), the gap with LoRA-FA (uniform) is 0.3pp (82.9% vs 82.6%), within ±0.5% uncertainty. On LLaVA (Table 4), LoLoRA HPCA (2.93) is slightly worse than LoRA-FA (EVA) (2.92). The abstract's claim of "maintaining performance comparable to standard LoRA while further reducing memory" overstates the evidence: LoLoRA matches LoRA-FA variants, not standard LoRA, and the memory savings come from the LoRA-FA design (frozen A), not from LoLoRA's local updates.

- **Narrow baseline comparison for a method claiming memory reduction:** The only baselines are LoRA, LoRA-FA, and EVA. For a paper positioned as "further reducing the memory required for fine-tuning," comparison with other memory-efficient approaches (e.g., GaLore, VeRA, LoRA+) would help contextualize LoLoRA's trade-off in the broader landscape.

### Minor
- **Rank not stated in main text:** The rank used for GLUE, GSM8K, and LLaVA experiments is deferred to Appendix C. Since memory savings depend critically on rank, this should be in the main paper for the tables to be interpretable.
- **Strong theoretical assumptions not validated empirically:** Theorem 4.4 assumes ΔW₀ has i.i.d. Gaussian entries (Assumption 4.1), but real fine-tuning updates are structured. The paper never measures alignment between the actual ΔW₀ (from full LoRA training) and the PCA subspace of inputs, which would directly test whether the theory's mechanism operates in practice.
- **GSM8K reports peak performance over checkpoints:** The model was tested every 0.2 epochs and the best result reported (line 265-266). This inflates all scores equally but means the comparison is on peak, not typical, performance—worth acknowledging more prominently.

## Nice-to-Haves
- Analysis of why HPCA does not improve EVA-initialized adapters on LLaVA—is the input covariance already well-captured by EVA's initialization?
- Wall-clock training time comparison of LoLoRA vs. LoRA-FA across all setups (only LLaVA includes runtime in Table 4)
- Statistical significance testing for differences between methods
- Experiment validating the theory: measure alignment between ΔW₀ (from full LoRA) and PCA subspace of inputs

## Removed Points
These points are flagged to be removed, treat them with caution:
- Remark 4.3 measurability nitpick — too pedantic; the paper provides the mathematical expression and the remark is supplementary.
- Theorem 4.5 being "disconnected from practice" (B initialized to zero in standard LoRA) — while true, the theorem is still theoretically valuable for understanding A/B asymmetry and doesn't harm the paper.
- Claim that "the rank is not stated" was verified as legitimate since Appendix C is stripped, but the information presumably exists in the original paper.

## Novel Insights
The core novel insight is the formal proof (Theorem 4.4) that PCA-based initialization of adapter A is optimal under well-defined random regression assumptions—this is genuinely novel and goes beyond EVA's empirical finding. The complementary result that any full-rank B is equally optimal (Theorem 4.5) formalizes the A/B asymmetry observed empirically. However, the practical insight is incremental: LoLoRA achieves what LoRA-FA(EVA) does, but without requiring an offline PCA precomputation step.

## Suggestions
- Reframe the central narrative around the online-vs-offline distinction (avoiding offline PCA precomputation) rather than positioning against standard LoRA
- Report rank and key hyperparameters in the main text rather than only in the appendix
- Add an experiment measuring alignment between ΔW₀ and the PCA subspace to validate the theoretical mechanism in practice
- Consider adding GaLore or other memory-efficient baselines to situate the contribution

## Reporting

**Anchors retrieved:**
- ALLoRA (3.33, Round 1) — Rejected LoRA variant with marginal improvements; LoLoRA has stronger theory
- HoLoRA (3.00, Round 1) — Rejected LoRA variant; LoLoRA clearly stronger
- UnoLoRA (3.00, Round 1) — Rejected single-adapter LoRA; LoLoRA clearly stronger
- GLoRA (4.75, Round 1) — Rejected adaptive rank LoRA; LoLoRA has better theory and experiments
- Singular Value Adaptation (3.75, Round 1) — Rejected theoretical PEFT; LoLoRA has more concrete results
- RAC-LoRA (5.00, Round 1) — Rejected theoretical LoRA framework; similar theory quality but LoLoRA has better experiments and presentation
- MoRA (4.75, Round 1) — Rejected high-rank LoRA; LoLoRA has cleaner contribution
- ReLoRA (5.75, Round 1) — Accepted; comparable borderline quality; ReLoRA has broader practical impact but weaker theory
- Expressive Power of LoRA (6.50, Round 1) — Accepted; broader theory paper; stronger theoretical contribution than LoLoRA
- Optimization Landscape (6.33, Round 1) — Accepted; stronger theory + practical method; GaRare has marginal GLUE gains similar to LoLoRA
- AdaRankGrad (7.00, Round 1) — Accepted; clearly stronger with better theory and practice
- HiRA (8.00, Round 1) — Clearly stronger accepted paper
- PERFT (5.33, Round 1) — Rejected MoE PEFT; LoLoRA has better theory
- GE-PEFT (4.50, Round 1) — Rejected continual PEFT; LoLoRA has better theory
- Neutral Residues (4.33, Round 1) — Rejected adapter extension; LoLoRA has better theory
- Optimal Adapter Placement (5.00, Round 1) — Rejected adapter placement; LoLoRA has better theory
- ProteinAdapter (3.40, Round 1) — Rejected domain-specific adapter; LoLoRA clearly stronger
- Incremental Learning with Adapters (3.00, Round 1) — Rejected; LoLoRA clearly stronger
- Domain Shift Tuning (3.00, Round 1) — Rejected; LoLoRA clearly stronger

**Round 1 bracket: 5.0–6.0.** LoLoRA sits above RAC-LoRA (5.00, reject) due to cleaner theory and honest multi-domain experiments, and slightly below ReLoRA (5.75, accept) due to narrower practical impact. Final score: 5.5.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>