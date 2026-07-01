## Summary

This paper identifies a genuine blind spot in interventional causal discovery: post-treatment selection, where sample selection occurs after interventions and produces the same cross-intervention invariance patterns (variant marginal, invariant conditional) as genuine causal relations. The paper proposes a formal framework that models post-treatment selection via augmented DAGs, defines a finer-grained equivalence class (FI-Markov equivalence) and a corresponding graphical representation (F-PAG), and presents a sound and complete algorithm (F-FCI) for recovering causal structure under both latent confounders and post-treatment selection.

## Strengths

**1. Problem identification is genuinely novel and well-motivated (Section 1, Figure 1).** The paper identifies a gap the causal discovery community has largely overlooked: post-treatment selection can mimic the same cross-intervention invariance patterns as genuine causation. The examples in Figure 1 illustrate how causal and selection structures collapse into the same empirical signatures under existing frameworks. This is a real blind spot in methods like GIES, IGSP, and FCI with interventional data.

**2. Theoretical characterization is substantive (Sections 3.2–3.3, Lemmas 1–4, Theorem 2).** The FI-Markov equivalence class, the square mark (□) and the inducing-node typology (Type I vs. Type II) are principled extensions of MAG/PAG theory. The soundness and completeness claims (Theorems 3–4) provide formal guarantees for the constraint-based algorithm.

**3. The paper is honest about its central limitation (Section 6, line 291).** The conclusion explicitly states that the method depends critically on the presence of Type I inducing nodes and discusses this limitation rather than glossing over it.

## Weaknesses

### Fatal
None.

### Major

**1. The method's core claim is conditional on Type I inducing nodes, which the abstract overstates.** The abstract claims the method allows "going beyond traditional equivalence classes toward the underlying true causal structure" without qualification (line 9). The distinction between direct causal links and selection patterns depends on there being a Type I inducing node (a third variable that can be intervened on to block the path) for each pair of interest. The paper acknowledges this in Section 6 (line 291), but the abstract and introduction do not. For variable pairs where no such third variable exists or can be intervened on, the method falls back to the same ambiguity as existing frameworks. This scope constraint should be foregrounded at the outset.

**2. The experimental section lacks essential implementation details for reproducibility.** For a constraint-based method whose empirical performance depends entirely on CI test reliability, the paper does not specify: (a) what specific CI test is used (kernel-based? Gaussian likelihood ratio? discrete test for the binary ψ indicator?), (b) the p-value threshold or significance level for CI tests, (c) how many intervention targets are used or what proportion of variables are intervened on, (d) how the "predefined interval" for the selection mechanism is chosen. These omissions make the experiments difficult to reproduce or assess critically.

### Minor

**1. Experimental evaluation is thin.** Results are averaged over only 10 graphs per configuration (Figure 6 caption). For a stochastic data-generation process (random Erdős–Rényi graphs, random functions, random latent confounders, random selection variables), 10 trials yield wide confidence intervals. The "over 5% precision improvement" claim rests on this limited sample.

**2. No comparison on data without post-treatment selection.** Showing baselines fail on selection-corrupted data is the paper's premise. An informative control would be to run F-FCI on data *without* selection to verify it does not lose power or overfit to selection patterns that are absent.

**3. Naming inconsistency in the abstract.** The abstract (line 9) calls the algorithm "$\mathcal{F}$-FCL", while the rest of the paper calls it "$\mathcal{F}$-FCI." Minor but should be corrected.

**4. Odd noise distribution in data generation.** The noise is sampled from `Unif([0,2] ∪ [2,4])` (line 275), which is effectively `Unif([0,4])` with a missing point at 2. This appears unintentional and should be clarified or corrected.

### Trivial
None.

## Nice-to-Haves
- An ablation study that varies the presence/absence of Type I inducing nodes would directly quantify the method's main limitation.
- Runtime comparison against baselines would help assess practical applicability.
- Varying selection strength (the "predefined interval") as an experimental factor would provide insight into when the method works best.

## Removed Points
The following points from the input review are removed with justification (treat with caution — they may reflect parser artifacts or reviewer misunderstandings):

- **Algorithm pseudocode unreadable / garbled CI patterns (Critical Issue 1):** The six identical CI pattern strings `(⊥, ⊥, ⊥, ⊥)` and the garbled arrow notations in Step 2.3 are PDF parser artifacts — the original submission does not have these issues. The algorithmic logic is explained in prose (lines 249–251) and the orientation rules are summarized in Figure 4(i)'s table. This criticism stems from formatting artifacts, not author errors.
- **Missing Table 1, Figures 10–13 in main text:** These are in the appendix, which the parser strips from all submissions. The paper references them; they exist in the original.
- **Missing code URL (line 279):** The URL is blank in the parser output — likely a double-blind review redaction or parser artifact.
- **Definitions 7–11 deferred to appendix:** Standard practice in this field; the appendix is stripped by the parser.
- **"Baseline comparison likely stacks the deck" (Critical Issue 3):** The baselines are standard methods that do not model selection. Showing that they fail on selection-corrupted data is the paper's premise — it demonstrates the gap exists. The requested control (comparison without selection) is retained as Minor weakness #2 above, but the claim that the comparison is "unfair" or "uninformative" is not valid.
- **"No discussion of statistical significance of CI tests":** Merged into Major weakness #2 (implementation details).
- **Real-world application is a "placeholder":** The full results are deferred to the appendix (stripped by parser). The main text states the dataset and evaluation approach.
- **"Fundamental limitation constrains the method's scope more than the paper acknowledges":** The paper does acknowledge this in Section 6. The criticism is partly valid about the abstract but overstates the paper's omission — retained as Major weakness #1 above with proper calibration.
- **"The paper identifies a genuinely underexplored problem" (strength):** This is a genuine, specific strength (Figure 1, Section 1). Kept.
- **Various generic "strengths" from the original review:** No purely generic or sycophantic strengths were present; the three listed strengths are specific to the paper's content.

## Novel Insights
None beyond the paper's own contributions. The reviews surface a tension between the paper's strong theoretical framework and its thin empirical validation, but this is an expected evaluation trade-off rather than a novel finding.

## Suggestions

1. Add a table to the main text showing precision, recall, F1, and SHD with standard deviations for a representative configuration (e.g., n=1500, d=15).
2. Specify the CI test implementation, threshold, and how intervention targets are selected.
3. Add an explicit qualifying statement to the abstract about the Type I inducing node requirement.
4. Include an experiment on data without post-treatment selection to show F-FCI does not overfit to selection artifacts.
5. Fix the "$\mathcal{F}$-FCL" / "$\mathcal{F}$-FCI" naming inconsistency in the abstract.
6. Clarify or correct the noise distribution `Unif([0,2] ∪ [2,4])`.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>