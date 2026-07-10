## Summary

This paper provides a point-by-point rebuttal of claims made in a recent TPAMI response (Palazzo et al., 2024) regarding EEG-based object recognition experiments. It argues that several of Palazzo et al.'s criticisms of Bharadwaj et al. (2023) and Ahmed et al. (2021) are unfounded, inaccurate, or misleading. The paper includes one new experiment (Section 7) using frequency-domain supertrial averaging and identifies factual errors in Palazzo et al. (2024), such as the misstated session length and the false claim that the analysis involved only one subject.

## Strengths

- **Section 7 provides new experimental evidence** (frequency-domain supertrial averaging, Table 1, Figure 1) that preserves high-frequency information and confirms EEGChannelNet remains at chance, directly addressing the claim that the supertrial method was "designed to penalize EEGChannelNet." This is original experimental work.
- **Section 8 makes a valid methodological distinction** between within-run and cross-run temporal correlations, correctly identifying that the BDB confound analysis in Palazzo et al. (2020b) measures the wrong kind of correlation and therefore does not address the original concern from Li et al. (2021).
- **Identifies a clear factual error about the number of subjects**: Section 6 demonstrates that the claim by Palazzo et al. (2024) that the analysis was on "one subject only" is false — Bharadwaj et al.'s Table 1 reports results across 7 subjects (1 from Ahmed et al. 2021, 6 from Li et al. 2021).
- **Systematic quotation-based argumentation**: Every claim the paper addresses is presented alongside direct quotations from both the criticized work and the original sources, providing clear attribution and allowing readers to follow the chain of argument.

## Weaknesses

### Fatal
None. The paper's factual corrections appear accurate, and the Section 7 experiment is real work. However, the weaknesses below collectively make the paper unsuitable for ICLR.

### Major

- **Scope mismatch with ICLR**: The paper is a point-by-point rebuttal of specific claims in a single TPAMI article (Palazzo et al., 2024). It proposes no new ML method, theory, dataset, or generalizable finding about learning systems. Its one experiment (Section 7) exists solely to refute a specific criticism. ICLR publishes original research in machine learning; this commentary belongs in a journal's correspondence section or the same venue where the original exchange occurred (TPAMI).

- **Overclaim in the ethics statement**: The paper claims to "debunk nearly one hundred published papers" and provides a long list, but the paper itself only addresses Palazzo et al. (2024). The debunking of those other papers was done in prior work (Ahmed et al., 2021; Li et al., 2021; Bharadwaj et al., 2023). Attributing this as a contribution of the present paper is misleading.

- **Section 7 experiment overreaches on the signal-processing claim**: Palazzo et al. claimed that time-domain averaging (used by Bharadwaj et al.) attenuates high frequencies — a well-understood property of signal processing. The paper responds by switching to frequency-domain averaging (where magnitude and phase are averaged separately) and showing this *different method* does not attenuate high frequencies, then declares the original claim "invalid." This is a non sequitur. The experiment does provide useful evidence against the "designed to penalize EEGChannelNet" claim (EEGChannelNet remains at chance even with high frequencies preserved), but it does not invalidate the claim about time-domain averaging.

- **Unverifiable empirical claim in Section 5**: The paper asserts that Li et al. (2021) Tables 5, 26–30 "do not differ from chance in a statistically significant fashion" without reproducing the actual numbers, statistical tests, or chance baselines. A reviewer cannot verify this critical claim without accessing and re-analyzing Li et al. (2021).

- **No discussion of the paper's own limitations**: The paper never acknowledges potential issues with its own position — the supertrial method's loss of single-trial information, reduced sample size, statistical implications of averaging, or any limitations of the Ahmed et al. (2021) / Bharadwaj et al. (2023) analysis that could affect its conclusions.

### Minor

- **Section 2 relies on plausibility rather than evidence**: The claim that "1 s blanking between trials is likely to preclude significant signal bleeding" is asserted without any quantitative analysis (e.g., cross-trial correlation statistics). This is a reasonable argument but lacks the empirical rigor that the paper demands from others.

- **Section 4 elevates a small factual discrepancy to a full section**: The session-length error (350s vs. "about 4 minutes") is real but the disproportionate treatment makes the paper feel more like point-scoring than constructive critique.

- **Ethics statement tone escalates beyond the paper's demonstrated scope**: The claims of specific medical harms, the characterization of a research community "knowingly or unknowingly" churning out flawed results, and the statement that the confound allows "proving anything" (line 300) move from scientific critique to polemic without evidence that these specific harms have occurred.

### Trivial
None.

## Nice-to-Haves

- Reproduce the key numbers from Li et al. (2021) Tables 5, 26–30 in the current paper (or its appendix) so the claim about statistical insignificance can be independently verified, making the paper more self-contained.
- In Section 7, either directly compare classification performance using raw trials vs. time-domain supertrials to test whether the attenuation actually matters for classification, or accurately characterize the experiment as testing whether the result holds when high frequencies are preserved (rather than declaring the time-domain averaging claim invalid).
- Acknowledge the trade-offs of the supertrial method (reduced sample size, loss of single-trial dynamics) as the paper demands thoroughness from others but does not practice it itself.

## Removed Points

- "Section 8 is excessively long and gets into the weeds" — Removed as a formatting/style nitpick; the depth reflects the complexity of the confound analysis.
- "The paper is not self-contained in general" — Removed as overbroad. The paper does provide direct quotations for every claim it addresses. The specific unverifiable-claim point (Section 5) is retained as a Major weakness.
- Various presentation/structure complaints — Removed as style preferences.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface any insight that the paper's authors did not themselves articulate.

## Suggestions

1. If the authors wish to pursue this as a publication, submit it to a journal's correspondence section or to TPAMI as a follow-up commentary, not to ICLR.
2. Tone down the ethics statement to match what the paper actually demonstrates: specific factual errors in Palazzo et al. (2024), not a wholesale indictment of ~100 papers.
3. Add a limitations section acknowledging the trade-offs of the supertrial method and the single-subject data collection.
4. Either reproduce the critical numbers from Li et al. (2021) or restrict claims to what can be verified from the quotations provided.

## Score and Decision

The paper identifies some genuine errors in Palazzo et al. (2024) and contains one original experiment, but it is structurally a rebuttal/commentary rather than a self-contained ML research contribution. The scope mismatch with ICLR is decisive: this paper does not propose new ML methods, theory, datasets, or benchmarks, and its experimental work is narrowly focused on refuting a specific claim rather than establishing generalizable knowledge about learning systems. Combined with several overclaims (the "nearly one hundred papers" attribution, the overstated refutation in Section 7, the polemic ethics statement) and the absence of self-critique, the paper is not suitable for ICLR.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>