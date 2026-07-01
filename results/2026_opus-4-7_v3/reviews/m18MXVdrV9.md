Now let me draft my filtered review before calibration.Now let me do Round 1 calibration — bracketing across score bands:Let me read some key anchors to calibrate the score:Now I have enough information to form my bracket and write the final review. Let me assess the anchors:

**Round 1 Bracket:**
- Strong reject (1.0): KL divergence with GFlowNets — clearly much worse papers with fundamental flaws
- Reject (3.0): "No MCMC Teaching" (3.0), DFITE (3.0) — papers with significant methodological issues
- Borderline reject (3.5-5.5): NF-based MI estimator (4.83) — limited novelty, weak presentation; Discrete Copula Diffusion (5.25)
- Borderline accept (5.5-7.5): **MINDE (6.50)** — directly related predecessor, accepted; **SEDD (6.60)** — the base framework INFO-SEDD builds on; Convergence of discrete diffusion (7.00)
- Accept (7.5-8.5): Time-lagged IB (8.00), Learning to Permute (8.00) — stronger papers with cleaner contributions

**Initial bracket: 6.0–7.5.** The paper is at least comparable to MINDE (6.50), which is its continuous-domain predecessor. INFO-SEDD has a novel mathematical framework (Dynkin formula vs. Girsanov), addresses a genuine gap (discrete MI estimation), has stronger synthetic experiments, more diverse practical applications (motif discovery is compelling), and the absorbing-state trick. The main weakness (comparison asymmetry) is real but not fatal. The paper is not quite at the level of the 8.0 papers which have cleaner, more complete contributions.

Now let me write the final consolidated review.

---

## Summary
INFO-SEDD proposes a novel estimator for information-theoretic quantities (KL divergence, mutual information, entropy) on high-dimensional discrete data by leveraging Continuous Time Markov Chains and discrete diffusion models. The core theoretical contribution connects Dynkin's formula to KL divergence estimation via learned score ratios (Equation 4→5), while a key practical contribution — the absorbing-state trick (Equation 6) — enables single-model training for MI estimation. The method is validated on synthetic benchmarks with known ground truth and applied to text summarization model selection, genomics consistency tests, and DNA motif discovery.

## Strengths

- **Novel mathematical framework.** The derivation using Dynkin's formula (Eq. 3) to express KL divergence as an integral over score ratios along a CTMC trajectory (Eq. 4), and substituting learned parametric scores (Eq. 5), is a clean and original contribution. This requires a different mathematical apparatus (CTMCs, backward operators) from continuous diffusion estimators and the connection is non-obvious. The derivation in Section 2.2 is clearly structured.

- **Absorbing-state trick for single-model training.** Equation 6 and its justification in Section 3 show that choosing an absorbing-state noise process allows marginal scores to be computed from a single joint score model, reducing training from two models to one. This is the key practical enabler for INFO-SEDD-J and is cleanly justified via the independence structure of the absorbing process.

- **Strong synthetic validation in high-MI/high-D regime.** Table 1 demonstrates that INFO-SEDD is the only method that remains accurate as MI and dimensionality scale together (MI=50, D=50: estimate 47.77±1.18 vs. true 50), while competitors either plateau (SMILE: 18.97), diverge (MINDE: 32.60), or collapse (GAN-DIME: 17.27). The protocol (10⁵ samples, 10⁵ steps, 10 seeds, same backbone) is thorough.

- **Compelling motif discovery application.** Figure 5 shows the MI profile peaking precisely in the known TATA-box region (-39 to -26 relative to TSS), validating the method on a real biological discovery task. The sliding-window approach leverages the joint model's partial-masking capability without retraining — a genuine practical advantage over competitors.

- **Seamless integration with pretrained models.** Using MDLM-SMALL for text and CADUCEUS for genomics demonstrates that INFO-SEDD can leverage the growing ecosystem of pretrained discrete diffusion models, enhancing practical accessibility.

## Weaknesses

### Fatal
None

### Major
- **Comparison asymmetry confounds attribution of gains.** All competitors (GAN-DIME, KL-DIME, HD-DIME, SMILE, MINE, NWJ, MINDE) operate on continuous embeddings of discrete tokens, while INFO-SEDD operates natively in discrete space. The paper acknowledges this (Section 1, paragraph 3: "embed it in a continuous space and use neural estimators conceived for continuous distributions") and uses the same backbone architecture, but the experimental evidence cannot cleanly separate the contribution of the Dynkin-formula-based estimator from the advantage of avoiding the embedding bottleneck. A discrete-native baseline — e.g., estimating KL via ELBO-based log-likelihoods from the same SEDD model — would isolate the mathematical framework's contribution. This does not invalidate the contribution (the ability to avoid embeddings is itself a legitimate advance), but it leaves the source of the gains ambiguous.

### Minor
- **Approximate ground truth in real-data experiments.** The text consistency test (Section 4.2, Figure 1) uses entropy-rate estimates from Cover & King (1978) and Takahira et al. (2016) multiplied by average summary length, yielding a reference range of 256–303 nats — explicitly an order-of-magnitude estimate. The genomics consistency test (Section 4.3, Figure 4) approximates H(Y|X) ≈ H_b(Acc.), assuming uniform conditional entropy across samples. The paper is transparent about these limitations but frames the results as "consistency tests" that INFO-SEDD "passes" while competitors "fail," which somewhat overstates the tests' discriminative power. These establish plausibility, not accuracy.

- **Error bound (Eq. 7) is structurally informative but not empirically grounded.** The bound decomposes into estimation error (linear in ε_p, ε_q) and truncation bias (exponentially decaying in T), which is useful. However, constants C₁, C₂ are uncharacterized, score errors are never measured, and the bound is never evaluated numerically — even on synthetic distributions where ground truth is available. This limits the theoretical contribution to a consistency proof rather than a predictive tool.

- **Small sample for model selection correlations.** The Pearson correlation of 0.740 between INFO-SEDD-C and human consistency scores (Table 2) is based on only 15 models with human judgments. Confidence intervals on the correlation coefficients are not reported. The gap between INFO-SEDD-C (r=0.740) and INFO-SEDD-J (r=0.550) on the consistency metric is notable but not explained.

- **No computational cost analysis.** The paper does not discuss training or inference time for INFO-SEDD relative to competitors. Given that discrete diffusion model training may be substantially more expensive than training the embedding-based competitors, a cost comparison would help practitioners assess the accuracy-cost tradeoff.

### Trivial
None

## Nice-to-Haves
- An ELBO-based KL baseline using the same discrete diffusion model to disentangle the estimator's contribution from the discrete-space advantage
- Empirical evaluation of the error bound on synthetic benchmarks (measuring score errors against ground-truth score ratios, plotting bound vs. actual error as a function of T and D)
- Confidence intervals / bootstrap significance tests for model selection correlations
- Wall-clock time or FLOP comparison across methods
- Independent variation of MI and D (noted as in Appendix C.1.6 for |χ|; confirming D vs. MI independently would strengthen the analysis)

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- *(Reviewer suggested competitors' underestimation is "a known consequence of batch-size limitation" and thus "not a surprise finding")* — While true that variational bounds have known batch-size limitations (McAllester & Stratos, 2020), the paper explicitly cites this (Section 4.2: "variational approaches cannot reliably estimate MI with values larger than the logarithm of the batch size") and positions its contribution as *solving* this known problem via a different mathematical route. Demonstrating that a known problem is solved is a valid contribution, not a weakness.

- *(Suggestion that the abstract claim of outperformance should be "contextualized" since "outperformance is expected")* — Removed as a style nitpick. The abstract accurately states the result, and the introduction provides the context. Outperformance over embedding-based methods is not trivially "expected" since no prior discrete-native method existed.

## Novel Insights
The core insight — that Dynkin's formula provides a direct route from discrete diffusion score functions to KL divergence estimation, bypassing both the exponential sample complexity of variational bounds and the embedding bottleneck for discrete data — is genuinely novel. The absorbing-state trick that enables single-model MI estimation over arbitrary variable subsets (exploited effectively in the motif discovery application) is a practically important design contribution that extends the utility of pretrained discrete diffusion models beyond generation.

## Suggestions
- Add a discrete-native baseline (ELBO-based KL from the same SEDD model) to isolate the Dynkin-formula estimator's contribution
- Measure score approximation errors on synthetic distributions against known ground-truth score ratios, and plot the error bound (Eq. 7) vs. actual estimation error
- Explain the performance gap between INFO-SEDD-C and INFO-SEDD-J on the text model selection task (r=0.740 vs. r=0.550) — is this attributable to optimization difficulty, the conditional vs. joint formulation, or statistical noise?
- Report bootstrap confidence intervals for the model selection correlations given the small sample size (n=15)

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to INFO-SEDD |
|-------|------|-----------|-------|------------------------|
| KL Divergence with GFlowNets | Uj0h13lVrR | 1.00 | R1 | Much weaker; fundamental methodology issues |
| IC-Light (illumination) | u1cQYxRI1H | 0.50 (10.0 actual) | R1 | Anomalous retrieval; unrelated |
| Clothing-Irrelevant L-ReID | 5lUdTogEL3 | 1.00 | R1 | Much weaker; different domain |
| Financial Markets NN | nSDOkm0SKo | 1.00 | R1 | Much weaker; low quality |
| No MCMC Teaching for EBMs | 46tjvA75h6 | 3.00 | R1 | Weaker; more fundamental issues with method |
| DFITE | 4u0ruVk749 | 3.00 | R1 | Weaker; incomplete experiments, stronger assumptions |
| Deficit of New Info in Diffusion | rAZ3yCpc3K | 3.00 | R1 | Weaker; less novel contribution |
| TF-score | RDLvnUJ5JZ | 3.00 | R1 | Weaker; empirical-only, no theoretical novelty |
| NF-based MI estimator | vgQmK5HHfz | 4.83 | R1 | Weaker; limited novelty, weak presentation, synthetic-only |
| Conditional Entropy Reduction | OT2NFdNrny | 4.75 | R1 | Weaker; less impactful contribution |
| Discrete Copula Diffusion | FXw0okNcOb | 5.25 | R1 | Comparable scope but less compelling experiments |
| Derivative-Free Guidance | 2fgzf8u5fP | 3.80 | R1 | Weaker; different problem, mixed reviews |
| **MINDE** | **0kWd8SJq8d** | **6.50** | **R1** | **Direct predecessor; INFO-SEDD has stronger experiments, novel discrete framework, more applications** |
| Convergence of Discrete Diffusion | pq1WUegkza | 7.00 | R1 | More theoretical; INFO-SEDD more application-oriented but comparable quality |
| **SEDD** | **71mqtQdKB9** | **6.60** | **R1** | **Base framework; INFO-SEDD builds useful applications on top, similar quality level** |
| Steering MDMs via DDPP | Ombm8S40zN | 6.25 | R1 | Different focus; comparable contribution level |
| Time-lagged IB | bH6T0Jjw5y | 8.00 | R1 | Stronger; cleaner contribution, better validation |
| Learning to Permute | EO8xpnW7aX | 8.00 | R1 | Stronger; more complete contribution |
| Progressive Compression | CxXGvKRDnL | 8.00 | R1 | Stronger; cleaner theoretical-practical bridge |
| Variational Diffusion Posterior | 6EUtjXAvmj | 8.00 | R1 | Stronger; better validated methodology |

**Round-1 bracket: 6.0–7.5**

**Narrowing rationale:** INFO-SEDD is clearly stronger than the NF-based MI estimator (4.83) and the borderline papers in the 5.0-5.5 range. It compares favorably to MINDE (6.50), its direct predecessor: INFO-SEDD has a novel mathematical framework (Dynkin formula vs. Girsanov theorem), addresses a genuine gap (discrete MI estimation), demonstrates stronger synthetic results (Table 1), and offers more diverse practical applications (motif discovery, model selection). However, the comparison asymmetry weakness keeps it slightly below the 8.0 papers, which have cleaner experimental validations with less ambiguity in attribution. The paper's contribution level sits between MINDE (6.50) and the convergence paper (7.00) — novel method with solid but imperfect validation.

**Final score: 7.0** — The paper makes a genuine, well-executed contribution: a novel mathematical framework for discrete MI estimation that fills a real gap, with strong synthetic validation and compelling applications. The main weakness (comparison asymmetry) is methodological but addressable, and does not undermine the core contribution. The paper merits acceptance as a borderline but positive contribution.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>