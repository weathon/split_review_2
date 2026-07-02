## Summary
# Final Review Report

## Summary

This paper proposes a reinforcement learning (RL) framework for automated code refactoring that integrates contrastive pre-trained code graph embeddings. The core idea is to replace heuristic-based reward functions with learned representations obtained via a syntax-guided contrastive encoder. The framework has three main components: (1) a contrastive encoder that learns invariant representations of code graphs through structure-preserving augmentations, (2) a composite reward function fusing traditional code metrics with embedding dynamics and semantic preservation signals, and (3) a graph attention policy network operating on the joint representation space.

The authors evaluate on three refactoring datasets (Refactory, CodeRef, BigCloneBench) with baselines spanning rule-based, learning-based, RL-based, and hybrid methods. Results show that the proposed method outperforms all baselines across five metrics: Syntactic Improvement (83.7%), Semantic Preservation (93.8%), Edit Distance (0.36), Maintainability Gain (27.9%), and Generalization Score (72.4%). An ablation study confirms that contrastive pre-training provides the largest performance contribution.

**Core contribution claims (C1-C3):**
- **C1**: Syntax-guided contrastive encoder that learns structural invariant representations of code graphs using syntactic augmentations (subtree masking, edge rewiring, identifier shuffling).
- **C2**: Composite reward function combining learned embeddings with traditional code quality metrics and semantic preservation via differential testing.
- **C3**: Graph attention policy network that operates on joint representation space for refactoring action selection.

**Novelty note:** External literature verification is unavailable in this run (Retrieval-Disabled Mode). Novelty and comparison conclusions are explicitly deferred for manual verification. The assessment below is based solely on manuscript content analysis.

## Strengths
**S1 — Well-motivated integration of contrastive learning with RL for code refactoring.** The core research idea — using self-supervised contrastive pre-training to learn code representations that can serve as reward signals for RL-based refactoring — is timely and addresses a genuine bottleneck in the field. Heuristic-based reward functions are indeed a known limitation of existing RL approaches, and the proposed direction of learning representations from unlabeled code has practical merit.

**S2 — Comprehensive evaluation with multiple baselines and datasets.** The paper compares against 7 baselines spanning rule-based tools (PMD, Checkstyle), learning-based models (Code2Seq, Graph2Edit), RL methods (RLRefactor, GraphRL), and a hybrid approach (NeuroRefactor). Three refactoring datasets (Refactory, CodeRef, BigCloneBench) provide diversity in language (Java, Python), size (8,700–6M fragments), and task focus. The evaluation includes five complementary metrics that cover syntactic, semantic, maintainability, and generalization dimensions.

**S3 — Ablation study isolating component contributions.** The ablation study (Table 2) systematically removes four components (contrastive pre-training, embedding rewards, semantic tests, guided exploration) and quantifies the impact on SI, SP, and MG. This is a good practice that helps readers understand which design choices matter most. The finding that contrastive pre-training contributes the largest single gain (+7.5% SI) is an informative result that supports the core hypothesis.

**S4 — Cross-language generalization experiment.** Evaluating a Java-pretrained model on Python and C++ without fine-tuning demonstrates awareness of the practical need for language transfer. While the comparison baseline selection is debated in the Weaknesses section, the experimental design direction is valuable and provides preliminary evidence of transferability.

**S5 — Openness about LLM usage.** Section 8 transparently states that an LLM was used for polishing writing. This disclosure, while brief, aligns with emerging best practices for AI-assisted writing disclosure in academic publications.

## Weaknesses
### W1 — Missing statistical reliability and unequal comparison conditions (Major, Severity: High)

**Evidence:** Table 1 reports all metrics as point estimates without standard deviations, confidence intervals, or significance tests. The improvements over the strongest baseline (NeuroRefactor) are modest: SI +4.3%, SP +3.3%, ED -0.04, MG +3.3%, GS +5.2%. Without variance information, readers cannot assess whether these differences are statistically reliable or within noise range. Furthermore, the baseline training conditions are unequal: the proposed method uses CodeSearchNet (2M functions) for contrastive pre-training, while neural baselines (Code2Seq, Graph2Edit, GraphRL, NeuroRefactor) are not reported to have accessed comparable pre-training data. This confound means observed gains may partly reflect the larger pre-training corpus rather than the specific contrastive encoder design. The ablation study (Table 2) partially addresses this, but the main comparison table remains unfair.

**Impact:** Undermines the primary claim of <i>state-of-the-art</i> performance. Without statistical evidence and matched training conditions, the ranking in Table 1 is not scientifically robust.

**Required Action (Must):** (a) Report mean ± std over ≥3 random seeds for all methods. (b) Apply the same pre-training data to neural baselines, or alternatively train the proposed method without pre-training for a controlled comparison. (c) Add paired significance tests (bootstrap or Wilcoxon) against the strongest baseline.

---

### W2 — Formula errors in the GAT policy (Major, Severity: High)

**Evidence:** Equation (7) defines attention weights as $\omega_{ij} = \text{softmax}_j(\text{LeakyReLU}(\mathbf{a}^\top[\mathbf{W}_h \|\mathbf{W}_q] \mathbf{h}_j))$. This formulation has a critical indexing error: standard GAT attention requires both source and target node features ($\mathbf{h}_i$ and $\mathbf{h}_j$) to compute pairwise attention, but this equation only uses $\mathbf{h}_j$. As a result, the attention weight for edge $i \leftarrow j$ is independent of the target node $i$, which means every node would aggregate neighbor information with the same attention distribution — defeating the purpose of graph attention. Additionally, the joint representation $[\mathbf{h}_t; \mathbf{q}_t]$ concatenates a graph embedding with a metric vector, but $\mathbf{h}_j$ in the equation appears to be a single node embedding, creating a dimensionality mismatch.

**Impact:** If implemented as written, the policy network would not perform meaningful graph attention, likely degrading RL training quality. This is a correctness issue that could affect the reproducibility of the reported results.

**Required Action (Must):** Correct Eq. (7) to the standard GAT form: $\omega_{ij} = \text{softmax}_j(\text{LeakyReLU}(\mathbf{a}^\top[\mathbf{W}\mathbf{h}_i \| \mathbf{W}\mathbf{h}_j]))$, ensuring both node indices appear in the argument. Clarify how node-level embeddings and the joint state representation $[\mathbf{h}_t; \mathbf{q}_t]$ are reconciled.

---

### W3 — Contrastive loss formula inconsistency (Major, Severity: Medium)

**Evidence:** Equation (4) defines the pre-training loss with $\sum_{G' \in \mathcal{B}}$ in the denominator, where $\mathcal{B}$ is described as "the batch of negative examples." This diverges from standard InfoNCE (Eq. 2), where the denominator sums over all examples in the batch including the positive pair. If $\mathcal{B}$ truly contains only negatives, the positive pair is excluded from the denominator, which breaks the normalization and can cause the loss to be trivially minimized by pushing all negatives apart without pulling positives together. The similarity function $\text{sim}$ is also not explicitly defined as cosine similarity (unlike in Eq. 2), introducing ambiguity.

**Impact:** The pre-training objective may not behave as intended, potentially reducing the quality of learned code representations and downstream RL performance.

**Required Action (Must):** Clarify whether $\mathcal{B}$ includes the positive pair. If not, revise the denominator to include positives. Explicitly define $\text{sim}$ as cosine similarity for consistency with standard practice.

---

### W4 — Cross-language comparison against mismatched baselines (Major, Severity: Medium)

**Evidence:** Table 3 compares the proposed method against PyLint (Python) and Cppcheck (C++), which are rule-based linters, not learning-based refactoring systems. PyLint detects style violations but does not perform structural code transformations. The comparison is fundamentally misaligned: a refactoring system that can reorganize code will naturally achieve higher SI than a linter that only reports issues. The neural baselines used in Table 1 (GraphRL, NeuroRefactor) are not evaluated in the cross-language setting, so the claim of "outperforming language-specific rule-based tools" is weak. Furthermore, the SP of the proposed method (88.9% Python, 91.2% C++) is actually lower than the rule-based tools (90.4%, 93.1%), which receives no discussion.

**Impact:** The cross-language generalization claim is overstated. The experiment does not support the conclusion that the method transfers well to new languages, because a meaningful comparison would require neural refactoring baselines retrained on those languages.

**Required Action (Must):** (a) Add neural refactoring baselines (at minimum GraphRL) retrained on Python and C++ data. (b) Discuss the SP gap honestly. (c) Alternatively, reframe the experiment as a preliminary transferability analysis and add a clear caveat.

---

### W5 — Hedging, hype, and grammatical errors throughout the manuscript (Major, Severity: Medium)

**Evidence:** Multiple paragraphs contain defective English that obscures meaning: Abstract ("do last year"), Introduction ("objecting to code quality," "variable-contrastive learning"), Related Work ("Recent lemon deep learning," "The movement of using reinforcement learning on code refactoring has been a study of note"). Hype language appears in key claims: "our approach is excellent," "enormous improvement," "particularly promising." These issues are not minor typos — they affect the paper's readability and scientific credibility. The "variable-contrastive" term in the Introduction is never defined and does not appear in the Method section (where "syntax-guided contrastive encoder" is used instead), creating a terminology inconsistency.

**Impact:** Reviewers may interpret language quality issues as a lack of care in the research itself. The hype language reduces trust in the objectivity of the claims. The term inconsistency can confuse readers about the core technical contribution.

**Required Action (Must):** (a) Thorough proofreading pass over the entire manuscript. (b) Replace "excellent" and "enormous" with specific, quantified statements. (c) Align "variable-contrastive" with the consistent terminology used in Section 4.

---

### W6 — Limitation discussion is too brief and generic (Minor, Severity: Low)

**Evidence:** Section 6.1 mentions only one limitation (pre-training cost) in vague terms ("rather obvious limitations," "especially when dealing with large codebases"). No quantitative cost is reported (GPU hours, memory). Other critical limitations are omitted: (1) the action space — what refactoring types are supported? (2) symbolic execution limitations for semantic preservation checking (external libraries, non-determinism); (3) language coverage gaps (dynamically-typed languages not tested). The limitation section does not help readers understand when the method would fail.

**Impact:** Weakens the paper's scientific framing. A good limitation discussion increases, not decreases, reviewer confidence.

**Required Action (Nice-to-have):** Add quantified pre-training cost (e.g., "72 GPU hours on 8×V100 GPUs"), specify the supported refactoring action set, discuss symbolic execution failure modes, and explicitly state untested language categories.

---

### W7 — Conclusion contains unsupported causal claims (Major, Severity: Medium)

**Evidence:** The Conclusion states "The embedding-guided exploration strategy is especially important in the learning of an efficient policy" as a definitive causal finding. However, the ablation study removes "Random exploration" (which replaces the full exploration strategy, not just the Mahalanobis guidance), and this variant drops SI from 83.7 to 74.8. This ablation conflates multiple differences: removing embedding-guided exploration likely also changes the exploration noise schedule, initialization, and decay. A clean ablation would replace only the Mahalanobis distance term in Eq. (6) with uniform exploration while keeping all other components fixed.

**Impact:** The paper attributes importance to a component without clean causal evidence, which may mislead readers about which design choices are critical.

**Required Action (Must):** (a) Add a targeted ablation that replaces only the Mahalanobis-guided exploration distribution in Eq. (6) with a uniform distribution over actions, keeping all other components identical. (b) Tone down the causal language to "is consistent with" or "suggests."

---

### W8 — Reproducibility gaps in method description (Minor, Severity: Low)

**Evidence:** Several critical implementation details are missing: (a) The code graph construction pipeline (how AST nodes and edges are converted to the graph $G = (V,E)$) is not described. (b) The action space (which refactoring operations are available to the RL agent) is never enumerated. (c) The symbolic execution test case generation (Section 4.5) is cited to Cadar & Sen (2013), but the specific implementation (concolic vs. pure symbolic, path explosion handling, timeout) is unspecified. (d) The PPO training details (clip range, value function architecture, advantage normalization) are partially listed in Implementation Details but key hyperparameters are missing.

**Impact:** Without these details, independent reproduction is difficult or impossible, reducing the paper's long-term research value.

**Required Action (Nice-to-have):** Add a reproducibility appendix describing: (1) graph construction from source code, (2) complete action space with pre-/post-conditions, (3) symbolic execution configuration, (4) complete PPO hyperparameter table.

---

### W9 — Figure 2 correlation analysis is weak (Minor, Severity: Low)

**Evidence:** Figure 2 reports Pearson's $r = 0.72$ between embedding dynamics $\Delta h$ and syntactic improvement SI, claiming this "validates that the learned representations capture meaningful refactoring signals." However, $\Delta h$ is computed from the same encoder that is trained via a contrastive objective to encode structural differences — the correlation may be partially an artifact of the training objective rather than evidence that the embeddings causally guide good refactoring. No partial correlation or causal analysis is performed. The scatter plot shows points in the upper-right quadrant, but a single Pearson $r$ without confidence intervals or $p$-value is insufficient to validate representation quality.

**Impact:** The claim is over-interpreted from correlational evidence.

**Required Action (Nice-to-have):** Report confidence interval for $r$, add a baseline correlation (e.g., between random embeddings and SI), and consider a partial correlation controlling for code size or complexity.

---

### W10 — "THE USE OF LLM" section is insufficient (Minor, Severity: Low)

**Evidence:** Section 8 states "We use LLM polish writing based on our original paper" with no further details. Given the pervasive grammatical issues (W5), it is unclear whether the LLM was used before or after the current draft. Best practices for AI disclosure (e.g., NeurIPS guidelines) recommend specifying which sections were AI-generated, which model was used, and how the output was verified.

**Required Action (Nice-to-have):** Expand Section 8 to specify: (a) model used, (b) scope of AI assistance (whole paper vs. selected sections), (c) human verification process, (d) whether any technical content (equations, results) was AI-generated.

---

### W11 — OpenNovelty: Deferred manual verification

**Note:** Because this run operates in Retrieval-Disabled Mode (external paper search not available), all novelty and comparative positioning judgments are deferred. The claims C1–C3 (contrastive encoder, composite reward, GAT policy) each require systematic literature comparison against existing code representation learning methods (e.g., GraphCodeBERT, SyncoBERT) and RL-based refactoring systems (e.g., GraphRL, NeuroRefactor). The manuscript's own related work section suggests familiarity with these baselines, but independent verification of (a) whether the contrastive augmentation set is novel, (b) whether the composite reward design has prior art, and (c) whether the GAT policy on joint representations differs substantially from GraphRL's policy, cannot be completed without external retrieval. These novelty verdicts are explicitly marked as *deferred* and must be verified manually by the authors or a subsequent review round.

## Score
**Final Score: 5/10**

**Scoring rationale:** This score reflects the paper's strengths in research motivation, experimental breadth, and ablation methodology, weighed against the major weaknesses identified above. The paper proposes a well-motivated integration of contrastive learning with RL for code refactoring and provides a multi-dataset, multi-metric evaluation with ablation studies — these are genuine strengths. However, the score is constrained by the following factors:

1. **Validity concerns (W1–W4):** The main comparative results lack statistical evidence (no variance, no significance tests), and the experimental setup has confounding factors (unequal pre-training data, mismatched cross-language baselines). Formula errors in the core policy network (W2) and contrastive loss (W3) raise reproducibility questions.

2. **Writing quality (W5):** Pervasive grammatical errors, hype language, and terminology inconsistencies reduce the paper's scientific professionalism and readability. This is not merely a stylistic issue — it affects the clarity of the contribution claims.

3. **Missing causal evidence (W7):** A central conclusion about the exploration strategy's importance is not supported by clean ablation evidence.

4. **Novelty unverified:** Novelty and comparative positioning cannot be independently assessed in this run (Retrieval-Disabled Mode). The claims C1–C3 require external literature verification before a final novelty determination can be made.

5. **Fixability assessment:** The major issues are fixable with moderate effort: adding variance reporting, correcting equations, expanding limitations, and proofreading. The cross-language comparison (W4) requires additional experiments. The formula errors (W2, W3) are simple corrections. The statistical gaps (W1) require re-running experiments, which is more costly but standard for a revision.

The paper has a solid conceptual core and the experimental methodology is on the right track, but the current execution has several issues that prevent the results from being fully reliable. With careful revision addressing W1, W2, W3, W5, and W7, the paper could become a solid contribution.