## Summary
# Final Review Report

## Summary

This paper presents a learnable neural implementation of the Gray-Wyner Network for lossy multi-task source coding. The authors develop a three-channel codec (one common + two private representations) that disentangles shared information from task-specific details across pairs of computer vision tasks. The theoretical contributions include: (i) extending Wyner's lossless bounds for common information to the lossy setting (Theorem 1), establishing relationships between Gács-Körner and Wyner's lossy common information via interaction information; (ii) deriving a tractable optimization objective (Theorem 2) that replaces mutual information terms with entropy-based rate functions, enabling a Lagrangian relaxation that trades off transmit and receive rates via a single hyperparameter β; and (iii) a specific neural architecture with a hard-matching mechanism to combine common representations from two encoder branches.

The empirical evaluation covers synthetic data, controlled MNIST edge-cases with known mutual information, and two real-world vision benchmarks (Cityscapes for segmentation+depth, COCO for detection+keypoint). The method is compared against Joint (single shared channel), Independent (no common channel), Separated, and Combined architectures. Results show that the proposed method outperforms Independent coding and approaches Joint coding performance, with BD-rate advantages reported.

**Key Strengths:** The paper makes a principled connection between classical Gray-Wyner information theory and modern learnable compression, which is novel and timely. The theoretical framing (lossy common information bounds, transmit-receive tradeoff) is rigorous. The controlled edge-case experiments on MNIST with known PMFs provide strong validation of the method's behavior.

**Key Weaknesses:** (1) No statistical uncertainty quantification (variance, confidence intervals) across any experiment, undermining confidence in the headline -81.58% BD-rate claim. (2) The central quantitative claim is not traceable to reported data. (3) The hard-matching mechanism (Eq. 14) may create gradient starvation and its design is not empirically justified. (4) The Markov conditions underpinning the theory are trivially satisfied in the single-source experimental setup, creating a theory-experiment gap. (5) Results depend on frozen task models with no robustness testing across architectures.

## Strengths
1. **Principled Theory-Practice Bridge:** The paper successfully connects classical Gray-Wyner information theory with modern learnable compression. The derivation of the lossy common information bounds (Theorem 1) and the tractable entropy-based optimization objective (Theorem 2) are mathematically sound and provide a solid foundation for the proposed architecture.

2. **Novel Problem Framing:** The transmit-receive rate tradeoff is a well-motivated and practically relevant concept. The paper clearly articulates why three channels (one common, two private) are needed for two-task distributed inference, moving beyond the two-channel assumption in prior coding-for-humans-and-machines work.

3. **Controlled Edge-Case Validation:** The MNIST experiments with three different PMFs (Dependent, Independent, Mixture) are a strong validation strategy. By designing scenarios with known mutual information, the authors convincingly demonstrate that the method behaves as expected — placing more information on the common channel when tasks share more information, and less when they share less.

4. **Comprehensive Architecture Comparison:** The paper evaluates and compares four different encoder architectures (Shared, Separated, Combined, Joint) across multiple settings, providing useful empirical evidence about the design choices.

5. **Open Science:** Code is publicly available, which supports reproducibility and follow-up research.

## Weaknesses
### W1. Missing Statistical Uncertainty Quantification (Major)
No experiment in the paper reports variance, confidence intervals, or multi-seed statistics. All rate-distortion curves and BD-rate values are presented as single-run point estimates. Given that the central quantitative claim is a BD-rate advantage of -81.58% over independent coding, the lack of uncertainty quantification is a significant concern. Readers cannot assess whether the reported improvements are statistically reliable or whether the optimal β=3/2 result is robust to initialization. *Page 7-8 - Experimental Evaluation (Section 4.1-4.3).*

**Impact:** Undermines confidence in all quantitative conclusions. The ranking of architectures (Shared vs Separated vs Combined) and the comparison of β values may not be statistically significant.

**Required Action (Must):** Report mean ± std over ≥3 random seeds for all key experiments. Add confidence intervals for BD-rate comparisons. Include a statistical test (e.g., paired bootstrap) for the main claim that the proposed method outperforms Independent coding.

### W2. Untraceable Headline BD-Rate Claim (Major)
The conclusion states "our codecs achieved, on average, a BD-rate advantage of -81.58% in transmit rate, against single-task codecs." This number cannot be verified from the reported data. Figure 5 reports BD-rates relative to the Joint method, not single-task codecs. The synthetic experiment does not report BD-rates. The calculation methodology is not described. A BD-rate of -81.58% would be an extraordinarily large improvement (>5x bitrate reduction) that demands careful explanation and traceability. *Page 9 - Summary and Conclusion (Section 5).*

**Impact:** The paper's headline quantitative result is not reproducible from the published data, which is a serious scientific reporting issue.

**Required Action (Must):** Provide a complete breakdown of the BD-rate calculation: formula, per-experiment values, and averaging method. Ensure all numbers can be directly traced to tables or figures. If the -81.58% is the average of (1 - BD_Rate_Proposed/BD_Rate_Independent) across experiments, state this explicitly with per-experiment components.

### W3. Theory-Experiment Gap in Source Assumptions (Major)
The theoretical framework (Sections 2.1-3.2) is developed for two distinct sources X₁ and X₂, with Markov conditions (Eq. 1) that prevent cross-source information transfer. However, the experiments (Section 4) specialize to a single source X where (X₁, X₂) = X, making the Markov conditions trivially satisfied. The paper does not discuss whether results would generalize to truly distinct sources, nor does it characterize what happens when conditions (1) are violated. *Page 7 - Experimental Evaluation (Section 4) and Page 2-3 - Preliminaries.*

**Impact:** The empirical validation does not match the theoretical framing. Claims about the framework's applicability to multi-source settings are not supported by evidence.

**Required Action (Must):** Add an experiment or discussion addressing the distinct-source scenario. At minimum, discuss the conditions under which the method would handle X₁ ≠ X₂ and the expected performance degradation when Markov assumptions are violated.

### W4. Hard-Matching Gradient Starvation Risk (Major)
The common channel combination (Eq. 14) uses a hard mask: elements that do not match exactly between the two encoder branches are set to zero. During training, gradients from the common channel only flow through matching elements, creating a potential chicken-and-egg problem — common representations cannot improve via gradient descent unless they already match. The auxiliary L2 loss (Eq. 15) encourages matching, but the interaction between this hard mask and gradient-based optimization is not analyzed empirically. *Page 6 - Method (Section 3.3).*

**Impact:** This design choice may limit learning efficiency and could explain the gap between the proposed method and the Joint baseline. Without an ablation study comparing hard vs soft matching, the optimality of this design is not established.

**Required Action (Nice-to-have):** Add an ablation comparing hard-matching against (a) simple averaging and (b) soft-alignment (e.g., weighted by sigmoid of difference magnitude). Report the fraction of matched vs zeroed elements during training to quantify common channel utilization.

### W5. Frozen Task Model Dependency (Major)
The Cityscapes and COCO experiments freeze pre-trained task models (DeepLabV3+, Faster R-CNN, etc.) and train only the codec. The BD-rate advantage is conditional on these specific architectures. The paper does not test whether the improvement generalizes to alternative task model families (e.g., transformers, UNet, DPT). Different task models may have different feature requirements, and the codec's ability to distill common information could vary substantially. *Page 9 - Experiments (Section 4.3).*

**Impact:** Limits the generality of the claimed improvements. The practical value of the method across diverse deployment scenarios is untested.

**Required Action (Nice-to-have):** Test with at least one alternative task model per benchmark to assess robustness. Add a discussion paragraph acknowledging that results are conditional on the choice of task model.

### W6. Incomplete Comparison Against Prior Work (Moderate)
The Related Work section covers coding-for-humans-and-machines and multitask codecs but does not include a quantitative comparison. The paper would benefit from a systematic comparison table showing how the proposed method differs from prior Gray-Wyner-related work in terms of key properties (learnable vs analytic, lossy vs lossless, number of sources, task type). The novelty positioning — that this is the first learnable Gray-Wyner network — should be stated explicitly in the introduction. *Page 1-2 - Previous Work (Section 2).*

**Impact:** Without explicit positioning, readers familiar with the Gray-Wyner literature may not immediately recognize the paper's specific contribution.

**Required Action (Nice-to-have):** Add a comparison table in Related Work. Make the "first learnable Gray-Wyner network" claim explicit in the introduction's contribution list.

### W7. Abstract Overclaims Relative to Joint Baseline (Minor)
The abstract states the method "substantially reduces redundancy and consistently outperforms independent coding." This is true but omits the more relevant comparison: the Joint baseline consistently achieves better rate-distortion performance. The framing could mislead readers about the method's absolute performance. *Page 0 - Abstract.*

**Impact:** Minor — does not affect scientific validity, but reduces precision of contribution communication.

**Required Action (Nice-to-have):** Revise abstract to mention that the method approaches Joint coding performance while enabling flexible transmit-receive tradeoffs.

### W8. Missing Analysis of Common Channel Efficiency (Minor)
The paper demonstrates that the common channel rates change as expected with β, but does not quantify how efficiently the common channel captures shared information. Measuring I(Y₁; Y₂ | Y₀) — the mutual information between tasks given the common representation — would directly test whether the common channel successfully extracts shared information. *Page 3-4 - Theory, Page 7-9 - Experiments.*

**Impact:** Minor — the qualitative behavior is clear, but a direct information-theoretic diagnostic would strengthen the validation.

**Required Action (Nice-to-have):** Compute and report I(Y₁; Y₂ | Y₀) for key experiments to directly measure common information capture efficiency.

## Score
**Final Score: 6/10**

**Rationale:** The paper presents a conceptually novel and theoretically principled connection between Gray-Wyner information theory and learnable compression, which is a genuine research contribution. The controlled edge-case experiments are well-designed and provide valid qualitative validation of the approach.

However, the score is constrained by several significant weaknesses that directly affect the reliability of the paper's claims:

1. **Missing statistical validation (W1):** The complete absence of variance reporting or significance testing means the central quantitative results cannot be evaluated for reliability. This is a fundamental methodological gap for an empirical paper.

2. **Untraceable headline claim (W2):** The -81.58% BD-rate advantage cannot be verified from reported data, which undermines the paper's most impactful quantitative statement.

3. **Theory-experiment mismatch (W3):** The theoretical framework assumes two distinct sources, but experiments use a single source, limiting the empirical support for the theoretical claims.

4. **The novelty assessment is deferred** due to the retrieval-disabled mode in this review run. The paper claims to present the first learnable Gray-Wyner network; this claim requires manual literature verification before it can be validated.

The paper has solid conceptual merit and the theoretical development is sound. With proper statistical reporting, traceable quantitative claims, and additional experiments addressing the theory-experiment gap, the contribution could be significantly strengthened. The current presentation does not yet provide sufficient evidence to justify a higher score.