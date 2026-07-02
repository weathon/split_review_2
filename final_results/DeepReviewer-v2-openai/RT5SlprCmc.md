## Summary
This paper proposes a framework for learning the Minimum Action Distance (MAD)—the minimum number of actions required to transition between two states in an MDP—from state-only trajectory data. The authors introduce two algorithms: MadDist (direct distance regression with a scale-invariant loss) and TDMadDist (temporal-difference bootstrapping variant). Both use quasimetric (asymmetric) distance functions to capture directional structure in environments with irreversible dynamics, a limitation of prior symmetric approaches. A simple, computationally efficient quasimetric $d_{\text{simple}}$ is also introduced. Evaluation on a curated suite of environments with known ground-truth MAD—covering deterministic/stochastic dynamics and discrete/continuous state spaces—shows that MadDist achieves higher Pearson/Spearman correlations and lower coefficient-of-variation ratios compared to two baselines (QRL and a Hilbert-space embedding). MadDist also achieves near-perfect success rates in a downstream planning task across OGBench PointMaze environments.

**Core contributions (author-claimed):**
- C1: Two novel algorithms (MadDist, TDMadDist) for learning MAD from state-only trajectories, supporting both symmetric and asymmetric distances.
- C2: A novel simpler quasimetric distance function ($d_{\text{simple}}$) that is computationally efficient.
- C3: A diverse benchmark suite with known ground-truth MAD for systematic evaluation.

**Key assessment:** The paper presents a well-motivated problem and technically sound algorithmic contributions. However, the empirical evaluation is limited to only two baselines, which does not justify the broad "outperforms existing methods" claim. A corrupted equation (Eq. 9) in TDMadDist and a seed-count inconsistency (3 vs. 5) between text and figures reduce confidence in reproducibility. Architecture and hyperparameter details are deferred to the appendix. Novelty claims relative to prior MAD approximation methods cannot be fully verified without external literature access (Retrieval-Disabled Mode). The paper would benefit from broader baseline comparison, corrected equation formatting, transparent limitation discussion, and additional implementation details.

## Strengths
1. **Well-motivated problem.** Learning the Minimum Action Distance from state-only trajectories addresses a practical need in goal-conditioned RL and reward shaping. The paper clearly explains why MAD is useful and why existing symmetric approximations are inadequate for irreversible dynamics.

2. **Sound problem formulation.** The constrained optimization view of MAD (Eq. 1) provides a clean theoretical foundation, connecting MAD to all-pairs shortest paths and the Floyd-Warshall algorithm. The derivation of trajectory-index-difference as an upper bound on MAD is clearly reasoned.

3. **Scale-invariant loss design.** The main objective $\mathcal{L}_o$ (Eq. 5) normalizes by trajectory index distance $(j-i)$, which prevents long-range pairs from dominating the loss. This is a thoughtful improvement over the unnormalized prior work (Steccanella & Jonsson, 2022).

4. **Support for asymmetric distances.** The framework's ability to accommodate both symmetric and quasimetric distance functions within the same training pipeline is a genuine advance over prior work that is restricted to symmetric Euclidean embeddings.

5. **Controlled evaluation suite.** The environments (NoisyGridWorld, KeyDoorGridWorld, CliffWalking, PointMaze, OGBench PointMaze) are carefully chosen to span key MDP characteristics: deterministic/stochastic, discrete/continuous, symmetric/asymmetric, low-dimensional/noisy observations. The use of known ground-truth MAD enables precise quantitative comparison.

6. **Downstream validation.** The planning experiment (Table 1) provides evidence that learned MAD representations transfer to a concrete task, with MadDist achieving near-perfect success rates. This strengthens the case for practical utility beyond correlation metrics.

7. **Clear writing structure.** The paper is generally well-organized, with separate sections for background, MAD definition, asymmetric metrics, algorithms, and experiments. The notation is mostly consistent and the derivations are logically presented.

## Weaknesses
### W1. Insufficient baseline comparison (Major)
**Evidence:** Page 7 - Baselines paragraph, lines 216-217. Only two methods are compared: QRL (Wang et al., 2023b) and a Hilbert-space embedding (Park et al., 2024b). The Related Work section (lines 72-80) discusses several additional families—constrained optimization (Steccanella & Jonsson, 2022), Laplacian-based methods (Wu et al., 2019), successor features (Myers et al., 2024), bisimulation metrics (Dadashi et al., 2021)—but none are included in the experiments.
**Impact:** The abstract and conclusion claim to "significantly outperform existing state representation methods," but this is only validated against two baselines. The reader cannot judge whether MadDist is genuinely superior to the broader set of approaches discussed in the paper. This is an evidence-sufficiency gap that weakens the core claims.
**Repair path (Must):** Add at least one additional baseline from a different family (e.g., the constrained-optimization approach of Steccanella & Jonsson, 2022, or a Laplacian embedding). Alternatively, narrow the claim to "outperforms two representative baselines—QRL (asymmetric) and Hilbert-space (symmetric)—on the evaluated environments."

### W2. Corrupted equation in TDMadDist (Major)
**Evidence:** Page 5 - Section 6.2, line 144, Equation (9). The equation reads: $\mathcal{L}'_r = \mathbb{E}[ (d_\theta(s_i, s_{i+1} + d_{\theta'}(s_{i+1}, s_r) - 12(9)))^2 ]$. This contains what appears to be a rendering artifact ("12(9)"), mismatched parentheses, and an unclear target structure.
**Impact:** Reproducibility of TDMadDist is compromised. The verbal description suggests the target should be $1 + d_{\theta'}(s_{i+1}, s_r)$, but the equation as shown is mathematically nonsensical. This is a correctness-critical defect.
**Repair path (Must):** Replace with a correctly parenthesized equation, e.g.:
$$\mathcal{L}'_r = \mathbb{E}_{\tau \sim \mathcal{D}, (s_i, s_j) \sim \tau, s_r \sim \mathcal{S}_D} \left[ \left( d_\theta(s_i, s_r) - \big(1 + d_{\theta'}(s_{i+1}, s_r)\big) \right)^2 \right]$$

### W3. Seed-count inconsistency (Major)
**Evidence:** Page 7 - Empirical Setup paragraph, line 226 states "means over five independent runs (random seeds)." Page 8 - Figure 3 caption, line 236 states "Shaded regions indicate minimum and maximum values across three random seeds."
**Impact:** Direct factual contradiction. If Figure 3 shows only 3 of 5 seeds, the selection rationale is unclear. If the true protocol is 3 seeds, the "5 seeds" claim is overstated. This reduces confidence in the reported statistics.
**Repair path (Must):** Unify the seed count. If 5 seeds were used, regenerate Figure 3 to show all 5 and add an explanation. If Figure 3 is a 3-seed subset, clarify the selection criteria and report full 5-seed results in the appendix with a reference in the caption.

### W4. Missing implementation details (Major)
**Evidence:** Page 4-5 - Section 6, lines 123-147. The method section defines loss functions but omits: neural network architecture (depth, width, activations), embedding dimension $d$, optimizer and learning rate, batch size, values of hyperparameters $d_{\max}$, $H_c$, $w_r$, $w_c$, $\beta$, and gradient clipping threshold. These are deferred to Appendix D (not provided in the reviewed manuscript).
**Impact:** The experiments cannot be reproduced from the main text. Reproducibility is a core scientific requirement.
**Repair path (Must):** Add an "Implementation Details" paragraph in the main experiments section stating architecture, optimizer, and key hyperparameter values used in all main experiments. Keep extended details in the appendix.

### W5. TDMadDist underperformance unexplained (Minor)
**Evidence:** Page 7 - Discussion paragraph, line 229. The text states "TDMadDist underperforms the MadDist and QRL algorithm" but provides no analysis of why this occurs.
**Impact:** Readers cannot assess whether the underperformance is inherent to TD learning for this problem or due to suboptimal hyperparameters. The contribution of TDMadDist as a "novel algorithm" is weakened.
**Repair path (Nice-to-have):** Add a brief analysis of TDMadDist's failure mode. Hypotheses to explore: (a) early-training bootstrap error propagation, (b) sensitivity to target EMA rate $\beta$, (c) instability from the $\min(\cdot)$ selection in the denominator. Report an ablation on $\beta$ if available.

### W6. Missing limitation discussion (Minor)
**Evidence:** Page 9 - Conclusion, lines 250-252. The conclusion discusses future work but does not explicitly list limitations of the proposed approach.
**Impact:** The paper lacks scientific self-critique. A limitations paragraph is standard for responsible scholarship.
**Repair path (Nice-to-have):** Add a limitations paragraph covering: (a) dependence on behavior policy coverage quality, (b) limited baseline comparison, (c) applicability primarily validated on low-dimensional state spaces.

### W7. Introduction narrative could be sharper (Minor)
**Evidence:** Page 0 - Introduction, lines 8-11. The first two paragraphs are generic RL motivation before reaching MAD. The contribution paragraph (paragraph 4) is split across a page break.
**Impact:** The reader must wait until paragraph 3 before encountering the specific problem. A more direct opening would improve narrative engagement.
**Repair path (Nice-to-have):** Merge paragraphs 1-2 into a compact opener that states (1) the need for state similarity in RL, (2) the gap in existing metric learning, and (3) the paper's solution—within the first paragraph.

---
### Ranked Error Board (Top-5 core defects)

| Rank | Defect | Severity | Validity Risk | Fixability | Confidence |
|------|--------|----------|---------------|------------|------------|
| 1 | W2: Corrupted Eq. (9) | Major | High | Easy | High |
| 2 | W1: Insufficient baselines | Major | High | Medium | High |
| 3 | W3: Seed inconsistency | Major | Medium | Easy | High |
| 4 | W4: Missing implementation details | Major | Medium | Easy | High |
| 5 | W5: TDMadDist underperformance unexplained | Minor | Low | Medium | Medium |

---
### Novelty & Retrieval Note
External literature search was not available in this run (Retrieval-Disabled Mode). Therefore:
- Novelty verdicts for C1-C3 cannot be fully verified against external prior work.
- The paper's claims about "first systematic evaluation" and "outperforms existing methods" require manual literature verification.
- The baseline comparison discussion is grounded solely in the manuscript's own discussed references.

---
### Page Coverage Audit

| Page | Annotation Count | Coverage Status | Skip Reason |
|------|-----------------|-----------------|-------------|
| 1 (Abstract + Intro + Related Work + MAD + Methods + Experiments + Conclusion) | 12 all on page 1 | Covered | Single-page text file; all substantive paragraphs covered. |

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses a well-motivated problem—learning the Minimum Action Distance from state-only trajectories—with a technically sound algorithmic framework (MadDist). The scale-invariant loss and support for asymmetric quasimetrics are genuine improvements over prior symmetric approaches. The controlled evaluation suite with known ground-truth MAD is a positive contribution. However, the empirical validation is significantly limited by comparing against only two baselines, which does not support the broad "outperforms existing methods" claim. A corrupted equation (Eq. 9) undermines reproducibility of TDMadDist, and a seed-count inconsistency (3 vs. 5) between the text and Figure 3 caption reduces statistical confidence. Key implementation details are deferred to an inaccessible appendix. Novelty claims cannot be fully assessed without external literature access (Retrieval-Disabled Mode). With the major issues resolved—particularly broader baseline comparison, corrected equation, and consistent seed reporting—the paper could reach 7-8/10. The core methodological ideas are sound and the research direction is valuable; the primary gap is in the strength of the empirical evidence relative to the claims made.