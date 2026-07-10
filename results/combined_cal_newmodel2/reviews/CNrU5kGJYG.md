Now I have all the verification I need. Let me write the final review.

## Summary

This paper proposes TrojanTO, the first action-level backdoor attack against trajectory optimization (TO) models in offline reinforcement learning. The key insight is that existing RL backdoor attacks rely on reward manipulation during training, which is ineffective against TO models that minimize reconstruction loss. TrojanTO operates as a **post-training** attack, using alternating optimization of trigger and model parameters, combined with trajectory filtering and batch poisoning, to implant backdoors at a very low poisoning rate (0.3%). Experiments across 3 TO architectures (DT, GDT, DC) × 6 D4RL environments × 3 target actions show strong attack success.

## Strengths

- **Well-motivated problem framing.** The paper correctly identifies that existing RL backdoor attacks (which manipulate reward signals during training) are ineffective against TO models, whose training objective is reconstruction loss rather than reward maximization (Section 3.1, Section 4.3). The shift to a **post-training** paradigm that decouples the attack from the original training pipeline is a meaningful re-framing of the threat model for large-scale TO models. [favorability=9.84]

- **Systematic empirical investigation of key factors (Section 4).** The study of target action types, trigger dimensions/values, and reward manipulation provides useful findings independent of TrojanTO itself. The observation that boundary target actions yield near-perfect ASR while interior actions are far harder, and that trigger dimension choice can swing ASR from 0.915 to 0.000 (Table 2), are concrete and reproducible insights. [favorability=14.22]

- **Strong and well-structured experimental evaluation.** TrojanTO is evaluated across 3 TO model architectures (DT, GDT, DC) × 6 D4RL environments × 3 target action types with 3 seeds. The average CP of 0.701 substantially exceeds IMC (0.551). The ablation study (Table 5) convincingly isolates the contribution of each component, and the very low poisoning rate (0.3%) is a genuine advantage for stealth. [favorability=14.05]

- **Consistent and well-defined evaluation metrics.** CP (harmonic mean of ASR and BTP) is a principled choice that prevents a method from scoring high by sacrificing either effectiveness or stealth. The paper correctly computes CP per run rather than from averaged ASR/BTP (line 98). [favorability=11.77]

## Weaknesses

### Fatal
None.

### Major

- **The ASR threshold ε is never specified.** Equation (2) defines attack success as all action components being within ε of the target action, but the paper never states what value of ε is actually used. This makes the ASR numbers uninterpretable in an absolute sense — if ε is large (e.g., 10% of the action range), a "successful" attack could produce actions far from the intended target. Without knowing ε, a reader cannot evaluate the stringency of the reported ASR values. This is a straightforward methodological gap that must be filled. [favorability=1.35]

- **The comparison against Baffle on action-level metrics is structurally unfair.** The paper's Section 3.2 correctly distinguishes policy-level from action-level backdoors: "Policy-Level Backdoor… focuses solely on whether the adversary's objective can be achieved and does not consider the model's specific actions." Baffle (Gong et al., 2024b) is a policy-level attack designed to degrade long-term returns, yet it is compared against TrojanTO on ASR (an action-level metric measuring exact action match). The same issue affects CP, which includes ASR in its computation. The paper's claim of "105.0% improvement over Baffle" is thus inflated by a metric mismatch. The IMC comparison is cleaner and more informative; the Baffle comparison should be reframed with explicit caveats or an adapted baseline. [favorability=-0.24]

### Minor

- **Unresolved data provenance in the threat model.** The paper states (Section 3.3) that the adversary operates "without access to the original training dataset." However, TrojanTO's training procedure (Section 5) uses a filtered set of trajectories Fτ sampled from an initial set of N trajectories. The paper does not clarify where these trajectories come from. The answer matters for assessing the attack's real-world practicality — if they come from the same public D4RL dataset the victim used, the "without access" claim needs qualification. [favorability=7.03]

- **Reward manipulation experiment shown for only one environment in the main text.** Figure 1 demonstrates reward insensitivity only for the Walk environment. The paper cites Appendix K.1 for additional results, but the main text would benefit from showing at least one more environment to support the claim that this insensitivity is a general property of TO models. [favorability=4.54]

### Trivial
None.

## Nice-to-Haves

- The paper could discuss why exactly one transition per batch is poisoned (Section 5.2) and whether poisoning more transitions would improve ASR at the cost of stealth.
- The target action types ('arithmetic', '0.5staggered', etc.) are defined only in the appendix; a brief main-text description would help readability.

## Removed Points

These points were raised in the input review but are removed for the following reasons:

- **"First" action-level backdoor claim and missing concurrent work:** Per policy, we do not flag missing related works or argue about "first" framing as a substantive weakness.
- **Defense results deferred to appendix (Section 6.5):** The appendix is stripped by the parser; these sections exist in the original submission. Criticizing their absence is an artifact of the review format.
- **Trigger dimension choice for reward experiment:** The critic worried that dimensions (8,9,10) produce a "generally weak backdoor setup." However, the reward experiment uses target type '1', which Table 1 shows yields ASR 0.993 for Walk — this is not a weak setup. The concern is speculative and factually incorrect.
- **Various section-by-section notes about readability and presentation:** These are minor formatting/style observations that do not affect the core claims.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Specify ε.** Report the exact threshold value used for ASR computation and provide a rationale (or sensitivity analysis) for the choice.
2. **Reframe the Baffle comparison.** Either (a) add explicit caveats about the policy-level vs. action-level mismatch, or (b) construct an adapted action-level variant of Baffle for fairer comparison. The IMC comparison is fine and does not need changes.
3. **Clarify data provenance.** Explain where the adversary's trajectories come from under the "no access to original training dataset" assumption.
4. **Add reward manipulation results for one more environment in the main text** (e.g., HalfCheetah) to strengthen the generality claim.

## Score and Decision

### Calibration Anchors

| Path | Avg Human Score | Round | Itemized | Comparison |
|------|----------------|-------|----------|------------|
| `/home/.../em0gAL8fbK.md` | 4.00 | R1 | Yes | Multi-vehicle backdoor attack against offline RL. Has higher poisoning rate (~15%) and stronger threat model assumptions. This paper is stronger empirically and has lower poisoning rates. |
| `/home/.../rp5vfyp5Np.md` | 4.25 | R1/R2 | Yes | BATTLE: behavior-oriented attacks against DRL. Has unclear success rate definitions and unfair baseline comparisons similar to this paper's Baffle issue, but overall weaker empirical evaluation. |
| `/home/.../AKAlVyunxA.md` | 5.75 | R1 | Yes | SHINE: backdoor shielding in DRL. Strong defense paper with similar empirical rigor. Comparable in quality but addresses a different aspect of the problem. |
| `/home/.../HZnnHDrBXD.md` | 5.75 | R1/R2 | Yes | Tree-based action-manipulation attack. Strong theoretical results but very limited evaluation (2 simple environments). This paper's empirical evaluation is substantially broader. |
| `/home/.../S1Bv3068Xt.md` | 6.25 | R2 | Yes | BALD: backdoor attacks against embodied LLM decision-making. Comparable breadth of evaluation and similar mixed review pattern. |
| `/home/.../X2x2DuGIbx.md` | 6.75 | R2 | Yes | Multi-level certified defense for offline RL. Stronger theoretical contributions but narrower scope. |
| `/home/.../5sdUTpDlbX.md` | 5.20 | R1 | No | EEG BCI backdoor attack. Less relevant topic but similar score band. |
| `/home/.../GxCGsxiAaK.md` | 5.75 | R1 | No | Universal jailbreak backdoors from poisoned human feedback. |
| `/home/.../DoB8DmrsSS.md` | 4.25 | R1 | No | Diffusion-guided adversarial state perturbations in RL. |

**Round 1 bracket:** The paper sits above the 4.00–5.20 range (where papers have weaker evaluations or more fundamental flaws) and below the 6.75–8.00 range (where papers have theoretical proofs or exceptionally polished presentation). Initial bracket: 5.5–7.0.

**Narrowing (Round 2):** Comparing item-level favorability ratings against the closest anchors:

- Against the 5.75 anchors (SHINE, Tree-based): This paper's peak strength favorability (14.22 for empirical insights, 14.05 for evaluation) matches or exceeds those anchors. Its major weaknesses (ε unspecified at 1.35, Baffle comparison at -0.24) are fixable methodological gaps, not structural flaws. The Tree-based paper was criticized for only 2 simple environments, while this paper covers 6 environments × 3 models, a clear advantage.

- Against the 6.25 anchor (BALD): BALD has a similar pattern — strong strengths and a few fixable gaps. However, BALD had one reviewer give a score of 3/8 due to novelty concerns, while this paper's core technical contribution is clearer.

- Compared to the 6.75 anchor (Multi-level defense): That paper benefits from theoretical proofs (favorability 16.08) that this paper lacks. This paper's strength is instead in empirical breadth and a well-motivated practical threat model.

The two major weaknesses (ε unspecified, Baffle comparison mismatch) are genuine concerns that lower confidence in the headline numbers, but both are addressable without changing the method. The IMC comparison remains fair and favorable. The paper's core contribution — a practical post-training action-level backdoor for TO models at 0.3% poisoning rate — is well-supported.

**Final score: 6.0** — a solid borderline accept. The paper makes a genuine contribution to an underexplored problem, with a well-designed method and strong empirical support. The two major weaknesses are fixable but currently prevent a higher score.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>