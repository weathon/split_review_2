## Summary
This paper introduces INFO-SEDD, a novel method for estimating information-theoretic quantities—specifically KL divergence, mutual information (MI), and entropy—on high-dimensional discrete data using Continuous Time Markov Chains (CTMCs) and discrete diffusion models. The key idea is to leverage score functions trained via the DWDSE objective (from discrete diffusion) as plug-in estimators for density ratios, which are then used in a Dynkin's-formula-based KL estimator. Two variants are proposed: INFO-SEDD-J (joint distribution vs. product of marginals) and INFO-SEDD-C (conditional vs. marginal). The method explicitly avoids the "embedding trick" of projecting discrete data into continuous spaces, which prior neural estimators require.

The paper's main strengths are: (1) a theoretically principled framework connecting discrete diffusion to information estimation via Dynkin's formula and absorbing-state CTMCs; (2) the ability to compute MI with a single score model by leveraging the absorbing-state property to derive marginal scores from a jointly trained model; (3) strong empirical performance on synthetic benchmarks (Table 1) where INFO-SEDD is the only estimator that remains accurate at high MI and high dimensionality; (4) practically useful applications in text summarization (model selection aligned with human consistency judgments) and genomics (TATA-box motif discovery via sliding-window MI).

The paper also has several weaknesses: (1) the core KL estimator derivation (Eq 4) skips critical algebraic steps, and the main text does not provide sufficient verification of the integrand's correctness; (2) the theoretical error bound (Eq 7) depends on undefined constants (C₁*, C₂) and has a D|χ| scaling factor that could be large in practice; (3) novelty claims ("unique", "invaluable tool") cannot be verified without external literature due to Retrieval-Disabled Mode; (4) several important experimental details (backbone architecture, training modifications) are deferred to the appendix; (5) the conclusion lacks explicit limitations despite the method having clear failure modes (small C₁*, large D|χ| scaling, backbone dependence).

## Strengths
**S1. Theoretically principled framework.** INFO-SEDD connects discrete diffusion models (CTMCs) to information estimation through Dynkin's formula, providing a solid mathematical foundation. The use of absorbing-state CTMCs to derive marginal scores from a jointly trained model (Eq 6) is elegant and practically important, as it reduces the number of required score networks from two to one for the joint-variant MI estimation.

**S2. Strong synthetic benchmark results.** Table 1 convincingly demonstrates that INFO-SEDD is the only estimator that remains accurate across the full range of MI values (10 to 50 nats) and dimensionalities (D=10 to 50). Competing methods either saturate (MINE, NWJ), exhibit high bias (SMILE, GAN-DIME), or collapse (KL-DIME, HD-DIME). The standard deviations over 10 seeds are also the smallest among all methods, indicating good stability.

**S3. Practical applicability on real discrete data.** The text summarization experiments (Section 4.2) show that INFO-SEDD correlates well with human consistency judgments (Pearson r=0.74 for INFO-SEDD-C), matching the state of the art (Darrin et al., 2024) without requiring complex embedding models. The genomics applications (Section 4.3) demonstrate the method's versatility—both in a low-MI consistency test and in the TATA-box motif discovery task, where INFO-SEDD's ability to compute MI between arbitrary subsets without per-window retraining is a genuine practical advantage.

**S4. Two complementary variants.** The formulation of both joint (INFO-SEDD-J) and conditional (INFO-SEDD-C) MI estimators is a thoughtful design choice. The experiments show that each variant has distinct strengths: INFO-SEDD-C is more sample-efficient for low-dimensional conditioning (genomics labels), while INFO-SEDD-J provides a single unified model for joint distributions.

**S5. Reproducibility-oriented reporting.** The paper reports means and standard deviations over 10 seeds for synthetic benchmarks, uses established baselines with controlled experimental settings, and provides explicit references to appendix sections containing additional details (architectures, hyperparameters, dataset descriptions).

## Weaknesses
**W1. Incomplete derivation of the core KL estimator (Major).** The transition from Eq (2)+(3) (Dynkin's formula) to Eq (4) (the KL integrand) is presented as a single jump without intermediate algebraic steps in the main text. The resulting integrand involves the function K(a)=a(log a-1) together with terms q_t/q_t and (p_t/p_t) log(q_t/q_t), whose structural relationship to the KL divergence is not immediately obvious. While the appendix presumably contains the full derivation (not available in this run), the main text should at minimum sketch the key algebraic manipulation for a technically capable reader to follow. Specifically, the derivation requires: (a) choosing f = log(p_T/q_T), (b) expanding the backward operator B applied to f, and (c) simplifying the resulting expression using the CTMC generator structure. Without this sketch, the estimator's correctness cannot be verified from the main text alone.

**W2. Undefined constants in the theoretical error bound (Major).** Eq (7) presents an error decomposition with constants C₁* and C₂ that are not defined in the main text. C₁* appears in the denominator (1 + C₂/C₁*), suggesting it relates to a minimum probability ratio, but the exact condition is not stated. The term C₂ is described as a "boundedness" constant for scores, but the specific norm (L∞? L₂?) and domain (over t? over x?) are unspecified. Additionally, the scaling factor D|χ| (sequence length × vocabulary size) could be extremely large for text data (e.g., D=512, |χ|≈30,000 gives D|χ|≈1.5×10⁷), making the bound vacuous in practice. The paper should discuss when this bound is tight versus pessimistic.

**W3. Novelty claims unverifiable without external literature (Moderate).** The abstract claims INFO-SEDD "outperforms alternatives that rely on the 'embedding trick'" and the conclusion states "to the best of our knowledge, our method is unique." Due to Retrieval-Disabled Mode in this run (external paper search unavailable), these novelty claims cannot be verified against prior art. The paper should either provide a more thorough related-work discussion in the main text or scope the claims more precisely (e.g., "to our knowledge, the first discrete diffusion-based MI estimator that avoids continuous embeddings"). A dedicated novelty verification section should be added in a revision.

**W4. Missing experimental details in main text (Moderate).** Several important experimental choices are deferred to the appendix without sufficient main-text description: (a) the score network backbone architecture is not specified (MLP? transformer? parameter count?), (b) the "slight modification" to the MDLM-SMALL training strategy for INFO-SEDD is not described, (c) the hyperparameter choices (T, σ(t), learning rate) are not reported in the main text. While the appendix may contain these details, a self-contained main text would significantly improve reproducibility and reader confidence.

**W5. Text summarization reference MI derivation (Moderate).** The consistency test in Section 4.2 uses a reference MI estimate of 256ρ to 303ρ nats, obtained by multiplying entropy rates from prior work by the average summary length. This is a coarse approximation: MI at mixing probability ρ is not simply entropy × ρ—it depends on the joint distribution of paired and unpaired texts. The paper should either provide a more rigorous derivation or clearly label this as a rough order-of-magnitude estimate rather than a ground-truth reference. The qualitative trend (monotonic increase) is sufficient for the consistency comparison, but the numerical reference should not be over-interpreted.

**W6. Absence of explicit limitations in the conclusion (Minor).** The conclusion discusses extensions and applications but does not mention any limitations of INFO-SEDD. Key limitations that should be acknowledged: (a) the D|χ| scaling in the error bound may limit applicability to long sequences or large vocabularies, (b) the method requires a pretrained or fine-tuned backbone model, which may not be available for all discrete data modalities, (c) the absorbing-state assumption (Eq 6) constrains the choice of transition matrices, and (d) the error analysis assumes bounded scores, which may not hold for all distributions. Including explicit limitations would improve the paper's scientific credibility.

**W7. Overclaiming on motif discovery (Minor).** The paper states that INFO-SEDD "makes it an invaluable tool for motif discovery" based on a single known motif (TATA-box) in one species (Arabidopsis thaliana). This is a proof-of-concept demonstration, not a validated general-purpose tool. The paper also claims robustness to correlated motifs without a controlled experiment. These claims should be softened to match the evidence level.

**W8. Potential circular definition in Eq (1) (Minor).** The reverse-time generator Eq (1) defines $\overleftarrow{Q}_t(b,a)$ on the left-hand side, while the diagonal correction term on the right-hand side references $\sum_{b \neq a} \overleftarrow{Q}_t(b,a)$, which is a function of the same entries being defined. Standard practice is to define off-diagonal entries first and then set diagonal entries as negative row sums. This should be clarified to avoid confusion.

## Score
**Final Score: 6/10**

**Rationale:** The paper introduces a principled and well-motivated approach (INFO-SEDD) to a practically important problem—MI estimation for high-dimensional discrete data without continuous embeddings. The theoretical framework connecting CTMC-based discrete diffusion to KL estimation via Dynkin's formula is novel and the synthetic benchmark results are compelling. The applications in text summarization and genomics demonstrate practical utility. However, the score is tempered by several notable weaknesses: the core derivation (Eq 4) is presented without sufficient intermediate steps in the main text, the theoretical error bound (Eq 7) depends on undefined constants, novelty claims cannot be externally verified in this run, key experimental details are deferred to the appendix, and the conclusion lacks explicit limitations. These issues are fixable but currently reduce confidence in the estimator's full correctness and scope of applicability.

---

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Problem: MI estimation for high-dimensional discrete data]
    |
    v
[Prior gap: "embedding trick" degrades with dimensionality]
    |
    v
[Proposed method: INFO-SEDD (CTMC + Dynkin's formula)]
    |
    +-- [Theoretical contribution: KL estimator Eq(4), error bound Eq(7)]
    |       |
    |       +-- W1: Eq(4) derivation skipped in main text -- needs verification
    |       +-- W2: Eq(7) constants C₁*, C₂ undefined
    |
    +-- [Synthetic experiments (Table 1)] -- evidence level: strong
    |       |
    |       +-- S2: Best accuracy across all MI/D settings
    |       +-- W4: Backbone architecture not specified in main text
    |
    +-- [Text summarization (Section 4.2)] -- evidence level: moderate
    |       |
    |       +-- S3: Good correlation with human consistency (r=0.74)
    |       +-- W5: Reference MI derivation is approximate
    |
    +-- [Genomics (Section 4.3)] -- evidence level: moderate
    |       |
    |       +-- S3: Motif discovery without per-window retraining
    |       +-- W7: "Invaluable tool" overclaim for single-motif demo
    |
    +-- [Conclusion] -- W6: No explicit limitations stated
```

---

### ASCII Diagram — Revision Strategy Roadmap

```text
Priority | Issue | Fix | Expected Impact
---------|-------|-----|-----------------
P0 (Must) | W1: Eq(4) derivation gap | Add 3-5 line derivation sketch in main text | Verifiability, correctness confidence
P0 (Must) | W2: Undefined C₁*, C₂ | Define constants explicitly; discuss D|χ| scaling | Theoretical completeness
P1 (Must) | W4: Missing experimental details | Move backbone arch, hyperparameters to main text | Reproducibility
P1 (Must) | W6: No limitations section | Add 3-5 sentence limitations paragraph | Scientific credibility
P2 (Nice) | W5: Reference MI approximation | Provide caveat or more rigorous derivation | Accuracy of claims
P2 (Nice) | W7: Motif discovery overclaim | Soften language, acknowledge proof-of-concept scope | Claim-evidence alignment
P2 (Nice) | W3: Unverifiable novelty | Scope claims; add thorough related-work in revision | Novelty positioning
```

---

### ASCII Diagram — Experiment Upgrade Plan

```text
Current experiments:
├── Synthetic (Table 1): high MI/D benchmarking ✓
├── Text summarization (Section 4.2): consistency + model selection ✓
├── Genomics (Section 4.3): consistency + motif discovery ✓
└── Ising model entropy (Appendix D): not in main text

Proposed additions (P0/P1 priority):
├── [P0] Convergence analysis: learning curves for INFO-SEDD vs competitors
│   └── Currently in Appendix C.1.3; move one representative curve to main text
├── [P0] Ablation: effect of time horizon T and noise schedule σ(t) on MI estimates
│   └── Key hyperparameter sensitivity currently unreported
├── [P1] Sample complexity: explicit table of MI error vs training set size
│   └── Currently mentioned qualitatively (10^3 samples); needs main-text figure
├── [P1] Controlled correlated-motif experiment for genomics
│   └── Test robustness claim with synthetic correlated motifs
└── [P2] Computational cost comparison: training time, inference time, memory
    └── Currently absent; important for practitioners
```

---

### Page Coverage Audit

All substantive paragraphs in the main body (Pages 1 of the paper text, covering Abstract, Introduction, Methodology, Experiments, Conclusion) have been annotated. Since the paper PDF is contained on a single text page (page 1) with multiple sections, the 14 annotations provide coverage of: Abstract (1 annotation), Introduction (5 paragraph-level annotations covering all 5 intro paragraphs), Methodology (3 annotations covering CTMC preliminaries, KL derivation, INFO-SEDD approach, error bound), Experiments (4 annotations covering synthetic benchmarks, text summarization, genomics consistency, motif discovery), Conclusion (1 annotation). Appendix content was not available in this run and is excluded from the audit.