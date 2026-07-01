Now let me produce the final consolidated review.

## Summary

This paper proposes SigMap, a multimodal foundation model for wireless localization under NLoS conditions. The approach has two main components: (1) a cycle-adaptive masking strategy that detects periodicity in CSI and generates masks that prevent shortcut learning, and (2) a "map-as-prompt" framework that encodes 3D building meshes via a GNN and injects the result as soft prompts into a frozen transformer backbone. Experiments on DeepMIMO and WAIR-D datasets show consistent improvements over baselines (e.g., 34.4% MAE reduction over LWLM in Single-BS localization) with parameter-efficient fine-tuning.

## Strengths

1. **Well-motivated problem framing.** The paper correctly identifies two genuine limitations in existing work: generic masking fails to account for CSI periodicity, and geographic information is used only superficially. The research gaps (Section 1.1) are clearly articulated.

2. **The map-as-prompt pipeline (Algorithm 1, Section 3.4) is a clean and well-described architectural contribution.** Encoding a 3D building mesh via graph convolution and injecting the result as a soft prompt into a frozen transformer is technically sound. The design is parameter-efficient: only 0.085M parameters are trainable during fine-tuning vs. 11.73M during pre-training (Table 5), and the generation algorithm is clearly specified with equations and pseudocode.

3. **The map modality ablation (Table 4) provides genuine diagnostic insight.** The result that a 2-D bird's-eye view (MAE 1.692) retains most of the benefit of a full 3-D mesh (MAE 1.564) is informative — it suggests topological and LoS cues drive the improvement, not height or facade normals. This is a useful finding for practitioners.

4. **Strong empirical results.** The method consistently outperforms baselines (OMP, CNN, SWiT, LWLM) across multiple settings, with substantial margins (34.4% MAE improvement in Single-BS, 18.7% in Multi-BS).

## Weaknesses

### Fatal
None.

### Major

1. **The "zero-shot" claim is contradicted by the paper's own experimental setup and must be corrected.** The abstract (line 9) and contributions list (line 43) both claim "strong zero-shot generalization in unseen environments." However, Section 4.5 (line 317) explicitly states: *"only the downstream task heads are fine-tuned using limited target samples (approximately 100 instances per scenario)."* This is few-shot fine-tuning, not zero-shot (which requires no gradient updates on target data). The generalization results may still be meaningful as few-shot transfer, but the paper characterizes its central capability incorrectly. The authors should replace "zero-shot" with "few-shot" or "limited-sample" throughout.

2. **The "NLoS-aware attention mechanism" — described as "the key advantage" — is introduced in the results section without proper definition.** In Section 4.2 (line 247), the paper states: *"The key advantage stems from our NLoS-aware attention mechanism that explicitly models multi-path propagation"* and presents Equation 11. The variables $\phi$, $\mathbf{o}_s$, and $\mathbf{W}_{\text{NLoS}}$ in this equation are never defined anywhere in the paper, and the mechanism is not referenced back to any component in the methodology (Sections 3.3–3.5). Section 3.5 describes a multi-BS fusion attention (Eq. 9) with different notation and functional form, but Eq. 11 appears to describe something different. A reader cannot determine what this mechanism actually is or how it relates to the described architecture. The paper should either properly introduce this mechanism in the methodology or clearly connect it to the multi-BS attention already described (Eq. 9) if they are the same.

3. **The core algorithmic contribution — cycle-adaptive masking — is under-specified to the point of irreproducibility.** Equation 6 defines the mask pattern in terms of $d_{\text{final}}$ ("the detected periodicity shift"). The paper says (line 133) *"we compute shift patterns using cross-correlation analysis"* but provides no procedure: what signals are cross-correlated, along which dimension, with what reference, and how is $d_{\text{final}}$ extracted from the correlation? The variable $d_{\text{final}}$ appears in Equation 6 but is never defined or computed anywhere else in the paper (confirmed via grep). Without this, the adaptive masking claim — the paper's first listed contribution — cannot be reproduced or evaluated.

### Minor

4. **Numerical inconsistency in the generalization results.** The text (line 340) reports SIGMAP achieving *"1.580 m on WAIR-D Scenario-2,"* but the corresponding table (lines 335–338) clearly shows an MAE of **1.880** for SIGMAP (w/ map) on WAIR-D. The value 1.580 does not appear in any row of that table. While this may be a typo, it damages confidence in numerical accuracy.

5. **No variance reporting for main results.** All results are averaged over 5 runs (line 239), but Tables 1–3 report only point estimates without standard deviations or confidence intervals. Error bars are mentioned only for the map modality ablation (line 301). Without variance, the reader cannot assess whether the reported improvements (e.g., 34.4% over LWLM) are statistically reliable.

6. **The masking ablation (Table 3) is presented without specifying the setting.** The MAE of 0.673 matches the Multi-BS results in Table 2, confirming it is the Multi-BS setting, but this is not stated in the table caption or text. Since cycle-adaptive masking is a core contribution, its effect should also be shown in the harder Single-BS setting where the benefit matters most.

7. **Narrow baseline comparison for the central claim.** The paper cites several localization-related SSL methods in related work (CrowdBERT, signal-guided masked autoencoders; lines 26–27) but does not compare against them experimentally. The paper offers a partial justification (these methods are "confined to specific configurations"), but stronger validation would include at least one of these as a baseline.

### Trivial
None.

## Nice-to-Haves

- **Empirical demonstration of the periodicity-shortcut failure mode.** The paper asserts that generic masking lets models exploit periodic shortcuts (Section 1.1) but provides no analysis of existing methods' failure modes. A simple diagnostic (e.g., showing that a standard MAE learns periodic interpolation rather than propagation physics) would strengthen the motivation.
- **Real-world CSI evaluation.** All experiments use simulated ray-tracing data (DeepMIMO, WAIR-D). The paper acknowledges this indirectly in future work, but even a small real-world validation would substantially strengthen practical deployability claims.
- **Clarify whether pre-training and fine-tuning share the same DeepMIMO O1_3p5 scenario.** Line 237 states both use O1_3p5. If pre-training and fine-tuning data come from the same simulated environment, the claim of learning "general-purpose" representations is weakened and should be discussed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Replace all instances of "zero-shot" with "few-shot" or "limited-sample generalization" to accurately describe the experimental protocol.
2. Either properly introduce the NLoS-aware attention mechanism in Section 3 (with defined variables and an architectural diagram) or remove Equation 11 and connect the results discussion to the already-described multi-BS attention (Eq. 9).
3. Specify the cross-correlation procedure for computing $d_{\text{final}}$ in Section 3.3 — even a few lines describing the input, dimension, reference signal, and extraction method would make the core contribution reproducible.
4. Add standard deviations or confidence intervals to all main result tables.
5. Correct the numerical inconsistency (1.580 → 1.880 or explain the discrepancy) in Section 4.5.

## Removed Points

These points were raised by reviewers but are removed from the main review for the reasons indicated:

- **"Transformer backbone architecture not specified in main text"** — The paper states (line 237) that detailed configuration is in Appendix B.3. Since the appendix is stripped by the parser, criticizing its absence is invalid per review guidelines.
- **"No evidence that existing SSL methods fail because of periodicity shortcuts"** — This is a motivation statement rather than an experimental claim. Most papers assert gaps without proving them; it is not a weakness of the proposed method.
- **"1000 epochs for fine-tuning seems very high"** — Speculative concern without evidence; the paper reports the total fine-tuning time is only 30 minutes, which is reasonable for 0.085M parameters.
- **"Cycle-adaptive masking ablation only shown for Multi-BS"** — Already included as Minor weakness #6; the removed "missing Single-BS" framing was redundant.

## Score and Decision

The paper addresses a real problem and proposes a reasonable two-part solution with strong empirical results. However, it has three verifiable major weaknesses: (1) a central claim of "zero-shot generalization" that is contradicted by the paper's own few-shot fine-tuning protocol, (2) the "NLoS-aware attention" mechanism claimed as the key advantage is introduced in the results section with undefined variables and no connection to the methodology, and (3) the core algorithmic contribution (cycle-adaptive masking) is under-specified to the point of irreproducibility. These issues are fixable but collectively prevent the paper from being acceptable in its current form.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>