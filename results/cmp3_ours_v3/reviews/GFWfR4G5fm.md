Now let me compile the final review with all verified cross-checks and the calibrated score.

## Summary

This paper identifies three limitations of static supervised causal learning (SCL) pre-training — fragility to distribution shifts, failure in compositional generalization, and a gap between synthetic and real-world performance — and proposes TTT-SCL, a framework that dynamically generates training data aligned with each test instance. The method is instantiated as TACTIC, which uses an Alignment of Distribution (AD) metric with sparsity constraints to search over candidate graphs and construct a customized training set for each test instance. Experiments on synthetic, pseudo-real, and real-world datasets show TACTIC outperforming existing methods, particularly on the real-world Sachs dataset (78.9 AUROC vs. AVICI's 62.3).

## Strengths

1. **Well-motivated problem diagnosis (Section 3).** The paper systematically documents three failure modes of static SCL pre-training with concrete evidence in Figure 2 and Table 1. This diagnosis is thorough, well-designed, and useful independently of the proposed method — it makes a genuine contribution to the field's understanding of SCL limitations.

2. **Conceptually novel framing.** The "diversity vs. concentration" framing (introduction) cleanly articulates an inherent limitation of static pre-training: you cannot exhaustively cover all possible SCMs, and models appear to memorize configurations rather than learn modular causal representations. The idea of test-time training as an alternative to ever-larger synthetic pre-training is a genuinely new direction for SCL.

3. **Stage-wise analysis (Table 4).** Decomposing performance into seed graph → best search graph → final SCL output cleanly separates the contributions of TACTIC's search procedure from the supervised learning phase. This analysis convincingly demonstrates that both stages contribute meaningfully to the final result.

## Weaknesses

### Fatal
None.

### Major

1. **The SCL model training protocol at test time is critically underspecified.** The paper states "An SCL model is then trained on this set" (Section 4.2, step 3) and "We mainly use the AVICI as the model backbone" (Section 3.1), but never specifies whether the model is trained **from scratch** on the 200 dynamically generated instances or **fine-tuned** from a pre-trained checkpoint (such as the AVICI scm-v0 model used as a baseline). All training hyperparameters (learning rate, batch size, number of epochs, optimizer, regularization) are omitted. This is a structural gap: if TACTIC fine-tunes a pre-trained AVICI, the comparison in Table 2 is between a pre-trained model applied directly and the same model after additional test-time compute — the improvement could partly reflect the extra compute, not the quality of the generated training data. If it trains from scratch, the claim that 200 instances suffice for a deep transformer is extraordinary and would require extensive validation. Either way, the results as reported cannot be properly interpreted or reproduced.

2. **Missing statistical uncertainty on real-world results.** Results for Sachs and Syntren in Tables 1, 2, and 3 are reported as point estimates without standard deviations, while synthetic results include them. Given that the paper's central motivation (Issue 3) is precisely the synthetic-to-real generalization gap, this omission makes it impossible to assess whether the reported improvements on real data (e.g., TACTIC 78.9 vs. AVICI 62.3 on Sachs) are statistically meaningful or could be within the noise of a single run.

### Minor

1. **The stochastic graph refinement procedure has a text/figure inconsistency and missing details.** Section 4.2 says candidates are "accepted with probability proportional to its score," but Figure 3 shows α = min[1, score(G_{k+1})/score(G_k)] — the standard Metropolis ratio, which is different from "proportional to its score." Additionally, the number of refinement iterations and how the K=200 final graphs are selected from the chain are not stated in the main text. This makes the search procedure harder to follow than it should be.

2. **The learning improvement mechanism (stage 2→3 in Table 4) lacks analysis.** On Sachs, the best graph found by search has AUROC 66.6, but the SCL model trained on data generated from that search outputs AUROC 78.9. The paper calls this "the crucial advantage of our approach" but provides no analysis of how training on ~66.6-AUROC graphs produces a 78.9-AUROC output. This is the most interesting scientific question raised by the paper and is left entirely unanswered.

3. **TACTIC (random) underperforms the static baseline on Sachs (58.6 vs. AVICI's 62.3).** This reveals that the method's success depends substantially on the NOTEARS initialization. While Table 4 shows that TACTIC-Notears substantially improves beyond the NOTEARS seed (61.8 → 78.9), the random variant's failure to match even the static pre-trained baseline is a practical limitation that should be acknowledged more prominently.

4. **The "state-of-the-art" claim on Chebyshev_G is overstated.** TACTIC-Notears achieves 83.0 vs. AVICI's 81.7 on Chebyshev_G, but with a standard deviation of 8.7 (TACTIC) vs. 10.5 (AVICI), this difference is well within one standard deviation and likely not statistically significant. The paper's phrasing — "state-of-the-art performance on all other datasets" — overstates the result for this dataset.

5. **Naming inconsistency in Figure 2.** The text in Section 3.1 describes test settings as "RFF.G.ER" and "RFF.G.SF," but Figure 2's table labels them "RFF_G_62.3" and "RFF_G_97.8." The numbers 62.3/97.8 (which may refer to graph sparsity) are not explained in the main text, making the figure less self-contained than it should be.

### Trivial
None.

## Nice-to-Haves

- Provide an analysis of why the SCL model improves on its training labels (the 66.6→78.9 jump on Sachs). This could involve ablating the training set size, analyzing which edges the model corrects, or comparing the model's predictions to the training graphs.
- Add a baseline that applies NOTEARS with different regularization strengths or post-processing to further isolate whether TACTIC's improvement over NOTEARS comes from the SCL model or from better use of NOTEARS.
- Report the value of λ (sparsity penalty weight) and describe how it was selected.
- Acknowledge the computational cost asymmetry between TACTIC and a single forward pass of AVICI, and discuss practical viability.

## Removed Points

These points were raised in the input review but are removed for the following reasons:

- **"The AD metric has unstated implementation assumptions"** — REMOVED: The paper explicitly defers AD implementation details to Appendix A, which was stripped by the parser. The main text provides the core formulation, which is standard for the venue.
- **"Issues 1 and 2 (distribution shift vs. compositional generalization) are not distinct"** — REMOVED: The paper's framing is reasonable; the Component-mixed setting in Figure 2 shows a distinct pattern from individual shifts and tests a different failure mode.
- **"The claim of generality is overstated"** — REMOVED: The paper makes a framework-level claim about TTT-SCL, not about the specific AD implementation, and the list of identifiable SCM classes is appropriate for a framework paper.
- **"Missing 'to' in line 152"** — REMOVED: Formatting/typographical nitpick, not present in the original submission.
- **"TACTIC (random) vs. AVICI conflates NOTEARS contribution"** — REMOVED (stronger version): The critic claimed the comparison "conflates the contribution of NOTEARS with the contribution of TACTIC's own components," but Table 4 shows TACTIC-Notears (78.9) substantially outperforming NOTEARS alone (61.8), directly refuting that claim. A watered-down version is retained as Minor #3.

## Novel Insights

The interaction between Weaknesses 1 and 2 (Major) is interesting: if TACTIC fine-tunes a pre-trained AVICI, then the unexplained 66.6→78.9 jump on Sachs could be a result of the pre-trained model's strong prior being productively guided by the 200 fine-tuning instances — which would actually validate the paper's core thesis (test-time adaptation helps) while simultaneously undermining the claim that static pre-training is the problem. Conversely, if trained from scratch, the 66.6→78.9 jump is genuinely puzzling and would demand a deeper explanation. The paper's silence on this point is its most consequential gap because resolving it would either strengthen or dramatically weaken the central argument.

## Suggestions

1. **Specify the training protocol.** State clearly whether the SCL model at test time is trained from scratch or fine-tuned from a pre-trained checkpoint. Provide all training hyperparameters: learning rate, batch size, number of epochs, optimizer, regularization, and any learning rate schedule.
2. **Add error bars on real-world results.** Report standard deviations for Sachs and Syntren (e.g., by repeating TACTIC with different random seeds or bootstrapping the test data).
3. **Resolve the text/figure inconsistency** between "accepted with probability proportional to its score" (Section 4.2) and the Metropolis ratio shown in Figure 3. Clarify the number of iterations and how K=200 graphs are selected.
4. **Provide an analysis of the learning improvement mechanism** — what enables the SCL model to outperform its own training labels? This would substantially strengthen the paper.
5. **Acknowledge the NOTEARS-dependence issue** more prominently and report TACTIC (random) results in the main comparison table with a clear discussion.
6. **Tone down the "state-of-the-art" claim on Chebyshev_G** given the overlapping error bars.
7. **Report the λ value** used for the sparsity penalty and describe the selection procedure.

---

**Calibration report:**

*Round 1 bracket:* 4.0–6.0

| Anchor paper | Path | Avg human score | Round | Comparison |
|---|---|---|---|---|
| Demystifying amortized causal discovery with transformers | lQYi2zeDyh.md | 5.00 | R1, R2 | Closest topic (SCL generalization analysis). The under-review paper has more empirical scope (real data, multivariate) and a novel method, but the "Demystifying" paper had no comparable methodological omissions. |
| Causal Structure Learning Supervised by LLM | JzFLBOFMZ2.md | 3.20 | R1 | Less rigorous, more significant methodological issues. The under-review paper is substantially stronger in execution and evaluation. |
| Zero-Shot Learning of Causal Models | x3F8oPxKV2.md | 6.25 | R1, R2 | Similar amortized/zero-shot setup but different task (SCM inference vs. causal discovery). Stronger theoretical framing but also had reproducibility gaps. |
| On the OOD Generalization of SSL | 22ywev7zMt.md | 5.67 | R2 | Related topic (OOD generalization + causal models). The under-review paper has more empirical evaluation on real data. |
| Fine-Tuning PLMs for Robust Causal Representation Learning | tlH4vDii0E.md | 5.60 | R2 | Similar theme (adaptation for causal robustness). The under-review paper proposes a more novel framework for SCL specifically. |

*Narrowing:* The closest comparison is the "Demystifying" paper (5.00, Reject), which was criticized for limited scope (bivariate only, synthetic only). The under-review paper addresses those scope limitations but has a more significant methodological gap (underspecified training protocol). The "Zero-Shot Learning" paper (6.25, Reject) had stronger theoretical foundations and was still rejected. Given these anchors, the paper sits below the acceptance threshold due to the unresolved major weakness about training protocol.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>