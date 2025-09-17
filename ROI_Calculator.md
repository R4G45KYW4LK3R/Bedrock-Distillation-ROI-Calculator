# Bedrock Distillation ROI Calculator

This repository evaluates **model distillation in Amazon Bedrock** by comparing a larger foundation model (**Llama 3 70B Instruct**) with a smaller distilled variant (**Llama 3 8B Instruct**) on the task of **text summarization**.  

The final goal is to measure **accuracy, latency, and cost trade-offs** and compute **Return on Investment (ROI)** when using distilled models.

---

## ROI Formula

<img width="788" height="95" alt="image" src="https://github.com/user-attachments/assets/b243a109-9cbd-4436-9fdc-f9724bc9fa69" />


- **Cost Savings** = Cost(70B) – Cost(8B)  
- **Accuracy Loss** = Accuracy(70B) – Accuracy(8B)  
- If there is no accuracy loss, ROI = ∞ (infinite ROI).  

---

## Experiment Setup

- **Models Used**:  
  - Llama 3 70B Instruct (baseline/original)  
  - Llama 3 8B Instruct (distilled variant)  

- **Use Case**: Text Summarization  
- **Metrics Recorded**: Input/Output Tokens, Latency, Accuracy (manual scoring), and Estimated Cost.  

---

## Sample Results (Paragraph #1)

| Metric        | Llama 3 70B | Llama 3 8B | Difference | ROI Impact |
|---------------|-------------|------------|------------|------------|
| Cost (per request) | $0.00047 | $0.00007 | ↓ 85% | Huge savings |
| Latency       | 1318 ms     | 653 ms    | ↓ 50%     | Faster |
| Accuracy (assumed) | 95%        | 90%       | -5%       | Small loss |

**ROI = 85% / 5% = 17×**  
→ The distilled 8B model is **17× more cost-effective per unit accuracy** than the 70B model.  

---


