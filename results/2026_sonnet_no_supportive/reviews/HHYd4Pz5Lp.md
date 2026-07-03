Now I have enough information to draft the review.## Summary
DelRec introduces the first SGL-based method to train axonal or synaptic delays in **recurrent** spiking neural network (RSNN) connections. Using a differentiable triangle-interpolation kernel with annealing spread parameter σ and a scheduling-matrix buffer, the method enables per-neuron recurrent delay learning via backpropagation. The paper achieves SOTA on SSC (82.58±0.08% with 0.37M parameters, vanilla LIF neurons) and PS-MNIST (96.21%), and includes a multi-configuration functional ablation study on SHD examining the comparative roles of delay type, granularity, and network size.

## Strengths
- **Technically sound implementation**: The scheduling-matrix approach (Eq. 8–13) and pointer-buffer mechanism cleanly handle non-integer recurrent delays with well-defined gradients. The progressive σ-annealing (Fig. 2C) makes training dynamics interpretable and ensures smooth convergence from coarse to fine delay localization. The generalization from feedforward (DCLS) to the recurrent setting — requiring the future-oriented scheduling matrix rather than simple convolution — is a non-trivial engineering step.
- **Genuine SOTA with minimal architectural complexity**: DelRec (only Rec. delays) achieves 82.58±0.08% on SSC with 0.37M parameters using vanilla LIF neurons, surpassing all LIF-based and non-LIF RSNN models in Table 1, including SE-adLIF (80.44%), DCLS (80.69%), and SiLIF (82.03%). Achieving this with LIF rather than adaptive or resonant neurons sharpens the paper's core claim that recurrent delays, not neuron complexity, are the bottleneck.
- **Informative ablation study**: Section 3.2 compares six model configurations (vanilla SNN/RSNN, fixed random recurrent delays, learned feedforward, learned recurrent, combined) across parameter budgets and firing rates, providing genuine mechanistic evidence. The finding that *fixed random* recurrent delays already improve over vanilla RSNN (Fig. 3B) — suggesting gradient amelioration via temporal skip-connections is part of the benefit, independent of learning — is an interesting secondary result reported honestly.
- **Honest reporting of energy–accuracy tradeoff**: Section 3.2 explicitly reports that feedforward delays reach comparable accuracy with a lower firing rate than recurrent delays, providing actionable guidance for practitioners who prioritize energy efficiency over peak performance.
- **Sound benchmark methodology**: The authors correctly exclude SHD from Table 1 and relegate it to a validation/analysis role, citing statistical saturation — a methodological choice that improves credibility.

## Weaknesses

### Fatal
None.

### Major
- **Insufficient positioning against Xu et al. (ASRC-SNN)**: The abstract and introduction claim DelRec is "the first SGL-based method to train axonal or synaptic delays in recurrent spiking layers," but Xu et al. (ASRC-SNN) already learns recurrent delays via backpropagation. The real distinction — DelRec learns per-neuron (axonal) delays while Xu et al. learns a single global delay per layer using a softmax/temperature schedule — is real and non-trivial, but the paper articulates it only in passing. Section 1 describes Xu et al.'s method in a single sentence, without venue, year, or technical elaboration. Since ASRC-SNN is the model DelRec most directly supersedes and is also the closest competitor on both SSC and PS-MNIST (with reproduced results), the paper needs a more complete description of the contribution boundary: specifically, what makes per-neuron recurrent delays technically harder than global per-layer recurrent delays, and what the scheduling matrix achieves that Xu et al.'s softmax approach cannot.

### Minor
- **Unexplained inversion: combined delays underperform recurrent-only on SSC**: Table 1 shows DelRec (Rec. and Ff. delays) at 82.19±0.16% vs. DelRec (only Rec. delays) at 82.58±0.08% — adding feedforward delays *hurts* on SSC — while Table 2 shows the combined model higher on SHD (93.73% vs. 93.39%). The paper notes in Section 3.2 that "we found no advantage in using both types of delays in these small configurations" (referring to small SHD ablation models), but this does not explain the SSC reversal at full scale. The conclusion acknowledges the combination needs further study, but offers no hypothesis. Since "Rec. and Ff. delays" is one of the two headline configurations reported in the primary results table, this inversion deserves at least a mechanistic hypothesis (e.g., optimization interference, task-specific temporal structure, regularization effects from different parameter counts).
- **PS-MNIST single-seed improvement**: The paper explicitly notes single-seed evaluation follows prior practice, but the improvement over ASRC-SNN (96.21% vs 95.77%) is only 0.44% — small enough that a single-seed result cannot establish significance. A note contextualizing expected variance from prior work would strengthen the evidential value.

### Trivial
None.

## Nice-to-Haves
- An experiment using *axonal* feedforward delays (one per presynaptic neuron) alongside the current *synaptic* feedforward delays (DCLS) would disentangle the contribution of recurrence from the contribution of delay granularity — the ablation in Section 3.2 currently conflates both. The paper notes this asymmetry in one sentence but does not address it experimentally.
- A brief discussion of practical tradeoffs between axonal and synaptic delays would help practitioners, since the paper states compatibility with synaptic delays but uses axonal delays throughout.
- Providing multi-seed PS-MNIST results, even briefly, would elevate the evidential strength of that SOTA claim.

## Removed Points
*These points are flagged as removed; treat them with caution.*
- **Missing reference details for Xu et al.**: The harsh critic flags the absence of a year/venue/DOI for "Xu et al." in the extracted text. This is a parser artifact — the reference list is stripped from all papers in the extraction pipeline; the original submission contains it. Removed per the hard rule.
- **Table 2 ranking implies meaningful ordering where confidence intervals overlap**: Accurate observation, but trivial presentation concern; the paper's own text (Section 3.2) explicitly warns that differences above ~93% are likely not statistically meaningful. The authors already address this adequately. Removed as a strawman weakness.
- **Fig. 3B: "relatively small, yet consistent and significant" understates the figure**: A minor precision nitpick; the statement is defensible given that the comparison was made on a small, saturated dataset. Removed as trivial.

## Novel Insights
The most consequential secondary finding — largely unremarked upon by the authors — is that *fixed random* recurrent delays already substantially outperform a vanilla RSNN in the ablation (Fig. 3B), while learned recurrent delays provide only an additional increment. This implies that delay *diversity* itself, not optimization, is the dominant mechanism behind much of the benefit: recurrent delays function primarily as temporal skip-connections that ameliorate gradient pathologies, and their learned values provide only marginal gains on top of this structural effect. This has practical implications: even a simple random-delay RSNN without any delay-learning machinery can capture a large fraction of the benefit, suggesting that the implementation barrier for delay-enhanced RSNNs is lower than the full DelRec method implies.

## Suggestions
- Add a paragraph (perhaps in the Introduction or Section 2.2) explicitly comparing DelRec's technical contribution to Xu et al.'s: the per-neuron vs. per-layer distinction, why the scheduling matrix is needed (Xu et al.'s softmax approach does not generalize to heterogeneous per-neuron delays), and what performance gap the additional expressivity unlocks.
- Provide a hypothesis or brief empirical analysis explaining why Rec.+Ff. delays underperform Rec.-only on SSC — even framing it as an open question with a proposed mechanism would strengthen the paper.
- For PS-MNIST, include at minimum an estimate of expected variance (e.g., from bootstrapping or comparison with Xu et al.'s reported variance) to contextualize the 0.44% improvement.

---

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| pIJR9uPjy3 (DeNN, delay neural networks for event datasets) | 4.50 | 1 | Closest topical match; rejected. Less technically rigorous than DelRec, no SOTA claim as strong, narrower scope. |
| ROxsH4rMe4 (Systolic array acceleration for SNNs) | 4.20 | 1 | Hardware-focused SNN work; rejected. Systems contribution without algorithmic novelty comparable to DelRec. |
| 4ILqqOJFkS (SPikE-SSM, sparse spiking state-space model) | 3.67 | 1 | Rejected. Weaker experimental results and narrower ablation than DelRec. |
| Nz2UApmv2e (Spiking hybrid attention for sound) | 5.00 | 1 | Rejected borderline. More complex setup, no SOTA on standard benchmarks. |
| drPDukdY3t (DeepTAGE, gradient enhancement for SNNs) | 6.25 | 1 | Accepted. Gradient-enhancement method for SNNs with multi-benchmark SOTA — comparable scope and ambition to DelRec. |
| rDe9yQQYKt (TS-LIF, temporal segment LIF) | 6.00 | 1 | Accepted. Novel LIF variant with SOTA on time-series; single-dataset focus vs. DelRec's two datasets + ablation. |
| eN4g4cjFX1 (Spatio-temporal dependency-aware neuron) | 5.75 | 1 | Borderline reject. Improvement method for SNNs but narrower ablation and weaker SOTA margin than DelRec. |
| 6iM7mmVhXh (Asynchronous SNNs) | 5.75 | 1 | Borderline reject. Interesting analysis paper but no SOTA improvement. |
| GRMfXcAAFh (LinOSS) | 8.00 | 1 | Accepted. Strong SSM paper with theoretical guarantees; higher bar than DelRec's contribution. |

**Round 1 bracket**: The most directly comparable accepted paper is DeepTAGE (6.25) — a novel SNN training method achieving SOTA on temporal benchmarks with an ablation study. DelRec's SOTA improvements on SSC are larger and more robust (3 seeds vs. single seed for DeepTAGE), and the functional ablation in Section 3.2 is more informative. The positioning weakness against Xu et al. is the primary drag but is a Major (not Fatal) flaw fixable in revision. The rejected DeNN paper (4.5) is clearly weaker — less technical rigor, no multi-benchmark SOTA. **Bracket: 6.0–7.0.**

**Round 2 (narrowing)**: Within the 6–7 range, DelRec sits closer to 6.5. It exceeds the DeepTAGE threshold (6.25) on experimental strength and novelty, but falls short of an 8 because (a) the Xu et al. positioning gap means the novelty boundary is not crisply established, (b) one of two headline results (SSC combined) underperforms the simpler variant without explanation, and (c) the PS-MNIST improvement is single-seed and small. These collectively prevent a confident 7 or higher.

**Final score: 6.5**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>