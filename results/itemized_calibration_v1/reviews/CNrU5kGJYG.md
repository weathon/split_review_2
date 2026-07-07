## Summary

This paper presents TrojanTO, the first action-level backdoor attack specifically designed for trajectory optimization (TO) models (Decision Transformer, Graph Decision Transformer, Decision ConvFormer) in offline RL. Unlike prior RL backdoor attacks that rely on training-time reward manipulation (which the paper demonstrates is ineffective for TO models), TrojanTO operates as a post-training attack via fine-tuning with a learned trigger. It employs three components — trajectory filtering, batch poisoning, and alternating training — achieving high attack success rates with a very low poisoning rate (0.3% of trajectories). The method is evaluated across three TO architectures, six D4RL environments, three target action types, and three random seeds.

---

## Strengths

1. **Well-motivated problem framing with genuine novelty.** The paper correctly identifies that existing RL backdoor attacks target Bellman-equation-based agents, while TO models operate on fundamentally different principles (sequence modeling, reconstruction loss). The post-training threat model (Section 3.3) is a genuine contribution — all prior work operates at training time, and the threat-model taxonomy (pre-training / during-training / post-training) is clear and useful. This is the first paper to study action-level backdoors specifically for TO models.

2. **Valuable empirical analysis of key factors (Section 4).** The systematic investigation of target action selection, trigger design, and reward manipulation is the paper's strongest analytical contribution. The finding that reward manipulation is largely irrelevant for TO model backdoors (Figure 1) is cleanly demonstrated and follows from architectural properties. The observation that target action type dramatically affects ASR (Table 1: '0' vs '1' in Walk yields 0.110 vs 0.993) is important and justifies the paper's multi-target evaluation protocol.

3. **Broad and systematic evaluation.** The paper tests across three TO architectures (DT, GDT, DC), six D4RL environments spanning locomotion, navigation, and manipulation, three target action types, and three random seeds. This is more thorough than typical for a security paper in this area. The ablation study (Table 5) provides useful decomposition of which components contribute most to efficacy vs. stealth.

4. **Very low data requirement.** Achieving meaningful attack success with 0.3% of trajectories (versus Baffle's 10%) is a strong empirical result that underscores the practical threat.

---

## Weaknesses

### Major

1. **Baseline comparison inflates the claimed advantage.** The paper compares TrojanTO against Baffle (a pre-training data-poisoning attack that must train from scratch) and IMC (originally proposed for image classification). The headline claims — "105% improvement over Baffle" and "27.2% gain over IMC" — are factually correct given the numbers in Table 4, but the comparisons are asymmetric: Baffle fights full training dynamics from random initialization, while TrojanTO fine-tunes a converged model. The paper lacks a simple fine-tuning baseline that removes all TrojanTO-specific components (TF, BP, AT) and uses only the backdoor loss under the same data budget. Such a baseline would directly answer whether the method's complexity is warranted and would provide a fairer reference point. The ablation study (Table 5) partially addresses this by removing one component at a time, but the "w/o" variants are still TrojanTO-specific designs rather than independent baselines. This does not invalidate the core contribution, but it overstates the margin over prior work. **(Paper lines 264–270)**

2. **Trigger dimensions are selected via pilot experiments on evaluation environments with no principled selection mechanism.** The paper tests trigger dimension choices on HalfCheetah and Walker2d (Table 2), finds that (1,2,3) works best, then fixes this choice for *all* environments including AntMaze, Kitchen, and Pen. Table 2 shows that trigger dimension choice causes ASR to vary from 0.000 to 0.915 — the difference between complete success and complete failure. The Ant results (ASR only 0.296 for DT in Table 4) may partly reflect suboptimal trigger dimensions. The paper mentions "Additional attempts at dimension selection methods are detailed in Appendix F" (line 138), but the main text does not describe a principled, automated mechanism for selecting trigger dimensions on new environments. Since the method's effectiveness critically depends on this choice, the claim of generality is weakened. **(Paper lines 129–138, Table 2, Table 4 Ant results)**

### Minor

3. **ASR threshold ε is not specified in the main text.** Equation (2) defines ASR using a threshold ε, but the numerical value is never stated in the main paper (lines 1–334). Since actions are continuous vectors, the interpretation of ASR depends critically on this tolerance — a large ε could trivially inflate ASR. The paper references Appendix I for implementation details (stripped by the PDF parser), but this basic experimental parameter should appear in the main text. **(Paper lines 82–86, Equation 2)**

4. **Source of trajectories in the post-training threat model is underspecified.** The paper states the adversary acts "without access to the original training dataset" (line 60) but the method uses "an initial set of N trajectories" (line 174) for trajectory filtering and backdoor training. Where these trajectories come from — a public dataset? collected by the adversary? a held-out portion of the original data? — is never clarified. This does not invalidate the results, but it creates a gap in the threat model specification. **(Paper lines 60, 72, 174)**

5. **Defense analysis is underdeveloped for a security paper.** Section 6.5 lists several defense methods and reports that fine-tuning is the most effective, but provides no quantitative results in the main text — all are deferred to Appendix B.1. The claim that "the other tested methods proved largely ineffective" is unsubstantiated without numbers. For a paper introducing a security threat, the defense analysis should be a first-class component. **(Paper lines 324–326)**

6. **The 0.3% poisoning rate is not precisely defined.** It is stated as a percentage of trajectories, but the denominator is not specified — 0.3% of the original dataset's trajectories? Of transitions? The absolute number of trajectories used is not reported. Since the contrast with Baffle's 10% is a prominent claim (abstract, line 270), the reader needs to know whether the denominators are comparable. **(Paper lines 9, 72, 270)**

### Trivial

7. Some standard deviations of ±0.000 are reported (Table 6, several entries), which is unusual for a stochastic process and may indicate insufficient reporting precision or rounding.

---

## Nice-to-Haves

- Add a straightforward fine-tuning baseline: remove all three TrojanTO-specific components (TF, BP, AT) and simply fine-tune the pretrained model with the backdoor loss, using the same data budget. This would answer whether the methodological complexity is necessary and provide a fairer comparison.
- Either demonstrate that (1,2,3) is consistently optimal across all six environments, or propose a principled mechanism for trigger dimension selection (e.g., a brief automated search on held-out data, or incorporating dimension selection into the learnable trigger optimization).
- Expand the defense analysis with quantitative results in the main text.
- Clarify the source of the "initial set of trajectories" in the post-training threat model.
- Precise definition of the 0.3% poisoning rate (denominator, absolute counts).

---

## Removed Points

- **Questioning Baffle/IMC as baselines entirely:** The critic argued the comparison is "not informative." This is too strong — Baffle is the most relevant prior work in offline RL backdoors, and IMC is the source of the alternating training idea. The comparison is imperfect (pre-training vs. post-training) but still informative. Downgraded from "Evidential" to "Major."
- **"Fatal" classification of trigger dimension selection:** The critic labeled this "Structural" (roughly fatal). However, the paper does reference Appendix F for alternative selection methods, and the method still achieves high ASR on most environments. This is a significant weakness but not fatal. Downgraded to Major.
- **Figure 1 labeling error (w/ RM-4 appearing twice):** This may be a parser artifact from figure extraction; not the authors' error. Removed.
- **Criticism about missing appendix content:** The PDF parser strips appendices from all papers; they exist in the original submission. Removed.
- **Missing related works:** The reviewer lacks external sources to confirm existence of unmentioned works. Removed per guidelines.

---

## Novel Insights

The most interesting observation to emerge is the architectural insight that reward manipulation is near-completely irrelevant for TO model backdoors (Section 4.3), and the bounded persistence duration tied to the model's finite context window (Section 6.3). These are not just empirical observations but follow from the fundamental properties of TO models as conditioned behavior-cloning systems. A second insight is the sharp dependence on target action type: boundary actions yield near-perfect ASR while interior actions can fail (Table 1), suggesting that the choice of attack objective may be more limiting than the attack method itself for practical threat models. The alignment between the critic's observations and the paper's own data is noteworthy: the paper's own data (Ant results, Table 2 variance) already hints at the trigger dimension issue that the critic identifies as a weakness.

---

## Suggestions

1. State the ASR threshold ε explicitly in the main text (single sentence).
2. Add a "vanilla fine-tuning" baseline to ground the comparison fairly.
3. Clarify the trajectory sourcing for the post-training threat model.
4. Either automate trigger dimension selection or add a caveat about environment-specific tuning.
5. Define the 0.3% poisoning rate precisely and report absolute trajectory counts.
6. Include quantitative defense results in the main text (at minimum a summary table).

---

## Score and Decision

**Anchoring:** The Round 1 bracket was [5.5, 6.25]. Compared to the closest anchors:

| Anchor | Avg Score | Comparison |
|--------|-----------|------------|
| em0gAL8fbK — Temporal Logic Backdoor Attacks (offline RL) | 4.00 | Weaker on poisoning rate (too high) and threat model realism. This paper is stronger → above 4.0. |
| ZyPRwskBli — Backdoor in Seconds (model editing) | 4.75 | Fatal-level weaknesses (-5 for "model not modified", -5 for "fine-tuning defeats attack"). This paper has no such fatal issues → above 4.75. |
| HZnnHDrBXD — Action-Manipulation Attack (continuous RL) | 5.75 | Strong theory but weak experiments (-4 for low-dimensional envs). This paper has stronger experiments but no theory. Comparable weakness profiles. |
| S1Bv3068Xt — BALD (backdoor attacks on embodied decision-making) | 6.25 | Strong on novelty (+4) but has -5 from one reviewer for "imaginary threat model." This paper's weaknesses are less severe; but the threat model here is well-grounded in real TO model deployment. |

The paper's strongest shared traits with upper anchors (5.75–6.25) are: genuine novelty as first study of this threat, broad evaluation, and well-motivated problem framing. Its heaviest negative weights relative to those anchors are: imperfect baseline comparisons and lack of automated trigger dimension selection. The paper lacks any fatal-level weakness (no -4 or -5 items), but has two Major weaknesses that meaningfully temper the contributions.

**Final Score: 5.5** — Below "borderline accept" (6) but clearly above "borderline reject" (4). The paper's real contributions (first study of this threat, valuable empirical analysis, low poisoning rate) are undercut by the inflated baseline framing and the unresolved trigger dimension selection issue, which together prevent a clear acceptance recommendation.

**Decision: Reject**

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>