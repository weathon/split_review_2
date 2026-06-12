Now let me write the final consolidated review.

## Summary

This paper proposes OML, a brain-inspired hierarchical neural network for online multimodal learning with three key capabilities: (1) continual learning of new multimodal concepts without catastrophic forgetting, (2) precise reference extraction (identifying which visual features a word refers to using coefficient of variation across examples), and (3) conflict detection with human-in-the-loop interactive resolution. The architecture uses feature neurons, unimodal association neurons, and multimodal association neurons connected via ascending, descending, and lateral pathways.

## Strengths

- **Reference extraction via coefficient of variation (Section 3.4) is a well-motivated algorithmic idea.** The paper identifies a concrete problem — when a word like "red" refers to only a subset of an object's visual features (color but not shape), how does a learner determine which features are the referent? The solution of measuring the coefficient of variation across multiple examples to distinguish stable (referenced) dimensions from variable (non-referenced) ones is intuitive, simple, and connects to a real learning phenomenon. This is the paper's most original component.

- **The conflict detection and interactive resolution procedure (Section 3.5) is systematically designed.** The four cases (both channels recognize, only visual recognizes, only auditory recognizes, neither recognizes) exhaust the space of possible states, and the question-asking logic in each case follows coherently from the mismatch condition. This provides a principled framework for interactive continual learning.

## Weaknesses

### Major

- **The accuracy metric for cross-modal retrieval is never formally defined.** The paper reports accuracy percentages in Tables 1–3 but never specifies what counts as a correct retrieval: whether it is top-1 accuracy, a thresholded match between feature vectors, exact name matching, or some other criterion. This is a reproducibility gap that makes it difficult for other researchers to replicate or compare against the reported numbers. The issue is compounded in Tables 2 and 3, where the paper states that baselines receive credit for returning supersets of features (e.g., shape+color for a color word, or visual+taste for a taste word), while OML returns only the precise referent. Although this asymmetry favors the baselines (making OML's reported results conservative rather than inflated), the lack of a precise, uniformly applied metric definition undermines experimental rigor.

- **The human-in-the-loop interaction — listed as a core claimed attribute (Attribute 2 in Section 1) — is never evaluated with actual human subjects.** The experiments (line 240) state: *"if the question posed to the user by OLM remains unanswered for a certain period of time, we set the answer to be positive."* This means the interactive loop is effectively automatic in the evaluation. The paper provides no evidence that the generated questions are appropriate, that users would answer them correctly, or that the interaction improves learning outcomes. A paper that claims human-in-the-loop learning as a distinguishing capability should validate it with human participants or at minimum discuss why the automatic simulation is sufficient.

### Minor

- **No statistical analysis is reported.** All results in Tables 1–3 are single numbers with no confidence intervals, standard deviations, or indication of the number of independent runs or random seeds. Given that the close-environment evaluation involves random sampling and the open-environment evaluation depends on dataset partitioning, the reader cannot assess whether OML's margins over baselines are meaningful or within noise.

- **No ablation studies isolate the contribution of key components.** The reference extraction algorithm (Section 3.4) — the paper's most novel idea — is never evaluated in isolation. There are no results with and without it, nor with alternative feature-selection methods. The contributions of individual pathways (ascending vs. descending vs. lateral) are not studied. Key thresholds (θ set to a quarter of the weight norm, ϑ=0.8, r=0.5) are reported but never varied, leaving the reader unable to assess robustness to these choices.

- **Several mathematical components appear decorative or unmotivated.** In Eq. (1), the ascending activation sums over T time steps of a cosine signal even though T *"does not affect the algorithm"* (line 72) — if T has no effect, its presence in the activation function is unnecessary complexity. The Fourier transform in the MAN activation (Eq. 6) is applied to UAN outputs to extract amplitude and frequency for routing signals, but the paper provides no intuition for why the output of a visual UAN (which sums signals from feature neurons) would have a meaningful frequency-domain representation. This appears to be an indirect mechanism for what could be accomplished with a simpler routing table.

- **The paper does not analyze network growth or scalability.** The architecture creates new feature neurons, UANs, and MANs for each new concept or association, with no pruning or capacity management mechanism described. The paper does not report how many neurons were created in the experiments or discuss how the method would scale to realistic settings with thousands of categories and high-dimensional input features. Feature engineering is also hand-crafted (Fourier descriptors for shape, MFCCs for audio), and the paper does not address whether the method works with learned representations.

### Trivial

None.

## Nice-to-Haves

- An ablation of the reference extraction module (disabling it and treating all words as referring to all features) would directly isolate the contribution of Section 3.4, which is the paper's most novel component.
- A small-scale human study (5–10 participants) measuring whether the network's questions are interpreted correctly and whether human answers improve learning would substantially strengthen the human-in-the-loop claim.
- Sensitivity analysis of the three key thresholds (θ, ϑ, r) would demonstrate robustness.

## Removed Points

These points from the input review were flagged for removal; treat with caution:

- *Criticism about reference extraction failing for shape-referring words (e.g., "round"):* This is incorrect. Stable dimensions across examples would correctly identify shape for "round," just as they identify color for "red." The coefficient-of-variance approach works symmetrically.
- *Request for comparison with CLIP/BLIP-2:* These models are not designed for online learning and require large-scale pre-training and fine-tuning, which is outside the paper's stated scope of online learning from scratch.
- *Complaint about old baselines (DAE 2011, DBM 2014):* The paper also includes modern baselines from 2024–2025 (NRCH, FUME, ART, AEN), making the comparison set adequate.
- *Criticism about "OLM" typo:* Minor formatting artifact.
- *Claim that the evaluation metric makes results "uninterpretable":* Overstated; the results are interpretable as relative comparisons under an implicit metric, but the lack of formal definition is a legitimate reproducibility concern.
- *Missing related work, appendix content, and other parser-removed sections:* These exist in the original submission and are absent only due to parser limitations.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's insight about the counting-rule asymmetry (baselines receiving credit for superset returns) is worth noting but the review did not surface any novel cross-paper synthesis beyond this observation.

## Suggestions

1. **Define the evaluation metric precisely in the text.** State whether accuracy is top-1, threshold-based, or some other measure, and apply the same counting rule uniformly across all methods. If baselines receive credit for superset returns, this should be justified and the metric for OML should be clearly distinguished.
2. **Ablate the reference extraction mechanism.** Compare full OML against a version where all words are treated as referring to all features (equivalent to disabling Section 3.4). This directly validates the paper's most novel contribution.
3. **Report variance.** Run each experiment multiple times with different random seeds and report mean ± standard deviation.
4. **Add a discussion of network growth** (how many neurons were created per experiment) and scalability to larger, higher-dimensional datasets.

## Score and Decision

**Round 1 bracket:** 3.5–5.0 (based on calibration search).

**Anchor papers used for calibration:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| jYyste2HLP.md (FlyOrien) | 4.33 | R1 | Bio-inspired incremental learning model. Similar scope and evaluation rigor; OML has a more novel algorithmic component (reference extraction) but similar evaluation gaps. |
| 0CtIt485ew.md (Artsy) | 4.00 | R1 | Brain-inspired continual learning. Similar evaluation weaknesses (no variance, no ablations). OML is comparable in contribution novelty and evaluation rigor. |
| RyUvzda8GH.md (iPC) | 5.25 | R2 | Predictive coding algorithm with stronger experimental validation and theoretical grounding. OML has less rigorous evaluation. |
| gNoqEdT2wO.md (MCIL benchmark) | 2.33 | R1 | Benchmark paper with limited contribution. OML has stronger algorithmic novelty. |
| EwFJaXVePU.md (Scalable Lifelong) | 6.50 | R1 | Significantly stronger evaluation on larger-scale problems. OML is a step below in experimental rigor. |
| 7gUrYE50Rb.md (EQA-MX) | 8.00 | R1 | Large-scale embodied QA with comprehensive evaluation. Not directly comparable in scope. |

**Final score:** 4.0. The paper introduces a genuinely interesting reference extraction mechanism and a coherent interactive learning framework, which are novel contributions to online multimodal learning. However, the evaluation has structural gaps that prevent acceptance: the accuracy metric is never formally defined, the human-in-the-loop interaction (a core claimed attribute) is never tested with real users, and no ablations isolate the contribution of key components. These weaknesses are serious enough to require substantial revision before the paper can be accepted, but the core ideas have merit and could form the basis of a strong paper with a more rigorous evaluation.

<score>4.0</score>
<decision>Reject</decision>