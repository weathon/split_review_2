### Summary

This paper proposes a new method for quantum state preparation. The authors first provide a unified framework for existing approximate quantum loaders (AQLs), and then derive theoretical bounds on the approximation error in terms of the entanglement measure. Based on this analysis, they propose AQER, a scalable AQL that constructs the loading circuit by systematically reducing entanglement in target states. The authors demonstrate the effectiveness of AQER through extensive experiments on various datasets, showing that it outperforms existing methods in both accuracy and gate efficiency.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. Theoretical Contribution: The paper provides a unified framework for AQLs and establishes information-theoretic bounds on the approximation error, which is a significant theoretical contribution to the field.
2. Novel Method: AQER is a novel AQL method that effectively balances fidelity and circuit complexity, which is crucial for practical quantum computing.
3. Empirical Validation: The authors conduct thorough experiments on diverse datasets, demonstrating AQER's superior performance compared to existing methods.

### Weaknesses

#### Some Related Works


#### comment

1. Theoretical Assumptions: The information-theoretic bounds derived in the paper may rely on certain assumptions that could limit their applicability in real-world scenarios. It would be beneficial to discuss the robustness of these bounds under different conditions and potential violations of these assumptions.
2. Practical Implementation: While the paper demonstrates the effectiveness of AQER through simulations, the practical implementation on actual quantum hardware may face challenges such as noise and decoherence. A discussion on the robustness of AQER to these factors and potential mitigation strategies would strengthen the paper.
3. Comparison with Other Methods: Although AQER is compared with some existing AQL methods, a more comprehensive comparison with a wider range of state preparation techniques could provide a more complete picture of its advantages and limitations.
4. Generalizability: The paper primarily focuses on specific datasets. It would be useful to discuss the generalizability of AQER to other types of quantum data and potential applications in different domains of quantum computing.
5. Resource Requirements: While AQER is shown to be resource-efficient, a detailed analysis of its computational and quantum resource requirements, especially for large-scale systems, would be beneficial.

### Suggestions

The paper would benefit from a more detailed discussion of the assumptions underlying the derived information-theoretic bounds. Specifically, the authors should elaborate on the conditions under which these bounds hold and the potential impact of violating these assumptions. For instance, the bounds might be based on idealized scenarios that do not fully capture the complexities of real-world quantum systems. A thorough analysis of the sensitivity of the bounds to various factors, such as the specific entanglement structure of the target state or the presence of noise, would be valuable. Furthermore, it would be helpful to explore alternative theoretical frameworks that could provide more robust guarantees in practical settings. This could involve investigating different entanglement measures or considering the effects of noise and decoherence directly in the theoretical analysis. A more nuanced understanding of the limitations of the current theoretical framework would significantly enhance the paper's impact.

To strengthen the practical relevance of the work, the authors should provide a more in-depth analysis of the resource requirements of AQER, particularly for large-scale systems. This should include a detailed breakdown of the computational cost associated with each step of the algorithm, such as the entanglement reduction process and the optimization of the loading circuit. It would be beneficial to quantify the number of qubits, the number of quantum gates, and the coherence time required for AQER to achieve a desired level of accuracy. Additionally, the authors should discuss the scalability of the algorithm with respect to the size of the target state and the complexity of the entanglement structure. A comparison of the resource requirements of AQER with those of other state preparation techniques would also be valuable. This analysis should consider both the theoretical scaling and the practical limitations imposed by current quantum hardware.

Finally, the paper should include a more comprehensive discussion of the generalizability of AQER to different types of quantum data and potential applications. While the authors demonstrate the effectiveness of AQER on specific datasets, it is important to explore its performance on a wider range of quantum states, including those with different entanglement properties and those arising from different physical systems. The authors should also discuss the potential for adapting AQER to different quantum computing tasks, such as quantum simulation or quantum machine learning. This could involve investigating how the algorithm can be modified to accommodate different types of target states or how its performance can be optimized for specific applications. A more thorough exploration of the generalizability of AQER would significantly broaden the scope and impact of the paper.

### Questions

1. How do the information-theoretic bounds derived in the paper hold up under different noise models and varying levels of quantum decoherence? Are there specific types of noise that AQER is more susceptible to, and if so, how can these be mitigated?
2. Can the authors provide a more detailed analysis of the computational complexity of AQER, especially in terms of the number of iterations required in Step I and the optimization process in Step III? How does this complexity scale with the number of qubits and the entanglement entropy of the target state?
3. How does AQER perform when applied to highly entangled states or states with specific symmetries? Are there any known classes of quantum states for which AQER might not be the most efficient approach, and if so, what alternative methods would be more suitable?
4. The paper mentions that AQER can be used for both classical and quantum data loading. Can the authors provide more details on how the method adapts to these different types of data? Are there any specific challenges or advantages when using AQER for quantum data as opposed to classical data?
5. For downstream tasks, how sensitive is the performance of AQER to the choice of the number of iterations T? Is there a systematic way to determine the optimal T for a given task and dataset, or does it require extensive hyperparameter tuning?

### Rating

6

### Confidence

3

**********