## Summary

This paper proposes SigMap, a wireless localization foundation model combining two core innovations: (1) a cycle-adaptive masking strategy for self-supervised pre-training that detects periodic structure in CSI signals and generates masks that disrupt shortcut learning, and (2) a "map-as-prompt" framework that encodes 3D building geometry via a GNN into lightweight soft prompts injected into a frozen Transformer backbone. The model is evaluated on simulated ray-tracing datasets (DeepMIMO, WAIR-D) for single- and multi-BS localization, demonstrating improvements over OMP, CNN, SWiT, and LWLM baselines while updating only ~0.7% of parameters during fine-tuning.

---

## Strengths

1. **Cycle-adaptive masking is a genuine domain-motivated contribution (Section 3.3).** The observation that wireless CSI has inherent periodic structure, and that standard masked autoencoding can exploit this as a shortcut rather than learning meaningful representations, is a specific and well-reasoned insight. The proposed fix—detecting periodicity via cross-correlation and generating mask patterns that disrupt it—is a principled response grounded in signal characteristics. This is the paper's most novel contribution.

2. **The map-as-prompt framework is a sensible architectural design (Section 3.4).** Encoding 3D building geometry through a GCN and injecting the result as soft prompts into a frozen Transformer backbone is well-motivated for a problem where environmental geometry directly affects signal propagation and maps change across deployment scenarios. The design choice to keep the backbone frozen aligns with the paper's stated goal of parameter-efficient cross-scenario adaptation.

3. **Parameter efficiency is convincingly demonstrated (Section 4.6, Table 5).** Fine-tuning only 0.085M parameters (0.7% of total, 30 minutes for 1000 epochs) while achieving competitive accuracy is a genuine practical advantage for real deployment, especially given that 3D maps vary across environments and full fine-tuning is expensive.

4. **Generalization experiments on WAIR-D and DeepMIMO O2 provide evidence beyond a single in-distribution setting (Section 4.5).** Testing on 100 real-world city scenes from WAIR-D gives some indication of cross-domain robustness, and the improvements over LWLM (53.2% on O2, 44.3% on WAIR-D) are notable even with only one comparison baseline.

---

## Weaknesses

### Fatal
None.

### Major

1. **Missing the most relevant SSL-based baselines, undermining the SOTA claim.** The introduction (Section 1) discusses CrowdBERT (Han et al., 2024), signal-guided masked autoencoders (Wang et al., 2025), LWM (Alikhani et al., 2024), and WirelessGPT (Yang et al., 2025) as prior works whose limitations the paper aims to address. Yet none of these appear in any comparison table (Tables 1–2, Section 4.2). The baselines used are OMP (a classical method), a generic CNN, SWiT, and LWLM. The paper's core claim of "state-of-the-art performance" (abstract, Section 1.2, conclusion) cannot be evaluated when the most directly relevant SSL-based localization competitors are absent from head-to-head comparison. This is the most significant weakness in the paper.

2. **The NLoS-aware attention mechanism (Eq. 11, Section 4.2) has no architectural precedent in the methodology.** Equation 11 is introduced as "the key advantage" for NLoS scenarios but uses variables (`o_s^{(i)}`, `W_NLoS`, `φ`) that are never defined in the methodology section (Section 3). Sections 3.1–3.5 describe a standard Transformer backbone, cycle-adaptive masking, geographic prompt tuning, and a task-specific fusion head (Eq. 9–10)—but nothing matching this NLoS-attention component. It is unclear whether Eq. 11 describes an actual architectural component omitted from the method write-up or a post-hoc interpretive lens. A reader cannot determine the model's full architecture from the paper as written.

### Minor

3. **"Zero-shot generalization" claim conflicts with the actual experimental protocol.** The abstract and Section 1.2 claim "strong zero-shot generalization in unseen environments." However, Section 4.5 explicitly describes the setup as "few-shot" — only the downstream task heads are fine-tuned using approximately 100 labeled target samples per scenario. Zero-shot implies no gradient updates on the target domain; the paper evaluates few-shot transfer with a frozen backbone. The results are still meaningful, but the terminology should be corrected to "few-shot cross-scenario generalization" to match what is actually evaluated.

4. **No variance reported despite 5 independent runs.** Section 4.1 states "All results are averaged over 5 independent runs," yet every table reports only point estimates without standard deviations, confidence intervals, or error bars. This is problematic because some claimed improvements are modest (e.g., Table 2: multi-BS MAE of 0.673 vs. 0.789 for the w/o-map variant, a ~15% gap). Without variance estimates, the reader cannot assess whether the reported improvements are statistically significant or within run-to-run noise.

5. **Ablation results in Table 3 contain a discrepancy that is not discussed.** Strip-masking achieves better RMSE (0.972) than the proposed adaptive masking (1.099), yet the paper concludes that adaptive masking "yields the best trade-off" without explaining why RMSE degrades under the adaptive strategy. Since RMSE penalizes large errors more heavily than MAE, this could indicate that adaptive masking introduces occasional large outliers. The paper should address this directly rather than glossing over it.

6. **The periodicity detection step is underspecified.** Equation 6 defines the mask pattern using parameters `d_final`, `j_0`, and `w`, but the paper provides no equation or algorithm explaining how these are computed from the cross-correlation analysis. The text states that "shift patterns" are computed "using cross-correlation analysis" (Section 3.3) but does not specify whether this is done per-sample or per-dataset, on amplitude or phase, or how the dominant periodicity is extracted. This limits reproducibility of the core methodological contribution.

7. **Main results (Tables 1–2) are on a single scenario of one simulated dataset (DeepMIMO O1_3p5).** While the generalization experiments (Section 4.5) add DeepMIMO O2 and WAIR-D, those use a different setup (few-shot, only LWLM as baseline). The central "state-of-the-art" claim rests primarily on one synthetic urban environment. Broader evaluation across more datasets or scenarios in the main comparison would strengthen the contribution.

8. **No model size comparison with baselines.** Table 5 reports SigMap's parameter counts but provides no comparable numbers for LWLM, SWiT, or CNN. Without this, it is unclear whether SigMap's advantage comes from being a larger model or from better architectural design and pretraining.

9. **The claimed "interpretability" benefit is not supported.** Section 1.2 lists interpretability as a benefit of the geographic prompt mechanism, but the paper provides no visualization, probing, or analysis of what the learned prompt tokens capture. Even a simple attention-weight analysis or t-SNE visualization would substantiate this claim.

### Trivial
None.

---

## Nice-to-Haves

- Including confidence intervals or standard deviations would substantially strengthen the quantitative comparisons at negligible cost (the authors already run 5 trials).
- Adding CrowdBERT or signal-guided MAE to even one comparison table would directly substantiate the paper's narrative of surpassing prior SSL-based localization work.
- A visualization or probing analysis of the learned geographic prompt tokens would support the interpretability claim.

---

## Removed Points

These points were raised in the input review but are removed because they do not meet the verification criteria:

- **"The 2D bird's-eye map obtains most of the benefit, undermining the emphasis on 3D geometry."** — The paper already discusses this finding honestly (Section 4.4: "most of the topological benefit is retained even without vertical detail") and proposes a future direction based on it. The paper is reporting a result, not making a false claim; this is a finding, not a weakness.
- **"No appendix content" / missing proofs in appendix** — The parser strips appendix content from all papers; these existed in the original submission.
- **"The paper's central SOTA claim rests on one synthetic urban environment" — already merged into weakness #7 above** (this is kept but downgraded to Minor; the paper does have generalization results on O2 and WAIR-D, so the criticism of complete reliance on one dataset is partially addressed).

---

## Novel Insights

None beyond the paper's own contributions. The two reviews converge on the same core assessment: the technical ideas (cycle-adaptive masking and map-as-prompt tuning) are genuinely novel and well-motivated, but the evaluation is incomplete relative to the strength of the claims made. The key insight from review integration is that the paper's strongest contribution (cycle-adaptive masking as a domain-specific SSL strategy) is actually the least well-documented aspect (the periodicity detection algorithm is underspecified), while the most thoroughly evaluated aspect (parameter efficiency) is also the least novel. Closing this gap by fully specifying the periodicity detection and adding the missing SSL baselines would significantly strengthen the paper.

---

## Suggestions

1. **Add the most relevant SSL-based baselines** (CrowdBERT, signal-guided MAE, or their equivalents) to the main comparison tables. This is the single most impactful fix for substantiating the SOTA claim.
2. **Integrate the NLoS-aware attention mechanism** (Eq. 11) into Section 3's methodology, or explicitly state that Eq. 11 is a post-hoc interpretive analysis rather than an architectural component.
3. **Correct the "zero-shot" language** to "few-shot cross-scenario generalization" throughout the abstract and contributions section to match the experimental protocol.
4. **Add standard deviations or confidence intervals** to all tables where 5-run averages are reported.
5. **Specify the periodicity detection algorithm** — describe how `d_final`, `j_0`, and `w` are computed from cross-correlation, including whether detection is per-sample or per-dataset and which signal domain (amplitude, phase, complex) is used.

---

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>