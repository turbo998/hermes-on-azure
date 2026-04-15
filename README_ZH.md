# Hermes Agent on Azure Workshop

[English](README.md) | 中文

这是一个面向客户技术团队的 **Hermes Agent on Azure** workshop 仓库，用于在 Azure 上设计、部署、演示 Hermes Agent，并对齐：

- **CAF（Cloud Adoption Framework）**
- **WAF（Well-Architected Framework）**

本项目参考了 AWS 示例：
<https://github.com/aws-samples/sample-host-hermesagent-on-amazon-bedrock-agentcore>

但这里的目标是把方案完整改造成 Azure 版本，并沉淀为客户可看的 workshop 仓库。

---

## 这个仓库要解决什么问题

很多客户会问：

- Hermes Agent 能不能放到 Azure 上？
- 如果要走企业级架构，身份、密钥、存储、监控怎么设计？
- 如果要做 workshop，怎样把方案讲清楚而不是只讲一个 demo？

这个仓库就是为这些问题准备的。

---

## 目标架构

```text
Telegram / Slack / Discord / 飞书 / 钉钉 / 微信类渠道
                        |
                        v
               Azure API Management
                        |
                        v
             Azure Container Apps Ingress
                        |
                        v
             Hermes Agent Runtime Container
                |         |         |
                v         v         v
        Azure Blob   Key Vault   Azure Monitor
        Storage      + MI        + Log Analytics
```

---

## 分阶段交付方式

这个仓库按阶段建设，确保随时可恢复：

### Phase A — 基础文档层
- README
- 中文 README
- 架构设计文档
- 部署手册

### Phase B — 基础设施层
- Bicep
- Terraform
- 部署/清理脚本

### Phase C — Runtime / Demo 层
- Azure bridge
- provider 接入
- demo 脚本

### Phase D — Workshop 交付层
- 讲师手册
- 学员手册
- Slides 大纲

---

## Azure 对应关系

| AWS 示例 | Azure 设计 |
|---|---|
| Bedrock AgentCore | Azure Container Apps |
| Bedrock Claude | Azure AI Foundry / Azure OpenAI |
| S3 | Azure Blob Storage |
| Secrets Manager | Azure Key Vault |
| API Gateway + Lambda | Azure API Management + Container Apps |
| CloudWatch | Azure Monitor + Log Analytics |
| IAM | Managed Identity + RBAC |
| CDK | Bicep + Terraform |

---

## Workshop 目标

这套 workshop 最终希望让客户理解：

- Hermes Agent 如何落在 Azure
- 为什么方案要对齐 CAF / WAF
- Azure 上的身份、密钥、存储、监控如何组合
- 如何把它变成一套客户可演示、可交付、可继续扩展的 repo
