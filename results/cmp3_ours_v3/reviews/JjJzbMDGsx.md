Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper introduces the Language Confusion Gate (LCG), a lightweight MLP module that operates at decoding time to filter tokens by language family (CJ, Latin, Symbols, Low-Res) in multilingual LLMs. The gate is trained via a novel norm-adjusted self-distillation procedure: the paper first identifies a token embedding norm imbalance that biases models toward high-resource languages (Section 3.2), then uses norm-corrected top-k/p predictions as pseudo-targets for training. LCG achieves substantial reductions in cross-script language confusion (e.g., Qwen3-30B CJ confusion 1.0%→0.0%, Latin 4.4%→0.4%) across Qwen3, Llama3.1, Gemma3, and GPT-OSS models, with a sparse intervention rate of ~0.3–0.4% of tokens and ~0.4% latency overhead.

## Strengths

- **A clean mechanistic finding — the token embedding norm imbalance (Section 3.2, Table 1, Figure 2).** The paper identifies that output token embeddings are systematically larger for high-resource-language tokens, and demonstrates this across five models. Adjusting logits by these norms cleanly removes CJ tokens from the top-10 at a confusion point (Figure 2). This observation is reproducible and is itself a useful contribution to understanding language confusion.

- **The self-distillation training target is well-grounded in the norm analysis (Section 4.2).** Rather than using an arbitrary training signal, the paper derives pseudo-targets from norm-adjusted top-k/p logits, creating a coherent conceptual arc from the mechanistic observation to the training method. The ablation comparing LCG-adjusted vs. LCG-unadjusted (Table 3) convincingly demonstrates that norm-adjustment in training matters (e.g., Llama3.1-8B Latin confusion drops from 5.7% to 2.9% with norm adjustment).

- **Sparse intervention with low overhead.** The intervention rate of ~0.3–0.4% of tokens (Section 5.3) and 0.4% latency overhead (Section 6) make this practically attractive for production deployment. The method is demonstrated to be compatible with speculative decoding.

- **Evaluation across multiple model families and sizes.** Experiments cover Qwen3-8B, Qwen3-30B, Llama3.1-8B, Gemma3-12B, and GPT-OSS, in both standard and reasoning-model variants. This breadth strengthens generalizability claims.

## Weaknesses

### Major

**1. Missing comparison against the most directly relevant baselines (Nie et al. 2025, Ji et al. 2025).** Both are decoding-time intervention methods — the same class as LCG. The paper cites them in Related Work (Section 2, line 84) and positions LCG as addressing their limitations ("some require model retraining… others lack ability to distinguish legitimate code-switching"), yet neither appears as an experimental baseline. The existing baselines (ICL, greedy decoding, ORPO) are either weak or constitute a fundamentally different approach (training-based preference optimization). Without comparison against the closest prior work, the paper cannot substantiate its claim that LCG offers a genuine improvement over existing decoding-time interventions. This is the most significant gap in the evaluation.

**2. Training signal has known blind spots that are not empirically characterized.** Section 3.2 (line 155) explicitly states that norm-adjustment "can't explain language confusion between English and Chinese since they both have high norm, or between low resource languages since they both have low norm." Yet the gate is trained on pseudo-targets derived *entirely* from norm-adjusted logits. This means the training signal has known blind spots — cases where confusion is not norm-driven. The paper never evaluates the gate on such scenarios (e.g., same-script confusion between English and Spanish, or between two low-resource languages). Without this characterization, it is unclear how much of the observed improvement comes from the gate's learned predictions vs. the fact that most evaluated confusion is cross-script and norm-driven. The paper acknowledges this limitation in Section 6 but does not assess its practical severity.

### Minor

**3. The "order of magnitude" claim is broader than the evidence.** The abstract and introduction claim LCG reduces confusion "often by an order of magnitude." From Table 3: Llama3.1-8B Latin confusion drops 8.4%→2.9% (~2.9×), Gemma3-12B CJ 0.2%→0.1% (2×), Latin 1.0%→0.5% (2×). Several model/metric combinations show 2–6× reductions, not 10×. While some cases do reach or exceed 10× (e.g., Qwen3-30B CJ 1.0%→0.0%), the "often" qualifier in the abstract overstates the typical case. The reductions are still meaningful, but the claim should be calibrated to match the empirical distribution.

**4. No variance or confidence intervals reported.** All confusion rates in Tables 2–5 are point estimates. For small rates (0.0%, 0.06%, 0.11%), it is unclear whether differences are stable or within noise. The FLORES-NO-LATIN subset size is not reported, so a CJ confusion rate of 0.2% could correspond to very few sentences. Similarly, Pass@1 differences on Humaneval-XL (Table 4: e.g., Qwen3-8B 83.81→83.13) could be within sampling variability, but the paper does not discuss this.

**5. Intervention rules (Section 4.3) not individually ablated.** Rules 2 and 3 can override the gate's own predictions (Rule 2: no intervention if the model's high-confidence candidates don't contain the gate-predicted language family; Rule 3: always allow the previous token's language). Only the aggregate "No Rule" condition is shown in Figure 3. The paper does not report how often each rule triggers or their individual contribution to the overall reduction.

**6. Code-switch evaluation lacks annotation details.** The first experiment (86.7% preservation of natural code-switch) is based on human-annotated examples, but the number of examples, inter-annotator agreement, and annotation criteria are not reported. This makes it difficult to assess the reliability of this finding.

**7. Four-way language-family granularity limits scope.** The paper acknowledges this in Section 6 (cannot resolve within-script confusion like Spanish vs. English), but the practical prevalence of such confusion across the evaluated benchmarks is not discussed. The method targets *cross-script* confusion; this should be stated more prominently.

### Trivial

None.

## Nice-to-Haves

- Evaluate on a broader set of generation tasks beyond translation and QA (e.g., open-ended generation, dialogue) to strengthen generality claims.
- Report results on the Language Confusion Benchmark (LCB) as a supplement, with discussion of which cases are confounded.
- Provide more detail on the ORPO training setup (data size, hyperparameters, training epochs) to support the fairness of that comparison.
- Ablate the contribution of each intervention rule individually (trigger frequency, effect on confusion rate).

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Abstract frames solving evaluation problem but proposes intervention"** — The sentence about "lack of automatic way of evaluation" (line 19) is slightly unclear but is not a core issue; it reads as a motivation statement, not a mischaracterization of the method. REMOVED as not a genuine weakness.
- **"Figure 2 after norm-adjustment shows mostly 'n' variant artifacts"** — The norm-adjusted distribution is used solely to identify the correct language family, not as a final sampling distribution. The paper's purpose in showing this is clear from context. REMOVED as a misinterpretation.
- **"Not using LCB makes cross-study comparison difficult"** — The paper provides explicit rationale for this design choice (code-switching in queries, unreliable detector, lines 233). This is a reasonable methodological decision. MOVED to nice-to-have.
- **"ORPO baseline fairness unclear"** — The paper describes preparing a custom dataset with synthesized confusion samples, which is standard practice for preference optimization. MOVED to nice-to-have.
- **"Missing related works"** — Cannot be verified without external sources. REMOVED per policy.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add the two most directly relevant baselines:** Implement the neuron-suppression method (Nie et al., 2025) and the post-hoc token-smoothing method (Ji et al., 2025) on the same models and benchmarks. This is the single highest-impact improvement the paper could make — it would allow readers (and the paper itself) to assess whether LCG genuinely advances the state of the art in decoding-time intervention.
2. **Calibrate the "order of magnitude" claim** to match the empirical results, or report per-model/metric reductions transparently.
3. **Report confidence intervals or bootstrap estimates** for the main confusion-rate results, especially for very small rates where noise could dominate.
4. **Characterize the gate's blind spots empirically:** Construct a diagnostic set where confusion is not norm-driven (e.g., English→Spanish within Latin script) and report the gate's accuracy.
5. **Report per-rule trigger frequencies and effect sizes** for the three intervention rules, so readers can assess the gate's independent contribution.
6. **Document the code-switch annotation procedure** (number of examples, annotator agreement, criteria) to support the 86.7% preservation claim.

## Score and Decision

**Calibration bracket (Round 1):** Based on the retrieved anchors, the plausible score range was 4.75–6.6. The paper is substantially stronger than papers scoring ~3.0 (e.g., "Llamas think in English" — single task, presentation issues, rejected) but has evaluation gaps that prevent it from reaching the level of papers scoring ~6.6 (e.g., "The Same but Different" — clean mechanistic analysis, accepted). The closest comparable anchor is "The Rise and Down of Babel Tower" (avg 5.25, accepted) which also has methodological limitations but a clear contribution. The paper under review has a stronger practical contribution and broader evaluation than the Babel Tower paper, but the missing baselines and training-signal blind spots are more significant weaknesses.

**Calibration anchors retrieved (all rounds):**

| Paper | Score | Round | Comparison |
|-------|-------|-------|------------|
| gwZ90hFSL2 (Advancing Cross-Lingual Capabilities) | 1.00 | 1 | Not a real contribution; far weaker |
| 8QTpYC4smR (Systematic Review of LLMs) | 1.00 | 1 | Survey paper; far weaker |
| 5kMwiMnUip (NEMESIS Jailbreaking) | 1.40 | 1 | Nonsense paper; far weaker |
| fSbPwHjdDG (Llamas think in English) | 3.00 | 1 | Single-task, presentation issues; our paper is substantially stronger |
| 4y3GDTFv70 (Latent Space Theory) | 3.25 | 1 | Theoretical paper with limited validation; weaker |
| r3GxWNGpSj (XTransplant) | 4.75 | 1 | Multilingual probing method; comparable scope but weaker method contribution |
| eznTVIM3bs (Rise and Down of Babel Tower) | 5.25 | 1 | Accepted; similar profile with methodological concerns; our paper has stronger practical contribution |
| BCyAlMoyx5 (Crosslingual Capabilities/Knowledge Barriers) | 5.67 | 1 | Rejected; analysis-focused; our paper has stronger practical contribution |
| hsMkpzr9Oy (Mexa) | 5.40 | 1 | Evaluation-focused; different contribution type |
| cif0JVXJ3b (Qualifying Knowledge) | 5.25 | 1 | Analysis paper; different contribution type |
| HMa8mIiBT8 (Knowledge Cross-Lingually Consistent) | 6.00 | 1 | Solid analysis paper; our method contribution is comparable in quality |
| NCrFA7dq8T (The Same but Different) | 6.60 | 1 | Accepted; clean mechanistic interpretability; our paper has more evaluation breadth |
| FrFQpAgnGE (Unified Representation Space) | 7.00 | 1 | Strong accepted paper; our paper is not at this level |
| vf5aUZT0Fz (DEPT) | 8.00 | 1 | Strong accepted paper; far above our paper's level |

The paper presents a genuinely useful contribution — a practical, low-overhead solution to language confusion grounded in a clean mechanistic finding — but the evaluation has two significant gaps: (1) the most directly comparable prior methods are not included as baselines, and (2) the training signal's known blind spots are not empirically characterized. These issues are addressable but prevent the paper from making a fully convincing case in its current form.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>