Now I have enough to write the draft review.Now I have enough to write the final review.

---

## Summary
VQ-Transplant proposes a two-stage framework to enable plug-and-play integration of new VQ modules into frozen, pre-trained visual tokenizers: first substituting the VQ module (Stage I) and then performing lightweight decoder adaptation to resolve distributional mismatch (Stage II). The paper also introduces MMD-VQ, a non-parametric distribution-alignment VQ method using maximum mean discrepancy. Evaluated on the pre-trained VAR tokenizer, the framework is tested with five VQ algorithms across multi-scale and fixed-scale configurations, and on four datasets.

---

## Strengths

- **Concrete problem framing**: Table 1's cost breakdown demonstrates the computational barrier to VQ research, and the two-stage decomposition—freeze the expensive encoder/decoder, substitute the cheap VQ component, patch the distributional mismatch—is logically sound and reusable by the community.

- **Comprehensive VQ sweep**: Tables 3 and 7 systematically compare five distinct VQ algorithms in both multi-scale and fixed-scale configurations across multiple codebook sizes and both stages. The consistent pattern—distribution-alignment methods outperform vanilla/EMA/Online across all settings—is a credible, informative finding that stands independent of the efficiency framing.

- **Decoder-VQ mismatch insight (Section 5.1)**: The observation that lower quantization error after VQ substitution *does not* immediately translate to better r-FID—because the frozen decoder is conditioned on the original quantization space—is the paper's most analytically interesting finding and directly motivates the necessity of Stage II.

- **Transparent adaptation analysis (Tables 4–5, Figure 3)**: Tracking r-FID per epoch through 20 epochs and reporting the full trajectory, including continued improvement past the headline "5 epochs," is presented openly rather than obscured.

---

## Weaknesses

### Fatal
None.

### Major

- **Structurally misleading efficiency claim (Table 1, abstract, Section 4.1)**: The paper claims "reducing the training cost by 95%" and a 21.8× speedup. VQ-Transplant's reported 22 GPU-hours (2×A100) covers *only* the decoder adaptation stage. It entirely omits the cost of the pre-trained VAR tokenizer it borrows: 16×A100 × 60 hours = 960 GPU-hours, trained on OpenImages. The total compute consumed before VQ-Transplant can produce any result is ≈982 GPU-hours—more than the VAR baseline itself. The 21.8× speedup column in Table 1 divides other models' full training costs by VQ-Transplant's adaptation-only cost, an incoherent comparison. The legitimate claim—*given an existing pre-trained tokenizer, marginal cost per new VQ experiment is 22 GPU-hours vs. 960*—is both accurate and compelling, but it is not what the paper currently states. This affects every efficiency claim in the paper and is not a minor presentation issue.

- **Cross-dataset comparisons conflate encoder/decoder pretraining advantage with the transplant mechanism (Section 5.3, Tables 8–10)**: VQ-Transplant uses a VAR encoder/decoder pre-trained on OpenImages—a massive, diverse dataset that subsumes the face and scene domains tested. Baselines such as VQGAN-LC (r-FID 3.81 on FFHQ) were trained on far less data. Claiming state-of-the-art reconstruction (r-FID 1.21 on FFHQ) while the encoder/decoder already carries strong priors over these domains conflates the transplant mechanism's contribution with the base model's pretraining data advantage. The paper does briefly acknowledge this context (Section 5.3 notes "the original VAR tokenizer was trained on OpenImages—where ImageNet-1k is a subset") but does not disclose it as a potential confound for the cross-dataset comparison.

### Minor

- **"5-epoch" headline vs. 20-epoch results (abstract, Tables 4–5, Figure 3)**: The abstract frames "only 5 epochs" as the core efficiency claim, but Table 5 shows clear and consistent r-FID improvement from 5 epochs (0.91/0.81) to 20 epochs (0.79/0.74). The paper lacks a principled stopping criterion, and the gap is non-trivial. The authors should either adopt a defensible stopping rule or qualify the 5-epoch figure as a "reasonable early checkpoint" rather than the standard recommendation.

- **Non-Gaussianity motivation for MMD-VQ is unverified (Section 4.2)**: The paper motivates MMD over Wasserstein VQ by claiming real feature distributions are non-Gaussian, making Wasserstein's alignment (which reduces to matching first- and second-order moments under Gaussianity) insufficient. This is plausible but not empirically verified—no histogram, kurtosis test, or distributional visualization is provided. Furthermore, the empirical improvement of MMD over Wasserstein is thin: Table 3 (K=4096, adaptation) MMD VAR r-FID 0.91 vs. Wasserstein 0.93; Table 7 (K=65536, adaptation) MMD VQ 0.86 vs. Wasserstein 0.92. The advantage exists but is modest and does not strongly validate the theoretical motivation.

### Trivial
None.

---

## Nice-to-Haves

- Restate the efficiency claim explicitly as *marginal* cost given an existing pre-trained tokenizer: "A researcher who already has access to a pre-trained VAR tokenizer can trial a new VQ algorithm in 22 GPU-hours instead of 960." This is actually a stronger framing because it is accurate and practically actionable.
- For cross-dataset experiments, either compare against baselines that use a similarly large-scale pre-trained encoder/decoder, or explicitly scope the claim as: "zero-shot cross-domain generalization of the transplanted VQ module, given a strong OpenImages-pre-trained backbone."
- Empirical visualization (e.g., histogram or kurtosis measurement) of VAR encoder feature distributions to substantiate the non-Gaussian motivation for MMD-VQ.
- An ablation on a weaker base tokenizer would bound the method's sensitivity to base model quality—a practical concern for researchers who cannot access industry-level models.

---

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Table 6 "from-scratch" comparison critique**: The critic argues this fails to prove VQ-Transplant is faster for the same total compute. However, the paper explicitly acknowledges this limitation ("discrete tokenizers typically require hundreds of epochs to achieve high-quality visual reconstruction when trained from scratch") and frames Table 6 as showing qualitative superiority at matched training time, not total-compute equivalence. The paper's intent is clear and the table is appropriately labeled. Removed as a strawman weakness.

- **Generic request for more baselines / larger datasets**: The reviewer's implied concern about evaluation breadth is not anchored to a specific missing comparison that would change the paper's conclusions. Removed as noise.

---

## Novel Insights
The most useful analytical observation—that substituting a better VQ module (with lower quantization error) into a frozen tokenizer *worsens* reconstruction fidelity relative to the original because the decoder is conditioned on the original quantization space, not the new one—is underemphasized in the paper. This "decoder-VQ mismatch" phenomenon is a genuinely useful finding for practitioners designing modular tokenizer systems: quantization quality and reconstruction quality are decoupled when the decoder is frozen, and no amount of VQ improvement in Stage I can substitute for decoder re-alignment.

---

## Suggestions

1. **Reframe the efficiency contribution accurately**: Distinguish "marginal cost per VQ experiment given a pre-trained tokenizer" (22 GPU-hours, genuinely cheap) from "total training cost reduction" (which does not exist). Add a single sentence to Table 1's caption and the abstract.
2. **Cross-dataset disclosure**: Add an explicit caveat in Section 5.3 that the encoder/decoder was pre-trained on OpenImages, which subsumes the test domains, and that cross-dataset gains reflect both the transplant mechanism and the base model's generalization capacity.
3. **Epoch recommendation**: Commit to either 5 or 10 epochs as the recommended default with a validation-based justification, or provide a clear compute/performance trade-off table.
4. **Empirical non-Gaussianity check**: Add a brief distributional analysis of encoder features to ground the MMD-VQ motivation.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Human Score | Round | Comparison |
|---|---|---|---|
| nS2DBNydCC.md (Wasserstein VQ) | 4.75 | R1 | Closest domain match—single new VQ method without framework; this paper adds a transplant framework and is more comprehensive |
| sfTsvy05MX.md (LL-VQ-VAE) | 4.75 | R1 | Similar scope, single VQ method, narrower experiments |
| YlWvQSBCgl.md (Channel-wise Quantization) | 4.00 | R1 | Narrower contribution, weaker baselines |
| mLxxv5gts0.md (Gaussian Mixture VQ) | 3.80 | R1 | Narrower, weaker empirical support |
| yGnsH3gQ6U.md (Binary Spherical Quantization) | 5.75 | R1 | Accepted; similar scope—new VQ method + strong experiments, cleaner efficiency claim |
| 0Nui91LBQS.md (SEED Tokenizer/LLaMA SEE) | 6.33 | R1 | Accepted; broader scope, downstream generation integration |
| 3TnLGGHhNx.md (BPE Visual Tokens) | 6.00 | R1 | Accepted; richer theoretical grounding, cleaner claims |
| WNLAkjUm19.md (Discrete Tokenization SSL) | 7.00 | R1 | Higher bar—theoretical + empirical, well-scoped |
| IqGVIU4rvM.md (VQ-VAE + Diffusion) | 2.50 | R1 | Weaker contribution, less grounded |
| qPTFzmXVLd.md (Language of Visual Tokens) | 5.50 | R2 | Borderline—analytical but limited contributions |
| tNxr38vfYR.md (Victor token compression) | 5.00 | R2 | Borderline reject; useful but limited scope |

**Round 1 bracket**: The paper sits between the VQ method anchors at 4.75 (Wasserstein VQ, LL-VQ-VAE—rejected) and the accepted visual tokenizer papers at 5.75–6.33. The transplant *framework* is broader than just proposing a new VQ algorithm, which pushes it above the 4.75 anchors. However, the major misleading efficiency claim and inflated cross-dataset comparisons would weigh significantly against acceptance, pulling it below the 6.0+ accepted papers. Initial bracket: **4.5–6.0**.

**Narrowing**: The BSQ paper (5.75, accepted) offers a clean comparison—it proposes a new VQ scheme with strong experiments and accurate claims. VQ-Transplant has a comparable or broader experimental sweep, but its central efficiency framing is materially misleading in a way the BSQ paper is not. The Wasserstein VQ paper (4.75, rejected) is a close domain match; VQ-Transplant adds the framework abstraction and more thorough experiments but carries significant framing problems. Settling on **5.0**: the core contribution is real and the experimental work is solid, but the misrepresentation of the efficiency claim is a significant concern that would prevent acceptance without substantial revision.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>