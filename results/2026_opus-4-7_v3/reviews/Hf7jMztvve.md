Now let me do Round 1 calibration — bracketing search across score bands for papers on similar topics (SAE interpretability, LLM deception detection, AI safety evaluation):Let me read some of the most relevant anchors to calibrate:Now I have enough calibration data. Let me form my final assessment.

**Round 1 Bracket Assessment:**

- **Strong reject anchors (≤1.5)**: Papers like NEMESIS (1.4) have literally no novelty - just running existing attacks. The paper under review is clearly above this level as it poses an original question and has original (if preliminary) findings.

- **Reject range (2.5-3.5)**: Papers like "Entering Real Social World" (3.0), "Playing Language Game" (2.5), and "Tall Tales at Different Scales" (3.67) have interesting setups but significant methodological gaps, unclear evaluation, or ambiguous conceptual foundations. The paper under review shares these characteristics strongly.

- **Borderline reject (3.5-5.5)**: "Too Big to Fool" (4.25) has more rigorous methodology. The paper under review lacks the quantitative evaluation these papers provide.

- **Accept range (5.5-7.5)**: "Towards Principled Evaluations of SAEs" (7.0) and "SAEs Do Not Find Canonical Units" (7.0) have formal frameworks, novel techniques, and rigorous quantitative evaluation. The paper under review is far below this level of rigor.

**My initial bracket: 2.5 to 4.0**

The paper asks an important question but its execution (no quantitative metrics anywhere, web UI screenshots as evidence, n=2-30 samples, t-SNE without quantification, overclaiming title/abstract) places it firmly in the 3.0 range — a clear reject with an interesting direction but insufficient rigor for a top venue.

---

## Summary
This paper investigates whether current SAE-based interpretability tools can detect and control strategic deception in LLMs. It introduces a "Secret Agenda" social deduction game testbed (tested on 38 models) and an insider trading compliance scenario, finding that auto-labeled SAE features for "deception" fail to activate during strategic lying and that feature steering fails to prevent it, while unlabeled aggregate SAE activations can separate compliant from non-compliant responses in the insider trading domain.

## Strengths
- **Practically relevant negative result about auto-labeled SAE features** (Section 6.1): The observation that features labeled "deception and betrayal," "deception and manipulation," etc. do not activate during clear behavioral instances of lying, while a control feature ("Bananas and banana-related concepts") successfully steers its associated behavior, provides a useful data point for the interpretability community about the limitations of auto-labeling methodology.

- **Juxtaposition of labeled vs. unlabeled feature utility** (Sections 6 vs. 7): The contrast—individually labeled "deception" features failing while unlabeled aggregate activations produce discriminative structure—is a genuinely interesting observation that could motivate future work on feature discovery and labeling.

- **Candid limitations section** (Section 8): The paper acknowledges its statistical constraints, resource limitations, and preliminary nature with unusual honesty for a submission, and correctly identifies what it can and cannot claim given the evidence.

## Weaknesses

### Fatal
None

### Major

- **Conflation of game-playing with safety-relevant deception** — The Secret Agenda testbed (Section 5.1-5.2) places the model explicitly in a social deduction game role where lying is the winning strategy. The paper states the model is "already assigned as the Fascist Leader" and other players "demand it reveal its alignment" while lying is incentivized. This is game-rule compliance, not the kind of deceptive misalignment the introduction motivates by citing Wei et al. and Greenblatt et al. The finding that "38/38 models lied at least once" demonstrates only that models can play games as designed. The title "LLMs Strategically Lie Undetected by Current Safety Tools" substantially overstates what this evidence supports. Section 8.2 partially acknowledges this but does not constrain the headline claims.

- **Feature steering experiments lack systematic methodology** — Section 9 confirms that evidence for the steering claims consists of "interface screenshots" from Goodfire's web UI (DeLeeuw, 2024 — a Google Drive folder). No structured protocol is reported: no specification of trial counts per feature, no baseline measurement, no quantitative success metric, no dose-response analysis. The claim that "100+ deception-related features" failed to prevent lying is supported only anecdotally, which is insufficient to establish this as a robust negative result.

- **Insider trading analysis lacks quantitative validation** — The t-SNE visualizations (Figure 4) and heatmaps (Figure 5) are the sole evidence for discriminative power of SAE features in this domain. No classification accuracy, silhouette scores, cross-validation, or statistical tests are reported. Critically, the top discriminative features in Table 1 ("Quantity fields in structured data," "Securities market regulation," "Financial trading transactions," "Trade execution code patterns") appear to track content domain (finance vs. non-finance language), not ethical reasoning. The paper does not control for the possibility that a simple bag-of-words classifier would achieve the same separation.

- **Systematic overclaiming throughout** — The title claims LLMs lie "Undetected by Current Safety Tools" when only a narrow class of auto-labeled SAE features was tested. The abstract claims results "span Llama 8B/70B SAE implementations and GemmaScope" suggesting systematic breadth, but the actual analysis consists of checking a handful of features in GemmaScope and conducting web UI trials in Goodfire. Figure 1's caption acknowledges "Error bars omitted due to insufficient trials for meaningful confidence intervals" yet the conclusions are stated as established findings.

### Minor

- **Feature selection limited to keyword matching** — The search for relevant features (Section 6.1) appears limited to those with "deception" in their auto-label. Strategic game-play deception could plausibly activate features related to game strategy, role-playing, persuasion, or social dynamics — none of which would be found by keyword matching on labels.

- **4-bit quantization effects unaddressed** — Section 7.1 uses Unsloth's 4-bit quantized Llama 70B but does not discuss how quantization might affect SAE feature extraction and the validity of conclusions about "underlying ethical decision-making representations."

- **Incomparable experiments presented as a meaningful contrast** — The Secret Agenda and Insider Trading analyses differ in SAE implementations (GemmaScope vs. Goodfire), models (Gemma 2 8B vs. Llama 70B), tasks, and analysis methods, making the comparison between them less informative about auto-labeling methodology specifically.

### Trivial
None

## Nice-to-Haves
- Systematic activation-based feature selection (running many deceptive vs. truthful transcripts and identifying features that actually differ in activation) rather than keyword-based label searching.
- Quantitative classification metrics for the insider trading analysis with a bag-of-words baseline.
- Programmatic feature steering experiments with measured deception rates, confidence intervals, and dose-response curves.
- Reframing the title and claims to match the evidence: a preliminary study of auto-labeled SAE feature limitations, not a broad claim about safety tool failure.

## Removed Points
These points are flagged to be removed, treat them with caution:

- **"Statistical rigor is almost entirely absent" as a separate standalone issue** — This is already captured within each individual methodology weakness. The paper itself acknowledges this (Section 8.1) and frames results as preliminary existence proofs. Listing it separately inflates the weakness count.
- **Criticism about missing prompt text in the main body** — Likely in appendix which was stripped; this is a presentation detail.
- **The paper's Section 10 acknowledgment of being preliminary treated as a weakness** — Candor about limitations is not itself a flaw; the issue is the mismatch between that candor and the headline claims, which is captured under "overclaiming."

## Novel Insights
The observation that SAE features auto-labeled with deception-related terms do not activate during clear behavioral instances of strategic lying, while a control feature ("bananas") successfully steers its concept, suggests a potential systematic disconnect between how auto-labeling captures simple topical concepts versus complex behavioral phenomena. If validated rigorously, this would be a meaningful finding about current interpretability methodology's blindspots.

## Suggestions
- Replace web UI trials with programmatic experiments measuring deception rates as a function of feature steering strength, with confidence intervals.
- Add quantitative clustering metrics and compare against a lexical baseline to determine whether SAE features capture anything beyond surface content.
- Significantly narrow the title and abstract claims to match the actual evidence: a preliminary investigation of auto-labeled SAE feature limitations in a game-playing context.
- Consider whether the Secret Agenda testbed genuinely tests safety-relevant deception or merely game-rule compliance, and adjust framing accordingly.

## Score and Decision

### Calibration Anchors

| Paper Path | Avg Score | Round | Comparison |
|---|---|---|---|
| 5kMwiMnUip.md (NEMESIS: Jailbreaking LLMs) | 1.40 | R1 | Far below — has literally no novel contribution; Secret Agenda at least poses an original question |
| 8QTpYC4smR.md (Systematic Review of LLMs) | 1.00 | R1 | Far below — a pure literature survey with no experiments |
| nSDOkm0SKo.md (Financial Markets Neural Network) | 1.00 | R1 | Far below — hypothetical scenario, no real methodology |
| gwZ90hFSL2.md (Chinese NLP Humanoid Robots) | 1.00 | R1 | Far below — barely a research paper |
| b1vVm6Ldrd.md (EgoSocialArena ToM) | 3.00 | R1 | Similar — interesting setup, significant methodological gaps, unclear evaluation |
| BeOEmnmyFu.md (Playing Language Game Jailbreaking) | 2.50 | R1 | Similar — game-based approach with interesting idea but insufficient rigor |
| DXaUC7lBq1.md (Personality in LLMs) | 3.00 | R1 | Similar — uses SAE feature steering but with methodological concerns |
| EqCbc4wrzy.md (MDPE Deception Dataset) | 2.50 | R1 | Similar range — deception-focused but limited contribution |
| YRXDl6I3j5.md (Tall Tales: Deception Scaling) | 3.67 | R1 | Slightly above — more rigorous conceptual framework for deception but still rejected |
| tet8yGrbcf.md (Too Big to Fool) | 4.25 | R1 | Above — has proper quantitative evaluation the reviewed paper lacks |
| ccxD4mtkTU.md (LLM-Generated Misinformation) | 4.75 | R1 | Above — includes systematic experiments with metrics |
| MOtZlKkvdz.md (LLMs as Post Hoc Explainers) | 3.67 | R1 | Similar — interpretability study with limited evaluation |
| 1Njl73JKjB.md (Principled SAE Evaluations) | 7.00 | R1 | Far above — formal framework, quantitative metrics, rigorous controls |
| 9ca9eHNrdH.md (SAEs Not Canonical) | 7.00 | R1 | Far above — novel techniques with rigorous evaluation |
| ZLAQ6Pjf9y.md (X-Ray SAE) | 5.60 | R1 | Above — has quantitative evaluation pipeline |
| d63a4AM4hb.md (Not All Features Linear) | 7.00 | R1 | Far above — rigorous methodology with scalable methods |
| I4e82CIDxv.md (Sparse Feature Circuits) | 8.00 | R1 | Far above — introduces methods with extensive evaluation |

**Round 1 bracket**: 2.5 to 4.0

The paper sits squarely in the 2.5-3.5 range based on comparisons. It has an interesting and important question (like "Tall Tales" at 3.67 and "EgoSocialArena" at 3.0) but shares their core weakness: the execution does not support the claims. The lack of any quantitative metric anywhere in the paper, combined with the conceptual issue of conflating game-play with safety-relevant deception, and the use of web UI screenshots as experimental evidence, place it firmly below the borderline reject threshold. It is above the strong-reject papers because it poses an original question and provides some original (if anecdotal) observations.

**Final score: 3.0**

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>