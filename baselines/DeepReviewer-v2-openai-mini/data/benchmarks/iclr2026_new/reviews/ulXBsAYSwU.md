## Summary
# Final Review Report

## Summary

This paper presents MolMiner, a fragment-based autoregressive generative model for molecular design that integrates three capabilities: (1) dynamic 3D geometry awareness via forcefield relaxation during generation, (2) symmetry-aware fragment attachment handling, and (3) order-agnostic rollout that allows molecules to be grown from any fragment in any valid order. The model supports conditional generation over 12 physicochemical and structural properties using a GMM-based probabilistic conditioning mechanism. Experiments on the ZINC drug-like subset show calibrated conditional control for most properties and competitive (though systematically biased) unconditional generation compared to HierVAE.

**Core strengths:** The unified architecture targeting multi-property conditioning is a relevant and under-explored direction. The order-agnostic rollout with dynamic geometry is technically sound, and the calibration-based evaluation protocol is more informative than simple aggregate metrics. The symmetry-aware fragment handling is a practical contribution that addresses a real engineering challenge in fragment-based generation.

**Core weaknesses:** (i) The unconditional generation quality shows systematic 2-3x larger Wasserstein distances on molecular weight, TPSA, and MR compared to the HierVAE baseline—this gap is understated in the paper. (ii) Conditional generation evaluation lacks baselines, quantitative aggregate metrics, and multi-property joint conditioning tests. (iii) The "first model" claim is unverifiable without broader literature comparison (deferred). (iv) The implicit conditioning design without auxiliary loss has known failure modes (QED) that are insufficiently analyzed. (v) The conclusion introduces unsupported broader-impact claims that may reduce reviewer confidence.

## Strengths
**S1 — Unified multi-property conditional generation with practical value.** MolMiner's core achievement is demonstrating that a single autoregressive framework can conditionally generate molecules over 12 properties simultaneously with reasonable calibration for most properties. This is a non-trivial engineering and modeling accomplishment. The GMM-based partial conditioning (specify any subset, sample the rest) is a user-friendly design that addresses a real need in high-throughput screening pipelines where only some property targets are known upfront.

**S2 — Thoughtful methodological contributions.** The combination of order-agnostic rollout (randomized attachment order) with dynamic forcefield-based geometry updates is novel in the fragment-based generative space. The symmetry-aware attachment handling (Section 3.2) addresses a genuine technical challenge that prior fragment-based models (e.g., MoLeR) did not systematically solve. The use of Morgan fingerprint similarity to resolve cyclic permutation ambiguities is practical and principled.

**S3 — Informative evaluation protocol.** Instead of reporting only aggregate metrics, the paper proposes Wasserstein-distance-based distributional comparisons (unconditional) and calibration plots (conditional) that reveal per-property control quality. This is a meaningful improvement over single-number summarization and allows readers to distinguish between well-controlled and poorly-controlled properties.

**S4 — Honest limitations section.** The paper explicitly identifies the unconditional performance gap and hypothesizes a mechanism (termination imbalance). While this hypothesis needs quantitative support (see Weaknesses), the presence of a dedicated Limitations section that directly addresses the paper's shortcomings is a positive sign of scientific maturity.

**S5 — Reproducibility-oriented details.** The paper reports computational requirements (7 days RTX 3090, 70 GB RAM) and commits to releasing code, model checkpoints, and processed data. The use of RDKit's canonical SMILES and SSSR decomposition is clearly specified, supporting reproducibility.

## Weaknesses
**W1 — Unconditional performance gap is understated and the single baseline is dated.** (Severity: Major; Fatal: No)
Table 1 shows that MolMinerD has Wasserstein distances of 47 (vs 15 for HierVAE) on molecular weight, 11.9 (vs 3.8) on MR, and 7.6 (vs 2.3) on TPSA — gaps of 2-3x, not "modest differences" as claimed. The paper attributes part of this to GMM approximation error but acknowledges it does not fully explain the gap. Furthermore, HierVAE (2020) is the only unconditional baseline; newer fragment-based models (e.g., MARS, MolLeR) are excluded with partially justifiable but incomplete reasoning. The MolLeR comparison, run for only two mini-epochs over seven days, is inconclusive. A stronger evaluation would include convergence-guaranteed runs or acknowledgment of baseline limitations. (*Issue annotation: Page 1 - Experimental Results interpretation paragraph*)

**W2 — Conditional generation lacks baselines, quantitative metrics, and multi-property testing.** (Severity: Major; Fatal: No)
The conditional evaluation (Section 4.3) presents calibration plots but provides no aggregate quantitative summary (e.g., mean calibration error, R² per property, or rank correlation). There is no baseline comparison — the paper's strongest claim ("first model to support simultaneous conditioning across 12 properties") is presented without context for how poorly/easily a simpler baseline (e.g., linear regression on fragments, CVAE) would perform. Moreover, the evaluation varies one property at a time while sampling the rest from the GMM, which tests single-property rather than true multi-property control. Joint conditioning on multiple extreme values is not evaluated. (*Issue annotation: Page 1 - Conditional Generation section*)

**W3 — Termination imbalance hypothesis is unsupported by quantitative evidence.** (Severity: Major; Fatal: No)
The Limitations section hypothesizes that order-agnostic rollups cause a termination imbalance that biases the model toward smaller molecules. While plausible, no data supports this claim — no termination frequency statistics, no per-molecule correlation between termination count and size error, and no evidence that the proposed fixes (balancing termination actions or RL fine-tuning) would resolve the gap. Without quantitative backing, this section reads as speculation, which weakens the paper's scientific rigor. (*Suggestion annotation: Page 1 - Limitations section*)

**W4 — Implicit conditioning design has known failure modes that are insufficiently analyzed.** (Severity: Major; Fatal: No)
The model uses implicit conditioning (properties as inputs, no auxiliary loss). The paper notes QED calibration degrades (Figure 2) but does not analyze why or whether an explicit property-prediction loss would help. Other properties with systematic deviations (molWt, MR) also correlate with the termination bias. The paper should include an ablation comparing implicit vs explicit conditioning to isolate whether the calibration gaps stem from the objective design or from model capacity / termination bias. (*Suggestion annotation: Page 1 - Training Objective section*)

**W5 — Equation (2) omits a critical hyperparameter (σ).** (Severity: Minor; Fatal: No)
The Gaussian-decayed distance kernel in the geometry-aware attention mechanism depends on an unspecified bandwidth σ. Whether σ is learned, fixed, or cross-validated is not stated. This omission impairs reproducibility and prevents readers from understanding the spatial scale at which geometric attention operates. The ablation mentions that positive bias initialization helps, but without σ specification, various distance scales could lead to very different attention patterns. (*Issue annotation: Page 1 - Model Architecture, Eq(2)*)

**W6 — Conclusion introduces unsupported broader-impact claims.** (Severity: Major; Fatal: No)
The final paragraph of the Conclusion claims MolMiner could "accelerate discovery... sustainable energy storage... organic redox flow batteries... organic photovoltaics... drug discovery... green chemistry." None of these applications are tested or even directly supported by the paper's experiments on a ZINC subset. Such unsupported claims signal over-selling and may reduce reviewer confidence even in valid contributions. Recommending removal or replacement with bounded future directions. (*Issue annotation: Page 1 - Conclusion final paragraph*)

**W7 — "First model" claims require external verification.** (Severity: Verification; Fatal: No)
Both the Abstract and Conclusion claim that MolMiner is "the first model to unify [four capabilities]." Due to Retrieval-Disabled Mode, external literature verification is unavailable in this run. The authors should conduct a thorough prior-art search and qualify the novelty claim with explicit comparisons to the most closely related prior work covering each capability dimension. Until then, this claim cannot be accepted at face value. (*Suggestion annotation: Page 1 - Abstract / Conclusion*)

**W8 — Related Work is overly compressed.** (Severity: Minor; Fatal: No)
The entire related work is a single dense paragraph that contrasts MolMiner against JTNN, HierVAE, G-SchNet, and MoLeR across multiple dimensions simultaneously, making it hard to track comparison axes. Restructuring into 2-3 focused sub-paragraphs organized by theme (fragment-based methods, order-agnostic/3D-aware methods, conditional generation) would improve readability and positioning clarity. (*Suggestion annotation: Page 1 - Related Work section*)

**W9 — RAM usage (70 GB) vs hardware specification inconsistency.** (Severity: Verification; Fatal: No)
Section 7 states RAM usage of 70 GB, but the model was trained on a single NVIDIA RTX 3090 (24 GB VRAM). The "RAM" terminology likely refers to system memory rather than GPU memory, but this should be clarified to avoid confusion. If GPU memory exceeded 24 GB, multi-GPU or memory optimization details would be needed for reproducibility. (*Verification issue*)

**W10 — Lack of statistical significance and variance reporting.** (Severity: Major; Fatal: No)
Results are reported without variance across multiple training runs or seeds. For unconditional generation (Table 1), a single set of Wasserstein distances is presented without confidence intervals. The conditional calibration plots show prediction variance but not model variance. Given the stochasticity of training (single-rollout Monte Carlo estimation), reporting at least 2-3 seed runs would improve confidence in the reported numbers.

## Score
**Final Score: 5.5/10**

**Scoring rationale (evidence-grounded):**

The score prioritizes research value and novelty as primary dimensions, consistent with the scoring policy.

- **Research value (6/10):** The unified multi-property conditioning framework addresses a relevant and practical problem in molecular design. The order-agnostic rollout with dynamic geometry is a meaningful engineering contribution. However, the actual empirical gains over the 2020 HierVAE baseline are mixed — MolMiner underperforms on key properties (molecular weight, TPSA, MR) by 2-3x in Wasserstein distance, and the conditional evaluation lacks baselines needed to quantify added value. The paper's practical impact is currently limited to a single ZINC subset benchmark without domain-specific validation.

- **Novelty (5/10):** The combination of fragment-based generation with order-agnostic rollout, dynamic 3D geometry, and multi-property conditioning is novel at the system level. However, individual components have prior art: order-agnostic generation (G-SchNet), fragment-based assembly (JTNN, HierVAE), and property conditioning (various VAE/diffusion approaches). The symmetry-aware attachment protocol is a genuine technical novelty. The "first model" claim requires external verification (Retrieval-Disabled Mode active this run; novelty verdicts are deferred).

- **Validity/soundness (5/10):** The method is internally consistent and the mathematical formulation is correct. However, the evaluation has significant gaps: no quantitative conditional metric, no multi-property joint conditioning test, no statistical significance/variance reporting, and a key hypothesis (termination imbalance) is unsupported by evidence. The single-rollout Monte Carlo estimator's variance and potential impact on training are unexplored.

- **Reproducibility (6/10):** The paper commits to releasing code, checkpoints, and data. The method description is largely complete, though the undefined σ in Eq(2) and the ambiguous "70 GB RAM" vs "RTX 3090" specification need clarification.

**Weaknesses limiting the score:** (W1) understated unconditional gap with dated baseline, (W2) missing conditional baselines and quantitative metrics, (W4) insufficient analysis of implicit conditioning failure modes, (W6) unsupported conclusion claims, (W10) no variance/seed reporting.

**Key strengths supporting the score:** (S1) unified multi-property conditioning framework, (S2) thoughtful methodological contributions (order-agnostic + 3D + symmetry handling), (S3) informative calibration-based evaluation protocol.