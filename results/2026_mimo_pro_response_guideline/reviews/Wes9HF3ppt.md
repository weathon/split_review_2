## Summary
This paper introduces Insertion Language Models (ILMs), a generative paradigm that generates sequences by iteratively inserting tokens at arbitrary positions, jointly predicting both the insertion position and the vocabulary token. ILMs are motivated by limitations of autoregressive models (rigid left-to-right order) and masked diffusion models (fixed-length masks, simultaneous unmasking incoherence). The paper demonstrates strong advantages on planning tasks (star graphs: 99.1% vs. 23%/21% for ARM/MDM; zebra puzzles: 90% vs. 81.2%/82.6%) and competitive text generation/infilling on LM1B and TinyStories.

## Strengths
- **Dramatically strong planning task results (Table 1, Section 5.1):** On Star_hard, ILM achieves 99.1% accuracy vs. 23% ARM and 21% MDM. The mechanistic explanation—ILM uses relative positions and iterative insertion while MDM relies on absolute positions that fail with variable arm lengths—is convincing and well-supported. The Insertion Transformer baseline (35.2/22.1/17.5) isolates the critical contribution of the stopping classifier and training design.

- **Zebra puzzle results validate out-of-order generation on constraint satisfaction (Table 1, Section 5.2):** ILM at 90% outperforms ARM (81.2%) and MDM (82.6%), approaching ARM with oracle solver ordering (91.2%). Training on fixed-order solutions while achieving strong results demonstrates the insertion paradigm handles constrained generation without problem-specific orderings.

- **Clean and well-motivated method design (Section 3, Eqs. 2–4):** The two-component loss (token insertion via normalized counts + stop prediction) and single-transformer parameterization are well-motivated. The denoising formulation using token counts between visible tokens as an approximate target insertion distribution is a practical solution to the high-variance trajectory-based objective.

- **Consistent infilling superiority over MDM (Table 3, Section 5.3.2):** ILM outperforms MDM on all infilling benchmarks across LM1B and TinyStories. The structural advantage of arbitrary-length infilling without mask constraints is a genuine capability that MDMs cannot replicate.

- **Fair experimental framework (Section 5):** All models use comparable architectures (~85M parameters) with same optimizer settings. The paper explicitly acknowledges architectural differences (DDiT AdaLN layers for MDM).

## Weaknesses

### Fatal
None

### Major
- **Text generation NLL gap with ARM is substantial, undermining "on par" framing.** On LM1B, ILM achieves 4.67 NLL vs. ARM's 3.94 — an 18.5% relative gap (Table 2). ILM (4.67) is numerically closer to MDM (4.81) than to ARM (3.94). The abstract claims ILMs "perform on par with ARMs" and the paper repeats "competitive with ARMs" throughout, but the LM1B results do not support this. The Stories gap is small (2.14 vs. 2.11) but no variance estimates are provided to confirm this is meaningful. The paper attributes the gap to "training token efficiency and scaling laws" without evidence (e.g., loss curves).

- **Systematic sequence length undershoot not discussed.** Table 2 shows ILM generates sequences with mean length 119 on Stories (dataset mean: 205, a 42% shortfall) and 21 on LM1B (dataset mean: 28, a 25% shortfall). The paper discusses MDM's overshoot ("the MDM produces longer sequences...the main reason for the high entropy") but never addresses ILM's undershoot. This matters because: (a) shorter sequences are easier for LLM judges to score as "coherent," creating a confound in Prometheus evaluations (Figure 5); (b) the stopping classifier's calibration is central to the "arbitrary-length generation" claim; and (c) the inference-time stopping procedure (threshold, argmax, max steps?) is not specified in the main text.

### Minor
- **Biased training objective introduced without analysis.** The paper acknowledges the training objective is "biased" (line 79) and defers variance discussion to Appendix D, but provides no analysis of the bias direction, magnitude, or when the approximation breaks down. This is the central technical contribution enabling ILM training; even a small-scale empirical comparison with the trajectory-based loss would strengthen the paper.

- **ILM-generated text entropy falls below dataset entropy.** On LM1B: ILM entropy = 2.80 vs. dataset entropy = 3.08; on Stories: 3.76 vs. 4.19 (Table 2). This suggests reduced vocabulary coverage or mode collapse. The paper notes ILM's entropy is "on the lower side" but doesn't analyze implications.

- **Missing inference details.** Top-k value for position sampling not specified; stopping threshold/mechanism at inference not described; no maximum step count mentioned. These affect reproducibility.

- **No variance/confidence intervals reported.** Given the small gap on Stories (0.03 NLL) and single training runs, statistical significance of text generation claims cannot be assessed.

### Trivial
None

## Nice-to-Haves
- Loss curves comparing ILM and ARM convergence rates would substantiate the "training token efficiency" explanation.
- Ablation on stopping threshold sensitivity would address the sequence length calibration concern.
- Comparing against stronger MDM sampling strategies (greedy, flow-based) rather than only tau-leaping.
- Reporting mean ± std over 3–5 seeds for text generation metrics.

## Removed Points
These points are flagged to be removed, treat them with caution:
- Criticisms about model/benchmark existence or release status removed per hard rules.
- Formatting/typo-related nitpicks removed as parser artifacts per hard rules.
- Generic methodological sweeps without specific textual grounding removed per filtering discipline.

## Novel Insights
The paper's genuinely novel contribution is demonstrating that insertion-based generation with relative positions fundamentally outperforms both ARMs (fixed order) and MDMs (absolute positions) on variable-length planning tasks, with a clear mechanistic explanation. The Insertion Transformer baseline comparison is particularly valuable—it shows that the specific design choices (denoising objective + stopping classifier) are what enable success, not merely the insertion paradigm. The arbitrary-length infilling capability is a concrete structural advantage over MDMs that cannot be trivially replicated.

## Suggestions
1. Either substantiate "competitive with ARMs" with loss curves and variance, or honestly downscope text generation claims to "better than MDMs."
2. Add analysis or ablation of the stopping mechanism and its effect on sequence length distribution.
3. Provide a small-scale empirical analysis of the biased objective's properties.
4. Report mean ± std over multiple seeds for text generation metrics.

## Reporting — Calibration Anchors

**Round 1 bracket: 5.5 – 7.0. Round 2 narrowed to 6.0 – 6.5.**

All anchors retrieved:

| Paper | Score | Round | Comparison |
|-------|-------|-------|------------|
| FiLM (Fill-in Language Models) | 4.25 | 1 | Very similar topic; rejected. Our planning results are dramatically stronger. |
| COrAL (Order-Agnostic LM) | 5.75 | 1 | Order-agnostic generation; rejected. Our planning results more convincing. |
| Path Selection BERT Generators | 3.75 | 1 | NAR generation; rejected for unclear motivation. Our paper better motivated. |
| SequenceMatch | 6.00 | 1 | Novel sequence generation approach; accepted. Comparable contribution level. |
| Scaling up MDMs | 6.50 | 1 | MDM scaling laws; accepted. More fundamental contribution but similar area. |
| SEDD | 6.60 | 1 | Score entropy discrete diffusion; rejected despite competitive AR results. |
| Energy-Based Diffusion LMs | 6.75 | 1 | Improves diffusion with energy models; accepted. Similar strengths/weaknesses. |
| Interpolating AR and Diffusion | 8.00 | 1 | Bridges AR and diffusion, SOTA. More convincing LM results; our planning results stronger. |
| Reparameterized Discrete Diffusion | 5.50 | 2 | Discrete diffusion improvements; rejected. |
| DDPD (Think while You Generate) | 5.75 | 2 | Discrete diffusion with planned denoising; accepted. Similar improvement-over-diffusion framing. |
| Efficient Perplexity Bound | 6.75 | 2 | Discrete diffusion improvements; accepted. |
| Retrieval is Accurate Generation | 6.96 | 1 | Novel generation paradigm; accepted. |

Our paper sits between Scaling up MDMs (6.5) and Energy-Based Diffusion (6.75). The planning task results are genuinely impressive and demonstrate clear advantages of the insertion paradigm. The text generation weaknesses (18% LM1B gap, 42% length undershoot, overclaimed framing) prevent a higher score but do not negate the core contribution.

## Score and Decision
The paper introduces a genuinely novel generative paradigm with compelling evidence on planning tasks. The star graph results (99.1% vs. 23%/21%) are dramatic and well-explained. The text generation evaluation has real weaknesses, but the core contribution—demonstrating that insertion-based generation with relative positions solves failure modes of both ARMs and MDMs on tasks with non-sequential dependencies—is well-supported and significant.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>