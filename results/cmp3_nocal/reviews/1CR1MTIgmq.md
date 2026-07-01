## Summary

This paper is a point-by-point rebuttal of claims made in Palazzo et al. (2024), a TPAMI response to an earlier comment by Bharadwaj et al. (2023) about temporal confounds in EEG-based visual decoding experiments. The paper identifies specific factual inaccuracies in Palazzo et al. (2024) regarding session durations, cross-subject variability claims, and the number of subjects in cited studies; provides new experimental evidence (Section 7) showing that frequency-domain supertrial averaging does not change the core conclusion that EEGChannelNet operates at chance on non-confounded data; and offers a methodological critique of the blank-screen (BDB) analysis used to argue against temporal confounds.

## Strengths

1. **Verifiable factual corrections (Sections 4, 5, 6).** The paper identifies specific, concrete errors in Palazzo et al. (2024) by citing the original sources: the session duration in Spampinato et al. (2017) is 350 s (~5 min 50 s), not "about 4 minutes" (Section 4); the claim that Li et al. (2021) "observe large subject-to-subject variability" is based on block-run tables that Li et al. themselves argued are confounded, while the randomized-trial results do not show statistically significant above-chance accuracy (Section 5); and Bharadwaj et al. (2023) report results on 7 subjects total, not a single subject (Section 6). These are clear, verifiable corrections to the scientific record.

2. **New experimental evidence (Section 7).** The paper performs a new analysis constructing supertrials via frequency-domain averaging (FFT-based, averaging magnitude and phase separately) and re-running the classification benchmark from Bharadwaj et al. (2023, Table 1 left). Table 1 shows EEGChannelNet remains at chance across all supertrial sizes while several other methods (SVM, 1D CNN, EEGNet, SyncNet) remain above chance in multiple configurations, directly testing and refuting the claim that Bharadwaj et al.'s results are artifacts of time-domain averaging.

3. **Methodologically precise critique of the BDB analysis (Section 8).** The paper correctly identifies that the BDB blank-screen analysis in Palazzo et al. (2020b) tests between-run temporal correlations (with temporal distances of 25–35 s between blank screens and stimulus periods), not the within-run correlations (0.5–25 s stimulus-to-stimulus distances within a block) that drive the original high accuracies. This distinction is a valid and specific methodological point.

## Weaknesses

### Fatal
None.

### Major

1. **The incremental contribution beyond prior work is narrow, and the paper overclaims its scope in the ethics statement.** The paper's core function is defending an existing position within a highly specialized debate about EEG experimental design confounds. The position itself — that block-design EEG experiments have a temporal confound and that interleaved designs do not suffer from the same flaw — was already staked out in Li et al. (2021) and Bharadwaj et al. (2023). The incremental value is: (a) correcting a handful of factual errors in one response paper, and (b) one new experiment (Section 7). Importantly, the ethics statement claims "this work debunks nearly one hundred published papers whose results are based on the same confound" (line 301) and lists ~100 papers (lines 337–357), but this sweeping assertion is not supported by evidence presented *in this paper*. The paper only directly engages with Palazzo et al. (2024); it does not analyze each listed paper to demonstrate that they individually suffer from the confound. This overclaim inflates the paper's demonstrated significance and invites judgment by a standard the paper does not meet. (Minor: the problem is not the claim itself — it may be substantiated by prior work — but presenting it as something *this paper* debunks.)

### Minor

1. **Internal inconsistency in Section 7 between the text and figure description.** The text states that frequency-domain averaging "does not attenuate higher-frequency components. In fact, it amplifies them" (lines 151–152). The Figure 1 caption states: "All spectra show a general downward trend as frequency increases, with the raw trials having the highest power and the 100 supertrial size having the lowest power" (lines 168–171). If raw trials have the highest power across all frequencies and supertrials have lower power, the method has not amplified anything — it has reduced power uniformly. The intended claim (that frequency-domain averaging preserves spectral shape rather than disproportionately attenuating high frequencies) is correct and valuable, but the "amplifies" wording is an overstatement that contradicts the caption. This does not invalidate the experimental results in Table 1, but it is an error in the paper's own description of its most novel contribution.

2. **The paper does not contextualize the practical significance of its own results.** The paper refutes claims about supertrials and confounds but never steps back to ask what the results mean. EEGNet achieves up to 9.5% on a 40-class task (2.5% chance) — is this meaningful for real-world BCI? How do these accuracies compare to behavioral benchmarks or practical usability thresholds? The paper stays entirely within rebuttal mode and misses the opportunity to help readers understand the broader implications of the debate.

### Trivial
None.

## Nice-to-Haves

- **Direct comparison of frequency-domain vs. time-domain supertrial results.** The paper introduces frequency-domain averaging but never presents the original time-domain results from Bharadwaj et al. (2023) in the same table for direct comparison. Presenting both would let readers see whether frequency-domain averaging produces higher, lower, or equivalent accuracies.
- **Confidence intervals on Table 1.** At larger supertrial sizes, the number of test samples shrinks considerably, introducing quantization noise. Confidence intervals (rather than binomial significance stars alone) would strengthen the analysis.
- **A more carefully scoped ethics statement** that separates what this paper itself establishes from what prior work established, rather than making a sweeping claim about ~100 papers that the paper does not individually analyze.

## Removed Points

These points were raised in the input review but are removed per the filtering rules:

- *"The paper does not make a contribution appropriate for ICLR"* — This is a venue-fit judgment rather than a specific, factual weakness about the paper's content. The paper's limited scope is already captured in weakness #1 under Major.
- *Criticism that the paper does not address whether the interleaved design has limitations* — The paper does address this in Section 8 (lines 203–211), arguing that any issues would underestimate rather than overestimate accuracy. Whether one agrees with this argument, it is present, so the criticism is not accurate as stated.
- *"No statistical comparison of frequency-domain vs. time-domain supertrial methods"* — While this is a valid suggestion, it is moved to Nice-to-Haves because it asks for additional work rather than identifying a flaw with what is presented.
- *Criticism that classification accuracy as evidence of attention is weak* — The paper also provides the N1-P2 evoked-response evidence from Ahmed et al. (2021) as primary support, so the attention claim does not rest on classification accuracy alone.

## Novel Insights

None beyond the paper's own contributions. The most insightful observation from the review process is the inconsistency between the text claim that frequency-domain averaging "amplifies" high-frequency components and the figure caption stating raw trials have the highest power across the spectrum. This is a genuine error that points to an overstatement in how the paper describes its most novel experimental contribution. The review also surfaces the disjuncture between the paper's modest scope (correcting a few claims in one response paper) and the sweeping ethics statement claiming to debunk ~100 papers — a gap worth noting but ultimately a framing issue rather than a technical flaw.

## Suggestions

1. Fix the inconsistency in Section 7: replace "amplifies them" with language about preserving spectral shape (e.g., "does not disproportionately attenuate higher-frequency components relative to lower-frequency ones").
2. Rewrite the ethics statement to clearly separate what the present paper demonstrates from what prior work has demonstrated, and avoid claiming credit for debunking papers the present work does not analyze.
3. Add a brief discussion contextualizing the practical significance of the obtained accuracy levels (e.g., what 9.5% on a 40-class task means relative to behavioral benchmarks or real-world BCI requirements).

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>