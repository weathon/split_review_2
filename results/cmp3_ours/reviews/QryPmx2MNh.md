## Summary

This paper proposes a method to automatically discover learning-friendly output-token orderings for Transformers learning arithmetic tasks. The approach trains a small model on a mixture of permutations, uses early-training loss dynamics ("loss profiling") to rank orders, and employs a two-stage hierarchical search (global block-level + local intra-block) to manage the factorial search space. Experiments on three constructed arithmetic tasks and one multiplication task show the method can recover the known optimal order from billions of candidates.

## Strengths

- **Novel problem formulation.** Automatically finding a permutation of decoder outputs that minimizes learning difficulty is a genuine contribution. Prior work (Shen et al., 2023) showed output order matters but relied on heuristic choices; formalizing this as an optimization problem is a clear step forward. Section 1 and the first paragraph of Section 2 correctly situate this gap.

- **Clever loss profiling mechanism.** Using easy-to-hard learning dynamics (Arpit et al., 2017) to rank permutations by validation loss after brief training is intuitive and validated by a clean sanity check: Figure 5(a) shows the forward order cleanly separates from 127 random permutations, and Figure 5(b) confirms that higher-ranked orders yield higher success rates for ReLU and SQUARE-19.

- **Hierarchical search makes a factorial space tractable.** The two-stage design (global block-level + local intra-block) is a reasonable strategy for handling L! permutations. The reported 1–7 hour search time on a single GPU for up to ~6×10⁹ candidates (L=13) is a nontrivial practical achievement.

## Weaknesses

### Major

1. **No comparison to any alternative search method.** The paper introduces a new optimization problem but evaluates only one method against trivial baselines (forward, reverse, random orders). The only non-trivial alternative is a soft-permutation approach (Section 3, Figure 2) described qualitatively with no quantified comparison. Many alternatives exist—evolutionary search over permutations, greedy sequential construction, Bayesian optimization with permutation kernels, or brute-force for small L. Without any such comparisons, the reader cannot assess whether the proposed method is effective or merely adequate. This is the most consequential omission.

2. **No ablation studies.** The pipeline (global stage → local stage → loss profiling → candidate initialization) is treated as monolithic. There are no experiments isolating the contribution of any component. Does the global stage alone suffice for some L? Does the local stage consistently improve over global-stage results? How does the choice of initial candidate set affect the outcome? These questions are unanswered.

3. **The method fails on a non-trivial fraction of cases, understated by selective reporting.** From Table 2 (random initialization): the method does not recover the forward order for ReLU L=7, L=10, L=12; SQUARE-19 L=8, L=13; INDEX d=4, d=8. Figure 6(a) shows the discovered order for ReLU L=10 achieves only ~35% success rate. For INDEX with d=4 and d=8, the method simply fails (success rate "close to zero"). The paper states this in passing but the headline claim ("increasing the success rate from approximately 10% to 100%," abstract and line 23) is drawn from favorable cases and does not reflect the method's overall reliability. An honest accounting of success/failure across all tested configurations is needed.

4. **PROD/multiplication validation is confusingly framed.** The paper defines PROD's "forward order" as least-significant-digit (LSD) first (line 220). The method discovers the identity permutation [0,…,9], identifying LSD-first as the learning-friendly order. This is a valid positive result—the method correctly identifies the known optimal order for multiplication. However, the abstract and conclusion frame this as "rediscovered the reverse-digit order reported in prior studies" (line 9, line 23, line 328). Meanwhile, Figure 1 defines "forward order" as most-significant-digit first for the same task (contradicting the PROD definition), and Shen et al. (2023) used "reverse" to mean LSD-first. The terminology is internally inconsistent, and the framing overclaims what is essentially a sanity check on a known result.

5. **Method description is under-specified for reproducibility.** The paper does not explain how the block-level permutations Q_i (Eq. 4.2) and intra-block permutations R_i (Eq. 4.3) are generated. It says "we conceptually split each target sequence into k blocks" but does not specify whether blocks are contiguous, interleaved, or formed by another strategy. The candidate-generation procedure at each hierarchical level is unclear.

### Minor

6. **Unclear relationship between Table 2 and Figure 6.** For ReLU L=10, Table 2 lists a discovered final order [4,5,6,7,8,9,0,1,1,2,3] (with a formatting error: 11 elements for L=10 and a duplicate "1"), but Figure 6(a) shows only ~35% success rate at L=10. Is this success rate after retraining on the discovered order? If so, why is a 35%-success order considered "discovered"? The paper should clarify how the "discovered final order" is selected and how it relates to the reported success rates.

7. **No variance or error-bar reporting.** All success rates in Table 1 and Figure 6 are point estimates without error bars or discussion of stability across random seeds. Given that loss profiling depends on stochastic early-training dynamics, this is a limitation.

### Trivial

8. **Table 2 formatting error.** For ReLU L=10, the discovered final order [4,5,6,7,8,9,0,1,1,2,3] contains 11 elements for L=10 with a duplicate "1"—likely a typesetting error.

## Nice-to-Haves

- A task where multiple orders are feasible and the method discovers a genuinely non-obvious optimal ordering would significantly strengthen the claims beyond known-answer testing.
- Per-token loss analysis to understand why loss profiling works (does the model learn to ignore hard-to-predict tokens, or does gradient signal from easy-order samples dominate?).

## Removed Points

- **"The experimental validation is fundamentally circular"** (Harsh Critic Issue 1): The tasks are designed with a known ground truth—this is a standard known-answer evaluation paradigm, not circular reasoning. The scope limitation is valid but the framing was too strong.
- **"No analysis of loss-profiling mechanism"**, **"L up to 100 mentioned but not used"**, **"GPT-2 small/large terminology"**: These are either nice-to-haves, minor non-issues, or standard practice in the field. Not substantive weaknesses.
- Various formatting nitpicks and speculations about missing appendix content.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the gap between the paper's claims and the strength of its evidence, but do not identify unrecognized technical insights.

## Suggestions

1. Add comparison to at least one alternative search method (evolutionary search, greedy construction, etc.).
2. Add ablation studies isolating global stage, local stage, loss profiling, and initial candidate set.
3. Clarify the PROD terminology: state explicitly that the method recovers LSD-first ordering (the known optimal order for multiplication).
4. Specify how block-level and intra-block permutation candidates are generated.
5. Report success rates with variance across multiple runs or random seeds.
6. Fix the formatting error in Table 2 (ReLU L=10).
7. Explain the relationship between discovered orders (Table 2) and success rates (Figure 6).
8. Provide an honest accounting of success/failure across all (L, task) configurations rather than highlighting only favorable cases.

## Score and Decision

**Calibration procedure:** I retrieved anchors from a human-reviewed corpus across score bands, using queries about transformer arithmetic, chain-of-thought reasoning, and permutation search. The closest topical anchors were:
- "Positional Description Matters for Transformers Arithmetic" — avg 4.0, rejected. The current paper has a clearer scientific contribution (new problem + method) and is stronger.
- "How Capable Can a Transformer Become?" — avg 5.0, rejected (scores 3,6,3,8). The current paper has comparable evaluation depth but a more novel problem formulation; the contributions are roughly comparable.
- "From Interpolation to Extrapolation" — avg 5.5, rejected (scores 5,5,6,6). The current paper has a novel problem but weaker evaluation (no baselines, no ablations); the current paper is slightly weaker than this anchor.
- "Arithmetic Transformers Can Length-Generalize" — avg 6.5, accepted. Much stronger paper with theory + extensive ablations. The current paper is clearly weaker.

**Initial bracket:** 4.5–5.5 after Round 1. The paper has a genuinely novel problem formulation and clever method, placing it above the reject cluster of papers near 4.0. However, the significant evaluation gaps (no baselines, no ablations, partial failures, under-specified method) prevent it from reaching the 5.5–6.5 range.

**Final score:** 5.0 — a weak reject. The paper has a real contribution in the problem formulation and method design, but the evaluation is not yet rigorous enough to support the strength of the claims. The most critical missing elements are baseline comparisons and ablation studies, without which the method's effectiveness cannot be properly assessed.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>