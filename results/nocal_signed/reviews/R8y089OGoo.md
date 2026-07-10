Now I have the per-item impact scores. Let me compile the final review.

## Summary

The paper proposes DIPOLE (Dichotomous Diffusion Policy Improvement), a novel RL algorithm for training diffusion policies. The core idea is to formulate a greedified KL-regularized objective that decomposes the optimal policy into two dichotomous policies (positive/reward-maximizing and negative/reward-minimizing) trained with bounded sigmoid weights, combined at inference via classifier-free guidance. The method is evaluated on 39 offline RL tasks, 4 offline-to-online tasks, and a large-scale autonomous driving benchmark.

## Strengths

- **Theoretical derivation is sound and elegant.** The chain from the greedified KL-regularized objective (Eq. 5) through Theorem 1 (Eq. 6) to the dichotomous decomposition (Eqs. 7–8) is mathematically clean. The observation that the optimal policy can be written as a ratio of two sigmoid-weighted policies and maps onto classifier-free guidance (Eq. 10) is genuinely insightful — this is the paper's central intellectual contribution.

- **Broad evaluation spanning multiple scales.** The paper evaluates on 39 offline RL tasks (ExORL + OGBench), 4 offline-to-online tasks, and a large-scale real-world autonomous driving benchmark (NAVSIM) with a 1-billion parameter VLA model. This breadth goes well beyond most diffusion policy RL papers.

- **Consistent empirical improvements.** DIPOLE outperforms baselines across most ExORL tasks, achieves best or near-best performance on OGBench, and improves the DP-VLA model on the standard navtrain split (88.3 → 89.7 PDMS).

## Weaknesses

### Major

- **Missing exp-weighted regression baseline (Eq. 4).** The paper devotes Section 3.1 to arguing that the exp-weighted scheme (Eq. 4) suffers from an optimality-stability trade-off, loss explosion, and inefficient learning. The dichotomous decomposition is presented as the solution to these precise problems. Yet the experiments include no baseline that trains a diffusion policy using Eq. (4) — neither with clipping (as used in practice by IQL/AWAC-style methods) nor without. This is the single most relevant ablation for the paper's core motivation. Without it, the reader cannot tell whether the dichotomous decomposition actually resolves the claimed limitations or whether simpler existing techniques (clipping, small β) suffice.

- **NAVSIM navtest evaluation protocol.** The headline +6.5 PDMS improvement on navtest (DP-VLA w/ DIPOLE navtest, 94.8) trains on the test split, which is not the standard held-out evaluation protocol. While the paper acknowledges this and also reports a standard navtrain result (+1.4, 89.7), the "substantial" 6.5-point gain that drives the narrative (line 225) uses a non-standard protocol where training and evaluation splits overlap. Additionally, DPPO is only evaluated on navtest and not navtrain, making the comparison asymmetric and preventing a complete assessment of relative improvement.

### Minor

- **Unsupported claim about CFGRL.** Line 119 states CFGRL "lacks theoretical backing" without providing argument or citation. The claim that CFGRL's design "limits greediness" is offered as an explanation for DIPOLE's superior performance, but no experiment isolates this factor — DIPOLE differs from CFGRL in multiple aspects (sigmoid vs. indicator weighting, two separate models vs. conditional/unconditional, dichotomous decomposition), so the specific attribution is unfounded.

- **Inconsistent claim about adoption of exp-weighted scheme.** Line 72 states "we do not observe the adoption of this scheme in many recent diffusion-based RL methods," yet several cited works (Kang et al., 2023; Zheng et al., 2024) do use this scheme, creating a minor inconsistency.

### Trivial

None.

### Nice-to-Haves

- Add a brief sentence in Section 3.3 clarifying how A(s,a) is estimated (e.g., "following IQL, we use expectile regression to estimate V(s), and compute A(s,a) as the difference"), even if full details remain in the appendix. While the appendix contains this information and the main paper references it, a short clarification would improve self-containedness.
- Ablate the greediness factor ω across tasks to show sensitivity.
- Report DPPO on navtrain for symmetric comparison in Table 4.
- Report computational cost (training time, memory) of maintaining two diffusion models vs. one.

## Removed Points

- **Critic/advantage learning unspecified (originally framed as Fatal):** REMOVED per hard rule. The paper states G(s,a) is set to the advantage function (Section 3.3) and explicitly references Appendix C and D for implementation details. The parser stripped the appendix, which exists in the original submission. Deferring implementation details to an appendix is standard practice in RL papers. A weakened version is retained as a nice-to-have above.
- **Figure 2 assessment:** REMOVED — parser stripped figure images from the text; this is not an author error.
- **Section-by-section notes about FQL tying/beating DIPOLE on some individual tasks:** These are factual observations but do not constitute a weakness — DIPOLE wins or ties on most categories and significantly outperforms on others (e.g., cube-double: 29 vs 44).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add the exp-weighted regression baseline (Eq. 4) to Table 1.** Implement Eq. (4) with the same diffusion architecture, with and without weight clipping. This single ablation would directly validate or refute the paper's central motivation.
2. **Clearly separate the navtest result** into a distinct "in-domain fine-tuning" demonstration and clearly label the navtrain result as the primary held-out evaluation.
3. **Ablate ω** to show how the greediness factor affects performance across different tasks.
4. **Add a sentence in Section 3.3** briefly describing how A(s,a) is obtained (e.g., learned via expectile regression).

---

## Score and Decision

The paper's core theoretical contribution — the dichotomous decomposition and its connection to CFG — is genuinely novel and elegant. The evaluation is broad, and results are consistently positive. However, two significant evidential gaps prevent full confidence: (1) the absence of the exp-weighted baseline that the method is explicitly designed to improve upon, and (2) the strongest experimental result relying on a non-standard evaluation protocol. The mathematical insight is strong enough to warrant publication, but the empirical case needs strengthening.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>