Now let me write the final consolidated review.

## Summary

This paper introduces Insertion Language Models (ILMs), which generate sequences by inserting tokens one at a time at arbitrary positions, combining the variable-length capability of autoregressive models (ARMs) with the flexible generation order of masked diffusion models (MDMs). The authors propose a denoising training objective (with a bias to avoid high variance) and a transformer parameterization with a shared backbone for insertion and stopping decisions. On planning tasks (star graph path generation and Zebra puzzles), ILMs achieve large-margin improvements over both ARMs and MDMs. On text generation, ILMs are competitive with ARMs on the Stories dataset but underperform on LM1B, while outperforming MDMs overall.

## Strengths

- **Well-motivated problem formulation.** The paper clearly identifies two genuine limitations not simultaneously addressed by prior work: ARMs are constrained to left-to-right generation, and MDMs require fixed-length masks that prevent arbitrary-length infilling. ILMs address both by learning to insert tokens at arbitrary positions. This motivation is clearly laid out in Sections 1–2, and Figure 1 effectively contrasts the three approaches.

- **Strong results on planning tasks.** On Star_medium and Star_hard, ILM achieves 100% and 99.1% exact-match accuracy, compared to 36.5%/21.0% (MDM) and 75.0%/23.0% (ARM). On Zebra puzzles, ILM achieves 90.0% vs 82.6% (MDM) and 81.2% (ARM). These are clean, large-margin improvements on tasks that directly test the paper's central thesis — that out-of-order, position-flexible generation provides concrete advantages.

- **Elegant and architecturally simple training formulation.** The target insertion distribution in Equation (2) (normalized counts of tokens appearing between kept positions) avoids the high-variance marginalization over generation trajectories. Using a single transformer backbone with both an insertion head and a stopping head (Section 3.1) is practical and sensible.

## Weaknesses

### Fatal
None.

### Major

- **The biased training objective is acknowledged but never characterized.** The paper states (line 79) it uses a biased objective to avoid high variance: the model is trained to predict normalized counts of each vocabulary item between kept positions in the full original sequence. At inference, however, the model inserts one token at a time. The paper never addresses: (a) how large the bias actually is, (b) whether the sequential inference behavior corresponds to what the training objective optimizes, or (c) under what conditions the approximation breaks down. Without any characterization — not even synthetic or empirical — it is unclear whether the method's success on planning tasks will generalize to settings where token distributions are less structured. This is a structural gap in the method's justification.

- **Text generation claims overreach the evidence.** The abstract states ILMs "perform on par with ARMs and better than MDMs in unconditional text generation." On Stories, ILM NLL (2.14) is close to ARM (2.11), but on LM1B, ILM NLL (4.67) is 18.5% *worse* than ARM (3.94) — this is not "on par." The paper attributes the gap to "training token efficiency and scaling laws" without any analysis specific to LM1B. Additionally, ILM generates substantially shorter sequences than ground truth on both datasets (Stories: 119 tokens vs 205 gt; LM1B: 21 vs 28 gt), yet the paper offers no analysis of why the stopping classifier stops early or how this confound affects NLL comparisons. The limitations section acknowledges ILMs "perform slightly worse than ARMs" on text but does not mention the sequence length discrepancy.

- **No variance or error bars across any experiment.** Tables 1, 2, and 3 all report point estimates with no confidence intervals, standard deviations, or measures of statistical significance. Since generation involves stochastic sampling (nucleus, top-k, tau-leaping) and the Prometheus judge is a stochastic LLM, some claimed differences may not be significant. For example, the ILM–ARM NLL gap on Stories is only 0.03 (2.14 vs 2.11), and the gap between ILM (90.0) and ARMO (91.2) on Zebra puzzles is only 1.2 percentage points.

### Minor

- **Insertion Transformer (IT) baseline is only evaluated on planning tasks.** IT is absent from text generation and infilling experiments. The paper explains IT's poor performance as due to "using the EOS token instead of a dedicated stopping classifier," but without IT on text tasks it is impossible to tell whether ILM's text generation success comes from the new training objective, the stopping classifier, or both.

- **The infilling comparison against MDM on multi-segment infilling has limited value.** The paper's own critique is that MDMs cannot handle arbitrary infilling when the number of tokens is unknown in advance, yet the evaluation compares ILM against MDM on multi-segment infilling. The MDM can attempt the task when segment lengths are provided, but the comparison is inherently asymmetric. A non-MDM baseline (e.g., fill-in-the-middle ARMs) would strengthen this evaluation.

### Trivial

- **Figure 6 is confusing.** The caption says it compares MDM and ILM, the figure description mentions ARM (w/o KV cache) as well, and the NLL values in the figure (~3 for MDM, ~1.5 for ARM/ILM) do not match Table 2 values (MDM 2.54, ARM 2.11, ILM 2.14 on Stories), suggesting different experimental conditions that are not explained.

## Nice-to-Haves

- A synthetic experiment comparing the biased training objective against the unbiased (high-variance) Monte Carlo objective on a small controlled problem would clarify when the approximation is reliable.
- Evaluating IT on text tasks, or at minimum discussing why the comparison was omitted.
- Analysis of the stopping classifier's calibration: why does it stop so early on text? Can a post-hoc threshold adjustment fix the length discrepancy?
- A discussion of the conditions under which the training bias might cause the model to fail.

## Removed Points

- **MDM entropy/length claim (factually incorrect):** The critic claimed MDM generates sequences "closer to data statistics" on entropy and length. Verifying from Table 2: on LM1B, data entropy = 3.08, ILM = 2.80 (|diff| = 0.28), MDM = 3.70 (|diff| = 0.62); data mean length = 28, ILM = 21 (|diff| = 7), MDM = 85 (|diff| = 57). ILM is strictly closer on both metrics. Removed as factually wrong.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the need for a characterization of the training bias and more honest framing of text results, but these are corrective observations rather than novel insights.

## Suggestions

1. Include at minimum a qualitative/empirical analysis of the biased training objective (e.g., a small-scale comparison with the unbiased Monte Carlo objective).
2. Add error bars (multiple seeds or bootstrapped confidence intervals) to all quantitative results.
3. Analyze the stopping classifier's calibration: why does it stop early on text, and can a threshold adjustment fix the length discrepancy?
4. Reframe text generation claims to match the evidence: "competitive with ARMs on structured short-form text (Stories) but underperforms on more diverse data (LM1B)" rather than "on par with ARMs."
5. Clarify the experimental conditions for Figure 6 so the NLL values can be reconciled with Table 2.
6. Evaluate IT on text tasks, or add a discussion explaining the omission.

## Score and Decision

This paper presents a genuinely novel and well-motivated approach to sequence generation. The planning results decisively validate the core thesis — ILM's out-of-order, position-flexible generation outperforms both ARMs and MDMs on tasks where the failure modes of those paradigms are most acute. The training formulation is elegant and the architecture is simple. However, the paper has three weaknesses that require attention: (1) the biased training objective is acknowledged but never characterized, which is a structural gap; (2) the text generation claims in the abstract overreach the evidence, particularly on LM1B; and (3) no error bars are reported anywhere. None of these issues is fatal — the planning results alone constitute a genuine contribution — but they must be addressed. With honest reframing of the text claims, added error bars, and at least a qualitative discussion of the training bias, this would be a solid paper. In its current form it is a **borderline accept**.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>