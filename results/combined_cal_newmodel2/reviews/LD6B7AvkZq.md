Now I have all the information I need. Let me write the final consolidated review.

**Calibration summary.** I retrieved anchors across all score bands (strong-reject through accept). Most relevant: `uOnElfFuey.md` (avg 3.00, "Recovering Knowledge by Hardening Language Models") — a paper about extracting DFAs from LMs trained on formal languages with a working method but limited novelty; `F0Zd3knG9j.md` (avg 5.00, "How transformers learn structured data") — a PCFG-based study of hierarchical filtering with clearer methodology but overlapping prior work; `eRkNNQRppH.md` (avg 3.50, "Pre-training Dynamics with FOL") — a paper about learning dynamics on formal structures with a dataset contribution but unclear findings; `fp77Ln5Hcc.md` (avg 4.50, "Depth Extrapolation of Decoders") — a paper about depth generalization in nested structures with an interesting theoretical construction. The paper under review sits below all of these because it has verifiable mathematical errors (equation (4) uses log ratios instead of log differences for KL divergence; Definition 4.2 uses undefined notation and is structurally incoherent) that the anchor papers at ≥3.0 do not have. **Round-1 bracket: [1.5, 4.5].** Round‑2 narrowed to [2.5, 3.5] by comparing against `uOnElfFuey.md` (3.00) and `eRkNNQRppH.md` (3.50): our paper has a verifiable mathematical error that neither anchor has, placing it below the 3.00 anchor. Final score: **3.0**.

---

## Summary

This paper studies how small transformers learn probabilistic context-free grammars (PCFGs) through the lens of "subgrammar" structure. It introduces definitions of inner and outer subgrammars, claims theoretical results showing that KL divergence decomposes recursively over subgrammar structure, and presents empirical results on parallel learning (all subgrammars learned simultaneously), curriculum learning via subgrammar pretraining, CKA-based representation analysis, and depth-vs-length generalization. The subgrammar definitions and controlled experimental setup are promising directions, but the paper's core theoretical contribution contains verifiable mathematical errors, and the main empirical findings are either unsurprising consequences of training on the full distribution or replications of known results from prior work.

## Strengths

- **Novel subgrammar definitions (Def. 3.3–3.5).** The paper introduces clean, well-motivated formal definitions of inner subgrammars (subtrees of derivations) and outer subgrammars (rule subsets). These provide a useful vocabulary for discussing substructure in CFGs and are a genuine conceptual contribution. [favorability=12.39]

- **Clean controlled experimental paradigm.** Training small transformers on fully-specified small PCFGs where ground-truth distributions are known enables exact computation of subgrammar-level KL divergences. This setup is well-suited for studying learning dynamics and contrasts with work that only probes trained models on natural language with unknown underlying structure. [favorability=12.14]

- **CKA-based representation analysis (Section 5.2, Table 1).** The attempt to look beyond loss curves at internal representations — showing that subgrammar pretraining leads to measurably different (more aligned) internal representations — is a welcome addition and the kind of analysis that could grow into a deeper contribution with more rigorous treatment. [favorability=11.61]

- **Curriculum learning results.** The finding that pretraining on a subgrammar can yield lower final loss for small (2-layer) transformers, and that this benefit is robust to subgrammar position (prefix/suffix/infix), is the most empirically interesting result in the paper, though the effect is modest and disappears for larger models. [favorability=12.59]

## Weaknesses

### Fatal

- **Equation (4) is mathematically incorrect.** The paper's core theoretical derivation (Section 4.2) writes KL divergence terms as ratios of log probabilities (log P / log Q) instead of differences (log P − log Q). KL divergence is defined as Σ P(s)[log P(s) − log Q(s)], not Σ P(s) · (log P(s) / log Q(s)). The paper's characterization as "an abuse of notation" does not resolve the error — dividing logs instead of subtracting them produces a fundamentally different quantity. Since the paper explicitly calls this derivation its "most important contribution" (Section 4, line 26), this error undermines the central theoretical claim as presented in the main text. [favorability=-1.65]

- **Definition 4.2 uses undefined notation and is structurally incoherent.** The restricted KL term D_KL(P_G ∥ Q)_A is defined using the notation "D_KL(P_G ∥ Q | ¬s)," which is never defined anywhere in the paper. Moreover, the definition sums over contexts s ∈ Σ* and then over a ∈ Σ*, but the innermost term does not depend on the summation index a. Without a clear, self-consistent definition, the core technical apparatus for the theoretical claims cannot be evaluated. [favorability=-1.49]

### Major

- **Theoretical novelty is substantially overstated.** The claim that KL divergence decomposes recursively over subgrammar structure (Theorem 4.3, Corollary 4.5, Theorem 4.6) is largely a restatement of the standard autoregressive chain rule for KL divergence — a basic probability identity that holds for *any* autoregressive distribution, not specifically for CFGs. Theorem 4.6's geometric-series formula follows directly from the expected recursion depth in a branching process and is a known property of PCFGs, not a discovery about how neural networks learn them. The paper's framing of these as "fundamental theorems" about CFG learning far exceeds what the mathematical content supports. [favorability=-4.68]

- **The "parallel learning" result is an unsurprising consequence of training on the full distribution.** Since the model is trained on samples from the full PCFG, every batch contains strings from all subgrammars, and the total loss decomposes as a sum over subgrammar terms (Theorem 4.3), gradient descent naturally reduces all terms simultaneously absent strong negative interference. Corollary 4.7 states that if optimizing on one subgrammar does not hurt others, then all improve — which is the definition of "no negative interference" restated as a conclusion. The claimed contrast with child language acquisition is asserted without specific supporting evidence. [favorability=-3.04]

- **The depth-vs-length generalization experiments (Section 6) replicate known findings.** The paper itself cites Bhattamishra et al. (2020), Lampinen (2024), and Hahn (2020) as showing that transformers struggle with recursion and long-range dependencies. Demonstrating this again in a controlled PCFG setting is a clean validation but does not constitute a novel discovery about CFG learning dynamics, as the framing suggests. [favorability=-4.10]

- **The main text lacks essential experimental details.** There is no specification of model architecture beyond "2-layer transformer" and "4-layer transformer" (number of heads, embedding dimension), no training hyperparameters (learning rate, optimizer, batch size, number of steps), and no dataset sizes or data generation procedures. While some of these may reside in the appendix (stripped by the parser), a reader should be able to understand the experimental setup from the main text without cross-referencing supplementary material. [favorability=-2.30]

### Minor

- **Figure 1 lacks error bars or uncertainty measures.** The core empirical validation of the theoretical decomposition (Figure 1) shows KL divergence curves without any measure of variance across the 30 random seeds. Without this, it is impossible to assess whether the reported decomposition is statistically robust. (Figure 3 does include variance shading, so this is not a uniform issue.) [favorability=2.73]

- **CKA results (Table 1) lack significance measures and show mixed evidence.** Attention-layer alignment increases with pretraining (+8.9% to +21.7%), but MLP layers show negligible or negative changes (−0.2% to −4.7%). No statistical significance measures are provided, and the negative MLP results weaken the claim that pretraining meaningfully improves representation alignment. [favorability=0.80]

### Trivial

None.

## Nice-to-Haves

- If the theoretical contribution is to be retained, the authors should make precise what property of CFGs (not shared by arbitrary autoregressive distributions) makes the subgrammar decomposition non-trivial. The "context insensitivity" condition (Corollary 4.5) deserves rigorous treatment — either a proof that small transformers satisfy it approximately, or a characterization of the error term.
- A controlled baseline for the parallel learning result would strengthen the claim: for example, show what non-parallel learning looks like (a multi-task setup where different subgrammars are trained on disjoint data).

## Removed Points

These points from the input review were removed per meta-reviewer guidelines:

- **Criticism about Evanson et al. (2023) showing "sequential mastery, the opposite of what this paper claims":** REMOVED. The paper cites Evanson et al. as showing that GPT-2 exhibited developmental stages reminiscent of child language acquisition. The critic's characterization of what Evanson et al. "actually showed" is an interpretation not verifiable from the paper alone; the paper's contrast with children is a valid framing even if the relation to GPT-2 is debatable.
- **Criticism about missing figures and tables (Figures 5, 6, Table 3) and grammar specifications:** REMOVED. The parser stripped all appendix content (line 305). These materials exist in the original submission; the meta-reviewer rules forbid penalizing the paper for absent appendix content caused by the extraction pipeline.
- **"Definition 4.2 fix — notation must be properly defined":** MERGED into the Fatal weakness on Definition 4.2 as a concrete, verified issue (undefined notation, structural incoherence), not a suggestion.
- **Formatting/style nitpicks and typos:** REMOVED per rules against penalizing parser artifacts.
- **"Reproducibility" complaints about undisclosed hyperparameters:** PARTIALLY KEPT — re-framed as "missing experimental details" major weakness, but softened to acknowledge these may be in the stripped appendix.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Correct Equation (4) and Definition 4.2.** The mathematical error in Equation (4) (log ratios instead of log differences) must be fixed. The restricted KL term in Definition 4.2 needs a clear, self-consistent definition with all notation properly introduced.
2. **Right-size the claims.** The theoretical contribution should be presented as a straightforward application of the autoregressive chain rule to CFG-structured distributions, not as "fundamental theorems" about CFG learning. The parallel learning result should be described as expected behavior under standard optimization, and the depth experiments as a controlled replication/validation.
3. **Add statistical rigor.** Include error bars or confidence intervals for Figure 1, computed over the 30 random seeds. Report statistical significance for the CKA comparisons in Table 1.
4. **Include key experimental specifications in the main text.** Architecture details (number of heads, embedding dimension), hyperparameters (learning rate, optimizer, batch size), and data generation procedures should be stated in the main body, not deferred entirely to the appendix.

## Score and Decision

**Bracket rationale (Rounds 1–2).** Round 1 bracketing across all score bands identified `uOnElfFuey.md` (avg 3.00, DFA extraction from LMs) and `F0Zd3knG9j.md` (avg 5.00, hierarchical filtering) as the closest topical anchors. Round 2 compared itemized favorability between this paper and those anchors. The 5.00 anchor has no mathematical errors in its core derivation and has a clearer methodology; our paper is substantially weaker. The 3.00 anchor has a working method with limited novelty (most negative item favorability −5.57). Our paper has **two** Fatal weaknesses (equation error at −1.65, definition incoherence at −1.49) plus four Major weaknesses with negative favorability (−4.68, −4.10, −3.04, −2.30). No anchor paper in the ≥3.0 range has a verifiable mathematical error in its core theoretical claim. This places our paper below the 3.00 anchor. Final calibrated score: **3.0**.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>