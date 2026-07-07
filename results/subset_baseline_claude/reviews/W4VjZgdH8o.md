## Summary

This paper applies Decision Transformer (DT) variants—specifically Critic-Guided Decision Transformer (CGDT) and Online Decision Transformer (ODT)—to the Gym-µRTS real-time strategy environment. The authors combine both into a novel Online Critic-Guided Decision Transformer (OCGDT) by simply summing the CGDT and ODT loss terms. A dataset of 3,000 trajectories is collected from competition-winning rule-based bots. The agents are benchmarked against rule-based bots and IQL, showing comparable win rates with fewer gradient update steps.

## Strengths

- **Non-trivial environment adaptation**: Gym-µRTS uses a large multi-discrete action space with per-step invalid action masking. The authors handle this carefully—e.g., dynamically recalculating the ODT entropy lower bound at each step based on the mean number of valid actions over the last K steps—which is a genuine engineering contribution.
- **Multi-budget IQL comparison**: Comparing OCGDT to three IQL variants trained at equal gradient steps, equal wall-clock time, and equal sample counts (Table 1) is methodologically thorough and honest. It avoids cherry-picking favorable comparisons.
- **Ablation breadth**: The 7 ablations (A–G) systematically explore context length, buffer management, and training duration, providing useful insights about fine-tuning stability and overfitting under data scarcity.

## Weaknesses

### Fatal
None.

### Major

- **The central combination (OCGDT) does not deliver meaningful gains**: Ablation D (OCGDT without online fine-tuning) performs on par with or better than OCGDT itself against every bot (23.0% vs 26.2% against CoacAI—overlapping confidence intervals; 43.3% vs 40.1% against Mayari). The online fine-tuning component, which is the primary novel element of OCGDT over CGDT, provides no statistically significant benefit and is sometimes detrimental. The paper acknowledges this but still presents OCGDT as the headline contribution.

- **Thin algorithmic novelty**: OCGDT's derivation (Eq. 11) is a trivial linear combination of existing loss terms from ODT and CGDT with no theoretical motivation for why this combination should work better, and empirically it does not. The combination is not informed by any structural insight about the two methods' interaction.

- **Misleading sample-efficiency framing**: The paper claims DT requires "fewer gradient updates (≤13,000 vs ≥400,000)" than IQL to match performance. However, DT with K=100 and batch size 32 processes 3,200 token-steps per update, meaning OCGDT actually consumes 25.6M samples total—while the closest IQL comparison (IQL 13k at 13,000 gradient steps × 32 = 416,000 samples) performs far worse. The DT efficiency advantage largely disappears under equal-sample comparison, and the paper's framing obscures this.

### Minor

- The cross-agent win rates in Table 2 show OCGDT's advantage over IQL 800k is 51.6% ± 4.9%—statistically indistinguishable from 50%. The claims of OCGDT "matching" or "beating" IQL should be tempered by confidence interval analysis throughout.
- The learned behavior analysis (Section 5.2) describes a "pocket" survival exploit but does not assess whether this is a robust strategy or an artifact of the narrow evaluation bot set.

### Trivial
None worth noting.

## Nice-to-Haves

- A sweep over dataset quality (e.g., mixed data from weaker bots) would clarify whether CGDT's critic guidance is beneficial specifically in low-data or low-quality-data regimes as theoretically motivated.
- Reporting training curves (win rate vs. training step) during the online phase for OCGDT and OCGDT-D would strengthen the claim about fine-tuning degradation timing.

## Novel Insights

The ablation findings contain a practically useful observation: when an offline-pre-trained DT-based policy is fine-tuned online, the replay buffer pollutes rapidly with suboptimal early-exploration trajectories, causing degradation; preserving the offline buffer by increasing total buffer size (OCGDT C) mitigates but does not eliminate this issue, and the agent's generalization after offline training alone (OCGDT D) is already near its fine-tuned ceiling. This concretely suggests that for DT methods in sparse-reward strategy games, online fine-tuning requires either a higher-quality initial policy or curriculum-controlled exploration to be productive—a negative result with practical value for the community.

## Suggestions

- Reframe the paper around the negative result: online fine-tuning of DT in sparse-reward RTS environments does not help, and analyze why (e.g., trajectory return distribution shift, non-stationarity of the opponent during self-play collection).
- Provide a rigorous statistical comparison (e.g., two-proportion z-test or bootstrap) in Tables 1 and 2 to avoid overstating win-rate differences within the margin of error.

## Score and Decision

The paper is an honest, well-executed applied study with carefully designed ablations and fair multi-budget comparisons. However, the proposed OCGDT combination delivers no measurable improvement over its constituent parts, the sample-efficiency framing is misleading, and the algorithmic novelty is limited to a one-line loss summation. The contribution is better suited to a workshop on offline/game RL than a top venue.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>