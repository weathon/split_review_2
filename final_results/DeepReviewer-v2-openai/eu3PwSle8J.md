## Summary
This paper addresses indirect prompt injection attacks in large language models (LLMs), a security vulnerability where adversaries inject malicious instructions into the input context (e.g., emails, web pages) to override user intentions. The authors identify that existing instruction hierarchy (IH) based defenses inject privilege signals only at the input layer—either via special delimiter tokens or additive segment embeddings—and hypothesize that this limits effectiveness as signals degrade through deeper decoder layers.

To overcome this, the paper proposes **Augmented Intermediate Representations (AIR)**, which injects IH signals into every decoder layer via layer-specific trainable embedding tables. Each decoder block contains a small embedding table (K entries, one per privilege level) whose vectors are added to intermediate token representations before processing by that block. This adds only ~0.4M parameters for an 8B model (0.005% increase).

The evaluation spans three model families (Llama-3.2-3B, Qwen-2.5-7B, Llama-3.1-8B), two training methods (SFT, DPO), and two datasets (AlpacaFarm, SEP). Against gradient-based attacks (GCG, Astra), AIR achieves 1.6x–9.2x ASR reduction compared to prior IH methods, with less than 2% utility degradation in most settings. On SEP, AIR with DPO training achieves the best utility-separation trade-off.

**Core contribution**: The paper's insight—injecting privilege signals at every layer rather than only the input—is conceptually sound, technically straightforward, and empirically effective. The work is well-positioned within the existing IH defense literature and provides a clean architectural improvement.

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: Indirect prompt injection attacks]
    -> [Existing IH defenses inject signals only at input layer]
    -> [Hypothesis: IH signals degrade across decoder layers]
       -> Evidence: cosine similarity of privilege-level representations increases with depth (Fig. 3)
    -> [Proposed solution: AIR — inject IH signals at every decoder layer]
       -> Mechanism: Trainable embedding table S_j per layer, additive to hidden states
       -> Overhead: 0.005% parameter increase, negligible inference cost
    -> [Empirical evaluation]
       -> 3 models x 2 training methods x 2 benchmarks
       -> Gradient attacks: 1.6x–9.2x ASR reduction vs prior IH methods
       -> Static attacks: near-ceiling for all IH methods
       -> Utility: <2% degradation in most settings
    -> [Remaining gaps]
       -> SFT vs DPO confounded by LoRA/full-FT asymmetry
       -> No adaptive attack evaluation
       -> SEP separation score conditioned on utility
       -> Only models up to 8B tested
```

## Strengths
**S1. Clean, principled architectural insight.** The core idea—injecting instruction hierarchy signals at every decoder layer rather than only the input—is motivated by a clear hypothesis (signal degradation through depth) and supported by a simple, parameter-efficient implementation. The analogy to positional embedding research (RoPE) effectively situates the contribution within a familiar design pattern.

**S2. Systematic and multi-dimensional evaluation.** The paper evaluates across 3 model families (3B–8B), 2 training methods (SFT, DPO), 2 categories of attacks (static and gradient-based), and 2 datasets (AlpacaFarm, SEP). This breadth strengthens confidence that AIR's advantage is not limited to a single configuration.

**S3. Strong empirical differentiation on gradient-based attacks.** AIR consistently achieves lower ASR than prior IH injection methods (Delimiters, ISE) across all model/training combinations under GCG and Astra attacks. The improvement is often substantial (e.g., 38%→4.1% on GCG for Llama-3.2-3B SFT). The loss curves in Figure 7 corroborate the ASR results.

**S4. Transparent overhead reporting.** The paper explicitly calculates the parameter overhead (0.4M for 8B model, 0.005% increase) and acknowledges that training compute is comparable to prior methods. Inference overhead is correctly noted as negligible (simple addition operations).

**S5. Reproducibility-oriented experimental design.** The two-stage training procedure (instruction tuning + adversarial training) is clearly specified with learning rates, optimizer details, and epoch counts. The comparison mechanisms (Delimiters, ISE) are implemented within the same codebase, enabling fair within-family comparison.

## Weaknesses
**W1. SFT vs DPO comparison confounded by training protocol asymmetries [critical/major].** (Page 5 - Training, Page 6 - Evaluation Methodology)

The adversarial training stage uses fundamentally different configurations for SFT and DPO: SFT undergoes full fine-tuning (LR=1e-5) while DPO uses parameter-efficient LoRA (LR=2e-4). Additionally, gradient-based attack optimization uses 50 steps for SFT models and 200 steps for DPO models. These asymmetries mean that observed differences between SFT and DPO—including the paper's claim that "DPO yields more robust models than SFT"—cannot be attributed solely to the training objective; they may partly reflect the number of trainable parameters, learning rate schedules, or optimization budget. This confound weakens one of the paper's secondary conclusions. *Fix: Ablate with DPO full fine-tuning or SFT LoRA at matched optimization steps.*

**W2. Central motivational experiment (cosine similarity, Fig. 3) has limited scope [major].** (Page 3 - Limitation of Existing Defenses)

The claim that input-level IH signals "degrade as they propagate through decoder layers" is supported by cosine similarity measurements on only one model (Llama-3.2-3B) and only 100 prompts. The Delimiter condition shows near-1.0 similarity throughout—which is expected since identical delimiter tokens carry the same embeddings—but this makes the comparison less informative than it appears. More critically, cosine similarity is a proxy measure; it does not directly demonstrate that *task-relevant behavior* (instruction following) degrades correspondingly. *Fix: Add similarity measurements on at least one more model (e.g., Qwen-2.5-7B) and include a behavioral metric (e.g., per-layer intervention ASR) to link representation similarity to actual robustness.*

**W3. Evaluation methodology has a metric incomparability issue [major].** (Page 6 - Evaluation Methodology)

Static attack ASR is measured via exact string match (output contains "hacked!"), while gradient-based attack ASR is measured via logit likelihood (probability of generating the target phrase). These are fundamentally different thresholds: likelihood-based ASR is more permissive and can count an attack as "successful" even when the actual generated output does not contain the target string. The paper does not disclose this discrepancy or discuss how it affects cross-attack-type comparisons. Furthermore, the SEP separation score S is conditioned on the model's utility performance (denominator = number of cases where the probe is correctly followed in the instruction segment), which means that a model with low utility can paradoxically achieve a high separation score. *Fix: Report both likelihood-based and sampling-based ASR for gradient attacks. Report unconditional robustness for SEP. Disclose metric differences explicitly in the evaluation design.*

**W4. Static attack evaluation suffers from ceiling effects and limited coverage [major].** (Page 6 - Results)

All three IH methods achieve ASR near 0% on the four static attack types (Naive, Ignore, Completion, Escape Separation). The paper acknowledges that the first two are "in-distribution as they are seen during adversarial training," making the near-zero ASR expected rather than informative. More importantly, the evaluation does not include adaptive static attacks designed to exploit the IH mechanism itself—for example, adversarial instructions that mimic system-message formatting to claim P0 privilege, or attacks that use encoding tricks to bypass privilege-level assignment. Without such tests, the claim of "near-perfect protection" against static attacks is not adequately supported. *Fix: Design and evaluate at least 2-3 adaptive static attacks that target the IH mechanism directly. Discuss ceiling effects and their implications for robustness generalization.*

**W5. Paper lacks formal connection between threat model and evaluation metrics [major].** (Page 2 - Preliminaries, Page 6 - Evaluation Methodology)

Section 2 introduces an alignment function A(O,I) as the formal measure of instruction following, but the evaluation never references A. Instead, ASR and SEP scores are used without formal mapping to A. This disconnect between the formal framework and the empirical methodology reduces theoretical rigor. The defender's goal is described as maximizing A(O,I) and Q(O|I,D), but no attempt is made to bound or relate these quantities to the reported metrics. *Fix: Explicitly state how ASR operationalizes 1-A(O,I) for a fixed adversarial target, and how SEP measures a related but distinct aspect of privilege-level compliance.*

**W6. Conclusion lacks limitations discussion [moderate].** (Page 8 - Conclusion)

The paper ends without any limitations or future work section. This omission is significant given the scope boundaries: only models up to 8B parameters, only two gradient-based attack algorithms, no adaptive attacks, unknown generalization to larger models or different IH mappings, and no analysis of failure cases. Including a limitations paragraph would strengthen scientific credibility and guide future research. *Fix: Add a limitations paragraph covering model scale, attack diversity, adaptive robustness, and computational costs.*

**W7. Relative improvement framing can be misleading [moderate].** (Page 1 - Abstract, Page 7 - Results)

The paper reports ASR reduction as "1.6x to 9.2x" (relative factor) without consistently providing absolute percentage point differences. When baseline ASR is high (e.g., 38% for Delim), a reduction to 4.1% (AIR) is indeed impressive, but the 9.2x relative factor sounds more dramatic than the 33.9 percentage point absolute improvement. When both numbers are small, relative factors can inflate perceived improvement. *Fix: Always report absolute ASR alongside relative reduction. Consider adding a table showing absolute differences with confidence intervals.*

```text
ASCII Diagram — Revision Strategy Roadmap

[W1: SFT/DPO confound]
    -> Fix: Add matched-parameter ablation (full-FT DPO or LoRA SFT)
    -> Expected: Clean attribution of training objective effect

[W2: Limited cosine similarity evidence]
    -> Fix: Add second model + behavioral metric
    -> Expected: Stronger causal chain from signal degradation to robustness

[W3: Metric incomparability]
    -> Fix: Unify ASR definition across attack types; report unconditional SEP
    -> Expected: Transparent, comparable evaluation

[W4: Static attack ceiling]
    -> Fix: Add adaptive IH-targeting attacks
    -> Expected: Reveal genuine robustness boundaries

[W5: Formal-empirical disconnection]
    -> Fix: Map A(O,I) to ASR; clarify operationalization
    -> Expected: Stronger theoretical-empirical linkage

[W6: Missing limitations]
    -> Fix: Add limitations paragraph
    -> Expected: Improved scientific completeness

[W7: Relative vs absolute framing]
    -> Fix: Report absolute differences + confidence intervals
    -> Expected: Accurate, interpretable results
```

## Score
**Final Score: 6/10**

**Rationale.** The paper presents a conceptually clean and technically simple architectural improvement—injecting instruction hierarchy signals at every decoder layer—that consistently improves robustness against gradient-based prompt injection attacks across multiple models and training configurations. The core insight is well-motivated, the implementation is lightweight, and the empirical results on GCG and Astra attacks demonstrate clear improvements over prior IH injection methods.

However, the score is tempered by several methodological concerns that reduce confidence in the full strength of the claims:

1. The SFT vs DPO comparison contains a training protocol confound (full FT vs LoRA, different optimization steps) that weakens the secondary conclusion about preference optimization.
2. The central motivational evidence (cosine similarity, Fig. 3) is limited to one model and 100 prompts, and the metric incomparability between static and gradient-based ASR definitions undermines cross-attack-type comparisons.
3. Static attack evaluation is at ceiling, and no adaptive attacks are tested, so robustness boundaries remain unclear.
4. The absence of a limitations discussion and the reliance on relative (rather than absolute) improvement framing moderately overstate the contributions.

The paper's research value lies in identifying and addressing a genuine blind spot in IH-based defenses. The innovation is incremental but practically meaningful. The evaluation, while systematic in breadth, would benefit from tighter experimental controls and broader attack coverage. Novelty/comparison conclusions are deferred pending manual literature verification due to retrieval unavailability in this run.

**Post-Revision Target: [6.5, 7.5]/10** — If the authors address the confound between SFT/DPO, add adaptive attacks, unify metric definitions, and include a limitations section, the score could rise to the 6.5–7.5 range.

```text
ASCII Diagram — Related-Work Taxonomy (Layered, Deferred Verification)

Note: External literature search was not available in this run. The taxonomy below
is constructed from the manuscript's own citations and represents the paper's
self-positioning. Deferred manual verification is required for novelty judgments.

Instruction Hierarchy (IH) Defense Methods
├── Branch 1: IH Injection Mechanism
│   ├── Leaf 1.1: Delimiter-based
│   │   └── Wallace et al. 2024; Chen et al. 2024a (StruQ)
│   ├── Leaf 1.2: Segment Embedding-based
│   │   └── Wu et al. 2024 (ISE)
│   ├── Leaf 1.3: Multi-layer injection
│   │   └── THIS WORK: AIR (Augmented Intermediate Representations)
│   └── Leaf 1.4: Preference-optimized IH
│       └── Chen et al. 2024b (SecAlign — uses delimiters + DPO)
├── Branch 2: Training Objective
│   ├── Leaf 2.1: Supervised Fine-Tuning (SFT)
│   └── Leaf 2.2: Direct Preference Optimization (DPO)
└── Branch 3: Attack Methodology (used for evaluation)
    ├── Leaf 3.1: Static attacks (Ignore, Completion, Escape Separation)
    ├── Leaf 3.2: Gradient-based (GCG, Momentum-GCG, NeuralExec, Astra)
    └── Leaf 3.3: Evaluation frameworks (AlpacaFarm, SEP)

Value contribution of AIR: Multi-layer injection improves IH signal persistence,
enabling stronger gradient-attack robustness without utility degradation.
```