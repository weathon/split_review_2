## Summary
This paper introduces the Perceptually-Grounded Geospatial Chain-of-Thought (Geo-CoT), a framework designed to elicit verifiable step-by-step reasoning in Vision-Language Models (VLMs) for remote sensing. The key contributions are: (1) formalizing Geo-CoT as a reasoning paradigm where each analytical step must be explicitly grounded to visual evidence; (2) constructing Geo-CoT380k, a large-scale dataset of 384,591 structured rationales generated via a GPT-4V pipeline conditioned on verified bounding boxes and captions; and (3) presenting RSThinker, a VLM fine-tuned from GLM-4.1V-9B-Base using a two-stage alignment strategy—supervised fine-tuning (SFT) to instill the cognitive architecture, followed by Group Relative Policy Optimization (GRPO) to refine factual correctness.

The experiments evaluate RSThinker across seven remote sensing tasks (visual grounding, object counting, object detection, scene classification, image captioning, VQA) on multiple benchmarks. The model consistently outperforms existing generic and domain-specific VLMs, often by substantial margins. Ablation studies confirm that both the CoT-based SFT and the GRPO stage contribute to the final performance, with KL-regularized GRPO preventing format collapse. A qualitative analysis shows that RSThinker produces interpretable reasoning traces that expose both correct evidence gathering and occasional perceptual errors.

**External literature verification is unavailable in this run (Retrieval-Disabled Mode); all novelty/comparison conclusions are explicitly deferred for manual verification.**

## Strengths
1. **Well-motivated problem framing.** The paper clearly identifies a genuine limitation in current remote sensing VLMs—the lack of verifiable intermediate reasoning steps—and links it to high-stakes applications (disaster response, environmental monitoring) where output verifiability is critical. This problem framing is compelling and timely.

2. **Clean two-stage alignment strategy.** The proposed SFT→GRPO pipeline is principled: SFT instills the structural template of Geo-CoT (cognitive architecture), while GRPO refines sequence-level faithfulness (policy optimization). This decoupling of architectural and policy challenges is well-grounded in recent LLM alignment literature (DeepSeek-R1) and is clearly motivated.

3. **Comprehensive empirical evaluation.** The evaluation covers a wide range of tasks (7 tasks) and benchmarks (15+ datasets), including both in-distribution and zero-shot settings. The visual grounding results (Table 4) are particularly impressive, with RSThinker nearly doubling the mIoU of the next best model on several benchmarks.

4. **Large-scale dataset contribution.** Geo-CoT380k (384,591 structured rationales across multiple tasks) is a substantial resource that could benefit the community. The scalable GPT-4V-based pipeline with strict conditioning (providing verified bounding boxes, captions, and CoT exemplars) is a practical methodology for generating faithful rationales.

5. **Transparency through failure analysis.** The paper includes an honest failure case (Figure 7) showing that RSThinker can produce coherent reasoning chains while making perceptual errors. This transparency, and the acknowledgment that the grounding mechanism makes errors auditable, demonstrates scientific integrity and provides a realistic picture of the model's capabilities and limitations.

## Weaknesses
### W1. Lack of statistical significance reporting (High Severity)

All experimental results (Tables 4–7, Figure 3) are reported as single-point estimates without standard deviations, confidence intervals, or statistical significance tests. This is a critical omission because several reported advantages are modest in absolute terms (e.g., RSThinker accuracy on SIRI-ZS is 77.67% vs. EarthDial's 73.42%, a 4.25% gap; on RSVQA-HR Color, 64.33% vs. ChatGPT-5's 59.49%). Without variance information, readers cannot assess whether the reported improvements are statistically reliable or within noise range.

**Required action:** Report all main results as mean±std over at least 3 random seeds. Add pairwise significance tests (e.g., bootstrap or Mann-Whitney U) against the strongest baseline for each benchmark. This is a **must** for publication.

### W2. Baseline fairness concerns in object detection (High Severity)

Figure 3 reports EarthDial's mAP@0.25 as 4% on HRRSD and 3% on DOTAv2-val—levels so low that they suggest the evaluation setup may not have been compatible with conversational VLMs not designed for detection. If baselines were not given task-appropriate prompts or output parsers, the reported gains are artificially inflated and the "SOTA" claim is misleading.

**Required action:** Describe the exact prompt and output parsing used for each baseline on the detection task. Include at least one detection-specialized model (e.g., YOLOv8, DETR) as a reference baseline to calibrate task difficulty. Add the evaluation protocol details to the main paper, not only the appendix.

### W3. Unverifiable "first" and "state-of-the-art" claims (High Severity)

The paper makes unqualified "first" claims ("first large-scale SFT dataset for remote sensing chain-of-thought," Page 2 Contribution 2; conclusion: "first to propose such a framework," Section 2.3) and global "state-of-the-art" claims (abstract, contributions) without external literature verification or statistical support. Because external paper search is unavailable in this run, these claims are flagged for manual verification.

**Required action:** (a) Add "to the best of our knowledge" qualifiers to "first" claims. (b) Bound SOTA claims to specific benchmarks and settings (e.g., "RSThinker achieves competitive results on Visual Grounding benchmarks VRSBench-VG and DIOR-RSVG under the evaluated setting"). (c) Conduct a thorough literature review to verify that no prior work constructs CoT datasets of comparable scale for remote sensing.

### W4. Internal inconsistency in GRPO reward formulation (Medium Severity)

Section 3.3 states that "the reward signal is derived solely from the final output of the reasoning trace," but Table 3 shows that grounding and detection rewards (IoU, mAP) require parsing intermediate outputs (bounding boxes from the think block), not just the final answer. This contradiction needs resolution.

**Required action:** Clarify what constitutes the "final output" for reward computation. If the reward is computed from the entire generated sequence (including the think block), revise the text to say "the reward signal is derived from the model's generated output sequence" and explain how task-relevant elements are extracted.

### W5. Missing evidence for the "perceptual mismatch" motivation (Medium Severity)

Section 2.2 claims that "generalist grounded models often falter in this domain" (remote sensing) due to a perceptual mismatch (salient objects vs. dense tiny objects). No empirical evidence is provided—no experiment showing that Visual CoT, VoCoT, or Argus underperform on RS benchmarks.

**Required action:** Either (a) add quantitative evidence (e.g., run Visual CoT on a remote sensing benchmark and report results), or (b) soften the claim to: "Existing grounded CoT frameworks have been primarily validated on domains with salient objects; their effectiveness on dense RS imagery remains an open question that this paper addresses."

### W6. Weak causal attribution for Geo-CoT's contribution (Medium Severity)

Section 4.2.1 claims that counting improvements are a "direct consequence" of Geo-CoT architecture. However, the ablation study (Table 8) only compares SFT(w/ CoT) vs SFT(w/o CoT), which conflates the effect of structured reasoning with the effect of different training data/target format. A proper causal test would compare RSThinker with and without spatial grounding while keeping the output format identical.

**Required action:** (a) Replace causal language ("direct consequence") with correlational language ("consistent with the hypothesis"). (b) Add an ablation where grounding coordinates are removed from the reasoning trace while maintaining the same overall output structure, to isolate the effect of perceptual grounding.

### W7. Annotated "Δ" row in Table 8 is uninterpretable (Medium Severity)

The ablation table includes a "Δ" row that contains only the Δ symbol in each cell without numerical values or labels. Readers cannot determine what delta is being shown (Δ between which two rows?).

**Required action:** Remove the ambiguous Δ row or replace it with explicitly labeled deltas: "Δ_CoT = SFT(w/ CoT) - SFT(w/o CoT)" and "Δ_GRPO = SFT(w/ CoT)+GRPO - SFT(w/ CoT)."

### W8. Overclaiming in failure analysis framing (Medium Severity)

Section 4.4 describes a misidentification error (dock extension → ship) as a "safety feature" because the grounding makes the error auditable. While transparency is valuable, the model still produces an incorrect answer. Calling this a "safety feature" overstates the benefit of explicability—the error still requires human detection.

**Required action:** Reframe the failure analysis to acknowledge both the benefit (auditability for debugging) and the limitation (error still propagates, requiring human oversight). Discuss the fraction of errors caught by human inspection of the grounding trace.

### W9. Conclusion adds unsupported new claim (Low Severity)

The conclusion introduces the concept of "analytical agents" in its final sentence, which was neither tested nor discussed in the paper. The paper evaluates standard VLM benchmarks, not agentic tasks.

**Required action:** Replace the final sentence with a description matching what was actually validated (verifiable reasoning in VLMs for remote sensing analysis).

### W10. Missing reproducibility details (Low Severity)

Several important experimental details are deferred to the appendix: full training protocol, hyperparameters, baseline evaluation details. Additionally, Equation (1) does not define W_p and H_p (dimensions of the pre-trained position table). These details affect reproducibility.

**Required action:** Add definitions for all variables in Equation (1). Move critical reproducibility information (e.g., number of training steps, batch size, learning rate, number of GRPO samples k, KL penalty coefficient β) to the main paper or ensure the appendix is comprehensive.

## Score
**Final Score: 6/10**

**Rationale:** This score reflects a paper with a well-motivated technical framework and comprehensive empirical coverage, but whose findings are currently undermined by the absence of statistical validation, baseline fairness concerns, and unverifiable novelty claims. All major weaknesses are fixable with targeted revisions (adding variance reporting, fair baseline comparisons, claim qualifiers), which would raise the score significantly. The core idea—structured, perceptually-grounded reasoning via two-stage alignment—is sound and the dataset contribution (Geo-CoT380k) is a practical resource for the community.

**Scoring Dimensions:**
- Research Value: 7/10 — The problem is well-motivated and the solution addresses a genuine gap in remote sensing VLMs. The dataset and framework have potential community impact.
- Novelty: 5/10 (provisional) — The combination of Geo-CoT + two-stage alignment is novel, but "first" claims cannot be verified without literature search (Retrieval-Disabled Mode). Some components (SFT→GRPO pipeline, grounded CoT) build on existing work. Manual verification is required.
- Validity/Soundness: 5/10 — The methodology is technically sound, but the lack of statistical significance testing and potential baseline unfairness in detection tasks weaken confidence in the reported gains.
- Reproducibility: 6/10 — The dataset release is commendable, but missing definitions (Eq. 1), deferred implementation details, and unspecified prompt/parsing for baselines reduce reproducibility.
- Presentation: 7/10 — Well-structured, clear figures, good motivation. Some overclaiming and the ambiguous "Δ" row in Table 8 need attention.

---

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Problem: VLMs lack verifiable reasoning in RS]
    |
    v
[Solution: Geo-CoT framework (Planning-Grounding-Synthesis)]
    |
    v
[Method: Two-stage alignment]
    ├── Stage 1: SFT on Geo-CoT380k (cognitive architecture)
    └── Stage 2: GRPO (factual correctness refinement)
    |
    v
[Model: RSThinker]
    |
    v
[Evidence presented]
    ├── Strong: Visual Grounding (Table 4) — large margins
    ├── Strong: Object Counting (Table 5) — large margins
    ├── Moderate: Classification/VQA (Table 6) — consistent gains
    ├── Moderate: Captioning (Table 7) — good but mixed (EarthDial higher CIDEr on NWPU)
    ├── Moderate: Ablation (Table 8) — shows CoT > no-CoT, GRPO helps
    ├── Weak: No statistical significance anywhere
    ├── Weak: Detection baselines may be unfair (Fig 3)
    └── Weak: Causal attribution for counting gains unproven
    |
    v
[Gaps to close]
    ├── Add variance/std/CI to all results
    ├── Fix detection baseline fairness
    ├── Verify "first" claims with literature search
    ├── Bound SOTA claims to evaluated settings
    └── Add causal ablation for grounding effect
```

---

### ASCII Diagram — Revision Strategy Roadmap

```text
Priority | Task                          | Effort | Impact | Must/Nice
---------|-------------------------------|--------|--------|---------
P0       | Add multi-seed std to all     | Medium | High   | Must
         | results (W1)                  |        |        |
P0       | Qualify "first"/"SOTA" claims | Low    | High   | Must
         | (W3)                          |        |        |
P0       | Fix detection baseline setup  | Medium | High   | Must
         | + add detection specialist (W2)|       |        |
P1       | Resolve GRPO reward           | Low    | Medium | Must
         | inconsistency (W4)            |        |        |
P1       | Add perceptual mismatch       | Medium | Medium | Nice
         | evidence (W5)                 |        |        |
P1       | Replace Δ row with labeled   | Low    | Low    | Must
         | deltas in Table 8 (W7)        |        |        |
P1       | Reframe failure analysis (W8) | Low    | Medium | Nice
P2       | Add causal ablation for       | High   | Medium | Nice
         | grounding effect (W6)         |        |        |
P2       | Fix conclusion overclaim (W9) | Low    | Low    | Nice
P2       | Add missing definitions (W10) | Low    | Low    | Must
```

---

### ASCII Diagram — Related-Work Taxonomy Tree (Layered)

```text
Remote Sensing Vision-Language Models (Root)
├── Branch 1: Conversational VLMs (End-to-end mapping)
│   ├── Leaf 1.1: GeoChat (Kuckreja et al., 2024)
│   ├── Leaf 1.2: EarthDial (Soni et al., 2025)
│   └── Common limitation: Latent reasoning, no externalized trace
│
├── Branch 2: Architecturally-novel VLMs
│   ├── Leaf 2.1: VHM (Pang et al., 2025)
│   ├── Leaf 2.2: SkyMoE (Liu et al., 2025b)
│   └── Leaf 2.3: GeoDiT (Liu et al., 2025a)
│   └── Common limitation: Still end-to-end, reasoning not externalized
│
├── Branch 3: Chain-of-Thought / Reasoning VLMs
│   ├── Leaf 3.1: Grounded CoT (general vision)
│   │   ├── Visual CoT (Shao et al., 2024)
│   │   ├── VoCoT (Li et al., 2025b)
│   │   └── Argus (Man et al., 2025)
│   │   └── Limitation: Validated on salient-object domains, not RS
│   ├── Leaf 3.2: RS-specific reasoning
│   │   ├── SegEarth-R1 (Li et al., 2025a)
│   │   ├── RemoteReasoner (Yao et al., 2025)
│   │   ├── SkySense-O (Zhu et al., 2025)
│   │   └── Ringmo-Agent (Hu et al., 2025)
│   │   └── Limitation: Abstract text descriptions, no perceptual grounding
│   └── Leaf 3.3: Geo-Reasoning (ground-level)
│       ├── GeoChain (Yerramilli et al., 2025)
│       └── GAEA (Campos et al., 2025)
│       └── Limitation: Semantic reasoning, not top-down perceptual grounding
│
└── This paper (Geo-CoT / RSThinker)
    └── Position: First VLM to externalize perceptually-grounded, structured
        reasoning chain (Planning-Grounding-Synthesis) for overhead EO imagery
    └── Novelty risk: "First" claim unverified due to Retrieval-Disabled Mode
    └── Value addition: Geo-CoT380k dataset, two-stage alignment recipe
```

---

**External literature verification unavailable in this run (paper_search not started due to missing API token); novelty/comparison conclusions are intentionally deferred and require manual verification before acceptance decisions.