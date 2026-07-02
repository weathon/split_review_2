## Summary

This paper connects Predictive State Representations (PSRs) with tensor decomposition methods to recover explicit POMDP observation and transition matrices from action-observation data. The key theoretical contribution is showing that the similarity transform separating PSR representations from explicit POMDP parameters can be estimated via joint diagonalization of observation matrices from full-rank actions. When states share the same observation distributions across all full-rank actions, the method recovers partition-level transition models. The paper evaluates the approach on Tiger, T-Maze, and Sense-Float-Reset domains.

## Strengths

- **Clean theoretical connection between PSRs and tensor methods.** Sections 3–4 develop a principled link between these two previously separate literatures. The paper shows how the similarity transform from PSR representations to explicit POMDP parameters can be estimated via joint diagonalization of observation matrices from full-rank actions (Eqs. 16–18, Lemma 1). This is the paper's central technical contribution and is well-motivated.

- **Honest characterization of what can and cannot be recovered.** Theorem 1 and the surrounding discussion (lines 115–145) precisely state that recovery is only possible up to the full-rank observability partition. When states share observation distributions across all full-rank actions, the paper acknowledges that only partition-level transition models can be obtained. The Sense-Float-Reset example (Figure 1) concretely illustrates this limitation.

- **Reward-specification experiment identifies a genuine advantage of explicit models.** The noisy-hallway domain (lines 237–243) presents a case where observation-based reward assignment fails because middle-state and uniform-belief distributions are indistinguishable by observation alone, motivating the need for state-based methods enabled by explicit models.

## Weaknesses

### Fatal
None.

### Major

- **No experimental comparison against the tensor methods the paper claims to improve upon.** The paper's central claim (lines 9, 23) is that it relaxes assumptions of prior tensor methods (Azizzadenesheli et al., 2016; Guo et al., 2016) to "learn a broader class of POMDPs than existing tensor methods." Yet the experiments compare only against PSR and EM — never against the tensor methods whose assumptions are being relaxed. The paper describes domains where prior tensor methods should fail by design (Tiger, Sense-Float-Reset's repeating observation distributions), but provides no evidence that the proposed method actually succeeds where they fail. This is the most significant evidential gap: the paper's core comparative claim is unsupported.

- **How the PSR baseline produces observation/transition errors in Figure 3 is unexplained.** The paper states (lines 15–19) that PSRs "cannot yield direct estimates of transition and observation likelihoods" and that "transition and observation likelihoods cannot be directly read from a PSR." Yet Figure 3 (Rows 2–3) reports "Obs. matrix error" and "Trans. matrix error" for a "PSR" (orange) baseline. The paper never explains how PSRs — which by its own description produce only predictive likelihoods — generate explicit observation/transition matrices for comparison against ground truth. Either the PSR line is not actually plotted in those rows (making the legend misleading), or some conversion procedure was applied that must be justified. As presented, this figure is uninterpretable on this point.

- **Reward-specification experiments do not cleanly support the claimed advantage.** The paper argues that explicit observation/transition models enable state-based reward specification that PSRs cannot do (lines 25–26, 233–243). However: (a) In the directional domain (Figure 4, top row), observation-based methods ("Ours_obs" and "PSR_obs") work well, while state-based reward ("Ours_state," the unique capability of the proposed method) performs poorly — the claimed advantage does not materialize. (b) In the noisy domain (Figure 4, bottom row), the paper claims observation-based reward "does not elicit the correct behavior from the planner" (line 243), yet the plotted "Total hacked reward" shows "Ours_obs" and "PSR_obs" achieving the *highest* reward, with state-based "Ours_state" only approaching this level slowly at the largest data regime. The textual claims and plotted data appear to contradict each other. (c) Because "Ours_obs" and "PSR_obs" produce similar results throughout, and "Ours_state" underperforms in one domain and converges slowly in the other, the experiments do not convincingly demonstrate that the explicit model provides a practical advantage over the simpler observation-based approach that PSRs can already implement.

### Minor

- **No algorithm pseudocode or end-to-end procedure.** The method is described across three sections (3, 4.2, 4.3) in prose and equations, but there is no consolidated algorithm, pseudocode, or step-by-step listing. Given the multiple steps (Hankel estimation → SVD rank factorization → PSR extraction → identification of full-rank actions → joint diagonalization → partition-level recovery with rotation), the method is difficult to assess, implement, or reproduce.

- **Unsupported claim about EM convergence.** Line 231 states that "EM consistently converges to a local minimum and does not obtain correct observation or transition likelihoods." This is stated as a fact about the EM baseline, but no supporting evidence is provided — no training curves, no analysis of local minima, no discussion of random restarts or convergence criteria. Given that EM is a standard baseline for this problem, a more careful treatment is expected.

- **Full-rank action identification threshold not specified.** Line 165 states that full-rank actions "can easily be determined by a threshold test on the singular value decomposition," but the paper does not specify the threshold or analyze sensitivity of results to this choice. Near-singular matrices from finite data will have small singular values, and a principled criterion is needed to distinguish full-rank from near-rank-deficient matrices.

- **SVD rank-selection threshold unspecified.** The number of states is determined by SVD truncation of the Hankel matrix, but the paper does not specify what threshold is used. The "No. estimated states" plots in Figure 3 show variance (especially for 3- and 4-state Sense-Float-Reset), indicating that this choice matters in practice.

- **Figure 3 truncation is not visually indicated.** The caption (line 194) states that transition error curves are truncated because they are "only measurable once the estimated number of states matches that of ground truth," but this truncation is not marked in the figure. The reader expects continuous curves since data is plotted at each point.

### Trivial
None.

## Nice-to-Haves

- A sensitivity analysis examining how the p_succ parameter (line 151) affects recovery quality, especially near the "mild assumptions" boundaries p_succ = 1/2, 1.
- A clearer notation in the reward-specification experiments distinguishing between "directional" and "noisy" hallway domains (the text appears to have the descriptions switched relative to their names).

## Removed Points

- **"Missing comparison with prior tensor methods" framing as fatal.** The reviewer called this a "critical issue" but did not establish that it invalidates the theoretical contribution — it weakens the experimental validation of comparative claims. Demoted to Major since the theoretical core (Sections 3–4) stands independently.
- **Formatting/style nitpicks about Figure 3 y-axis scale differences.** Minor presentation issue; removed per hard rules.
- **Criticism about EM having oracle state-count knowledge being "fair but could be noted more clearly."** The reviewer already called this fair; not a genuine weakness.
- **"The paper's claim about meeting PSR performance is a modest bar" (from Strengths section).** This is a value judgment, not a concrete strength or weakness.
- **Generic speculations about "could the metric be measuring a proxy?"** Not anchored in specific paper content; removed.
- **Strengths that are generic or superficial** (e.g., "this paper addressed an important problem"). Kept only the three concrete strengths above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Run prior tensor methods as baselines** (Azizzadenesheli et al., 2016; Guo et al., 2016) on domains where the proposed method succeeds and those methods fail by design (e.g., Tiger, Sense-Float-Reset). This directly validates the paper's central claim of learning a broader class of POMDPs.
2. **Clarify the PSR baseline** in Figure 3: either explain how explicit matrices are extracted from the PSR, or remove the PSR curve from the observation/transition error rows if it does not belong there.
3. **Resolve the contradiction in the reward-specification experiments.** Explain why observation-based methods achieve the highest "total hacked reward" in the noisy domain while the text claims they fail, or adjust the paper's narrative to match the data. Consider a controlled domain where observation-based reward definitively fails and only state-based reward works.
4. **Add algorithm pseudocode** consolidating the full pipeline (Hankel estimation → SVD → PSR parameters → full-rank action identification → joint diagonalization → rotation → partition-level models).
5. **Provide evidence for the EM convergence claim** (training curves, number of random restarts, convergence criteria).

## Score and Decision

This paper presents a genuine theoretical contribution — the connection between PSRs and tensor decomposition methods for POMDP learning — and honestly characterizes its limitations. However, the experiments fall substantially short of supporting the paper's central comparative claims. The most critical gap is the absence of any comparison against the prior tensor methods the paper positions itself as improving upon. Additionally, the PSR baseline's inclusion in the observation/transition error plots is unexplained, and the reward-specification results are ambiguous or contradictory with respect to the paper's narrative. A substantial experimental revision is needed before the paper's claims can be considered validated.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>