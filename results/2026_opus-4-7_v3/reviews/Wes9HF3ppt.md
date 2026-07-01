Now let me verify several specific claims from the reviewer in more detail.Now let me check the abstract and the paper's own framing of the LM results more carefully:Now I have a thorough understanding of the paper. Let me draft the review.Now let me run calibration Round 1 to bracket the score:Let me read a few of the most relevant anchors:Now let me read the SEDD paper for additional calibration:Now let me do Round 2 calibration to narrow the bracket from 5.0-7.0:Let me read the most directly comparable anchor — "Beyond Autoregression: Discrete Diffusion for Complex Reasoning and Planning":Now I have enough calibration data. Let me finalize the review.

**Round 1 Bracket: 5.0–7.0**

Key anchor comparisons:
- "Beyond Autoregression: Discrete Diffusion for Complex Reasoning and Planning" (6.25, accepted) — nearly identical scope: shows non-AR models outperform ARMs on planning, limited natural language evaluation, ~85M parameters. ILM adds infilling capability but has under-analyzed training bias and overclaiming.
- "Think while You Generate" (5.75, accepted) — diffusion for planning, similar scope.
- COrAL (5.75, rejected) — order-agnostic LM, similar in ambition but different failure modes.
- FiLM (4.25, rejected) — fill-in LMs, weaker execution.
- SEDD (6.60, rejected) — stronger theoretical foundation but different focus.
- SAD3-LM (8.00, accepted) — significantly stronger paper with comprehensive theory.

**Round 2 Narrowing: 5.5–6.5** — The paper's planning contributions are genuine and well-demonstrated (comparable to "Beyond Autoregression"), the infilling capability is an additional real contribution, but the overclaimed LM results and under-analyzed training approximation prevent it from reaching 6.5+.

**Final score: 6.0**## Summary
This paper introduces Insertion Language Models (ILMs), which generate sequences by inserting tokens at arbitrary positions one at a time, jointly predicting both insertion position and token identity. ILMs are positioned as a synthesis of autoregressive models (variable length) and masked diffusion models (flexible order), overcoming limitations of both. The paper proposes a biased denoising training objective with a clean single-transformer parameterization, and evaluates on synthetic planning tasks (star graphs, zebra puzzles) and text generation/infilling, showing clear advantages on structured planning tasks and competitive infilling results.

## Strengths
- **Star graph experiments cleanly isolate ILMs' structural advantage (Table 1, Section 5.1.1).** On variable-arm-length variants, ILMs achieve 100%/99.1% accuracy vs. ARMs (75.0/23.0) and MDMs (36.5/21.0). The mechanistic explanation — MDMs must predict absolute positions of the junction node in a single pass (equivalent to solving the problem), while ILMs build iteratively via relative positions — is convincing and supported by the generation trajectories in Figure 7.
- **Joint (position, token) parameterization is architecturally elegant (Eq. 3–4, Section 3.1).** Using position-wise unembedding with a single softmax over the full position×vocabulary product space avoids needing separate prediction heads, resulting in a simple and principled design.
- **ILMs demonstrate a genuine structural advantage for variable-length infilling (Table 3, Section 5.3.2).** Unlike MDMs, ILMs can fill an arbitrary number of tokens without knowing the fill length in advance. ILMs consistently outperform MDMs across all infilling setups (TinyStories single-segment, LM1B single- and multi-segment) on ΔNLL.
- **Comparison with the Insertion Transformer highlights the stopping mechanism's importance (Table 1).** IT scores 35.2/22.1/17.5 vs. ILM's 100/100/99.1, demonstrating that the dedicated stopping classifier is a key design choice, not merely an incremental add-on.
- **Zebra puzzle results (Table 1) show ILMs (90.0%) nearly match the oracle-ordered ARM (91.2%) without requiring oracle ordering**, outperforming both standard ARM (81.2%) and MDM (82.6%).

## Weaknesses

### Fatal
None

### Major
- **Biased training objective is under-analyzed (Section 3, Eq. 2).** The paper openly acknowledges using a biased objective that predicts normalized token counts per gap rather than marginalizing over insertion trajectories. At inference time (Algorithm 2), the model inserts tokens sequentially with changing context, creating a structural train-test mismatch: training teaches the model a bag-of-tokens distribution per gap, while inference requires sequential conditional decisions. No ablation compares biased vs. unbiased objectives even on small problems, no analysis characterizes how the bias scales with gap size *n*, and no theoretical bound on the approximation error is provided. The language modeling results (ILM trailing ARM) are consistent with this bias being harmful on natural language, but the paper offers no tools to disentangle the bias's effect from other factors (e.g., training token efficiency). This is the paper's central methodological choice, and the lack of any characterization of its cost is a significant gap.

- **Language modeling results do not support the "on par with ARMs" framing (Abstract vs. Table 2).** The abstract claims ILMs "perform on par with ARMs," but Table 2 shows: on Stories, NLL 2.14 vs. 2.11 (close); on LM1B, NLL 4.67 vs. 3.94 (~18% gap). ILMs also generate markedly shorter sequences (119 vs. 205 on Stories; 21 vs. 28 on LM1B) and exhibit lower entropy (3.76 vs. 4.06 on Stories; 2.80 vs. 3.12 on LM1B), indicating less lexical diversity. The paper itself partially acknowledges this in Section 5.3.1 ("both the MDM and the ILM obtain worse NLL compared to the ARM"), and the introduction more carefully uses "competitive," but the abstract's "on par" framing is not supported, particularly on LM1B. This is an overclaiming issue rather than a methodological flaw, but it affects how readers assess the contribution's scope.

### Minor
- **Stopping mechanism formulation appears incomplete as written (Eq. below Eq. 2).** The stopping loss gives the S=1 ("stop") signal only when **b** = **0** (the complete sequence is presented). However, *n* is sampled from U[L] = {1,…,L}, so n ≥ 1 and at least one token is always dropped, meaning **b** ≠ **0** always. As formulated, the classifier only receives "don't stop" training signal. The model does produce finite sequences in practice, so the implementation presumably handles this — but the paper's mathematical formulation is incomplete or unclear on this point, which matters because the too-short sequences in Table 2 suggest the stopping mechanism may be miscalibrated.

- **No variance estimates reported (Tables 1–3).** All results are point estimates without confidence intervals or multi-seed runs. For the planning tasks where ILM claims decisive advantage (e.g., 99.1% on Star_hard), mean±std would strengthen the claims against the possibility of lucky seeds.

- **Figure 6 inference speed comparison is asymmetric.** The ARM is compared "without KV cache," as noted in the figure itself. With KV caching, ARMs would be dramatically faster per token, making this comparison misleading for practical inference cost assessment. The paper acknowledges the KV cache limitation in Section 6, but the figure without this context could leave a misleading impression.

### Trivial
None

## Nice-to-Haves
- A small-scale ablation comparing the biased vs. unbiased training objective (e.g., on star graphs where shorter sequences make the unbiased estimator more tractable) would directly address the core methodological concern.
- Analysis of the stopping threshold's behavior and its relationship to the too-short sequences — even just plotting stopping probability as a function of sequence completeness would be informative.
- Visualization of learned generation orders on natural language text (analogous to the star graph trajectories in Figure 7) would show whether ILMs discover meaningful non-left-to-right orderings on text data.
- A modest scaling curve (loss vs. model size) would help assess viability beyond the 85M-parameter regime.
- Comparison against more recent MDM inference strategies (e.g., Campbell et al. 2024, Zheng et al. 2024) on the infilling task would contextualize the MDM baseline's performance.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Scalability concerns (demanding scaling analysis):** The reviewer noted all experiments use ~85M parameters with no scaling evidence. While true, the paper is introducing a new generation paradigm and demonstrating the concept at proof-of-concept scale. Demanding scaling curves goes beyond the paper's stated scope for an initial contribution. Moved to nice-to-have.
- **Missing wall-clock training time comparisons:** Nitpick about implementation-level details not standard for this type of contribution.
- **Request for human evaluation on infilling:** Would strengthen but is not standard practice for initial method proposals of this type. LLM-judge evaluation is a reasonable proxy.
- **Concern about IT hyperparameter fairness:** The reviewer asked whether the Insertion Transformer baseline was given a fair hyperparameter search. The paper describes using a comparable single-transformer setup, which is reasonable for a controlled comparison. Without evidence of unfairness, this concern is speculative.
- **Notation issues in Eq. 2 (missing explicit sum over v):** Likely a parser artifact per the hard rules; the intent of the equation is clear from context.

## Novel Insights
The paper's key novel insight is that relative-position insertion provides a fundamental advantage over absolute-position masking for variable-length structured generation. The star graph experiments provide clean mechanistic evidence: MDMs must predict absolute positions of critical nodes (e.g., junction nodes) in a single pass — which is essentially equivalent to solving the problem — while ILMs can build iteratively using relative positions. This insight generalizes beyond star graphs: whenever the output length is unknown and critical tokens have context-dependent absolute positions, insertion-based generation should be preferred over mask-based generation. The stopping mechanism's importance (demonstrated by comparison with the Insertion Transformer) is a secondary but useful practical insight.

## Suggestions
- Soften the abstract's "on par with ARMs" to "competitive with ARMs on shorter text and approaching ARM quality on LM1B" — this is supported by the data and more honest.
- Add a biased vs. unbiased objective ablation, even on a small task, to characterize the approximation cost.
- Clarify the stopping loss formulation — either show how n=0 is incorporated in practice or explain the extrapolation/generalization mechanism.
- Report mean±std over multiple seeds for at least the planning tasks (Tables 1) where the claim is decisive advantage.
- In Figure 6, add an ARM line with KV caching or explicitly annotate that practical ARM inference would be significantly faster.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to ILM paper |
|-------|------|-----------|-------|------------------------|
| Survey of LLMs | 8QTpYC4smR | 1.00 | R1 | Completely different — pure survey with no contribution. ILM paper is far stronger. |
| Cross-Lingual Humanoid Robots | gwZ90hFSL2 | 1.00 | R1 | Pseudoscience-adjacent. Not comparable. |
| IC-Light | u1cQYxRI1H | 10.00 | R1 | Different domain (vision); exceptional paper. ILM is below. |
| Financial Markets NN | nSDOkm0SKo | 1.00 | R1 | Extremely weak. Not comparable. |
| LLMs Self-Consuming | SaOxhcDCM3 | 3.20 | R1 | Analysis paper with methodological issues. ILM is stronger. |
| Inductive Transformers | NSBP7HzA5Z | 3.00 | R1 | Limited contribution and execution. ILM is clearly stronger. |
| AutoRegressive KB Completion | n87wrNlcJu | 3.00 | R1 | Different domain, weak baselines. ILM is stronger. |
| Reinforced Position Embedding | 5dDYhvt6dY | 3.00 | R1 | Incremental architecture change. ILM is substantially stronger. |
| **FiLM** | UbOzNf6hGq | **4.25** | R1 | Most directly comparable fill-in LM. FiLM was rejected for unfair comparisons, limited novelty, and narrow improvement. ILM has stronger synthetic demonstrations, cleaner architecture, and broader evaluation. ILM is clearly above. |
| Design Space of LMs for Images | zkMRmW3gcT | 4.80 | R1 | Different domain. |
| Path Selection NAR | 7jDv1RrNQX | 3.75 | R1 | NAR generation for BERT-like models. More incremental than ILM. |
| Extrapolative Seq Transformations | DQfHkEcUqV | 4.75 | R1 | Different approach (MCMC + AR). ILM has stronger planning demonstrations. |
| **SequenceMatch** | FJWT0692hw | **6.00** | R1 | Imitation learning for AR generation. Similar ambition level. ILM has comparable quality. |
| **COrAL** | 0JjsZC0w8x | **5.75** | R1,R2 | Order-agnostic LM. Similar ambition; rejected with mixed reviews (3,6,8,6). ILM has stronger synthetic results but similar LM limitations. Comparable quality. |
| **Energy-Based Diffusion LM** | sL2F9YCMXf | **6.75** | R1 | Stronger theoretical foundation and closer to matching ARMs. ILM is below. |
| **SEDD** | 71mqtQdKB9 | **6.60** | R1,R2 | Stronger theory (score entropy), competitive with GPT-2. ILM has weaker LM results but stronger planning demonstrations. Roughly comparable. |
| **SAD3-LM** | tyEyYT267x | **8.00** | R1 | Much stronger: comprehensive theory, variance analysis, SOTA results. ILM is clearly below. |
| **Think While You Generate** | MJNywBdSDy | **5.75** | R2 | Diffusion with planned denoising. Similar scope. Comparable quality. |
| **Beyond Autoregression** | NRYgUzSPZz | **6.25** | R2 | Most comparable: shows non-AR outperforms ARM on planning, ~85M params, limited NL evaluation. Accepted. ILM adds infilling capability but overclaims on LM results. Very similar quality. |
| DfPO | 6UQaXJm53B | 5.25 | R2 | Different topic (RL fine-tuning). |
| RADD | sMyXP8Tanm | 6.20 | R2 | Absorbing diffusion with clean formulation. Similar quality level. |
| Infilling Score | 9QPH1YQCMn | 6.25 | R2 | Different focus (data detection). |

**Round 1 bracket:** 5.0–7.0
**Round 2 narrowing:** 5.5–6.5

The ILM paper's planning results are its strongest suit and genuinely compelling (comparable to "Beyond Autoregression" at 6.25). The infilling capability is an additional real contribution. However, the overclaimed LM results (Major) and under-analyzed training approximation (Major) prevent it from reaching the upper end. The paper is comparable to "Beyond Autoregression" (6.25, accepted) but slightly weaker due to the overclaiming and the methodological gap around the biased objective.

**Final score: 6.0** — This is a borderline accept paper. It introduces a genuinely novel generation paradigm with clean demonstrations of where it shines (planning, infilling), but the language modeling story is weaker than framed, and the core training approximation needs more scrutiny. The planning contributions carry the paper.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>