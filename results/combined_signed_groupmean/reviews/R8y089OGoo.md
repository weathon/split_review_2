Now I have sufficient calibration data. Let me synthesize and write the final review.

**Round 1 Bracket:** Based on comparison with anchors, the paper sits between score 6.0 and 7.5. The closest methodological anchor is DAC (Diffusion Actor-Critic, score 6.5), which also formulates KL-constrained policy iteration with diffusion models. Our paper has similarly strong theory (+9.92 vs DAC's +9.96) and experiments (+10.00 vs DAC's +10.00), and a similarly impactful confound weakness (-9.96 for NAVSIM vs DAC's -9.99 for Q-ensemble). Our paper has cleaner theory (no equation errors like DAC's -9.93) and broader evaluation (39 tasks vs D4RL). This places it slightly above DAC.

**Round 2 Narrowing:** Comparing to the 7.0-8.0 band anchors (CLoSD at 7.5, Safe Offline RL at 7.5, Diffusion-Based Planning at 7.5, Multi-Robot Motion Planning at 7.5), these papers address different problem settings without the NAVSIM confound. Our paper's NAVSIM weakness is a genuine limitation that doesn't apply to those papers. Hence our paper sits below the 7.5 band.

**Final placement:** Between DAC (6.5) and the 7.5 papers. The NAVSIM issue is real and would require addressing, but the core contribution is strong and well-supported. Score: **7.0**.

---

## Summary

This paper proposes DIPOLE, an RL algorithm for fine-tuning diffusion policies. The key idea is to reformulate the KL-regularized RL objective with a greedified reference policy, which naturally decomposes the optimal policy into two dichotomous components with bounded sigmoid weights — a "positive" policy for reward maximization and a "negative" policy for minimization. During inference, actions are generated via CFG-style score interpolation, enabling controllable greediness. The method is evaluated on 39 tasks across ExORL and OGBench (offline and offline-to-online RL) and on a real-world autonomous driving benchmark (NAVSIM) with a billion-parameter VLA model.

## Strengths

- **Theoretically clean decomposition.** The core insight — that the optimal policy under the greedified KL-regularized objective decomposes into a ratio of two dichotomous policies weighted by bounded sigmoid functions (Eqs. 7–10) — is mathematically sound and elegant. The score-combination formula ∇log π* = (1+ω)∇log π⁺ − ω∇log π⁻ provides a principled alternative to unstable exp(βG) weighting. **[impact=+9.92]**

- **Elegant connection to classifier-free guidance.** The observation that the resulting inference procedure (Eq. 10) mirrors CFG follows from the mathematics, not a superficial analogy. The paper correctly identifies the smoothing and decoupling advantages over CFGRL, which uses hard thresholding I_{A≥0} and the same model for both terms. **[impact=+9.39]**

- **Strong empirical results across many tasks.** The paper evaluates on 39 tasks across two benchmarks (ExORL and OGBench) plus a real-world driving benchmark. DIPOLE achieves best or near-best performance on most task categories, with substantial gains on ExORL (e.g., Walker and Quadruped tasks) and OGBench cube-double-play (44 vs. 29 for next best). **[impact=+10.00]**

- **Scalability demonstration to billion-parameter VLA models.** The autonomous driving experiment with a 1B-parameter model shows the method does not break at scale, a genuine practical contribution. **[impact=+10.00]**

## Weaknesses

### Fatal
None.

### Major

- **NAVSIM evaluation confound.** Table 4 reports DIPOLE navtrain (89.7 PDMS, +1.4 over DP-VLA 88.3) and DIPOLE navtest (94.8, +6.5). The navtest variant is trained on **test-split data** — a non-standard protocol. The paper acknowledges this ("we provide a variant of our model trained on the test split") but presents both results side by side without sufficiently distinguishing the experimental regime. The proper apples-to-apples comparison is DIPOLE navtrain (89.7) vs. baselines, where the 1.4-point gain over an already-strong imitation baseline is modest. Additionally, DPPO is only reported on navtest (89.0), not navtrain, making the RL fine-tuning comparison incomplete. **[impact=-9.96]** (Combined from three sub-items with impacts -9.96, -6.24, -2.11)

### Minor

- **Overclaimed "completely resolving" sample dominance.** The paper states (line 105) that dichotomous weighting "completely resolves the issue of being dominated by high-return samples as in exp-weighted regression." While sigmoid weights are bounded (unlike exponential weights), σ(βG) still increases with G, so high-return samples retain higher weight. The improvement is meaningful (bounded vs. unbounded weights) but "completely resolves" overstates the benefit. **[impact=-0.01]**

- **Not universally dominant across all tasks.** On OGBench (Table 2), DIPOLE underperforms IFQL on humanoidmaze-large-navigate (6 vs. 11) and FQL on antsoccer-arena-navigate (57 vs. 60). The paper does not discuss when or why the method struggles. **[impact=-0.00]**

### Trivial
None.

## Nice-to-Haves

- Add discussion of the interaction between β (temperature) and ω (greediness factor), since both control greediness but their trade-off is not analyzed.
- Discuss the computational cost of training two diffusion models (π⁺ and π⁻) versus one, and whether LoRA-style parameter sharing is used beyond the AD experiment.
- Analyze when DIPOLE underperforms (e.g., humanoidmaze-large-navigate) to help readers understand the method's limitations.

## Removed Points

These points were flagged by the input review but are removed per the filtering rules:

- *"Value function learning not specified in main paper"* — REMOVED: The paper states "algorithm pseudocode and additional implementation details are provided in Appendix C and D." The parser strips appendices from all papers; this content exists in the original submission.
- *"No ablation analysis in main paper"* — REMOVED: The paper states "we refer to Appendix D.4 for ablation studies." Same reasoning as above.
- *"Rejection sampling does heavy lifting"* — REMOVED: IFQL (a key baseline) also uses rejection sampling, so the comparison is fair. DIPOLE w/o rs still outperforms CFGRL on most tasks.
- *"Abstract/intro highlight 94.8 without caveat"* — REMOVED: Factually inaccurate; the abstract and introduction do not cite specific NAVSIM numbers.
- *"Greedified objective introduced ad hoc"* — REMOVED: Subjective opinion, not a concrete weakness.
- *"'We do not observe adoption' claim overstated"* — REMOVED: Minor wording quibble.

## Novel Insights

None beyond the paper's own contributions. The core insight (dichotomous policy decomposition from greedified KL-regularized RL) and the connection to CFG are the paper's own novel contributions; the reviews surface no additional synthesis beyond what the authors already provide.

## Suggestions

1. **Clean up the NAVSIM evaluation:** Clearly separate the navtrain and navtest regimes in a way that prevents conflation. Report DPPO on navtrain so that readers can compare DIPOLE navtrain (89.7) against a DPPO baseline on the same split. Consider moving the navtest result to a separate section with a clear caveat.
2. **Tone down the "completely resolves" claim** to something like "substantially mitigates" or "reduces the impact of."
3. **Briefly discuss the method's limitations** in tasks where it underperforms baselines (humanoidmaze-large-navigate, antsoccer-arena-navigate) to give a more balanced picture.

## Score and Decision

**Calibration anchors used:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| ldVkAO09Km (DAC) | 6.5 | R2 | Yes | Most similar methodologically (KL-constrained policy iteration + diffusion). Both have strong theory (+9.96) and experiments (+10.00), and both have a confound weakness (~-9.99). Our paper has cleaner theory and broader evaluation. Slightly above DAC. |
| xCRr9DrolJ (SRPO) | 6.25 | R2 | Yes | Score-regularized policy optimization. Main weakness: limited novelty (-10.00). Our paper has stronger novelty. |
| cXxfVkRCHJ (CFDG) | 3.0 | R1 | Yes | Much weaker theory and novelty. Our paper is clearly stronger. |
| fXkoROek1M (HRF) | 4.0 | R1 | Yes | Incremental over DDPO. Our paper has stronger contribution. |
| 1vmSEVL19f (DRaFT) | 6.0 | R1 | Yes | Different domain (image generation). Strong experiments but DRaFT-LV questioned as minor over ReFL (-10.00). |
| svp1EBA6hA (CTRL) | 6.5 | R1 | Yes | Conditional control via RL for image generation. Limited experiments (-9.97). |
| TeeyHEi25C (DVF) | 6.25 | R2 | Yes | Diffusion for value estimation. Weaker empirical evidence, missing baselines (-9.88). |
| tGQirjzddO (LDCQ) | 6.33 | R2 | Yes | Latent diffusion for offline RL. Different approach. |

**Final score rationale:** The paper's core theoretical contribution is strong and original. The RL benchmark evaluation on 39 tasks is thorough and convincing. The NAVSIM evaluation is the main weakness: the navtest (94.8) result is trained on test-split data, and the navtrain (89.7) gain is modest. However, the paper is transparent about the setup, and the core contribution does not depend on the AD experiment. Comparing to the closest anchor DAC (6.5), our paper has similarly strong theory and experiments but a cleaner mathematical derivation and broader evaluation. The NAVSIM confound is comparable to DAC's Q-ensemble confound in severity. This places the paper slightly above DAC but below the clean 7.5-band papers that lack such confounds.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>