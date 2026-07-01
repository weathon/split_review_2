## Summary

This paper proposes **STNAdam**, a variant of Adam that maintains two coupled iteration trajectories — a regular update track and a Nesterov-style extrapolation track — for solving "nonconvex + weakly-convex" composite optimization problems. The stochastic gradients can be provided by any variance-reduced estimator (SVRG, SAGA, SARAH, SPIDER). The paper provides a convergence analysis under the Kurdyka-Łojasiewicz (KL) property and reports empirical results on low-light image enhancement (LIE) on the LOL dataset.

---

## Strengths

1. **Genuinely novel algorithmic structure (Algorithm 1, Section 2).** The two-track framework — maintaining a regular update point $x^{k+1}$ and an extrapolation track $\tilde{x}^{k+1}$ via an intermediate point $\bar{x}^{k+1}$, coupled through shared adaptive learning rates and separate momentum corrections — is a non-trivial architectural departure from single-track Adam variants (NAdam, SNAdam, SAdan). This is not a simple recombination of existing components.

2. **Broad convergence framework (Section 3, Theorems 1–2).** The analysis accommodates arbitrary variance-reduced gradient estimators within a unified KL-based framework and covers both almost-sure convergence and finite-length properties. The convergence rates in Theorem 2 (exponential for KL exponent $\vartheta \in (0,1/2]$, polynomial for $\vartheta \in (1/2,1)$) are explicit. This level of theoretical generality is rare among Adam-variant papers.

3. **Strong quantitative results on the LOL benchmark (Table 2).** STNAdam-SARAH achieves PSNR 22.26, SSIM 0.906, LPIPS 0.050, substantially ahead of the best baseline (Retinex-Net at 18.44 PSNR). Even the fairly-compared STNAdam-SGD (18.06 PSNR) outperforms all three single-track baselines (SGD 14.80, SAdam 16.38, SNAdam 17.14).

---

## Weaknesses

### Fatal

None.

### Major

1. **Confounded experimental design prevents attribution of the best results (Table 2).**  
   The headline results for STNAdam-SAGA (21.05 PSNR) and STNAdam-SARAH (22.26 PSNR) use variance-reduced gradient estimators (SAGA, SARAH), while all baselines (SGD, SAdam, SNAdam) use plain SGD without variance reduction. This conflates **two separate factors**: the novel two-track framework and the use of variance-reduced estimators. It is well-established that SAGA and SARAH improve convergence in finite-sum problems. Missing baselines that would isolate the two-track mechanism include:
   - **Adam-SAGA**, **Adam-SARAH** (single-track Adam with the same variance-reduced estimators)
   - **SNAdam-SAGA**, **SNAdam-SARAH** (Nesterov-accelerated single-track with the same estimators)

   The paper's central empirical claim — that STNAdam is superior — is not supported by an experiment that isolates STNAdam's actual novelty. The one fair comparison (STNAdam-SGD vs SNAdam, both using SGD) shows a modest ~5% improvement (18.06 vs 17.14 PSNR), which is not the basis for the paper's strongest claims. *Evidence in paper:* Table 2 (lines 291–298) and Section 1.2 contribution (iii) (line 50) claim "excellent performance on LIE tasks."

2. **Single-task, single-dataset evaluation is insufficient for the claims made (Section 4).**  
   Every experiment is on the LOL dataset for low-light image enhancement. The paper claims general applicability to a broad class of "nonconvex + weakly-convex composite optimizations" (abstract, line 17, line 336). Standard practice for optimizer papers at top venues includes evaluation across multiple domains (classification, generation, restoration), architectures (CNNs, Transformers), and datasets. Even within LIE, only one dataset is used. *Evidence in paper:* Section 4 (lines 279–332), claims in title and abstract (lines 5–9).

### Minor

3. **Inconsistent baseline citations undermine reproducibility (lines 33, 50, 281).**  
   There are factual inconsistencies in how baselines are attributed:
   - **SAdam** is cited as Kingma & Ba (2014) in the experiments (line 281), but Kingma & Ba is the original Adam paper, not the SAdam variant. In the related work (line 33), SAdam is attributed to Le-Duc et al. (2024).
   - **SNAdam** is attributed to Reddi et al. (2019) in the related work (line 33), but to Xie et al. (2024) in both the contributions (line 50) and experiments (line 281). Xie et al. (2024) is described in the same related work paragraph as proposing "SAdan," not SNAdam.

   These inconsistencies make it unclear what the baseline algorithms actually are and compromise reproducibility.

4. **"Dynamically scheduled" hyper-parameters depend on unknown problem constants (Eqs. 6–8, lines 172–193).**  
   The paper claims that internal parameters $\gamma_{k+1}, \alpha_{k+1}, \lambda_{k+1}$ can be "dynamically scheduled within some iterate-dependent finite intervals, removing hand-tuning" (lines 47–48). However, the lower bounds for these intervals depend on the smoothness modulus $L$, weak-convexity modulus $\tau$, variance-reduction constants $V_1, V_\Upsilon, \rho$, and a parameter $M$ from the energy function (9). These are global problem-dependent quantities unknown to the user. Remark 3's suggestion to "appropriately increase" $L$ and $\tau$ is circular — these are properties of the problem, not free parameters. The claim of removing hand-tuning is therefore overstated.

5. **No statistical uncertainty reported for any experimental result (Tables 2–3).**  
   No confidence intervals, standard deviations, or variance information is reported for any metric. The reader cannot assess whether the reported differences (e.g., PSNR 18.06 vs 17.14 between STNAdam-SGD and SNAdam) are statistically significant. *Evidence in paper:* Tables 2–3 (lines 291–322).

6. **Timing values are implausibly small and unclarified (Table 2).**  
   Values like 2.64e-05 seconds (~26 µs) are reported as "Time(s)." These numbers are orders of magnitude faster than typical image-level processing. If these are per-iteration or per-patch timings, the column heading and text should clarify this. Additionally, STNAdam-SARAH (2.64e-05) is reported as faster than SGD (2.85e-05), which is counterintuitive since SARAH has additional overhead from periodic full-gradient computations and table maintenance. *Evidence in paper:* Table 2 (lines 293–298).

7. **Key intuitive concept "larger update neighborhood" is never formally defined (lines 9, 43, 91).**  
   This phrase is the paper's central intuitive motivation for the two-track framework, appearing in the abstract, contributions list, and method description. Yet it is never given a precise mathematical or geometric definition, leaving the core intuition qualitative and unverifiable.

8. **Gap between theory and one experimental variant (Lemma 1, Algorithm 1, line 124).**  
   The paper explicitly acknowledges that "SGD does not exhibit variance reduction" (line 124), and Lemma 1 defines conditions for an estimator to be "called variance-reduced." Algorithm 1 specifies that the stochastic gradient is generated "by a variance-reduced gradient estimator" (line 100). Yet the paper evaluates STNAdam-SGD, which uses the non-variance-reduced SGD estimator. The paper does not clarify whether the theoretical guarantees (Lemma 2–Theorem 2, which are derived under Lemma 1's variance-reduced conditions) apply to STNAdam-SGD or only to STNAdam-SAGA/SARAH variants.

### Trivial

None.

---

## Nice-to-Haves

- **Ablation isolating the two-track mechanism from the gradient estimator choice.** The single most informative experiment would be to implement single-track versions of STNAdam (i.e., remove the $\bar{x}^{k+1}/\tilde{x}^{k+1}$ extrapolation while keeping everything else) and compare them against the two-track versions with the same estimator.
- **Evaluation on one or two standard deep learning benchmarks** (e.g., training a small CNN on CIFAR-10, or a small Transformer on a text task) to demonstrate generality beyond LIE.
- **Clarification** of what "larger update neighborhood" means geometrically or analytically, perhaps with a synthetic 2D example showing the trajectory difference.

---

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Criticism about convergence theory deferring to appendix (Critical Issue #5 in input):** The reviewer faulted the main text for not summarizing feasibility conditions that are in the appendix. Per policy, content that was stripped by the parser is assumed to exist in the original submission. Removed.
- **Complaint about notation heaviness in Section 2:** This is a presentational observation that does not constitute a substantive weakness. Removed.
- **Complaint about Figure 1 description being text-only:** Parser artifact — the original PDF would contain the actual figure. Removed.
- **Criticism that SAdam/SNAdam comparison counts as "factual error" about the existence of certain methods:** This is kept as a citation inconsistency within the paper (different citations for the same method in different sections), but the removed version was that it's a "structural" error implying the methods don't exist. Removed and replaced with the specific, verified inconsistency.

---

## Novel Insights

None beyond the paper's own contributions. The review surfaces the key confound between the two-track mechanism and variance-reduced estimators, but this is a standard experimental-design observation, not a novel insight about the algorithm itself.

---

## Suggestions

1. **Add controlled baselines:** Implement Adam-SAGA, Adam-SARAH, SNAdam-SAGA, and SNAdam-SARAH so that the only difference between each pair is the two-track vs. single-track structure. Report these alongside the current results.
2. **Add uncertainty quantification:** Report means and standard deviations over multiple runs (at least 3–5) for all metrics.
3. **Correct baseline citations:** Ensure SAdam is consistently attributed, and resolve the SNAdam attribution conflict between Reddi et al. (2019) and Xie et al. (2024).
4. **Clarify timing units:** Explain whether "Time(s)" is per-iteration, per-image, or something else; explain why STNAdam-SARAH is faster than SGD.
5. **Provide practical defaults for the dynamic scheduling intervals** that do not require the user to estimate $L$, $\tau$, and variance constants, or clearly state that the intervals are theoretically-motivated bounds requiring estimation.
6. **Define "larger update neighborhood"** more precisely, even if only qualitatively or with a simple illustrative example.

---

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>