The calibration tool is not accessible. I will proceed with my best judgment based on the thorough reading and analysis of the paper and reviewer inputs.

Let me now write the final consolidated review.

---

## Summary
This paper re-evaluates claims that programmatic RL policies generalize better OOD than neural policies, examining TORCS, KAREL, and PARKING benchmarks. It demonstrates that with simple modifications (cautious reward functions, providing the last action as input), neural policies match programmatic ones, arguing the reported gap stems from experimental confounds rather than representational differences. It introduces an expressivity + discoverability framework and identifies instance-scaling memory as the genuine regime where programmatic representations provide an advantage, supported by a proof-of-concept synthesizing BFS via FUNSEARCH.

## Strengths
1. **TORCS reward-function ablation (Section 4.1, Table 1):** Shows that reducing β from 1.0 to 0.5 in the intrinsic reward flips DRL from 0% OOD generalization (all seeds crashed) to 76% success on G-TRACK-2 and 69% on E-ROAD, with lap times competitive with NDPS (1:48 vs 1:40). This cleanly isolates the confound — the neural policy's ability to better optimize speed on the training track, not its representation — and directly falsifies the prior claim that programmatic policies generalize better for representational reasons in TORCS.

2. **KAREL result with feedforward + last action (Section 4.2, Table 2):** Demonstrates that "PPO with a_{t-1}" — a plain fully-connected network with the observation augmented by the previous action — achieves perfect 1.00 (0.00) average return on 100×100 grids for four of five KAREL tasks, matching or exceeding LEAPS (e.g., LEAPS gets 0.21 on TOPOFF 100×100 while PPO+a_{t-1} gets 1.00) and dramatically outperforming the LSTM baseline (which gets 0.00–0.04 on 100×100). This directly refutes the claim that programmatic representations are inherently better for KAREL generalization.

3. **Expressivity + Discoverability framework (Section 5, Definitions 2 & 3):** Introduces two crisp, composable conditions — (i) the policy space must contain a generalizing policy, and (ii) the search algorithm must find it — that disentangle representational limitations from optimization/algorithmic confounds. The framework cleanly explains all three re-evaluation results (TORCS: both spaces expressive, gradient search discovered the solution with a safer reward; KAREL: both spaces expressive, but LSTMs made discoverability hard; PARKING: both spaces struggled) and identifies the one case where expressivity itself fails (instance-scaling memory). This is a reusable conceptual tool beyond the paper's specific experiments.

4. **Information-theoretic argument for fixed-capacity limitations (Section 5):** Grounds the expressivity limitation in concrete reasoning: BFS requires maintaining a frontier and visited set of size Θ(|V|); indexing a vertex among |V| candidates requires Ω(log|V|) bits. Since feedforward and recurrent policies have fixed-sized hidden states independent of |V|, they provably cannot represent the needed algorithmic structures. This argument is precise and distinguishes the paper from vague claims about programmatic superiority.

5. **Honest treatment of ambiguous PARKING results (Section 4.3, Table 3):** The paper candidly reports that PARKING remains challenging for both representations: PSM's test Success Rate (0.16) is actually lower than DQN's (0.18), and only 2 of 30 PSM seeds solved all 100 test initial states. The paper concedes "PARKING is a challenging domain for both types of representation" and does not sweep this negative result under the rug, strengthening the credibility of the positive findings.

## Weaknesses

### Major

1. **Missing control undermines the TORCS confound claim (Section 4.1).** The paper changes β from 1.0 to 0.5 and interprets the resulting neural generalization as evidence that the original gap was a confound. However, changing β changes the training objective — with β=0.5, the agent optimizes for slower, safer driving. The paper does **not** run NDPS with β=0.5, which is the necessary control: would programmatic policies trained with the cautious reward also behave differently? The paper's own discussion (Section 4.4) conjectures "NDPS and PROPEL would not generalize to OOD problems if they could find better optimized policies," but this is precisely the counterfactual the experiment should test. Without this control, the TORCS result is consistent with two interpretations: (a) the gap was a confound (paper's preferred reading), or (b) both representations fail when optimized for the same objective, and programmatic policies' advantage was that they were *harder to over-optimize* for speed — a representational property, not a confound. The paper cannot distinguish between these without the missing control.

2. **Proof-of-concept for the positive contribution is too thin (Section 5).** The paper claims that programmatic representations provide a genuine advantage for problems requiring instance-scaling memory, but the supporting evidence is minimal: three runs of FUNSEARCH with Qwen 3-Coder (30B) returning a correct BFS implementation. No success rate, variance, or prompt sensitivity is reported. More critically, FUNSEARCH uses a large language model pre-trained on code that includes BFS implementations — the paper does not control for the possibility that the LLM is simply retrieving a memorized algorithm rather than demonstrating any inherent advantage of programmatic representations. There is no neural baseline with comparable external memory (e.g., stack-RNN, neural Turing machine, transformer with scratchpad) attempting the same task. The comparison is FUNSEARCH+LLM vs. feedforward/LSTM, which is not a fair test of the paper's stated thesis ("programmatic representations can express such solutions"). This weakness is consequential because the paper's claim about "when programmatic representations provide an inherent OOD generalization advantage" (Abstract) rests heavily on this experiment.

### Minor

3. **KAREL HARVESTER task remains unsolved (Table 2).** PPO with a_{t-1} scores 0.04 (0.00) on HARVESTER 100×100 — effectively a failure, similar to all other baselines. The abstract's claim that "neural policies... can match or exceed the OOD generalization of programmatic policies" is accurate for this case (LEAPS also scores 0.00), but the broader narrative of neural policies matching programmatic ones does not hold uniformly across the KAREL suite.

4. **Selective reporting in TORCS (Table 1 caption).** Generalization results are reported only for seeds that "learned to complete laps" on the training track (13/30 for G-TRACK-1, 4/15 for AALBORG). More than half of seeds failed to learn the training task. The paper does not report what fraction of NDPS or DRL (β=1.0) seeds succeeded on training, making it impossible to compare selection rates across conditions. The generalization results come from a self-selected subset of all seeds, and we cannot assess whether the same selection process applies to all methods.

5. **No LEAPS baseline with last-action augmentation (Section 4.2).** The paper shows that PPO with a_{t-1} outperforms the LEAPS baseline on KAREL, but does not test whether LEAPS would also benefit from the same last-action augmentation. This would be a natural control: if LEAPS also improves with this modification, the advantage is not about programmatic vs. neural representation but about observation design.

### Trivial

6. **Inconsistent variance reporting (Table 1).** Standard deviations are reported for DRL (β=0.5) but not for the NDPS and DRL (β=1.0) columns, making direct comparison of variability impossible.

## Nice-to-Haves
- Run NDPS with β=0.5 on TORCS to distinguish between the confound interpretation and the "harder-to-over-optimize" alternative.
- Include a neural memory-augmented baseline (stack-RNN, neural Turing machine) on the wall-sparse KAREL maze to provide a fair comparison for the proof-of-concept.
- Report seed success rates on training for all conditions in TORCS (NDPS, DRL β=1.0, DRL β=0.5).
- Test LEAPS with the last-action augmentation for KAREL.
- Either substantially expand the FUNSEARCH experiment (more runs, variance, prompt sensitivity, ablation of LLM pre-training knowledge) or appropriately temper the claims about it.

## Removed Points
- The harsh critic's claim that the TORCS β change "conflates changing the objective with controlling confounds" in a fatal way is downgraded to Major because (a) the paper explicitly justifies the reward as intrinsic (evaluation uses different metrics — lap time and crashes), and (b) the finding is still informative even without the NDPS β=0.5 control. The critic's alternative interpretation ("both representations fail similarly") is a plausible alternative, not a refutation.
- The harsh critic's claim about the LSTM analysis being "vague" is a presentational preference, not a weakness; the paper's empirical result (PPO with a_{t-1} works) stands on its own regardless of whether the explanation for LSTM failure is fully fleshed out.
- The harsh critic's concern about "expressivity is not proved for KAREL" and "Definition 3's time limit is vague" are removed because the framework is intended as a conceptual tool, not a formal verification system.
- The harsh critic's concern about "figure references broken" is a formatting artifact from PDF extraction.
- The Strength Finder's claim about the FUNSEARCH proof-of-concept being a strength is removed because it conflicts with the verified weakness that this experiment is too thin to support the weight placed on it (weakness wins over strength per filtering rules).

## Novel Insights
None beyond the paper's own contributions. The paper's central insight — that prior claims of programmatic generalization advantages in TORCS, KAREL, and PARKING can be explained by confounds (reward design, observation sparsity, architecture choice), and that the genuine advantage lies in problems requiring instance-scaling memory — is well-articulated by the paper itself. The reviews do not surface a novel observation beyond this.

## Suggestions
1. **Add the NDPS β=0.5 control for TORCS.** This single experiment is the highest-leverage improvement. If NDPS with β=0.5 also generalizes, the confound story is strongly supported; if NDPS with β=0.5 behaves differently, the paper would need to substantially revise its central claim about TORCS. Either outcome advances science.

2. **Expand or temper the FUNSEARCH proof-of-concept.** Either (a) add neural memory baselines (stack-RNN, transformer scratchpad) on the wall-sparse maze and report proper statistics, or (b) explicitly acknowledge that the experiment is only suggestive and that the theoretical Ω(log|V|) argument is the paper's main contribution regarding memory-scaling — not the FUNSEARCH result.

3. **Report seed success rates on training for all conditions in TORCS** and provide consistent variance reporting across all Table 1 cells.

4. **Test LEAPS with last-action augmentation** as a control for the KAREL experiment.

5. **Add a caveat about HARVESTER** to the abstract or introduction to avoid overclaiming.

## Score and Decision
Given the paper's strengths — particularly the clean TORCS and KAREL re-evaluations and the useful expressivity/discoverability framework — and its weaknesses — particularly the missing NDPS β=0.5 control and thin proof-of-concept — I place this paper in the borderline-accept to accept range.

The paper makes two genuinely useful contributions: (1) a much-needed critical re-examination showing that prior claims of programmatic generalization advantages were confounded, with strong empirical evidence in two of three domains, and (2) a clear conceptual framework and theoretical argument for when programmatic representations actually help. The missing NDPS β=0.5 control is the most significant weakness, as it leaves the TORCS finding open to an alternative interpretation. However, the paper's overall thesis is well-supported by the combination of the TORCS result (even imperfect), the stronger KAREL result, and the framework.

The paper's conceptual contribution (framework + memory-capacity argument) is its strongest aspect and does not depend on the experiments being perfect. The experimental weaknesses are fixable, and the paper would benefit from one more round of revisions to address them.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>