Now I have all the information I need. Let me write the final consolidated review.

---

## Summary

This paper proposes **VQ-Transplant**, a framework that replaces the VQ module of a pretrained visual tokenizer (e.g., VAR) while keeping the encoder-decoder frozen, followed by lightweight decoder adaptation (5 epochs on ImageNet-1k). The paper also introduces **MMD-VQ**, a VQ method using Maximum Mean Discrepancy for distribution alignment. Experiments show that VQ-Transplant can match or exceed the original VAR tokenizer's reconstruction fidelity (0.81 r-FID vs 0.92) at substantially lower compute cost (44 vs 960 GPU-hours). The core idea — decoupling VQ method development from expensive full-model retraining — is practically useful and the experiments are reasonably thorough.

## Strengths

- **Clean, well-motivated framework that addresses a real bottleneck.** The two-stage design (VQ substitution followed by lightweight decoder adaptation) is clearly described. The decoder mismatch problem is convincingly documented: Table 3 shows that even with *lower* quantization error after substitution, reconstruction metrics are *worse* than the original tokenizer, and the 5-epoch decoder adaptation cleanly recovers and exceeds the original performance. This validates the claimed mechanism directly.

- **Comprehensive experimental validation across diverse settings.** The paper evaluates five VQ algorithms (Vanilla, EMA, Online, Wasserstein, MMD) in both multi-scale and fixed-scale configurations, on ImageNet-1k and three cross-dataset benchmarks (FFHQ, CelebA-HQ, LSUN-Churches). The adaptation epoch analysis (Tables 4, 5) showing monotonic r-FID improvement from 0.91→0.79 (K=4096) and 0.81→0.74 (K=8192) over 20 epochs provides fine-grained evidence for the framework's behavior.

- **Cross-dataset generalization is demonstrated.** On FFHQ (Table 8), Wasserstein VQ via VQ-Transplant achieves r-FID 1.21 at K=32768, substantially outperforming full-training baselines like VQGAN-LC (3.81) which trains on FFHQ directly. This shows the framework's practical utility beyond the adaptation distribution.

- **Controlled multi-scale comparisons are provided.** Table 3 compares MMD VAR (K=4096, 680 tokens) against the original VAR (K=4096, 680 tokens) at matched token count and codebook size — a fair head-to-head where MMD VAR achieves 0.91 vs 0.92 r-FID.

## Weaknesses

### Major

- **MMD-VQ's claimed advantage over Wasserstein VQ is unsupported, and the stated motivation is contradicted by the data.** The paper motivates MMD-VQ (Section 2) as overcoming Wasserstein VQ's Gaussian assumption, arguing it should help when features deviate from Gaussianity (e.g., cross-dataset settings). However, on cross-dataset tasks where non-Gaussian distributions would most plausibly arise, Wasserstein VQ consistently matches or beats MMD VQ: FFHQ K=32768 (1.21 vs 1.37, Table 8), Churches K=16384 (1.79 vs 1.87, Table 10). The settings where MMD leads are on ImageNet — where features are likely closer to Gaussian since the encoder was designed for this data. On CelebA-HQ K=16384 (Table 9), MMD wins (2.60 vs 3.02), but this is one cross-dataset result out of several. Overall MMD-VQ and Wasserstein VQ are empirically competitive with neither clearly dominant, and the pattern directly undermines the paper's stated motivation. MMD-VQ should be honestly reframed as an alternative to Wasserstein VQ rather than an improvement.

- **The headline compute-savings claim (95% reduction, 21.8× speedup) conflates multiple confounds.** Table 1 compares VAR training (16×A100, 60 hours, OpenImages) against VQ-Transplant (2×A100, 22 hours, ImageNet-1k). The 21.8× factor simultaneously mixes differences in: (a) dataset (OpenImages vs ImageNet-1k — the paper notes ImageNet-1k is a subset of OpenImages), (b) GPU count (16 vs 2), and (c) training scope (full model vs partial decoder-only). Additionally, the "95% cost reduction" framing does not acknowledge the upfront cost (~960 GPU-hours) of the pretrained base tokenizer that VQ-Transplant depends on. The honest value proposition — that VQ-Transplant enables cheap iteration on VQ methods once a base tokenizer exists — is still a real contribution and should be presented with these caveats explicitly.

### Minor

- **Baseline comparisons in Table 2 are not controlled for token count.** Most cited baselines use 256 tokens while MMD VQ uses 512 tokens (and up to K=65,536 codebook size). RQVAE with 512 tokens achieves 2.69 r-FID vs MMD VQ's 1.05 — the margin is large enough that the conclusion likely holds, but the paper would benefit from controlled comparisons at matched token counts. (The multi-scale VAR comparisons in Table 3 use the same 680 tokens and are properly controlled.)

- **The from-scratch comparison (Table 6) adds little value.** It compares VQ-Transplant (22h) against from-scratch MMD VAR training for 5-7 epochs (25-35h), which the paper itself acknowledges produces "relatively poor" results and notes that "discrete tokenizers typically require hundreds of epochs." Since both sides agree that <10 epochs of from-scratch training is insufficient, this comparison does not provide useful evidence for the framework's advantage. It should either be replaced with a properly trained from-scratch baseline or removed.

### Trivial

- The "Speedup" column in Table 1 could be misinterpreted: it shows each baseline's speedup *relative to VQ-Transplant*, but the row ordering and lack of explicit labeling may confuse readers.

## Nice-to-Haves

- An analysis of the computational overhead of MMD computation (O(NK) per batch) versus Wasserstein VQ would help practitioners assess the practical trade-off.
- Inference cost analysis: larger codebooks (up to 65,536) may increase inference latency or memory; this is relevant for the claimed practical utility.
- An ablation of the GAN loss during decoder adaptation (with vs. without) would clarify how much of the quality gain comes from the framework vs. adversarial training tricks inherited from prior work.

## Removed Points

These points from the reviews were removed with justification:

- **Harsh Critic's claim that MMD-VQ "does not empirically outperform Wasserstein VQ" using CelebA-HQ as evidence that Wasserstein wins:** **Removed — factually incorrect.** In Table 9 (CelebA-HQ, K=16384), MMD VQ achieves r-FID **2.60** vs Wasserstein VQ's **3.02** — MMD wins. The Harsh Critic also cited a non-existent "CelebA-HQ K=32768" row that does not appear in the paper (the K=32768 results shown under that critic's table are from FFHQ, Table 8, where Wasserstein does win). The corrected picture is that MMD and Wasserstein are competitive overall, with neither dominant.

- **Harsh Critic's classification of the cost-comparison issue as a "Structural" fatal flaw:** **Demoted to Major.** While the compute comparison is imprecise, the qualitative conclusion that VQ-Transplant is substantially cheaper than full retraining is almost certainly correct and not invalidated by the imprecision.

- **Strength Finder's "Systematic controlled comparison against from-scratch training":** **Removed.** The Table 6 comparison trains from-scratch for only 5-7 epochs, which the paper itself acknowledges is insufficient — making this a weak baseline that does not constitute a "systematic controlled comparison."

- **Harsh Critic's claim that the paper is missing from-scratch training for "hundreds of epochs":** **Removed — scope creep.** The paper's contribution is efficient VQ iteration, not beating full-training SOTA on a compute budget; running a hundreds-of-epoch from-scratch baseline would defeat the purpose.

- **Strength Finder's generic strength about the problem being important:** **Removed — generic/superficial,** not tied to specific content in the paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe MMD-VQ honestly.** Either: (a) show a concrete setting where MMD's nonparametric nature yields measurable gains over Wasserstein VQ, ideally on data with demonstrably non-Gaussian features; or (b) reframe MMD-VQ as a competitive alternative to Wasserstein VQ rather than an improvement, and remove the claim that it overcomes Wasserstein VQ's limitation.

2. **Revise the compute comparison.** Acknowledge the upfront cost of the base tokenizer. If possible, provide a controlled comparison on the same dataset with matched hardware (e.g., estimate what VAR would cost on ImageNet-1k with 2 GPUs, or show what VQ-Transplant would cost on OpenImages).

3. **Remove or replace Table 6.** The from-scratch comparison at 5-7 epochs is not informative.

4. **Add controlled token-count ablations** for the fixed-scale comparisons in Table 2, or at minimum note the token-count difference explicitly when making claims about beating baselines.

---

## Score and Decision

### Calibration Round 1 — Bracketing

The calibration tool was unavailable due to infrastructure issues (missing files in the calibration corpus). I instead rely on my own comparative judgment calibrated against ICLR reviewing standards.

**Bracket assessment:** This paper sits in the 5.0–7.0 range. It has a genuine, well-executed technical contribution (VQ-Transplant) with thorough experiments. However, the presentation overclaims on both the compute savings (mixing confounds) and MMD-VQ's advantages (contradicted by the data pattern). These are not fatal — the core framework is solid and the qualitative findings hold — but they lower the paper from a what would otherwise be a clear accept.

The strongest comparable contribution is the general idea of decoupling components in trained systems to enable cheap iteration — which is a proven recipe for practical impact. The weaknesses are in framing, not in technical soundness. This places the paper clearly above "reject" territory (where papers have unsalvageable methodology) but below the top tier (where claims are precisely supported by evidence).

**Final calibration:** The paper's primary contribution is solid and well-supported. The main weaknesses are overclaiming in the compute comparison and the unsupported MMD-VQ motivation. These are addressable with honest reframing. This corresponds to a **borderline accept** — the paper should be accepted conditional on the authors fixing the framing issues.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>