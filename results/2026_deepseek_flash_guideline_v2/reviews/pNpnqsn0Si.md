Now I have all the evidence I need. Let me produce the final review.

## Summary

Thoughtbubbles proposes a transformer variant that learns to dynamically fork (clone) and delete residual streams during pretraining using only language-modeling loss. The method uses cumulative scores to gate both attention and residual updates, forcing the model to allocate more computation to tokens it deems important. The paper shows consistent perplexity improvements over parameter-matched and computation-matched baselines at 150M–772M scales on OpenWebText and peS2o, with a 319M Thoughtbubbles model achieving *lower* perplexity on OpenWebText than a 772M regular transformer.

## Strengths

1. **Genuinely novel mechanism for unsupervised, input-adaptive allocation of parallel latent computation.** Prior pause-token methods insert extra computation at fixed, manually designed positions. Thoughtbubbles learns *where* to allocate computation using only the LM loss via its score-attenuated attention and residual update equations (Eqs. 8–10). Table 1 shows Thoughtbubbles (κ=4L) outperforms the non-adaptive Copy-5 baseline on *every* perplexity metric across all six model-scale/dataset combinations (e.g., 19.74 vs. 20.90 on OpenWebText 772M), isolating the benefit of adaptivity.

2. **Smaller model surpasses a much larger baseline.** The 319M Thoughtbubbles achieves 20.23 perplexity on OpenWebText, which is *lower* than the 21.22 of the 772M baseline transformer (Table 1, rows OpenWebText 319M Ours κ=4L vs. 772M Baseline). This demonstrates a genuine parameter-efficiency benefit of adaptive parallel computation that standard scaling cannot replicate.

3. **Learned allocation targets semantically meaningful regions without supervision.** Figure 5 shows a clear positive correlation between the number of forks a token receives and its output distribution entropy, measured both by the Thoughtbubbles model itself and by an independently trained baseline LM. This provides direct evidence that the unsupervised allocation policy tracks genuine uncertainty.

4. **Attention analysis confirms forked streams are functionally integrated.** Figure 4 shows the parent ("og") token attends to its child forks with median attention scores an order of magnitude higher than to other tokens, verifying that forked residuals actively participate in computation rather than being inert padding.

## Weaknesses

### Fatal
None.

### Major

1. **No experimental comparison against any prior adaptive computation or pause-token method.** The introduction (Section 1) motivates Thoughtbubbles by critiquing pause-token approaches (Herel & Mikolov 2024; Goyal et al. 2024; Sun et al. 2025), yet the experimental section provides no comparison against them. The Copy-3 and Copy-5 baselines are FLOPs-matched controls — they serve to demonstrate that extra FLOPs alone do not explain the gains — but they do not represent the prior art the paper claims to supersede. Without at least a small-scale comparison (e.g., at 150M) against a pause-token baseline, the reader cannot assess whether the gains come from the specific forking mechanism or simply from having multiple parallel computation paths. This is the most significant gap in the evaluation.

2. **No variance or uncertainty reported for any result.** All results in Table 1 and Figures 3–6 come from single training runs. No standard deviations, confidence intervals, or multiple seeds are provided. This matters because several headline comparisons involve small numeric differences:
   - OpenWebText 772M HellaSwag: Baseline 30.6 vs. Ours κ=2L 31.1 — a 0.5-point gain.
   - peS2o 319M HellaSwag: Ours κ=4L 27.2, Copy-3 27.2 — a tie.
   - PIQA across almost all settings shows differences of 0–2 points, and the baseline sometimes ties or beats Thoughtbubbles.
   
   While single runs are common at this pretraining scale, the paper should at minimum report bootstrap uncertainty on validation metrics or run multiple seeds for one representative scale.

### Minor

1. **BLiMP underperformance is acknowledged but not analyzed.** Across peS2o and most OpenWebText scales, Thoughtbubbles underperforms the Copy baselines on BLiMP (e.g., peS2o 772M: Ours κ=4L 67.4 vs. Copy-3 73.3). The paper attributes this to syntax not benefiting from parallel computation (Section 4) but provides no analysis or ablation. Understanding whether the model prunes residual streams for syntactic tokens, or whether the output averaging harms fine-grained discrimination, would either reveal a genuine limitation or point to a fix.

2. **The top-k gradient bottleneck limits deep forking and is uncharacterized.** The paper acknowledges (Section 8) that too much forking stops improving performance, hypothesizing that early-layer high-scoring tokens are dropped by later top-k decisions, preventing gradient flow. However, it provides no empirical diagnostic — e.g., measuring gradient norms on forking parameters, tracking the survival rate of early high-scoring tokens, or quantifying how often the bottleneck occurs. This leaves the practical severity of the limitation unknown.

3. **Causal masking interaction with score attenuation is underspecified in the main text.** Equation 8 adds a score-based bias to the attention logits: $\text{softmax}((QK^\top + \mathbb{1}\log(P^{(k)})^\top)/\sqrt{d}) (V \odot P^{(k)})$. The main text does not clarify how this interacts with causal masking in autoregressive decoding — e.g., whether low-scoring future tokens are doubly penalized. (The stripped appendix may address this, but the main text should be self-contained on this point.)

### Trivial

1. Parameter matching: The paper states "each setting is parameter-matched" (Table 1 caption) but never explains how — the forking decision functions and fork embeddings add parameters, so presumably the baseline's hidden dimension or layer count is slightly larger to compensate.
2. Fork embedding initialization is not specified.
3. The BLiMP discussion oversimplifies: OpenWebText 772M Ours κ=4L actually *outperforms* computation-matched on BLiMP (81.6 vs. 80.9/81.2), so the claim of consistent underperformance on syntax is not fully accurate.

## Nice-to-Haves

- **Comparison against a pause-token baseline.** Even at 150M scale, comparing against a simple pause-token variant would directly validate the claimed advantage over prior art.
- **Wall-clock efficiency profiling.** The paper acknowledges poor wall-clock efficiency (Section 8) but provides no FLOPs analysis or profiling breakdown. A theoretical FLOPs comparison against baselines would help contextualize the practical cost of adaptivity.
- **Top-k bottleneck diagnostic.** Measuring gradient norms on forking parameters or tracking survival rates of early high-scoring tokens across layers would clarify the practical severity of this limitation.

## Removed Points

These points were assessed against the paper and removed for the following reasons:

- **"Copy baselines are strawman / not competitive"** — Removed because the Copy-3 and Copy-5 baselines serve as valid FLOPs-matched *controls*, not as state-of-the-art competitors. They demonstrate that simply adding more FLOPs (without adaptivity) does not match Thoughtbubbles' gains, which is a scientifically meaningful comparison. The critic's "strawman" characterization overstates the case. However, the related concern about missing comparison with actual pause-token methods is kept as a Major weakness above.
- **"First-known claim should be tempered"** — Removed because it is a framing judgment without clear evidence of falsehood; the paper carefully scopes its novelty claim.
- **"Wall-clock efficiency is a significant gap"** — Moved to Nice-to-Haves because the paper already acknowledges this limitation transparently in Section 8.
- **"Missing related works"** — Removed per policy (I cannot independently verify whether any specific work is missing).
- **Strength Finder's claim "Computation-matched baselines isolate the adaptive advantage"** — Dropped because it overstates what these baselines demonstrate; the Copy baselines are controls, not isolates of adaptivity per se. The other strengths are retained.

## Novel Insights

None beyond the paper's own contributions. The Harsh Critic and Strength Finder both surface the same core observations: the method is genuinely novel and the perplexity results are compelling, but the evaluation is weakened by the absence of comparisons against prior adaptive computation methods and by the lack of variance information. No reviewer-identified insight meaningfully extends the paper's own analysis.

## Suggestions

1. **Add at least one comparison against a pause-token baseline** at a smaller scale (e.g., 150M) or, if truly infeasible, acknowledge this gap explicitly with a discussion of expected theoretical trade-offs.
2. **Report variance.** Run 2–3 seeds for one representative scale (e.g., 150M) or report bootstrap uncertainty on validation metrics to establish which comparisons are statistically reliable.
3. **Diagnose the top-k gradient bottleneck empirically.** Measure gradient norms on the forking decision parameters or track the survival rate of early-layer high-scoring tokens across layers.
4. **Analyze BLiMP degradation.** Investigate whether forked streams are pruned for syntactic tokens or whether the output averaging mechanism causes the drop.
5. **Clarify causal masking interaction** with score-based attention attenuation in the main text.
6. **Explain the parameter matching scheme** explicitly so readers can verify the comparison is fair.

## Score and Decision

Due to the unavailability of the calibration tool, I calibrated based on the ICLR scoring scale (1: strong reject, 3: reject, 4: borderline reject, 6: borderline accept, 8: accept, 10: strong accept) and compared against the content of the paper.

**Reasoning:** The paper presents a genuinely novel architectural idea (the forking mechanism) with consistent perplexity improvements, including the striking result of a 319M model outperforming a 772M baseline. The mechanism is well-motivated and the analysis provides qualitative support that forks are used meaningfully. However, the evaluation has real gaps: no comparison against any prior adaptive computation method (the very methods the paper critiques), no variance estimates for any result, and limited analysis of known degradations (BLiMP). These gaps prevent a higher score but do not undermine the core contribution. The paper would benefit substantially from a rebuttal that addresses the baseline comparison gap and adds variance information.

**Score:** 6 — The paper is on the positive side of the borderline. The core idea is novel and interesting enough to warrant presentation, but the evaluation as presented has significant gaps that should be addressed.

FINAL SCORE: <score>6</score>
FINAL DECISION: <decision>Accept</decision>