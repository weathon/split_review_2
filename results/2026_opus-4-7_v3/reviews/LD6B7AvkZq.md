Now let me read the remaining sections to verify specific claims about Tables 3 and other details.Now I have a thorough understanding of the paper. Let me draft my review.Now let me run calibration search to properly score this paper.Let me read some of the most relevant anchor papers for calibration.Now I have enough anchors to calibrate. Let me form my initial bracket and write the final review.

**Round 1 Bracket Analysis:**

- **Strong reject (1.0)**: Survey papers and pseudoscience — clearly not this paper.
- **Reject (3.0)**: Papers like "Recovering Knowledge by Hardening Language Models" — limited novelty, simple methods. This paper is clearly stronger.
- **Borderline reject (4.0-5.0)**: Papers like "How transformers learn structured data" (5.0) and "Depth Extrapolation" (4.5) — interesting ideas but incomplete execution. Both study transformers on synthetic hierarchical data with theoretical contributions criticized as limited. Very comparable.
- **Borderline accept (6.25-6.67)**: Papers like "Training NNs as Recognizers" (6.25) and "Stack Attention" (6.67) — clear novel contributions with solid execution. This paper's theory is less developed than these.
- **Accept (7.0)**: "A Percolation Model of Emergence" — has a framework that makes predictions and is validated. This paper's framework doesn't yet predict anything non-obvious.

**Initial bracket: 4.5 – 5.5**

The paper is comparable to the 4.5-5.0 rejected anchors: interesting research direction, competent execution within scope, but theory that is more elementary than claimed, and key findings either unexplained or not new. The framework doesn't yet produce non-obvious predictions that justify its existence.

Now let me write the final consolidated review.

---

## Summary
This paper proposes a framework for studying how language models learn context-free grammars (CFGs) through the lens of subgrammar decomposition. It introduces definitions of inner and outer subgrammars, proves KL-divergence decomposition theorems over subgrammar structure, empirically demonstrates parallel subgrammar learning in small transformers, investigates curriculum learning via subgrammar pretraining with CKA-based representation analysis, and shows that recursive depth (not length) is the primary challenge for models.

## Strengths

- **Novel framework connecting subgrammar decomposition to learning dynamics.** The definitions of inner subgrammars (subtrees of derivations, Definition 3.3) and outer subgrammars (subsets of rules, Definition 3.5) are clean, well-motivated, and capture two distinct notions of "simpler substructure." The connection to Gruska's grammatical levels (Theorem 4.1) grounds this in classical CFG theory. This is a genuinely new angle for studying how models acquire syntax.

- **Clean depth-vs-length separation (Section 6, Figure 3).** The controlled experiment on Nested Parentheses isolates a specific difficulty: prediction error stays flat at 0.017 for contexts of increasing length at fixed depth ($(a)^i$), but grows inverse-logarithmically to 0.173 for contexts of increasing recursive depth ($( ^i$), where the ground-truth next-token distribution is identical in both cases. This is a well-designed experiment producing a crisp, interpretable signal.

- **CKA activation analysis provides evidence beyond surface-level loss (Section 5.2, Tables 1 and 3).** Using 30 random seeds, pretrained models show +8.9% to +21.7% higher CKA alignment in attention layers compared to scratch-trained models. Table 3 demonstrates that pretrained models cluster subgrammar sequences closer together and better segregate subgrammar from non-subgrammar sequences. This goes beyond loss curves and says something about what the model has learned internally.

- **Intellectual honesty.** The paper is unusually forthcoming about limitations: careful caveats around the GPT-5.1 anecdote (footnotes 2–3: "purely anecdotal and should not be interpreted as direct evidence"), acknowledgment that context-insensitivity is "a strong assumption," and explicit framing of open questions in Section 7.

## Weaknesses

### Fatal
None

### Major

- **The central theoretical contribution (Theorem 4.3) is more elementary than the paper's framing suggests.** The paper calls the KL decomposition "the most important contribution" and "a suite of fundamental theorems" (Section 4). However, the derivation in Equations (1)–(4) follows directly from writing out the autoregressive factorization of both $P_G$ and $Q_\theta$ and grouping the resulting conditional log-probability terms by which non-terminal generated them. This is the chain rule of KL divergence applied through the lens of PCFG structure — correct and useful as analytical bookkeeping that enables the empirical work, but not a deep mathematical insight. The gap between claimed significance ("fundamental theorems") and actual mathematical depth weakens the paper's identity, since it positions theory as its primary contribution.

- **The "elegant" decompositions (Corollary 4.5, Theorem 4.6) rest on context-insensitivity that is insufficiently validated and partially undermined by the paper's own experiments.** The paper acknowledges this is "a strong assumption" (Section 4, paragraph following Corollary 4.5) and provides only informal validation: "varying the prefix did not result in qualitatively different results" (Figure 1 caption). Section 6 then directly demonstrates that context-insensitivity fails for deep recursive contexts — precisely the regime where the theorems' predictions would be most interesting. The paper's defense that deep contexts are "rare" under the PCFG distribution creates a circularity: the framework is validated only where it trivially holds (high-probability, shallow contexts) and breaks where it could say something non-obvious. This substantially weakens the claimed generality of the theoretical framework without invalidating it entirely.

### Minor

- **Corollary 4.7 (parallel learning) is near-tautological.** It states that if gradient updates for one subgrammar don't hurt performance on others, then all subgrammars are learned in parallel — close to restating non-interference as a sufficient condition for parallel progress. The paper candidly acknowledges this: "An immediate future direction would be to study whether the small transformers and PCFGs of this paper learn subgrammars in parallel because they satisfy the independence condition" (Section 4). The genuinely interesting empirical observation (Figure 1) that parallel learning *does* occur is left without a real explanation.

- **The depth-vs-length result is not integrated with the theoretical framework.** Section 6's finding and the decomposition theorems (Theorem 4.6) remain separate stories. Theorem 4.6's $1/(1-\mathbb{E}[R])$ factor says the divergence blows up as expected recursion approaches 1, but the depth experiment is about *conditioning on* deep contexts, which is a different quantity. Making this connection precise would unify the paper's two main contributions.

- **"Parallel learning" is loosely defined.** The paper defines it as all subgrammar KL-divergences decreasing simultaneously (Figure 1). No measurement of convergence *rates* is provided — whether certain subgrammars converge faster or whether ordering correlates with subgrammar complexity. "All decrease monotonically" is a weak condition that most reasonable optimizers would satisfy.

- **CKA pretraining effect appears limited to attention layers.** Table 1's MLP columns show negligible or negative changes (-0.2%, -4.7%, -2.6%, -0.1%), while attention layers show clear gains (+8.9% to +21.7%). This asymmetry is not discussed and weakens the breadth of the representation-alignment claim.

### Trivial
None

## Nice-to-Haves

- Systematically vary grammar complexity (number of non-terminals, DAG depth, branching factor) to test whether the framework predicts learning difficulty — this would be the natural test of whether the decomposition is *useful* beyond being *correct*.
- Derive a specific prediction from the subgrammar framework about error scaling with depth, then test it, to connect Sections 4 and 6 into a unified story.
- Report variance/confidence intervals for Figures 1 and 2 (Figure 3 already includes them).
- Quantitatively validate context-insensitivity by measuring the actual gap between the elegant decomposition and true loss across different contexts.

## Removed Points
These points are flagged to be removed; treat them with caution.

- **Definition 3.5 appears incomplete** ("for each of its non-terminals" ends abruptly). REMOVED: Parser artifact, not an author error per the paper's formatting rules.
- **Equation (4) notation** shows fractions that should be log-ratio differences. REMOVED: Parser rendering issue, not a mathematical error.
- **Child language comparison overselling.** The abstract states "unlike children" but no experiments on children are run. REMOVED: The paper uses known developmental stages as motivation and does not claim experimental comparison with children; this is standard framing.
- **Scale gap (framing vs. evidence).** All experiments use 2-4 layer transformers on tiny PCFGs while the title suggests broad scope. WEAKENED rather than kept as major: this is standard for theory-oriented papers using synthetic setups. The framing could be more calibrated but this is not a methodological flaw.
- **Depth finding not novel in itself.** Bhattamishra et al. (2020) and Lampinen (2024) showed transformers struggle with recursion. WEAKENED: The paper cites these works; novelty lies in the controlled depth-vs-length separation on the same grammar with identical target distributions. The weakness is retained only as the observation that the connection to the subgrammar framework is underdeveloped (folded into Minor #2).
- **Curriculum learning findings not robust across model sizes.** WEAKENED: The paper honestly acknowledges this limitation ("This effect diminishes as the model size and representational complexity increase").
- **Missing variance for Figures 1 and 2.** MOVED to nice-to-have: while desirable, this is a standard practice concern rather than a core flaw.

## Novel Insights
The paper's most distinctive insight is the idea that CFG learning dynamics should be studied through subgrammar decomposition — viewing the loss landscape as structured by the algebraic hierarchy of the grammar. While the formal theorems are relatively elementary, the framework itself opens a concrete direction: measuring whether models acquire compositional substructures in parallel or sequentially, and whether structural pretraining reshapes internal representations. The CKA finding that pretraining causes models to internally segregate subgrammar from non-subgrammar sequences (Table 3) is a genuine insight about how inductive bias shapes representation geometry. The depth-vs-length separation (Figure 3) cleanly isolates recursive depth as the bottleneck, distinct from sequence length, using identical target distributions — a cleaner version of prior findings.

## Suggestions

- **Recalibrate the theoretical framing.** Present the decomposition as useful analytical bookkeeping that enables the empirical program, rather than as "fundamental theorems." This would better match the mathematical depth and set appropriate expectations.
- **Quantitatively validate context-insensitivity.** Measure the actual KL gap between the elegant decomposition (Corollary 4.5) and the true loss across different contexts, reporting this as a function of context depth.
- **Connect Section 6 to Theorem 4.6.** Derive a specific prediction about error scaling with depth from the $1/(1-\mathbb{E}[R])$ factor and test it — this would turn two separate contributions into a unified story.
- **Characterize parallel learning more precisely.** Measure convergence rates of different subgrammar KL-divergences and test whether the ordering correlates with subgrammar complexity or position in the DAG.
- **Discuss the attention-vs-MLP asymmetry in CKA results.** The negligible MLP changes deserve comment — do they suggest pretraining primarily reshapes attention routing rather than learned features?

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| Systematic Review of LLMs | 8QTpYC4smR | 1.0 | 1 | Entirely different; survey paper with no contribution — far below paper under review |
| Cross-Lingual Humanoid Robots | gwZ90hFSL2 | 1.0 | 1 | Pseudoscience-adjacent; far below |
| NEMESIS Jailbreaking | 5kMwiMnUip | 1.4 | 1 | Shallow explorations with limited rigor; far below |
| Financial Markets Neural Network | nSDOkm0SKo | 1.0 | 1 | Toy scenario with no real contribution; far below |
| Recovering Knowledge by Hardening LMs | uOnElfFuey | 3.0 | 1 | Regular languages + FSA extraction; limited novelty. Paper under review is clearly stronger in framework and breadth |
| Inductive Transformers | NSBP7HzA5Z | 3.0 | 1 | Vague approach with limited evidence; paper under review is stronger |
| FreeLM | qgLyKwXVDs | 2.0 | 1 | Different topic, weak execution; far below paper under review |
| Self-Consuming Training Loop | SaOxhcDCM3 | 3.2 | 1 | Different topic; paper under review has more substance |
| **How transformers learn structured data** | **F0Zd3knG9j** | **5.0** | **1** | **Most comparable anchor. Both study transformers on synthetic hierarchical data with limited theoretical contributions. Rejected for contributions not rising to full paper. Paper under review has more breadth (definitions, curriculum, CKA) but similarly elementary theory.** |
| **Depth Extrapolation on Nested Structures** | **fp77Ln5Hcc** | **4.5** | **1** | **Directly relevant. Both study depth limitations. Theory criticized as too simplistic. Paper under review has broader framework but comparable depth of insight.** |
| Transformers Learn Variable-order Markov Chains | TdgAtxP6G2 | 4.0 | 1 | More formal but narrower; paper under review is slightly stronger |
| Transformers are Efficient Compilers | sprjE7BTZR | 3.75 | 1 | Theory paper on compilers; more formal but less well-executed. Paper under review is slightly stronger |
| **Percolation Model of Emergence** | **0pLCDJVVRD** | **7.0** | **1** | **Both study transformers on formal languages. The percolation paper has a framework that makes predictions and is validated. Paper under review's framework doesn't yet predict non-obvious phenomena. Clearly stronger.** |
| Training NNs as Recognizers of Formal Languages | aWLQTbfFgV | 6.25 | 1 | Clear novel contribution with solid execution; paper under review's contribution is less complete |
| Grammar Reinforcement Learning | yEox25xAED | 6.6 | 1 | Different focus (MCTS + CFG); more concrete results. Stronger than paper under review |
| Stack Attention | XVhm3X8Fum | 6.67 | 1 | Novel architectural contribution for CFLs; more concrete. Stronger than paper under review |
| When can transformers reason | STUGfUz8ob | 7.6 | 1 | Strong theoretical paper with proofs and architectural insights. Clearly stronger |
| TopoLM | aWXnKanInf | 8.0 | 1 | Novel brain-inspired architecture; clearly stronger |
| LLM-SR | m2nmp8P5in | 8.0 | 1 | Different topic; clearly stronger contribution |
| Small-scale proxies for training instabilities | d8w0pmvXbZ | 8.0 | 1 | Different topic; clearly stronger |

**Round 1 bracket: 4.5 – 5.5**

The paper sits most comfortably alongside the 4.5-5.0 rejected anchors (F0Zd3knG9j, fp77Ln5Hcc). Like those papers, it studies transformers on synthetic structured data with a theoretical framework that is sound but elementary, and empirical contributions that are interesting but incomplete. It is clearly above the 3.0 rejected papers (which have fundamental novelty or execution problems) and clearly below the 6.25+ accepted papers (which deliver concrete, non-obvious contributions).

**Final calibration reasoning:** The paper opens a genuine research direction and is well-written with honest limitations. However, the theory is elementary (chain rule repackaged), the most interesting finding (parallel learning) is unexplained, the context-insensitivity assumption is partially undermined by the paper's own experiments, and the depth finding — while cleanly executed — is not well-integrated with the framework. The framework does not yet produce non-obvious predictions. This places it squarely at 5.0: interesting work that doesn't yet deliver enough to cross the acceptance threshold.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>