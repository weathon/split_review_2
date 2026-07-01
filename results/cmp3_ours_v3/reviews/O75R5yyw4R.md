## Summary

The paper proposes IterRef, a test-time scaling method for discrete diffusion models that uses Multiple-Try Metropolis (MTM) to iteratively refine intermediate states via noising-denoising transitions. The method is evaluated across text (MDLM, LLaDA-8B) and image (MaskGIT) domains with multiple reward functions, consistently outperforming baselines (BoN, SoP, SVDD, FK). Key analyses show that refinement is most effective at later denoising stages and that increasing iterations is more beneficial than increasing particle count.

## Strengths

1. **Principled theoretical framing (Section 3).** The adaptation of MTM to discrete diffusion is technically clean: the transition kernel K combines noising and denoising, and the balancing function λ simplifies the acceptance ratio to β = min(1, exp((r(x_t')−r(x_t))/α)), which depends only on the reward difference. This is elegant and computationally advantageous.

2. **Broad evaluation scope.** The paper evaluates across two modalities (text and image), three backbones (MDLM, LLaDA-8B, MaskGIT), and multiple reward functions (Toxicity, Sentiment, CoLA, Perplexity, CLIPScore). The MaskGIT results (Table 1) demonstrate the method transfers to images without modification.

3. **Informative analysis of refinement placement (Table 2).** The finding that later denoising stages (0.1T–0.3T) are more effective for IterRef, contrasting with continuous diffusion where early steps dominate, is genuinely useful. It gives practitioners concrete guidance on where to allocate compute.

4. **Scaling analysis: iterations vs. particles (Table 3, Figure 4).** The systematic comparison showing that increasing iterations k is more effective than increasing particles N directly supports the paper's core thesis.

## Weaknesses

### Fatal
None.

### Major

1. **Missing directly competitive baselines.** The Related Work (Section 5) discusses PG-DLM (Dang et al., 2025, Particle Gibbs resampling of entire trajectories), DSearch (Li et al., 2025, search-based alignment), and DTS (Jain et al., 2025, MCTS-based value backup) — all methods specifically developed for reward-guided discrete diffusion. None are included in the experiments. The paper claims IterRef "consistently outperforms prior reward guidance methods" (Contributions, line 33), but PG-DLM in particular is a direct competitor that also performs iterative refinement of intermediate states via Gibbs sampling. Without these comparisons, the strongest claims about state-of-the-art performance are unsubstantiated. This is the single most important weakness and should be addressed in any revision.

### Minor

2. **NFE accounting conflates cost structures.** The paper treats generative-model calls and reward-model calls as equivalent NFEs (Section 4.1). As the authors themselves note (Section 3.3, line 174), "aggregating these into a single NFE value may obscure meaningful differences." For large models like LLaDA-8B, diffusion-model calls dominate, while IterRef's cost profile differs from SMC-based methods in how often the reward model is called. The paper references Appendix C.4 for wall-clock analysis, but the main paper's narrative relies entirely on NFE comparisons.

3. **The "8× faster" claim is tied to a single data point.** The claim (Section 4.2, line 200) refers to IterRef at 4T NFEs matching FK at 32T NFEs on Toxicity with MDLM. While qualified with "nearly" and "up to," this specific crossover point is presented as a headline in Figure 1 and the abstract. On MDLM with Toxicity the gap actually narrows at higher NFEs (line 202).

4. **Proposition 1's reversibility assumption is unverified.** The convergence guarantee assumes "q and p_θ form a reversible Markov kernel" (line 146). In absorbing-state discrete diffusion, q adds mask tokens and p_θ is a learned approximation of the true posterior — these are not generally reversible for finite-capacity models. The paper does not discuss how violations affect the guarantee. While common in theoretical ML work, this disconnect between the clean theory and empirical conditions is worth noting.

5. **Cost accounting inconsistency (Section 3.3 vs. Eq. 3).** The complexity analysis states "N reward-model evaluations required for computing the acceptance ratio" (line 174). However, with the simplified acceptance ratio (Eq. 3), β = min(1, exp((r(x_t')−r(x_t))/α)), only one reward evaluation is needed (for the selected proposal; r(x_t) is already known). This appears to describe the general MTM algorithm before the simplification with λ, but the inconsistency is confusing and should be clarified.

6. **Safety experiment uses a small evaluation set.** The detoxification experiment (Section 4.5) uses 15 prompts × 20 samples = 300 generations total. For a safety-critical claim, this is a modest sample. No per-prompt variance is reported.

7. **No error bars on results.** The main paper reports no standard deviations or confidence intervals. Given the modest sample sizes (15 prompts), difference significance is unclear.

8. **Figure 5(a) uses unexplained baselines.** The detoxification figure shows baselines labeled SLP, SR, SVTOD alongside "IterRef" and "Ours." These names do not match the main experiment baselines (FK, SVDD, SoP, BoN) and are not defined in the caption or text.

9. **Choice of s (how far to noise) is not analyzed.** The transition kernel K involves noising to a timestep s > t. The paper does not explain how s is chosen or ablate its effect, though this controls the exploration-exploitation trade-off.

### Trivial
None.

## Nice-to-Haves
- Adding confidence intervals or standard deviations.
- Analyzing whether IterRef induces reward over-optimization (the Ethics Statement mentions this concern but the paper does not evaluate it).
- Ablating the choice of s (how far to noise).
- Explaining the baselines in Figure 5(a) in the main paper.
- More thorough analysis of why BoN outperforms IterRef on CoLA with LLaDA-8B.

## Removed Points
- **Criticism about "tokens cannot be corrected" contradicting the method (Harsh Critic section-by-section note 1).** The paper describes this as a limitation of *standard* discrete diffusion (line 15), which is correct — standard single-pass denoising does fix tokens. IterRef is presented as overcoming this limitation. The reviewer misread this as the paper claiming a fundamental impossibility rather than describing existing methods' limitation. *Removed: misreading of paper.*
- **Criticism that the "Evenly" column in Table 2 trivially outperforms single-step allocations.** The comparison is fair: the budget is fixed (4T NFEs at each selected step), and "Evenly" distributes the same total compute differently. The paper notes that 0.1T sometimes beats Evenly (CoLA), which is the genuinely interesting finding. *Removed: does not reflect actual paper content.*
- **Criticism about missing appendix, missing proofs, or absent references.** The parser strips these sections; they exist in the original submission. *Removed: parser artifact.*

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add PG-DLM as a baseline to substantiate the claim of outperforming prior reward guidance methods. DSearch and DTS would further strengthen the comparison. This is the single most impactful improvement.
2. Move the wall-clock analysis (Appendix C.4) to the main paper or at least summarize the key finding in the main text to address the NFE accounting concern.
3. Add error bars to all experimental results.
4. Clarify the cost analysis in Section 3.3: explain why N reward-model evaluations are stated versus the 1 needed for Eq. 3.

---

### Calibration Anchors

**Round 1 — Bracketing (5.5–6.5)**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/2fgzf8u5fP.md` (SVDD) | 3.80 | R1 | Same problem setting (reward-guided discrete diffusion), but weaker method and narrower evaluation. This paper is clearly stronger. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/x1uv2gdjKV.md` (DNO) | 5.50 | R2 | Inference-time alignment of diffusion models; rejected partly due to missing baselines — same issue. This paper has a more principled method and broader evaluation. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Aye5wL6TCn.md` (Nabla-GFlowNet) | 6.00 | R2 | Reward finetuning of diffusion models; accepted. Comparable methodological novelty and evaluation breadth. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/peNgxpbdxB.md` (Scalable Discrete Diffusion Samplers) | 6.00 | R1,R2 | Discrete diffusion for sampling; accepted. Similar evaluation depth and clarity. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Ombm8S40zN.md` (DDPP Steering) | 6.25 | R2 | Same problem (steering discrete diffusion for reward); accepted. Broader evaluation (incl. wet-lab) but less novel method. Comparable overall. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/XsgHl54yO7.md` (Unlocking Guidance) | 6.50 | R2 | Guidance for discrete diffusion/flow; accepted. Broader scientific applications. Similar methodological contribution. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/pq1WUegkza.md` (Convergence of Score-Based Discrete Diffusion) | 7.00 | R1,R2 | Theory-focused discrete diffusion paper; accepted. More rigorous theory, narrower scope. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/kIPEyMSdFV.md` (Reverse Diffusion Monte Carlo) | 7.00 | R1 | Methodologically related (MCMC + diffusion); accepted. Stronger theoretical analysis. |

**Narrowing:** The paper is clearly stronger than SVDD (3.80) and DNO (5.50, rejected), comparable to DDPP (6.25, accepted) and Nabla-GFlowNet (6.00, accepted), and weaker than the theory-focused papers (7.00). The missing-baselines issue is the primary factor preventing a higher score.

**Final Score: 6.0** — The paper makes a genuine contribution (principled MTM adaptation with clean theoretical framing, broad evaluation, and insightful analyses) but the absence of directly competitive baselines (PG-DLM, DSearch, DTS) weakens the central claim of "consistently outperforming prior reward guidance methods." With these baselines added, the score would likely rise to 6.5–7.0.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>