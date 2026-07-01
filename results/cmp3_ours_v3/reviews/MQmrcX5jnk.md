**Round 1 bracket:** 5.5–7.5  
**Round 2 narrowing:** The paper clearly exceeds BNEM (6.00, Reject) and NETS (6.25, Reject), both rejected for limited scaling and novelty concerns respectively — issues this paper does not share. It is empirically stronger than Neural Sampling from Boltzmann Densities (6.40, Accept), which only tested in 2D. It compares favorably to BoPITO (7.00, Accept) in empirical scope. The approximation gap and overclaimed abstract prevent it from reaching 7.0+.  
**Final score: 6.5**

---

## Summary

This paper introduces Constrained Mass Transport (CMT), a variational framework that constructs annealing paths by constraining both the KL divergence (trust-region) and the entropy decay between successive intermediate distributions. The authors derive closed-form optimal intermediate densities under these constraints (Propositions 2.1–2.3), characterize the induced annealing paths (Theorem 2.4), and instantiate the framework with normalizing flows. Evaluated on molecular Boltzmann generator benchmarks including a new ELIL tetrapeptide system (d=219), CMT consistently outperforms state-of-the-art methods like FAB and TA-BG across EUBO, ESS, and Ramachandran TV metrics, while using comparable or fewer target energy evaluations.

## Strengths

- **Clean theoretical derivations.** Propositions 2.1–2.3 derive closed-form intermediate densities for the trust-region, entropy, and combined constraints, and Theorem 2.4 characterizes the resulting geometric/tempered/geometric-tempered annealing paths. These analytical results are legitimate and constitute the paper's core theoretical contribution.
- **Strong and consistent empirical results.** Table 1 shows CMT achieves the best EUBO on all four systems, best ESS on all four, and best RAM TV on three of four. On the two largest systems (alanine hexapeptide d=180 and ELIL tetrapeptide d=219), ESS improvements over the strongest baseline (TA-BG) are roughly 1.6× and 1.9× respectively, with small standard errors across four independent runs.
- **Ablation study proves the joint value of both constraints.** Figures 2 and 3 show that omitting the trust-region constraint causes entropy collapse (Figure 2a), and only the combined geometric-tempered variant avoids mode collapse in the Ramachandran plots (Figure 3). This directly supports the paper's central thesis that both constraints are necessary.
- **Sample-efficient.** CMT achieves superior results with the same or fewer target energy evaluations than baselines, which is practically important because energy evaluations (especially from DFT) dominate computational cost.
- **New ELIL tetrapeptide benchmark (d=219).** This is the largest system studied to date under the setting of learning Boltzmann generators exclusively from energy evaluations without MD samples, and its inclusion meaningfully extends the evaluation.

## Weaknesses

### Fatal
None.

### Major

- **Approximation gap between exact theory and practical algorithm.** The theoretical framework (Section 2) derives optimal intermediate densities q_i with closed-form expressions (Propositions 2.1–2.3). The practical algorithm (Section 3) must approximate these with normalizing flows \hat{q}_i via forward KL minimization (13)/(15), acknowledging that "it is typically not possible to sample from [the exact densities] directly" (line 130). The paper does not analyze how well the flow approximation preserves the theoretical guarantees about overlap, mass teleportation avoidance, or constraint satisfaction. The claim about dimension-independent importance weight variance (line 144) is also deferred to Appendix C.3 without main-text justification. While the strong empirical results (Table 1, Figures 2–3) partially fill this gap, the paper would benefit from explicitly discussing this theory-practice distinction rather than treating the transition as seamless.

### Minor

- **Headline ESS claim is overstated.** The abstract states "achieving more than 2.5× higher effective sample size." Per Table 1, the improvement over the strongest baseline (TA-BG) on the two largest systems is ~1.6× (hexapeptide) and ~1.9× (ELIL). The 3.61× figure is against FAB on ELIL, which is a substantially weaker baseline on that system. The "2.5×" claim is not representative of typical gains against the strongest baselines.
- **RAM TV exception on the largest system.** On ELIL tetrapeptide, TA-BG achieves better RAM TV (0.0254) than CMT (0.0313). The paper qualifies this by noting TA-BG had only 2/4 successful runs, but the claim of "consistently surpasses" baselines should acknowledge this exception on the metric measuring distributional accuracy.
- **Fixed-number-of-steps protocol decouples theory from practice.** The paper uses a fixed number of annealing steps \tilde{T} (line 223) rather than the Lagrangian-based stopping criterion (λ=η=0), justified by fair benchmarking. The sensitivity of results to \tilde{T}, ε_tr, and ε_ent is deferred to Appendix B. Without main-text analysis, it is unclear how tuned these hyperparameters are and whether settings transfer across systems.
- **Variance-of-importance-weights claim lacks main-text support.** The claim that the trust-region constraint keeps importance weight variance "approximately constant, independent of the problem dimension d" (line 144) is potentially a major advantage, but is only supported by a reference to Appendix C.3 without any explanation in the main text.

### Trivial
None.

## Nice-to-Haves

- A wall-clock time comparison (not just target evaluations) would benefit practitioners, though the paper notes the dual optimization is only ~0.01% of training time on alanine dipeptide.
- Exploring alternative divergences (e.g., log-variance loss) beyond forward KL is mentioned as future work but would strengthen the practical instantiation.
- A brief main-text justification for the dimension-independent variance claim would help readers assess this claimed advantage.

## Removed Points

- **"Entropy-only constraint does not produce a transport path"** — REMOVED because the paper explicitly acknowledges this limitation (lines 96–97: the KL can be arbitrarily large; the combined constraint addresses it). The entropy constraint is presented as a building block for the combined approach, not a standalone method.
- **"Forward KL comparison is asymmetric (trained from MD samples)"** — REMOVED because the paper is transparent about this: Table 1 caption states "forward KL is trained from samples rather than from energy" and marks it as a reference method.
- **Generic formatting/presentation nitpicks** — REMOVED per filtering rules.

## Novel Insights

The most striking synthesis across the reviews is that while the paper's theoretical contribution (constrained optimization producing structured annealing paths) is elegant and self-contained, the practical significance hinges entirely on the empirical validation of the approximate flow-based instantiation. The gap between exact q_i and approximate \hat{q}_i is the central tension: the paper treats the transition from theory to algorithm as a standard implementation step, but it is actually the axis on which the strength of the entire contribution rests. The paper would be strengthened by explicitly acknowledging and discussing why the flow approximation preserves the benefits of the theoretically derived path, rather than presenting the transition as seamless.

## Suggestions

1. Address the approximation gap by either (a) providing bounds on how far \hat{q}_i can deviate from q_i under forward KL minimization, or (b) explicitly clarifying in the main text that the theoretical guarantees apply to the optimal path while the empirical results demonstrate the approximate path inherits these properties.
2. Tone down the "2.5× higher ESS" claim in the abstract to reflect gains against the strongest baselines (e.g., "up to 1.9× higher ESS than the best baseline, with larger gains on larger systems").
3. Include a brief sensitivity analysis of \tilde{T}, ε_tr, and ε_ent in the main text (or move key results from Appendix B to the main text) to establish that the method is robust to these choices.
4. Provide a short main-text justification for the dimension-independent variance claim about importance weights.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>