Now let me compile my final review.

**Round 1 Bracket:** Based on the anchors, particularly the "Is Memorization Actually Necessary for Generalization?" papers (avg 3.75 and 4.40 — closest in being critical commentaries) and the CALM paper (3.50), I estimate our paper sits in the **2.5–4.0** range.

**Narrowing to Final Score:** The memorization paper at 3.75 addressed a foundational ML question (memorization-generalization) with broad relevance and was rejected as too minimal. Our paper is even narrower — it rebuts seven claims in a single response paper within a field-specific EEG debate and contributes no new methodology, theory, or broadly applicable finding. Our paper also has the additional Ethics Statement overclaiming issue. Comparing scored items: both papers have similarly high-magnitude strengths and weaknesses (our two major weaknesses both scored -10.00, the memorization paper's "minimal contribution" scored -9.96). The distinguishing factor is topical breadth — the memorization paper engaged a community-wide question, while our paper serves a narrow prior exchange. This places our paper slightly below the 3.75 anchor, at **3.0**.

---

## Summary

This paper is a point-by-point critical rebuttal of seven specific claims made in Palazzo et al. (2024), a TPAMI response to an earlier comment (Bharadwaj et al., 2023) about confounds in block-design EEG experiments for visual decoding. Each section quotes the contested claim and provides counter-evidence from the original sources, and Section 7 contributes a new control experiment (frequency-domain supertrial averaging with Table 1 of classification results). The paper also includes an Ethics Statement that makes broad claims about nearly 100 published papers being flawed.

## Strengths

- **Well-documented rebuttal with specific evidence.** Each section directly quotes the contested text from Palazzo et al. (2024), then provides counter-evidence with page-specific citations and direct quotations from Bharadwaj et al. (2023), Ahmed et al. (2021), and Li et al. (2021). The reader can see exactly what claim is being contested and on what basis.

- **New analysis in Section 7 (frequency-domain supertrial averaging).** The paper constructs supertrials by averaging magnitude and phase independently in the frequency domain and replicates the classification analysis from Bharadwaj et al. (2023, Table 1 left) on the Ahmed et al. (2021) data. Table 1 shows EEGChannelNet remains at chance while EEGNet and SyncNet remain above chance for various supertrial sizes, providing relevant evidence for the debate.

- **Clear factual corrections.** Sections 4 and 6 identify demonstrably inaccurate claims in Palazzo et al. (2024): the session length (claimed "about 4 minutes" vs. 350s = 5 min 50s stated in the original papers' own tables) and the number of subjects (claimed "one subject only" vs. 7 subjects actually reported in Bharadwaj et al. 2023). These are specific, verifiable corrections.

- **Valid methodological point about the BDB analysis (Section 8).** The paper correctly identifies that Li et al. (2021) discusses two types of temporal confound (within-block and between-block) and that the BDB blank-screen analysis in Palazzo et al. (2020b) measures only the weaker between-block kind, not the stronger within-block kind that drives the high accuracy in Spampinato et al. (2017).

## Weaknesses

### Fatal
None.

### Major

- **The paper's contribution is too narrow for a major ML conference.** This is a point-by-point rebuttal of a single published response in a field-specific debate about EEG experimental design and confounds. It is entirely backward-looking (defending prior claims rather than advancing new knowledge) and entirely field-specific (the debate concerns confounds in block-design EEG experiments). Even the new analysis in Section 7 is a control experiment in service of defending prior work, not a methodological contribution that stands on its own. The paper does not propose a new method, dataset, theory, or broadly applicable finding that would justify presentation at ICLR. A reader who has not followed the multi-paper debate (Bharadwaj et al. 2023 → Palazzo et al. 2024 → this paper) would lack the context to evaluate the claims. This paper's proper venue is a journal comment section or a preprint server, not a major ML conference proceedings.

- **The Ethics Statement makes sweeping claims far beyond what the paper demonstrates.** The Ethics Statement (Section 10) claims the paper "debunks nearly one hundred published papers" (lines 301, 337–356), describes a research community that "churn[s] out a plethora of flawed results," and alleges direct ongoing harm to people with disabilities. However, the paper's evidence is limited to rebutting seven specific claims from a single response paper (Palazzo et al., 2024). The paper does not evaluate the nearly 100 cited papers individually. This mismatch between the modest evidence base and the sweeping claims about systemic misconduct and harm undermines the paper's credibility and is inappropriate for a conference paper.

### Minor

- **Section 7 rebuts a claim about time-domain averaging by substituting frequency-domain averaging.** Palazzo et al.'s claim was that the *time-domain* supertrial method used by Bharadwaj et al. (2023) attenuates high frequencies. The paper shows that *frequency-domain* averaging does not attenuate high frequencies, but this does not directly establish that the original time-domain method lacked this property. The rebuttal is partial and this gap should be acknowledged.

- **Table 1 lacks variance measures.** The table reports classification accuracies for 8 methods × 11 supertrial sizes but only flags significance via a binomial CDF threshold. No measure of variability (standard deviation, confidence intervals) is reported, which is standard for ML classification tables and would help assess the reliability of the reported accuracies.

- **The claim about signal bleeding (Section 2) is asserted without quantitative support.** The paper states that "1 s blanking between trials is likely to preclude significant signal bleeding" (line 31) but provides no quantitative analysis or citation to support this. The temporal dynamics of ERP components like P300/N400 are well-studied; a quantitative estimate of residual energy given the 3s ISI would strengthen the argument.

### Trivial
None.

## Nice-to-Haves

- A direct analysis of whether *time-domain* supertrial averaging selectively attenuates higher frequencies (e.g., the ratio of high-frequency to low-frequency power before and after averaging), rather than substituting a frequency-domain analysis.
- Variance or confidence interval measures for Table 1.

## Removed Points

The following points from the input review were removed with justification:

1. **Criticism about the title/tone undermining credibility** — The harsh critic claimed the polemical title and framing are inappropriate. This is primarily a stylistic judgment. The substantive concern about the Ethics Statement overclaiming is already captured in a Major weakness above. The additional claim that tone erodes scientific credibility is a style critique, not a verifiable scientific weakness.

2. **Claimed internal inconsistency in Figure 1** — The harsh critic argued the caption and text contradict each other (caption says larger supertrials have lowest power, text says high frequencies are amplified). However, the caption describes overall power (vertical offset), while the text claim about amplification refers to relative frequency content (spectrum shape). Without seeing the actual figure, the claimed contradiction is unverifiable and reflects a confusion between overall power reduction and frequency-specific attenuation.

3. **Missing code/data availability statement** — The parser strips the end of all papers, so this cannot be verified from the available text. Per review guidelines, this criticism is removed.

4. **Section 3 conflating signal information with semantic processing** — The paper's rebuttal responds to a specific concern about inattentiveness being a fatal flaw. The claim that above-chance accuracy demonstrates attention is reasonable in context, and the paper provides additional supporting evidence (N1-P2 onset responses from Ahmed et al. 2021). This is not a genuine weakness.

5. **APA definition being pedantic (Section 8)** — A minor point about terminology conventions across fields; not substantive.

6. **Section 5 noting argument depends on accepting confound position** — This is an observation about the nature of a standing debate, not a weakness of the paper.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface a novel observation that the paper itself does not already articulate.

## Suggestions

1. The most significant recommendation is about venue: this paper is a well-executed rebuttal but makes a contribution more appropriate for a journal comment section or preprint server than a major ML conference. If submitting to a conference, the authors should frame the work around a broadly applicable methodological insight rather than a point-by-point rebuttal of one paper.

2. Either remove or drastically restructure the Ethics Statement to match the evidence the paper actually presents — the specific rebuttal of seven claims from Palazzo et al. (2024) — rather than making sweeping claims about nearly 100 papers that are not individually evaluated.

3. Directly address the time-domain supertrial averaging concern by analyzing whether time-domain averaging selectively attenuates higher frequencies relative to lower frequencies, rather than substituting a frequency-domain analysis.

4. Add variance measures (standard deviation or confidence intervals) to Table 1.

## Score and Decision

**MY FINAL SCORE:** <score>3.0</score>
**MY FINAL DECISION:** <decision>Reject</decision>