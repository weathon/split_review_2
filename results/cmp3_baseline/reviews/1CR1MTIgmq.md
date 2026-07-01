## Summary

This paper is a point-by-point rebuttal of claims made in a recent TPAMI response (Palazzo et al., 2024) that had criticized earlier work by Bharadwaj et al. (2023) and Ahmed et al. (2021) on EEG-based object classification. The authors argue that several claims in Palazzo et al. (2024) are unfounded, inaccurate, misleading, false, or invalid, supporting each argument with direct quotations from the cited works and one new analysis using frequency-domain supertrial averaging. The paper aims to defend the validity of the interleaved-design EEG experiments and to expose what it calls a temporal confound in the block-design protocols that underlie dozens of published papers.

## Strengths

- **Clear, well-structured argumentation**: Each claimed error is presented in a separate section with the original claim quoted verbatim, followed by counter-evidence drawn from published text and data. This makes the paper easy to follow and allows the reader to verify claims directly.
- **Uses direct evidence from primary sources**: The paper does not rely on reinterpretation but repeatedly cites specific passages, tables, and figures from the original papers (e.g., Bharadwaj et al. 2023, Ahmed et al. 2021, Li et al. 2021) to support its rebuttals. This gives the arguments a strong evidentiary basis.
- **Provides a new control analysis**: Section 7 includes a new experiment where supertrials are constructed via frequency-domain averaging to show that the attenuation of high frequencies is not an inherent property of supertrial methods, partially refuting a claim by Palazzo et al. (2024). Table 1 replicates the original findings under this alternative construction.

## Weaknesses

### Fatal
None.

### Major
1. **The paper is a rebuttal of a rebuttal and does not present a novel research contribution to machine learning.** Its content consists entirely of correcting claims in a prior response paper. While the arguments may be technically sound, the paper does not introduce new methods, datasets, theory, or significant empirical findings that advance the field. For a top venue like ICLR, the contribution is too narrow and niche to be of broad interest or impact. The paper reads more like a comment or letter to the editor than a research paper suitable for a conference that values original ML contributions.

2. **The new analysis in Section 7 only partially addresses the criticism about supertrial spectrum attenuation.** The original claim by Palazzo et al. (2024) concerned time-domain averaging acting as a low-pass filter due to phase inconsistency—a well-known property. The paper constructs supertrials via frequency-domain averaging (averaging magnitude and phase separately) and shows that this does not attenuate higher frequencies. While this demonstrates that the supertrial concept can be implemented without high-frequency loss, it does not refute the claim for the time-domain averaging method actually used by Bharadwaj et al. (2023). The paper claims the original statement is "invalid" but this is too strong; the original statement is valid for the specific method employed, even if alternative methods exist.

3. **The paper assumes extensive familiarity with a prolonged debate in the EEG community** (Spampinato et al., Kavasiidis et al., Palazzo et al., Li et al., Ahmed et al., Bharadwaj et al., and many others). A reader without deep knowledge of this literature will struggle to evaluate the arguments or appreciate their importance. This significantly limits the paper’s audience and impact at a general ML conference.

4. **The Ethics Statement makes sweeping, unsubstantiated claims**. It asserts that "nearly one hundred published papers" are flawed due to a temporal confound, lists dozens of references, and claims direct medical harm to people with disabilities. While the temporal confound in block designs may be real, the paper provides no evidence that the listed papers all use confounded data, that their results are wrong, or that any actual harm has occurred. This section reads as advocacy rather than rigorous scholarship and undermines the paper’s scientific tone.

### Minor
- Some of the arguments rely on the authors’ interpretation of what constitutes a "confound." Section 8 argues that Palazzo et al. misuse the term and then provides a definition, but the debate about whether interleaved designs introduce their own confounds (e.g., task-switching effects, attentional modulation) is not fully addressed.
- The paper could be more self-contained: it frequently references the same few sources without summarizing the experimental protocol for readers unfamiliar with them.

### Trivial
- Figure 1 caption describes the plot in detail but the plot itself is missing from the text (OCR artifact). This is understandable but means readers cannot verify the spectrum claim from the figure.

## Nice-to-Haves

- A direct comparison of time-domain vs. frequency-domain supertrial spectra on the same data would have made the Section 7 refutation much stronger.
- The paper could have briefly summarized the experimental protocols of Spampinato et al., Ahmed et al., and Li et al. in a table to aid readers unfamiliar with the debate.
- If the authors intended this as a position paper, they could have framed it more constructively—e.g., as a call for methodological rigor in EEG-based classification—rather than as a point-by-point rebuttal.

## Novel Insights

None beyond the paper’s own contributions. The observation that frequency-domain supertrial averaging preserves high-frequency information is a minor technical point. The core claim that block-design EEG datasets contain a temporal confound has already been established in prior work (Li et al. 2021, Ahmed et al. 2021, Bharadwaj et al. 2023).

## Suggestions

1. If the authors wish to submit this work to a conference like ICLR, they should reframe it as a research paper with a positive contribution—e.g., a systematic analysis of confounds in EEG-based visual decoding, accompanied by a new carefully-controlled dataset or a novel method for removing temporal confounds. As-is, the paper is a rebuttal that belongs in a journal correspondence section or an archival comment venue.

2. The list of "nearly one hundred papers" in the ethics statement should be substantiated with a per-paper analysis showing that each indeed used the confounded protocol and drew conclusions that could not be supported. Without such analysis, the claim is unacceptably broad.

## Score and Decision

The paper is well-written and its individual arguments appear logically sound, but its contribution is that of a rebuttal letter, not a novel research paper. It does not advance machine learning methods, theory, or empirical understanding beyond a narrow debate. The new analysis is minor and does not fully resolve the criticized point. For ICLR, the paper lacks the novelty, breadth, and significance expected of an accepted submission.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>