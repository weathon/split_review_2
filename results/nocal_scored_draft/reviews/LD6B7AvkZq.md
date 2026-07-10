Based on the favorability signals from the scoring model, I can see the key patterns clearly. Let me now produce the final review.

## Summary
2-3 sentence summary of the paper's contribution.

**Paper summary:** This paper introduces formal definitions of inner and outer subgrammars for PCFGs and shows that the KL-divergence of an autoregressive language model from a PCFG decomposes over subgrammar structure via the chain rule. It presents empirical observations about "parallel learning" of subgrammars during training, studies whether curriculum learning via subgrammar pretraining helps, and uses CKA analysis to show that pretraining produces more separable internal representations of subgrammar structure. The paper also replicates existing findings that small transformers fail on deep recursive structures.

## Strengths

- **Clean formalization of inner and outer subgrammars (Definitions 3.3–3.5, Theorem 4.1).** These definitions give precise vocabulary for discussing substructure in CFGs and connect to Gruska's classical DAG decomposition. The distinction between subgrammars as subtrees of derivations (inner) vs. simplified versions of the full language (outer) is well-motivated and reusable beyond this paper.

- **The CKA analysis (Section 5.2, Table 1) provides mechanistic evidence about how subgrammar pretraining changes internal representations.** Showing that pretrained models cluster subgrammar sequences more tightly and better separate subgrammar from non-subgrammar strings goes beyond confirming that pretraining helps—it identifies representational differences that concretely align with the paper's subgrammar framework. This is the paper's most genuinely empirical contribution.

- **Theorem 4.3 and its corollaries establish a valid mathematical relationship between the KL-divergence of an autoregressive model from a PCFG and the subgrammar structure.** The decomposition is conceptually sound and provides a formal lens for connecting learning dynamics to grammar structure.

## Weaknesses

### Fatal
None.

### Major

- **The paper's central theoretical contribution is substantially less deep than presented.** Theorem 4.3 and its corollaries follow directly from the chain rule of KL-divergence applied to the autoregressive factorization implied by the PCFG generative process. The result is not incorrect, but framing it as "the most important contribution" and "a suite of fundamental theorems" (line 26) that "initiate the study" of subgrammar-aware learning inflates its significance. The mathematical content is an observation that a textbook identity, applied to this specific factorization, yields a sum over subgrammars. The paper would benefit substantially from recalibrating its claims—presenting the decomposition as a formalization tool rather than a new theorem about CFGs or learning dynamics. This gap between the framing and the substance is the paper's most significant weakness.

### Minor

- **The "parallel learning" finding (Section 4.2) is presented as non-obvious** ("One might have intuitively expected a model to first master a simpler subgrammar before progressing to the encompassing supergrammar") but simultaneous decrease of all subgrammar losses is the default expectation for gradient descent on a joint loss. The paper offers no evidence that sequential mastery is expected or observed in any relevant setting—the comparison to children is mentioned qualitatively but not operationalized. Corollary 4.7 formalizes a sufficient condition for parallel learning but is nearly tautological: "if gradient updates on one subgrammar don't hurt others, then all improve together." The observation itself is valid, but the framing oversells its surprise value.

- **The depth-generalization experiments (Section 6), while cleanly designed, replicate well-known findings** that transformers fail on deep recursive structures—documented in work the paper itself cites (Bhattamishra et al., 2020; Lampinen, 2024). The anecdotal GPT-5.1 test (explicitly disclaimed by the authors as not constituting evidence) adds no substance. The experiments confirm prior results but do not contribute new insight beyond what the existing literature already establishes.

- **Experimental reporting is incomplete.** The paper specifies only that a "2-layer, 2-head transformer" is used (line 299) with no details on embedding dimension, hidden size, parameter count, learning rate, batch size, optimizer, or training steps. The estimation of subgrammar-specific KL divergences is described only as using "a random (but likely) prefix" (line 200) without specifying how many prefixes are sampled, whether results are averaged, or how stable the approximation is across different choices.

- **Training curves (Figures 1, 2, 3) are reported as single runs without variance estimates** despite Table 1 reporting results averaged over 30 seeds, suggesting multi-seed data is available. The CKA analysis (Table 1) reports percentage changes (+8.9%, +21.7%) without confidence intervals or statistical significance tests.

- **Definitional imprecision in a few places.** Definition 3.3 is slightly ambiguous: "the set of all rules with non-terminals in $\mathcal{N}'$" could mean rules whose LHS is in $\mathcal{N}'$ or rules where all mentioned non-terminals are in $\mathcal{N}'$. The intended reading (LHS in $\mathcal{N}'$) can be inferred but should be explicit. Definition 4.2 uses unexplained notation ($P(s|\epsilon)$, "$\neg s$") and is acknowledged by the paper as not fully rigorous.

### Trivial
None.

## Nice-to-Haves

- The paper's own thesis—that studying CFG learning through subgrammar structure is fruitful—would be strengthened by demonstrating that the decomposition yields **predictive or analytical power that the chain rule alone does not**. For instance: can it predict which subgrammars will be learned faster? Can it explain conditions under which negative interference between subgrammars occurs? The current paper shows the decomposition holds (which follows from basic probability) and runs experiments that are not predicted by the decomposition. Tighter integration where the theory makes testable predictions would raise the contribution.

- A precise description of the subgrammar KL estimation procedure (number of random prefixes, averaging, variance across choices) would improve reproducibility.

## Removed Points
These points are flagged to be removed; treat them with caution.

1. **Garbled derivation in equation (4).** The harsh critic noted that equation (4) contains ratios of logarithms (log P / log Q) that do not follow from standard KL manipulation. This appears to be a parser artifact—LaTeX fractions were mangled during PDF extraction. The paper states the full proof is in Appendix A, and the conceptual conclusion (KL decomposes into a sum of conditioned KLs) is stated clearly in prose. Removed per instruction to disregard formatting artifacts.

2. **Criticism about Figure 5 being in the appendix.** The appendix is stripped from the review packet; this is not an author error.

3. **Criticism about the paper not addressing problems outside its stated scope** (e.g., requesting the paper establish a theory explaining why specific subgrammars are learned faster, or demanding the paper characterize learning dynamics beyond what the chain rule provides). Such demands go beyond evaluating what the paper sets out to do. Moved to Nice-to-Haves.

4. **Criticism about the paper not citing a specific missing related work** (none was specified).

## Novel Insights
None beyond the paper's own contributions.

## Suggestions

- Recalibrate the framing of the theoretical contribution throughout the paper. Present the KL decomposition as a formal observation/notational framework (which it is) rather than a fundamental new theorem about CFGs.
- Add complete experimental specifications: architecture dimensions, training hyperparameters, and a precise description of how subgrammar KLs are estimated (prefix sampling procedure, number of samples, variance across prefixes).
- Include error bars or variance bands for training curves where multi-seed data is available. Add confidence intervals or significance tests for the CKA percentage changes in Table 1.
- Clarify the ambiguity in Definition 3.3 and provide a cleaner, more rigorous presentation of Definition 4.2.
- The parallel learning discussion could be strengthened by investigating conditions where subgrammar interference occurs, rather than framing simultaneous decrease as surprising.

## Score and Decision

**Score:** 4.0  
**Decision:** Reject

**Rationale:** The paper makes a useful contribution by formalizing subgrammar structure for PCFGs and providing a clean vocabulary for discussing substructure in grammar learning. The CKA analysis is genuinely empirical and shows how pretraining shapes internal representations in a way that aligns with the subgrammar framework. However, the paper's central theoretical contribution is significantly oversold—the KL decomposition follows directly from the chain rule applied to the autoregressive factorization and does not constitute a new theorem about CFGs or learning dynamics. The empirical findings are modest: the parallel learning observation is the default expectation for joint optimization, and the depth-generalization experiments replicate established results. The gap between the strength of the paper's claims and the substance of its contributions, combined with incomplete experimental reporting, places this below the acceptance threshold. With recalibrated claims, fuller experimental details, and evidence that the subgrammar lens yields insight beyond what standard identities provide, a revised version could be publishable.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>