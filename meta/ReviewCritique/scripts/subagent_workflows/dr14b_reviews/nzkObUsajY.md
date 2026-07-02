### Summary

The paper proposes a novel dual ANN-to-SNN conversion framework for large language models (LLMs), aiming to address the challenges of deploying LLMs on edge devices. The key contributions include: (1) a dual conversion approach that eliminates the need for a specially trained, conversion-friendly ANN, reducing computational costs; (2) a parameter-efficient layer-wise calibration technique to mitigate unevenness error in spike arrivals, enhancing conversion accuracy; (3) theoretical analysis demonstrating the effectiveness of the calibration method in reducing conversion errors; and (4) extensive experiments on LLaMA models showing performance comparable to state-of-the-art quantization techniques.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The dual ANN-to-SNN conversion framework is a novel approach that addresses the computational and financial impracticality of training customized LLMs for conversion. This is a significant advancement in the field of efficient LLM deployment.
2. The layer-wise calibration method is theory-backed and achieves significant conversion error reduction with minimal computational and memory overhead. This method effectively reduces unevenness error, which is a key challenge in ANN-to-SNN conversion.
3. The paper provides a comprehensive theoretical analysis of the conversion errors, including clipping error, quantization error, and unevenness error. The authors also provide a detailed analysis of the layer-wise errors and how they can be bounded.
4. The experimental results on LLaMA models show that the proposed method achieves performance comparable to state-of-the-art quantization techniques, such as PrefixQuant and DuQuant. This demonstrates the effectiveness of the proposed framework in maintaining the performance of the original LLM while converting it to an SNN.

### Weaknesses

#### Some Related Works


#### comment

1. The paper primarily evaluates the method on LLaMA models. Testing on a broader range of LLM architectures would strengthen the generalizability of the findings.
2. While the paper discusses energy efficiency, it lacks empirical measurements of energy consumption, which would provide stronger evidence for the method's practical benefits.
3. The layer-wise calibration technique, while effective, may introduce additional complexity in implementation. A more detailed discussion of the practical challenges and potential solutions would be beneficial.
4. The paper does not extensively compare the proposed method with other state-of-the-art ANN-to-SNN conversion techniques, which could provide a more comprehensive understanding of its relative advantages and limitations.

### Suggestions

To enhance the paper's impact and practical relevance, several key areas warrant further attention. Firstly, the evaluation should be broadened to include a more diverse set of LLM architectures beyond the LLaMA family. This would involve not only replicating the existing experiments on different model families, such as those based on the Transformer architecture, but also adapting the calibration technique to the specific nuances of each architecture. For example, different attention mechanisms or layer configurations might require adjustments to the calibration parameters or the training procedure. Furthermore, a detailed analysis of the computational overhead introduced by the calibration process on these different architectures would be valuable. This would provide a more comprehensive understanding of the method's generalizability and its practical applicability across a wider range of LLMs. Such an analysis should include a breakdown of the computational cost of each step in the calibration process, as well as a comparison with the computational cost of the original ANN model.

Secondly, the paper should include empirical measurements of energy consumption for the converted SNNs on actual edge devices. This would involve deploying the converted SNNs on hardware platforms representative of edge computing environments and measuring the power usage during inference. The measurements should be conducted under realistic operating conditions and should include a comparison with the energy consumption of the original ANN models. This would provide concrete evidence of the method's practical benefits and would allow for a more accurate assessment of its potential for real-world deployment. Furthermore, the authors should provide a detailed breakdown of the energy consumption for different components of the SNN, such as the synaptic operations and the neuron activations. This would help identify potential bottlenecks and areas for further optimization. The analysis should also consider the impact of different SNN parameters, such as the time step and the number of layers, on the overall energy consumption.

Finally, the paper should include a more detailed comparison with other state-of-the-art ANN-to-SNN conversion techniques. This comparison should not only focus on the final performance metrics but also on the computational cost, memory requirements, and implementation complexity of each method. For example, the authors could compare their method with techniques that use different spiking neuron models or different calibration strategies. This would provide a more comprehensive understanding of the relative advantages and limitations of the proposed method and would help position it within the broader landscape of ANN-to-SNN conversion techniques. Furthermore, the authors should discuss the potential for combining their method with other techniques to further improve performance or reduce computational cost. This could involve exploring hybrid approaches that combine the strengths of different conversion methods or developing new techniques that address the specific limitations of the proposed method.

### Questions

1. How does the proposed method perform on other LLM architectures besides LLaMA?
2. Can you provide empirical measurements of energy consumption for the converted SNNs on edge devices?
3. What are the practical challenges of implementing the layer-wise calibration technique, and how can they be addressed?
4. How does the proposed method compare with other state-of-the-art ANN-to-SNN conversion techniques in terms of computational cost and performance?

### Rating

6

### Confidence

3

**********