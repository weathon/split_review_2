## Summary
This paper presents a systematic study of benchmark contamination detection in Large Reasoning Models (LRMs), structured around two realistic contamination scenarios. In Stage I (pre-LRM), the authors show that while SFT contamination of a base model is initially detectable, subsequent GRPO (Group Relative Policy Optimization) training systematically conceals contamination signals across 10 detection methods, with AUROC dropping by up to 19.84 percentage points. Through theoretical analysis (Theorem 3.1) and controlled ablations comparing RAFT, RAFT++, and GRPO, the authors identify PPO-style importance sampling and clipping as the root cause of this concealment. In Stage II (post-LRM), they demonstrate that extensive SFT contamination with chain-of-thought data applied to advanced LRMs yields substantial performance inflation (e.g., +11.76% on DeepSeek-R1-Distill-Llama-8B) while all tested detection methods perform near random guessing (AUROC ≈ 50%). The paper's core contribution is exposing a critical vulnerability: current contamination detection methods, designed for standard LLMs under memorization assumptions, are fragile against RL-based training dynamics and CoT generalization in LRMs. The findings underscore the need for detection methods and evaluation protocols that account for RL optimization objectives and LRM-specific reasoning capabilities.

## Strengths
1. **Timely and important problem.** The paper addresses a critical and timely question — whether benchmark contamination detection methods remain effective for reasoning models that undergo RL-based training. Given the rapid adoption of LRMs and the increasing reliance on public leaderboards, this investigation is both scientifically relevant and practically significant.

2. **Well-structured experimental design.** The two-stage framework (pre-LRM and post-LRM contamination) provides a clear organizing principle that maps onto realistic training pipelines. The contamination simulation protocols are carefully defined, distinguishing between SFT contamination (exposure to question+response) and RL contamination (exposure to question+reward), which helps isolate the distinct roles of each training stage.

3. **Comprehensive detection evaluation.** Evaluating 10 detection methods spanning four categories (generation-based, perturbation-based, reference-based, reference-free) under identical conditions provides a thorough picture of detection fragility. The inclusion of both Qwen2.5-7B-Instruct and Llama-3.1-8B-Instruct as base models strengthens the generality of Stage I findings.

4. **Rigorous control for "forgetting" hypothesis.** The authors explicitly test and rule out the alternative explanation that additional training simply makes the model forget contaminated data. The experiment comparing GRPO on clean data, GRPO on clean+contaminated data, and continued SFT on clean data is well-designed and convincingly demonstrates that performance inflation persists while detection signals drop — a key piece of causal evidence.

5. **Theory-experiment integration.** The theoretical analysis (Theorem 3.1) provides a mechanistic explanation for the observed concealment, and the ablation study comparing RAFT, RAFT++, and GRPO (with/without clipping) directly tests the theoretical predictions. This integration of theory and controlled experiment is a methodological strength that elevates the paper beyond a purely empirical study.

## Weaknesses
### W1. Detection evaluation lacks statistical reliability measures (Major)
The primary quantitative evidence for contamination detection (Tables 2, 3, 5) reports AUROC values without confidence intervals, standard deviations, or multiple-split validation. The member/non-member split is a single random draw per dataset. When AUROC differences between conditions are modest (e.g., Verbatim 52.76%, Neighbor 50.71% — barely above random guessing at 50%), the reported values could easily fall within split variance. This is a methodological limitation that weakens confidence in the central claim that GRPO systematically reduces detectability. 

**Required action:** Report AUROC as mean ± std over at least 3 random member/non-member splits for a representative subset of benchmarks to calibrate expected variance. The appendix already contains extensive additional experiments; adding multi-split statistics would significantly strengthen the paper's quantitative claims.

### W2. Root-cause ablation for clipping uses only one detection method (Major)
The controlled ablation in Section 3.2.1 (Table 3) that attributes concealment to PPO-style clipping evaluates only the Loss detector (Carlini et al., 2021). The paper previously evaluated 10 detection methods and found that concealment affects all of them (Table 2). If the theoretical mechanism (covariance contraction via importance sampling/clipping) is general, it should manifest across multiple detection methods. The current evidence leaves open the possibility that the clipping effect is specific to loss-based detection rather than a general phenomenon.

**Required action:** Add ablation results for at least 2-3 additional detection methods (e.g., Min-K%, LiRA, CDD) under the same clipping/no-clipping conditions on a representative benchmark (e.g., AIME24 or GPQA). If computational cost is prohibitive, explicitly acknowledge this limitation and discuss whether the theoretical mechanism predicts uniform effects across detection paradigms.

### W3. Theoretical analysis relies on strong assumptions that bound generality (Moderate)
Theorem 3.1 is derived under a tabular setting with first-order natural gradient approximations, correct-trajectory conditioning (r=1), and small step size η. These assumptions are reasonable for an initial theoretical treatment, but they are not explicitly discussed as limitations. The generalization from tabular analysis to practical RL algorithms (7B-parameter models, continuous policy spaces, learned representations) is an extrapolation. The paper's claim that "a broad class of RL methods may inherently exhibit similar concealment capability" (Section 3.2.1) rests on this extrapolation.

**Required action:** Add a "Limitations of the Theoretical Analysis" paragraph in Section 3.2 that explicitly states the tabular assumption, the correct-trajectory restriction, and the small-step approximation. Qualify the generalization claim: "Under the tabular setting, our analysis predicts that PPO-style importance sampling/clipping is the root cause; the empirical results on 7B-scale models are consistent with this prediction."

### W4. Generalization explanation for Stage II is a hypothesis, not a verified mechanism (Moderate)
The Discussion in Stage II (Section 4) proposes that LRMs "internalize underlying knowledge and reasoning process" rather than memorize trajectories, enabling generalization to distributionally similar non-member questions. While this is a plausible explanation, the paper does not test it directly. The observed pattern (log-prob increases similarly for members and non-members) could also arise from simpler mechanisms: distribution overlap between members and non-members, or a global confidence increase on all inputs sharing superficial benchmark features.

**Required action:**
(1) Add a similarity analysis: compute per-question embedding similarity between members and non-members and test whether the log-prob increase on non-members correlates with similarity to members.
(2) Alternatively, add a cross-domain contamination control: contaminate on one domain (e.g., math) and test log-prob changes on another domain (e.g., coding) to distinguish generalization from global confidence increase.
(3) In the Discussion, explicitly label the explanation as a hypothesis: "Our results are consistent with the hypothesis that LRMs internalize reasoning patterns, but simpler explanations such as distribution overlap cannot be ruled out."

### W5. Conclusion recommendations are generic and unsupported (Minor)
Section 5 proposes two directions: (I) releasing intermediate checkpoints, and (II) advancing beyond memorization-driven detection. Neither recommendation is validated or made specific by the paper's evidence. The checkpoint suggestion is a governance measure that the paper did not test. The "beyond memorization" call lacks specificity about what new assumptions or features should replace current approaches.

**Required action:** Replace or augment these recommendations with evidence-grounded directions based on the paper's own findings. For example, specify that viable detection methods must operate on signals that persist through PPO-style optimization (gradient statistics rather than log-prob separability) or leverage features not shared between members and non-members under LRM generalization (reasoning pattern diversity rather than per-sample confidence).

### W6. Missing contribution enumeration in Introduction (Minor)
The Introduction announces the two-stage study but does not provide explicit, numbered contribution claims. The "first systematic study" claim is a meta-claim about scope rather than a concrete scientific finding. The actual novel findings — RL concealment via clipping, undetectability of CoT contamination — should be stated as explicit contributions to help readers and reviewers evaluate novelty.

**Required action:** Add a paragraph with 3 enumerated contributions after the two-stage description (see annotation Page 1 - Introduction for a concrete rewrite).

### W7. Related Work is organized as a list rather than comparison axes (Minor)
The Related Work section enumerates categories and representative papers without explaining how each family of methods would or would not work under LRM-specific conditions. For example, reference-based methods require access to training data distribution — is this realistic for closed-source LRMs? Adding such analysis would make the section more useful for positioning the paper's contribution.

### W8. "First" claim requires external verification (Deferred)
The paper claims "the first systematic study of benchmark contamination in LRMs" and "the first to investigate contamination concealment at the algorithmic level." These claims cannot be verified within this review due to Retrieval-Disabled Mode (external paper search unavailable in this run). The claims should be qualified with "to the best of our knowledge" and independently verified by the authors against the latest literature before publication.

### W9. Title clarity improvement opportunity (Minor)
The current title "On the Fragility of Benchmark Contamination Detection in Reasoning Models" accurately identifies the topic but does not convey the paper's specific finding (RL-based concealment via importance sampling/clipping). Consider a more informative subtitle: "... in Reasoning Models: RL Training Can Conceal SFT Contamination Signals through PPO-Style Clipping."

### W10. Page coverage note
The paper markdown provided to the reviewer contained only the main body (pages 1-9), with the rest (references and appendix) truncated as "Rest of paper (reference and Appendix) is removed." The appendix, which presumably contains implementation details and additional experimental results referenced throughout the paper, was not available for audit. This review therefore focuses on the main claims and evidence presented in the core sections.

## Score
**Final Score: 6.5/10**

**Rationale:** The paper tackles a timely and important problem with a well-structured experimental design and provides both empirical evidence and theoretical analysis for a non-trivial finding (PPO-style importance sampling/clipping conceals contamination). The control experiments ruling out the "forgetting" hypothesis are rigorous, and the integration of theory with controlled ablations (RAFT vs. RAFT++ vs. GRPO) is a methodological strength.

However, several weaknesses reduce confidence in the strength of the claims: (1) the detection evaluation lacks statistical reliability measures (confidence intervals, multi-split validation), (2) the root-cause ablation for clipping evaluates only one detection method, limiting generality, (3) the theoretical analysis relies on strong assumptions that are not explicitly bounded, (4) the Stage II generalization explanation remains a hypothesis without direct testing, and (5) the "first systematic study" and "first algorithmic-level investigation" claims require external literature verification. These weaknesses are fixable with additional experiments and more precise writing, and the core finding — that RL training can systematically evade current detection methods — is likely to hold. The paper represents a solid contribution that, with revisions addressing the statistical robustness, ablation breadth, and claim precision, could become a strong publication.