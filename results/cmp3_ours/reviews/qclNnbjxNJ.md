Now I have a clear picture from the calibration. Let me write the final consolidated review.

## Summary
This paper addresses post-treatment selection in interventional causal discovery, where samples are selectively included after interventions (e.g., quality-control filtering in single-cell perturbation experiments). The authors show that post-treatment selection produces the same cross-intervention conditional independence patterns as true causal relations, making it non-identifiable under standard frameworks. They introduce a new causal formulation, define a fine-grained interventional equivalence class (ℱI-Markov equivalence) represented by ℱ-PAGs (extending PAGs with novel edge marks), and propose ℱ-FCI, a constraint-based algorithm for recovering this equivalence class. Experiments on synthetic and real-world data are presented.

## Strengths

1. **The problem is genuinely underexplored.** Post-treatment selection in interventional causal discovery is a real and important challenge, particularly in biological settings (quality-control filtering in single-cell perturbation studies is a compelling concrete example). The paper correctly identifies that this phenomenon produces CI patterns indistinguishable from causation under standard formulations. Figures 1 and 4(i) effectively illustrate this core diagnosis, and the paper's Section 2.2 explains why existing interventional frameworks fail to handle this case.

2. **The ℱ-PAG representation is a nontrivial extension of the PAG framework.** Adding the square mark (□) to denote inducing-path ambiguities that can be resolved through interventional data, and distinguishing Type I vs. Type II inducing nodes (Definition 6), meaningfully extends the PAG representation for the target problem. If the algorithm works as claimed, this representation would be strictly more informative than standard PAGs when post-treatment selection is present.

## Weaknesses

### Fatal
None.

### Major

1. **The algorithm presentation lacks critical clarity, particularly the mapping from CI patterns to orientation decisions.** Algorithm 1's Step 2.2 (lines 216–226) refers to "orientation rules summarized in Figure 4," but Figure 4's table maps CI patterns to structures (a–h), not to edge orientations in the ℱ-PAG, and there is no explicit mapping from the six rows of the table to the six branches of the pseudocode. The prose (lines 249–251) discusses the intuition but the pseudocode itself does not encode the decision logic. Step 2.3 (lines 230–240) uses update notation that is undefined in the paper — for example, line 240 uses `→` to chain variables in a way that is not a standard graph operation (`X_{ℐ^{(i)}} → X_{ℐ^{(j)}} → X_{ℐ^{(i)}} → X_{ℐ^{(i)}}` is not a coherent graph update). Because Algorithm 1 is the paper's central contribution, this lack of clarity prevents a reader from confidently understanding, implementing, or verifying the claimed procedure.

2. **The experimental evaluation lacks controlled comparisons that isolate the paper's central claim.** The baselines (GIES, IGSP, UT-IGSP, JCI-GSP, FCI-interven, CDIS) do not model post-treatment selection, so it is unsurprising that ℱ-FCI outperforms them — they are solving a different problem. What is missing is: (a) a comparison with standard FCI applied on the same selection-biased data to quantify the degradation caused by ignoring selection, and (b) a test of ℱ-FCI on data *without* post-treatment selection to verify it does not overfit to nonexistent selection structure. These controls would directly test whether the method's improved performance comes from correctly handling the target phenomenon rather than from other advantages.

3. **Limited practical scope not adequately characterized.** The method's ability to disambiguate causal relations from post-treatment selection depends critically on the presence of Type I inducing nodes and on having interventions on intermediate variables (lines 249–251, 290–291). The paper acknowledges this in the limitations section but provides no analysis of how often Type I inducing nodes arise in practice, what fraction of ambiguities can be resolved when they are absent, or how the method's performance degrades without interventions on intermediate nodes. Theorem 4's completeness guarantee is scoped to "among intervened variables," which may be narrower than readers assume from the abstract's language.

4. **The real-data experiment lacks quantitative results in the main text.** The evaluation on gene regulatory networks (Section 5.2) describes results at a high level without reporting any precision, recall, F1, or other quantitative metric. The results are referenced to Figure 13 in the appendix, leaving the main-text evaluation essentially non-existent for a reader without the appendix.

### Minor

1. **Small number of trials.** The synthetic experiments average over only 10 graphs per configuration (Figure 6 caption). Given the visible variance in the plots (precision from ~0.2 to 0.8, SHD from ~25 to 100), 10 trials provide limited statistical reliability for drawing strong conclusions.

2. **Vague quantification of improvement.** The paper claims "an average precision of over 5% in most configurations" (line 277) without clarifying whether this is absolute or relative improvement, or which configurations are excluded.

3. **Missing code.** The footnote on line 279 says "A Python implementation is available at" with no URL provided.

### Trivial
None.

## Nice-to-Haves
- A controlled experiment testing ℱ-FCI on data both with and without post-treatment selection, to demonstrate it handles the target problem without degrading performance on standard settings.
- An empirical characterization of how often Type I inducing nodes arise in realistic settings and how the method performs when they are absent.
- A complexity analysis of the algorithm (the AllPaths enumeration in Step 2.1 could be exponential in the graph size).
- Moving key selection-detection results to the main text.

## Removed Points
These points were identified in the harsh critic input but are removed with justifications:

1. **"All six conditional branches check the same condition"** — The pseudocode CI conditions being garbled to all `(⊥, ⊥, ⊥, ⊥)` is a parser artifact (hard rule on garbled text). The substantive criticism about the missing explicit CI-to-orientation mapping is **retained** in Major weakness 1.
2. **"Key experimental evidence deferred to the appendix"** — Removed per hard rule (the appendix exists in the original submission; this is a known limitation of the review copy). The separate point about the real-data experiment lacking *any* quantitative result in the main text is retained in Major weakness 4 because it is a main-text content choice, not an appendix availability issue.
3. **"Connection to prior work on selection bias could be sharper"** — Removed; the paper's novelty is specifically in the interventional post-treatment setting, which is a genuine extension beyond standard selection bias handling in FCI theory (Spirtes et al., 2000; Zhang, 2008b). The paper correctly frames its contribution.
4. **"Definition 5 garbled edge types"** — Removed per hard rule (garbled symbols = parser artifact).
5. **"ℱ-FCL vs ℱ-FCI inconsistency in abstract"** — Removed per hard rule (typo = formatting artifact, not author error).
6. **"Section 3.1 notation ambiguity"** — Removed; the notation `̂X_{pag(i)}` is standard in the causal discovery literature.
7. **"Section 5.1 data-generating details"** — Removed; the description is sufficiently clear for domain experts despite the unconventional `Unif([0, 2] ∪ [2, 4])` notation.
8. **Section-by-section minor nitpicks** — All removed as presentation-level comments that do not affect the paper's substance.

## Novel Insights
The reviews surface a genuine tension: the paper identifies a real and important gap in interventional causal discovery (post-treatment selection is structurally non-identifiable under standard formulations), and the ℱ-PAG framework makes a plausible theoretical contribution toward filling that gap. However, the presentation of Algorithm 1 is substantially less clear than it needs to be for a paper whose main deliverable is a new algorithm, and the experimental evaluation does not include the controlled comparisons that would most directly validate the paper's central claim (distinguishing causation from selection). The gap between the theoretical ambition and the algorithmic/empirical execution is the core issue that separates this paper from stronger contributions in the same space — compare with the cleanly-executed CDIS paper (Dai et al., 2025) on the related but distinct problem of pre-intervention selection bias, which achieved strong scores despite addressing a comparably complex problem.

## Suggestions
1. Rewrite Algorithm 1's Step 2.2 to explicitly map each CI pattern from Figure 4's table (the six columns) to the corresponding edge orientation. Fix Step 2.3's update notation to use standard graph operations with clear semantics.
2. Add a controlled experiment: compare ℱ-FCI against standard FCI on selection-biased data, and test ℱ-FCI on data without selection to demonstrate it does not hallucinate selection structure where none exists.
3. Provide an empirical analysis of how often Type I inducing nodes occur and the method's sensitivity to their absence.
4. Move key quantitative results (selection detection accuracy, F1 scores) to the main text, or at minimum provide a summary table with headline numbers.
5. Release the code and provide the URL.

## Score and Decision

**Calibration anchors used:**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| When Selection meets Intervention (CDIS) | 8.00 | Round 1 | Stronger in every dimension — cleaner presentation, more rigorous evaluation, addresses a related problem. The current paper is substantially weaker. |
| Recovery of Causal Graph via Homologous Surrogates | 6.00 | Round 1 | Accepted with presentation issues similar to the current paper, but had clearer theoretical claims and a cleaner algorithm specification. |
| Predicting perturbation targets with causal differential networks | 4.25 | Round 1 | Weaker overall — less novel problem framing, fewer baselines. The current paper has a stronger theoretical contribution but similar experimental limitations. |
| Extracting Post-Treatment Covariates for HTE | 5.50 | Round 2 | Different problem (effect estimation vs. discovery). Similar score band — useful for calibration. |
| Test-Time Learning of Causal Structure | 5.50 | Round 2 | Rejected despite reasonable experimental evaluation. Similar presentation clarity issues. |
| Causal Effect Estimation with Mixed Latent Confounders and Post-treatment Variables | 6.25 | Round 3 | Accepted — cleaner presentation, more rigorous evaluation, albeit for a different task (effect estimation vs. discovery). |

**Round-1 bracket:** 3.5–5.5 (based on topically similar papers in the deepreview corpus)
**Narrowing:** The paper is stronger than the 4.0–4.25 papers (GRNI, perturbation targets) and comparable to the 5.5 rejected papers, but weaker than the 6.0+ accepted papers. The algorithm presentation issues and lack of controlled comparisons prevent it from reaching the acceptance bar.
**Final score:** 5.0

**Rationale:** The paper identifies a genuinely underexplored problem and proposes a plausible theoretical framework. However, the central algorithm is presented with insufficient clarity (no explicit CI-to-orientation mapping, undefined update notation), the experimental evaluation lacks the controlled comparisons needed to isolate the claimed effect, and the real-data experiment provides no quantitative results in the main text. These weaknesses are not fatal — the core idea and theoretical framework are sound — but they are substantial enough that the paper cannot be accepted in its current form.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>