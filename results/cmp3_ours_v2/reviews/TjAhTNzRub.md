Now I have sufficient context. Let me write the final consolidated review.

## Summary

MoRE proposes a training-free framework for feature-level machine unlearning that uses prototype-orthogonal (PO) projection to decorrelate forget and remain prototypes before erasing/remapping, then scatters forget features across multiple remain prototypes via a mixture-of-experts architecture. The method achieves strong Knowledge Retention (KR) results—driving forget-class linear-probe accuracy to near-random levels—while requiring only a single forward pass and lightweight linear algebra.

## Strengths

- **Principled solution to a real limitation of ESC.** The observation that forget and remain prototypes have cosine similarity ~0.5 and that naive erasure damages both is well-supported (Fig. 3). The PO projection via pseudoinverse is mathematically clean, and the ablation (Table 3) confirms PO is essential for preserving remain utility. This is a genuine improvement over ESC's approach of simply pruning SVD directions.

- **Impressive KR results demonstrating genuine feature-level unlearning.** Under the KR metric (linear probe on frozen features), MoRE reduces forget accuracy to near-random levels (CIFAR-10: D_f=9.01, D_ft=8.93), substantially outperforming Retrain (D_f=72.62) and ESC (D_f=99.01). This is the strongest empirical result and represents a clear advance over prior work.

- **Training-free and computationally efficient.** Prototypes are activation means collected in one forward pass; all subsequent operations are linear algebra. MoRE completes unlearning in under 10 seconds with <200 MB GPU memory on CIFAR-10/100 (Fig. 5), a meaningful practical advantage over training-based methods.

## Weaknesses

### Major

- **Central "irreversible" claim is not supported by the evidence presented.** The word appears in the title, abstract, and throughout the text (lines 9, 65, 82, 88, 106, 120, 180, 253, 255, 364). Yet irreversibility is evaluated against only one form of recovery: linear probing (KR metric). The paper itself criticizes ESC for being "vulnerable to recovery through light fine-tuning" (lines 58, 106) and claims MoRE "significantly impedes the recovery of forgotten knowledge through fine-tuning or linear probing" (line 82). However, MoRE is never tested against fine-tuning recovery—not even fine-tuning just the classification head on forget data, which is the precise attack used to motivate the problem. Without this evaluation, the paper's strongest and most distinctive claim ("irreversible") is structurally unsupported. The authors should either (a) test against fine-tuning recovery and other adversarial probes, or (b) replace "irreversible" with language matching the evidence (e.g., "strong resistance to linear probing recovery").

### Minor

- **MoRE's multi-expert advantage over single-expert remapping is limited to KR metrics.** In standard (non-KR) evaluation, Remap (single expert) and MoRE (multi-expert) achieve nearly identical results (CIFAR-10 HM: 99.94 vs 99.93; CIFAR-100: 99.99 vs 99.98; Tiny-ImageNet: 98.04 vs 98.03). MoRE's advantage is real and significant in KR (CIFAR-100 HM_f: 51.88→0.07; Tiny-ImageNet HM_f: 55.18→0.50), which is the metric most relevant to irreversibility, but the paper should be transparent that the MoE architecture's contribution is primarily visible in this specific evaluation regime.

- **Diffusion results are modest and the qualitative claim is overstated.** In Table 2, MoRE's LPIPS_f scores (0.33 for both Van Gogh and Kelly McKernan) are mid-range; methods like UCE (0.25, 0.25) achieve higher LPIPS_f (better forgetting). MoRE wins on the composite LPIPS_d metric (best tradeoff), which is valid but less direct. The qualitative claim "ours is the only method that successfully removes Van Gogh's iconic artistic style" (line 280) is a visual judgment that cannot be verified from the quantitative data alone, and "only" is too strong given that UCE and RECE achieve higher LPIPS_f.

- **Random data forgetting results are incomplete.** Table 4 reports results only for "Remap" (single expert), not for "MoRE" (multi-expert), yet the text claims "MoRE achieves comparable or superior performance" (line 360).

- **Abstract claims "exact" feature-level unlearning** (line 9) but no formal guarantee of exactness is provided. This term is misleading for a method that provides empirical rather than certified unlearning.

- **KR evaluation uses a single learning rate (lr=0.1)** (lines 196, 210, 223). A sensitivity analysis over probe learning rates would strengthen the results, as probe recovery could be lr-dependent.

- **Condition number of the prototype matrix P is not reported** despite the paper acknowledging that pseudoinverse via SVD is used to avoid squaring the condition number (line 146). For larger concept sets (CIFAR-100: 100 classes; Tiny-ImageNet: 200 classes), ill-conditioning could amplify artifacts.

### Trivial

- Table 1 layout is dense (14+ columns per dataset block) and hard to parse.
- Several entries in Table 1 show single values without reported standard deviation despite the caption stating "mean ± std."

## Nice-to-Haves

- Ablate the complement-space projection term (Eq. 4 vs. Eq. 3) to quantify whether the "skip connection" matters.
- Test non-linear probes (e.g., 2-layer MLP) as additional recovery attacks.
- Report the condition number of P across datasets and discuss handling of near-singular cases.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Figure 7's x-axis labeled 'number of experts' ranging from 0.2 to 0.8 makes no sense"** — This is a parser artifact from the figure axis. The paper text (line 352) correctly discusses number of experts as a discrete count.
- **"Notation is inconsistent between Eq. 3-6"** — The paper's derivation is correct: Eq. 5 simplifies Eq. 4 (which includes the complement term), not Eq. 3. The text directly follows Eq. 4 with "Above expression can be simplified to," so the connection is clear.
- **"Complement-space projection is described as a 'skip connection' but is actually a projection onto the nullspace of P^T"** — Both descriptions are compatible; calling it "akin to a skip connection" is a reasonable pedagogical analogy and does not affect correctness.
- **"Stochastic router may not provide the scattering benefits claimed"** — Table 6 shows stochastic routing performs competitively with trained variants, and the paper explicitly acknowledges trained routers sometimes yield higher HM.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add fine-tuning recovery experiments (full-model and head-only) on forget data to substantiate the irreversibility claim, or retire the term.
2. Report MoRE (multi-expert) results in the random data forgetting table (Table 4).
3. Include a sensitivity analysis of probe learning rates for the KR metric.
4. Report condition numbers of P for each dataset to address potential numerical concerns.
5. Rephrase "exact" to something like "effective" or "empirically strong" in the abstract.

## Calibration Anchors

**Round 1 bracket:** 4.5–6.5

**Anchors retrieved:**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| SUN: Training-free MU via Subspace | 4.00 | R1 | Similar topic (training-free subspace unlearning). MoRE has more principled method (PO projection + remapping), better evaluation (KR metric, more baselines), and stronger results. Clearly above SUN. |
| Deep Unlearning: Fast Training-free | 5.25 | R1 | Similar topic. MoRE is comparable in methodological rigor with better evaluation (KR metric, diffusion models) but has the central overclaiming issue on "irreversibility." |
| Unlearning via Sparse Representations | 5.25 | R1 | Model-specific (DKVB bottleneck). MoRE is more general and better evaluated, but both have the issue of partial evidence for their claims. |
| NegMerge: Consensual Weight Negation | 6.00 | R1 | Different approach (weight negation), all scores 6. MoRE has stronger novelty but a larger claim-evidence gap. |
| Pseudo-Probability Unlearning | 3.00 | R1 | Lower-quality unlearning paper. MoRE is significantly stronger. |
| UGradSL | 3.00 | R1 | Lower-quality unlearning paper. MoRE is stronger. |
| MASIMU | 2.50 | R1 | Lower-quality unlearning paper. MoRE is much stronger. |
| Forget Vectors at Play | 4.80 | R1 | Input-perturbation approach. MoRE has better method and evaluation. |

**Narrowing:** The paper is clearly above SUN (4.00) and the 2.5–3.0 papers but below NegMerge (6.00, all scores 6). The key discriminator is that the central "irreversible" claim—in the title and throughout the paper—is supported only by linear probing evidence while the paper itself motivates the problem with fine-tuning attacks. This gap prevents the paper from reaching the 6+ level. Final score anchored between Deep Unlearning (5.25) and NegMerge (6.00), accounting for the stronger technical contribution discounted by the overclaiming.

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>