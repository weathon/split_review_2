## Summary

This paper proposes TrojanTO, the first post-training action-level backdoor attack against Trajectory Optimization (TO) models such as Decision Transformer. The key insight is that existing RL backdoor methods (which manipulate rewards during training) do not transfer to TO models, which use sequence modeling and reconstruction loss. TrojanTO combines trajectory filtering, batch poisoning, and alternating training to implant backdoors with a 0.3% poisoning rate. Experiments across three TO architectures (DT, GDT, DC) and six D4RL environments demonstrate that the attack achieves higher ASR and BTP than baseline methods Baffle and IMC.

## Strengths

1. **Well-motivated problem framing.** The paper correctly identifies that existing RL backdoor attacks (which rely on reward manipulation during Bellman-equation-based training) are fundamentally incompatible with TO models, which use sequence modeling and reconstruction loss. This insight is clearly articulated in Sections 1 and 3 and is the paper's primary intellectual contribution.

2. **Systematic empirical investigation of key factors (Section 4).** The analysis of how target action selection, trigger dimension choice, and reward manipulation affect backdoor efficacy on TO models is informative. The finding that boundary actions yield near-perfect ASR while interior actions perform much worse (Table 1), and that reward manipulation is essentially irrelevant for TO models (Figure 1), are concrete findings that future work must account for.

3. **Impressive attack efficiency.** The reported poisoning rate of 0.3% is substantially lower than the closest prior work (Baffle at 10%), and the attack maintains high BTP across most settings.

4. **Breadth of evaluation.** Testing across three TO architectures (DT, GDT, DC) and six D4RL environments, with results averaged over three target action types and three random seeds, constitutes a thorough evaluation for a first attack paper in a new setting.

## Weaknesses

### Fatal

None.

### Major

1. **ASR threshold ε is not stated in the main paper.** Equation (2) defines ASR using a threshold ε (all components of the predicted action must be within ε of the target), but the numerical value of ε is never specified in the main text. This is not a minor omission — it is a parameter that directly determines every ASR value reported in the paper. Without knowing ε, the reader cannot distinguish whether ASR ≈ 1.0 means "the model outputs actions extremely close to the target" or "the model outputs actions somewhere in the general vicinity of the target." The CP metric inherits this ambiguity. The fact that Tables 6 and 7 show many entries with ±0.000 variance across three seeds (e.g., CP of 0.922 ± 0.000, 0.972 ± 0.000) amplifies this concern, raising the question of whether ε is set so permissively that the metric saturates. The authors should state ε explicitly in the main paper and discuss sensitivity to this choice.

2. **Baseline comparison conflates different threat models.** The paper compares TrojanTO (a *post-training* attack that modifies pretrained model parameters) against Baffle (a *pre-training* data-poisoning attack that injects malicious trajectories into the training set) and IMC (an input-model co-optimization method from image classification). The headline claims — "105% improvement over Baffle," "0.3% poisoning rate vs. 10%" — compare fundamentally different attack capabilities. A Baffle attacker who also had post-training model access would not restrict themselves to Baffle's pre-training strategy. Furthermore, the "poisoning rate" quantities refer to different things: Baffle's 10% is the fraction of the *training dataset* that is malicious, while TrojanTO's 0.3% is the fraction of trajectories used in *post-training fine-tuning*. While the paper categorizes these distinctions in Section 3.3, the main results (Table 4) present all three methods side-by-side without caveat, and the text claims quantitative improvement percentages without acknowledging the different capability assumptions.

3. **Trigger dimensions are selected based on limited evaluation and then fixed across all environments.** In Section 4.2 (Table 2), the paper tests trigger dimension choices on only two environments (HalfCheetah and Walker2d), finds that (1,2,3) works best, and then *fixes the trigger dimensions to (1,2,3) for all subsequent experiments* — including AntMaze, Kitchen, and Pen, which are structurally different from locomotion tasks. Trigger dimension has a dramatic effect on ASR (ranging from 0.915 to 0.000 in Table 2). The paper does not verify whether (1,2,3) generalizes to the other environments, nor does it report results averaged across multiple dimension choices. The paper references Appendix F for "additional attempts at dimension selection methods," but the main results as presented reflect an attacker with privileged knowledge of good dimension choices for the specific evaluation environments.

### Minor

1. **Tension between "no original training data" claim and method requirements.** The threat model states the adversary operates "without access to the original training dataset" (line 60), yet the method requires a set of trajectories for trajectory filtering and fine-tuning. The paper says the adversary uses "a minimal set of poisoned trajectories (e.g., 0.3%)" (line 72) but does not clarify where these trajectories come from — whether they are independently collected or sampled from the original dataset. If the adversary can collect trajectories from the same distribution, the "without original data" claim needs qualification.

2. **Trajectory filtering assumption is unvalidated.** The method assumes "longer trajectories are more representative of successful behavior" (Section 5.1) without validating this for the specific D4RL datasets used. In environments like AntMaze, where agents may wander for many steps before succeeding, trajectory length may not correlate with quality.

3. **Defense analysis in the main paper lacks quantitative results.** Section 6.5 tests five defense methods but provides no numerical results (ASR/BTP after defense) in the main text, merely stating that fine-tuning "is the most effective defense" and the others are "largely ineffective." All numbers are deferred to the appendix.

4. **The most informative baseline — simple fine-tuning with poisoned data under the same post-training threat model — is not presented as a standalone comparison.** The ablation study (Table 5) removes components but does not directly show how TrojanTO compares to "fine-tune the pretrained model on the poisoned trajectories without any of TrojanTO's design choices." Since this is the natural baseline for a post-training attack, its absence weakens the causal claim that TrojanTO's specific components drive the improvement.

### Trivial

None.

## Nice-to-Haves

- For the baseline comparison in Table 4, consider adding a row showing results for a "simple post-training fine-tuning" baseline (i.e., fine-tuning the pretrained model on the same poisoned trajectories without alternating training, trajectory filtering, or batch poisoning). The ablation study already contains the building blocks.
- Report results averaged over several random trigger dimension choices, or provide a principled method for dimension selection that does not require evaluation access, or clearly acknowledge the limitation.
- Include a sensitivity analysis of ε in the main paper (e.g., a sweep over ε values showing how ASR changes).

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"No locomotion tasks are run here" (Section 4.2 criticism):** Factually incorrect. HalfCheetah and Walker2d *are* locomotion tasks. Removed as a factual error by the reviewer.
- **Criticisms about the ASR threshold value being missing from the appendix:** The parser strips appendix content; the value may appear in the original submission's appendices. The criticism kept above is about its absence from the *main paper*, which is a valid concern about clarity.
- **"105% improvement" vs. "different attack paradigms" claim reframing:** The original critic's framing called this a "structural" issue with strong language about unfairness. I have reframed it as a Major weakness with precise justification.
- **Generic concerns about missing variance in Table 4:** The paper reports aggregate means without standard deviations. This is noted above only in the context of the ε issue, not as an independent weakness.

## Novel Insights

None beyond the paper's own contributions. The merged reviews do not reveal a hidden structural flaw or overlooked opportunity that the paper itself does not already touch on (e.g., the different attack-stage categorization is acknowledged in Section 3.3; the trigger-dimension selection is partially addressed via Appendix F reference).

## Suggestions

1. **State ε in the main text** and include a brief sensitivity analysis showing how ASR varies with ε. This single addition would make the entire evaluation interpretable.
2. **Add a within-threat-model baseline** — fine-tune the pretrained model on the poisoned trajectories without alternating training, trajectory filtering, or batch poisoning (essentially the "w/o AT" ablation but positioned as a baseline, not an ablation).
3. **Acknowledge and address the trigger dimension selection limitation** — either report main results averaged over several dimension choices, or verify that (1,2,3) dimensions are effective in non-locomotion environments, or clearly state this as a limitation.
4. **Clarify what data the adversary actually has** — specify whether the poisoned trajectories are sampled from the original dataset or independently collected, and clarify the "without access to the original training dataset" claim.
5. **Move at least summary defense numbers** (post-defense ASR, BTP) into the main paper rather than deferring entirely to the appendix.

## Score and Decision

The paper addresses a genuinely new problem and makes a concrete contribution through its systematic analysis of backdoor factors for TO models (Section 4) and its proposed attack method. The core insight — that TO models require a different attack paradigm from traditional RL — is correct and well-articulated. However, the evaluation has three significant weaknesses: (a) the ASR metric depends on an unreported threshold ε, making quantitative claims uninterpretable; (b) the baseline comparison mixes different threat models without adequate caveats; and (c) trigger dimensions are selected from limited analysis and then used universally. These are addressable in revision but in the current form undermine the paper's quantitative claims.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>