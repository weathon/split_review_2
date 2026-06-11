## Summary
# Final Review Report

## Summary

This paper introduces a weight-based method for analyzing gated neurons in transformer LLMs by computing cosine similarities between their input (reading) and output (writing) weight vectors. Applying this method across 12 LLMs, the authors discover a class of "weakening" neurons whose $\cos(\mathbf{w}_{\text{in}}, \mathbf{w}_{\text{out}})$ is negative, indicating they remove detected directions from the residual stream rather than amplifying them. These weakening neurons are few (hundreds in a 7B model) but have outsized influence: they activate much more frequently than strengthening neurons, and ablating them substantially affects attribute rate (factual recall) and output entropy. Through a novel "conditional ablation" technique, the paper shows that much of this effect occurs when the gate value is negative—a surprising finding since negative gate values in Swish/GELU activations were previously considered unimportant for model mechanisms. The paper claims to be the first to observe a functional role for negative gate values, though it notes concurrent work by Kong et al. (2025).

**Overall assessment:** The paper presents a simple yet intriguing discovery with potential to open new directions in mechanistic interpretability. The main strengths are the surprising empirical findings about weakening neurons and the cross-model consistency of weight patterns. The main weaknesses are: (1) the ablation experiments use only one model (OLMo-7B), leaving generality unverified; (2) the central claim about negative gate values lacks quantitative statistical support for the difference between conditional ablation conditions; (3) the "first" claim requires tighter qualification given concurrent work; and (4) the weight preprocessing step may influence the taxonomy in ways not fully discussed. The paper is well-written and the methodology is clearly explained. With additional generality experiments and tightened claims, this could be a solid contribution.

**Novelty note (deferred verification):** Due to Retrieval-Disabled Mode in this run, external literature comparison is unavailable. The novelty claims about "first to investigate read-write behavior of gated neurons," "first to observe negative gate value mechanism," and the weakening neuron discovery should be verified against the full related-work literature before final acceptance decisions.

## Strengths
**1. Simple yet revealing methodological lens.** Computing cosine similarities between input and output weight vectors for gated neurons is a refreshingly straightforward idea that yields non-obvious findings. The paper demonstrates that even a weight-only analysis can uncover structural patterns (weakening vs. strengthening) that correlate with functional importance in downstream metrics. This simplicity is a genuine strength: it makes the method accessible and easy to apply to new models.

**2. Cross-model consistency of weight patterns.** The finding that $\cos(\mathbf{w}_{\text{in}}, \mathbf{w}_{\text{out}})$ follows a consistent trajectory across 12 diverse LLMs (positive in early layers, negative in late layers) is compelling evidence for a universal architectural property. Figure 1(a) elegantly summarizes this pattern, and the inclusion of models spanning different families, sizes (0.5B to 9B), and gating variants (SwiGLU and GeGLU) strengthens the generality claim of the weight-based analysis.

**3. Surprising and well-motivated discovery of negative gate value functionality.** The conditional ablation experiments revealing that negative gate values drive a substantial portion of the entropy-sharpening effect are the paper's most striking contribution. The case study with the "Omicron" example concretely illustrates how weakening neurons with negative gate activations boost the correct next token. This challenges the conventional view that Swish/GELU negative regions are merely training-dynamic artifacts, opening a new question for mechanistic interpretability.

**4. Excellent writing quality and exposition.** The paper is clearly written, with well-defined terminology (RW functionality, conditional strengthening/weakening, atypical categories), a logical flow from method to discovery to ablation to case study, and effective use of figures. The authors carefully explain their design choices (threshold-based classification, random baselines, preprocessing steps) and honestly acknowledge limitations (single-model ablation, concurrent work).

**5. Introduction of conditional ablation as a general tool.** The conditional ablation method, while simple, is a useful addition to the interpretability toolkit. It enables researchers to isolate which activation regimes of a neuron are responsible for specific behavioral effects, which goes beyond standard whole-neuron ablation.

## Weaknesses
### W1. Ablation experiments limited to a single model (Major)

The weight-based analysis in Section 5 covers 12 LLMs, establishing broad cross-model patterns. However, all functional claims—weakening neurons have highest ablation impact, negative gate values drive sharpening effects, activation-frequency correlations—are demonstrated only on OLMo-7B using a single 20M-token Dolma subset. Claims like "weakening neurons have the highest effect on the metrics" and "weakening neurons make the output distribution sharper" are presented as general statements about transformer LLMs, yet the evidence comes from one architecture. Given that OLMo-7B uses SwiGLU and specific training data (Dolma), the results may not transfer to models with different gating variants, data distributions, or scale.

**Required action (Must):** Either (a) replicate the key ablation (zero ablation of weakening neurons, attribute rate and entropy metrics) on at least one additional model (e.g., Llama-3.2-3B or Gemma-2-2B) on a smaller token subset (5M tokens), or (b) add an explicit generalizability caveat in the abstract and conclusion. A partial replication would substantially increase confidence in the claims.

### W2. Insufficient statistical support for conditional ablation comparison (Major)

The paper's most striking claim—that case (iii) ($x_{\text{gate}} < 0, x_{\text{in}} < 0$) dominates the entropy sharpening effect—is supported only by a qualitative visual comparison of histograms (Figure 3b). The text states that case (iii) "shows entropy effects similar to those of weakening neurons as a whole, whereas this is much less the case for the other subplots," but provides no quantitative comparison: no mean/SD per condition, no effect size, no statistical test (e.g., KS test or bootstrap) between case (iii) and the other three conditions. The histograms in Figure 3b appear visually similar across all six subplots, making it difficult for readers to verify the claimed difference without numerical evidence.

**Required action (Must):** Report the mean entropy change for each of the four conditional conditions with standard deviations, a pairwise significance test between case (iii) and each other condition, and the fraction of total entropy reduction attributable to case (iii). This data should already be computable from the recorded ablation runs.

### W3. "First" claim needs qualification due to concurrent work (Major)

The abstract and conclusion assert that the paper is "the first to observe a mechanism involving negative values of the Swish activation function." However, Section 6.2 acknowledges "concurrently with Kong et al. (2025) who focus on a different phenomenon." This creates a contradiction: the abstract claims exclusive priority, while the main text acknowledges independent concurrent discovery. The concurrent work (Kong et al., 2025) is cited but not discussed in sufficient detail for readers to assess the overlap. If Kong et al. also observe negative gate-value effects (even on a different phenomenon), the "first" claim is inaccurate.

**Required action (Must):** (a) Replace "for the first time" in the abstract with "to our knowledge, concurrently with concurrent work by Kong et al. (2025)" or remove the first-claim language. (b) Add a brief comparison to Kong et al. (2025) in the Related Work or Section 6.2, clarifying what phenomenon they study and how it differs from the mechanism reported here.

### W4. Weight preprocessing may influence taxonomy classification (Moderate)

Section 3.2 introduces a preprocessing step that multiplies $\mathbf{w}_{\text{in}}$ and $\mathbf{w}_{\text{out}}$ by $\text{sign}(\cos(\mathbf{w}_{\text{gate}}, \mathbf{w}_{\text{in}}))$, justified as not changing model behavior (symmetry). However, this step directly alters $\cos(\mathbf{w}_{\text{in}}, \mathbf{w}_{\text{out}})$, which is the primary classification criterion for the strengthening/weakening taxonomy in Table 1. If the preprocessing systematically shifts this cosine toward positive values, the observed number of weakening neurons could be underestimated. The paper does not report whether the main conclusions (existence of weakening neurons, layer-wise pattern, ablation effects) are robust to omitting this step.

**Required action (Nice-to-have):** Add a brief robustness check showing that the qualitative patterns (median cosine by layer, RW class distribution, key ablation results) hold without this preprocessing. Even a single sentence in Appendix C confirming this would significantly strengthen confidence in the taxonomy.

### W5. Metrics justification deferred to appendix (Moderate)

The ablation metrics (attribute rate and entropy) are introduced in the main text with the note "We justify these choices in section F." Without in-text motivation, readers may question whether these metrics were selected post-hoc to maximize the observed effect. The paper does not report whether other common metrics (perplexity, downstream task accuracy, loss) also show the same patterns.

**Required action (Nice-to-have):** Add one sentence per metric in the main text explaining their relevance, and briefly note whether other examined metrics show consistent patterns. This can be concise (one sentence each) and would improve reading flow.

### W6. Correlation vs. causation in activation frequency analysis (Minor)

Section 7 reports a strong negative correlation between $\cos(w_{\text{in}}, w_{\text{out}})$ and activation frequency, concluding that "weakening neurons activate very often" and are thus "highly influential." However, the analysis does not control for potential confounders such as weight vector norms, layer depth, or activation function range. It is possible that neurons with small-magnitude cosine similarity (which includes weakening) happen to activate more frequently for reasons unrelated to their RW functionality.

**Required action (Nice-to-have):** Report partial correlations controlling for weight norm and layer depth, or note this as a limitation in the discussion.

### W7. Conclusion overextends to SAEs without evidence (Minor)

The conclusion speculates about extending the RW analysis to SAE latents, but Section 4.1 acknowledges that this requires "well-defined input and output weights," which SAE latents may not have. This creates a tension between the paper's stated limitations and its forward-looking claims.

**Required action (Nice-to-have):** Recast the SAE comment as an open question: "Whether a similar analysis applies to SAE latents remains to be determined, as their weight structure differs from individual neurons."

### W8. Threshold $\tau = 0.5$ for taxonomy lacks sensitivity analysis (Minor)

The threshold-based classification uses $\tau = \pm 0.5$ without analysis of how the class sizes (e.g., "25% input manipulators," "80% conditional strengthening") vary with $\tau$. While scatter plots provide complementary evidence, the quantitative percentages depend on this choice.

**Required action (Nice-to-have):** Add a short sensitivity analysis showing class-size variation across $\tau \in [0.3, 0.7]$ in the appendix.

## Score
**Final Score: 6.5/10**

This score reflects a paper with genuinely interesting empirical discoveries and clear exposition, weighed against concerns about single-model ablation evidence, insufficient statistical support for the central conditional-ablation claim, and unverified novelty given concurrent work. The core findings—the existence and distribution of weakening neurons, their high activation frequency, and the surprising role of negative gate values—are valuable enough to warrant further investigation but require additional validation before their full significance can be assessed.

**Scoring rationale (research value + novelty emphasis):**
- **Research value (7/10):** The discovery of weakening neurons as a functionally important class opens a new angle for mechanistic interpretability. The conditional ablation method is a useful methodological contribution. However, the research value is somewhat bounded by the single-model ablation evidence. If replicated across models, the value would increase.
- **Novelty (6/10):** The RW cosine-similarity framework for gated neurons appears novel in its synthesis, though prior work computed similar cosines without interpretation. The negative gate value finding is partly concurrent with Kong et al. (2025). External literature verification is deferred.
- **Validity/Soundness (6/10):** The weight-based analysis is sound and reproducible. The ablation experiments are well-designed but the key conditional-ablation comparison lacks statistical rigor. Generalization to other models is unverified.
- **Reproducibility (7/10):** Code is provided, methodology is clearly described, and TransformerLens ensures consistent preprocessing. Missing peak GPU memory and some hyperparameter details are minor issues.

---

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Core Research Question: What is the relationship between what a gated neuron reads and writes?]
    |
    +-- [Method: Compute cos(w_in,w_out), cos(w_gate,w_out), cos(w_gate,w_in)]
    |       |
    |       +-- [Taxonomy: 6 RW classes (Table 1)]
    |       +-- [Preprocessing: sign-flip based on cos(w_gate,w_in)]
    |
    +-- [Key Finding 1: Cross-model layer-wise pattern]
    |       Evidence: 12 models, Fig 1(a) median cosine trajectory
    |       Claim: early-middle = strengthening, late = weakening
    |       Strength: strong (broad model coverage)
    |       Gap: only weight-based, no functional validation yet
    |
    +-- [Key Finding 2: Weakening neurons have outsized ablation impact]
    |       Evidence: OLMo-7B, 20M Dolma tokens, zero/mean ablation
    |       Claim: weakening >> other classes on attribute rate & entropy
    |       Strength: moderate (single model only)
    |       Gap: no replication on other architectures
    |
    +-- [Key Finding 3: Negative gate values drive sharpening effect]
    |       Evidence: conditional ablation, case (iii) dominant
    |       Claim: first observation of functional negative gate values
    |       Strength: potentially high but statistically unquantified
    |       Gap: no significance test between conditions; concurrent work
    |
    +-- [Key Finding 4: Weakening neurons activate very often]
            Evidence: strong negative correlation with cos(w_in,w_out)
            Claim: strengthening neurons are sparse, weakening are dense
            Strength: moderate (confounders not controlled)
```

### ASCII Diagram — Revision Strategy Roadmap

```text
Priority 0 (Must, before resubmission):
  [W1: Single-model ablation]
      -> Replicate on Llama-3.2-3B (5M tokens)
      -> Expected gain: generality evidence
  [W2: Conditional ablation statistics]
      -> Add mean/SD per condition + significance test
      -> Expected gain: quantitative support for central claim
  [W3: "First" claim qualification]
      -> Qualify/remove "first" in abstract
      -> Add comparison to Kong et al. (2025)
      -> Expected gain: factual accuracy, reviewer trust

Priority 1 (Nice-to-have, high impact):
  [W4: Preprocessing robustness]
      -> Verify main results without sign-flip preprocessing
      -> Expected gain: taxonomy robustness
  [W5: Metric justification]
      -> Add 1-sentence motivation per metric in main text
      -> Expected gain: improved reading flow

Priority 2 (Nice-to-have, moderate impact):
  [W6: Confounder control for activation frequency]
      -> Partial correlation controlling for weight norms
      -> Expected gain: stronger causal interpretation
  [W8: Threshold sensitivity analysis]
      -> Vary tau in [0.3,0.7], report class-size changes
      -> Expected gain: taxonomy stability evidence
```

### ASCII Diagram — Related-Work Taxonomy Tree (Layered)

```text
Mechanistic Interpretability of LLMs (Root)
├── Branch 1: Neuron-Level Analysis
│   ├── Leaf 1.1: Context-based neuron classification
│   │   └── Voita et al. (2024) — token detectors
│   ├── Leaf 1.2: Output-weight-based analysis
│   │   └── Gurnee et al. (2024) — suppression neurons, cosine computation
│   ├── Leaf 1.3: Key-value memory framework
│   │   └── Geva et al. (2021) — FF layers as memories
│   └── Leaf 1.4: Read-write functionality (THIS PAPER)
│       └── Cosine similarity of input/output weights for gated neurons
│
├── Branch 2: Feature-Level Analysis
│   ├── Leaf 2.1: Sparse autoencoders (SAEs)
│   │   └── Sharkey et al. (2022), Elhage et al. (2022)
│   └── Leaf 2.2: SAE criticism & middle ground
│       └── Kantamneni et al. (2025), Gurnee et al. (2023)
│
├── Branch 3: Residual Stream & Representation
│   ├── Leaf 3.1: Iterative inference hypothesis
│   │   └── Belrose et al. (2023), Rushing & Nanda (2024)
│   ├── Leaf 3.2: Linear representation hypothesis
│   │   └── Park et al. (2024)
│   └── Leaf 3.3: Input-output head analysis
│       └── Elhelo & Geva (2024) — heads, not neurons
│
└── Branch 4: Gating Mechanism Analysis
    ├── Leaf 4.1: Gated activation function introduction
    │   └── Shazeer (2020) — SwiGLU
    └── Leaf 4.2: Negative gate value functionality
        └── Kong et al. (2025) — concurrent work, different phenomenon
        └── THIS PAPER — weakening neurons & conditional ablation
```

**Novelty & comparison note:** This run operates in Retrieval-Disabled Mode (external paper search unavailable). The novelty and comparison judgments above are deferred for manual verification against full literature. The taxonomy tree is built from the paper's own references and should be independently validated. Claims about being "first" to investigate gated-neuron RW behavior or to observe negative gate-value mechanisms must be verified against prior art not cited in this manuscript.

**Page Coverage Audit:** The paper content spans pages 1-9 in the PDF, with main substantive content concentrated on a single logical page (page 1 in the viewer). All 12 annotations were placed on this page, covering: Abstract (1 annotation), Introduction (3 annotations), Related Work (1 annotation), Method/Preliminaries (2 annotations), Experiments (4 annotations), Conclusion (1 annotation). The appendix and reference pages (pages 2-9) contain supplementary figures, references, and technical details that were noted but not separately annotated as they are non-substantive support material. Coverage is balanced across sections and no substantive paragraph was skipped on the main content page.

**Final Score: 6.5/10**