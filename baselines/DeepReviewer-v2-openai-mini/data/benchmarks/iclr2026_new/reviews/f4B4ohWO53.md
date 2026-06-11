## Summary
# Final Review Report

## Summary

This paper proposes Nonparametric Variational Differential Privacy (NVDP), a method for sharing transformer embeddings with differential privacy guarantees. The core idea is to integrate a Nonparametric Variational Information Bottleneck (NVIB) layer as a trainable noise mechanism: the NVIB layer learns a posterior distribution over multi-vector embeddings, and a sample from this posterior serves as a sanitized, shareable representation. Privacy is measured using Rényi divergence (RD) and converted to Bayesian Differential Privacy (BDP) guarantees. The method is evaluated on six GLUE tasks using BERT-base.

**Strengths:** (1) The paper addresses an important problem — privacy-preserving sharing of multi-vector transformer embeddings — which is underexplored relative to single-vector embedding privacy. (2) The idea of using NVIB's learned posterior as a calibrated noise distribution is technically sound and connects two previously separate areas (information bottleneck regularization and differential privacy). (3) The comparison against a VIB-based ablation (VTDP) provides some evidence that the nonparametric formulation yields better privacy-utility tradeoffs.

**Core Weaknesses:** (1) The Rényi divergence formula (Eq. 7) contains notation aliasing and potential mathematical errors that affect the correctness of the privacy calculation. (2) Experimental results are reported using best-of-5-run selection without variance, making the reported gains potentially optimistic. (3) The absolute privacy guarantees (BDP epsilon 10.7–20.9) are moderate at best, and the paper overstates them as "strong, practical privacy budgets." (4) The adjacency definition used for DP is never specified, leaving the threat model incomplete. (5) No limitations are discussed, and the conclusion makes an unsupported claim about real-world deployment readiness.

**Novelty assessment:** Deferred to manual literature verification (external paper search unavailable in this run). The core idea — applying NVIB for DP on multi-vector embeddings — appears conceptually novel against the presented baselines (VIB-based VTDP), but a complete novelty assessment requires comparison against the broader literature on embedding perturbation and DP for NLP.

## Strengths
1. **Important problem formulation.** Addressing privacy in multi-vector transformer embeddings is practically relevant. As transformer-based representations become ubiquitous in data-sharing pipelines, having a mechanism that provides formal privacy guarantees while retaining utility addresses a genuine gap. The paper correctly motivates why single-vector DP methods do not trivially extend to multi-vector transformer outputs.

2. **Technically grounded approach.** The integration of NVIB — a Bayesian nonparametric information bottleneck — as a calibrated noise mechanism is conceptually elegant. The idea of training a posterior distribution whose samples serve as sanitized embeddings, and then measuring privacy through Rényi divergence between these sampling distributions, is a principled connection between variational information bottleneck and differential privacy.

3. **Ablation study design.** The comparison against VTDP (VIB-based noise injection) is a fair ablation: both models use the same architecture except for the nonparametric component. Showing that NVDP consistently achieves better privacy-utility tradeoffs across six tasks provides reasonable evidence that the Dirichlet Process formulation is beneficial for multi-vector noise injection.

4. **Dual privacy measurement.** Reporting both Rényi divergence (RD) and Bayesian Differential Privacy (BDP) provides complementary perspectives: RD captures worst-case distinguishability, while BDP provides a more practical average-case interpretation. This dual reporting is a good practice that helps readers calibrate the privacy guarantees.

5. **Clear architectural privacy safeguards.** The paper explicitly identifies two critical design choices for privacy: (a) sampling at both training and test time, and (b) removing the residual connection around Denoising MHA. These choices are clearly motivated and represent principled privacy engineering.

## Weaknesses
### W1 (Major) — Mathematical issues in the core Rényi divergence formula (Eq. 7)

**Location:** Page 5–6 / Section 3.3 — Rényi divergence formula

The central privacy measure relies on Eq. (7), which contains two problems:

**(a) Notation aliasing.** The symbol $\sigma_i^q$ is defined in Section 2.2 as the posterior standard deviation for input $x$. However, in the penultimate line of Eq. (7) and its following definition, $\sigma_i^q$ is redefined as $\sqrt{(1-\lambda)(\sigma_i^{q'})^2 + \lambda(\sigma_i^q)^2}$ — a weighted interpolation between two distributions' variances. Using the same symbol for two different quantities makes the formula ambiguous and may indicate an error in the derivation.

**(b) Ill-defined exponent.** The term $\log \frac{\sigma_i^q}{(\sigma_0^p)^{(1-\lambda)(\sigma_i^q)^\lambda}}$ is mathematically problematic: $(\sigma_0^p)$ is a scalar (the prior standard deviation), but the exponent $(1-\lambda)(\sigma_i^q)^\lambda$ is a vector (since $\sigma_i^q \in \mathbb{R}^d$). Raising a scalar to a vector-valued exponent is not standard. This appears to be a LaTeX rendering corruption of what should be standard Rényi divergence between diagonal Gaussians.

**Impact:** Since the privacy guarantees in Table 1 and all reported RD values are computed using this formula, the numerical results may be incorrect under the current presentation. Authors must clarify the exact computation, provide a corrected formula, and ideally release the RD calculation code for reproducibility.

**Required action:** Replace with the standard Rényi divergence between multivariate Gaussians with diagonal covariances, using distinct symbols for interpolated variance. Publish the privacy calculation code.

---

### W2 (Major) — Best-of-5 selection without variance reporting

**Location:** Page 7 / Section 4 — Experimental Protocol

The paper performs five independent runs but reports only the best validation performance on the test set. No means, standard deviations, or significance tests are provided. This introduces optimistic bias: the reported accuracy gaps between NVDP and baselines (typically 1–3 points) may be within seed variance.

**Impact:** The main claim "NVDP is better able to preserve task-critical information" may not hold under proper statistical evaluation. For instance, on MRPC, NVDP accuracy is 83.0% vs. +REG baseline 82.4% — a 0.6-point gap that could easily be reversed under a different seed.

**Required action:** Report mean ± std over all 5 runs for both accuracy and privacy metrics (RD, BDP). Add a paired significance test (e.g., Wilcoxon signed-rank) between NVDP and VTDP under matched $\lambda_D, \lambda_G$ settings.

---

### W3 (Major) — Privacy guarantees are overstated

**Location:** Page 7–8 (Table 1, Section 4.2), Page 9 (Conclusion)

BDP epsilon values are reported in the range 10.7–20.9. In standard differential privacy, epsilon < 1 is considered strong, epsilon < 10 moderate, and epsilon > 10 weak. While BDP is less conservative than standard DP, the paper does not contextualize these values. The Conclusion calls these "strong, practical privacy budgets" and claims a "significant step towards deploying privacy-preserving transformer embeddings in real-world applications" — both statements overstate the evidence.

**Impact:** A privacy-literate reviewer will notice the mismatch between the reported epsilon values and the paper's characterization. This reduces the credibility of the claims and may lead to rejection on grounds of overclaiming.

**Required action:** (a) Calibrate BDP epsilon against standard DP by discussing the conversion factor. (b) Replace "strong, practical privacy budgets" with a more measured description, e.g., "moderate privacy budgets under the Bayesian interpretation." (c) Remove or substantially qualify the real-world deployment claim.

---

### W4 (Major) — Missing adjacency definition leaves the threat model underspecified

**Location:** Page 4–5 / Section 3.2

The paper states "We do not assume any specific notion of adjacency between examples" (Section 3.2) but earlier spends substantial text discussing adjacency definitions (Section 2.1). Without an adjacency definition, the RDP guarantee is not fully specified: what does it mean for two inputs to be "adjacent" in this setting? If any pair of distinct sentences is considered adjacent, the privacy guarantee is much weaker than if adjacent means "differing by one token." The paper's reported RD values (max over all test set pairs) implicitly assume the strongest adjacency notion (any pair), but this is not stated.

**Impact:** The privacy numbers in Table 1 cannot be properly interpreted without knowing the adjacency definition. A reviewer cannot assess whether the guarantees are meaningful.

**Required action:** Explicitly state the adjacency definition used for both RDP and BDP calculations. If the worst-case RD is computed over all test set pairs, state this clearly and discuss why this choice is conservative/appropriate.

---

### W5 (Major) — No limitations section and unsupported deployment claims

**Location:** Page 9 / Section 5 (Conclusion)

The conclusion contains no discussion of limitations. Essential limitations include: (a) the noise calibration is task-specific (requires retraining for new downstream tasks), (b) the method is only tested on BERT-base, (c) BDP epsilon values are moderate, (d) the RD bound uses simplifying approximations (token alignment via padding, fixed $\kappa_i=1$) whose effect on bound tightness is unanalyzed. The final sentence about "real-world applications" is unsupported by the presented evidence.

**Impact:** The lack of limitations discussion and the presence of unsupported deployment claims reduces the scientific rigor of the paper and may mislead readers about the method's maturity.

**Required action:** Add a dedicated limitations subsection summarizing the four points above. Replace the final sentence with a bounded, cautious statement about future work needed before deployment.

---

### W6 (Minor) — NVIB loss terms ($L_D$, $L_G$) are not explicitly defined

**Location:** Page 3 / Section 2.2 — NVIB training objective

The training objective (Eq. 5) references $L_D$ and $L_G$ without providing their explicit mathematical forms. Given that the privacy guarantee depends on the noise injected by these KL divergence terms, the missing definitions hinder reproducibility. The reader must consult the original NVIB paper (Henderson & Fehr, 2023) to understand how the noise level is calibrated.

**Required action:** In Section 2.2, append the explicit KL divergence formulas for $L_D$ and $L_G$ (or provide them in the appendix with a clear reference). At minimum, state that $L_D = \text{KL}(\text{Dir}(\alpha^q) \parallel \text{Dir}(\alpha^p))$ and $L_G = \sum_i \text{KL}(\mathcal{N}(\mu_i^q, (\sigma_i^q)^2) \parallel \mathcal{N}(0, I))$.

---

### W7 (Minor) — Residual connection removal may limit scalability

**Location:** Page 3–4 / Section 3.1 — Architecture

Removing residual connections around Denoising MHA is a valid privacy choice but its impact on optimization is not discussed. Without residual connections, deeper stacks of NVDP layers would suffer from gradient vanishing. Since only a single NVIB layer is tested, readers cannot assess whether the method extends to multi-layer or deeper architectures.

**Required action:** Add a brief discussion of the gradient flow implications and note that multi-layer extension would require additional normalization or partial skip connections.

---

### W8 (Minor) — Reliance on token-aligned padding for RD computation

**Location:** Page 6 / Section 3.3, footnote 3

The RD calculation assumes that sequences are padded to equal length and aligned by token position. While pragmatic, this assumption breaks positional alignment for semantically different sentences where the same position contains different tokens. The paper acknowledges this is an upper bound ("ordered list is more informative") but does not analyze how tight this bound is.

**Required action:** Add a sensitivity analysis comparing the aligned-position RD against a randomly-permuted baseline to estimate the tightness of the upper bound.

---

### W9 (Minor) — Figure readability and missing error analysis

**Location:** Page 8 / Figure 2

Figure 2 plots accuracy vs. BDP epsilon for NVDP and VTDP. However, the curves appear to be monotonic step functions drawn from few discrete regularization-strength settings (as noted, full results are in Appendix A). Without confidence bands or at least individual run markers, the visual impression of a smooth privacy-utility frontier may be misleading.

**Required action:** Add error bars or individual run points for each regularization setting. If only 3–5 settings are tested, plot them as discrete points rather than interpolated curves.

---

### W10 (Minor) — Title does not convey the practical problem or result

The current title "Differential Privacy for Transformer Embeddings with Nonparametric Variational Information Bottleneck" lists the technique but does not communicate the problem setting or the practical benefit. Consider adding a problem-motivation phrase, e.g., "Calibrated Noise Injection via Nonparametric Variational Information Bottleneck for Private Transformer Embeddings" or a more outcome-focused title.

---

**ASCII Diagram — Paper Structure & Evidence Map**

```text
[Problem: Privacy-preserving sharing of multi-vector transformer embeddings]
    |
    v
[Proposed Solution: NVDP = BERT + NVIB layer + sampling + Denoising MHA (no residual)]
    |
    v
[Privacy Measurement: RD between sampling distributions (Eq. 7) -> BDP conversion]
    |
    v
[Empirical Evaluation: GLUE benchmark, 6 tasks, BERT-base]
    |
    +-- Claims C1-C3: method novelty, tradeoff, better than VIB
    |
    +-- Weaknesses:
         W1: Formula issues (Eq. 7) ---- RISK: Privacy numbers may be incorrect
         W2: Best-of-5 selection -------- RISK: Reported gains may be optimistic
         W3: Overstated privacy --------- RISK: Credibility gap
         W4: Missing adjacency def ------ RISK: Threat model incomplete
         W5: No limitations/overclaim --- RISK: Scientific rigor
```

**ASCII Diagram — Revision Strategy Roadmap**

```text
[Highest Priority Fixes]
    |
    +-- W1 (Correct Eq. 7) ---- [Fix: Replace with standard Gaussian RD, clarify symbols, release code]
    |       |
    |       v
    |   [Expected: Corrected privacy numbers + reproducibility]
    |
    +-- W2 (Add variance) ----- [Fix: Report mean±std over 5 runs, add significance tests]
    |       |
    |       v
    |   [Expected: Honest uncertainty intervals for accuracy comparisons]
    |
    +-- W3 (Calibrate privacy) - [Fix: Contextualize BDP vs standard DP, tone down claims]
    |       |
    |       v
    |   [Expected: Credible privacy positioning]
    |
    +-- W4 (Define adjacency) -- [Fix: Explicitly state threat model, compute RD under that model]
    |       |
    |       v
    |   [Expected: Complete privacy specification]
    |
    +-- W5 (Add limitations) --- [Fix: Insert limitations subsection, bound deployment claims]
            |
            v
        [Expected: Scientifically rigorous conclusion]

[Lower Priority]
    +-- W6: Define L_D, L_G explicitly
    +-- W7: Discuss residual-removal scalability
    +-- W8: Analyze RD bound tightness
    +-- W9: Improve figure presentation
    +-- W10: Revise title
```

## Score
**Final Score: 5/10**

**Rationale:** The paper proposes a conceptually interesting approach to a practically important problem (privacy in multi-vector transformer embeddings). The integration of NVIB for calibrated noise injection is technically creative, and the ablation against VIB-based noise is well-designed. However, the paper has several significant weaknesses that lower its score:

- **Research value and novelty (primary scoring dimension):** The core idea is novel, but the paper's contribution is weakened by the fact that NVIB pre-exists (Henderson & Fehr, 2023) and the main adaptation is using it for DP — a relatively straightforward application. Without external literature verification (retrieval unavailable in this run), the novelty assessment is deferred. Score on this dimension: 5/10.

- **Validity and soundness:** Mathematical issues in the core RD formula (W1) and the best-of-5 selection without variance (W2) undermine confidence in the reported numbers. The missing adjacency definition (W4) means the privacy guarantee is incompletely specified. Score on this dimension: 4/10.

- **Reproducibility:** The missing explicit forms of L_D and L_G, combined with the reliance on an external paper for core NVIB training details, reduce reproducibility. The lack of released code (not stated) and unclear formula in Eq. (7) further hinder reproduction. Score: 4/10.

- **Presentation:** The paper is generally well-structured, but the conclusion overstates findings, and key motivation paragraphs in the introduction lack crisp gap identification. The adjacency discussion is never resolved. Score: 5/10.

The weaknesses are fixable with moderate effort: correcting the RD formula, adding variance reporting, calibrating the privacy claims, and adding a limitations section would substantially strengthen the paper. A revised version addressing W1–W5 could reasonably target a score of 7/10.

**External literature verification:** Novelty and comparison against the strongest baselines in the embedding perturbation and DP-for-NLP literature are deferred to manual verification (paper_search unavailable in this run).