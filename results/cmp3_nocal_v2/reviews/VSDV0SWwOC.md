## Summary

LS-Merge proposes shifting model merging from weight space to a learned latent manifold. It uses a transformer-based VAE to encode LLM weights, performs merging (interpolation) in the latent space, and decodes back to weights. For heterogeneous architectures, it adds an Optimal Transport alignment step. The paper shows that (a) LLM weights are heavy-tailed and low-rank, motivating non-linear encoders; (b) latent-space expert merging (LoRA) outperforms weight-space baselines (Table 3); and (c) PCA collapses under compression while the VAE preserves functionality (Table 8).

---

## Strengths

1. **Novel conceptual framing.** Shifting merging from weight space to a learned latent manifold is a genuine departure from the existing literature (Model Soup, Task Arithmetic, DARE, etc.). The motivation — that a latent space can enable cross-architecture merging by mapping disparate weight structures into a common representation — is well-articulated (Section 1, Figure 1).

2. **Weight statistics analysis (Section 3.1, Table 1, Figure 2) is informative.** The observation that LLM weights exhibit high kurtosis (heavy tails) and low-rank structure directly informs the encoder design and is clearly presented. This is the strongest part of the paper's motivation.

3. **Strong LoRA-expert merging results.** In Table 3, LS-Merge (soup) achieves the best results on 5/8 benchmarks and LS-Merge (lerp) on 2/8, outperforming Uniform Soup, Greedy Soup, SLERP, and DARE-Ties. The advantage is attributed to sampling multiple latent codes per expert before merging, which is a plausible mechanism.

4. **PCA vs. VAE ablation (Table 8) is compelling.** The finding that PCA collapses at all compression ratios (MMLU drops to ~25% even at r=1.6) while the VAE preserves near-original accuracy cleanly demonstrates that linear methods are insufficient for weight manifold reconstruction. This validates the non-linear encoder choice.

---

## Weaknesses

### Fatal
None.

### Major

1. **The evidence for heterogeneous merging — the paper's headline contribution — is weak.** This is the setting that distinguishes LS-Merge from all prior work, yet the experimental support is thin:
   - **Cross-family results (Table 5)** show tiny improvements over the base model: +0.92 on WinoGrande, +0.56 on ARC-C, +1.03 on HellaSwag — well within evaluation noise for these benchmarks. More concerningly, OT alignment *alone* (without interpolation) *destroys* performance (e.g., WinoGrande 56.83 → 51.13, ARC-C 42.78 → 34.25), yet this degradation is not discussed. The recovery from interpolation is small and does not convincingly demonstrate that the framework "works" for cross-family merging.
   - **No heterogeneous baselines are compared against.** The paper only compares against self-constructed baselines (parameter/latent mixing without alignment) that are guaranteed to fail. Even simple baselines like "use the target model alone" or "train a small LoRA adapter on the target using source knowledge" would establish a meaningful bar.
   - **Intra-family results (Figure 4a) are shown only as bar charts with no numerical values reported.** Quantitative numbers should be in tables.
   - **The 1:1 layer-pairing assumption (Algorithm 1)** — pairing source and target layers by index, using min(|L_src|, |L_tgt|) — is not validated. Different model families (LLaMA vs. Gemma) may organize computation very differently across depth, yet the paper provides no analysis of whether paired latents actually correspond to similar functionality.

2. **No perplexity or direct language modeling evaluation.** The entire evaluation relies on downstream task benchmarks (MMLU, HellaSwag, etc.). The paper never reports perplexity or any direct measure of whether the VAE preserves the model's core language modeling capability. This is a significant gap because: (a) downstream benchmarks can be noisy and may not capture fundamental degradation; (b) for a method that compresses and reconstructs weights, reporting perplexity is standard practice in the weight-space learning literature; (c) the compression-ratio ablation (Tables 7–8) evaluates task accuracy but not language modeling fidelity, making it impossible to distinguish between "the VAE preserves the model" and "the benchmarks happen to be robust to mild weight corruption."

### Minor

3. **Suspicious standard deviations in Table 2.** Several entries report standard deviations of exactly 0.00 (e.g., LS-Merge on Gemma-3-4b-it: MMLU 54.20 ± 0.00, HellaSwag 50.10 ± 0.00), while VAE entries with the same number of decimal places show non-zero variance. The method samples multiple latent codes from the posterior, which should introduce variance. A reported std of 0.00 is either a misleading rounding artifact or reflects single-run reporting without multiple seeds. Either way, it undermines confidence.

4. **Computational cost is unreported despite a "scalable" claim.** The abstract and conclusion claim LS-Merge is "scalable," but no information is provided about GPU hours for VAE training, VAE parameter count, encoding/decoding latency, or memory requirements. Training a transformer VAE on the weights of billion-parameter models is non-trivial; without cost analysis, the scalability claim is unsupported.

5. **Two different evaluation pipelines used without cross-validation.** The main experiments use one evaluation codebase, while cross-family evaluation (Section 4.4) and ablations (Section 5) switch to *lm-eval*, stated as due to "some issues with llama model when using the previous evaluation code" (line 228). This makes results across experiments hard to compare and suggests technical reliability issues that are not discussed further.

6. **"Data Merge †" baseline (Table 3) is never explained.** The dagger symbol appears on this baseline row but no footnote is provided in the extracted paper, and the surrounding text does not define it. Readers cannot interpret this baseline's meaning.

7. **VAE training data composition is underspecified.** The paper states training data "consist of pretrained weight snapshots for Gemma-3-1B-it and Gemma-3-4B-it" (line 153) — how many snapshots? From what training stages? Single run or multiple runs? For the LoRA experiments (Table 3), it is unclear whether the VAE was trained on the specific LoRA weights or on base-model weights.

8. **No ablation of the two-stage curriculum.** The paper's key training stabilization technique (Section 3.2) first trains a deterministic autoencoder (KL off), then enables the KL term. This is never ablated: would a deterministic AE suffice? Does the KL regularization contribute meaningfully, or is the benefit entirely from the first stage? Since the entire method hinges on learning a structured latent space, ablating this choice is important.

9. **Table 1 presentation of kurtosis is confusing.** Per-layer rows show kurtosis values of 5–15 (e.g., llama3-2-3b-it self_attn: 8.40, 7.34, 6.22, 5.45), while the `avg` row reports 1.43 for the same block. The caption mentions these are "representative layers" (the early, high-kurtosis ones), but the large gap between displayed individual values and the average is jarring and the explanation is easy to miss. A clearer note or a full-layer plot would help.

### Trivial
None.

---

## Nice-to-Haves

- Ablate the KL regularization (deterministic AE vs. VAE) to validate the two-stage curriculum.
- Report perplexity at all compression ratios as a direct measure of language-modeling preservation.
- Provide compute cost estimates (GPU hours, VAE parameter count, wall-clock encoding time) to support the scalability claim.
- Validate the 1:1 layer-pairing assumption for heterogeneous merging (e.g., by computing feature similarity or functional correspondence between paired layers).
- Report exact numerical values for Figure 4 (intra-family heterogeneous merging).

---

## Removed Points

*(These points appeared in the input review but are removed per filtering rules. Treat with caution.)*

- **"The core idea is genuinely novel" (strength)**: Retained as Strength 1.
- **"The OT alignment formulation is principled" (strength)**: Retained as Strength 2.
- **"The weight statistics analysis is the strongest part" (strength)**: Retained as Strength 3.
- **"Missing comparison to AutoModel or weight-space VAEs from the literature"** (weakness from input review): Removed. This asks the authors to compare against methods whose applicability to LLM weights is speculative from the reviewer's end. The paper already benchmarks against the relevant weight-space merging methods.
- **"The paper does not discuss the weight-space learning literature in enough depth" / "missing related work"** (weakness from input review): Removed per hard rule: "DO NOT mention missing related works, as you do not have external sources to confirm their existence."
- **"Chunk size c not justified" / "optional token downsampling never explained"** (from input section-by-section): These are implementation details that could be stated in the (stripped) appendix. Demoted from the review as the parser strips appendices.
- **"The ≈4% claim does not match the numbers"** (from input review): Upon verification, the claim approximately holds for the 4B model vs. base (MMLU +2.07%, HellaSwag +5.70%, GSM8k +7.69% → average ~4%). The claim is loose but not false; removed as the criticism is exaggerated relative to the actual numbers.
- **"The Gaussian assumption for OT contradicts the heavy-tailed finding"** (from input review): The OT Gaussian assumption applies to the *latents* (after VAE encoding with a Gaussian prior), not the raw weights. The tension is weaker than stated. Removed.
- **"The self-merging claim of single-model augmentation is overclaimed"** (from input review): The paper reports results for this setting (Table 2), and the improvements, while modest, are present. The strength of the claim matches the evidence presented.
- **"PCA implementation not described"** (from input review): This is sufficiently standard; a linear baseline comparison is adequate for the ablation's purpose.

---

## Novel Insights

The most useful insight from the reviews is that LS-Merge's core methodological contribution (latent-space merging) and its strongest experimental support (expert merging, Table 3; PCA vs. VAE, Table 8) are somewhat decoupled from its most attention-grabbing claim (heterogeneous merging). The paper would benefit from recalibrating its claims to match the evidence — the heterogeneous results as presented do not yet convincingly demonstrate the claimed capability, while the homogeneous/expert results are considerably stronger. There is no novel insight beyond what the paper's own framing and results suggest.

---

## Suggestions

1. **Strengthen the heterogeneous merging section** by: (a) adding simple baselines (target model alone, a small LoRA adapter baseline); (b) reporting exact numbers for intra-family experiments instead of bar charts only; (c) analyzing whether the 1:1 layer pairing is functionally sensible; and (d) discussing why OT alignment alone degrades performance so severely.
2. **Report perplexity** for VAE-reconstructed models at all compression ratios.
3. **Clarify the statistical reporting** in Table 2 — report the number of seeds and explain near-zero standard deviations.
4. **Add a compute cost table** (GPU hours, VAE size, encoding time) to support the scalability claim.
5. **Ablate the two-stage curriculum** to validate whether KL regularization actually helps.
6. **Define the "Data Merge †" baseline** and clarify VAE training data composition.

---

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>