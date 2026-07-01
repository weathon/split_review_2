## Summary

Thoughtbubbles introduces a transformer variant that learns to dynamically fork and delete residual streams during pretraining using only language modeling loss. The method assigns cumulative scores to residual streams, uses top-k selection to decide which streams to duplicate or prune, and attenuates attention/residual updates by these scores. Experiments from 150M to 772M parameters on OpenWebText and peS2o show consistent perplexity improvements and gains on LAMBADA and HellaSwag compared to a parameter-matched transformer and a simple input-copying baseline.

## Strengths

1. **Genuinely novel architecture for adaptive parallel computation.** The forking mechanism (Eqs. 1–11) that learns where and how many parallel residual streams to allocate, trained with only an LM loss, is a meaningful departure from prior work on pause tokens (which require manual placement) and recurrent adaptive computation (Graves, 2016; Dehghani et al., 2019). The technical specification in Sections 2.3–2.4 is clear and precise.

2. **Consistent and non-trivial perplexity improvements across all settings.** In Table 1, Thoughtbubbles (κ=4L) achieves the lowest validation perplexity in every single configuration (6 model sizes × 2 datasets = 12 settings). The gains are meaningful — e.g., 19.74 vs. 20.90–21.22 for 772M on OpenWebText, and a 319M Thoughtbubbles model outperforms the 772M baseline on the same metric.

3. **Analysis connecting computation allocation to token uncertainty.** Figure 5 shows that the model allocates more forks at tokens with moderate output entropy, and less at both very low and very high entropy regions. This provides suggestive evidence that the forking mechanism responds to token-level difficulty, consistent with the paper's claimed motivation.

## Weaknesses

### Fatal
None.

### Major

1. **The evaluation is structurally disconnected from the paper's central motivation.** The paper repeatedly frames Thoughtbubbles as addressing *multi-step reasoning* and *scaling inference-time computation for complex problems* (lines 13–15: "solving complex, multi-step problems"; lines 312: "allows our model to solve more difficult tasks that require scaling inference-time computation"). Yet every benchmark evaluated — LAMBADA (single-word cloze), HellaSwag (sentence completion), BLiMP (grammaticality), PIQA (physical commonsense) — is a single-utterance or local prediction task. None requires multi-step reasoning, arithmetic, or compositional inference. The paper acknowledges this only in the limitations (line 322: "cannot experiment... on hard reasoning datasets such as GSM8k"). While the core architectural contribution stands independently, the framing in the abstract, introduction, and conclusion creates an expectation the evaluation does not meet. A simple arithmetic benchmark (e.g., variable-length addition) or TinyGSM at the 772M scale would have tested whether the dynamic bubbling mechanism actually aids multi-step computation; the absence of any such test narrows the claimed contribution considerably.

2. **Parameter-matched and FLOPs-matched claims are stated without supporting evidence.** The Table 1 caption says "Each setting is parameter-matched" and "roughly FLOPs-matched against copy-5 baseline," but the paper provides no actual parameter counts, no FLOPs measurements per forward pass, and no wall-clock time comparisons. Thoughtbubbles adds forking decision functions, per-layer fork embeddings, and score-attenuation machinery; if total parameters equal the baseline, the base transformer layers must be narrower — a confounding factor. If total parameters are larger, the "parameter-matched" claim is incorrect. Similarly, the dynamic number of forks makes exact FLOPs comparison nontrivial, and "roughly" is not quantified. Without these measurements, the reader cannot verify the fairness of the central comparisons.

### Minor

3. **Overstated characterization of zero-shot results.** The paper claims "Across most zero-shot evaluations, our approach outperforms baselines" (line 218). Examining Table 1: on **BLiMP**, Thoughtbubbles *underperforms* the Copy baselines in 10 out of 12 settings (e.g., 78.8 vs. 80.5 at 319M OWT; 67.4 vs. 73.3 at 772M peS2o). On **PIQA**, results are mixed with margins under 2 points and no clear pattern. Only LAMBADA and HellaSwag show consistent improvements. The paper does acknowledge the BLiMP limitation (lines 220–223) in one sentence, but the phrase "across most zero-shot evaluations" overstates the empirical picture.

4. **Gradient flow through the hard top-k operation is not specified.** Equations (4)–(6) implement a hard discrete selection (top-k). The paper does not state how gradients are propagated through this operation — whether via a straight-through estimator, REINFORCE, soft top-k relaxation, or some other mechanism. The limitations section mentions a "top-K gradient bottleneck" (line 320) but does not connect this to the training mechanism. This is a critical architectural detail for reproducibility.

5. **The Copy-3/Copy-5 baseline is a weak instantiation of "non-adaptive parallel computation."** The paper itself calls it "naive" (line 169): it simply copies the input residual multiple times before the transformer and takes the rightmost for decoding. A more informative non-adaptive baseline would maintain parallel streams throughout all layers with a fixed topology, which would isolate the benefit of *adaptivity* vs. *parallelism itself*. Since the main comparison is against the regular transformer (where Thoughtbubbles clearly wins), this weakness is not fatal, but it weakens the claim of beating "non-adaptive parallel computation."

6. **No error bars, confidence intervals, or variance measures reported.** Given the modest gains (often <2 points) and the small evaluation datasets, it is impossible to assess statistical significance. This is a standard expectation for experimental papers.

7. **The BLiMP negative result is under-analyzed.** The paper dismisses it with one sentence (lines 220–223: "pruned dynamic parallel computation may not be as helpful for syntax matches"). Given that the degradation is systematic (worse in 10/12 settings against Copy baselines), this deserves exploration — e.g., does forking disrupt syntactic structure? Does the score-attenuated attention hurt long-range syntactic dependencies? This is an important limitation worth more than a sentence.

8. **Basic statistics about fork allocation are missing.** Figure 5 shows aggregated fork counts, but the paper never reports: what fraction of tokens get forked? How many forks per token on average? How does allocation vary across layers? Without this, the reader cannot tell whether the model is truly adaptive or uses a nearly-fixed allocation.

9. **The entropy-computation "concave parabolic relationship" (Figure 5) is asserted without statistical support.** No curve fit, regression, or correlation measure is reported. The post-hoc explanation for the downturn at high entropy ("edges of clauses or coreferences," line 282) is speculative.

### Trivial
None.

## Nice-to-Haves

- Compare against a properly designed non-adaptive parallel baseline (fixed k parallel streams with cross-attention throughout all layers) to isolate the value of adaptivity.
- Compare against pause-token baselines (Goyal et al., 2024; Herel & Mikolov, 2024; Sun et al., 2025) directly, even at one scale.
- Report wall-clock time or tokens/second to complement the "FLOPs-matched" claim.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"First-known" priority claim is too strong (Abstract/Introduction).** The reviewer argued the claim should be tempered because prior work on adaptive computation (Graves, 2016; Dehghani et al., 2019) already addresses unsupervised adaptive compute allocation. *Reason for removal*: The reviewer acknowledges the distinction ("though not via parallel residual forking"). The paper's claim is specifically about "unsupervised dynamic allocation of latent *parallel* computation," which differs from recurrent adaptive computation. This is a correct claim, not an overstatement.

- **Causal attention mask discussion is missing (Missing Parts).** *Reason for removal*: The paper does discuss this. Line 73 states "We fork tokens to the left of the original input token" and line 271 states "forked children cannot attend to its parent." The causal masking implications are addressed.

- **Figure 4 attention analysis is trivial due to position adjacency.** *Reason for removal*: While position is a confound, the paper shows the parent token attends to its children at rates an order of magnitude higher than to other tokens (Figure 4, left column). The effect size far exceeds what adjacency alone would explain. This criticism underestimates the evidence presented.

- **Score-attenuated attention inefficiency (low-scoring tokens consume compute but contribute nothing).** *Reason for removal*: This is a design characteristic, not a flaw. Low-scoring tokens are pruned at the next forking layer; the "inefficiency" spans at most one layer. The paper's design intentionally uses attenuation to learn useful scores.

- **Missing comparison to pause-token baselines.** *Reason for removal*: The paper's contribution is orthogonal to pause-token methods (which insert tokens before computation). The paper cites and distinguishes itself from these approaches conceptually. An empirical comparison would strengthen the paper but its absence is not a weakness given the different mechanisms.

- **No discussion of time-matched evaluations (from Missing Parts).** *Reason for removal*: The paper explicitly acknowledges this in the limitations section (line 318: "Time-matched evaluations… raw wall-clock efficiency is relatively low"). This is already addressed.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the central tension between the paper's ambitious framing (scaling inference-time compute for reasoning) and its narrow evaluation (perplexity + simple benchmarks), but do not add a new analytical perspective beyond what the paper's own analysis and limitations already suggest.

## Suggestions

1. **Provide concrete parameter counts and FLOPs measurements** for all models (baseline, Copy-3, Copy-5, Thoughtbubbles κ=2L and κ=4L) to substantiate the "parameter-matched" and "FLOPs-matched" claims.
2. **Add at least one simple multi-step reasoning evaluation** (e.g., variable-length addition, or TinyGSM at the 772M scale) to test whether the dynamic bubbling mechanism aids compositional computation. If the method does not help on such tasks, revise the claims accordingly.
3. **Tone down the claims about "solving more difficult tasks that require scaling inference-time computation"** given the evaluation only covers perplexity and single-utterance benchmarks.
4. **Specify the gradient mechanism** for the hard top-k selection (straight-through, soft top-k, or other).
5. **Report basic fork statistics** (fraction of tokens forked, mean forks per token, variance across layers) to demonstrate that allocation is meaningfully adaptive.
6. **Add error bars** (e.g., bootstrap confidence intervals) for all evaluation metrics.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>