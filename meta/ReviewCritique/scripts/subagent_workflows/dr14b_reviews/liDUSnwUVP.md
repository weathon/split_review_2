### Summary

This paper proposes a method to forecast the trajectory of a newly emerging pandemic by leveraging historical data from past global outbreaks. The authors introduce a framework called History-Guided Deep Compartmental Model (HG-DCM), which combines deep learning with epidemiological modeling. The deep learning component learns to map early-stage signals and associated metadata to the parameters of a compartmental model, which is then used to generate the predicted cumulative case curve. The authors demonstrate that HG-DCM outperforms state-of-the-art methods in early-stage COVID-19 forecasting.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper addresses a critical problem in pandemic forecasting: the lack of data in the early stages of a new outbreak. By leveraging historical data from past pandemics, the proposed method can provide more accurate and stable forecasts even when current data is minimal.
2. The integration of deep learning with epidemiological modeling is a novel approach that combines the strengths of both methods. The deep learning component learns to extract universal temporal patterns and parameter dynamics from historical data, while the compartmental model provides an interpretable framework for forecasting.
3. The authors construct a comprehensive pandemic dataset that includes time-series case and death data, along with associated pandemic- and country-level metadata, from major global outbreaks since 1990. This dataset is a valuable contribution to the field and can be used for future research.
4. The experimental results on early-stage COVID-19 forecasting demonstrate the effectiveness of the proposed method. HG-DCM consistently outperforms state-of-the-art methods, including the original DELPHI model and advanced deep learning-only models, in terms of forecasting accuracy and stability.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a detailed analysis of the computational complexity of the proposed method. It would be helpful to understand how the computational cost scales with the size of the input data and the number of parameters in the deep learning model.
2. The paper does not discuss the sensitivity of the proposed method to the choice of hyperparameters. It would be helpful to understand how the performance of the method varies with different hyperparameter settings and to provide guidelines for selecting appropriate values.
3. The paper does not explore the potential limitations of the proposed method in the context of pandemics with different characteristics. For example, it would be interesting to investigate how the method performs in the case of pandemics with different transmission dynamics or different levels of data availability.

### Suggestions

The paper should include a more thorough analysis of the computational demands of the HG-DCM framework. Specifically, the authors should provide a breakdown of the time and memory requirements for both the training and inference phases. This should include a discussion of how these costs scale with the size of the input time series data, the number of historical pandemics used for training, and the complexity of the deep learning model (e.g., number of layers, number of parameters). Furthermore, it would be beneficial to compare the computational cost of HG-DCM with that of other state-of-the-art forecasting methods, such as the original DELPHI model and deep learning-only approaches. This analysis should also consider the impact of different hardware configurations (e.g., CPU vs. GPU) on the overall computational efficiency. Such a detailed analysis would allow practitioners to better assess the feasibility of using HG-DCM in resource-constrained environments and to make informed decisions about model deployment.

To address the sensitivity of the method to hyperparameter choices, the authors should conduct a more extensive hyperparameter tuning study. This should involve systematically varying key hyperparameters, such as the learning rate, batch size, and the number of layers in the deep learning component, and evaluating their impact on forecasting performance. The authors should also explore different optimization algorithms and regularization techniques. The results of this study should be presented in a clear and concise manner, perhaps using tables or graphs, to illustrate the sensitivity of the method to different hyperparameter settings. Furthermore, the authors should provide practical guidelines for selecting appropriate hyperparameter values based on the characteristics of the input data and the desired forecasting performance. This would make the method more accessible to practitioners who may not have extensive experience with deep learning model tuning.

Finally, the paper should include a more in-depth discussion of the potential limitations of the HG-DCM framework when applied to pandemics with different characteristics. For example, the authors should investigate how the method performs when applied to pandemics with different transmission dynamics, such as those caused by airborne viruses versus vector-borne diseases. They should also explore the impact of different levels of data availability and quality on the forecasting performance. This could involve simulating scenarios with missing or noisy data and evaluating the robustness of the method under these conditions. Furthermore, the authors should discuss the potential for incorporating additional data sources, such as mobility data or genomic data, to improve the forecasting performance of the method. This would help to establish the generalizability of the method and to identify potential areas for future research.

### Questions

1. How does the computational cost of HG-DCM compare to other state-of-the-art forecasting methods?
2. How sensitive is the performance of HG-DCM to the choice of hyperparameters?
3. How does the performance of HG-DCM vary when applied to pandemics with different characteristics?

### Rating

6

### Confidence

3

**********