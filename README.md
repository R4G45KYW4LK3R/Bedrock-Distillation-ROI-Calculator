# Bedrock-Distillation-ROI-Calculator
This file will have tasks, updates and readme files relating to persistent systems internship

# Bedrock Distillation Evaluation – Summarization Use Case

## Project Overview
This project explores **model distillation in Amazon Bedrock** by comparing performance between a larger foundation model and a smaller variant. The goal is to evaluate **accuracy, latency, and cost trade-offs** and eventually build an **ROI Calculator** for model distillation.

## Models Used
- **Llama 3 70B Instruct** – Large foundation model (baseline/original).  
- **Llama 3 8B Instruct** – Smaller model, treated as the distilled version for this study.  

Both models were accessed via **Amazon Bedrock**.

## Use Case: Text Summarization
We tested summarization of sample paragraphs using both models. The same text input was sent to each model.

### Experiment 1: Sample Paragraph #1
| Model              | Input Tokens | Output Tokens | Latency (ms) | Observations |
|--------------------|--------------|---------------|--------------|--------------|
| Llama 3 8B Instruct | 69           | 73            | 653          | Faster, concise output |
| Llama 3 70B Instruct | 69           | 82            | 1318         | Longer summary, higher latency |

### Notes
- Latency increases with larger models.  
- Output length varied slightly, with 70B producing a more detailed summary.  
- Billing data is not instant. AWS Bedrock usage costs appear in the **Billing & Cost Management Dashboard** after ~24 hours.  
 

## Next Steps
1. Run additional test cases with different paragraphs/domains.  
2. Record accuracy (manual scoring or automatic metrics like ROUGE).  
3. Add cost estimates once billing reports update.  
4. Build an **ROI Calculator** that compares cost savings and accuracy trade-offs between 70B and 8B.  

