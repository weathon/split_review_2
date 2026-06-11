## Summary
This paper studies curriculum learning in goal-conditioned reinforcement learning (GCRL) from the perspective of data selection. The central claim is that curricula should be understood as a structural mechanism for selective data acquisition rather than merely an exploration heuristic. Using Universal Value Function Approximators (UVFAs) with potential-based reward shaping in a GridWorld navigation task, the authors compare uniform goal sampling to curricula that upweight harder-to-reach (edge) goals. The experiments report modest improvements in policy success on edge goals under curriculum sampling, particularly with a weighted variant that further biases sampling toward edge cells. The paper is positioned as a conceptual reframing — arguing that the field should view curricula as tools for shaping the training data distribution and thereby influencing function approximation — rather than as a new algorithmic contribution.

**Bottom Line:** The paper presents a conceptually interesting reframing of curriculum learning, but the empirical support is weak: gains are small relative to variance, key experimental details are missing, and the evidence does not discriminate the proposed "selective data acquisition" interpretation from simpler alternatives. The paper would benefit from substantial additional experiments (causal controls, distribution quantification, comparisons to existing curriculum methods) before the central thesis can be considered empirically supported.

## Strengths
1. **Conceptually interesting reframing.** The paper's central idea — viewing curriculum learning as selective data acquisition rather than merely an exploration heuristic — is a thoughtful conceptual contribution. This perspective could be valuable for the GCRL community if it leads to new curriculum design principles or connects curriculum learning to broader questions in data-centric RL.

2. **Clean experimental isolation.** Using a simple GridWorld with UVFAs allows the authors to isolate the effect of goal-sampling distribution from confounding factors (e.g., policy architecture, exploration noise). The comparison between uniform and curriculum sampling under fixed architecture and training budget is a valid approach for studying distributional effects.

3. **Honest limitations section.** The paper acknowledges several important limitations: the simplicity of GridWorld, the manual specification of curricula, and the modest and sometimes inconsistent gains. This transparency is commendable and helps set appropriate expectations for the scope of the work.

4. **Reproducibility-focused details.** The training protocol includes key hyperparameters (learning rate, batch size, epochs, seeds) that support reproduction. The use of PBRS with a clear potential function and the description of the UVFA architecture provide a solid foundation for replicating the basic setup.

## Weaknesses
### W1: Critical — Numerical inconsistencies between figures and tables (unreconciled)
The paper presents substantially different numbers for the same experimental conditions across Figure 1, Figure 2, and Table 1. For example, the NoCurr edge success rate is reported as 0.183 ± 0.131 (Fig 1), ~0.19 (Fig 2 Baseline panel), ~0.05 (Fig 2 Weighted panel), and 0.060 ± 0.055 (Table 1). These discrepancies are never explained. If different experimental conditions (grid size, horizon, sampling proportions) are being compared, they must be explicitly identified. As presented, the reader cannot determine which numbers correspond to which experiment, which fundamentally undermines the paper's empirical claims. *(See annotations on Page 1 — Fig 1/Table 1 inconsistency, Results 3.1-3.2.)*

### W2: Critical — Data collection policy is unspecified (reproducibility threat)
The paper states that data is collected by "rolling out 1000 episodes with greedy action selection under PBRS shaping" but never specifies: greedy with respect to what? If the UVFA is trained *after* data collection, what policy generated the trajectories? Is it an untrained random policy? A hand-designed controller? A previously trained policy? Without this information, the entire experiment cannot be reproduced, and the nature of the "training distribution" that curricula supposedly shift is unknowable. *(See annotation on Page 1 — Training Protocol.)*

### W3: Major — Effect sizes are dwarfed by variance; no statistical significance testing
All reported improvements are within one standard deviation of the baseline, with only 3 seeds per condition. The paper uses language like "modest but consistent improvements" and "systematically bias training data," but no statistical significance tests (t-test, bootstrap CI) are provided. With 3 seeds and overlapping ±1σ intervals, the "consistency" claim is unsupported. *(See annotation on Page 1 — Results 3.1.)*

### W4: Major — Claim-evidence mismatch on "reduced approximation error"
The introduction and conclusion repeatedly claim that curricula "reduce approximation error," but the experiments never directly measure value approximation error (e.g., MSE between predicted V(s,g) and true values). Only policy success rates are reported. This is a significant mismatch between what is promised and what is delivered. *(See annotations on Page 1 — Abstract, Introduction Paragraph 4, Conclusion.)*

### W5: Major — PBRS formulation with λ scaling may break policy invariance
The paper introduces λ=0.5 as a multiplicative coefficient on the potential-based shaping term, modifying the standard PBRS framework (Ng et al., 1999). This scaling changes the relative weight of shaping vs. terminal reward/step cost, potentially altering the optimal policy. No justification or discussion of this modification is provided. The negation step for evaluation is also confusing and potentially unnecessary. *(See annotation on Page 1 — PBRS formula.)*

### W6: Major — Curriculum design is underspecified
The baseline and weighted curriculum proportions are not quantified. The "fixed proportion" for edge sampling is never stated. The weighted curriculum "match their empirical difficulty" is not defined operationally. Grid dimensions and the number of edge vs. interior cells are omitted. Without these details, the experiment cannot be replicated. *(See annotation on Page 1 — Curriculum Design.)*

### W7: Major — Causal language exceeds correlational evidence
The Discussion and Conclusion use causal framing ("reshape," "improve," "amplified gains") that implies a causal mechanism from selective sampling to improved approximation. However, no controlled experiments isolate whether gains come from distribution shift, increased data quantity on hard goals, or other confounds. The evidence is purely correlational, so causal language is inappropriate. *(See annotation on Page 1 — Discussion.)*

### W8: Major — Unclear what the paper contributes beyond existing curriculum literature
The paper's central claim is that curricula should be seen as "selective data acquisition" rather than exploration heuristics. However, many existing curriculum methods (e.g., Graves et al., 2017; Florensa et al., 2017; Racanière et al., 2020) already operate by biasing the training distribution toward harder tasks. The paper does not systematically compare against these methods or demonstrate that the "selective data acquisition" framing leads to different predictions or designs than existing perspectives. The novelty claim in Paragraph 3 of the Introduction is asserted without evidence that prior work truly neglects this perspective. *(See annotation on Page 1 — Introduction Paragraph 3.)*

### W9: Moderate — No comparison to existing curriculum methods
The paper compares only uniform vs. edge-weighted sampling. It does not benchmark against standard curriculum learning methods (reverse curriculum generation, teacher-student, self-play, AMIGo, etc.). Without such comparisons, the practical significance of the selective-data-acquisition framing is unclear. The paper would be substantially strengthened by showing that this perspective leads to better curriculum design or explains phenomena that existing methods cannot. *(See annotation on Page 1 — Limitations.)*

### W10: Moderate — Introduction lacks a clear problem-gap-solution structure
The first paragraph provides background but does not clearly articulate a specific, well-defined research gap. The connection to open-ended learning (OEL) via Hughes et al. (2024) is referenced as motivation, but the specific unresolved question is deferred to the third paragraph. This weakens the narrative and makes it harder for readers to understand what the paper uniquely contributes. *(See annotation on Page 1 — Introduction Paragraph 1.)*

### W11: Minor — Horizon set inconsistency
Section 2.5 (Training Protocol) states H ∈ {30, 20, 16, 12}, but Section 3.1 (Results) adds H=10 to the set. It is unclear which horizons were actually used. *(See annotation on Page 1 — Training Protocol.)*

### W12: Minor — Missing distribution quantification
The paper claims curricula "shift the training distribution" but never quantifies this shift. No divergence metric (KL, EMD) is reported. A simple histogram or density comparison would substantially strengthen this central claim. *(See annotation on Page 1 — Results 3.1.)*

### W13: Minor — Conclusion contains an unfinished reference "?"
The conclusion includes a "(?)" placeholder for a missing citation, indicating the paper is in an incomplete draft stage. *(See annotation on Page 1 — Conclusion.)*

## Score
**Final Score: 4/10**

**Rationale:** This paper presents a conceptually interesting reframing of curriculum learning as selective data acquisition, which has potential value as a perspective-shifting idea. However, the empirical support is substantially weaker than what the claims require. The core issues are: (1) the numerical results are internally inconsistent across figures and tables, making it impossible to determine which experimental conditions produced which outcomes; (2) the data collection policy is unspecified, preventing reproducibility; (3) the effect sizes are smaller than the measurement variance, with no statistical significance testing; (4) the paper repeatedly claims that curricula "reduce approximation error" without ever measuring it; and (5) the central novelty claim (that prior work neglects the distributional perspective) is asserted without systematic evidence. These issues collectively mean that the paper's main thesis — that curricula should be understood as selective data acquisition mechanisms — currently rests on insufficient and partially contradictory evidence. The conceptual framing is worth preserving, but the empirical component needs major revision and extension before the claims can be considered validated.

**Note on Novelty:** External literature verification was unavailable in this run (Retrieval-Disabled Mode due to API token unavailability). The assessment of novelty and comparison with prior curriculum learning methods is therefore deferred. The score above reflects the paper's internal quality, claim-evidence alignment, and reproducibility, not a novelty judgment relative to external literature. Manual verification by the authors or reviewers is recommended to confirm the paper's positioning against existing work.