Now I have all the calibration data I need. Let me compile the final review.

**All anchors for the record:**

| File | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| NEMESIS jailbreaking | 1.40 | R1 | No | Off-topic, much weaker |
| Advancing Cross-Lingual Humanoid Robots | 1.00 | R1 | No | Off-topic |
| Balancing Differential Discriminative Knowledge | 1.00 | R1 | No | Off-topic |
| Scaling In-the-Wild Training for Illumination | 0.50 | R1 | No | Outlier, different field |
| Early Fusion VLA (EF-VLA) | 3.33 | R1 | No | VLA architecture paper; rejected for unclear presentation and limited eval |
| RED - Robust Environmental Design | 3.00 | R1 | No | Adversarial patches for road signs; less ambitious |
| Seeing Through the Mask (CAPTCHAs) | 3.00 | R1 | No | Different domain |
| Building Generalist Robot Policy | 3.40 | R1 | No | Robotics policy, not security |
| **HardPatch** | **4.40** | R1 | **Yes** | **Adversarial patch on LVLMs; rejected for practicality. Our paper is stronger.** |
| Improving Adversarial Transferability in MLLMs | 4.00 | R1 | No | Transfer focus, not VLA-specific |
| Invisibility Stickers Against LiDAR | 4.00 | R1 | No | Different sensor modality |
| Transferable Adversarial Attack on VLLMs | 4.00 | R1 | No | Transfer focus |
| **BadRobot** | **5.75** | R2 | **Yes** | **Embodied LLM attacks; broader eval, simpler attacks. Comparable quality.** |
| Non-targeted Attacks on VLMs via MIE | 5.25 | R2 | No | White-box VLM attack; simpler eval |
| One Perturbation is Enough (UAP) | 5.00 | R2 | No | Universal perturbations on VLP |
| **BALD (backdoor attacks)** | **6.25** | R2 | **Yes** | **Embodied LLM backdoors; strong eval, novelty concerns** |
| **Jailbreak in Pieces** | **6.25** | R2 | **Yes** | **Encoder-only embedding-space attack; very similar approach, stronger eval** |
| OT-Attack (transferability) | 6.00 | R2 | No | Transfer focus |
| PLA (copyright tracking) | 6.25 | R1 | Yes | Adversarial approach for copyright; comparable depth |
| **OT adversarial patch** | **6.20** | R1 | **Yes** | **Patch attack with OT; strong eval, limited novelty** |
| **Fusion Is Not Enough** | **6.25** | R1 | **Yes** | **Single-modal patch on fusion models; comparable** |
| TraceVLA | 7.00 | R1 | No | VLA prompting, not security |
| Visual Data-Type Understanding | 8.00 | R1 | No | Different topic |
| PhysBench | 8.00 | R1 | No | Benchmark paper |
| Test-time Adaptation | 8.00 | R1 | No | Different topic |
| MOS (3D detection) | 8.00 | R1 | No | Different topic |

**Round 1 bracket: 4.5–6.5.** The paper is clearly above the reject band (3–4) occupied by HardPatch (4.40) and well above EF-VLA (3.33). It uses gradient-based optimization with a clear two-objective formulation (HardPatch was query-based) and includes a defense. The most similar high-impact items are the +10.00 (reduced dependency) and +9.95 (multi-architecture eval) strengths versus the -9.86 (defense scope) and -9.87 (no defense baseline) weaknesses. Compared to Jailbreak in Pieces (6.25) which had similar +9.30 eval strength but weaker methodological clarity, our paper's single-model defense evaluation is the main factor keeping it below 6.0.

**Final score: 5.5.** This sits between the rejected HardPatch (4.40) and the accepted BadRobot (5.75) / Jailbreak in Pieces (6.25). The attack contribution is solid and well-evaluated, but the incomplete defense evaluation prevents a higher score.

---

## Summary

This paper proposes EDPA (Embedding Disruption Patch Attack), the first adversarial patch attack targeting the latent embedding space of Vision-Language-Action (VLA) models, and a corresponding adversarial fine-tuning defense. EDPA operates with access only to the visual encoder (no action space, robot geometry, or LLM backbone knowledge required), representing a meaningful reduction in prior-knowledge requirements over the existing UADA/UPA attacks. The attack is evaluated on three VLA models (OpenVLA, OpenVLA-OFT, π₀) across all four LIBERO task suites with statistical reporting, and the defense is tested on OpenVLA.

## Strengths

- **Reduced dependency profile is a genuine advance.** EDPA needs only encoder parameters, compared to UADA (needs action space knowledge + full model parameters) and UPA (needs manipulator structure + full model parameters). Table 1 and Figure 1 make this concrete and fair. This is not marginal — it enables attacks on OpenVLA-OFT and π₀ (Table 3) that prior attacks could not target at all. **[impact=+10.00]**

- **Multi-architecture evaluation with statistical rigor.** Evaluation across three VLA models (OpenVLA, OpenVLA-OFT, π₀) on all four LIBERO task suites, using 3 random seeds with standard deviations (Tables 2, 3). This exceeds the single-model evaluations common in adversarial robustness papers, and supports the claim of cross-architecture effectiveness. **[impact=+9.95]**

- **Principled defense design.** The adversarial fine-tuning objective (Eq. 5) directly counters EDPA's attack objective: EDPA maximizes embedding discrepancy (Eq. 2) while the defense minimizes distance between the fine-tuned encoder's outputs on adversarial inputs and the original encoder's outputs on clean inputs. Algorithm 1's min-max dynamic (generating fresh patches against the current encoder, with periodic patch resets) is well-structured. **[impact=+2.48]**

- **Insightful patch visualization analysis.** Section 5's observation that adversarial patches consistently develop arm-like patterns, and the hypothesis about visual encoder overfitting due to limited camera viewpoints in robotic datasets, provides scientifically interesting discussion beyond raw empirical results. **[impact=+0.14]**

## Weaknesses

### Fatal
None.

### Major

- **Defense evaluation scope is severely limited.** The defense is tested only on OpenVLA, not on OpenVLA-OFT or π₀. The paper justifies this choice (OpenVLA showed weakest robustness), but this leaves the defense's generalizability unestablished. Furthermore, there is no comparison against alternative defense baselines (e.g., standard adversarial training on random perturbations or PGD-based encoder training). Without knowing whether the proposed fine-tuning scheme outperforms simpler alternatives, the defense contribution is incompletely supported. **[impact=-9.86 / -9.87 combined]**

- **The defense's transfer to UADA/UPA lacks mechanistic explanation.** Table 2 shows the defense reduces UADA failure rates from ~99% to 46–97% and UPA from ~99% to 46–87%. This is interesting, but UADA and UPA operate on action tokens/vectors, not on the embedding space. Without any analysis (e.g., measuring whether UADA/UPA patches also cause embedding deviation that the defense mitigates), this remains an unexplained empirical finding that weakens the scientific grounding. **[impact=-9.19]**

### Minor

- **"Model-agnostic" framing is overstated.** EDPA still requires white-box access to the encoder (gradient computation via Eq. 4). In adversarial ML, "model-agnostic" typically implies black-box transfer. The paper uses it to mean "less prior knowledge than prior attacks." This distinction matters in deployment scenarios where even encoder parameters may be unavailable. The paper's actual contribution — reduced prior-knowledge requirements — is strong enough to stand without overclaiming. **[impact=-1.64]**
  
- **No black-box transfer evaluation.** The most practically relevant test — whether EDPA patches generated on one VLA model transfer to another without encoder access — is not conducted. This would directly test the practical scope of the attack. **[impact=-6.37]**

- **The InfoNCE-based patch contrastive loss (Eq. 2), when maximized, has ambiguous theoretical behavior.** Maximizing Eq. 2 could push p_i toward resembling some other p'_j (j≠i) rather than purely making p_i and p'_i diverge. The paper does not analyze or discuss this property. Empirical success suggests it works in practice, but the theoretical justification of the loss choice is incomplete. **[impact=-3.42]**

### Trivial

- **Inner attack iteration K=1 is unusually low and not justified.** Standard adversarial patch generation typically uses multiple inner iterations (10–50). While the total of 50K outer iterations provides sufficient gradient updates, the K=1 choice warrants explanation. **[impact=-0.06]**

## Nice-to-Haves

- A physical-world realizability discussion (lighting, printing distortions, occlusions) would strengthen the practical relevance, though the paper's simulation-only scope is explicitly stated.
- An ablation summary of the two loss components in the main text (currently deferred to Appendix C, stripped by the parser) would help justify the two-objective design.

## Removed Points

These points from the input review were flagged for removal and should be treated with caution:
- **Ablation of loss components:** The critic requested ablation from the main text; the paper states sensitivity analysis is in Appendix C (stripped by the parser). Removed per hard rule about missing appendix content.
- **EMA normalization decay rate not specified:** Removed as an undisclosed hyperparameter detail (nitpick).
- **Patch placement underspecified:** The paper states patches "can be randomly placed at any location" — removed as a minor detail consistent with standard practice.
- **Grammar/writing issues:** Removed as formatting artifacts from the parser.
- **Missing citation or related work complaints:** Removed per instruction (cannot verify external sources).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Test the defense on at least one additional VLA model** (OpenVLA-OFT or π₀). This is the single highest-leverage improvement — it would establish whether the defense generalizes or is specific to OpenVLA.
2. **Compare against a simple adversarial training baseline** (e.g., training on random noise patches or PGD-based encoder perturbations) to show the proposed method's added value.
3. **Analyze why the defense transfers to UADA/UPA** by measuring whether those attacks also cause embedding-space deviation that the proposed defense regularizes.
4. **Replace "model-agnostic" with more precise language** such as "reduced-knowledge" or "encoder-only" to better reflect what the paper actually demonstrates.
5. **Discuss the InfoNCE loss maximization behavior** — acknowledge that maximizing Eq. 2 could theoretically exploit cross-patch similarity rather than pure divergence, and explain why this is not a practical concern given the experimental setup.

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>