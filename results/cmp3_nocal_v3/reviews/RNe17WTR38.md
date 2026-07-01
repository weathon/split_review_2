## Summary

This paper proposes a self-evolution framework where a single language model acts as both generator and verifier: it generates candidate solutions, uses thresholded majority voting to construct high-confidence preference pairs from its own noisy self-verification, and trains with DPO. Two variants are studied: SimpleGV (single-turn verification) and RevisionGV (multi-turn with iterative feedback). The method is evaluated on the synthetic Knights and Knaves (KK) benchmark and four math reasoning benchmarks (GSM8K, MATH500, MATHHard, TabMWP).

## Strengths

- **Clean, well-motivated framework.** The idea of using the same model as generator and verifier with thresholded majority voting to extract reliable signals from noisy self-assessment is conceptually elegant and clearly presented. The framework is simple enough to be reproducible and general enough to be extended.

- **Thorough exploration of design variants within the KK setting.** The paper systematically tests SimpleGV, RevisionGV, iterative training, curriculum learning, and analyzes effects of model size, data size, and cost trade-offs — all on the KK benchmark. Section 3.4 (Table 2) and Section 3.5 (Table 3) provide a well-structured ablation of how different design choices interact. This thoroughness within the KK setting is the paper's most rigorous contribution.

- **Easy-to-hard generalization finding.** Training on KK instances with 2–3 people transfers to 4–8 people (Table 2: 31.0% base → 44.1% after 3 iterations, with the hardest 6–8 subset improving from 10.3% to 19.7%). It is non-obvious that self-generated preference data from easy problems would improve performance on substantially harder problems where the model initially could not produce correct solutions at all. This is the paper's most novel empirical finding.

## Weaknesses

### Fatal

None.

### Major

1. **Missing test-time majority voting / self-consistency baseline.** The method generates k candidate responses per query, runs the verifier n times per candidate, applies thresholded voting to construct preference pairs, and trains with DPO. The natural baseline — simply applying majority voting (or self-consistency) at test time with k samples from the *base* model, without any training — is not evaluated. This baseline is critical because the training signal is essentially a filtered version of the model's own majority-vote judgments. If test-time majority voting already achieves the same or better accuracy, the DPO training pipeline would not be justified. As it stands, the reader cannot tell whether the contribution is genuine self-evolution or distillation of inference-time compute into weights (the paper evaluates with a single sample per query at test time, per line 94). This gap directly affects the paper's core claim.

2. **RevisionGV is only evaluated on the synthetic KK benchmark.** The multi-turn variant — positioned as a more sophisticated form of self-improvement (Section 4) — is evaluated exclusively on KK (Table 4). On the four math benchmarks (GSM8K, MATH500, MATHHard, TabMWP), where the community cares most about improvements and where SimpleGV already shows only modest gains (1–3 points), there are no RevisionGV results. Since the paper claims RevisionGV "outperforms SimpleGV" generally, the lack of evidence on realistic math benchmarks is a significant gap.

### Minor

3. **Framing gap between KK results and math results.** The abstract and introduction lead with the large KK gains (31% → 40.7%–44.8%) and state "similar improvements are observed across diverse mathematical reasoning benchmarks." In reality, the math benchmark gains are 1–3 points (Table 1), and GSM8K actually *decreases* for gemma-3-4b-it (89.2 → 89.0). While the abstract does qualify "For example, on the Knights and Knaves benchmark" (line 9), the overall framing inflates the perceived contribution by presenting the in-distribution KK results as the headline while the cross-distribution (OpenThoughts3 → math) results are substantially weaker. The paper would benefit from clearly separating these two experimental tracks.

4. **Missing simple SFT baseline on self-generated correct solutions.** Table 1 compares against INTUITOR, AZR, AZR-Coder, and GRPO, but does not include a simple supervised fine-tuning baseline where the model is trained on its own self-generated correct solutions (without DPO). Such a baseline would help disentangle whether the DPO signal or simply exposure to correct solutions drives improvement. The paper also does not compare against R-Zero or TTRL on the same benchmarks, though these are mentioned in the related work.

5. **Curriculum learning confound.** The curriculum experiment (Table 3) compares "KK23 w/ SimpleGV → KK45" (train on 2–3 people, then 4–5) against "KK2345 w/ SimpleGV" (random mix of 2–5 people). Because these conditions differ in both difficulty scheduling *and* data composition, the comparison does not cleanly isolate the effect of curriculum ordering. A baseline using all difficulties simultaneously (reordering the same data) would be more controlled.

6. **Table 1 vs. Table 2 training setup needs clearer exposition.** Table 1 trains on OpenThoughts3 (cross-distribution), while the large KK gains in Table 2 train on KK itself (in-distribution). This is described in the text but the distinction could be made more salient — a reader could easily assume the tables are contradictory.

7. **1B model analysis is shallow.** The paper notes that RevisionGV underperforms SimpleGV for the 1B model (line 288) but offers only a brief speculation about scaling trends without deeper analysis of why the pattern reverses.

### Trivial

8. **"Emergent" easy-to-hard generalization.** The paper uses "emergent" to describe positive transfer from easy to hard training. This is a well-studied curriculum learning phenomenon and the term "emergent" may overclaim without a discontinuity argument.

## Nice-to-Haves

- A supervised DPO upper bound on the math benchmarks (analogous to the KK oracle verifier in Table 2) would help calibrate how much of the gap to fully-supervised methods remains.
- The computational cost analysis (Section 3.6) would benefit from being contextualized against the inference cost of test-time majority voting at equivalent budgets.

## Removed Points

These points were raised in the input review but are removed with brief justification:

- **Abstract does not qualify KK numbers**: The abstract explicitly says "For example, on the Knights and Knaves benchmark" (line 9), so this specific claim is factually incorrect. The broader framing concern is retained as Weakness #3 above.
- **Section 2.1 OpenThoughts3 criticism**: The paper says OpenThoughts3 "includes problems that are not directly verifiable... highlighting the importance of a general and self-contained verifier" — this is motivation for the approach, not a claim that the method is evaluated on those problems. Strawman.
- **"gamma-34b-it" typo**: Parser/formatting artifact (should be "gemma-3-4b-it"). Removed per hard rules on formatting artifacts.
- **DPO hyperparameters not in main text**: The paper's appendix (stripped by parser) contains these details. Removed per hard rule about missing appendix content.
- **Limitations section should appear earlier**: Style preference, not a substantive weakness.
- **Computational cost not contextualized**: Section 3.6 does analyze cost trade-offs with n₁ and n₂ variation (Figure 5), so this claim is inaccurate.

## Novel Insights

The most interesting insight from the review process is the structural asymmetry between the paper's two evaluation tracks. The KK closed-loop setting (train on KK, test on KK) produces large, clean improvements that enable thorough ablation of design variants. The cross-distribution setting (OpenThoughts3 → math benchmarks) produces modest but directionally consistent gains. The paper's contributions are strongest when viewed through the lens of in-distribution self-evolution on a synthetic reasoning task — the easy-to-hard generalization, iterative DPO compounding, and curriculum learning results are the most novel findings. The weakest link is the absence of a test-time majority voting baseline, which would determine whether the DPO training step is doing real work beyond what inference-time compute already provides.

## Suggestions

1. **Run test-time majority voting / self-consistency** on the base model (without any training) on all five benchmarks, matching the inference budget used during training data generation. This is the single most informative missing experiment and directly addresses whether the DPO step adds value.
2. **Evaluate RevisionGV on at least one math benchmark** (GSM8K or MATH500) with the 4B model to support the claim that multi-turn verification broadly outperforms SimpleGV.
3. **Add an SFT-on-self-generated-correct-solutions baseline** to Table 1 to isolate whether DPO's preference signal matters beyond exposure to correct completions.
4. **Make the distinction between in-distribution (KK-trained) and cross-distribution (OpenThoughts3-trained) results explicit** in table captions and the abstract's framing.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>