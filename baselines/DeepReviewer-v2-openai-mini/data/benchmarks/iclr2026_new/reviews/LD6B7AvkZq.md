## Summary
# Final Review Report

## Summary

This paper introduces a framework for studying how language models learn context-free grammars (CFGs) by analyzing the *subgrammar* structure of these grammars. The authors define two types of subgrammars — inner (corresponding to derivation subtrees) and outer (simplified rule subsets) — and prove several theorems showing that the KL-divergence (or loss) of a language model decomposes recursively over subgrammar structure. Empirically, they demonstrate that small transformers learn all subgrammars in parallel (unlike children), that pretraining on subgrammars can improve representational alignment and final loss for small models, and that trained models struggle with deep recursion even when they perform well on non-recursive sequences of similar length.

The paper addresses an interesting and timely question at the intersection of formal language theory, mechanistic interpretability, and learning dynamics. The concept of subgrammar decomposition is a natural and potentially productive lens. However, the theoretical core contains a critical mathematical error in Equation (4) that invalidates the central derivation, and several key assumptions (especially context-insensitivity in Corollary 4.5) are inadequately justified. The experimental evidence, while suggestive, is limited to one small transformer architecture and a handful of synthetic CFGs without statistical rigor. The paper would benefit from correcting the mathematical errors, strengthening the empirical methodology, and more carefully bounding the scope of its claims.

## Strengths
1. **Timely and relevant research question.** The paper addresses an important gap: understanding how language models acquire hierarchical structure during training, rather than only analyzing fully trained models. The subgrammar framework introduces a formal vocabulary for studying learning dynamics over syntactic substructures.

2. **Elegant theoretical framing.** The decomposition of PCFGs into inner and outer subgrammars (Definitions 3.3–3.5) and the DAG representation (Theorem 4.1) provide a clean mathematical foundation for analyzing how language modeling loss relates to grammar structure. The recognition that Gruska's "grammatical levels" connect to this framework shows historical awareness.

3. **Non-trivial empirical findings.** The parallel-learning observation (that small transformers learn all subgrammars simultaneously rather than sequentially) is genuinely interesting and counter to the intuitive hypothesis inspired by child language acquisition. The depth-vs-length generalization experiment (Section 6) cleanly separates two confounded factors and reveals a non-trivial limitation.

4. **Addressing an underexplored dimension.** Prior work on CFG learning has focused on representation analysis (what trained models know) rather than learning dynamics (how they get there). This paper's emphasis on the interaction between learning trajectories and grammatical substructure opens a productive new direction for future work.

5. **Transparency about limitations.** The paper explicitly acknowledges several limitations: the experiments are not exhaustive, the context-insensitivity assumption is strong, the depth-probing experiments use a single grammar, and the GPT-5.1 arithmetic anecdote is explicitly marked as informal. This candor is commendable.

## Weaknesses
The following weaknesses are ordered by severity and impact on the paper's validity and contribution.

### W1. Critical mathematical error in the core derivation [Page 1, Section 4.2, Equation (4)]

The derivation from Equations (2)-(3) to (4) commits a fundamental algebraic error: it transforms a sum over $P_G(\alpha a \beta) \cdot \log(P/Q)$ into a ratio $\log P / \log Q$. The identity $\log(P/Q) = \log P - \log Q$ is a *difference* of logs, not a ratio, and the sum over $a$ cannot be moved inside separate logs. Specifically:

$$\sum_{a} P_G(\alpha a \beta) \left[\log\frac{P_G(\alpha|\epsilon)}{Q_\theta(\alpha|\epsilon)}\right] \neq \frac{\log P_G(\alpha|\epsilon)}{\log Q_\theta(\alpha|\epsilon)}$$

The correct simplification should yield expected log-ratio terms of the form $\mathbb{E}_{s \sim P_G}[\log P_G(\alpha|\epsilon) - \log Q_\theta(\alpha|\epsilon)]$, not ratios of marginal log probabilities. This error propagates to Definition 4.2, Theorem 4.3, and Theorem 4.6, undermining the mathematical foundation of the paper's central theoretical contribution. **Severity: critical. Fixability: fixable** — the decomposition can be rewritten using conditional expected log-ratios (conditional KL divergence), preserving the additive structure over subgrammars while correcting the algebra.

### W2. Undefined and unclear notation in Definition 4.2 [Page 1, Section 4.2]

Definition 4.2 introduces $D_{\text{KL}}(P_G \parallel Q)_A$ using the symbol $\neg s$ (without definition), $R$ (undefined, presumably $P_G$), and ambiguous summation structure. The expression $\sum_{a \in \Sigma^*} D_{\text{KL}}(P_G \parallel Q \mid \neg s)$ does not correspond to any standard definition of conditional KL divergence. This imprecision makes the subsequent theoretical development (Corollary 4.4–4.5, Theorem 4.6) difficult to interpret rigorously. **Severity: major. Fixability: fixable** — the definition should be restated as a weighted expectation of conditional KL divergences over contexts.

### W3. Context-insensitivity assumption is inadequately justified [Page 1, Corollary 4.5 and surrounding text]

Corollary 4.5 relies on the assumption that $Q_\theta$ is "context-insensitive" — producing identical distributions for a subgrammar across all contexts. The paper's defense ("our experiments suggest this condition is perhaps not so strong") is circular (the experiments are meant to validate the theorem that uses this assumption) and lacks quantitative bounds. No formal robustness guarantee is provided for when the assumption is violated. **Severity: major. Fixability: partially fixable** — adding a formal bound on decomposition error under approximate context-insensitivity would significantly strengthen the paper.

### W4. Corollary 4.7 is nearly circular [Page 1, Section 4.2]

The "independence condition" in Corollary 4.7 states that if gradient updates for one subgrammar don't hurt others, then all subgrammars are learned in parallel. This is essentially the definition of parallel learning restated as a condition, providing no mechanistic insight into *why* or *when* it occurs. Additionally, the gradient expression $\delta = \nabla_\theta(-D_{\text{KL}}(P_G \parallel Q_\theta)_{A_i})$ has a sign error: standard training minimizes D_KL (gradient descent), not maximizes -D_KL (gradient ascent). **Severity: major. Fixability: fixable** — rewrite with correct gradient descent formulation and clarify the corollary as an empirical observation with conjectured causes.

### W5. Narrow experimental validation [Page 1, Sections 5–6]

The empirical results, though interesting, are limited in scope: (a) only one small transformer architecture (2-layer, with some 4-layer results) is tested; (b) only synthetic CFGs are used, with no details about the complexity or size of the grammars; (c) the depth-vs-length experiment (Section 6) uses a single grammar (Nested Parentheses); (d) CKA values are reported only for a "top quantile" of seeds, raising selection-bias concerns; (e) no statistical significance tests or confidence intervals are reported for any experimental results; (f) several figures (Figures 5, 6, Table 3) are referenced but not present in the provided manuscript, making key claims unverifiable. **Severity: major. Fixability: fixable** — add multi-grammar experiments, report full seed distributions, include significance tests, and ensure all referenced figures are present.

### W6. Overclaiming and imprecise language [Page 1, Abstract and throughout]

The abstract claims to "prove a suite of fundamental results" and "show definitively" — language that exceeds the evidence, especially given the mathematical error in the core derivation. The phrase "most important contribution" (Page 1, line 18) is presented as self-assessment rather than letting the results speak. "Quite definitively" (Page 1, line 19) regarding alignment analysis is overstated given the small-scale, single-architecture study. **Severity: minor. Fixability: fixable** — replace with evidence-calibrated language throughout.

### W7. Related Work is organized as a list rather than thematically [Page 1, Section 2]

The Related Work section proceeds paper-by-paper rather than organizing around conceptual axes (representation probing, formal language limits, learning dynamics). This makes it harder for readers to see how the current work fits into the broader landscape. **Severity: minor. Fixability: fixable** — reorganize into 3-4 thematic paragraphs with clear gap statements.

### W8. Discussion section could be more concrete [Page 1, Section 7]

The open problems are stated at a programmatic level rather than as specific, testable hypotheses. The conjecture about weight existence is hard to falsify without specifying the depth bound. **Severity: minor. Fixability: fixable** — reframe as concrete research questions with proposed experimental paradigms.

## Score
## ASCII Diagrams

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Research Question: How do LMs learn syntactic substructure?]
    |
    |--- C1: KL-loss decomposes over subgrammar structure [Theoretical]
    |       |-- Evidence: Theorem 4.3, Theorem 4.6, Figure 1
    |       |-- Error: Eq(4) derivation invalid (log-ratio vs ratio-of-logs) [CRITICAL]
    |       |-- Gap: Context-insensitivity assumption unquantified
    |
    |--- C2: Small transformers learn subgrammars in parallel [Empirical]
    |       |-- Evidence: Figures 1-2, Corollary 4.7
    |       |-- Gap: Corollary 4.7 is circular; gradient sign error
    |       |-- Risk: Only one architecture tested
    |
    |--- C3: Subgrammar pretraining improves alignment [Empirical]
    |       |-- Evidence: CKA analysis (Table 1), Figure 6 (missing)
    |       |-- Gap: "Top quantile" selection bias; no significance tests
    |
    |--- Additional: Depth-vs-length generalization difficulty [Empirical]
            |-- Evidence: Figure 3 (single grammar, nested parentheses)
            |-- Gap: Only one CFG; no baselines (LSTM, n-gram)
```

### ASCII Diagram — Revision Strategy Roadmap

```text
Priority 0 (Before Resubmission):
  [Eq(4) error] --> [Rewrite using conditional expected log-ratios]
      --> [Re-derive Theorem 4.3 and 4.6 with corrected algebra]
      --> [Expected impact: Core theoretical claim becomes valid]

Priority 1 (High Impact, Moderate Effort):
  [Def 4.2 notation] --> [Restate with clear conditioning notation]
  [Cor 4.7 circular] --> [Rewrite as empirical finding + conjecture]
  [Context-insensitivity] --> [Add formal robustness bound]
  [CKA quantile selection] --> [Report full 30-seed distributions + tests]

Priority 2 (Medium Impact, Higher Effort):
  [Single-grammar experiments] --> [Add 2-3 CFG families (palindromes, arithmetic)]
  [Single architecture] --> [Include LSTM baseline for depth-probing]
  [Missing figures/tables] --> [Ensure all referenced exhibits are present]

Priority 3 (Quality Polish):
  [Overclaiming language] --> [Calibrate to evidence throughout]
  [Related Work structure] --> [Reorganize thematically]
  [Discussion framing] --> [Make open problems more concrete]
```

### ASCII Diagram — Related-Work Taxonomy Tree (Layered)

```text
Related Work: Neural Models & Formal Languages (Root)
├── Branch 1: Trained Model Analysis (static)
│   ├── Leaf 1.1: Mechanistic interpretability of syntax
│   │   └── [Allen-Zhu & Li 2023: stack-like computations in transformers]
│   ├── Leaf 1.2: Probing studies
│   │   └── [Meng et al.; Geva et al.; Dar et al.; Ferrando & Voita]
│   └── Leaf 1.3: Representational similarity
│       └── [Kornblith et al. 2019: CKA]
├── Branch 2: Formal Language Expressivity & Limits
│   ├── Leaf 2.1: Theoretical limits of transformers
│   │   └── [Hahn 2020: long-range dependency limits; Pérez et al. 2021: Turing-completeness]
│   ├── Leaf 2.2: Empirical limitations on formal languages
│   │   └── [Bhattamishra et al. 2020; Lampinen 2024; Suzgun et al. 2018]
│   └── Leaf 2.3: Optimization challenges for structured functions
│       └── [Klivans & Kothari 2014; Telgarsky 2016; Abbe et al. 2024; Daniely & Malach 2020]
├── Branch 3: Learning Dynamics & Development
│   ├── Leaf 3.1: Child language acquisition parallels
│   │   └── [Evanson et al. 2023: GPT-2 developmental stages]
│   ├── Leaf 3.2: PCFG learning curves (THIS PAPER'S MAIN AREA)
│   │   └── [Cagnetta & Wyart 2024: random-hierarchy models for compositional learning]
│   └── Leaf 3.3: Subgrammar decomposition (THIS PAPER'S NOVEL CONTRIBUTION)
│       └── [Current work: KL recurrence over subgrammar structure]
└── Branch 4: Curriculum Learning for Structured Tasks
    └── Leaf 4.1: Pretraining strategies
        └── [Bengio et al. 2009; Wang et al. 2021; Weinshall et al. 2018]
```

## Score

**Final Score: 5/10**

**Rationale:** The paper tackles an important and timely research question — how language models acquire hierarchical syntactic structure during training — and introduces the subgrammar framework as a promising analytical lens. The parallel-learning observation and depth-vs-length dissociation are genuinely interesting empirical findings. However, the score is constrained by a critical mathematical error in the core theoretical derivation (Equation (4)), which invalidates the central claim of "fundamental theorems" about KL decomposition over subgrammars. Additionally, the experimental validation is too narrow (one architecture, limited grammars, no statistical rigor) to support the strength of the claims made. The paper would benefit from correcting the mathematical errors, providing formal robustness guarantees for key assumptions, substantially expanding the experimental methodology, and recalibrating the language to match the evidence. In its current form, the work is best positioned as a promising early-stage contribution that opens a new direction rather than a fully validated set of results.

**Novelty & Retrieval Note:** External literature verification was unavailable for this run (paper_search provider unavailable due to missing API token). All novelty/comparison conclusions are based on manuscript content alone and should be verified against the full literature before publication.

*Score is on a 10-point scale emphasizing research value and novelty as primary scoring dimensions, consistent with the identified weaknesses and their impact on validity.*