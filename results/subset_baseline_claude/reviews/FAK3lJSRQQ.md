## Summary
ExLLM is an LLM-as-optimizer framework for large discrete optimization problems, particularly molecular design. It introduces three components: (1) a compact, evolving "experience snippet" that distills non-redundant optimization cues instead of retrieval-style memory, (2) a k-offspring scheme that samples multiple candidates per LLM call by exploiting autoregressive factorization, and (3) a feedback adapter for normalizing multi-objective signals and formatting constraints. The method achieves a new PMO aggregate score of 19.165 (+7.3% over previous SOTA MOLLEO) and transfers to domains including circle packing, stellarator design, routing, peptide design, and GPU kernel optimization.

---

## Strengths

- **Strong, well-supported PMO benchmark results:** ExLLM scores 19.165 vs. the previous best 17.862, ranking first on 17/23 tasks with multiple seeds and clear standard deviations reported. The ablation "ExLLM w/o experience" reaching 18.165 further decomposes the contributions.
- **Fair baseline comparison within the 5-objective setting:** Both ExLLM and MOLLEO use the same backbone (GPT-4o-2024-05-13), and three controlled initializations (best/random/worst) are used to isolate method contribution from initialization luck.
- **Compelling empirical critique of retrieval-style memory (Table 1):** The controlled ablation showing retrieval-style memory causing uniqueness collapse (<10%), prompt cost explosion (>100 USD), and early termination is concrete and informative—not merely a theoretical argument.
- **Breadth of cross-domain validation:** Success across circle packing (geometric), stellarator design (physics), MOCVRP/MOTSP (combinatorial), peptide design (biochemical), and GCU kernel optimization (code generation) demonstrates the framework's claimed plug-and-play generality. The Tencent Kaiwu 2025 top-10 placement provides real-world validation.
- **Practical efficiency:** ~$7 USD and <30 min per 5-objective PMO run is substantially more efficient than retrieval-style alternatives ($100+, >24 h), making the framework practically usable.

---

## Weaknesses

### Fatal
None.

### Major

- **Overclaiming in circle packing results.** The paper claims ExLLM "sets new records" for circle packing, but the evidence is mixed. For n=26, the improvement is 2.635977 → 2.635983 (a difference of ~6e-6), which is within numerical precision of existing solvers. For n=27–31, ExLLM "matches" published records but existing records are stated as "2.685+" which means the existing result is at least 2.685, and ExLLM achieves 2.68598—this is not clearly an improvement without knowing the exact prior value. The "+" notation makes it impossible to determine whether ExLLM actually exceeds or merely equals the known lower bound. The abstract should clarify this nuance rather than flatly claiming new records.

- **Experience module shows moderate marginal gain over k-offspring alone.** The ablation (Table 3) shows "ExLLM w/o experience" reaches 18.165 vs. 19.165 for full ExLLM—a gap of 1.0 points on a 23-point scale. While non-trivial, the k-offspring alone accounts for the majority of improvement over prior SOTA (from 17.862 to 18.165), and the evolving experience provides a secondary boost. Given that the paper frames the evolving experience as the primary novel contribution, the contribution ordering in the narrative may overstate its relative importance.

- **Proprietary LLM dependency limits reproducibility and fairness across different comparisons.** While the 5-objective experiment uses the same GPT-4o backbone for MOLLEO and ExLLM, the full PMO Table 3 comparison does not explicitly state which LLM version was used for ExLLM or whether the same model underlies the comparison. This is a significant gap: AlphaEvolve, ReEvo, and other LLM-based baselines in Table 4 (MOCPOP) may use different LLM generations, and the ablation from Table 1 uses Gemini-2.5-flash. The reliance on black-box proprietary APIs means results cannot be reproduced when API versions change.

### Minor

- **Stellarator P3 score reporting inconsistency.** The text claims a 3% improvement on P3 (133.634 vs. 129.796) but separately notes "6% improvement on the single point (97 vs. 103)." These two metrics seem to be different aggregation of P3 scores; both should be explained clearly in the main text rather than appearing contradictory.

- **The "evolving experience" update algorithm is presented informally.** The update rule $E_{t+1} = S_\theta(E_t, D_t)$ is described in prose but the stopping criteria, maximum token budget, or format specification for $E_t$ are not stated. Reproducing this design requires guessing prompt templates.

- **Diversity metric drops significantly in some configurations** (e.g., Random-init diversity 0.494 for ExLLM vs. 0.670 for MOLLEO). The paper acknowledges the fitness–diversity tradeoff but does not discuss whether this reduced diversity could be a concern for downstream wet-lab screening where structural diversity is often a hard requirement.

### Trivial
- Table 2 shows DyMol and Genetic-GFN as N/A under worst-init and best-init conditions. These methods appear to have no principled mechanism to fix initial populations. Brief commentary on whether such N/A conditions disadvantage or benefit ExLLM comparisons would be useful.

---

## Nice-to-Haves
- An open-source backbone LLM (e.g., Llama-3 70B or Qwen2.5) comparison would significantly strengthen reproducibility and allow practitioners without API budgets to adopt ExLLM.
- The adaptive k and p_exp online scheduling mentioned in the conclusion would be a natural experiment to include in ablations.

---

## Novel Insights
The most genuinely novel insight is the identification and characterization of "exploration collapse" in retrieval-style memory systems applied to large discrete optimization (Table 1). Prior LLM optimization work implicitly assumes that more memory is better; this paper provides concrete evidence—dropping uniqueness below 10%, unbounded prompt growth, and premature run termination—that per-step retrieval injection actively harms search in high-iteration regimes. The single evolving memo design, while heuristic, offers a principled alternative that decouples memory cost from iteration count. The probabilistic injection ($p_\text{exp} \sim \text{Bernoulli}(p)$) as a simple mechanism to prevent over-exploitation from experience is also a clean insight that generalizes beyond molecular optimization.

---

## Suggestions
- Clarify which exact LLM version and temperature were used for all PMO experiments in Table 3, to enable replication as model APIs evolve.
- Revise circle packing claims: for n=27–31, "matches existing lower bounds" is more accurate than "sets new records." Claim improvements only for n=26 and n=32 where a numerical improvement is demonstrated.
- Report an ablation comparing k=1 (standard single-offspring) vs. k=2,4,8 in the same cost-controlled setting (same total evaluations) to isolate the k-offspring contribution more cleanly.
- Provide an approximate prompt template for the evolving experience update call to aid reproducibility.

---

## Score and Decision

ExLLM makes a genuine engineering contribution: a well-motivated and well-executed framework that surpasses prior SOTA on a standard benchmark by a non-trivial margin and transfers convincingly across diverse domains. The core ideas are simple but effective. The main concerns are moderate overclaiming in circle packing, the proprietary LLM dependency, and the framing that somewhat overstates the evolving experience module's relative contribution versus the k-offspring baseline. These are significant but not fatal; the empirical substance is real and the cross-domain breadth is exceptional.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>