Now let me compile and write the final review.

**Calibration Anchors Summary:**

| Anchor | Path | Score | Round | Itemized? | Comparison |
|--------|------|-------|-------|-----------|------------|
| Q-Score Matching | StkLULT1i1 | 5.00 | 1 | Yes | Diffusion RL with score matching; weaker experiments (6 tasks), similar theoretical depth |
| SRPO | xCRr9DrolJ | 6.25 | 1 | Yes | Diffusion-based offline RL; some reviewers noted marginal empirical benefits |
| CFDG (O2O) | cXxfVkRCHJ | 3.00 | 1 | Yes | Offline-to-online RL + CFG; weaker theoretical contribution, limited novelty |
| DAC | ldVkAO09Km | 6.50 | 2 | Yes | Similar KL-constrained diffusion-policy method; strong D4RL results, comparable depth |
| EFM/QIPO | HA0oLUvuGI | 6.25 | 2 | Yes | Energy-weighted flow matching; some reviewers questioned novelty vs. known weighted regression |

**Bracket determination:** Round 1 placed the paper in the 4.0–7.0 band. The narrowest plausible bracket is 5.5–7.0 based on comparison with SRPO (6.25), EFM (6.25), and DAC (6.50).

**Narrowing:** DIPOLE's theoretical contribution (dichotomous decomposition → CFG) is cleaner than EFM's (criticized as "not particularly novel") and broader in scope than SRPO's (limited to efficiency gains). DIPOLE's experimental breadth (39 tasks + AD) exceeds both DAC and Q-Score Matching. However, DIPOLE's overclaiming on the w/o-rs vs. CFGRL comparison (favorability 2.89) and missing CFGRL baselines (3.29) are real weaknesses that drag it below the 7.0 threshold. The closest comparator is DAC (6.50), which has similar theoretical depth and strong D4RL results; DIPOLE has broader scope but less rigorous baseline coverage. Final score: 6.5.

---

## Summary

This paper proposes DIPOLE, a reinforcement learning algorithm for diffusion-based policies. It identifies a limitation in existing KL-regularized approaches — the unbounded exponential weighting term `exp(βG)` causes training instability — and replaces it with a bounded sigmoid weighting via a dichotomous policy decomposition. The optimal policy is decomposed into a positive policy (reward-maximizing) and a negative policy (reward-minimizing), whose score functions are combined linearly at inference time, analogous to classifier-free guidance. The method is evaluated on 39 offline RL tasks (ExORL, OGBench), offline-to-online settings, and scaled to a 1-billion-parameter VLA model for autonomous driving on NAVSIM.

## Strengths

- **Clean, principled theoretical contribution.** The paper correctly identifies a genuine limitation of exp-weighted regression for diffusion policies — unbounded weights causing training instability. Replacing the exponential with a sigmoid-bounded weight via the dichotomous decomposition (Eqs. 7–8) is mathematically sound and well-motivated. The derivation from the greedified KL-regularized objective (Eq. 5) through Theorem 1 to the final score combination (Eq. 10) is clear and correctly executed.

- **Insightful connection to classifier-free guidance.** Showing that the optimal policy's score function decomposes into `(1+ω)ε⁺ − ωε⁻`, formally analogous to CFG, provides both theoretical grounding and a natural mechanism for controllable greediness during inference. This is more than a superficial analogy — it follows directly from the derivation and is likely to be reused by future work.

- **Unusually broad experimental scope.** The paper evaluates on 39 offline RL tasks across ExORL and OGBench, provides offline-to-online results, and scales to a 1-billion-parameter VLA model for autonomous driving on NAVSIM. This breadth — especially the billion-parameter AD experiment — demonstrates scalability that few prior diffusion-policy RL works attempt.

- **Competitive results on RL benchmarks.** On ExORL (Table 1), DIPOLE achieves the best score on 7 of 9 tasks. On OGBench (Table 2), it achieves the best on 4 of 6 task categories (and near-best on the remaining 2). The offline-to-online results (Table 3) show meaningful improvement from offline pre-training to online fine-tuning.

## Weaknesses

### Fatal
None.

### Major

1. **DIPOLE w/o rs vs. CFGRL claim is overstated.** The paper states "*DIPOLE w/o rs* demonstrates better performance compared to *CFGRL*, highlighting the importance of our design for achieving more greedy policy optimization." The data in Table 1 does not support a claim of clear superiority: DIPOLE w/o rs wins on 5 of 9 tasks, CFGRL wins on 3 (Walker run, Cheetah run, Cheetah run-backward) by clear margins, and 1 task (Quadruped run) is within error bars. This is a draw, not a win. Since this comparison is central to arguing that the dichotomous decomposition itself (without rejection sampling) provides benefit over the closest prior work, the overstatement weakens what would otherwise be a supporting argument. *(Verified from Table 1: CFGRL 282±6 vs. DIPOLE w/o rs 256±12 on Walker run; CFGRL 216±15 vs. 194±9 on Cheetah run; CFGRL 262±26 vs. 227±7 on Cheetah run-backward; Quadruped run 571±25 vs. 560±11.)*

2. **NAVSIM comparison is asymmetric.** In Table 4, DPPO (the most natural diffusion-policy-RL baseline for this setting) is evaluated only on the navtest split (89.0 PDMS), not on navtrain. DIPOLE is evaluated on both navtrain (89.7) and navtest (94.8). Without DPPO navtrain results, we cannot fully assess whether DIPOLE's +1.4 navtrain improvement over the DP-VLA baseline (88.3→89.7) is matched or exceeded by DPPO on the same split. The paper should either provide DPPO navtrain results or explicitly frame the comparison as navtest-only and explain why. *(Verified from Table 4 and Section 4.2: DPPO row only reads "navtest" while DIPOLE has both "navtrain" and "navtest" rows.)*

### Minor

3. **CFGRL missing from OGBench and offline-to-online.** CFGRL (Frans et al., 2025) — the most closely related prior method, also using a CFG-style linear combination for diffusion policy improvement — appears in ExORL (Table 1) but is absent from OGBench (Table 2) and offline-to-online (Table 3). The paper does not explain why. Since CFGRL is discussed as a directly related approach in Section 3.2, its exclusion from two of three experimental settings is a gap. *(Verified: Section 4.1 baselines list CFGRL only in ExORL context; Tables 2 and 3 have no CFGRL column.)*

4. **Doubled model cost not acknowledged for RL benchmarks.** Section 3.2 specifies that positive and negative policies are trained "using two diffusion models" `ε⁺_{θ₁}` and `ε⁻_{θ₂}`. For the RL benchmarks, these are full diffusion models (unlike the AD section which uses LoRA). This roughly doubles parameter count, memory, and per-iteration training cost compared to methods like IFQL, FQL, or IDQL that train a single diffusion/flow model. The paper does not discuss this computational overhead anywhere. *(Verified: Eq. 9 uses two separate model parameters; no discussion of cost in the paper.)*

5. **Derivation assumes normalization constants cancel.** The step from Eq. (8) to Eq. (10) implicitly assumes the partition functions for π⁺ and π⁻ either cancel or are negligible when taking the score ratio. The paper does not discuss this. In practice, the score-ε connection in diffusion models handles this (since εθ learns the score of the *unnormalized* distribution), so this is not a fatal issue, but the derivation should note the assumption. *(Verified from Eq. 7–10 chain.)*

### Trivial
None.

## Nice-to-Haves

- A systematic ablation of the greediness factor ω on one or two ExORL tasks would better validate the "controllable greediness" claim. (The paper states ablations are in Appendix D.4, which is stripped by parsing.)
- A direct comparison between DIPOLE (w/o rs) and training with the original exp-weighted regression loss (Eq. 4) — using the same architecture, critic, and data — would be the cleanest test of the paper's central hypothesis that sigmoid weighting resolves instability. The paper criticizes exp-weighted regression but never runs it as a baseline.

## Removed Points

These points were raised in the input reviews but removed for the following reasons:

1. **Criticism that the greedified objective (Eq. 5) is "constructed, not derived"**: Removed — this is a subjective framing preference, not a verifiable weakness. The paper transparently provides the full derivation. No mathematical error or omitted principle is identified.

2. **Criticism about "we do not observe the adoption of this scheme" (line 72)**: Removed — the claim is about adoption frequency, not existence. Citing works that use the scheme does not contradict the claim.

3. **Request for ω ablation and critic learning details**: Removed — the paper states these are in the appendix (D.4, C/D), which is stripped by parsing. No verification possible.

4. **Criticism that the method is "not novel" or "just weighted regression"**: Removed — this is contradicted by the paper's actual contribution (dichotomous decomposition enabling stable training with bounded weights + CFG connection).

## Novel Insights

The central insight from the reviews is that the DIPOLE w/o rs vs. CFGRL comparison in Table 1 is more nuanced than the paper presents — a 5/4 task split favoring DIPOLE marginally does not support the paper's claim of clear superiority for the dichotomous decomposition alone. This matters because it directly tests whether the core algorithmic novelty provides benefit beyond CFGRL without the confound of rejection sampling. A fairer characterization would note that DIPOLE w/o rs shows *comparable or slightly better* performance to CFGRL, not outright superiority. The second key finding is the asymmetric NAVSIM comparison, where missing DPPO navtrain results reduces the informativeness of an otherwise impressive AD scaling demonstration.

## Suggestions

1. Either soften the "DIPOLE w/o rs vs. CFGRL" claim to reflect the mixed results, or add aggregate/statistical significance analysis across tasks.
2. Evaluate DPPO on the navtrain split to complete the NAVSIM comparison.
3. Add CFGRL to OGBench and offline-to-online experiments, or explain why it was excluded.
4. Acknowledge the computational overhead of training two diffusion models in a limitations paragraph.
5. Add a note about the normalization constant assumption in the transition from Eq. (8) to Eq. (10).

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>