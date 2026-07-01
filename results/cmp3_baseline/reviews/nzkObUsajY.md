## Summary
This paper proposes a dual ANN-to-SNN conversion framework for large language models (LLMs). Instead of training a conversion-friendly ANN, it starts from a training-free static quantized LLM and uses an Integer Spiking (IS) neuron with multi‑hierarchical thresholds to approximate the quantization function. A parameter‑efficient, layer‑wise calibration of threshold and initial membrane potential is introduced to reduce conversion errors—especially unevenness error—with theoretical bounds. Experiments on LLaMA‑2 and LLaMA‑3 show that the converted SNN achieves accuracy close to state‑of‑the‑art quantization methods.

## Strengths
- **Novel pipeline that avoids costly ANN re‑training:** The dual conversion (quantization → SNN) eliminates the need for a conversion‑specific LLM, which is a significant practical advantage for large models.
- **Parameter‑efficient calibration:** The method fine‑tunes only thresholds and initial membrane potentials per layer, using far fewer parameters than weight‑based calibration while maintaining competitive accuracy.
- **Theoretical grounding:** The paper provides a formal analysis of conversion error (clipping, quantization, unevenness) and derives an upper bound that motivates the layer‑wise calibration.
- **Comprehensive experiments on modern LLMs:** Results on LLaMA‑2‑7B and LLaMA‑3‑8B across five zero‑shot reasoning tasks and perplexity demonstrate the method works at scale with acceptable degradation.

## Weaknesses

### Fatal
None.

### Major
- **Missing comparison to other SNN conversion methods for LLMs.** The paper compares only to quantization baselines (PrefixQuant, DuQuant). Without evaluating against prior SNN‑conversion work (e.g., SpikeZIP), it is unclear whether the proposed approach advances the state of the art in spiking LLM conversion.
- **No energy consumption analysis.** The entire motivation for SNNs is low power edge deployment, yet the paper provides no measurements or even analytical estimates of energy usage. The efficiency claim is unsubstantiated.
- **Calibration data and cost are not specified.** The calibration step requires some data (e.g., a few hundred samples), but the paper does not state how much, what kind, or the computational overhead. This hinders reproducibility and practical assessment.

### Minor
- **The “dual” terminology is confusing.** The pipeline is essentially a two‑step process (first quantize, then convert), not a “dual” framework in a symmetric sense. The name does not add clarity.
- **Figure 3 is visually misleading.** Dual axes with different scales (log left, linear right) make the comparison between ANN‑vs‑QANN error and ANN‑vs‑SNN error difficult to interpret. The claim that unevenness error dominates is not convincingly supported by the figure alone.
- **Performance degrades as time‑step T increases.** While acknowledged, the paper does not provide a deeper analysis of why this happens besides citing unevenness error, and whether the calibration can be improved to avoid this trend.

### Trivial
- Inconsistent casing: “LLaMA‑2‑7B” vs “LLAMA‑2‑7B” in tables.

## Nice‑to‑Haves
- Include at least one spike‑based conversion baseline (e.g., SpikeZIP) in the main comparison.
- Provide energy measurements or simple FLOPs‑to‑spike‑operations conversion to support the efficiency argument.
- Detail the calibration dataset (size, source, number of batches) and the time required for calibration.
- Add an ablation showing how much the calibration improves each error type separately.

## Novel Insights
None beyond the paper’s own contributions.

## Suggestions
- Add a comparison table that includes existing SNN‑conversion methods for LLMs (e.g., SpikeZIP). If such methods are not directly applicable, discuss why and still report numbers if possible.
- Estimate the theoretical energy advantage of the spiking model over its quantized counterpart (e.g., using spike‑rate statistics from the calibration data).
- Specify the calibration data source (e.g., 128 samples from WikiText‑2) and the batch size; include this in the experimental setup.
- Improve Figure 3 either by using a single set of axes or by clearly separating the two measures in different subplots with comparable scales.

## Score and Decision
Based on the analysis, the paper presents a practical and theoretically grounded conversion pipeline for spiking LLMs, with strong experiments and parameter efficiency. However, the lack of comparison to prior SNN‑conversion work and missing energy validation are significant gaps that prevent a higher rating. The paper is marginally acceptable.

MY FINAL SCORE: <score>6.0</score>  
MY FINAL DECISION: <decision>Accept</decision>