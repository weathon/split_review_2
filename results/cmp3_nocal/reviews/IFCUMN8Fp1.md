Now let me write the final consolidated review.

## Summary

This paper studies learning the parameters of a discrete POMDP (transition and observation matrices) from action-observation sequences collected under uniform random exploration. It connects Predictive State Representations (PSRs), which learn dynamics up to an unknown similarity transform, with tensor decomposition methods that can estimate that transform. The key theoretical contribution (Theorem 1) characterizes recovery up to a "full-rank observability partition" — states sharing identical observation distributions across all full-rank actions can only be recovered at the partition level. The method relaxes a prior requirement that each full-rank action individually distinguish states, replacing it with a weaker aggregate condition across all full-rank actions. Experiments on small domains (2–6 states) compare the learned models against PSRs and EM baselines in terms of parameter recovery and planning performance.

## Strengths

1. **Clear theoretical connection between PSRs and tensor methods (Sections 3–4).** The paper carefully works out how PSRs learn dynamics up to a similarity transform (Proposition 1, building on Carlyle & Paz 1971 and Balle et al. 2014) and then shows how joint diagonalization of matrices derived from the PSR parameters can estimate that transform. Theorem 1 formally characterizes what can and cannot be recovered — recovery up to the full-rank observability partition — which is a crisp theoretical contribution.

2. **Relaxation of a genuine assumption in prior tensor methods.** Prior approaches (Azizzadenesheli et al., 2016; Guo et al., 2016) required that each full-rank action have observation distributions that are unique per state. The proposed method replaces this with an aggregate condition over *all* full-rank actions (Lemma 1, line 23). This widens the learnable class: a POMDP where no single action distinguishes states but the combination does becomes learnable.

3. **Honest characterization of limitations.** Theorem 1 explicitly states when only partition-level recovery is possible. The running example (Sense-Float-Reset, Figure 1) clearly illustrates the residual ambiguity. The paper does not overclaim.

## Weaknesses

### Fatal
None.

### Major

1. **No experimental domain showcases the paper's main claimed advantage.** The paper's central advance over prior tensor methods is the relaxation from per-action uniqueness to aggregate uniqueness across actions (line 23: "simultaneously leverage all observation distributions from *all* actions... rather than a per-action basis"). Yet none of the tested domains demonstrate a case where this relaxation matters — i.e., a POMDP where no single action has unique observation distributions per state, but the aggregate across full-rank actions does distinguish states. Tiger satisfies the stricter per-action condition. Sense-Float-Reset has states that are indistinguishable even in aggregate. The hallway domains are designed to have full recovery (each state in its own partition under the aggregate condition), but they would also satisfy the per-action condition. The paper's claimed advance thus remains theoretically stated but experimentally unvalidated.

2. **The claimed advantage over PSRs (reward specification from explicit state-based likelihoods) is not convincingly demonstrated.** Figure 4 provides the evidence:
   - In the Directional domain (top row), the observation-based methods (Ours_obs, PSR_obs) *outperform* the state-based method (Ours_state), directly contradicting the claim that explicit state-based likelihoods are advantageous there. The paper acknowledges this is due to "slow convergence of transition matrices."
   - In the Noisy domain (bottom row), Ours_state eventually approaches the performance of observation-based methods, but error bars substantially overlap throughout most of the data range. The paper's conclusion that these likelihoods "are necessary to correctly direct agent behavior in POMDPs with very noisy observations" (line 25) goes beyond what the empirical separation supports.

### Minor

3. **State-count recovery is unreliable on several domains, and evaluation metrics are conditional on correct recovery.** Figure 3 (Row 1) shows the method does not always converge to the correct number of states. On T-Maze, the estimated count varies between ~3 and ~6. On Sense-Float-Reset (3 states), the method estimates ~4.5 states even at 10⁶ interactions. The paper honestly notes that transition error "is only measurable once the estimated number of states matches that of ground truth, which truncates the curves" (Figure 3 caption). This means the favorable parameter-recovery results are conditional on a step that does not always succeed.

4. **Algorithm description in Section 4.3 has confusing notation and is vague on key details.** The notation $P^{t-1}$ (lines 196–198) is not defined and appears to conflate notation in a confusing way — likely meaning $P'^{-1}$ given the context, where $P'$ is the eigenvector-based transform introduced earlier. The random block-diagonal rotation matrix $R$ is described as having "blocks correspond to the full-rank observability partition," but the criterion for choosing $R$ and the mechanism by which this procedure satisfies Theorem 1 are not explained in the main text (deferred to Appendix A.5). The joint diagonalization method of He et al. (2024) is cited without explanation. A reader cannot implement the core recovery step from the main paper alone.

5. **EM baseline comparison is somewhat weak.** EM is initialized with the number of states determined by the SVD truncation of the spectral method (line 211), tying EM's state count to the spectral method's estimate. The paper notes EM "consistently converges to a local minimum" (line 231), which is a known limitation. Running EM with multiple random restarts or with the true number of states as an oracle would provide a stronger comparison and would better isolate whether the proposed method succeeds where EM *can* succeed with proper tuning.

6. **No guidance on the threshold for identifying full-rank actions.** The paper states that full-rank actions "can easily be determined by a threshold test on the singular value decomposition on all matrices $M^a$" (line 165) but does not specify how this threshold is chosen or how sensitive the results are to it. Since the set $\mathcal{A}_{full}$ determines which actions are used for the entire recovery procedure, this is a consequential hyperparameter that receives no analysis.

### Trivial
- The notation $P^{t-1}$ in Section 4.3 (lines 196, 198) appears to be a typesetting error for $P'^{-1}$ and should be corrected.

## Nice-to-Haves
- A pseudocode or algorithm listing would substantially improve reproducibility, given the multi-step pipeline (SVD truncation, threshold determination, matrix inversion, eigendecomposition, joint diagonalization, random rotation).
- The reward-specification experiments would be more convincing with: (a) a domain where state-based reward specification is *provably* impossible with observation-only methods, and (b) tighter error bounds that do not overlap between state-based and observation-based methods.
- The T-Maze modification (random restart instead of termination, line 216) changes the problem's dynamics substantially; a brief discussion of how this affects the evaluation would be helpful.
- An analysis of how violations of the uniform-random-exploration assumption affect the Hankel matrix estimate would strengthen the practical relevance discussion.

## Removed Points
These points are flagged to be removed; treat them with caution.

1. *Claim that "full state observability" characterization of prior work is misleading.* The reviewer questions whether Azizzadenesheli et al. (2016) and Guo et al. (2016) assume "full state observability." I cannot independently verify the exact assumptions of those papers, and the paper's phrasing ("often assume") states a general tendency rather than a specific claim about those two papers. This criticism cannot be verified from the paper under review alone.

2. *Criticism about Hankel matrix rank being an idealized infinite-data property.* The paper already discusses the infinite-data regime (Section 3.3, line 91) and refers to Appendix B.1 for finite-data parameters. This is already acknowledged.

3. *Critique of missing appendix content (Appendix A.5).* The parser strips appendices; they exist in the original submission. Per instructions, removed.

4. *General speculation about confounders or metric validity not anchored to a specific passage.* Several concerns in the original review ("could the metric be measuring a proxy?", "are confounders controlled?") were area-of-concern sweeps without concrete anchors. Removed.

5. *Missing related works.* Removed per instructions (cannot verify existence of omitted works).

6. *Formatting/style nitpicks and requests for expanded discussion of well-known limitations.* Removed.

## Novel Insights
The most pointed insight from the review is the gap between the paper's claimed theoretical advance (aggregate condition relaxes per-action uniqueness) and its experimental validation, which never tests this condition in isolation. This is not a contradiction — the theory may be sound and the experiments simply incomplete — but it means the paper's strongest conceptual contribution remains a theoretical result without empirical backing in this submission. A secondary insight is that the reward-specification experiments, which are the primary argument for the practical advantage of explicit POMDP parameters over black-box PSRs, show the opposite of what is claimed in the directional domain, undermining the paper's central motivation.

## Suggestions
- Add at least one experimental domain where the aggregate condition matters (no single full-rank action distinguishes states, but the combination does) and show the proposed method succeeds while prior tensor methods would fail.
- Substantially strengthen the reward-specification experiments: either produce a domain with clear, non-overlapping separation between Ours_state and observation-based methods, or temper the claims about the necessity of state-based likelihoods.
- Fix the notation issue in Section 4.3 and provide a self-contained algorithm description (with pseudocode) in the main paper or a reliably accessible appendix.

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>