## Summary

This paper introduces Purrception, which adapts Variational Flow Matching (VFM) to vector-quantized (VQ) latent spaces for image generation. The key idea is to learn a categorical posterior over codebook indices while computing the velocity field as a convex combination of continuous codebook embeddings. This hybrid formulation provides categorical supervision (cross-entropy loss) while preserving smooth, geometry-aware transport in the embedding space. On ImageNet-1k 256×256, Purrception demonstrates faster training convergence than both continuous and discrete flow matching baselines and enables inference-time temperature scaling — a unique capability not available in standard continuous or discrete flow models.

## Strengths

1. **Principled hybrid formulation (Section 3, Eqns. 12–14).** The paper correctly identifies a genuine tension in VQ-latent generative modeling — continuous methods preserve geometry but ignore categorical structure, discrete methods do the reverse — and resolves it through a mathematically clean adaptation of VFM. Equation (13) elegantly shows how a categorical posterior over codebook indices yields a continuous velocity field as an expectation over codebook embeddings. This is the paper's core intellectual contribution, and it is sound.

2. **Temperature control as a genuine, practical benefit (Section 4.2, Figure 4).** The hybrid formulation naturally produces logits, enabling inference-time temperature scaling — something neither continuous FM nor discrete FM can do in the same way. Figure 4 shows a clear U-shaped FID-vs-temperature curve, demonstrating that τ is a meaningful and controllable knob. This is a clean, well-documented advantage that follows directly from the method.

3. **Convergence speed advantage is well-documented (Figure 3).** The 2.3×–3.5× faster convergence to a given FID threshold is practically meaningful for training efficiency. The comparison against both CFM and CFM-endpoint (which controls for the velocity-vs-endpoint prediction distinction) is a reasonable experimental design.

## Weaknesses

### Fatal
None.

### Major

1. **SOTA claims are contradicted by the paper's own data (Section 4.3, Table 1, lines 195–201).** The paper claims Purrception shows "stronger performance against most autoregressive methods" and "firmly establishes Purrception as a novel, state-of-the-art approach, among VQ-based latent generative models." However, the paper's own Table 1 tells a different story:

   | Model | FID |
   |---|---|
   | ViT-VQGAN (autoregressive, VQ-based) | 3.04 |
   | LlamaGen-XL (autoregressive, VQ-based) | 3.39 |
   | RQTransformer (autoregressive, VQ-based) | **3.80** |
   | **Purception** (VQ-based) | **3.88** |
   | Open-MAGVIT2-L (masked, VQ-based) | 2.51 |

   Purception (FID 3.88) beats only VQGAN (5.20) among the four autoregressive methods listed. It loses to ViT-VQGAN (3.04), LlamaGen-XL (3.39), and RQTransformer (3.80). It also loses to Open-MAGVIT2-L (2.51), a masked generative model listed under the same table section. Claiming "stronger performance against most" methods when the model ranks near the bottom of its own comparison table is misleading. This is not a marginal embellishment — the SOTA framing appears in the Abstract, Introduction, and Section 4.3, and the claims do not survive contact with the reported data. The paper's genuine contributions (convergence speed, temperature control) do not depend on this framing, but the overclaiming undermines the reader's trust.

2. **Convergence speed advantage is partially confounded by the loss function difference (Section 4.1, lines 157–173).** The paper compares Purrception (cross-entropy loss over K logits) against CFM/CFM-endpoint (MSE loss over D-dimensional vectors). While CFM-endpoint controls for prediction target (endpoint prediction), the loss function itself differs — cross-entropy and MSE have different gradient properties and optimization landscapes. The paper attributes the faster convergence to "categorical supervision" specifically (line 173), but the comparison measures the combined effect of (a) switching to endpoint prediction and (b) using a discrete/categorical objective. Without an ablation that isolates the loss function (e.g., soft labels with MSE on the same prediction targets), the attribution is not fully supported. This weakens the causal claim but does not invalidate the observed speedup.

3. **No variance or error bars reported on convergence curves (Figure 3).** The FID-vs-iterations curves are presented as single trajectories with no indication of run-to-run variance, multiple seeds, or confidence intervals. FID-10k itself has Monte Carlo noise, so it is unclear whether the reported speedup factors (e.g., "3.5× faster") would hold across independent training runs. This is a meaningful omission for a paper whose strongest empirical claim is about convergence speed.

### Minor

1. **Temperature analysis focuses on FID but does not measure diversity.** The paper frames temperature as a "quality-diversity knob" (Section 3.1, line 109) but only evaluates FID. Showing that temperature trades off quality against diversity metrics (recall, coverage, or intra-FID) would directly substantiate this framing and make the experiment more complete.

2. **Differentiation from CDCD is not fully articulated (Related Work, lines 234–235).** The paper acknowledges the close relationship to Continuous Diffusion for Categorical Data (Dieleman et al., 2022) but dismisses it as "relying on continuous relaxations" and potentially diverging "from the true categorical structure." Since Purrception's softmax posterior is itself a continuous relaxation, the paper should clarify what specifically prevents CDCD's approach from preserving categorical structure that Purrception preserves — especially given that both methods use cross-entropy over token predictions with continuous embeddings.

### Trivial
None.

## Nice-to-Haves
- Add variance/error bars over multiple seeds for the convergence experiments.
- Provide diversity metrics (recall, coverage) for the temperature analysis to support the quality-diversity framing.
- Include an ablation comparing expected-endpoint inference vs. sampling from the categorical posterior.
- Since LlamaGen-XL (FID 3.39) uses the same tokenizer family (vq-ds8-c2i) and similar parameter count, a direct discussion of this comparison would strengthen the paper's positioning.

## Removed Points

These points were raised in the input review but removed or demoted for the following reasons:

- **CatFlow/CDCD similarity as a novelty concern** (Critical Issue 3 in input): The paper consistently describes itself as an "adaptation of VFM" (Abstract, Introduction, Section 3). This is honest positioning, not overclaimed novelty. The application of VFM/CatFlow to VQ image generation with a DiT backbone is a genuine engineering contribution. Removed because the paper does not claim fundamentally new methodology.
- **Missing appendix content**: The parser strips appendices from all papers; they exist in the original submission. Removed per instructions.
- **Name inconsistency (Purrception vs Purception)**: Classified as a formatting artifact/typo. Removed per instructions.
- **FID-10k vs FID-50k for convergence plots**: This is an acknowledged methodological choice, not a weakness. Removed.
- **Request for larger dataset / higher resolution validation**: Outside the paper's stated scope, which is ImageNet-1k 256×256. Removed per soft rule on scope creep.

## Novel Insights

None beyond the paper's own contributions. The input review's observations largely recapitulate what the paper itself claims (hybrid formulation bridges discrete and continuous, temperature control is useful, convergence is faster) or identify verification issues (SOTA claims not matching data). The most valuable meta-observation is that the paper's genuine strengths (convergence speed, temperature control) are independent of the overstated SOTA claims, and that the paper would be stronger if it reframed around those advantages rather than absolute FID ranking.

## Suggestions

1. **Reframe the contribution honestly.** Drop all SOTA language and claims of outperforming "most" autoregressive methods. Reposition Purrception as "a competitive VQ-based generative model with unique advantages in training efficiency and inference-time temperature controllability." This is a stronger, more defensible claim that aligns with the actual evidence.
2. **Add variance estimates** to the convergence experiments — even 2–3 seeds would substantially increase confidence in the speedup claims.
3. **Clarify the CDCD distinction** by explaining why a fixed pretrained codebook (Purrception) preserves categorical structure better than learned embeddings (CDCD) when both use softmax-based categorical supervision.
4. **Add diversity metrics** (recall or coverage) to the temperature analysis to directly support the "quality-diversity knob" framing.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>