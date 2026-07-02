## Summary
# Final Review Report

## Summary

This paper studies adversarial patch attacks and defenses for Vision-Language-Action (VLA) models. The authors propose EDPA (Embedding Disruption Patch Attack), a model-agnostic adversarial patch attack that requires only access to the visual encoder parameters (no knowledge of architecture, action space, or manipulator needed). EDPA uses two complementary objectives: (i) a patch contrastive loss that maximizes the discrepancy between clean and adversarial latent patch embeddings, and (ii) an image-instruction alignment loss that disrupts the semantic alignment between visual and language representations. As a defense, the authors propose adversarial fine-tuning of the visual encoder, training it to produce representations for adversarial inputs that match the original encoder's clean representations.

The work is evaluated on the LIBERO robotic simulation benchmark across four task suites (Spatial, Object, Goal, Long) and three VLA models (OpenVLA, OpenVLA-OFT, π0). Key results show EDPA achieves 100% failure rate on OpenVLA across all task suites, and the adversarial fine-tuning defense reduces EDPA-induced failure rates by ~34 percentage points on average, with only a 1.6% average clean-condition degradation. The paper also provides an interesting qualitative observation that generated adversarial patches resemble robotic arm structures, leading to a hypothesis about visual encoder overfitting to limited training data.

The paper addresses a timely and relevant problem (adversarial robustness of VLA models) with a clean technical approach. However, the evaluation has significant gaps: simulation-only results without physical-world validation, defense evaluated only on a single model (OpenVLA), weak baselines (only random noise patches as a universal baseline), and critical missing analyses such as patch placement sensitivity and adaptive attacks. The Discussion section's central hypothesis about overfitting is purely speculative without quantitative support. Overall, the paper makes a useful contribution to an underexplored area but requires substantial additional evidence to support its stronger claims.

## Strengths
**S1 — Timely and well-motivated problem.** Adversarial robustness of VLA models is an important and underexplored area. As VLA models are increasingly deployed in physical robotic systems, understanding their vulnerability to adversarial patches — which can be physically placed in the environment — is a practically relevant research direction. The paper clearly articulates this motivation.

**S2 — Clean, principled attack formulation.** EDPA targets the latent representation space rather than action outputs, which is a conceptually clean approach. The two complementary objectives (patch discrepancy + vision-language alignment disruption) are well-motivated and together provide a reasonable mechanism for generating effective adversarial patches.

**S3 — Model-agnostic design.** EDPA's key advantage — requiring only encoder parameters and no knowledge of the downstream architecture, action space, or robot platform — is a genuine improvement over prior work (UADA/UPA) that requires full model access. This makes the attack more broadly applicable across different VLA architectures.

**S4 — Comprehensive evaluation across models and task suites.** The paper evaluates three VLA models (OpenVLA, OpenVLA-OFT, π0) across four distinct LIBERO task suites with multiple seeds, providing a solid empirical foundation. The clean 100% failure rate on OpenVLA convincingly demonstrates the attack's effectiveness.

**S5 — Defense with favorable robustness-accuracy trade-off.** The adversarial fine-tuning defense is lightweight (only fine-tunes the visual encoder, not the full model) and achieves meaningful FR reduction (e.g., from 100% to 39.4% on Spatial tasks) with only 1.6% average clean degradation. The defense also shows cross-attack generalization (improving robustness against UADA and UPA).

**S6 — Interesting qualitative observation.** The finding that adversarial patches consistently resemble robotic arm structures is intriguing and opens up a promising research direction into understanding what visual encoders learn from limited-domain robotic data.

## Weaknesses
**W1 — Simulation-only evaluation without physical-world validation (High Severity).** All experiments are conducted in the LIBERO simulation environment. The paper claims the attack is practical for "real-world scenarios" but never demonstrates that printed patches placed in a physical environment remain effective under varying lighting, viewing angles, camera calibration, and perspective distortion. This is a critical gap because: (a) the gap between simulated patch insertion and physical patch placement is well-known to be substantial in adversarial patch literature, and (b) the paper's central argument for EDPA over prior work is based on *practical applicability*, yet no practical validation is provided. *Required action:* Add at least one real-world evaluation with printed patches and a physical camera setup, or explicitly bound all practicality claims to simulation and add physical-world validation as future work.

**W2 — Defense evaluated on a single model with selection bias (High Severity).** The adversarial fine-tuning defense is evaluated only on OpenVLA, which was selected *because* it showed the weakest robustness ("Due to our experimental results showed that OpenVLA exhibited the weakest robustness against EDPA, it was chosen as the primary model for defense evaluation"). This creates a selection bias: the defense is validated on the model where it is most likely to succeed. Without defense evaluation on OpenVLA-OFT or π0, the paper cannot support claims that the defense generalizes across VLA architectures. *Required action:* Evaluate the defense on at least one additional model (OpenVLA-OFT or π0) and report per-suite results. If computational constraints prevent this, explicitly state the generalization limitation and remove any implied generality claims.

**W3 — Weak and insufficient baselines (High Severity).** The paper uses only a random Gaussian noise patch as a universal baseline. This is a minimal control that any reasonable attack should outperform. The paper states "no existing baseline directly matches our experimental setting" but this overstates the gap: (a) the paper's own references include embedding-space attacks on LVLMs (Bagdasaryan et al. 2024, Zhang et al. 2022) that could be adapted; (b) a constant-color patch or an optimized patch for a different objective (e.g., classification loss) would provide stronger baselines. Additionally, UADA/UPA are only evaluated on OpenVLA, not on other models, so the claim of "model-agnostic" superiority over these methods lacks cross-model comparison. *Required action:* Add at least one stronger non-random baseline (constant patch, or patch optimized for a generic classification objective) and discuss why embedding-specific baselines cannot be directly transferred.

**W4 — Results narrative obscures important variation across task suites (Medium Severity).** The text reports aggregate numbers like "average decreases of 34.2%" and "minor 1.6% increase in failure rate under clean conditions" without clarifying that these are simple averages across four task suites that show drastically different behavior. Specifically, on the Long suite, the defense reduces EDPA-induced FR from 100% to only 91.2% (8.8pp reduction, far below the 34.2pp average), and the clean-condition degradation varies from +0.9pp (Long) to +5.3pp (Object, a 44% relative increase). *Required action:* Replace aggregate-only reporting with per-suite reporting for all key claims. Include a table or paragraph clearly showing the range of defense effectiveness across task suites.

**W5 — Central overfitting hypothesis in Section 5 is entirely speculative (Medium Severity).** The observation that patches resemble robotic arms is interesting, but the paper's explanation — that visual encoders overfit to arm appearances due to limited data and restricted camera viewpoints — is presented as causal without any supporting evidence. No quantitative analysis (e.g., representation similarity measurement, attention visualization, or probe-based classification) is provided. The arm-like patterns could also emerge from optimization dynamics, background texture biases, or other confounds. Additionally, the comparison between π0 and OpenVLA-OFT's robustness is confounded by architectural differences (flow matching vs. next-token prediction, different training data scales). *Required action:* Either add quantitative analysis supporting the overfitting claim (e.g., embedding similarity between patches and arm regions, or a controlled experiment varying training data diversity), or explicitly reframe the hypothesis as a conjectural observation and remove causal language.

**W6 — Missing critical experimental analyses (Medium Severity).** Several analyses that are standard in adversarial patch literature are absent: (a) patch placement sensitivity — how does patch effectiveness vary with translation, rotation, and scale? (b) patch size sensitivity — the fixed 50×50 patch size is inherited from prior work but not ablated; (c) adaptive attacks — the defense is not evaluated against an attacker who knows the defense mechanism and adapts the attack accordingly; (d) computational cost — no reporting of patch generation time, GPU hours, or convergence behavior. These analyses are important for understanding the practical applicability the paper claims. *Required action:* Add at least a subset of these analyses (placement sensitivity and patch size ablation are the most informative) in the appendix.

**W7 — Threat model and assumptions not clearly specified (Low Severity).** The paper describes EDPA as requiring "only access to the encoder parameters" but does not fully specify the threat model assumptions. Is the encoder assumed to be frozen? Can the attacker use a surrogate encoder? What access does the attacker have to the training data? Is the patch assumed to be printable? Can the attacker control patch placement or only patch content? These details matter for assessing the attack's practical feasibility and should be explicitly enumerated. *Required action:* Add a dedicated threat model subsection in the Method section that clearly states assumptions about attacker capabilities, knowledge, and constraints.

**W8 — Grammar and writing quality issues (Low Severity).** Several sentences contain grammatical errors: "Due to our experimental results showed that..." (ungrammatical)," "adversarial patch generation through EDPA are conduct on LIBERO" (subject-verb agreement), "a clean input visual input" (redundancy). These errors reduce confidence in the manuscript's preparation quality. *Required action:* Thorough proofreading pass, particularly in Sections 3-4.

**W9 — Novelty and related-work coverage deferred (note).** Because external literature search was unavailable in this run, novelty and positioning conclusions cannot be fully verified. The paper's claims about being the "first" to propose embedding-disruption patch attacks for VLA models and the inadequacy of prior work (UADA/UPA) should be independently verified against the broader adversarial patch and VLA robustness literature. The overfitting hypothesis also requires comparison with similar observations in related domains.

## Score
**Final Score: 5/10**

*Evidence-grounded rationale:* The paper addresses a timely problem with a clean technical approach (EDPA + adversarial fine-tuning) and provides reasonable simulation-based evidence of effectiveness. However, the score is constrained by: (1) simulation-only evaluation without any physical-world validation, which undermines the central practicality claim; (2) defense evaluation on a single model selected for maximal attack effectiveness, creating a best-case evaluation bias; (3) weak baselines that inflate the apparent attack advantage; and (4) speculative overfitting hypothesis presented without supporting evidence. The paper has the foundations of a solid contribution but requires substantial additional evidence to support its stronger claims about practical applicability and defense generality. Novelty and comparative positioning could not be independently verified due to unavailable literature search; these are marked for deferred manual verification.

---

### ASCII Diagrams

#### A. Paper Structure & Evidence Map

```text
[Paper Core Claim: EDPA is a practical, model-agnostic adversarial patch attack for VLAs]
    |
    ├── [C1: EDPA attack requires only encoder parameters]
    │   └── Evidence: Table 1 (requirements comparison); Sec 3.2 (loss formulation)
    │       └── Gap: Threat model assumptions not fully specified (W7)
    │
    ├── [C2: Adversarial fine-tuning defense mitigates attack]
    │   └── Evidence: Table 2 (OpenVLA pre/post defense); Alg 1 (procedure)
    │       └── Gap: Defense evaluated on OpenVLA only (W2); selection bias
    │
    ├── [C3: EDPA is effective across multiple VLA models]
    │   └── Evidence: Table 3 (OpenVLA-OFT, π0 results)
    │       └── Gap: No UADA/UPA comparison on non-OpenVLA models (W3)
    │
    └── [Qualitative: Patches resemble robotic arms → overfitting hypothesis]
        └── Evidence: Figure 2 (patch visualization)
            └── Gap: Hypothesis is speculative, no quantitative support (W5)
```

#### B. Revision Strategy Roadmap

```text
Priority 0 (Must-fix before acceptance)
├── W1: Add physical-world evaluation OR bound all claims to simulation
├── W2: Evaluate defense on at least one additional VLA model
└── W3: Add stronger baselines (constant patch, alternative objective patch)

Priority 1 (Strongly recommended)
├── W4: Replace aggregate reporting with per-suite results throughout
├── W5: Add quantitative evidence for overfitting hypothesis OR reframe as speculative
└── W6: Add patch placement/size sensitivity analysis + adaptive attack evaluation

Priority 2 (Quality improvements)
├── W7: Add explicit threat model subsection
├── W8: Proofreading pass for grammar errors
└── W9: Literature verification (deferred)
```

#### C. Related-Work Taxonomy Tree (Layered)

```text
[Adversarial Robustness for Vision-Language-Action Models]
│
├── Branch 1: VLA Models & Embodied AI
│   ├── Leaf 1.1: RT-2 [Zitkovich 2023], Octo [Team 2024]
│   ├── Leaf 1.2: OpenVLA [Kim 2024], OpenVLA-OFT [Kim 2025]
│   └── Leaf 1.3: π0 [Black 2024]
│
├── Branch 2: Adversarial Patch Attacks
│   ├── Leaf 2.1: Generic patch attacks [Brown 2017, Karmon 2018]
│   ├── Leaf 2.2: VLA-specific patch attacks
│   │   ├── UADA (action-token discrepancy) [Wang 2024]
│   │   ├── UPA (position-aware action vector) [Wang 2024]
│   │   └── EDPA (embedding disruption) [This paper]
│   └── Leaf 2.3: Embedding-space attacks on LVLMs [Zhang 2022, Bagdasaryan 2024]
│
├── Branch 3: Adversarial Defenses
│   ├── Leaf 3.1: Adversarial training (standard) [Goodfellow 2014, Madry 2017]
│   └── Leaf 3.2: Encoder-based adversarial fine-tuning [This paper]
│
└── Branch 4: Evaluation & Metrics
    ├── Leaf 4.1: LIBERO benchmark [Liu 2023]
    └── Leaf 4.2: Failure Rate metric [Wang 2024]
    │
    └── Note: External literature verification deferred (Retrieval-Disabled Mode)
```

---

**Final Assessment:** The paper has a solid technical core and addresses an important emerging problem. The EDPA formulation is clean and the model-agnostic property is a genuine improvement over prior work. However, the evaluation has critical gaps — particularly the lack of physical-world validation and single-model defense testing — that prevent the paper from supporting its stronger claims. With the Priority 0 revisions (physical validation or bounded claims, additional defense evaluation, stronger baselines), the paper could be suitable for publication. In its current form, the contribution is clear but the evidence is insufficient for the claimed scope.

*External literature verification unavailable in this run; novelty/comparison conclusions are intentionally deferred.*