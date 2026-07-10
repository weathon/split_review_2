## Summary

This paper proposes Generative Trajectory Policies (GTP) for offline RL, built on a unified ODE framework that connects diffusion, flow matching, consistency models, and CTMs as instances of learning a continuous-time solution map Φ. GTP learns the full ODE solution map and introduces two key adaptations for offline RL: a score approximation (Theorem 1) that avoids costly ODE integration during training, and an advantage-weighted training objective (Theorem 2) for value-guided policy improvement. Empirically, GTP achieves strong results on D4RL Gym and AntMaze benchmarks, including notably strong BC performance on long-horizon AntMaze tasks.

## Strengths

- **A clean unifying ODE framework (Section 3).** The paper formalizes diffusion, flow matching, consistency models, CTMs, shortcut models, and mean flows as instances of learning the solution map Φ of a continuous-time ODE. The two-component training (instantaneous flow loss as local anchor + trajectory consistency loss as global regulator) provides a genuinely useful conceptual lens. The table in Section 3.4 showing how each prior model instantiates these losses is informative and well-structured.

- **Theorem 1 provides formal backing for a practical training trick.** Replacing the score (which would require ODE solving) with the closed-form surrogate \(\tilde{f}(\mathbf{x}_t,t)=(\mathbf{x}_t-\mathbf{x})/t\) and showing the two training objectives differ by only \(O(h^p)\) is a clean theoretical result that justifies a real computational saving. This is the paper's clearest technical contribution.

- **Strong BC results on AntMaze (Table 1).** GTP-BC achieves 66.3 average on AntMaze versus 44.1 for the next-best generative BC method (C-BC). The gap on antmaze-medium-diverse (85.0 vs. 31.6) is genuinely striking and suggests that trajectory-level modeling provides a meaningful inductive bias for capturing long-horizon, temporally extended behaviors.

## Weaknesses

### Fatal
None.

### Major

- **Factual misrepresentation in headline claims.** The abstract states GTP achieves "perfect scores on several notoriously hard AntMaze tasks" and the introduction repeats this claim. However, Table 2 shows exactly one perfect score (100.0) on antmaze-umaze. All other AntMaze tasks are well below 100. The paper's own discussion in Section 5.2 correctly notes only the umaze task reaches 100.0. The term "several" implies multiple; this is a factual error in the paper's most prominent empirical claim and must be corrected. (Lines 9, 27 vs. Table 2)

- **Novelty oversold relative to CTM.** The core formalism — learning the full solution map Φ, the reparameterization φ(x_t,t,s) from Eq. (3) (credited as "inspired by (Kim et al., 2024)"), and the two training objectives (instantaneous flow + trajectory consistency) — is directly inherited from Consistency Trajectory Models. The paper itself acknowledges that "CTMs instantiate both core components of our unified framework" (Section 3.4). Yet GTP is repeatedly framed as "a new and more general policy paradigm" (lines 25, 351). The RL-specific contributions are: (a) the score approximation (Theorem 1) and (b) advantage-weighted training (Theorem 2). Theorem 2 is a standard KL-regularized RL result that appears in prior work going back to Peters & Schaal (2007) and is used in offline RL methods such as MPO, AWAC, and IQL. Presenting it as a "theorem" that "confirms that exponential advantage weighting is the theoretically correct way to incorporate value guidance into generative training" overstates its novelty.

- **Expressiveness-efficiency trade-off not properly evaluated despite being the paper's central claim.** GTP uses K=5 inference steps — the same as the diffusion policies it seeks to improve upon (line 259). Consistency policies use K=2. The paper never reports: (a) GTP's performance with K=1 or K=2 steps to verify it can match consistency models at low step counts, (b) wall-clock inference time comparisons between GTP, D-QL, and C-AC, or (c) training time comparisons with D-QL and C-AC (only an internal ablation vs. the ODE-solver variant is reported in Table 3). The conclusion admits "reducing the substantial training time of this model class remains an important avenue for future research," which undercuts the efficiency framing. Without evidence that GTP works competitively at fewer steps than diffusion, the central motivating claim is unsupported.

### Minor

- **Missing baseline results not explained.** In Table 2, C-AC scores for antmaze-medium-diverse, antmaze-large-play, and antmaze-large-diverse are shown as "—". BDM scores for the large AntMaze tasks are also "—". The paper does not explain why these entries are missing, which could raise concerns about selective reporting.

- **Zero variance on antmaze-umaze not discussed.** Achieving 100.0 with std=0 across 5 random seeds on a stochastic simulation environment is unusual and warrants explanation. The paper does not address this.

- **Ablation limited to one task.** Table 3 evaluates the ablation only on hopper-medium-expert. While the results are informative, showing that the score approximation saves ~1 hour of training time and improves score by ~12 points, the generality of these conclusions across tasks is unclear.

### Trivial
None.

## Nice-to-Haves

- Add experiments varying inference step counts (K=1, 2, 5, 10) for GTP vs. D-QL and C-AC to directly substantiate the expressiveness-efficiency claim.
- Report wall-clock inference time and training time compared to D-QL and C-AC.
- Include a brief discussion of the std=0 result for antmaze-umaze.
- Consider evaluating on additional D4RL domains (Adroit, Kitchen) if feasible.

## Removed Points

These points from the input review were filtered or merged:

- **Critic's objection to Table 1 including non-generative BC baselines:** Removed. The asymmetry favors the author's method (baselines are used in a setting they weren't designed for), so it does not constitute unfair comparison against the author. The relevant generative BC comparisons (D-BC, C-BC) are fairly presented and GTP-BC outperforms them.
- **Critic's claim about Eq. (17) target not being a valid ODE trajectory:** Removed. The paper explicitly justifies this via Theorem 1's score approximation; the critic's concern about degradation with larger step sizes is speculative without empirical evidence.
- **Critic's note about missing empirical analysis of score approximation error:** Removed. The ablation in Table 3 provides empirical comparison between the approximation and ODE-solver variants.
- **"Limited domain coverage" (no Adroit/Kitchen):** Removed. D4RL Gym + AntMaze evaluation is standard in offline RL generative policy papers.
- **Critic's formatting/style nitpicks and reproducibility concerns:** Removed per filtering rules.

## Novel Insights

None beyond the paper's own contributions. The reviewer analysis surfaces the factual error in the abstract's "several perfect scores" claim and the gap between the novelty framing and the actual CTM inheritance, but these are standard review observations rather than novel insights.

## Suggestions

1. **Correct the factual error:** Replace "perfect scores on several notoriously hard AntMaze tasks" with an accurate description (e.g., "a perfect score on antmaze-umaze and strong performance on the remaining AntMaze tasks").
2. **Recalibrate novelty claims:** Position GTP as "an adaptation of CTM to offline RL with two practical innovations" rather than "a new policy paradigm."
3. **Add step-variation experiments:** Test GTP at K=1, 2, 5, 10 inference steps alongside D-QL and C-AC to substantiate the expressiveness-efficiency trade-off claim.
4. **Explain missing baselines:** Add a note on why C-AC and BDM entries are absent for certain AntMaze tasks.
5. **Discuss the std=0 result:** Briefly address the zero-variance perfect score on antmaze-umaze.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>