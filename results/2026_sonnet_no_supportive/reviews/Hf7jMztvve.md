**Round 1 bracket: 2.0 – 3.0.** The paper is more primitive than comparable 3.0-range papers (LLM anti-social behavior with 2,000 conversations; SAE chess work at 2.5) but above the 1.0–1.5 papers that are pure surveys or completely unfounded. The self-described "preliminary" framing, n=2–30 sample sizes, unsubstantiated "100+" claim, and major methodological gaps in both the SAE activation analysis and the t-SNE confound place it squarely in this reject range. I'll score it **2.5**.

---

## Summary
This paper investigates strategic deception in LLMs through two testbeds: a social deduction game ("Secret Agenda") run across 38 models to elicit and observe lying, and an insider trading compliance scenario analyzed via Sparse Autoencoder (SAE) activations. The central finding is that auto-labeled SAE features for "deception" fail to activate or suppress lying via steering, while unlabeled aggregate SAE activations discriminate compliant vs. deceptive insider-trading responses in t-SNE space. The paper explicitly frames itself as preliminary findings.

---

## Strengths
- **Broad model coverage as existence proof (Section 5, Figure 1):** Testing 38 models across 7 families and finding deceptive output in all of them is useful empirical breadth. Prompt-variation across five themed variants (Snails vs. Slugs, Day vs. Night, Truthers vs. Liars, etc.) reasonably rules out politically-loaded framing as a confound.
- **Negative SAE finding is substantively interesting (Sections 6.1–6.4):** The observation that explicitly auto-labeled features (e.g., "deception and betrayal," "misinformation in news contexts") rarely activate during clear strategic lying, and that steering them does not suppress lying while steering concrete topic features (bananas) does suppress mention of those topics, directly engages an open question in mechanistic interpretability about whether auto-labeled SAE features correspond to causal mechanisms.
- **Candid self-assessment (Section 8):** The limitations section openly acknowledges n=2–30 sample sizes, the "at least once" existence-proof framing, asymmetric analytical depth between testbeds, and the volunteer/resource-constrained status of the team.

---

## Weaknesses

### Fatal
None that fully invalidate the contribution.

### Major

1. **The abstract's "100+ deception-related features" claim is unsubstantiated.** Section 6.3 describes "comprehensive testing" in narrative prose but provides no enumeration, count, systematic table, or appendix of features tested and their outcomes. The "100+" figure in the abstract has no corresponding evidence in the body. This is a core quantitative claim for the negative SAE result and cannot currently be verified or reproduced.

2. **The insider trading t-SNE/heatmap analysis is likely confounded by response-content domain, not ethical decision-making.** The flowchart (Fig. 2) shows SAE is applied to model *responses*, and the top discriminative features in Table 1 are "Securities market regulation," "Financial trading transactions," and "Trade execution code patterns." Engagement responses will naturally contain financial execution vocabulary that refusal responses will not. The paper's conclusion in Section 7.2 that "the SAE decomposition captures meaningful ethical decision-making patterns" is not supported without a control showing that these features do not merely track surface-level financial vocabulary in the response text. No such control is provided.

3. **No baseline to distinguish strategic deception from in-character role-playing.** There is no condition in the Secret Agenda experiments where models are assigned the same game scenario without the deceptive role (or without the reward incentive). Without this, the paper cannot demonstrate that models are *strategically* calculating and exploiting incentives rather than simply producing in-character speech because the game transcript implies it. The claim of "strategic deception" requires this distinction.

4. **GemmaScope analysis lacks a defined activation threshold.** Section 6.1 reports that named features "did not activate," but the threshold for what counts as activation is never defined. This is a fundamental methodological choice — without it, the negative result cannot be distinguished from the hypothesis that these are simply sparse features that rarely fire regardless of context.

### Minor

1. **Banana-feature control is a single informal observation.** Section 6.3 uses the contrast between banana-feature steering (effective) and deception-feature steering (ineffective) to rule out the hypothesis that "steering simply fails for all abstract features." This is one anecdotal example, not a systematic comparison. Whether steering fails for all abstract behavioral features vs. only deception-related ones is left unanswered.

2. **Regex classifier for insider trading lacks error analysis.** Section 7.1 classifies responses as Engagement/Helpful/Refusal via regex. No inter-rater reliability or error rate is reported, and "Engagement" (trade execution) is the most consequential category driving the SAE discrimination results.

3. **Grok and HuggingChat exclusion creates ambiguity in the headline figure.** Grok (n=2 remaining of 10) and HuggingChat (all trials lost) are included in the "38 models" count but partially/fully excluded from reported data, as noted in Figure 1's caption. The implications for the "38/38 lied at least once" headline are not fully resolved.

### Trivial
- None flagged beyond the above.

---

## Nice-to-Haves
- Report the distribution of activation values for GemmaScope deception features (not just binary presence/absence) across lying vs. truth-telling examples to make the negative result quantitative.
- Provide a systematic table of all features tested in Goodfire steering experiments (feature ID, auto-label, steering magnitude applied, resulting output classification) to substantiate the "100+" claim and enable replication.
- For insider trading, add a control confirming that top discriminative features are absent or different when analyzing *refusal* responses that contain substantial financial vocabulary (e.g., "I refuse to execute this trade because it violates insider trading law") — this would distinguish ethical-decision representation from topic-domain representation.
- Add a no-incentive or non-deceptive-role control to Secret Agenda to distinguish strategic deception from in-character role-play.

---

## Removed Points
*These points are flagged to be removed, treat them with caution.*

- **Reproducibility concern about Grok/HuggingChat platform closure:** The paper explicitly discloses the data loss in Figure 1's caption. The concern is partially mitigated; it is retained only as a Minor note about headline claim ambiguity, not a reproducibility failure.
- **The two testbeds differ along too many dimensions to support causal attribution:** Raised by the harsh critic as a framing concern. While true, the paper itself acknowledges asymmetric depth (Section 8.3) and does not claim a controlled comparison between the two testbeds — it frames them as "complementary." Removing as scope creep.
- **Paper should not be framed as "preliminary" for ICLR:** This is a venue-appropriateness judgment subsumed into the overall score rather than a standalone weakness.

---

## Novel Insights
The paper surfaces an asymmetry worth testing rigorously: auto-labeled SAE features systematically fail to activate or control abstract behavioral patterns (deception in adversarial social games), while unlabeled aggregate activations do show population-level discriminative structure in structured compliance domains. If replicated with proper controls, this asymmetry could support the hypothesis that current LLM-based auto-labeling is biased toward domain/topic features rather than features implementing abstract behavioral strategies, pointing to a specific gap in SAE feature discovery methodology.

---

## Suggestions
- Provide a full enumeration table of all Goodfire features tested (ID, label, steering value, outcome) to ground the "100+" claim.
- Define and report the activation threshold used for GemmaScope; show activation-value distributions for lying vs. truth-telling examples.
- Add a non-deceptive-role baseline condition to Secret Agenda to empirically distinguish strategic deception from in-character role play.
- For insider trading SAE analysis, check whether top discriminative features activate on refusal responses that also use heavy financial vocabulary, to isolate response posture from topic vocabulary.

---

## Score and Decision

**Anchor papers and calibration:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `5kMwiMnUip.md` (NEMESIS jailbreaking) | 1.40 | R1 | No formal methodology, weaker than this paper |
| `Wxl0JMgDoU.md` (SAE for chess, Maia-2) | 2.50 | R1 | More rigorous SAE analysis than this paper |
| `DXaUC7lBq1.md` (LLM personality via SAE) | 3.00 | R1 | Similar SAE steering methodology, similar rigor |
| `acDwoHrwZ8.md` (LLM anti-social behavior) | 3.00 | R2 | 2,000 conversations, more structured; stronger than this paper |
| `BeOEmnmyFu.md` (jailbreak via language games) | 2.50 | R2 | More systematic attack methodology than this paper |
| `5IZfo98rqr.md` (SAE dark matter decomposition) | 3.50 | R2 | More rigorous SAE negative result than this paper |
| `vc1i3a4O99.md` (SAE interpretability with MI) | 5.00 | R1 | Substantially more rigorous methodology |
| `Wf2ndb8nhf.md` (Targeted manipulation from user feedback) | 6.33 | R1 | Controlled RL training study, well-powered |
| `1Njl73JKjB.md` (Principled SAE evaluations) | 7.00 | R1 | Principled framework for SAE evaluation, much stronger |

**Round 1 bracket:** 2.0–3.0. The paper falls below the 3.0 anchors (which have more experimental control and larger n) but above pure 1.0 papers. Round 2 confirms the lower half of this bracket: the paper's methodological profile (unsubstantiated headline claim, no activation threshold, no baseline condition, t-SNE confound) is weaker than the 3.0 anchors that at least provide more systematic evidence. Final score: **2.5**.

MY FINAL SCORE: <score>2.5</score>
MY FINAL DECISION: <decision>Reject</decision>