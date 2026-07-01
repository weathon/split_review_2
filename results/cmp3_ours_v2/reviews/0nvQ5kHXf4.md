Now I have enough calibration data. Let me produce the final review.

## Summary

This paper proposes WASI (Weight-Activation Subspace Iteration), a method for resource-constrained fine-tuning of transformers that jointly compresses both weights and activations into low-rank subspaces during training. WASI extends prior work on Activation Subspace Iteration (ASI) by also decomposing weight matrices, enabling inference in the compressed representation. The method uses an initial SVD followed by warm-started subspace iteration to avoid expensive full decompositions, under the assumption that the essential subspaces remain stable during fine-tuning. Experiments on ViT, SwinT, and TinyLlama show favorable accuracy-efficiency trade-offs against vanilla training, ASI, and SVD-LLM, with a hardware demonstration on a Raspberry Pi 5.

## Strengths

- **Joint compression of weights and activations is a meaningful extension of prior art.** Prior work (ASI) compressed activations during training but left weights intact, so inference cost remained high. WASI extends this to weight matrices, enabling inference in the compressed representation. This is a clear conceptual advance over ASI, and the method design (subspace iteration applied to weights, warm-started from an initial SVD) is technically sensible.

- **The core stability assumption is experimentally validated.** Fig. 3a shows that the ranks of weight matrices (which singular values to keep under a fixed explained-variance threshold) remain stable across 40 epochs of fine-tuning ViT on Pets. This directly supports the claim that the weight subspace can be reused without recomputing the full SVD at every iteration — evidence that many papers in this area state without providing.

- **Real hardware deployment.** The Raspberry Pi 5 experiment (Fig. 8) demonstrates the method on actual edge hardware, not just in simulation. The per-iteration training speedup is visually clear and monotonic in the compression rate.

## Weaknesses

### Fatal

None.

### Major

- **Missing LoRA baseline.** LoRA is discussed at length in the introduction (line 25) and related work (lines 41–45) as a major category of approach, and the paper critiques LoRA's limitations (adapter memory overhead, no inference compression). Yet LoRA is never evaluated as a standalone baseline. The closest comparison is SVD-LLM, which uses LoRA adapters on top of SVD-decomposed weights — a qualitatively different method from vanilla LoRA. Since the paper positions WASI against "LoRA-style approaches," the absence of a direct LoRA comparison is a significant evidential gap that prevents the reader from assessing whether WASI's claimed advantages hold against the most widely used efficient fine-tuning method.

- **TinyLlama experiment is poorly controlled and overclaims.** Several issues (lines 227–237): (i) ε=0.1 is far more aggressive than the ε=0.9 used for the headline 62× memory claim, yet this discrepancy is not explained. (ii) The paper never reports what vanilla fine-tuning on BoolQ achieves, so the claim that "WASI consistently achieves higher accuracy than Vanilla" (Fig. 7 caption) lacks an anchor — we don't know if both methods are near state-of-the-art or both near the 50% random baseline. (iii) The 953.86× activation memory reduction at ε=0.1 is extraordinary and would require much more careful validation (for context, the SwinT results claim 62× at ε=0.9). (iv) The paper states the experiment was limited to the last 5 layers "due to limited resources" (line 227), suggesting a preliminary exploration, yet presents the extreme numbers in the main text without appropriate caution.

### Minor

- **On-device evaluation reports only per-iteration time, not total training cost.** Fig. 8 shows time per training iteration and per inference iteration on a Raspberry Pi 5. However, the key question for on-device learning is whether WASI converges to the same accuracy in the same number of iterations. If the method requires more iterations (due to truncation error accumulation), the per-iteration speedup could be partially or fully offset. The paper does not report learning curves, final accuracy on the device, or total training time to convergence.

- **Abstract's "up to 2× FLOPs" claim does not match any stated experimental result.** The SwinT experiment reports "FLOPs by 1.5×" (line 225). The TinyLlama experiment gives much larger numbers (13.11× training, 30.27× inference) but at ε=0.1 with only 5 layers fine-tuned. The abstract's "up to 2×" does not clearly correspond to any result in the main text, giving an inflated impression of the method's capabilities.

- **Subspace stability evidence is incomplete.** The paper shows that singular value magnitudes (and hence ranks) are stable (Fig. 3a), but subspace iteration additionally requires that the *subspace orientation* (the directions, not just the number of components) is stable. Measuring principal angles between subspaces at consecutive iterations would provide more direct validation. The empirical success of WSI vs. full SVD (Fig. 3b) partially mitigates this, but the theoretical argument would benefit from stronger evidence.

- **SVD-LLM baseline usage creates tension with the paper's own scope statements.** The paper states that SVD-LLM "cannot be directly applied to all vision transformer-based models" (lines 27, 47) and references Appendix A.4 for explanation, yet uses SVD-LLM as a primary baseline on ViT (Fig. 5). The appendix presumably explains the adaptation, but this tension in the main text is confusing. The paper should more clearly state how SVD-LLM was adapted and whether this adaptation may have handicapped its performance.

### Trivial

- The claim of being "the first method for efficient model-activation-decomposition-aware training" (line 29) could be more precisely stated, since ASI already does activation decomposition. WASI's novelty is in doing both simultaneously.
- The conclusion's claim that "the underlying principles apply broadly to any neural network trained with backpropagation" (line 259) is unsupported — experiments only cover transformers.

## Nice-to-Haves

- A convergence analysis showing whether WASI requires more or fewer epochs to reach the same validation loss as vanilla training.
- If the Raspberry Pi experiment were run to completion (reporting final accuracy and total training time), it would substantially strengthen the practical claims.

## Removed Points

These points are flagged to be removed, treat them with caution:

- *Ablation criticism (no separation of WSI and ASI):* Removed because Fig. 5 compares WASI vs. ASI directly, and the difference between them *is* the marginal contribution of weight compression — the ablation exists as presented.
- *Critique that LoRA's memory criticism is overstated:* Removed — the paper's claim that LoRA requires both frozen weights and adapters in memory during training is factually correct; the degree of overhead is debatable but not a factual error.
- *Request for quantization comparison:* Removed as scope creep — the paper explicitly scopes to low-rank decomposition methods (line 39).
- *Claims that SVD-LLM adaptation is unexplained:* Weakened — the paper references Appendix A.4, which exists in the original submission. The tension in the main text is retained but not the accusation of missing explanation.
- *Formatting/style nitpicks:* Removed as parser artifacts per instructions.

## Novel Insights

None beyond the paper's own contributions. The reviews offer a careful catalog of evaluation gaps but no novel technical insight that the paper itself misses.

## Suggestions

1. **Add LoRA as a standalone baseline** on at least one vision task (ViT/CIFAR-10) and one language task (TinyLlama/BoolQ). This is the most impactful improvement.
2. **Run the Raspberry Pi experiment to completion** — report final accuracy and total training time, not just per-iteration time.
3. **Fix the TinyLlama experiment** — report vanilla accuracy on BoolQ, use comparable ε values, and either verify or remove the 953× claim.
4. Add principal-angle measurements between consecutive subspaces to directly validate subspace stability.
5. Reconcile the abstract's "up to 2× FLOPs" with the experimental results (SwinT gives 1.5×).
6. Clarify in the main text how SVD-LLM was adapted to work on vision transformers, given the paper's own statement that it is not readily applicable.

## Calibration Report

**Anchors retrieved (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| SubTrack-Grad (nR0n4R1Ck2) | 4.75 (Reject) | R1 | Very similar concept (gradient subspace tracking for memory-efficient training); WASI has stronger empirical validation (hardware results, stability validation) but similar evaluation gaps |
| SubZero (FK6T0U4Mg1) | 4.25 (Reject) | R1 | Similar goal (memory-efficient training) but different technique (ZO vs SVD); WASI has relatively stronger empirical eval but no theory |
| Subspace Opt. for LLMs (udtrtwkvk5) | 5.25 (Reject) | R1 | Convergence analysis paper; mostly theoretical, less directly comparable |
| TinyTrain (xNdE7RiRyP) | 5.25 (Reject) | R2 | On-device training at edge; WASI has clearer novelty but TinyTrain has more thorough on-device metrics |
| Memory-Efficient FT via Pruning (JMgxtZqkvO) | 4.50 (Reject) | R2 | Pruning-based efficient fine-tuning; less directly comparable |
| Harnessing Orthogonality (0tsJ7Nv5hk) | 4.25 (Reject) | R2 | Low-rank training via SVD; similar technical approach but less applied |
| Activations Aren't Cheap (3ylNuZXtMg) | 4.25 (Reject) | R3 | About activation memory in LoRA; tangentially related |

**Round 1 bracket:** 4.5–6.0

**Narrowing:** The most similar paper (SubTrack-Grad, 4.75) was rejected with similar critiques about missing baselines and limited evaluation. WASI is empirically stronger (hardware results, stability validation, multiple vision datasets) but has similar evaluation gaps (missing LoRA baseline, TinyLlama issues). The score sits at 5.0 — borderline reject. The method has genuine merit, but the evaluation does not fully substantiate the paper's central claims against the most relevant competitors.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>