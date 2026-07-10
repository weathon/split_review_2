Now let me compile the final authoritative review.

## Summary

This paper presents a detailed re-analysis of "Turning Up the Heat: MIN-P Sampling for Creative and Coherent LLM Outputs" (Nguyen et al., 2024), an ICLR 2025 Oral paper. The re-analysis examines four lines of evidence from the original paper (human evaluations, NLP benchmarks, LLM-as-a-Judge evaluations, and community-adoption claims) and identifies specific, documented flaws: omitted data, incorrect statistical testing, mischaracterized qualitative feedback, unsubstantiated and retracted claims, and methodological ambiguities. The paper also contributes a "Best-of-N" analysis methodology for fairly comparing sampling methods by controlling for hyperparameter search volume. The core finding — that the original paper's evidence does not support its claims of min-p's superiority — is well-supported.

## Strengths

- **Specific, documented flaws in the original paper.** The paper identifies: (i) omission of 1/3 of human evaluation data (basic sampling scores) without justification, confirmed by the original authors; (ii) incorrect statistical analysis (pooling over conditions, no multiple-comparison correction), with re-computed one-sided t-tests showing only 1 of 12 comparisons survives Bonferroni correction; (iii) mischaracterization of qualitative feedback, with manual annotation showing basic sampling was preferred by more evaluators than min-p; (iv) unsubstantiated and retracted community-adoption claims (54k repositories, 1.1M stars). Each finding is grounded in the original paper's own released data and is publicly verifiable.

- **Extensive re-benchmarking with a methodological contribution.** The paper reports ~6000 A100-hours of hyperparameter sweeps across 9 models, 4 samplers, 31 temperatures, and 3 seeds. The "Best-of-N" analysis that equalizes hyperparameter search volume across samplers is a genuinely useful methodological contribution — it provides a principled way to detect whether a method's reported advantage comes from the method itself or from searching a larger hyperparameter space.

- **Transparency and engagement with original authors.** The paper documents correspondence with the original authors, notes where they confirmed issues (omitted data, retracted adoption claims, changed hyperparameters in new human evaluation), and updates claims based on that correspondence. This strengthens the credibility of the critique.

## Weaknesses

### Major

- **The NLP benchmark analysis covers only GSM8K, not GPQA, despite the original paper evaluating both.** The abstract states "Extensive hyperparameter sweeps on NLP benchmarks show min-p's claimed superiority vanishes" (plural "benchmarks"), which overstates coverage. The paper transparently notes this is due to compute budget (line 150: "Due to our compute budget, we only evaluated GSM8K CoT"), but the abstract and conclusions should explicitly scope the benchmark conclusion to GSM8K rather than implying full coverage. The original paper claimed superiority on both GSM8K and GPQA, so the re-analysis is incomplete. This does not undermine the core finding on GSM8K, but it limits the generality of the headline claim.

- **The selective-reporting allegation (Section 4.3) relies on a Telegram link that is not independently verifiable in the paper.** The paper states that the original paper's first author shared a Telegram link showing the higher of two win rates was reported for min-p (52.01 vs. 50.14) but the lower for top-p (50.07 vs. 50.43). For an imputation as serious as selective reporting, the evidence chain should be documented as an archival screenshot or persistent record, not merely described from a private communication channel. This is fixable — the authors can archive the relevant data.

### Minor

- **The claim about reviewers being influenced by retracted community-adoption numbers (line 204) is stated without direct citation to the reviews themselves.** The paper says "3 of 4 ICLR 2025 reviewers and the Area Chair identified these retracted community adoption numbers as the main justification for their strong endorsement" without quoting from or citing the reviews. Providing excerpts would strengthen the point.

- **The conclusion that "min-p sampling improves neither quality, nor diversity, nor the trade-off" is somewhat stronger than the evidence strictly supports.** What the evidence shows is that the original paper's claims are unsupported and that min-p is statistically indistinguishable from baselines under proper controls. "Indistinguishable" and "does not improve" are different claims — the latter is a definitive negative finding that would require more statistical power to establish. The paper's own limitation statement (line 210: "new evidence might lead to different conclusions") acknowledges this implicitly, but the abstract and conclusions do not carry this nuance. A phrasing like "does not reliably outperform" would be more precise.

- **The "blueprint" framing (title, abstract, Section 6) over-reaches relative to what a single case study can support.** The six "General Lessons" are standard best practices in empirical science (correct for multiple comparisons, release data, ensure reproducibility, scrutinize qualitative summaries). The paper's genuine novelty is in the depth and specificity of the documented failures, not in the novelty of the methodological principles. A more accurate framing would be "a case study demonstrating how violations of established principles can undermine published claims."

### Trivial

- The paper lacks a formal reproducibility statement for its own re-analyses (where its analysis code and derived data will be released). Given the paper's thesis about transparency, this is an ironic omission that should be fixed.

## Nice-to-Haves

- Including effect sizes for the human evaluation comparisons would allow readers to assess whether observed (non-significant) differences are practically meaningful.
- The paper could benefit from a brief explanation of why LLM intransitivity (cited from Xu et al., 2025) is particularly problematic here, rather than just citing it.

## Removed Points

These points were flagged in the input review but are removed from the main assessment with justification:

1. **Criticism about GPQA gap being "evidential/methodological gap" that should be acknowledged more prominently in abstract.** This is retained but demoted from the harsh critic's severity level — the paper does acknowledge it inline, and the core finding on GSM8K is solid. The abstract overstates slightly but the limitation is not concealed.

2. **Criticism about the paper lacking a formal reproducibility statement for its own re-analyses.** This is a valid suggestion but more of a nice-to-have than a real weakness; the paper provides substantial methodological detail.

3. **Criticism about no discussion of effect sizes.** This is a methodological preference, not a flaw. The paper's statistical analysis (t-tests, confidence intervals) is appropriate for its claims.

4. **Criticism about missing argument depth for intransitivity claim (Section 4.1).** The paper cites Xu et al. (2025) which is sufficient; additional explanation would be helpful but is not required.

5. **Section-by-section presentation preferences** (Introduction reading as a list, Section 5 claim lacking citation) — the latter is already retained as a minor weakness; the former is a stylistic preference.

## Novel Insights

None beyond the paper's own contributions. The review confirms the paper's core findings — omitted data, incorrect statistics, retracted claims — but does not surface additional insights beyond what the paper itself presents.

## Suggestions

1. **Address the GPQA gap:** Run a smaller-scale replication on GPQA (fewer models, fewer seeds) or explicitly revise the abstract and conclusions to scope the benchmark claim to GSM8K only.
2. **Archive the Telegram evidence:** Save a screenshot or archival snapshot of the referenced Telegram data for independent verification of the selective-reporting claim.
3. **Provide review excerpts:** If the ICLR reviews are accessible, include the relevant excerpts showing that reviewers cited retracted community-adoption numbers as justification.
4. **Add a reproducibility statement** noting where the re-analysis code and derived data will be released.
5. **Reframe the contribution:** Consider re-titling from "blueprint" to a framing like "A Case Study in Scientific Rigor: Re-Analyzing min-p Sampling" to better match the paper's actual contribution.

## Score and Decision

**Calibration report:**

| Anchor Paper | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| Is Memorization Actually Necessary for Generalization? (lf8QQ2KMgv) | 3.75 | R1 | Yes | Similar re-analysis paper but weaker: only 1 dataset, no novel methodology, unfounded subpopulation critique. Current paper is substantially stronger. |
| Is Memorization Actually Necessary for Generalization? (GbEmJmnQCz) | 4.40 | R1 | No | Same paper, different review set. Confirms the 3.75-4.40 range for re-analyses that lack strong positive contribution. |
| On Evaluating Durability of Safeguards for Open-Weight LLMs (fXJCqdUSVG) | 6.50 | R1 | Yes | Evaluation critique paper with strong empirical rigor. Current paper is comparable in rigor but targets a narrower claim. |
| Never Train from Scratch (PdaPky8MUn) | 8.00 | R1 | Yes | Strong re-analysis with clear positive finding (SPT works). Current paper is less impactful — it finds flaws but offers no new positive method. |
| LLMs Cannot Self-Correct Reasoning Yet (IkmD3fKBPQ) | 6.75 | R2 | Yes | Critical re-examination of a claimed general capability. Current paper is somewhat less impactful (targets a specific method, not a general claim) but has more concrete documented findings. |
| Interpretability Illusion for Subspace Activation Patching (Ebt7JgMHv1) | 6.33 | R2 | Yes | Identified illusions in a widely-used method. Comparable in structure to current paper. Current paper has more empirical scale. |

**Round-1 bracket:** 4.0–6.5
**Round-2 narrowing:** The paper is substantially stronger than the "Is Memorization" anchors (3.75–4.40) due to more verified findings, a methodological contribution, and extensive empirical work. It is comparable to the "Interpretability Illusion" paper (6.33) and somewhat weaker than "LLMs Cannot Self-Correct" (6.75) because it critiques a specific method rather than a general capability and has evidentiary gaps (GPQA scope gap, Telegram link). Comparing favorability-rated items: the paper's strongest items (re-benchmarking effort at 16.29, contribution to self-correction at 14.63) are competitive with the 6.0-7.0 range anchors, while its weaknesses are less severe (most in positive favorability territory) than anchors at the same level. The most damaging weakness is the blueprint framing (-2.37), which is milder than the title-claim weakness in "LLMs Cannot Self-Correct" (-4.67).

**Final score: 6.0.** The paper makes a meaningful contribution to scientific self-correction. The core findings — omitted data, incorrect statistics, retracted claims — are well-documented and individually sufficient to cast doubt on the original paper's conclusions. The Best-of-N method is a useful methodological addition. The weaknesses (GPQA scope gap, Telegram evidence chain, overclaiming in conclusions) are addressable and do not undermine the paper's central contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>