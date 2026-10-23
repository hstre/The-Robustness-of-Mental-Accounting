# Results: mental accounting in LLMs

## Sample per model

| model                        |   n_started |   n_complete |   n_included |   cost_usd |   n_truncated |   n_unparseable | family         |   parse_retry_rate |
|:-----------------------------|------------:|-------------:|-------------:|-----------:|--------------:|----------------:|:---------------|-------------------:|
| anthropic/claude-sonnet-5.5  |          10 |           10 |           10 |     1.26   |             0 |               0 | Anthropic      |            0       |
| cohere/command-a-plus        |          15 |           14 |           14 |     0.777  |             1 |               0 | Cohere         |            0.0248  |
| deepseek/deepseek-v4.1-flash |          15 |           15 |           15 |     0.227  |             0 |               0 | DeepSeek       |            0.00606 |
| google/gemini-3.8-flash      |          15 |           15 |           15 |     0.519  |             0 |               0 | Google         |            0       |
| meta/muse-spark-1.3          |          10 |           10 |           10 |     0.562  |             0 |               0 | Meta           |            0       |
| minimax/minimax-m3           |          15 |           15 |           15 |     0.158  |             0 |               0 | MiniMax        |            0       |
| mistralai/mistral-large-4-0  |          10 |           10 |           10 |     2.03   |             0 |               0 | Mistral        |            0       |
| moonshotai/kimi-k3           |          15 |           15 |           15 |     0.481  |             0 |               0 | Moonshot       |            0       |
| openai/gpt-6-sol             |          15 |           15 |           15 |     0.363  |             0 |               0 | OpenAI         |            0       |
| qwen/qwen3.8-max-0902        |          10 |           10 |           10 |     0.622  |             0 |               0 | Alibaba (Qwen) |            0       |
| x-ai/grok-4.7                |          10 |           10 |           10 |     0.765  |             0 |               0 | xAI            |            0       |
| z-ai/glm-5.3                 |          15 |           15 |           15 |     0.0852 |             0 |               0 | Zhipu (GLM)    |            0       |

## Pooled effects (random effects across models) vs. humans

| effect      | metric         |   k |   estimate |   ci_low |   ci_high |   tau |   I2 |   replication_rate |   human_estimate |   human_ci_low |   human_ci_high |
|:------------|:---------------|----:|-----------:|---------:|----------:|------:|-----:|-------------------:|-----------------:|---------------:|----------------:|
| MrAB_gains  | evidence ratio |  12 |       2.69 |     1.84 |      3.54 |  1.26 | 0.76 |               0.83 |             1.48 |           1.31 |            1.65 |
| MrAB_losses | evidence ratio |  12 |       1.61 |     1.08 |      2.14 |  0.67 | 0.54 |               0.67 |             2.13 |           1.99 |            2.27 |
| Game        | log OR         |  12 |       3.74 |     2.88 |      4.60 |  0.00 | 0.00 |               0.83 |             1.78 |           1.54 |            2.01 |
| Drink       | Cohen's d      |  12 |       3.35 |     2.54 |      4.16 |  1.26 | 0.82 |               1.00 |             0.76 |           0.66 |            0.86 |
| Jacket      | log OR         |  12 |       2.62 |     1.47 |      3.77 |  1.37 | 0.49 |               0.58 |             0.53 |           0.42 |            0.63 |
| Play        | log OR         |  12 |       2.97 |     1.37 |      4.58 |  2.39 | 0.74 |               0.58 |             0.58 |           0.41 |            0.75 |
| Gym         | Cohen's d      |  12 |       2.59 |     2.03 |      3.16 |  0.82 | 0.70 |               1.00 |             0.72 |           0.50 |            0.94 |
| Plane       | log OR         |  12 |       4.23 |     3.32 |      5.14 |  0.20 | 0.02 |               0.83 |             0.82 |           0.69 |            0.95 |

## Unpooled replication (95% CI > 0 in predicted direction)

Overall: 76/96 effects (79.2%); humans: 133/147 (90.5%).

| model                        | MrAB_gains   | MrAB_losses   | Game   | Drink   | Jacket   | Play   | Gym   | Plane   |
|:-----------------------------|:-------------|:--------------|:-------|:--------|:---------|:-------|:------|:--------|
| anthropic/claude-sonnet-5.5  | no           | no            | no     | yes     | no       | no     | yes   | yes     |
| cohere/command-a-plus        | yes          | yes           | yes    | yes     | no       | no     | yes   | yes     |
| deepseek/deepseek-v4.1-flash | yes          | no            | yes    | yes     | yes      | yes    | yes   | yes     |
| google/gemini-3.8-flash      | yes          | yes           | yes    | yes     | yes      | yes    | yes   | no      |
| meta/muse-spark-1.3          | yes          | yes           | yes    | yes     | yes      | yes    | yes   | yes     |
| minimax/minimax-m3           | yes          | yes           | yes    | yes     | no       | no     | yes   | yes     |
| mistralai/mistral-large-4-0  | yes          | no            | no     | yes     | no       | no     | yes   | yes     |
| moonshotai/kimi-k3           | yes          | yes           | yes    | yes     | yes      | yes    | yes   | yes     |
| openai/gpt-6-sol             | yes          | yes           | yes    | yes     | no       | no     | yes   | yes     |
| qwen/qwen3.8-max-0902        | yes          | yes           | yes    | yes     | yes      | yes    | yes   | yes     |
| x-ai/grok-4.7                | yes          | no            | yes    | yes     | yes      | yes    | yes   | no      |
| z-ai/glm-5.3                 | no           | yes           | yes    | yes     | yes      | yes    | yes   | yes     |

## Exploratory MDS

MDS variance share (dim1-3): 39.8%, 33.7%, 13.7%
