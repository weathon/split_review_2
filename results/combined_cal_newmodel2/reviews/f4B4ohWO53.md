Now I have enough calibration data. Let me produce the final review.

## Summary

The paper proposes NVDP (Nonparametric Variational Differential Privacy), which integrates a Nonparametric Variational Information Bottleneck (NVIB) layer into the transformer architecture to inject calibrated noise into multi-vector embeddings. Privacy is measured via Rényi divergence (RD) between the resulting posterior distributions, with conversion to Bayesian Differential Privacy (BDP) values. The paper evaluates on GLUE tasks, showing NVDP outperforms a VIB-based ablation (VTDP) in the privacy-utility trade-off.

## Strengths

- **Novel and well-motivated idea.** Combining NVIB (a nonparametric information bottleneck for transformer attention layers) with Rényi divergence as a privacy measure is a genuinely novel synthesis. The paper correctly identifies that transformer embeddings consist of multiple vectors per token, making standard single-vector perturbation methods inapplicable, and proposes a nonparametric approach tailored to this setting.

- **Principled architectural design.** Removing the residual skip connection around the denoising multi-head attention (Section 3.1) to ensure no unsanitized information bypasses the stochastic bottleneck is a specific, defensible engineering decision directly motivated by the privacy goal.

- **Technically non-trivial derivation.** The Rényi divergence formula for the NVIB sampling procedure (Section 3.3, Equation 7) represents a genuine mathematical contribution. Adapting the Dirichlet Process formalism to produce a tractable, differentiable sampling procedure with a closed-form divergence expression is technically competent.

- **Empirical advantage over VIB baseline.** The results consistently show NVDP achieves a better privacy-utility trade-off than the VTDP ablation across several GLUE tasks, providing evidence that the nonparametric formulation offers practical advantages over a parametric VIB.

## Weaknesses

### Fatal

- **The paper's central claim — that it provides differential privacy guarantees — is unsupported by the methodology.** The title, abstract, and conclusion repeatedly claim "differential privacy," "strong privacy protection," and "privacy guarantees" (e.g., lines 9, 21, 204). However, the actual evaluation measures Rényi divergence empirically on a finite test set: lines 112 and 182 state "we report the maximum Rényi divergence over all input pairs as the RDP measure" and "report the worst-case divergence across all test set pairs." Definition 2.2 (RDP) requires the bound to hold for *any pair of adjacent inputs*, not just examples drawn from a test distribution. No analytical, input-independent bound on the Rényi divergence is derived. The paper measures empirical divergences on test pairs and calls this a privacy guarantee — this is a fundamental mismatch between claim and evidence. The method might be salvageable as an empirical privacy auditing framework or a regularization method, but the paper's framing asserts a stronger claim than the methodology can support.

### Major

- **No adjacency notion is defined.** Definition 2.2 (RDP) requires a randomized mechanism to satisfy the bound for "any pair of adjacent inputs." Yet the paper explicitly states "We do not assume any specific notion of adjacency between examples" (line 112). Without an adjacency relation, the RDP definition is ill-posed. The reported privacy numbers (RD, BDP) measure distinguishability between entirely different sentences (e.g., a positive vs. a negative review), which is a substantially different (and weaker) threat model than standard DP, which protects against inferring whether a single attribute or record is present. The paper does not discuss what notion of protection its numbers correspond to.

- **No comparison to standard differential privacy baselines.** The only privacy-preserving baseline is VTDP, an ablation designed by the authors. Missing comparisons include: (a) DP-SGD fine-tuning of BERT (Abadi et al., 2016), the standard approach for private NLP; (b) calibrated Gaussian noise added directly to BERT embeddings (a standard LDP baseline); and (c) other DP embedding methods from the NLP+DP literature. Without these, it is impossible to assess whether NVDP offers any practical advantage over established DP methods, or whether the reported BDP values (ε_μ ≈ 10.7–22.2) represent meaningful privacy protection relative to alternatives.

- **Training-phase information leakage is not addressed.** The paper fine-tunes BERT during training (line 148), meaning the BERT parameters are updated on private data and could themselves encode sensitive information. The privacy analysis only considers the final NVIB posterior distributions at test time; the fine-tuning process itself (which standard methods like DP-SGD would protect) is not accounted for. An adversary with access to the final model parameters could potentially extract training-data information through the BERT parameters themselves, independent of the NVIB noise.

### Minor

- **The experimental protocol introduces optimistic bias.** The paper selects the best-performing run on the validation set out of 5 runs for final evaluation (line 182), and both utility and privacy numbers come from this cherry-picked run. Standard practice is to report means and variances across runs. Since privacy is reported as a *worst-case* measure (maximum RD), using the run with the best utility likely understates the privacy leakage of a typical model.

- **The NVDP vs. VTDP comparison is confounded.** The two methods differ in more than just the parametric vs. nonparametric nature of their bottleneck — they have different architectures, capacity, and regularization mechanisms. The paper attributes VTDP's worse privacy-utility trade-off solely to it being "VIB-based" rather than "NVIB-based" (line 200), without controlling for these confounds.

- **The reported BDP values (ε_μ ≈ 10.7–22.2) are very high.** The paper does not contextualize what ε_μ = 10.7 means in practice. In standard DP, ε > 10 is generally considered very weak privacy; even though BDP is a different framework, the reader is left without guidance on whether these numbers constitute meaningful protection.

### Trivial

None.

## Nice-to-Haves

- **Derive analytical privacy bounds.** The most impactful improvement would be to derive input-independent bounds on the Rényi divergence in terms of the NVIB parameters. Even loose bounds would convert the method from an empirical measurement to a genuine DP mechanism.

- **Define an appropriate adjacency notion.** The paper should define what constitutes "adjacent" text inputs (e.g., single-word substitution, bounded edit distance) and report privacy numbers under that notion, consistent with standard DP practice.

- **Add standard DP baselines.** At minimum, DP-SGD fine-tuning of BERT on the same GLUE tasks should be compared, along with a Gaussian-noise LDP baseline on the embeddings.

- **Report means and variances** across all 5 runs rather than selecting the best validation run.

- **Discuss composition.** If multiple embeddings from the same user are shared, privacy guarantees degrade; the paper should address this.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Task-specific calibration defeats reusable embeddings."** The paper mentions reusability as a motivation for the general approach of sharing noisy embeddings (line 17-18: "the shared data can be reused for multiple purposes"), not as a demonstrated property of NVDP. The method is explicitly task-specific. This criticism overstates the paper's claim.

- **"No discussion of sensitivity."** Computing the sensitivity of the NVIB posterior parameters would require a fundamentally different analytical approach. This is a direction for future work, not a flaw in the current empirical methodology.

- **"No discussion of composition."** Beyond the paper's stated scope.

- **"BDP conversion not explained."** The paper cites the original work (Triastcyn & Faltings, 2020) for the derivation, which is standard practice.

- **"NVIB sampling approximation tightness unknown."** The paper explicitly acknowledges this in footnote 3 ("We leave better bounds on the RD between samples from Dirichlet Processes to future work"), so it is not a hidden weakness.

- **Generic strengths** ("The paper is clearly written," "well-motivated problem") are removed as insufficiently specific.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the fundamental disconnect between the claimed DP guarantees and the empirical methodology, but this is a critique of the paper's framing rather than a novel insight about the method itself.

## Suggestions

1. **Reframe the paper honestly.** Present NVDP as an empirical privacy-regularization framework that measures Rényi divergence on test data, not as a method that provides formal DP guarantees. The title would need to change accordingly (e.g., "Empirical Privacy Auditing of Transformer Embeddings with Nonparametric Information Bottleneck"). This reframing would honestly reflect what the paper actually demonstrates.

2. **Add standard DP baselines** (DP-SGD, Gaussian noise) to situate the results within the literature.

3. **Report all 5 runs** (mean and variance) instead of cherry-picking the best.

4. **Define adjacency** and discuss what privacy threat the reported numbers correspond to.

5. **Contextualize the BDP values** by explaining what ε_μ ≈ 10–22 means for practical privacy protection.

---

**Calibration Summary:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison to paper under review |
|--------|------|-----------|-------|-----------|----------------------------------|
| Nonlinear Inference Learning | uxFme785fq | 2.50 | R1 | Yes | Similar overclaiming of DP; less technical novelty. |
| MAAD Private | FNCFiXKYoq | 3.00 | R1 | Yes | Similar structural issue (claims DP without proper guarantees, missing baselines). Most comparable in severity and score. |
| Adv. DP through Synth. Alignment | TbOcySs6g8 | 2.50 | R2 | Yes | Similar fatal flaw ("does not offer DP guarantees as claimed"); comparable severity. |
| Private Wasserstein Distance | O7wTfBLSFn | 5.00 | R2 | Yes | Also lacks formal privacy guarantees, but framed honestly (does not claim DP in title). Scored higher due to honest framing. |
| DPPN (embedding defense) | DF5TVzpTW0 | 6.00 | R1 | Yes | Empirical embedding defense without formal DP, but framed honestly. Stronger experiments and baselines. |
| Copyright & Privacy | HmL2Buf0Ur | 3.75 | R2 | Yes | Different topic; less direct comparison. |

**Round 1 bracket:** Based on the strong-reject anchors (1.0–1.5) being clearly below the paper's technical substance and the 5.5+ anchors requiring more complete evaluation, the plausible range was [2.0, 4.5].

**Round 2 narrowing:** The MAAD Private anchor (3.00) shares the same structural flaw (claims DP without adequate guarantees) and missing-baseline issue. The PASDA anchor (2.50) shows what a fatal DP-claim-invalidity scores. Our paper has more technical novelty than either, but its central contribution is equally undermined by the claim-evidence mismatch. The Private Wasserstein Distance (5.00) demonstrates the ceiling achievable when a paper is technically sound and honestly framed — our paper cannot reach that due to the fatal framing issue.

**Final score: 3.0.** The paper's technical ideas (NVIB + RD for privacy measurement) are novel and the derivation is competent. However, the fatal mismatch between claiming "differential privacy guarantees" and only providing empirical test-set measurements, combined with the absence of adjacency definition, missing DP baselines, and unaddressed training-phase leakage, place this firmly in the reject range.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>