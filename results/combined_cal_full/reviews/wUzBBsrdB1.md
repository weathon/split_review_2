Now I'll produce the final consolidated review.

## Summary

This paper studies how the L0 sparsity hyperparameter in Sparse Autoencoders (SAEs) affects feature quality. Using toy models with known ground-truth features, it demonstrates that when L0 is set too low, SAEs resort to "feature hedging" — mixing correlated features together to improve MSE reconstruction — even as the resulting latents become polysemantic and do not correspond to the true underlying features. The paper also shows that sparsity-reconstruction tradeoff plots are misleading in this regime: a ground-truth SAE can score *worse* on reconstruction than a corrupted one. The authors propose a decoder pairwise cosine similarity metric ($c_{\text{dec}}$) for detecting incorrect L0, and validate their findings with LLM SAEs trained on Gemma-2-2b and Llama-3.2-1b.

## Strengths

- **The toy model finding (Section 3.1–3.3) is crisp, non-obvious, and important.** The demonstration that when the SAE's L0 is set below the true L0 of the data-generating process, the MSE loss actively rewards mixing correlated features into latents — and that a ground-truth SAE with correct features scores *worse* on reconstruction than a corrupted one (MSE 4.88 vs. 2.73) — is a sharp result that should change how practitioners think about L0. This is the paper's strongest contribution.

- **The critique of sparsity–reconstruction tradeoff plots (Section 3.4, Figure 4) is conceptually valuable.** Showing that a ground-truth SAE can be dominated on variance explained by a feature-mixing SAE at the same L0 is a clean counterexample to the implicit assumption that better reconstruction implies better features. This is well-supported by the toy model evidence.

- **The $c_{\text{dec}}$ metric (Section 3.5) is intuitive and well-motivated.** In the toy model, it has a clear minimum at the true L0 (Figure 6, with standard deviation across 5 seeds), and the theoretical intuition — that feature mixing inflates pairwise similarities between decoder latents — is sound. The metric is simple enough to be immediately useful for detecting L0 values that are clearly too low.

- **The JumpReLU "sticking" observation (Section 3.6, Figure 7)** — that a wide range of sparsity coefficients produces SAEs near the correct L0 — is an interesting empirical finding that sheds light on why JumpReLU SAEs may be more robust than BatchTopK SAEs in the high-L0 regime.

## Weaknesses

### Major

- **The Abstract overclaims the LLM validation, creating a mismatch with the evidence.** The Abstract states "our method finds the correct L0" as a definitive finding, but the LLM results are substantially messier. For Gemma-2-2b layer 5 (Figure 8), $c_{\text{dec}}$ drops sharply then remains nearly flat from L0≈250 to 2000, and the paper resorts to identifying the correct L0 by the qualitative "elbow" rather than the global minimum. For Gemma-2-2b layer 12 (Figure 9), BatchTopK and JumpReLU SAEs give different $c_{\text{dec}}$ minima (≈200 vs. 250–300). The Discussion appropriately tempers this ("we do not view this as a perfect guide"), but the Abstract and Introduction do not reflect this caution. This mismatch undermines reader trust.

- **The claim that "most commonly used SAEs have an L0 that is too low" (Abstract) goes beyond what the experiments directly support.** The paper's LLM experiments cover only 2 models (Gemma-2-2b, Llama-3.2-1b) and 2–3 layers. Even if Appendix A.13 (removed by parser) shows that L0<100 is common, the paper has not established what the correct L0 should be for those models and layers. The paper's own results suggest correct L0 is ~200 for the layers tested, but generalizing this to "most commonly used SAEs" is an inference that the current evidence does not support.

- **The validation chain for "correct features" in LLMs is indirect.** In toy models, the paper can check whether SAE latents match ground-truth features directly via cosine similarity. In LLMs, this is impossible, so the paper validates against sparse probing performance. But sparse probing is itself a proxy — it measures how well a linear probe predicts a label from SAE latent activations. The paper does not establish that peak sparse probing performance *means* that the SAE has learned correct, monosemantic features rather than just getting better at the probing task for other reasons. The connection from "peak sparse probing" → "correct L0" → "correct features" involves unvalidated steps.

### Minor

- **The $c_{\text{dec}}$ "elbow" identification in LLM experiments is qualitative and post-hoc.** The paper identifies the correct L0 as "the elbow just before $c_{\text{dec}}$ jumps due to low L0," but this is a visual heuristic rather than a defined quantitative criterion. Providing a precise rule (e.g., "the L0 at which $c_{\text{dec}}$ exceeds its minimum by X%") would strengthen the practical utility.

- **Sparse probing F1 differences in the LLM experiments are small** (range ~0.04 in Figure 8), and the paper does not report whether these differences are statistically significant across seeds. The paper uses 3 seeds per L0 but does not quantify uncertainty in the probing results.

- **Only 2 LLMs and 2–3 layers are tested.** While this is a reasonable start, it is a narrow basis for the broad claims made. Validation on at least one more diverse model family (e.g., a Pythia or Mistral model) and additional layers would substantially strengthen the paper.

- **The toy model experiments use limited correlation structures.** Section 3.1 uses a single simple pattern (all features correlated with $f_0$). Section 3.2 uses a single randomly-generated correlation matrix without testing across multiple random seeds for the correlation structure. The MSE comparison (2.73 vs. 4.88) in Section 3.3 is presented without error bars over multiple runs.

- **No discussion of computational cost.** Sweeping L0 to find the $c_{\text{dec}}$ minimum requires training multiple SAEs — for a single LLM layer with 32k latents at 500M tokens each, this is expensive. The paper should acknowledge this practical barrier.

### Trivial

None.

## Nice-to-Haves

- A direct comparison between $c_{\text{dec}}$ and alternative L0 selection methods (e.g., MDL SAEs from Ayonrinde et al. 2024) would strengthen the practical utility claims.
- Clarifying whether $c_{\text{dec}}$ is computed on the trained BatchTopK decoder or the converted JumpReLU decoder, and whether the conversion step affects the metric.
- A quantitative rule for using $c_{\text{dec}}$ in practice (e.g., "the L0 at which $c_{\text{dec}}$ drops below 1.5× its minimum value") would turn it from a qualitative heuristic into a usable method.

## Removed Points

These points are from the input review and were removed with justification:

- **"Sparsity-reconstruction critique is misdirected"** — REMOVED (strawman). The paper's critique is well-supported: at L0 below true L0, a worse SAE (with mixed features) gets better reconstruction than a ground-truth SAE. This challenges using such plots even for architecture comparison at the same L0, which is what the critic claims researchers do.

- **"Absolute cosine similarity discards sign information"** — REMOVED. The critic acknowledges this is fine for the metric's purpose.

- **"Section 4.2 discussion is speculative"** — REMOVED. The paper clearly frames this as speculation, which is appropriate for an exploratory section.

- **"The toy model's orthogonal-feature assumption may not transfer"** — REMOVED (subsumed by the validation chain weakness above; the paper acknowledges the LRH assumption and the Discussion notes the metric is imperfect).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Revise the Abstract and Introduction** to match the Discussion's measured tone. Replace "our method finds the correct L0" with something like "our method identifies a plausible L0 range that coarsely tracks downstream task performance." Hedge the "most SAEs have too low L0" claim.

2. **Provide a quantitative criterion** for the $c_{\text{dec}}$ elbow, evaluated across multiple layers and models.

3. **Add error bars or statistical significance** for the sparse probing F1 differences in Figure 8.

4. **Acknowledge the computational cost** of the L0 sweep method, and discuss potential mitigations (e.g., whether the sweep can be done with fewer tokens or coarser granularity).

5. **Add at least one more model family** (e.g., a Pythia or Mistral model) and 2–3 additional layers to broaden the LLM validation.

---

## Calibration

**Round 1 bracket:** 6.0–7.5

**Anchors used:**

| File | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| LC2KxRwC3n.md ("A is for Absorption") | 7.50 | 2 | Yes | Very similar topic (SAE feature absorption/failure modes), similar methodology (toy + LLM), similar limitation about single model/task. My paper's strongest weakness (-5.42 for narrow LLM scope) maps to this paper's weakness (-3.20). The absorption paper scored higher, but my paper has more severe overclaiming in its front matter. My paper sits slightly below. |
| 9ca9eHNrdH.md ("Canonical Units") | 7.00 | 1 | Yes | Critiques SAE assumptions with novel diagnostics; similar weight magnitudes. My paper has comparable strength-to-weakness balance (+5.24 vs -5.42) but the overclaiming issue pushes it below. |
| 1Njl73JKjB.md ("Principled Evaluations") | 7.00 | 1 | Yes | SAE evaluation framework, limited task scope. A similar-caliber paper. |
| OeHSkJ58TG.md ("Incidental Polysemanticity") | 5.67 | 2 | Yes | Toy model analysis of polysemanticity with limited real-world validation. Weaker than my paper because its core claims connect less directly to LLM practice. |
| tcsZt9ZNKD.md ("Scaling SAEs") | 8.20 | 1 | Yes | Stronger novelty (TopK SAE, scaling laws) and broader evaluation. My paper is not at this level. |

**Final score:** 6.5. The paper has a genuinely important toy-model contribution that the community needs, but the Abstract overclaims significantly and the LLM validation is narrower and messier than the framing suggests. These issues are fixable with revisions, bringing the paper closer to the 7.0–7.5 range of similar SAE-critique papers.

---

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>