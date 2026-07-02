## Summary
This paper proposes a self-evolution framework where a single language model acts as both generator and verifier to construct preference data for fine-tuning without external supervision. The authors introduce thresholded majority voting to extract reliable signals from noisy self-verification and explore single-turn (SimpleGV) and multi-turn (RevisionGV) generator-verifier games. Experiments on logical reasoning (Knights and Knaves) and mathematical reasoning benchmarks show consistent improvements, with the 4B model on KK improving from 31.0% to 44.8% with curriculum learning, and demonstrate easy-to-hard generalization where training on simpler instances transfers to harder ones.

## Strengths
- **Clean and well-motivated framework**: The paper systematically studies a minimal self-evolution setup (single model, no external signals) and clearly delineates the design space (single-turn vs multi-turn, thresholded voting, iterative training, curriculum learning). This provides a useful reference point for the community.
- **Strong empirical results on controlled benchmarks**: On the Knights and Knaves benchmark, the paper shows substantial and consistent improvements across multiple variants (SimpleGV: 31.0%→40.7%, RevisionGV: 42.2%, iterative: 44.1%, curriculum: 44.8%). The easy-to-hard generalization finding (training on 2-3 person instances transfers to 4-8 person instances) is a particularly interesting and non-trivial result.
- **Thorough ablation and analysis**: The paper investigates scaling with model size (1B, 4B, 12B), data size (5K-40K), threshold sensitivity, cost-performance trade-offs, and iterative training dynamics. This provides practical guidance for practitioners and helps isolate which components drive improvement.

## Weaknesses
### Major
- **Limited novelty relative to concurrent work**: The core idea of using a model as both generator and verifier for self-improvement has been extensively explored in recent literature (R-Zero, Absolute Zero, INTUITOR, LSP, EMPO, TTRL, etc.). The paper's main technical contribution—thresholded majority voting for constructing preference pairs—is a straightforward extension of majority voting. While the paper provides a clean synthesis and systematic study, the individual components are not novel. The paper would be stronger if it demonstrated a clear advantage over these methods on shared benchmarks or provided deeper theoretical insight into when/why self-verification works.
- **Weak baselines and selective comparisons**: The main comparison table (Table 1) compares SimpleGV against methods that are either from different base models (INTUITOR, AZR, GRPO use Qwen2.5-7B) or use different training setups (online RL, external environments). The paper does not compare against the most directly relevant baselines: (1) simple supervised fine-tuning on the same self-generated data using ground-truth labels (to isolate the value of the verifier), (2) standard DPO with random preference pairs (to verify the verifier adds value beyond any preference data), or (3) self-consistency/majority voting at inference time (to compare self-evolution vs. inference-time compute). Without these, it's unclear whether the gains come from the verifier signal or simply from having more training data.
- **Results on standard math benchmarks are marginal**: On GSM8K, MATH500, MATHHard, and TabMWP, SimpleGV's improvements over the base model are small (e.g., GSM8K: 89.2→89.0 for 4B, 90.2→90.6 for 7B) and often within one standard deviation. The paper claims "consistent improvements" but the evidence is weak on these benchmarks. The strongest results are on the synthetic KK benchmark, which raises questions about generalizability to more realistic tasks.

### Minor
- **Computational cost is understated**: The paper acknowledges cost but does not provide a fair comparison. SimpleGV requires generating k candidates and running n verifier passes per candidate, which is substantially more expensive than standard training. The paper should report total FLOPs or wall-clock time and compare against a baseline that uses equivalent compute for inference-time improvements (e.g., majority voting with k samples).
- **Threshold sensitivity**: While the paper notes that τ=0.6-0.7 works well, the optimal threshold varies across tasks and model sizes. The 1B model actually degrades with SimpleGV at most thresholds (Table 4), suggesting the method is not universally applicable. The paper should discuss when the method fails and why.

### Trivial
- The paper uses "gemma-3-it" and "gamma-34b-it" inconsistently in Table 2 (likely a typo for "gemma-3-4b-it").

## Nice-to-Haves
- Compare against a simple baseline: fine-tune on the same self-generated data but with random preference labels, to verify the verifier signal is meaningful.
- Report inference-time majority voting accuracy for the base model to compare self-evolution vs. inference-time compute.
- Analyze the quality of the verifier's feedback in RevisionGV—how often does the verifier provide correct vs. misleading feedback?

## Novel Insights
The paper's most interesting finding is the easy-to-hard generalization: training on simpler KK instances (2-3 people) using self-generated preference data transfers effectively to harder instances (4-8 people), even though the model never saw hard examples during training. This suggests that self-evolution can amplify latent reasoning capabilities that are present but not reliably expressed. The observation that verification accuracy also improves after training (Figure 2) indicates a co-evolution process where both generation and verification abilities reinforce each other, which is a non-trivial dynamical property.

## Suggestions
- Add a baseline where the same self-generated data is used for SFT with ground-truth labels (oracle) to quantify the gap between self-supervised and supervised learning.
- Add a baseline comparing SimpleGV against inference-time majority voting with the same total compute budget.
- Report results on a more diverse set of reasoning tasks beyond math and synthetic logic to better assess generalizability.

## Score and Decision
The paper presents a clean, well-executed study of a simple self-evolution framework. However, the technical novelty is limited given the extensive concurrent work in this area, and the empirical results on standard benchmarks are marginal. The strongest results are on a synthetic benchmark, and the comparisons against relevant baselines are incomplete. The paper provides useful analysis and practical insights, but does not constitute a sufficiently novel or impactful contribution for acceptance at a top venue.

MY FINAL SCORE: 4.0score</score>
MY FINAL DECISION: Reject</decision>