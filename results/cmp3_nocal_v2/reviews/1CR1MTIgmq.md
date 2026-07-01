## Summary

This is a rebuttal/commentary paper responding point-by-point to Palazzo et al. (2024), which had itself challenged the authors' earlier work (Bharadwaj et al., 2023; Ahmed et al., 2021) on EEG-based object recognition. The paper identifies factual inaccuracies, unsupported claims, and logical issues in Palazzo et al. (2024) across eight substantive sections, and contributes new empirical evidence (frequency-domain supertrial averaging) showing that supertrial construction does not attenuate high-frequency information as Palazzo et al. claimed. The core conclusion — that nothing in Palazzo et al. (2024) refutes the original claim of Bharadwaj et al. (2023) — is well-supported by the paper's analysis.

## Strengths

- **New empirical evidence (Section 7).** The paper performs a novel frequency-domain supertrial averaging experiment on the Ahmed et al. (2021) data, demonstrating that this averaging method does *not* attenuate higher frequencies (Figure 1), and that EEGChannelNet remains at chance regardless of averaging method (Table 1). This directly and empirically counters Palazzo et al. (2024)'s central technical objection that the supertrial method was designed to penalize EEGChannelNet by suppressing high-frequency information.

- **Clean, verifiable factual corrections (Sections 4 and 6).** Section 4 shows that published tables (Spampinato et al., 2017, Table 1; Kavasiidis et al., 2017, Table 1; Palazzo et al., 2017, Table 1) state 350 s sessions, not "about 4 minutes." Section 6 shows that Bharadwaj et al. (2023) analyzed data from 7 subjects (1 from Ahmed et al. + 6 from Li et al.), directly contradicting Palazzo et al. (2024)'s claim of "one subject only." These are falsifiable, primary-source-verified corrections.

- **Precise conceptual distinction in Section 8.** The paper correctly distinguishes between *within-run* temporal correlation (training and test from same blocks of same run) versus *cross-run* temporal correlation (training and test from temporally correlated blocks of different runs), and shows that Palazzo et al. (2020b)'s blank-screen analysis measures only the latter. This explains why the BDB analysis fails to address the actual confound present in the original block-design experiments, and is the paper's most analytically valuable contribution.

- **Corrective on terminological misuse of "confound" (Section 8).** The paper invokes the APA definition to argue that the concerns Palazzo et al. raise about interleaved designs would at most reduce data quality (underestimating accuracy), not introduce an inseparable independent variable — which is conceptually sound and clarifies an important methodological point.

## Weaknesses

### Fatal
None.

### Major

1. **Ethics Statement radically overclaims what this paper does (lines 301–365).** The Ethics Statement opens with "This work debunks nearly one hundred published papers whose results are based on the same confound" and lists ~100 papers it claims "draw flawed conclusions." This is false as a description of this paper's content. The paper rebuts *one* paper: Palazzo et al. (2024). It does not analyze, re-analyze, or even mention any of the ~100 listed papers beyond their names. The broader debunking of block-design EEG datasets was the contribution of earlier work (Li et al., 2021; Ahmed et al., 2021; Bharadwaj et al., 2023). A reader taking this sentence at face value would believe the paper contains analyses across ~100 papers when it does not. This structural misrepresentation of the paper's contribution undermines its credibility. The statement must be removed or rewritten to reflect the paper's actual scope.

2. **Unverifiable, unsupported accusations in the Ethics Statement (lines 305–310).** The statement reads: "A research community, knowingly or unknowingly, has discovered that one can use confounded datasets to churn out a plethora of flawed results without reviewers noticing. They have also discovered that one can collect new confounded datasets to churn out even more flawed results without reviewers noticing." This is an accusation of systemic scientific misconduct spanning an entire subcommunity. It is not supported by any evidence or analysis presented in this paper — it is imported from the authors' broader body of work. Including it as if it follows from this paper's limited analysis is inappropriate and would need to be removed.

### Minor

3. **Figure 1 / text ambiguity on "amplifies" (lines 150–152 vs. caption).** The text states that frequency-domain averaging "does not attenuate higher-frequency components. In fact, it amplifies them" (line 151–152). However, the figure caption (line 170) states "raw trials having the highest power and the 100 supertrial size having the lowest power" — all supertrial spectra are *below* the raw trial spectrum at every frequency. These can be reconciled if "amplifies" means "amplifies relative to time-domain averaging, not relative to raw trials," but this comparison is not shown, and the text as written is misleading. This ambiguity needs clarification.

4. **Logical asymmetry on null results (Section 8 vs. Table 1).** The paper cites Frost (2024) — "You can't prove a negative!" (lines 222–227) — to argue that Palazzo et al.'s failure to find a temporal confound in blank-screen data is not proof of its absence. Yet the paper treats its own null result (EEGChannelNet at chance in Table 1) as positive evidence "validating the original claim of Bharadwaj et al. (2023)" (lines 155–156). By the same logic, a null result for EEGChannelNet is not proof that the classifier *cannot* extract class information — it is only evidence that under these conditions it did not. This asymmetry weakens the paper's logical coherence. (Note: the paper's overall case does not rest solely on this null result — other classifiers show above-chance performance — but the framing is inconsistent.)

5. **No limitations discussion.** The paper has no dedicated limitations section. Rebuttal papers should acknowledge the bounds of their claims — e.g., the frequency-domain averaging experiment uses one dataset and one family of averaging parameters; the null results for EEGChannelNet are specific to the data and methods used. Including such discussion would strengthen the paper's rigor.

### Trivial
None.

## Nice-to-Haves

- A quantitative statistical comparison between time-domain and frequency-domain supertrial spectra (e.g., power in specific frequency bands) would strengthen the claim in Section 7 beyond the qualitative description of Figure 1.
- An explicit statement that all claims in Palazzo et al. (2024) are addressed somewhere in the paper would help readers, though a charitable reading suggests they are.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Criticism about signal bleeding rebuttal being "plausible but not empirically demonstrated"** (from Section-by-Section Notes). Removed because the paper provides reasoned argumentation based on trial duration parameters (2 s trials, 1 s blanking) and cites subject attentiveness evidence — this is appropriate for a rebuttal paper. Demanding new empirical demonstration for every sub-claim would be an unreasonable burden.

- **Criticism about cross-subject variability (Section 5)** being weak because it "doesn't directly contradict Palazzo et al.'s broader point." Removed because the reviewer acknowledges the point is valid. The paper correctly observes that the variability cited by Palazzo et al. comes from confounded block-run data, not unconfounded randomized data.

- **"No statistical comparison" for Figure 1.** Removed — this is a nice-to-have enhancement, not a weakness. Qualitative spectral plots are a standard way to present this type of evidence.

## Novel Insights

The harsh critic makes two observations not present in the paper itself: (1) the Ethics Statement's scope claim is factually inconsistent with the paper's content, and (2) the "can't prove a negative" argument creates a logical tension with the paper's own use of null results. These are genuine meta-observations about framing and argumentative consistency that could help the authors improve the paper. The within-run vs. cross-run temporal correlation distinction (Section 8) is correctly identified as the paper's most analytically valuable contribution.

## Suggestions

1. **Rewrite or remove the Ethics Statement** to accurately reflect the paper's scope. The current claim of debunking ~100 papers is false. Replace with: "This paper rebuts specific claims in Palazzo et al. (2024). For broader discussions of confounded datasets, see Li et al. (2021), Ahmed et al. (2021), and Bharadwaj et al. (2023)." Remove the accusatory language about "a research community."

2. **Clarify Figure 1** by explicitly stating the baseline for the "amplifies" claim. If the comparison is against time-domain averaging, show that comparison or remove "amplifies" and state only that frequency-domain averaging preserves the spectral shape without attenuating high frequencies disproportionately.

3. **Acknowledge the null-result asymmetry** with a brief caveat: "We note that null results for EEGChannelNet are not proof that no classifier can succeed on these data, but they are consistent with the claim that this method does not extract class information under these conditions."

4. **Add a brief limitations section** acknowledging the scope of the empirical evidence (single dataset, specific averaging parameters) and the bounds of the rebuttal's claims.

## Score and Decision

The paper's core contribution — the point-by-point rebuttal of Palazzo et al. (2024), supported by new empirical evidence and clean factual corrections — is sound and meaningful to an ongoing scientific debate. The frequency-domain averaging experiment directly counters a central technical objection, and the within-run vs. cross-run temporal correlation distinction clarifies a confusion in the prior literature. However, the Ethics Statement's sweeping claims (debunking ~100 papers without analysis, accusatory language about a research community) are unsupported by the paper's evidence and constitute a serious overreach that must be corrected. These are fixable but non-trivial. The paper would be acceptable after these corrections.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>