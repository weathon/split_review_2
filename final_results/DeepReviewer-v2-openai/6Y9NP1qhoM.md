## Summary
This paper addresses misinformation injection in Large Language Model-based Multi-Agent Systems (MAS). The authors make two contributions: (1) MISINFOTASK, a dataset of 108 multi-topic tasks with accompanying misinformation arguments designed for red-teaming MAS; and (2) ARGUS, a training-free defense framework combining adaptive graph-based localization of critical communication channels with goal-aware Chain-of-Thought reasoning for misinformation detection and correction.

The paper tackles a relevant and underexplored problem—subtle misinformation (as opposed to overtly malicious content)—and the proposed framework is modular, training-free, and evaluated across four LLMs and three injection methods. However, the current manuscript has several significant weaknesses that limit its impact. The evaluation metrics rely on an LLM-as-judge without human validation or alternative verification, the TSR threshold $\theta_m$ is never specified (making results non-reproducible), the threat model is narrow (single-agent, single-round compromise), the method description lacks critical implementation details (CoT prompts, normalization factor, weighted sum formula), and the dataset is small with missing quality metrics. Novelty assessment is deferred due to external literature verification being unavailable in this run.

**Overall assessment:** The problem is well-motivated and the ARGUS design is intuitive, but the current evidence—particularly the underspecified method, unvalidated metrics, and narrow evaluation—does not yet support the claimed level of generality and robustness. The paper requires substantial revision to the method description, metric validation, and experimental scope before it can be considered publishable at a top venue.

## Strengths
1. **Timely and relevant problem formulation.** Misinformation injection in multi-agent systems is an important and underexplored security concern. The paper's distinction between overtly malicious content (prompt injection, jailbreaks) and subtle misinformation (semantically plausible but factually incorrect statements) is well-motivated and practically relevant. This framing correctly identifies a gap in existing MAS safety research, which has primarily focused on detectable malicious inputs rather than covert misinformation.

2. **Training-free, modular architecture.** ARGUS's two-stage design—graph-based localization plus CoT-based correction—is pragmatic and does not require model fine-tuning or architectural modifications. This makes it potentially applicable to a wide range of existing MAS deployments without retraining costs. The separation of localization (which edges to monitor) from correction (what to do with suspicious messages) is a clean decomposition that facilitates future improvements to either component independently.

3. **Multi-dimensional evaluation.** The experimental design covers three injection methods (Prompt Injection, RAG Poisoning, Tool Injection) across four LLMs from different families (GPT-4o-mini, GPT-4o, DeepSeek-V3, Gemini-2.0-flash), providing reasonable breadth. The inclusion of two defense baselines (Self-Check and G-Safeguard) and an ablation study with both submodule removal and hyperparameter analysis is more comprehensive than many comparable works.

4. **Transparency in limitations.** The Limitations section (Section 7) acknowledges computational overhead and the reliance on parametric knowledge, which helps bound the paper's claims. This candor is appreciated, though the section would benefit from quantitative treatment (see Weaknesses).

5. **Dataset provision and reproducibility intent.** The authors commit to releasing the MISINFOTASK dataset and code, which is valuable for the community. If the dataset receives proper quality documentation, it could serve as a useful benchmark for future MAS misinformation research.

## Weaknesses
### W1 (Critical) — Undefined TSR threshold makes results non-reproducible
Equation (1) defines Task Success Rate (TSR) as the proportion of tasks where Score(O_k, g^k_task) ≥ θ_m, but θ_m is never specified or reported anywhere in the manuscript. All TSR values in Table 1—which form the basis for claims of ARGUS's effectiveness—depend on this unreported threshold. Different choices of θ_m (e.g., 5 vs. 7 on a 0-10 scale) could produce substantially different absolute TSR values and potentially alter the relative ranking of defenses. This omission represents a critical reproducibility failure.
- **Page 3 - Evaluation Metrics:** Equation (1) defines TSR with θ_m but θ_m is never defined.
- **Fix required:** Report θ_m explicitly, justify it, and provide a sensitivity analysis across θ_m ∈ {5.0, 5.5, 6.0, 6.5, 7.0, 7.5} showing the stability of rankings.

### W2 (Major) — LLM-as-judge circularity without validation
Both MT and TSR use the same LLM-judge Score() function (GPT-4o-2024-08-06) to evaluate output quality. Since the same LLM family powers the agents being evaluated, there is a risk of systematic bias: the judge may systematically prefer outputs that match its own generation style rather than measuring factual correctness. No human validation study, inter-annotator agreement metric, or alternative judge is provided.
- **Page 3 - Evaluation Metrics:** Score() is evaluated by an LLM judge.
- **Page 7 - Experimental Settings:** The judge is GPT-4o-2024-08-06.
- **Fix required:** (1) Report human agreement (Cohen's κ ≥ 0.7 on a 50-sample subset). (2) Add a second independent judge (e.g., a different LLM family) and report correlation. (3) Verify that MT and TSR scores are not correlated across instances.

### W3 (Major) — Threat model too narrow
The evaluation assumes a single compromised agent with one-shot injection at round 1. This does not test ARGUS against: (a) coordinated multi-agent compromises, (b) persistent multi-round injection, (c) adaptive misinformation that evolves to evade detection. The paper's claim of a "unified shield against diverse misinformation threats" is not supported by this narrow attack profile.
- **Page 3 - Threat Model:** "The attacker compromises a single agent" at "the initial round."
- **Fix required:** (1) Add a multi-round injection experiment to validate the adaptive re-localization mechanism. (2) Discuss adaptive adversary scenarios. (3) Acknowledge scope limitation explicitly in the main text, not only in limitations.

### W4 (Major) — Critical method underspecification
Three aspects of ARGUS are insufficiently specified for reproducibility:
- **N_norm in Eq. (2):** The normalization factor in edge betweenness centrality is never defined.
- **Weighted sum formula:** The comprehensive score Score^r(e) is described as "a weighted sum" of α, β, γ, but no explicit equation or default values are provided.
- **CoT detection/correction prompts:** The core detection mechanism (Section 4.2) describes "Multi-faceted Identification," "Internal Knowledge Resonance," and "Heuristic Persuasive Reconstruction" without any prompt templates, decision thresholds, or validation examples. The phrase "internal knowledge resonance" is a metaphor, not a computational specification.
- **Page 4 - Initial Localization:** Eq. (2) uses N_norm without definition.
- **Page 5 - Adaptive Re-Localization:** No explicit weighted sum equation.
- **Page 6 - Goal-aware Reasoning:** Three-stage process described only conceptually.
- **Fix required:** (1) Define N_norm. (2) Provide Score^r(e) = α·Score_topo + β·Score_rel + γ·Score_freq with default weights. (3) Include full CoT prompts in appendix and a worked example.

### W5 (Major) — Dataset quality concerns
MISINFOTASK has only 108 tasks, which is small for drawing robust statistical conclusions across 4 LLMs × 3 attacks × multiple defense conditions. More critically:
- No inter-annotator agreement reported for the manual filtering step.
- No category distribution statistics (how many tasks per category?).
- The "realistic tasks" claim is unsubstantiated by any task taxonomy or expert validation.
- The dataset is entirely LLM-generated with prompt-guided sampling, raising concerns about artifact patterns.
- **Page 3 - MISINFOTASK Dataset:** 108 tasks, LLM-generated + manual filtering.
- **Fix required:** (1) Report per-category distribution. (2) Provide inter-annotator reliability metrics. (3) Include a task diversity analysis. (4) Acknowledge sample size limitations.

### W6 (Major) — Missing variance for Attack-only baselines
Table 1 reports standard deviations for all defense methods but not for Attack-only rows. Without baseline variance, the claimed improvements from ARGUS cannot be statistically evaluated. Additionally, some ARGUS sub-conditions show extreme variance (e.g., GPT-4o-mini + Tool Injection MT: 2.67 ± 3.11, where std > mean), which is not discussed.
- **Page 7 - Table 1:** Attack-only rows lack standard deviations.
- **Fix required:** (1) Report std for Attack-only. (2) Add significance tests comparing ARGUS vs. Attack-only per condition. (3) Discuss high-variance conditions.

### W7 (Major) — Related Work lacks structured taxonomy
Section 6 is organized as a chronological list of papers rather than a comparison-driven taxonomy. Each paragraph states "X does Y" without grouping by approach type or explicitly positioning ARGUS against prior work along concrete dimensions (graph-based vs. content-based, training-free vs. trained, overt vs. covert threats).
- **Page 9 - Related Works:** List-style organization.
- **Fix required:** Restructure by thematic axes with explicit comparison of each family's assumptions, scope, and demonstrated effectiveness vs. ARGUS.

### W8 (Major) — Overclaiming in abstract and conclusion
The conclusion calls this work "pioneering" and claims "high generalization." The abstract and introduction use "robust defensive capabilities" and "significant efficacy" without bounding these claims to the evaluated settings. Novelty claims cannot be verified in this run (Retrieval-Disabled Mode), but the current wording exceeds what the evidence supports.
- **Page 1 - Abstract:** "significant efficacy across various injection attacks."
- **Page 9 - Conclusion:** "pioneering evaluation" and "outstanding performance and high generalization."
- **Fix required:** Replace "pioneering" with "initial investigation," bound generalization claims to tested conditions, and restate limitations in conclusion.

### W9 (Major) — Ablation study lacks statistical rigor
The ablation comparisons (Tables 2 and 3) report MT and TSR without significance tests. The hyperparameter ablation (Table 3) suggests the frequency score (β) contributes minimally (w/o β MT 3.76 vs. full ARGUS MT 3.73), but this is not discussed. No interaction analysis between components is provided.
- **Page 9 - Ablation Study:** Tables 2 and 3 without significance tests.
- **Fix required:** (1) Add paired bootstrap tests for all ablation contrasts. (2) Test two-way interactions between components. (3) Discuss the potential redundancy of the frequency score.

### W10 (Major) — Limitations section lacks quantitative depth
The limitations acknowledge "efficiency and cost" but provide no numbers. Missing: false positive rate of corrections, per-task overhead (latency, API calls), scalability analysis for larger MAS, and failure case analysis. Without these, readers cannot assess practical deployability.
- **Page 9 - Limitations & Future Works:** Qualitative only.
- **Fix required:** (1) Report latency/API cost per task. (2) Estimate false positive rate. (3) Discuss O(N^3) betweenness computation scalability. (4) Provide cost comparison table vs. baselines.

## Score
**Final Score: 5.5/10**

**Rationale:** The paper addresses a relevant and timely problem (misinformation injection in multi-agent systems) with a modular, training-free framework. However, the current version has one critical reproducibility failure (undefined TSR threshold $\theta_m$), a major unvalidated evaluation methodology (LLM-as-judge without human agreement), critical method underspecifications that prevent reproduction, and a narrow threat model that limits the generality of the claimed results. The dataset contribution (MISINFOTASK) is potentially useful but lacks quality documentation and is small (108 tasks). Novelty assessment is deferred because external literature verification was unavailable in this run, but even within the paper's own framing, the incremental combination of known techniques (graph centrality, CoT prompting) would benefit from clearer positioning against existing graph-based and consensus-based defenses. The strengths—particularly the problem framing and clean architectural decomposition—are meaningful, but the weaknesses in evidence quality and specification are significant enough that substantial revision is needed before the paper can be considered for a top-tier venue.

**Evidenced score breakdown:**
- Problem relevance and motivation: 7/10 (well-framed, clear gap)
- Novelty (deferred): N/A (external verification unavailable)
- Methodological soundness: 4/10 (critical underspecification, missing normalization, undefined threshold)
- Experiment validity: 4/10 (unvalidated judge metric, missing variance, narrow threat model)
- Reproducibility: 3/10 (missing $\theta_m$, prompt templates, normalization, and weight defaults)
- Dataset contribution: 5/10 (useful but small, limited quality documentation)
- Writing clarity: 6/10 (clear motivation, but overclaiming and metaphorical method descriptions)
- Ablation/comparison depth: 6/10 (good breadth but missing statistical rigor)

**Post-Revision Target:** 6.5-7.5/10 (conditional on addressing W1, W2, W4 as mandatory fixes, and most of W3, W5-W10 as strongly recommended improvements)