# Results: mental accounting in LLMs

## Sample per model

| model                        |   n_started |   n_complete |   n_included |   cost_usd |   n_truncated |   n_unparseable | family         |   parse_retry_rate |
|:-----------------------------|------------:|-------------:|-------------:|-----------:|--------------:|----------------:|:---------------|-------------------:|
| anthropic/claude-sonnet-5.5  |           3 |            3 |            3 |     0.386  |             0 |               0 | Anthropic      |             0      |
| cohere/command-a-plus        |           3 |            3 |            3 |     0.17   |             0 |               0 | Cohere         |             0.0455 |
| deepseek/deepseek-v4.1-flash |           3 |            3 |            3 |     0.0513 |             0 |               0 | DeepSeek       |             0      |
| google/gemini-3.8-flash      |           3 |            3 |            3 |     0.103  |             0 |               0 | Google         |             0      |
| meta/muse-spark-1.3          |           3 |            3 |            3 |     0.197  |             0 |               0 | Meta           |             0      |
| minimax/minimax-m3           |           3 |            3 |            3 |     0.0824 |             0 |               0 | MiniMax        |             0.0303 |
| mistralai/mistral-large-4-0  |           3 |            3 |            3 |     0.662  |             0 |               0 | Mistral        |             0      |
| moonshotai/kimi-k3           |           3 |            3 |            3 |     0.133  |             0 |               0 | Moonshot       |             0      |
| openai/gpt-6-sol             |           3 |            3 |            3 |     0.0757 |             0 |               0 | OpenAI         |             0      |
| qwen/qwen3.8-max-0902        |           3 |            3 |            3 |     0.194  |             0 |               0 | Alibaba (Qwen) |             0      |
| x-ai/grok-4.7                |           3 |            3 |            3 |     0.303  |             0 |               0 | xAI            |             0.0152 |
| z-ai/glm-5.3                 |           3 |            3 |            3 |     0.0334 |             0 |               0 | Zhipu (GLM)    |             0      |

## Pooled effects (random effects across models) vs. humans

| effect      | metric         |   k |   estimate |   ci_low |   ci_high |   tau |   I2 |   replication_rate |   human_estimate |   human_ci_low |   human_ci_high |
|:------------|:---------------|----:|-----------:|---------:|----------:|------:|-----:|-------------------:|-----------------:|---------------:|----------------:|
| MrAB_gains  | evidence ratio |  12 |       2.12 |     1.49 |      2.75 |  0.00 | 0.00 |               0.50 |             1.48 |           1.31 |            1.65 |
| MrAB_losses | evidence ratio |  12 |       1.81 |     1.13 |      2.49 |  0.00 | 0.00 |               0.50 |             2.13 |           1.99 |            2.27 |
| Game        | log OR         |  12 |       1.82 |     0.78 |      2.86 |  0.00 | 0.00 |               0.08 |             1.78 |           1.54 |            2.01 |
| Drink       | Cohen's d      |  11 |       2.68 |     1.49 |      3.87 |  1.52 | 0.63 |               0.67 |             0.76 |           0.66 |            0.86 |
| Jacket      | log OR         |  12 |       2.40 |     1.29 |      3.51 |  0.00 | 0.00 |               0.00 |             0.53 |           0.42 |            0.63 |
| Play        | log OR         |  12 |       1.93 |     0.84 |      3.03 |  0.00 | 0.00 |               0.00 |             0.58 |           0.41 |            0.75 |
| Gym         | Cohen's d      |  10 |       2.04 |     1.39 |      2.69 |  0.14 | 0.02 |               0.42 |             0.72 |           0.50 |            0.94 |
| Plane       | log OR         |  12 |       2.76 |     1.66 |      3.86 |  0.00 | 0.00 |               0.00 |             0.82 |           0.69 |            0.95 |

## Unpooled replication (95% CI > 0 in predicted direction)

Overall: 26/96 effects (27.1%); humans: 133/147 (90.5%).

| model                        | MrAB_gains   | MrAB_losses   | Game   | Drink   | Jacket   | Play   | Gym   | Plane   |
|:-----------------------------|:-------------|:--------------|:-------|:--------|:---------|:-------|:------|:--------|
| anthropic/claude-sonnet-5.5  | no           | no            | no     | yes     | no       | no     | yes   | no      |
| cohere/command-a-plus        | no           | no            | no     | yes     | no       | no     | no    | no      |
| deepseek/deepseek-v4.1-flash | no           | no            | no     | yes     | no       | no     | yes   | no      |
| google/gemini-3.8-flash      | yes          | yes           | no     | no      | no       | no     | no    | no      |
| meta/muse-spark-1.3          | yes          | yes           | no     | yes     | no       | no     | yes   | no      |
| minimax/minimax-m3           | no           | no            | no     | no      | no       | no     | no    | no      |
| mistralai/mistral-large-4-0  | no           | no            | no     | yes     | no       | no     | no    | no      |
| moonshotai/kimi-k3           | no           | yes           | no     | yes     | no       | no     | no    | no      |
| openai/gpt-6-sol             | yes          | yes           | yes    | no      | no       | no     | no    | no      |
| qwen/qwen3.8-max-0902        | yes          | yes           | no     | yes     | no       | no     | no    | no      |
| x-ai/grok-4.7                | yes          | yes           | no     | yes     | no       | no     | yes   | no      |
| z-ai/glm-5.3                 | yes          | no            | no     | no      | no       | no     | yes   | no      |

## Exploratory MDS

MDS variance share (dim1-3): 42.5%, 28.3%, 18.8%
