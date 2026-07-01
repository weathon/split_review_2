## Summary

This paper introduces a framework for studying how language models learn probabilistic context-free grammars by decomposing them into "subgrammars" (inner subgrammars corresponding to compositional substructures, and outer subgrammars corresponding to simplified rule subsets). The authors prove theorems relating language modeling loss (KL-divergence) to subgrammar structure via a recursive decomposition, show empirically that small transformers learn all subgrammars concurrently ("in parallel"), explore curriculum learning via subgrammar pretraining with CKA-based representational analysis, and demonstrate that models struggle more with recursive depth than with sequence length.

## Strengths

- **The subgrammar decomposition framework is genuinely novel.** The idea of decomposing a CFG into inner subgrammars (subtrees of derivations) and outer subgrammars (simplified rule subsets), then studying how language modeling loss relates to this decomposition, is a fresh perspective that goes beyond prior work on static representational analysis (Allen-Zhu & Li, 2023) or aggregate learning curves (Cagnetta & Wyart, 2024). This direction has real potential to connect learning dynamics to internal compositional structure.

- **The depth-vs-length experiment (Section 6, Figure 3) is well-designed and produces a clean, interpretable result.** Comparing contexts `(a)^i` (depth 0, increasing length) vs `(^i` (depth i, increasing recursion) while keeping the ground-truth next-token distribution identical is a smart controlled design. The finding that prediction error rises with depth but stays flat with length is specific, reproducible-looking, and connects to broader questions about whether transformers genuinely learn recursive rules. This is the paper's strongest empirical contribution.

- **CKA-based representational analysis (Section 5.2, Table 1) with 30 random seeds** provides reasonable evidence that subgrammar pretraining changes internal representations, and the distinction between attention-layer and MLP-layer CKA is methodologically appropriate.

## Weaknesses

### Major

- **The mathematical derivation of the core theoretical claim is garbled and unverifiable from the main text.** The paper states this is its "most important contribution" (line 26), yet the transition from equation (3) to equation (4) (line 130) is mathematically incoherent: Eq (4) shows terms of the form `(log P)/(log Q)` — ratios of log-probabilities — which do not arise from any valid manipulation of a KL-divergence (which should yield `P log(P/Q)` terms). The denominator `log Q` in these fractions has no place in a KL decomposition. Furthermore, Definition 4.2 (line 136) uses `¬s` (`\neg s`) in the summation subscript `D_KL(P_G ‖ Q | ¬s)` without defining what `¬s` means, rendering the definition formally uninterpretable. Since Theorems 4.3, 4.5, and 4.6 build on this definition and on the decomposition claim, a reader cannot verify from the main text whether the stated results are valid.

- **The "parallel learning" claim is presented as a main empirical finding without a rigorous definition or quantitative test.** The abstract and introduction state that "small transformers learn subgrammars in parallel," but the evidence provided is that per-subgrammar KL curves (Figures 1, 2) all decrease over training. This is close to tautological — the same model is trained on the same data containing all subgrammars. The paper never defines what "not in parallel" would look like nor provides any null model or quantitative measure against which to compare. The informal Corollary 4.7 gestures at a theoretical condition for parallel learning but explicitly states it is a direction for future work, not a tested result.

- **The curriculum learning experiments (Section 5) lack essential control conditions.** The comparison is between "train from scratch on full grammar" and "pretrain on subgrammar, then train on full grammar." The second condition receives strictly more total gradient steps. Attributing improvement to the *structure* of subgrammar pretraining — rather than to longer training — requires baselines such as: (i) pretraining on a random subset of rules of matched size, (ii) training on the full grammar for the same total number of epochs, or (iii) pretraining on a different subgrammar of matched complexity. Without these, the claim that subgrammar structure specifically helps is unsubstantiated.

### Minor

- **The "context insensitivity" assumption underlying Corollary 4.5 and Theorem 4.6 receives only cursory empirical validation.** The paper acknowledges this is a "strong assumption" and claims experiments "suggest this condition is perhaps not so strong" (line 168), citing that "varying the prefix did not result in qualitatively different results." For an assumption central to the paper's most elegant theoretical results, a systematic evaluation (e.g., quantitative measurement of context-sensitivity across training, or testing multiple grammars) is needed to establish relevance to the models studied experimentally.

- **The paper overclaims in several places relative to the strength of the evidence.** The abstract and introduction describe the CKA analysis as showing "definitively" that pretraining results in more aligned representations (lines 9, 28), yet the absolute CKA differences are small (e.g., 0.281 vs 0.258 for 2-layer attention, a 0.023 difference; MLP layers show essentially no difference at -0.2%). Table 1 emphasizes percentage changes (+8.9%) without highlighting how modest the raw absolute differences are.

- **The variance/error bars in Figure 3 are not described in the main text.** It is unclear whether they represent standard deviation across seeds, across runs, or some other measure, and for how many seeds/runs.

### Trivial

None.

## Nice-to-Haves

- The GPT-5.1 anecdotes (Section 6, 5 examples each) are explicitly disclaimed as "purely anecdotal and should not be interpreted as direct evidence" (footnote 3). They add little and could be removed for conciseness; if kept, statistical testing with many more examples would be needed.
- The definitions of inner/outer subgrammars (Definitions 3.3, 3.5) could clarify how the start symbol is determined for inner subgrammars and how rules whose RHS contains non-terminals outside N' are handled, to avoid ambiguity about closure.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **"No training details provided in the main text"** (model sizes, optimizer, learning rate, etc.): Training details are standard to place in the appendix, which was stripped by the parser. Hard Rule 9.
2. **"Grammar definitions for all experiments are in the appendix"**: Removed per Hard Rule 9 (parser-stripped appendix content).
3. **"Theorem 4.1 proof in appendix, cannot evaluate"**: Removed per Hard Rule 9.
4. **"The relationship to Gruska (1971) is not explained"**: The paper notes the connection and provides it at the appropriate level of detail for a main text; the in-depth discussion is in the appendix. Scope creep.
5. **Various section-by-section notes** that restate points already captured above (e.g., the derivation issue, the definitional concerns) are merged into the existing weaknesses rather than listed separately.

## Novel Insights

None beyond the paper's own contributions. The subgrammar decomposition perspective and the depth-vs-length dissociation are the paper's own novel conceptual and empirical contributions; the reviews do not surface additional insights the paper itself misses.

## Suggestions

1. **Fix and clarify the mathematical exposition in Section 4.** Rewrite equations (1)–(4) with proper KL notation, define all notation in Definition 4.2 (resolve `¬s`), and provide a concrete worked example showing the sum-of-subgrammar-KL claim for a small 4-rule grammar. This is the single highest-leverage improvement and is necessary for the paper's core contribution to be verifiable.
2. **Define "parallel learning" quantitatively** and test it against a null model (e.g., compare the empirical joint improvement across subgrammars to independent improvement at random). This would turn an observational claim into a testable result.
3. **Add control conditions to the curriculum learning experiments** that match total training compute and rule-subset size, to isolate the effect of subgrammar *structure* from longer training.
4. **Calibrate the claims** — remove "definitively," qualify "parallel learning" — to match the strength of the evidence.
5. **Describe the error bars in Figure 3** (what measure, how many seeds) in the main text.

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>