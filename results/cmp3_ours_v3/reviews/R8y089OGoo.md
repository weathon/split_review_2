Now let me produce the final consolidated review.

## Summary

DIPOLE proposes a method for RL fine-tuning of diffusion policies by introducing a greedified KL-regularized objective that decomposes the optimal policy into a pair of dichotomous policies: a positive policy (sigmoid-weighted, reward-maximizing) and a negative policy (sigmoid-weighted, reward-minimizing). The two policies are trained stably with bounded sigmoid weights, and the optimal policy is recovered via CFG-style score interpolation at inference, enabling controllable greediness through a parameter ω. Experiments span offline and offline-to-online RL on ExORL (9 tasks) and OGBench (30 tasks), plus scaling to a 1B-parameter VLA model for autonomous driving on NAVSIM.

## Strengths

1. **Elegant and theoretically grounded formulation (Sections 3.1–3.2).** The paper identifies a concrete problem with exp-weighted regression — the unbounded exponential weight causes loss explosion and training instability — and proposes a clean mathematical resolution. The derivation from the greedified KL-regularized objective (Eq. 5) through the closed-form solution (Theorem 1) to the dichotomous decomposition (Eqs. 7–8) is mathematically sound and well-motivated. The sigmoid-based replacement of the exponential is genuinely clever.

2. **Insightful connection to classifier-free guidance (Section 3.2, Eq. 10).** The paper shows that the score of the optimal policy can be expressed as a linear combination of the scores of the positive and negative policies, formally identical to CFG. This connection emerges naturally from the derivation, not as a superficial analogy, and provides a principled interpretation of the greediness factor ω.

3. **Scalability demonstration to large VLA models (Section 4.2, Table 4).** Scaling to a 1-billion parameter vision-language-action model for autonomous driving on NAVSIM is a genuine strength that goes well beyond what the diffusion-policy RL literature typically demonstrates. Positive results at this scale (+1.4 PDMS on the standard navtrain split, +6.5 on navtest) demonstrate practical viability beyond toy domains.

## Weaknesses

### Fatal
None.

### Major

1. **Missing ablation: the practical value of the negative policy π⁻ against a simpler alternative.** The paper trains two separate diffusion models (or two LoRA modules) for π⁺ and π⁻. A natural baseline is: train only π⁺ (sigmoid-weighted) and use the original reference policy μ as the negative policy in the CFG-style combination: ε^* = (1+ω)ε⁺ − ωε_μ. This would require only one model and directly tests whether the doubled model count is buying anything. The paper mentions CFGRL as related (which uses indicator-based weighting with μ as negative) but does not compare against this single-model sigmoid-weighted variant. Without this ablation, readers cannot assess whether the dichotomous decomposition (the paper's core design choice) provides meaningful benefit over a simpler approach, or whether the main contribution effectively reduces to "sigmoid weighting + CFG-style inference."

2. **Undiscussed underperformance on Jaco manipulation tasks (Table 1).** On ExORL, DIPOLE achieves 117/110 on Jaco reach-top-right/reach-top-left with rejection sampling, while IFQL scores 193/181 and FQL scores 224/222 — roughly a 50% deficit. These are large, systematic gaps on manipulation tasks — a core domain for diffusion policies — that the paper does not acknowledge or analyze. The paper's claim of "best or near-best performance" is accurate for most tasks (DIPOLE leads on 4/6 OGBench categories and all Walker/Quadruped/Cheetah tasks) but does not characterize where the method meaningfully falls short. Providing diagnostic analysis (e.g., whether poor Q-value estimates for high-DOF manipulation tasks make sigmoid weighting less effective) would strengthen the paper significantly.

### Minor

3. **NAVSIM test-split framing in the abstract is ambiguous.** The abstract states DIPOLE achieves strong results on NAVSIM without distinguishing the standard navtrain evaluation (+1.4 PDMS over the strong pretrained baseline) from the non-standard navtest evaluation (+6.5 PDMS) that trains on test-split scenarios without ground-truth labels. The table labels are clear (Table 4 explicitly marks both rows), and the paper does describe the setup in the text ("We also consider an RL application scenario where RL can be applied in human take-over situations..."). However, the high-level summary in the abstract and conclusion could lead a reader to conflate the larger navtest improvement with the standard evaluation protocol, since only the top-line 94.8 PDMS figure is highlighted without qualification.

4. **Computational cost is not discussed.** DIPOLE requires training two diffusion models (or maintaining two LoRA modules). The paper presents no analysis of training time, memory footprint, or inference overhead compared to single-model baselines. For practitioners evaluating the method, the doubled cost is relevant information.

5. **Potential inference-time distribution shift from CFG-style combination is not discussed.** While the paper correctly notes that the individual models π⁺ and π⁻ are trained with bounded sigmoid weights (ensuring stable training), the CFG-style score combination ε^* = (1+ω)ε⁺ − ωε⁻ used at inference can produce out-of-distribution samples for large ω — a known issue in the CFG literature. The paper frames the method as having "completely resolved" the issues of exp-weighted regression without acknowledging this distinction between stable training and potentially unstable inference behavior at high greediness factors.

### Trivial
None.

## Nice-to-Haves

- Analysis of the effect of the greediness factor ω on performance (the paper references Appendix D.4 for ablations).
- Statistical significance tests (e.g., paired bootstrap CIs) to indicate which improvements are reliable beyond the provided standard deviations and 8-seed evaluations.
- A brief discussion of why the method underperforms on Jaco tasks — whether the issue lies in Q-value quality for high-DOF manipulation, the sigmoid weighting scheme, or something else.

## Removed Points

- **Criticism that the stability claim is fundamentally misleading (exponential explosion "shifted to inference").** This criticism conflates training-time stability (which the paper correctly claims — individual models π⁺ and π⁻ use bounded sigmoid weights in [0,1], precluding loss explosion during training) with inference-time behavior (where the CFG-style combination is a separate concern). The paper's core claim about stable training is valid. The legitimate inference concern is retained as Minor weakness 5 above.

- **Criticism that the paper oversimplifies prior art on clipping.** The paper explicitly acknowledges clipping as a mitigation strategy used by prior work (Garg et al., 2023; Xu et al., 2023a; Hansen-Estruch et al., 2023) in Section 3.1. The distinction between hard clipping and smooth sigmoid weighting is fairly stated.

- **Notation concern about neutral actions (G≈0) being equally weighted by π⁺ and π⁻.** Both policies modeling neutral-reward actions at equal weight (σ=0.5) does not cause any methodological problem; it is a natural consequence of the sigmoid function and does not constitute a weakness.

- **Criticism about missing statistical significance tests.** Not standard practice for these benchmarks; 8-seed reporting with standard deviations is already provided.

- **Criticism about ω hyperparameter sensitivity being absent from the main text.** The paper references Appendix D.4 for ablation studies; the appendix is stripped by the parser and cannot be verified.

## Novel Insights

The most useful insight from the review process is the identification of a critical missing baseline: the paper's central practical claim hinges on training two separate policies via dichotomous decomposition, but the natural ablation (train π⁺ only with sigmoid weighting, using the reference policy μ as the negative policy in the CFG combination) is not tested. A second insight is that the paper's empirical results are more heterogeneous than the narrative suggests — strong on locomotion but notably weak on manipulation (Jaco), which the paper does not discuss. These gaps are fixable but require additional experimentation and analysis.

## Suggestions

1. **Add the single-model ablation.** Compare DIPOLE (two models) against a variant that trains only π⁺ with sigmoid weighting and uses μ as the negative policy. If the simpler variant performs similarly, reframe the contribution around sigmoid weighting + CFG-style inference rather than dichotomous decomposition. If π⁻ is materially better, the paper gains a much stronger empirical argument.

2. **Acknowledge and analyze the Jaco failure cases.** Provide diagnostic evidence — for instance, does the issue lie in Q-value accuracy for high-DOF manipulation, or does the sigmoid weight 1−σ(βG) for π⁻ dominate learning in these tasks?

3. **Clarify the NAVSIM results in the abstract** by briefly distinguishing the standard navtrain protocol from the non-standard navtest protocol.

4. **Add a brief discussion of computational overhead** (training time, memory, inference) and a note about inference-time behavior of the CFG-style score combination at high ω values.

---

**Calibration Report.** Round 1 bracket: [5.5, 7.0]. Retrieved anchors across all bands:

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| "Sampling from Energy-based Policies using Diffusion" | 3.75 | R1 | Weaker theory and experiments; narrower scope. DIPOLE is clearly stronger. |
| "Learning a Diffusion Model Policy from Rewards via Q-Score Matching" | 5.00 | R1 | Similar domain but weaker empirics and less clean theory. DIPOLE is stronger. |
| "Diffusion Actor-Critic" | 6.50 | R2 | Comparable contribution (KL-constrained diffusion policy optimization). DIPOLE has cleaner theory and broader experiments but similar-level weaknesses (missing ablations). |
| "Score Regularized Policy Optimization" | 6.25 | R1,R2 | Similar offline RL + diffusion space. DIPOLE has stronger theory and real-world scaling. |
| "Energy-Weighted Flow Matching" | 6.25 | R2 | Similar weighted-loss approach. DIPOLE has clearer novelty. |
| "Direct Distributional Optimization" | 7.00 | R1 | Stronger theory (convergence guarantees) but weaker experiments (toy + small images). Different contribution type. |

DIPOLE sits above the ~5.00 papers (which were rejected) and is comparable to the 6.25–6.50 papers (which were accepted). The main weaknesses (missing ablation, undiscussed underperformance) are fixable and do not invalidate the core contribution, but they prevent a higher score. Final score 6.0 reflects a borderline-to-solid accept with actionable revision requirements.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>