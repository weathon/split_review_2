## Summary
# Final Review Report

## Summary

This paper presents PRISM (Precision Restoration with Interpretable Separation of Mixtures), a conditional diffusion framework for compound image restoration in scientific and environmental domains. The core technical contribution is a two-stage approach: (1) fine-tuning a CLIP image encoder with a weighted contrastive disentanglement objective that explicitly models compositional structure among mixed degradations, and (2) using this encoder to condition a latent diffusion backbone (Stable Diffusion v1.5) for joint restoration of overlapping distortions. The framework supports both automated full restoration and expert-guided selective restoration through natural language prompts.

The paper addresses an important practical problem: scientific imagery often suffers from compound degradations (e.g., haze + blur + low light) that existing single-distortion or sequential methods handle poorly. The authors argue convincingly that scientific restoration requires simultaneous correction, precision over aesthetics, and controllability. Three contributions are claimed: (C1) a principled embedding design with structured compositional latent space for compound degradations, (C2) a novel scientific utility benchmark across four domains including a new Rooftop Cityscapes dataset, and (C3) a systematic study demonstrating that selective controllability improves downstream scientific accuracy.

The experimental evaluation spans a synthetic Mixed Degradations Benchmark (MDB) with up to four simultaneous distortions, zero-shot generalization to three unseen real-world domains (underwater, under-display camera, fluid lensing), and downstream task utility across remote sensing, camera traps, microscopy, and urban scenes. PRISM achieves competitive or state-of-the-art results across most metrics, and the controllability analysis (Table 3) provides compelling evidence that selective restoration can outperform full restoration in three of four scientific tasks.

Overall, this is a methodologically sound and well-motivated paper with a clear practical contribution. The main weaknesses are: reliance on synthetic degradations that may not capture real distortion physics, limited evidence for the claimed latent space compositionality beyond correlational metrics, missing statistical rigor in key comparisons, and some overreach in generalization claims that would require external literature verification (deferred due to retrieval constraints in this review). The paper would benefit from stronger causal evidence linking the contrastive objective to observed controllability, additional real-distortion validation, and tighter claim bounding.

## Strengths
**1. Well-motivated and practically relevant problem formulation.** The paper identifies a genuine gap in existing image restoration pipelines: scientific and environmental imagery rarely suffers from a single degradation type, yet most methods handle distortions sequentially or independently. The three guiding principles (simultaneous over sequential correction, precision over aesthetics, control over automation) provide a clear and convincing motivation that aligns the technical design with real-world scientific workflows.

**2. Clean and principled two-stage method design.** The contrastive disentanglement stage (Stage 1) is conceptually elegant. Using weighted Jaccard-based contrastive loss to organize the CLIP embedding space so that compound distortions lie near the span of their primitives is a sensible approach. The quality-aware regularizer $\mathcal{L}_{\text{qual}}$ that penalizes distortion evidence in clean embeddings addresses an important practical issue (degradation hallucination). The separation into encoder fine-tuning and diffusion conditioning is a clear architectural decomposition.

**3. Strong empirical results on compound restoration.** Table 1 shows PRISM achieving PSNR=22.08, SSIM=0.842, and LPIPS=0.218 on the MDB, outperforming eight baselines across all-core metrics by non-trivial margins (e.g., +1.24 PSNR over the next best, MPerceiver at 20.84). The scale-up experiment (Fig. 3) convincingly demonstrates that compound-aware training degrades more gracefully as distortion count increases (ΔPSNR 8.14 vs 11.12+ for baselines from 1 to 4 distortions).

**4. Compelling controllability analysis.** Table 3 is one of the paper's strongest assets. It moves beyond pixel-level metrics to downstream task performance and provides statistical evidence (p<0.05 for three of four domains) that selective restoration outperforms full restoration. The microscopy example (Fig. 6) concretely illustrates the trade-off: super-resolution improves segmentation mIoU (0.569) while denoising would erase faint structures. The fluorescence vs. segmentation tension in Table 4 further reinforces the task-dependence argument.

**5. Broad and relevant evaluation scope.** The paper evaluates across microscopy, wildlife monitoring, remote sensing, and urban domains using both synthetic and real datasets. The zero-shot experiments on UIEB, POLED, and ThapaSet (Table 2) extend beyond standard benchmarks and demonstrate practical generalization. The downstream utility framework using off-the-shelf models is a conservative and realistic design choice.

**6. Honest limitation discussion.** The paper explicitly acknowledges key limitations: dependence on synthetic augmentations, the need for finer-grained controllability (intensity and spatial extent), and computational cost. This transparency strengthens credibility.

## Weaknesses
### W1. Synthetic-to-real gap and limited real-distortion validation (Major)

The paper trains exclusively on synthetic degradations applied to clean images from diverse datasets (Sec. 3.1). While this is a common practical choice, the realism of the distortion library is not rigorously validated. The degradation pipeline (geometric warping, blur, photometric shifts, weather effects) uses random parameters and orders that may not reflect the physical coupling of real distortions. For example, underwater image formation involves wavelength-dependent attenuation and backscattering that interact non-linearly — composing independent augmentations (e.g., "add haze" then "add color shift") is a coarse approximation.

The zero-shot results on UIEB, POLED, and ThapaSet (Table 2) are intended to address this, but the evaluation protocol introduces its own concern: the authors use the compound-aware CLIP encoder to *identify* distortion types present in each dataset, then apply manual prompts over a *standardized set* across all models. This creates an advantage for PRISM, which has a fine-tuned encoder tailored to the same distortion vocabulary. A fairer zero-shot evaluation would use identical prompts derived independently of PRISM's encoder. Furthermore, UIEB predictions were "more variable" (Sec. 4.2), indicating the encoder's classifications may be unreliable. Without external literature comparison (deferred due to retrieval constraints), the claimed "state-of-the-art" zero-shot results should be treated as provisional.

**Recommendation:** (a) Add a real-distortion paired dataset (e.g., real hazy/clean pairs, real low-light/long-exposure pairs) to directly validate on non-synthetic distortions. (b) Disclose the prompt derivation procedure for baselines and ensure identical prompts are used. (c) Tone down "state-of-the-art" to "competitive with current methods" until external verification is completed.

---

### W2. Weak causal evidence linking contrastive loss to controllability (Major)

The central claim is that the weighted contrastive disentanglement objective (Eq. 1-3) creates a compositional latent geometry that "enables" selective and predictable restoration. However, the evidence for this causal chain is indirect:

- Fig. 4 shows that compound-aware CLIP achieves higher PSNR for both sequential and composite prompting, and reduces the gap between them. This is correlational: the observed improvement could come from better compound-aware supervision (more training data diversity) rather than the geometric structure of the latent space.
- Appendix Fig. 13 (mentioned but not available in the reviewed excerpt) shows embedding visualizations, but t-SNE/UMAP projections can be misleading and do not constitute a quantitative test of compositionality.
- There is no controlled experiment where the contrastive weight $w_{jk}$ is ablated (e.g., replaced with uniform weighting) to isolate its effect from the compound-aware supervision and the quality regularizer.

Without such an ablation, the claimed "principled embedding design" is supported only by end-to-end metric improvements that may be driven by other factors (e.g., the compound-aware training data itself, the SCPM module, or the diffusion backbone capacity).

**Recommendation:** Add an ablation study comparing the full method vs. a variant with $w_{jk}=1$ (uniform contrastive weighting) vs. a variant without the contrastive loss entirely. Report PSNR, SSIM, and a quantitative compositionality metric (e.g., linear interpolation accuracy in latent space). This is essential to substantiate the core methodological claim.

---

### W3. Missing statistical rigor in primary comparisons (Moderate)

Several key comparisons lack proper variance reporting or significance testing:

- **Table 1 (MDB results):** No standard deviations or confidence intervals are reported. Several method differences are small (e.g., PRISM FID=48.97 vs MPerceiver FID=48.18 — PRISM is *worse* on FID than the second-best method, though this is not discussed). Without variance estimates, readers cannot assess whether the observed ranking is stable.
- **Table 2 (Zero-shot):** Same issue — no variance reported. The LPIPS gap on POLED is tiny (PRISM 0.419 vs AutoDIR 0.431), and on ThapaSet PRISM's SSIM is 0.487 vs AutoDIR's 0.462. Without confidence intervals, the "state-of-the-art" claim across all metrics is not fully supported.
- **Table 3 (Downstream utility):** This table does report mean±std over 3 seeds, which is commendable. However, the p-values appear to come from pairwise tests not fully described (e.g., which specific comparison was tested? Full vs. Selective?). The remote sensing result (p=0.11, n.s.) is correctly labeled as not significant.

**Recommendation:** Run all main tables (1, 2) with at least 3 seeds and report mean±std. For Table 1, explicitly note that PRISM is second-best on FID and discuss why. Add Bonferroni correction or equivalent for multiple comparisons in Table 3.

---

### W4. Missing details on key design choices and reproducibility (Moderate)

Several critical implementation details are deferred to the appendix (not available in the reviewed excerpt), making independent assessment difficult:

- The distortion library composition, parameter ranges, and sampling strategy are needed to understand dataset bias (mentioned in Appendix E, Table 9).
- The SCPM architecture, which likely contributes to the perceptual quality gains, is described only as "lightweight decoder-side refinement block" (Sec. 3.2) with details deferred to Appendix E and Fig. 12.
- The automated distortion prediction MLP (Sec. 3.3) is mentioned but its architecture, training data (how are ground-truth distortion labels obtained for real images?), and accuracy are not discussed.
- The prompt generation process using GPT-4 may introduce systematic biases in language coverage. The number of distinct prompts, their distribution across distortion types, and validation of prompt quality are not reported.
- Computational requirements (training hours, GPU memory) are deferred to Appendix A, making it hard to judge practical feasibility from the main text.

**Recommendation:** (a) Move at least the distortion library summary and SCPM architecture description to the main paper. (b) Report automated MLP accuracy on the distortion classification task. (c) Include a brief prompt validation statistic (e.g., human evaluation of prompt accuracy on a random subset). (d) Provide a short compute summary in the main text.

---

### W5. Limited evaluation of the "selective restoration" interface (Moderate)

While the paper argues strongly for controllability, the actual selective restoration capability is not thoroughly evaluated:

- The only quantitative evaluation of selective restoration is the downstream task analysis (Table 3), which compares "full" vs. "selective" but does not measure how accurately the model follows prompts. For example, if a user asks to "remove haze but keep blur," does the model actually preserve blur faithfully? This is not tested.
- Prompt faithfulness itself is not measured (e.g., via a distortion classifier before/after selective restoration).
- The qualitative examples (Figs. 5, 6) are illustrative but do not provide a systematic evaluation across prompt types.

**Recommendation:** Add a prompt-faithfulness metric: for each selective prompt, apply a distortion classifier to the restored image and measure whether the specified distortions are reduced while unspecified distortions remain. Report per-distortion accuracy and a misgeneralization rate (e.g., unintended distortion removal).

---

### W6. Overclaiming in the conclusion and abstract (Minor)

Several statements over-extend the available evidence:

- Abstract: "PRISM outperforms state-of-the-art baselines on complex compound degradations" — this is supported for PSNR/SSIM/LPIPS on MDB, but FID is second-best and zero-shot results lack variance estimates.
- Sec. 5: "strong generalization beyond curated training sets" — the zero-shot results are on three specific datasets with encoder-based prompt selection, which may not generalize to all unseen domains.
- Sec. 5: "evaluations on real composite degradations confirm generalization beyond our synthetic training pipeline" — the evaluation protocol itself depends on PRISM's encoder for prompt selection, creating a potential circularity.

**Recommendation:** Replace "state-of-the-art" with "competitive with or superior to existing methods on evaluated benchmarks." Replace "strong generalization" with "promising zero-shot results on three unseen domains, which should be confirmed with standardized evaluation protocols."

---

### W7. Novelty claims require external verification (Deferred)

Due to retrieval constraints in this review run, external literature comparison is not available. The paper's claims about the novelty of the compositional latent space, the contrastive weighting scheme, and the controllability framework cannot be independently verified against prior work. Key questions that remain open: (a) How does the weighted contrastive objective differ from existing compositional contrastive learning methods (e.g., those in disentangled representation learning)? (b) Are there prior works that already achieve selective restoration through conditional diffusion without explicit latent disentanglement? (c) How does the MDB benchmark compare to CDD-11 and other existing multi-distortion benchmarks beyond the claim that it "extends beyond" them?

**Deferred Action:** The authors should include a detailed comparison table with relevant prior methods on compositional contrastive learning, selective restoration, and compound-degradation benchmarks. This verification is marked as deferred and should be addressed before final publication.

## Score
**Final Score: 7/10**

**Rationale:** This score reflects the paper's solid methodological contribution and strong empirical evaluation, tempered by several evidence gaps that limit full confidence in the core claims.

The paper addresses a genuinely important problem (compound restoration with controllability) with a clean two-stage design. The empirical results on the MDB benchmark are strong and the downstream utility analysis (Table 3) provides compelling evidence for the practical value of selective restoration. The evaluation scope across four scientific domains is ambitious and largely well-executed.

However, the score is constrained by the following factors:

- **Research value and novelty (primary dimension):** The core idea (contrastive disentanglement for compositional restoration) is conceptually novel, but the causal evidence linking the weighted contrastive loss to the claimed compositional geometry is weak. The observed gains could be explained by other factors (compound-aware data diversity, backbone capacity). The novelty claims cannot be independently verified against prior work due to retrieval constraints in this review (deferred).

- **Validity and soundness:** The main experiments are appropriately designed, but the lack of variance reporting in Tables 1 and 2, the missing ablation isolating the contrastive weighting mechanism, and the potential circularity in the zero-shot evaluation protocol reduce confidence. The synthetic-to-real gap is acknowledged but not adequately addressed with real-distortion validation.

- **Reproducibility:** Critical architectural details (SCPM, distortion library, prompt generation) are deferred to the appendix. While this is common, the main text should provide enough information for independent implementation assessment.

- **Strength of claims:** The paper uses "state-of-the-art" language that is not fully supported by the evidence (e.g., second-best on FID, no variance estimates). The generalization claims need tighter bounding.

The paper is clearly above the acceptance threshold for a good venue, and the identified weaknesses are addressable with reasonable additional experiments and revised wording. A post-revision target of 8/10 is achievable if the authors add the suggested ablation, variance reporting, and real-distortion validation.