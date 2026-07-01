## Summary

This paper studies plasticity loss in deep RL, attributing it to two mechanisms: NTK rank collapse and gradient magnitude decay (Θ(1/k)). The authors propose Sample Weight Decay (SWD), a method that assigns higher sampling probabilities to recent experiences in the replay buffer. Experiments across MuJoCo, ALE, and DMC environments with TD3, DDQN, and SAC show consistent IQM improvements of 13.7%–30.1%.

## Strengths

1. **SWD is simple, lightweight, and shows consistent empirical improvements.** The method requires only age-based weighting (Algorithm 1), making it easy to integrate. Experiments span three algorithm families (TD3, DDQN, SAC) and three environment suites (MuJoCo, ALE, DMC) with consistent positive results — a genuine practical contribution.

2. **The ablation studies are well-designed.** The SWA (reverse weighting) ablation convincingly demonstrates that recency direction matters: upweighting old data hurts performance, consistent with the intuition that recent data is more useful in non-stationary RL. The UTD experiment (Section 6.4) is particularly interesting — SWD shows the largest improvement (+30.1%) at UTD=5, where plasticity loss is most severe due to frequent gradient updates.

3. **Broad comparison against related plasticity methods.** The paper compares against ReGraMa, S&P, Plasticity Injection, and PER, showing SWD is competitive or better, and demonstrates orthogonality by combining SWD with S&P.

## Weaknesses

### Fatal

None.

### Major

1. **The theoretical framework assumes an ever-growing buffer, disconnected from the paper's own experiments.** Proposition 1 derives Θ(1/k) gradient decay by assuming |D_h^{k+1}| = k+1 — an ever-growing replay buffer. In practice, deep RL uses fixed-size replay buffers (standard capacity ~1e6). Once the buffer is full, the mixing coefficient for new data is 1/capacity, a constant, not 1/k. The paper never acknowledges this discrepancy. The claimed Θ(1/k) gradient decay that SWD is designed to "neutralize" does not describe the fixed-size buffer regime where all experiments operate. This breaks the claimed motivation for SWD.

2. **The GraMa metric definition contradicts its use, undermining the central plasticity claim.** Section 6.3 (line 232) states: *"a larger GraMa value indicates a weaker learning capability of the neural network."* Yet Figure 6 shows SAC+SWD achieves *higher* GraMa than SAC, and the paper claims this demonstrates SWD mitigates plasticity loss. Following the paper's own definition, higher GraMa would mean weaker plasticity. In Figure 5(c), SWA (worst-performing) has the *lowest* GraMa — following the paper's definition, SWA would have the strongest plasticity, yet it performs worst. The paper uses GraMa to argue both directions without reconciling them. This is not a minor wording issue; it confuses the central evidential claim.

3. **The "SOTA" claim on DMC Humanoid is unsupported.** The abstract and introduction claim "achieving SOTA performance on challenging DMC Humanoid tasks." The evidence consists only of comparisons against the SAC baseline and three plasticity-focused methods (ReGraMa, S&P, Plasticity Injection). No comparisons against established high-performing DMC methods (e.g., DrQ-v2, DreamerV2/V3, DMPO) are provided. Without these, the claim cannot be verified.

### Minor

4. **Theorem 3's Θ(1/k) result is only proven for the terminal step h=H.** The target-drift term in Equation 4 is eliminated "by setting f̂_{H+1} ≡ 0," which is valid only at the last horizon step (h=H). At all earlier steps h < H, the target-drift term is nonzero and its behavior is uncharacterized. The claimed Θ(1/k) decay is rigorously shown only for a single step of tabular FQI with an ever-growing buffer, not for the deep RL setting.

5. **Section 4.1 (NTK degeneration) is purely qualitative.** It contains no theorem, lemma, or bound — it observes that random initialization ensures NTK full-rankness (known) and that RL does not re-initialize (also known). The paper presents this as part of its "unified theory," but it does not constitute a theoretical result.

6. **SWD and SWD+S&P results in Figure 8 are reported at near-identical values** (~240 across Median, IQM, Mean, and ~80 for Optimality Gap for both). This either suggests S&P adds nothing on top of SWD (contradicting the claimed orthogonality/synergy) or is a rounding issue. Clarification is needed.

### Trivial

7. The bucket-based compute-efficient approximation for SWD is mentioned only briefly in the appendix; it deserves main-text placement.

## Nice-to-Haves

- Compare SWD against a "smaller replay buffer" baseline. If old data dilutes gradient signal, simply using a smaller buffer is a trivial alternative the paper should benchmark against.
- Discuss when SWD might hurt — overweighting recent data increases gradient variance, which could be harmful in settings with high reward noise.
- Clarify how the fixed-size buffer used in practice relates to the theoretical model.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"The 1/k factor is a trivial statistical identity"** — This is a subjective judgment about novelty/insightfulness, not a factual error. The substance is covered by Weakness 1 (buffer assumption disconnect).
- **"The connection between theory and SWD is circular"** — Reframed as Weakness 1, which captures the gap between theory and practice without pejorative framing.
- **"5 seeds is marginal"** — Common practice in RL; not a meaningful weakness for this domain.
- **Generic strengths** (e.g., "addresses an important problem," "this paper targets a real problem") — Removed as not specific to this paper's content.
- **Missing related works** — Removed per policy (cannot verify external sources).
- **Formatting/presentation nitpicks** — Removed per policy.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Resolve the GraMa contradiction** — Correct the definition at line 232 or reconcile the evidence presented in Figures 5 and 6.
2. **Acknowledge the buffer assumption gap** between theory (ever-growing) and practice (fixed-size) and explain why SWD still works in the fixed-buffer regime.
3. **Qualify or remove the SOTA claim** — Add proper comparisons against top DMC methods or limit the claim to "competitive with existing plasticity-focused methods."
4. **Clarify the SWD vs SWD+S&P results** in Figure 8 and explain whether S&P contributes additively on top of SWD.
5. **Consider reframing** the paper as primarily an empirical method contribution rather than a theoretical one — this would better match the evidence presented.

## Score and Decision

Calibration anchors used:

| Anchor | Score | Comparison |
|--------|-------|------------|
| KIq6p9iv2q ("Towards Perpetually Trainable") | 5.75 (Reject) | Similar topic, similar overclaiming issues. Our paper has broader experiments but a clearer self-contradiction (GraMa). |
| 20qZK2T7fa ("Neuroplastic Expansion") | 6.50 (Accept) | Stronger experimental validation with fewer internal contradictions. Our paper is weaker. |
| NIkfix2eDQ ("Plastic Learning with Deep Fourier Features") | 6.20 (Accept) | Solid theoretical backing; our paper's theory is weaker. |
| QmXfEmtBie ("Stay Hungry, Keep Learning") | 5.25 (Reject) | Similar topic and contribution level. Our paper has broader algorithm coverage but the GraMa error makes it comparable. |
| ffuHn3Q6Hc ("Reinitializing weights vs hidden units") | 5.33 (Reject) | Clear, simple method. Our paper has more complex framing but a self-contradiction. |
| bKswCSYkKq ("Neuron-level Balance") | 3.00 (Reject) | Limited experiments; our paper is clearly stronger. |
| HqmpIud9Uq ("Tackling Non-Stationarity") | 4.00 (Reject) | Unclear motivation and limited novelty; our paper has a cleaner method. |

**Round 1 bracket:** [4.0, 6.0]

**Narrowing rationale:** The paper has genuine empirical value (broader and cleaner than score-3 papers), but contains concrete errors — the GraMa self-contradiction and theory-practice disconnect — that papers at score 6+ typically avoid. The method itself is reasonable and well-tested, placing it above pure reject territory but below the strength needed for acceptance.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>