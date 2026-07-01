Now I have all the information needed. Let me produce the final consolidated review.

## Summary

The paper proposes LoLoRA, a variant of LoRA that replaces gradient-based training of the A matrix with local unsupervised (Hebbian) HPCA updates during the forward pass, avoiding storage of A's input activations while allowing A to adapt. The paper also provides a theoretical analysis (Theorem 4.4) proving that under a random linear regression model, the optimal A spans the top principal components of the input covariance, providing formal justification for PCA-based initialization (EVA) and for HPCA-based online adaptation.

## Strengths

1. **Clean theoretical result (Theorem 4.4, Section 4).** The paper proves that under a random linear regression model (Assumptions 4.1–4.2), the optimal A matrix spans the top *r* principal components of the input covariance matrix, up to a nonsingular transformation. This provides a formal mathematical justification for PCA-based initialization (EVA) and for Hebbian PCA updates as a means of converging to this subspace. The proof is the paper's most original contribution.

2. **Asymmetry result (Theorem 4.5, Section 4).** The parallel result showing that any full-rank B matrix is equally good under the same model sharpens the theoretical understanding of the two adapters' roles, consistent with prior empirical findings.

3. **Moderately thorough ablation study (Section 5.4, Tables 5–6).** The comparison of five local update rules (HPCA variants, AE, SoftHebb) on TinyLlama-1.1B provides useful information about which local learning rules are viable, with multiple ranks tested.

## Weaknesses

### Fatal
None.

### Major

1. **Central empirical claim is not supported by the evidence.** The paper's framing (abstract, conclusion) positions LoLoRA as mitigating the LoRA-FA performance-memory trade-off by allowing A to adapt. Across the three experimental setups, the evidence contradicts this:

   - **GLUE (Tables 1–2, largest experiment with 8 tasks):** LoLoRA HPCA is numerically worse than LoRA-FA (uniform) on 5 of 8 tasks, better on 2, and tied on 1 — all differences within noise. The summary concedes "classical LoRA remains the strongest overall."
   - **Math (Table 3):** LoLoRA HPCA (0.829±0.004) ties with LoRA-FA (EVA) (0.829±0.005) and beats LoRA-FA (uniform) (0.826±0.005) by 0.003 — less than one standard error.
   - **LLaVA (Table 4):** LoLoRA HPCA (loss 1.075±0.002) beats LoRA-FA (uniform) (1.087±0.003) but is *worse* than LoRA-FA (EVA) (1.070±0.004). The paper acknowledges "HPCA updates do not improve EVA-initialized adapters."

   The conclusion states "HPCA consistently outperforms standard LoRA-FA in two out of three experimental setups" — this overstates marginal, within-noise differences. The best characterization across all experiments is that LoLoRA is statistically indistinguishable from LoRA-FA (EVA) and does not offer a clear performance advantage.

2. **Memory claims are misleading relative to the relevant baseline.** The abstract claims "further reducing the memory required for fine-tuning," but this comparison is against standard LoRA, not against the directly relevant frozen-A baseline (LoRA-FA). Against LoRA-FA, LoLoRA offers zero memory savings (Math: both 26 GB, Table 3) or slightly *more* memory (LLaVA: 24.1 vs 23.9 GB, Table 4). The paper acknowledges this indirectly ("our method introduces a small amount of extra optimizer state for the local updates, unlike standard LoRA-FA"), but the consistent framing implies LoLoRA improves the memory-performance trade-off relative to LoRA-FA, which is not supported by the reported numbers.

3. **Claimed advantage over EVA does not materialize.** The paper's key differentiator from EVA (Paischer et al., 2024) is "iteratively adapt[ing] A during fine-tuning to the optimal subspace" rather than fixing it after one-time PCA initialization. However, LoLoRA does not outperform LoRA-FA (EVA) in the experiments — it is equivalent or slightly worse. If inputs were stationary (as the theory assumes), HPCA should converge to the same subspace as one-time PCA and should not outperform it. If inputs are non-stationary (the realistic case), the paper provides no analysis of whether HPCA tracks changing distributions effectively. The practical advantage reduces to avoiding a separate PCA pre-computation pass, which is a modest convenience gain, not a substantive improvement.

### Minor

1. **Theory-practice gap.** The theoretical analysis (Section 4) assumes: (a) a single linear layer, (b) random i.i.d. Gaussian targets (no downstream structure), (c) stationary input distributions, (d) isolated submodules. These assumptions are far from the LLM fine-tuning setting. The paper acknowledges some limitations in the conclusion ("we considered each submodule isolated with stationary targets"), but the theory is presented as directly motivating the method without clearly discussing when the assumptions break and why the method might still be expected to work.

2. **Runtime cost of local updates not decomposed.** Table 4 shows LoLoRA is slower than LoRA-FA (2h52m vs 2h46m for LLaVA), but the computation cost of the HPCA forward-pass update itself is not isolated or analyzed separately from other factors.

3. **PiSSA absent from main experiments.** PiSSA (Meng et al., 2024) appears only in the TinyLlama ablations (Table 5), not in the main GLUE, Math, or LLaVA comparisons (Tables 1–4). As a prominent informed-initialization baseline, its absence from the primary experimental comparisons is a gap.

### Trivial
None.

## Nice-to-Haves

- Statistical significance testing (e.g., paired bootstrap across GLUE tasks) to support claims of "outperformance" rather than relying on visual inspection of standard errors.
- Analysis of whether HPCA's online adaptation actually moves A toward a different subspace than the initial PCA estimate during training, which would validate the claimed benefit of iterative adaptation over one-time initialization.
- Longer training or larger models to test whether the benefits of online adaptation emerge with more distribution shift.

## Removed Points

These points were removed from the input review for the following reasons:

- *"Section 5.2 (Lines 277): Claims '13% extra memory reduction' — this is 30→26 GB for both LoRA-FA and LoLoRA, not an advantage specific to LoLoRA."* — REMOVED because the paper text explicitly says "LoRA-FA and LoLoRA HPCA achieve approximately 13% extra memory reduction," attributing the savings to both methods jointly, not to LoLoRA alone.

- *"Missing Appendix D"* and *"The paper references Appendix D for memory analysis multiple times."* — REMOVED per policy: the parser strips appendix sections from all papers; they exist in the original submission.

- *"Full LoRA (uniform) achieves strictly better perplexity than all LoLoRA variants across all ranks, yet the paper does not discuss this gap."* — REMOVED because Table 6 presents full LoRA as a reference point, and the paper already acknowledges "classical LoRA remains the strongest overall." This is illustrating the known cost of freezing A, not a gap the paper ignores.

- *"The paper provides no analysis of whether HPCA can track the changing distribution effectively"* (regarding non-stationarity) — REMOVED from standalone status and subsumed into the theory-practice gap weakness, where the paper's own acknowledgment of this limitation is noted.

- *"Section 5.4 (Table 6)... the paper does not discuss this gap"* — The paper explicitly notes "On Alpaca, the most stable and best results are obtained by HPCA (svd first), classic HPCA and AE" and presents full LoRA as a reference. The gap between full LoRA and any frozen/limited-A method is well-understood in the literature.

- *Counting inaccuracies in the reviewer's summary of GLUE results* — The claim of "strictly worse on 6 out of 8 tasks" is factually incorrect (it is worse on 5, better on 2, tied on 1 by strict numerical comparison, all within noise). The overall conclusion (LoLoRA does not outperform LoRA-FA on GLUE) stands, so the corrected version is used in this review.

## Novel Insights

None beyond the paper's own contributions. The core insight is that the theoretical result (Theorem 4.4) unifies several prior empirical findings (EVA, PiSSA-style initialization, the asymmetric roles of A and B) under a single optimality framework. The harsh review did not surface any novel analysis or framing beyond what the paper already provides.

## Suggestions

1. **Re-frame the paper's contributions.** Tone down the "mitigating the trade-off" and "outperforming" framing to match the evidence. The paper would be more credible if positioned primarily as: (a) a theoretical justification for PCA-based A initialization, with (b) an empirical investigation showing that LoLoRA achieves equivalent results to LoRA-FA (EVA) without requiring a separate PCA pre-computation pass, at a small memory/runtime cost.

2. **Quantify when HPCA adaptation matters.** If the benefit of online adaptation over one-time PCA is the main differentiator, provide direct evidence — measure distribution shift during fine-tuning and show HPCA tracking it, or compare LoLoRA against EVA under longer training where more shift accumulates.

3. **Fix the memory framing.** Be explicit that the memory savings are relative to standard LoRA, not to LoRA-FA, and report the small extra memory cost of LoLoRA relative to LoRA-FA (optimizer state for local updates) clearly in the main text.

## Score and Decision

MY FINAL SCORE: 4
MY FINAL DECISION: Reject