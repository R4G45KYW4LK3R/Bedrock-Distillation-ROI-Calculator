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

### Observations
- Latency increases with larger models.  
- Output length varied slightly, with 70B producing a more detailed summary.
- The **8B model** was faster and significantly cheaper (~6.5x lower cost)
- Billing data is not instant. AWS Bedrock usage costs appear in the **Billing & Cost Management Dashboard** after ~24 hours.

### Comparison
- Accuracy → 8B: good enough detail, 70B: overly detailed
- Latency → 8B: 653ms, 70B: 1318ms
- Cost → 70B ≈ 6.5× more expensive than 8B for this input/output size
  
- (Since very tiny tests were run, costs are minimal hence, it is calculated via manually estimate using token counts × pricing.
- (Source: AWS Bedrock Pricing)

Llama 3 8B Instruct
Input: $0.0004 per 1,000 tokens
Output: $0.0006 per 1,000 tokens
Case 1 Total ≈ $0.0000714

Llama 3 70B Instruct
Input: $0.00265 per 1,000 tokens
Output: $0.0035 per 1,000 tokens
Case 1 Total ≈ $0.0004699
 

## Next Steps
1. Run additional test cases with different paragraphs/domains.  
2. Record accuracy (manual scoring or automatic metrics like ROUGE).  
3. Add cost estimates once billing reports update.  
4. Build an **ROI Calculator** that compares cost savings and accuracy trade-offs between 70B and 8B.  

