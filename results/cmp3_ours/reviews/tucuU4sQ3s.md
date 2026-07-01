I have sufficient calibration data. Here is the final consolidated review.

---

## Summary

NuSA-CL proposes a memory-free continual learning method for CLIP that identifies low-energy subspaces (the "null space") of weight matrices via SVD before each task, then constrains LoRA-like updates to lie strictly within this subspace via frozen basis matrices (U_n, V_n). After training, the update is merged into the backbone, maintaining a fixed parameter budget with no replay buffer, gradient memory, or expanding modules. The method is evaluated on the MTIL benchmark (11 diverse vision datasets), CIFAR-100 class-incremental learning, and a 5-shot variant.

## Strengths

1. **Clean, well-motivated method with a genuine differentiator.** Using SVD of the weight matrix *itself* (not gradients, activations, or stored data) to identify a low-interference subspace for continual updates is novel and distinct from prior orthogonal-projection methods that require storing past information (InflLoRA, GPM, etc.). The persistent constraint — freezing U_n, V_n throughout training — is the key design choice that separates this from subspace-initialization methods like MiLoRA, and the ablation in Table 4a convincingly shows it matters (Transfer drops from 68.58% to 62.60% when U_n, V_n are also trained).

2. **Genuinely storage-free with a fixed parameter budget.** At 1.5M trainable parameters and 1.21 GPU-hours for the full MTIL benchmark, the efficiency numbers are concrete and impressive. The method requires no replay buffer, no growing prompt pool, no expanding adapter library, and no gradient memory — a real contribution for resource-constrained deployment.

3. **Strong empirical evidence for the mechanism, not just outcomes.** Figure 2's null-space dynamics analysis shows NuSA-CL's effective rank progressively increasing across tasks, while LoRA and Full-FT remain static. This provides direct evidence that the method accumulates knowledge by filling low-energy subspaces rather than overwriting principal components — a genuinely insightful diagnostic that goes beyond reporting aggregate metrics.

4. **Robust ablation study.** Subspace selection analysis (Figure 3a) shows Tail consistently outperforming Top and Random across ranks 32–256, validating that low-energy directions truly cause less forgetting. Hyperparameter sensitivity (Table 4b, ρ from 0.80 to 0.999) shows stable performance, which is practically important. The SVD efficiency analysis (Init. Time < 1 min) is also useful.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

1. **Prompt-based CL baselines are not compared.** Methods like L2P, DualPrompt, and CODA-Prompt are among the most prominent continual learning approaches for vision-language models. The paper mentions them in Related Work (Sec 2.1) but does not include them in Tables 1–3. While these methods use expanding prompt pools and thus fall outside the paper's "storage-free" scope, a comparison against a fixed-prompt-budget variant would substantially strengthen the empirical positioning. Without this, the claim of "new state-of-the-art within the storage-free setting" is less thoroughly supported than it could be.

2. **Theoretical framing overpromises.** Lemma 1 and Theorem 2 bound parameter-space inner products (⟨W, ΔW⟩\_F), not function-level forgetting. A small parameter-space inner product does not imply small function change, even under smoothness assumptions. The paper acknowledges this limitation ("should be viewed as a local stability condition rather than a full function-level guarantee") but the surrounding framing presents the theory as providing "a principled mechanism for mitigating catastrophic forgetting." The framing should be tightened; the theory is useful as motivation but does not constitute a forgetting guarantee.

3. **Training details for main results are underspecified.** The paper reports "1000 training iterations per task" for ablations (Sec 6.2) but does not state the learning rate, optimizer, batch size, scheduler, or weight decay used for the main MTIL and CIFAR-100 results. This affects reproducibility.

4. **No statistical significance reported.** For close comparisons (e.g., NuSA-CL 82.8% vs InflLoRA 83.6% Last in Table 1), the absence of error bars, confidence intervals, or significance tests makes it impossible to assess whether differences are meaningful.

5. **The data regime for the "full-shot" MTIL benchmark is not specified.** How many examples per task? Is this the full training set for each dataset? This basic experimental detail should be stated in the setup.

6. **Only evaluated on ViT-B/16.** The paper discusses scaling to larger backbones (Sec 6.3) but provides no experiments with ViT-L/14 or similar. While this does not invalidate the results, it limits the scope of the scalability claims.

### Trivial

- Units in Table 1's "Additional Storage" column mix GB and MB without clear grouping (e.g., "Grad. Proj. Mem. (9MB)" alongside "Data&Model (10.5GB)"). Consistent formatting would improve readability.

## Nice-to-Haves

- Compare against at least one prompt-based CL method (e.g., L2P or CODA-Prompt) with a fixed prompt budget on the MTIL benchmark.
- Include at least one additional long-sequence benchmark beyond CIFAR-100 (e.g., a cross-domain sequence or ImageNet-R) to strengthen the scalability claim.
- The theory section would benefit from being explicitly framed as providing a local stability condition in parameter space rather than a forgetting guarantee.

## Removed Points

These points from the input review were removed with justification:

- **"Memory-free framing overstated vs InflLoRA (9MB is negligible):** Removed because the paper is transparent about the 9MB figure and correctly classifies InflLoRA as storage-based. The classification is technically correct, and the table allows readers to judge for themselves. Whether 9MB is "negligible" is a subjective value judgment.
- **"CIFAR-100 baselines don't cover more recent class-incremental methods":** Removed because LwF (2017), ICaRL (2022), LwF-VR (2022), and ZSCL (2023) constitute a reasonable baseline set for this benchmark. The paper does not claim exhaustive coverage.
- **"Overclaimed 'decisively outperforming InflLoRA' selective quoting":** Removed because the paper's statement about "decisively outperforming" applies specifically to the 5-shot benchmark (Table 2), where NuSA-CL leads on all three metrics (Transfer 68.1 vs 66.8, Avg 70.3 vs 68.9, Last 75.4 vs 74.8). The full-shot results (Table 1) are discussed more neutrally as "highly competitive."
- **"Which layers receive adaptation not stated upfront":** Removed because Sec 6.3 explicitly states "attention projection matrices (W_q, W_k, W_v, W_o)" and this is sufficiently clear within the method section's flow.

## Novel Insights

The harsh critic's analysis identified an interesting tension in the paper: the theoretical section (Sec 4) provides *parameter-space* bounds but the empirical analysis (Sec 6, especially Figure 2) delivers the actual mechanistic insight. The most compelling case for the method comes not from the theory but from the spectral dynamics visualization — the progressive increase in effective rank across tasks. This suggests the paper might be better served by repositioning the theoretical analysis as post-hoc motivation for the spectral dynamics rather than as a forward guarantee, and expanding the empirical analysis of why the null-space constraint produces additive rather than overwriting learning dynamics.

## Suggestions

1. Add at least one prompt-based CL baseline (e.g., L2P with a fixed prompt budget) to Tables 1–2.
2. Report training hyperparameters (learning rate, optimizer, batch size, scheduler, weight decay) for all main experiments, either in the main text or an appendix.
3. Include error bars (e.g., 3 random seeds) for the key comparisons in Tables 1 and 3.
4. Explicitly state the data regime (number of examples per task) for the "full-shot" MTIL benchmark.
5. Tighten the theoretical framing to clarify that the bounds are on parameter-space interference, not function-level forgetting.

---

**Calibration Anchors Report:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| LVLM-CL (JIlIYIHMuv) | 2.50 | R1 | VLM CL; weaker method with more serious flaws. NuSA-CL is substantially stronger. |
| Projected Subnetworks (WM5G2NWSYC) | 2.00 | R1 | CL+PEFT; less rigorous evaluation. NuSA-CL is stronger. |
| CLIP as Online CL (G9Ea7mlqGO) | 3.80 | R1 | VLM CL; had lack-of-insight concerns. NuSA-CL has stronger ablations. |
| Rehearsal-Free VLM CL (9aZ2ixiYGd) | 5.00 | R1 | Prompt-based VLM CL with mixed reviews. NuSA-CL has a more novel method. |
| LwF for VLMs (k9NYnsC4Mq) | 5.67 | R1 | VLM CL; rejected. NuSA-CL has more convincing empirical validation. |
| C-CLIP (sb7qHFYwBc) | 6.50 | R1 | Most comparable — uses LoRA for CLIP CL, **Accept**. NuSA-CL has a more novel method and stronger ablations. |
| TiC-CLIP (TLADT8Wrhn) | 6.25 | R1 | CLIP CL benchmark paper, **Accept**. Different contribution type (benchmarks). |
| Spectral Regularization (Hcb2cgPbMg) | 6.25 | R1 | Spectral/SVD-based CL regularizer, **Accept**. Different approach (regularization vs. constraint). |
| Scalable LM CL (mz8owj4DXu) | 6.50 | R1 | LLM CL, **Accept**. Different domain (language models), similar scope of contribution. |

**Round 1 bracket:** 6.0 – 7.5. The paper is most comparable to C-CLIP (6.5) and TiC-CLIP (6.25), both accepted. NuSA-CL offers a more novel method than C-CLIP with comparably solid evaluation. Final score anchored at 7.0 — a solid accept with minor, addressable weaknesses.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>