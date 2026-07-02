Thank you for the information. Let me now compile the final review.

## Summary

The paper introduces Insertion Language Models (ILMs), which learn to insert tokens one at a time at arbitrary positions in a sequence. This addresses limitations of both autoregressive models (fixed left-to-right order) and masked diffusion models (simultaneous unmasking violating dependencies, fixed mask count preventing arbitrary-length infilling). The method uses a denoising objective where tokens are dropped (not masked), a transformer parameterization that outputs insertion logits, and a learned stopping classifier. Evaluation on planning tasks (star graphs, zebra puzzles) shows ILMs convincingly outperforming both ARMs and MDMs; on text generation and infilling the results are mixed—competitive on Stories but significantly behind ARMs on LM1B.

## Strengths

1. **Well-motivated design that directly addresses concrete limitations.** The paper articulates specific, identifiable problems with both ARMs (fixed generation order) and MDMs (simultaneous unmasking violating token dependencies, fixed mask count preventing arbitrary infilling) and designs ILMs to address them. The "chef added sugar" example (line 40) and the "conference mask was postponed" example (line 46) give intuitive, concrete illustrations of each failure mode.

2. **Strong synthetic-task evidence isolates the claimed capabilities.** The star graph experiments (Section 5.1.1) use three difficulty levels varying arm symmetry and length. ILM achieves 99–100% across all levels while MDM drops from 100% (easy) to 21% (hard) and ARM (non-oracle order) drops to 23% (hard). This controlled setup cleanly separates competing hypotheses about model capability—the contrast between `Star_easy` (all models perfect) and `Star_medium`/`Star_hard` (ILM stays near 100%, others collapse) directly supports the paper's diagnosis of MDM's variable-length limitation.

3. **Zebra puzzle result is a clear win on a nontrivial task.** ILM's 90.0% exact-match accuracy approaches the oracle-order ARM (91.2%) and substantially exceeds MDM (82.6%) and ARM (81.2%) on a constraint-satisfaction problem where the output must simultaneously satisfy multiple interacting constraints (Table 1).

4. **Honest limitations section.** The paper explicitly acknowledges that ILMs underperform ARMs on text NLL, cannot use KV caching, and that scaling is future work (Section 6). This transparency helps readers calibrate the scope of the claims.

## Weaknesses

### Fatal
None.

### Major

1. **Training objective bias is acknowledged but never characterized.** The paper states that the "naive infilling denoising objective can have extremely high variance" and that to avoid this they "use a biased training objective" (lines 78–79). The training loss in Eq. (2) trains the model to predict aggregate normalized token counts from a single corrupted view of the sequence. The inference procedure (Algorithm 2) inserts one token at a time. The nature, severity, and consequences of this bias are not analyzed anywhere in the main paper. For a paper whose primary contribution is a new training method, leaving the central training objective's properties unexamined is a significant gap—readers cannot tell whether the method is principled or a heuristic that happens to work on these particular tasks.

2. **The "on par with ARMs" claim is overstated for text generation.** The abstract claims ILMs "perform on par with ARMs" in unconditional text generation. From Table 2, on LM1B the gap is 0.73 nats/token (ARM: 3.94, ILM: 4.67)—a substantial difference for an 85M-parameter model. Only on Stories is the gap small (0.03 nats). The ILM also produces shorter sequences (21 vs 28 mean length on LM1B) and lower entropy. The claim should be qualified to reflect dataset-dependent performance.

3. **MDM baseline uses the weakest sampler, excluding variants that address the paper's central critique.** The paper's core criticism of MDMs is simultaneous unmasking. Yet the MDM baseline uses the basic tau-leaping sampler with a log-linear noise schedule (Section 5.3.1), while the paper itself cites Gong et al. (2024), Zheng et al. (2024), and Campbell et al. (2024) as addressing this limitation through greedy/top-k/flow-based sampling (lines 125–126). Including these stronger MDM variants would determine whether ILM's advantage stems from its model design or merely from using a better sampling strategy.

### Minor

4. **No variance or statistical significance reported.** All tables present point estimates without standard deviations, confidence intervals, or mention of multiple runs. While the star graph results are decisive enough that variance likely doesn't change the conclusion, the text generation (Table 2) and infilling (Table 3) results have modest gaps where readers need some sense of reliability.

5. **Infilling evaluation relies on indirect NLL-based metrics.** The infilling experiment (Table 3) uses only percentage changes in NLL and entropy. These do not directly measure whether the infilled content is semantically appropriate. The differences between ILM and MDM are modest (e.g., LM1B multi-segment ΔNLL_gt: ILM +23.52 vs MDM +25.64), and without human evaluation or task-specific accuracy, it is unclear whether the metric gaps correspond to practically meaningful quality differences.

### Trivial

6. **Figure 6 description inconsistency.** The text at line 215 refers to MDM (red) and ILM (blue), while the figure description at lines 221–223 refers to MDM (red), ARM (blue), and ILM (green). The legend colors and which models are shown should be aligned.

7. **Insertion Transformer baseline included only on synthetic tasks.** The IT baseline (Stern et al., 2019), the most directly related prior insertion-based method, is evaluated only on star graphs (where it scores 17.5–35.2%). Including IT on text tasks would sharpen the comparison.

## Nice-to-Haves

- A small-scale human evaluation or human-LLM correlation analysis for text generation quality would strengthen the qualitative claims.
- Analysis of the stopping classifier's behavior and accuracy, given that it controls sequence length and the observed length mismatches (ILM produces sequences substantially shorter than data averages).
- A characterization of the conditions under which the training objective's bias is small vs. large (e.g., as a function of gap size or vocabulary sparsity).

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Criticism about missing appendix content (Issue 1, parts referencing Appendix D):** The harsh critic noted that "The appendix (D) is referenced for 'more details' but is not available for review." Per hard rules, missing appendix content is a parser artifact and should not be penalized. The retained criticism focuses on what is absent from the main paper's analysis of the training bias, not on what may or may not exist in the appendix.

- **Criticism that the IT comparison should note IT was designed for text, not graphs:** This is a reasonable observation but elevates a framing nuance to a weakness; it is a trivial concern that does not affect the validity of the star graph comparison.

- **Criticism about relative position encoding advantage:** The harsh critic argued that both ILMs and MDMs use RoPE, so the claimed "relative position" advantage is misleading. The paper's claim (line 147) is that ILM "utilizes relative positions to solve the task iteratively"—the advantage is in the *combination* of iterative generation with relative positions. Both models use RoPE, so this is not a meaningful distinction and the criticism is over-interpreted.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Characterize the training objective bias.** Provide either a theoretical analysis (e.g., showing Eq. (2) corresponds to an upper bound or approximate posterior) or an empirical diagnosis on a small controlled task comparing the biased objective against a Monte Carlo estimate of the true marginalization objective.
2. **Qualify the "on par with ARMs" claim** to reflect the LM1B gap.
3. **Include MDM baselines using greedy/top-k sequential unmasking** (Gong et al., Zheng et al., or Campbell et al.) to isolate the source of ILM's advantage.
4. **Report confidence intervals or multiple-run statistics** for text and infilling results.
5. **Add Insertion Transformer results on text tasks** to validate the specific ILM design choices.

## Score and Decision

**Calibration anchors:** All papers from `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/`:

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| FiLM: Fill-in Language Models (UbOzNf6hGq) | 4.25 | R1 (3.5–5.5) | Similar topic (any-order generation) but substantially weaker method and evaluation; ILM has stronger planning results and more comprehensive experiments |
| COrAL: Order-Agnostic Language Modeling (0JjsZC0w8x) | 5.75 | R1 (5.5–7.5) | Similar theme of order-agnostic generation but applied to LLM refinement; ILM has stronger methodological novelty |
| Beyond Autoregression: Discrete Diffusion (NRYgUzSPZz) | 6.25 | Narrow (5.0–7.0) | Most comparable—both address AR limitations for planning, both have strong synthetic results, both have limited real-world scope; ILM additionally has text generation but has an uncharacterized training bias |
| PlaSma: Procedural Knowledge Models (dFcXJgnrGB) | 6.50 | Narrow (5.0–7.0) | Planning-focused; accepted at ICLR; ILM has comparable planning evidence plus text results |
| Tree-Planner (Glcsog6zOe) | 5.25 | Narrow (5.0–7.0) | Planning with LLMs, different domain; accepted despite score |

**Round-1 bracket:** The paper sits between 5.0 and 7.0 given that it is substantially stronger than FiLM (4.25) and comparable to Beyond Autoregression (6.25, Accept) and PlaSma (6.50, Accept).

**Round-2 narrowing:** Compared to Beyond Autoregression (6.25), the ILM paper has a more significant methodological concern (uncharacterized training bias) but broader evaluation (text + planning + infilling versus only planning). The paper is accept-worthy in the borderline range.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>