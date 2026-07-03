Now I will produce the final consolidated review.

---

## Summary

This paper investigates whether LLMs exhibit a human-like inductive bias toward Information Bottleneck (IB)-efficient semantic categorization. Using color naming as a testbed (chosen for uniquely rich cross-linguistic and behavioral data), the authors conduct two studies: (1) an English color-naming experiment across 39 models from 6 families, showing that larger instruction-tuned models achieve better English alignment and IB-efficiency; and (2) an iterated in-context language learning (IICLL) paradigm simulating cultural transmission of pseudo color-naming systems, finding that LLMs restructure initially random systems toward greater IB-efficiency. The strongest result—recapitulating the full range of near-optimal IB tradeoffs observed across human languages—is demonstrated by Gemini 2.0, while other tested models converge to lower-complexity solutions. A preliminary Shepard circles experiment provides initial evidence the bias may extend beyond color.

## Strengths

1. **Comprehensive model coverage with controlled variation.** The English naming study tests 39 models across 6 families (Gemini, Gemma, Llama, Qwen, Olmo, GPT-2), systematically varying size, instruction-tuning, modality, and training checkpoints. This enables specific attributions, e.g., that instruction-tuning (rather than scale alone) drives English alignment gains, and that Olmo's alignment only emerges in the second training stage (Section 3, Figure 2c, Appendix F).

2. **IICLL is a creative and principled methodological adaptation.** The paper adapts iterated in-context learning (I-ICL) to iterated in-context *language* learning (IICLL), closely mirroring the human iterated language learning paradigm of Xu et al. (2013). Using pseudo-words and presenting stimuli as unlabeled "features" (in the text-only variant) goes beyond simple pattern mimicry tests. Direct comparison with human IL data on the same information-plane axes (Figure 3) is a methodological strength.

3. **Quantitative comparison on the same IB information plane as human data.** The paper plots LLM IICLL trajectories alongside human IL data (Xu et al., 2013), cross-linguistic WCS data, and the theoretical IB bound (from Zaslavsky et al., 2018) on the same complexity-accuracy axes (Figure 3). Convergence within ~4 generations matching human dynamics is shown over 12 generations with confidence intervals (Figure 4). This enables a direct quantitative rather than qualitative analogy.

4. **Robust and somewhat surprising finding about English naming failures.** Many state-of-the-art LLMs struggle with basic English color naming. The finding that some models (e.g., Olmo 2 32B, Qwen 2.5 VL 7B) produce systems resembling low-resource WCS languages rather than English is underexplored but genuinely interesting (Section 4.1, Figure 9 in Appendix E). The observation that CIELAB coordinates degrade performance (consistent with Marjieh et al., 2024) reveals a systematic difference between how LLMs and humans represent color.

5. **Rotation analysis provides a non-triviality check.** The hue-rotation control (Regier et al., 2007) shows that for Gemini, the emergent IICLL systems are not random — rotating the label mapping significantly decreases efficiency and alignment. A clustering baseline (Appendix M) provides additional comparison.

## Weaknesses

### Fatal
None.

### Major

1. **The headline IICLL result (recapitulating the full human-like range of IB tradeoffs) is demonstrated only for Gemini 2.0, and the primary control for non-trivial structure also works only for Gemini.** The paper acknowledges this explicitly ("less conclusive" for other models on rotation analysis; "only the model with strongest in-context capabilities"). However, this means the paper's most striking claim — that "LLMs are capable of evolving human-aligned semantic systems" and that IICLL recapitulates "the wide range of near-optimal IB-tradeoffs observed in humans" — rests on a single proprietary model whose architecture, training data, and RLHF procedure are opaque. The other three models (Gemma 3 27B, Llama 3.3 70B, Qwen 2.5 32B) converge to low-complexity solutions, and the rotation analysis "is less conclusive" for them, meaning the paper cannot fully rule out that their emergent systems are trivially structured. While the paper is transparent about this, the abstract and discussion still use collective language ("LLMs iteratively restructure..."; "LLMs are capable of evolving...") that over-extrapolates from what the data actually supports. The finding about Gemini is genuinely interesting on its own terms, but the paper would be stronger if it led with: "Gemini 2.0, under IICLL, can recapitulate the full range of human IB-efficient color naming systems; other models converge to low-complexity solutions."

2. **The IICLL paradigm does not fully distinguish inductive bias from retrieved knowledge for multimodal models.** The paper argues that because IICLL uses pseudo-words and (in the text-only variant) does not tell models the stimuli are colors, convergence to IB-efficiency must reflect inductive bias rather than retrieval from training data. This argument is clearest for the text-only variant using coordinate inputs. However, for multimodal models (including Gemini, which receives color images), the model can clearly recognize these as colors. A model that has been trained on text describing efficient color naming systems across languages could plausibly reproduce IB-efficient category structures by *retrieving and applying* its knowledge about how colors are typically partitioned, rather than revealing a prior over all possible category systems. The pseudo-words prevent direct copying of English terms but do not prevent the model from using its knowledge that "color category boundaries tend to respect perceptual similarity" — a pattern present in its training data. The paper does not adequately address this alternative account.

### Minor

3. **Asymmetric inference procedures between Gemini and open models.** The paper uses controlled generation (Gemini API) for Gemini and log-probability scoring for all open-weight models. These are different decision procedures — controlled generation samples from a restricted output space, while log-probability scoring picks the highest-probability term. The paper does not discuss whether this asymmetry could affect comparability, particularly for the complexity metric (which depends on the entropy of the labeling distribution). If log-probability scoring yields sharper or more dispersed distributions than controlled generation, this could systematically affect the measured IB tradeoff. A control experiment on at least one open model using both procedures would be helpful.

4. **The Shepard circles experiment does not support the IB-efficiency domain-generality claim.** Section 4.3 is explicitly preliminary (k=4, Gemini only, no IB analysis) and acknowledges that "an important direction for future work is to test whether this emergent structure also supports greater IB-efficiency." The experiment only shows that Gemini can learn structured (compact) partitions of a 2D synthetic stimulus space under IICLL — it provides no evidence about IB-efficiency generalizing beyond color. The abstract says this "suggest[s] that our result could potentially apply also in other domains," which is appropriately hedged but overstates what a compactness-only result can support.

5. **Gemini reaches complexity values (~14 bits) far beyond any human language (~7 bits max).** Figure 3 shows Gemini's IICLL systems reaching complexity values roughly double the upper bound of human languages. The paper presents this positively ("captures the complexity range"), but this deviation from human-like behavior warrants discussion. Are these high-complexity systems actually efficient, or are they using the freedom of pseudo-words to create overly complex solutions that the IB bound deems efficient only because the IB bound doesn't penalize high complexity equally across all regimes?

### Trivial
None.

## Nice-to-Haves

- A control experiment using a genuinely novel stimulus space (not color, not Shepard circles) where the model has no plausible training data exposure, to more directly test whether the IB-efficiency bias is domain-general.
- Systematic analysis of *where* the non-Gemini models fail in IICLL: is the failure a capacity issue (context window), a learning issue (ICL degradation with many examples), or a representational issue?
- Error analysis of the English naming task: which color chips are most commonly mislabeled, and are the errors systematic or idiosyncratic?

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Claim that the paper "systematically overclaims" by presenting IICLL results as a property of "LLMs" generally.** This is removed because the paper actually qualifies its claims: the abstract says "only a model with strongest in-context capabilities (Gemini 2.0) is able to recapitulate the wide range" and Section 4.2 explicitly states the other models converge to lower-complexity solutions. The collective language ("LLMs iteratively restructure") refers to the finding that all four tested models show convergence toward IB-efficiency, which is supported by Figure 4. The paper is reasonably transparent.
- **Claim that models cannot be independently verified.** Removed per rule: we cannot question the existence or availability of cited models.
- **Claim about missing appendix details (chain counts, training data sampling).** Removed per rule: parser strips appendices; these exist in the original submission.
- **Claim about "no statistical testing."** Removed per rule: this likely lives in the stripped appendix; the paper reports "significant decrease" and shows 95% confidence intervals in Figure 4.
- **Generic "add more models" / "larger dataset" type requests.** Removed as the 39-model coverage is already adequate.

## Novel Insights

The most valuable insight from the reviews is the asymmetric inference procedures point (controlled generation vs. log-probability scoring), which the authors should address. The harsh critic's suggestion that the paper would be *more* interesting if it honestly led with "Gemini 2.0 can do X; other models cannot" is a framing insight that the authors could adopt regardless of any additional experiments. Beyond these, no genuinely novel observation emerged from the reviews that the paper's own discussion does not already contain.

## Suggestions

1. **Run a control comparing inference procedures on at least one open model.** Test controlled generation (via API or constrained decoding) vs. log-probability scoring on, e.g., Gemma 3 27B for the IICLL task to measure whether the procedure affects the IB tradeoff curves.

2. **Address the retrieved-knowledge alternative more directly for multimodal models.** If Gemini receives images, run an IICLL condition where the same color stimuli are presented to Gemini via text-only coordinates (like the open models) and compare the trajectories. If the inductive bias account is correct, the text-only Gemini should also converge to IB-efficient solutions; if the result depends on visual recognition of colors, the text-only condition should degrade.

3. **Calibrate the paper's framing.** The abstract and discussion should more precisely distinguish the claim that generalizes across models (all tested LLMs show some IB-efficiency bias) from the claim specific to Gemini (recapitulating the full human range of IB tradeoffs). The phrase "LLMs are capable of evolving human-aligned semantic systems" in the abstract is technically supported for Gemini but could mislead a casual reader.

4. **Discuss the ~14-bit complexity ceiling for Gemini.** Add a paragraph explaining why Gemini reaches complexity values double those of human languages and whether these high-complexity systems should be considered human-aligned.

5. **Remove or explicitly caveat the Shepard circles domain-generality claim** about IB-efficiency (vs. mere structured categorization) in the abstract, since the experiment does not measure IB-efficiency.

## Score and Decision

I am unable to use the calibration search tool due to file-system errors in the calibration database, so I anchor my score qualitatively. This paper is a well-motivated, methodologically creative empirical study with genuinely interesting findings: the large-scale English naming survey (39 models) is thorough; the IICLL paradigm is a novel adaptation of iterated learning to LLMs; and the observation that Gemini 2.0 can recapitulate human-like IB-efficient color naming systems is striking. The weaknesses are real but not fatal — they concern framing precision and limited generalizability rather than methodological invalidity. The paper is reasonably transparent about its main limitation (Gemini-specific nature of the strongest result), and the core contributions are solid. This is clearly above the borderline reject threshold and comfortably in the accept range, though not a top-venue "strong accept" due to the reliance on a single proprietary model for the headline IICLL result and the incomplete control for the retrieval alternative. I calibrate this against typical ICLR papers: it is stronger than a marginal empirical paper (score 4–5) but below a landmark finding with airtight controls across multiple models (score 8+).

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>