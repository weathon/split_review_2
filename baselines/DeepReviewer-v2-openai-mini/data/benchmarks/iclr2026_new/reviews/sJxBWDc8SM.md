## Summary
# Final Review Report

## Summary

This paper investigates the practical differences between Transformers and modern recurrent (SSM) models on two synthetic benchmarks—multi-query associative recall (MQAR) and copying—which are known to correlate with language modeling capabilities. Through over 3,000 runs and ~20,000 GPU hours, the authors demonstrate that SSMs (Mamba, Hyena) exhibit critical optimization instability: their success is confined to a narrow window of learning rates, while Transformers perform robustly across a wide range. This finding re-contextualizes prior claims that SSMs have fundamental expressivity limitations, suggesting that optimization challenges—not inherent expressivity—may be the primary differentiator in many settings. The paper further reveals contrasting scaling behaviors (SSMs favor width, Transformers favor depth), shows that single-layer SSMs can solve recall while single-layer Transformers cannot, and identifies architectural components (1D convolution, DeltaNet-style Householder mixing) that influence stability. The paper's main strength is its thorough empirical investigation with comprehensive learning rate sweeps. Its main weaknesses are: (1) over-strong claims that exceed the evidence scope (e.g., claiming the gap is "mainly" due to optimization rather than expressivity, when the evidence covers only two synthetic tasks); (2) confounded experimental comparisons (Table 1's width-vs-depth comparison varies multiple factors simultaneously); (3) a mismatch between some narrative claims and the presented visual evidence (e.g., Mamba's claimed "loss bump" is not clearly visible); and (4) missing mechanistic validation for the gradient-based explanation of DeltaNet's stability. Novelty verification is deferred in this run due to retrieval service unavailability.

## Strengths
**1. Comprehensive empirical methodology.** The paper's experimental protocol is a clear strength. With over 3,000 runs across 5 seeds and extensive learning rate grid searches spanning multiple orders of magnitude, the authors provide a thorough characterization of optimization sensitivity. This level of rigor is rare in the SSM-vs-Transformer comparison literature and directly addresses the concern that prior studies may have drawn conclusions based on suboptimal hyperparameters.

**2. Important, timely research question.** The paper tackles a genuinely important question: whether the SSM-Transformer performance gap stems from expressivity limits or optimization difficulties. This question is highly relevant to the current rapid adoption of SSMs in production systems (e.g., Mamba-based models), and the paper's framing of "learnability" as a key axis of comparison is valuable for guiding future architecture research.

**3. Clear and well-structured presentation of findings.** The paper is well-organized, with each main contribution (optimization instability, scaling behavior, 1-layer dynamics, architectural drivers) receiving a dedicated section. The figures (especially Figure 1 showing the narrow LR window) are effective at communicating the central finding. The use of both MQAR and Copying tasks helps validate that the observed phenomena are not task-specific.

**4. Valuable ablation studies in Section 7.** The ablation experiments isolating the role of convolution, gating, S6 mixer, and positional encodings are informative. The finding that a 1-layer Transformer + convolution can solve MQAR (99%) is particularly striking and provides a concrete architectural insight. The inclusion of DeltaNet as a more stable alternative offers a practical forward-looking direction.

**5. Honest limitation disclosure.** The conclusion explicitly acknowledges that the analysis is limited to synthetic benchmarks and that formal theoretical explanation for the optimization brittleness remains open. This transparency strengthens the paper's credibility.

## Weaknesses
### W1 (Major): Central thesis over-claimed beyond evidence scope

**Evidence:** Page 2 (lines 21-22) states as central thesis: "Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics." The same strong claim appears in the abstract and conclusion.

**Problem:** The paper's evidence is limited to two synthetic benchmarks (MQAR and Copying) with specific SSM families (Mamba, Hyena). The phrase "not...but mainly" creates a false dichotomy that contradicts the paper's own finding at low widths (Hyena still underperforms Transformers even with optimal tuning, as acknowledged on page 5 line 76: "a sizable gap with Transformers can still be observed at low widths"). The paper does not provide formal expressivity analysis, only empirical performance comparisons on two tasks. Furthermore, the conclusion's prescription that "future research should treat optimization stability as a first-class objective" is reasonable but not directly validated on real downstream tasks.

**Impact:** Overclaiming the central thesis reduces scientific credibility and invites justified criticism from reviewers familiar with expressivity literature where architectural capacity differences are established. It also obscures the paper's genuine contribution: demonstrating that optimization plays a *larger role than previously recognized*, which is a valuable but more nuanced claim.

**Required action:** Reframe the central thesis as a hypothesis with appropriate scope qualifiers. Replace "not...but mainly" with softer wording such as "a substantial part of the performance gap may stem from optimization difficulties, and learnability differences play a larger role than previously recognized." (Page 1 - Abstract, Page 2 - Introduction, Page 8 - Conclusion)

### W2 (Major): Width-vs-depth scaling evidence has confounds

**Evidence:** Table 1 (page 6) compares Mamba 24L/1024W (150M, 16%) vs Mamba 12L/1408W (150M, 100%). Section 5 (page 6 lines 85-86) claims that "attempts to provide fair comparisons by matching parameter counts through increased depth in SSMs are misguided."

**Problem:** The Table 1 comparison varies both width (1024 → 1408) and depth (24 → 12) simultaneously, making it impossible to attribute the performance difference to width alone versus the combination of width increase + depth reduction. Additionally, the deeper (24-layer) configuration has more nonlinearities and potentially different gradient flow dynamics, which independently affect trainability. The claim that SSMs "must be scaled along...width" is only partially supported because the experiment does not independently control for depth vs width. Furthermore, the depth-scaling claim for Transformers ("depth for Transformers") is not tested: there is no parameter-matched shallow-wide Transformer baseline for comparison.

**Impact:** This weakens one of the four main contributions (Contrasting Scaling Behavior). The strong normative language ("misguided") is not warranted by the experimental design.

**Required action:** (a) Soften the language from "misguided" to a more measured observation. (b) Add explicit discussion of the confound. (c) Acknowledge that the depth-scaling claim for Transformers was not tested. (Page 5-6 - Sections 4-5)

### W3 (Major): Missing quantitative anchors in main text

**Evidence:** Section 3 (page 4 lines 56-57) states that "carefully tuned learning rates" "drastically improve performance" but provides no concrete numbers in the main text. Specific accuracy figures and LR values are deferred to Appendix A.3.

**Problem:** The paper's core empirical claim—that proper LR tuning can make SSMs solve MQAR at small hidden sizes—requires readers to cross-reference the appendix to evaluate its strength. Without concrete numbers in the main text, the claim appears unsupported. For example, saying "Mamba becomes capable of solving MQAR at relatively small hidden model sizes" without stating the actual hidden size, LR, and accuracy is insufficient for a claim that challenges prior work.

**Impact:** Reviewers cannot immediately verify the strength of the empirical evidence supporting the paper's central thesis. This weakens the paper's persuasive power.

**Required action:** Add at least one specific quantitative anchor in the main text (e.g., "with sequence length 512 and hidden size 128, Mamba accuracy improved from near 0% under the prior LR grid to 98.4% with our optimal LR of 1e-3"). (Page 4 - Section 3 Results paragraph)

### W4 (Major): Claim of Mamba "loss bump" not clearly supported by figure evidence

**Evidence:** Section 6 (page 7 line 103) states that Mamba exhibits "a significant loss bump" similar to Attention, and point 1 (line 104) further reinforces this. However, Figure 6 (described on page 6) shows Mamba(64) converging smoothly to near-zero loss within ~5000 steps with no visible bump.

**Problem:** The paper attempts to draw a mechanistic parallel between Mamba and Attention based on a claimed loss bump. But the presented evidence (Figure 6) does not clearly show this bump for Mamba. Only Attention(2048) shows the characteristic phase transition. The claim that Mamba's dynamics are "mixed" is supported, but the statement that Mamba exhibits a "significant loss bump" like Attention is not visually verifiable from the figure as described. This narrative-figure mismatch weakens the induction head analysis.

**Impact:** The induction head analogy is presented as one of the four main contributions (Divergent Single-Layer Dynamics). If the key evidence for the Mamba-Attention connection is not clearly visible, this contribution loses force.

**Required action:** Either (a) provide a zoomed-in plot or additional LR configuration showing the Mamba loss bump more clearly, or (b) revise the text to honestly reflect that Mamba's dynamics are generally smooth and only occasionally show minor perturbations. (Page 6-7 - Section 6)

### W5 (Moderate): DeltaNet stability mechanism is hypothesized, not validated

**Evidence:** Section 7 (page 8 lines 124) states that "the off-diagonal terms such as C_N ∏ A_k B_0 do not necessarily incur vanishing gradients" for DeltaNet because of Householder matrices, while Mamba's A_k induces gradient decay.

**Problem:** This mechanistic claim about gradient dynamics is presented as an explanation for DeltaNet's superior stability but is not directly validated. The paper provides no gradient norm measurements, no analysis of the A_k eigenvalues during training, and no ablation isolating the Householder property from other DeltaNet design choices. The evidence is purely correlational: DeltaNet works better, and the Householder property is consistent with improved gradient flow. Without direct validation, this remains a plausible hypothesis rather than an established mechanism.

**Impact:** Claim C3 (Architectural Drivers to Stability) would be strengthened by mechanistic validation. As presented, the paper identifies *which* components affect stability but not *how* they do so at the gradient level.

**Required action:** (a) Add gradient norm comparisons across Mamba, Mamba2, and DeltaNet during training, or (b) explicitly frame this as a hypothesis and note that direct gradient measurement is needed for confirmation. (Page 8 - Section 7, Newer architectures paragraph)

### W6 (Minor): Notation incompleteness in SSM formulation

**Evidence:** Page 3 (lines 41-45): The SSM recurrence defines Z_i = A_i Z_{i-1} + B_i X_i with X ∈ R^{N×d}, but does not specify the dimension of state Z_i or matrices A_i, B_i, C_i, D_i. Eq. (1) has a typo ("admits a an") and mixed indexing (0-index vs 1-index for B_0 and the product range).

**Impact:** Reduces reproducibility and signals technical imprecision.

**Action:** Define all dimensions explicitly and fix typo. (Page 3 - Background: Transformers and SSMs)

### W7 (Minor): Introduction paragraph could be better structured

**Evidence:** The "Attention" paragraph (page 1, line 9) serves four distinct roles (mechanism description, complexity discussion, application list, approximation connections) in one dense block.

**Impact:** Reduces readability and makes it harder for readers to extract the key contrasts.

**Action:** Split into two focused paragraphs. (Page 1 - Introduction: Attention paragraph)

---

### Page Coverage Audit

Due to the PDF extraction format (all content in a single page in the tool), page-level counts are aggregated. All substantive sections (Abstract, Introduction paragraphs, Background, Sections 3-8, Conclusion) received at least one annotation. Non-substantive pages (Ethics Statement, Reproducibility Statement, Acknowledgments, References) were skipped as they are standard boilerplate.

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses a timely and important research question with impressive empirical thoroughness (3000+ runs, extensive LR grid sweeps). The core finding—that SSM optimization instability can confound expressivity comparisons—is a genuine contribution that should influence future research practices. However, the paper's impact is limited by four factors that directly affect its research value:

1. **Overclaimed central thesis (W1):** The strong "not expressivity but optimization" framing exceeds what the evidence supports (only two synthetic tasks), reducing the paper's scientific credibility and forcing readers to mentally qualify every major claim.

2. **Confounded experimental evidence for a core claim (W2):** The width-vs-depth scaling comparison, presented as a main contribution, has a confounded design that weakens its evidentiary value.

3. **Missing quantitative anchors (W3) and figure-narrative mismatch (W4):** These presentation issues reduce the persuasive power of the empirical evidence.

4. **Novelty is unverifiable in this run (Retrieval-Disabled Mode).** The paper's relationship to prior work (e.g., Arora et al. 2023, Jelassi et al. 2024, Waleffe et al. 2024) is acknowledged within the manuscript, but independent verification of novelty claims requires manual literature review.

**Scoring breakdown:**
- Research value / importance: 8/10 (timely question, well-motivated)
- Soundness / validity: 5/10 (claims exceed evidence, confounded comparisons)
- Novelty: Deferred (requires manual verification)
- Reproducibility: 7/10 (code released, hyperparameters in appendix, but missing some key numbers in main text)
- Presentation / clarity: 6/10 (well-structured but overclaiming and some figure-text mismatches)

**Recommended revision priority (post-review):** Reframe central thesis with scope qualifiers (P0) → Add quantitative anchors in main text (P0) → Address confound discussion in Table 1 (P1) → Clarify Mamba loss bump evidence (P1) → Add gradient measurements or hedge DeltaNet mechanism claim (P2).