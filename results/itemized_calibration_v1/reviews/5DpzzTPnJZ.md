## Summary

This paper studies plasticity loss in deep RL through an optimization lens. It proposes that plasticity loss stems from two mechanisms: NTK rank degeneration (echoing prior work) and gradient magnitude decay. The key theoretical result (Theorem 3) identifies a Θ(1/k) gradient decay factor for FQI with a growing replay buffer. The paper then proposes Sample Weight Decay (SWD), which weights replay buffer sampling by recency to counteract this decay, and evaluates it across MuJoCo/TD3, ALE/Double DQN, and DMC/SAC.

## Strengths

1. **A concrete theoretical result in a largely empirical area.** Theorem 3 provides a structured gradient decomposition showing that when the replay buffer grows linearly (|D_h^k| = k), the gradient at the initialization of each FQI round contains a 1/k factor from the distributional-shift term. Identifying this specific decay structure is a genuine theoretical contribution.

2. **Consistent and non-trivial empirical performance gains across diverse settings.** The return curves (Figures 2, 3, 4) show SWD improves learning across TD3+MuJoCo, Double DQN+ALE, and SAC+SimBa+DMC. The use of IQM with stratified bootstrap CIs (Agarwal et al., 2021) is appropriate. The reverse ablation (SWA — weighting older data more) provides a useful sanity check that the weighting direction matters.

3. **Methodological simplicity and broad applicability.** SWD is a lightweight, plug-and-play weighting scheme that can be added to any experience-replay-based algorithm without architectural changes.

## Weaknesses

### Major

1. **The GraMa plasticity evidence is internally contradictory (verified from the text).** Section 6.3 states: *"Notably, a larger GraMa value indicates a weaker learning capability of the neural network."* The Figure 6 caption states: *"In all cases, SAC+SWD maintains a higher GraMa value than SAC."* Section 6.3 then claims SWD *"effectively alleviates the gradient sparsity."* These three statements cannot all be true simultaneously: if higher GraMa = weaker learning capability, then SWD having higher GraMa than SAC means SWD has weaker learning capability — directly contradicting the claim that SWD mitigates plasticity loss. The paper must either correct the GraMa interpretation, correct the reported GraMa values, or explain why this apparent contradiction does not invalidate the plasticity evidence. This undermines the paper's central mechanistic claim that SWD alleviates plasticity loss.

2. **The theoretical framework assumes a growing replay buffer, while the method is evaluated on fixed-capacity buffers, with no bridge between them.** Proposition 1 and Theorem 3 depend on the assumption |D_h^k| = k (buffer grows with episodes). The 1/k gradient decay structure in Theorem 3 is a direct consequence of this growing-buffer assumption. However, SWD is evaluated on TD3, SAC, and Double DQN, which all use fixed-capacity replay buffers (typically 1e6). Once the buffer is full, the empirical distribution is a rolling window whose update no longer follows the 1/k scaling. The paper neither acknowledges this discrepancy nor provides any analysis showing a qualitatively similar gradient decay occurs under fixed-capacity buffers. This weakens the claim that SWD is a "theoretically grounded" or "principled" method for the actual evaluation setting.

### Minor

3. **No formal proof that SWD restores gradient magnitude.** The paper claims SWD *"neutralizes the 1/k attenuation, restoring gradient magnitude"* (Section 5) but provides no theorem or lemma establishing this. Theorem 3 characterizes the gradient under uniform sampling at the FQI initialization point. SWD modifies the sampling distribution. No formal connection is made between these two objects. The conceptual argument (re-weighting recent data increases their gradient contribution) is reasonable but falls short of the paper's "principled" framing.

4. **The orthogonality claim is unsupported by the data.** The paper claims SWD is orthogonal to existing methods and presents SWD+S&P as evidence. However, Figure 8 shows SWD alone and SWD+S&P achieving essentially identical scores (~240 on Median, IQM, Mean). SWD alone already matches the combined method's performance. This shows dominance by SWD, not synergy. The claim of orthogonality is at best unsubstantiated.

5. **Hyperparameter sensitivity analysis is relegated entirely to the appendix.** The two core SWD hyperparameters (T and w_min) are central to the method's behavior, but the main text offers only a brief mention directing readers to appendix tables. A summary of the sensitivity analysis would improve accessibility and assessment of robustness.

### Trivial

6. Some presentation aspects (computational overhead discussion, placement of the bucket-based approximation description) could be improved, but these do not affect the technical evaluation.

## Nice-to-Haves

- Comparing SWD against simpler recency-biased alternatives (e.g., a smaller replay buffer, FIFO discard) would help isolate whether the specific linear weighting scheme drives the improvement or whether any form of recency bias suffices.
- The bucket-based approximation for computational efficiency (mentioned in Section 6.6) would be better placed in the main method section, as it addresses a practical concern for large buffers.

## Removed Points

The following points from the input review were removed per the filtering rules, with brief justification:

- "The sentence about LLM post-training 'breaking the Turing test' is unnecessary and imprecise" → Removed as a style/formatting nitpick; parser artifact.
- "Proposition 1 is a straightforward algebraic identity" → Not a weakness; the paper uses it as a technical building block.
- "Theorem 2 resembles standard results" → The paper does not claim Theorem 2 as a novel contribution; it provides framing context.
- "NTK degeneration section restates known results" → The paper frames this section as context for the less-explored gradient decay mechanism, not as a novel result.
- "PER is not a direct competitor" → Including PER as a baseline is informative; outperforming it is not a weakness of the paper.
- Criticisms based on missing appendix content (missing proofs, missing tables, missing references) → These sections exist in the original submission but were stripped by the parser.

## Novel Insights

The reviewer's identification of the GraMa contradiction is a genuine finding — the paper itself does not surface or address this inconsistency. The contradiction (higher GraMa for SWD, yet higher GraMa is said to indicate weaker learning capability) is directly verifiable from the published text but is not reconciled or even acknowledged by the authors.

## Suggestions

1. **Resolve the GraMa contradiction.** Correct the stated interpretation of the metric, correct the Figure 6 reporting, or explain how a higher GraMa value for SWD is consistent with improved plasticity under the metric's definition. This is the most urgent fix.

2. **Acknowledge the growing-buffer vs. fixed-capacity gap.** Discuss how the 1/k decay intuition does or does not carry over to fixed-capacity replay buffers, and provide analysis or empirical evidence for the claim that a similar gradient decay occurs in the evaluated setting.

3. **Either provide evidence of synergy for SWD+S&P (a statistically significant improvement over SWD alone) or drop the orthogonality claim.**

---

## Calibration Evidence

All retrieved anchors are listed below. The most comparable are those on plasticity loss in RL.

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `DnBjhWLVU1.md` — Recovering Plasticity via SWR | 4.00 | R1 | Yes | Weaker experiments (VGG only, small-scale), limited novelty; this paper is stronger empirically but has the GraMa contradiction. |
| `QmXfEmtBie.md` — Stay Hungry, Keep Learning | 5.25 | R1 | Yes | Limited to PPO only; this paper covers more algorithms but has the GraMa issue. |
| `20qZK2T7fa.md` — Neuroplastic Expansion | 6.50 | R1 | Yes | Novel, well-motivated, extensive experiments; criticized for lacking math rigor. This paper has math but a significant internal contradiction. |
| `NIkfix2eDQ.md` — Plastic Learning with Deep Fourier Features | 6.20 | R1 | Yes | Strong theory, novel method; criticized for small-scale experiments. |
| `KIq6p9iv2q.md` — Towards Perpetually Trainable | 5.75 | R1 | Yes | Thorough analysis but misleading conclusions and missing experimental details. |
| `bKswCSYkKq.md` — Neuron-level Balance | 3.00 | R1 | Yes | Very limited experiments (2 task sequences), low novelty; this paper is clearly stronger. |
| `kf9phcBvQ5.md` — Replay can provably increase forgetting | 3.00 | R1 | No | Continual learning theory; different setting but similar score tier. |
| `sKPzAXoylB.md` — Addressing Loss of Plasticity | 5.25 | R1 | No | Addresses both forgetting and plasticity; accepted at 5.25. |
| `OMVFYTgj0H.md` — Continual RL by Reweighting Bellman Targets | 3.67 | R1 | No | Related (weighting in RL) but different mechanism. |

**Bracket reasoning (Round 1):** The paper's experimental breadth and concrete theoretical result place it above the 3.00–4.00 anchors (which were limited by narrow experiments or low novelty). However, the verified GraMa contradiction — an internal inconsistency in the central plasticity evidence — is a heavier penalty than any single weakness in the 5.25–5.75 anchors (which were criticized for limited scope or missing baselines, not contradictions). This places the paper between 4.00 and 5.25.

**Final placement:** The closest anchor is "Recovering Plasticity via SWR" (4.00), which had *-4 weights for limited experiments and limited novelty* but no internal contradiction. This paper avoids those weaknesses (strong experiments, genuine theory) but accumulates a comparable penalty from the GraMa contradiction (weight ≈ -4). The next anchor "Stay Hungry, Keep Learning" (5.25) was penalized mainly for being PPO-only (-5) — this paper avoids that but has the contradiction. The balance yields a score of **4.5**.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>