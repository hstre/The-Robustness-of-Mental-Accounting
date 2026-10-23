# Results: mental accounting in LLMs

## Sample per model

| model                        |   n_started |   n_complete |   n_included |   cost_usd |   n_truncated |   n_unparseable | family         |   parse_retry_rate |
|:-----------------------------|------------:|-------------:|-------------:|-----------:|--------------:|----------------:|:---------------|-------------------:|
| anthropic/claude-sonnet-5.5  |          10 |           10 |           10 |     1.26   |             0 |               0 | Anthropic      |             0      |
| cohere/command-a-plus        |           3 |            3 |            3 |     0.119  |             0 |               0 | Cohere         |             0.0152 |
| deepseek/deepseek-v4.1-flash |           9 |            9 |            9 |     0.146  |             0 |               0 | DeepSeek       |             0.0101 |
| google/gemini-3.8-flash      |          10 |           10 |           10 |     0.344  |             0 |               0 | Google         |             0      |
| meta/muse-spark-1.3          |          10 |           10 |           10 |     0.562  |             0 |               0 | Meta           |             0      |
| minimax/minimax-m3           |           9 |            9 |            9 |     0.0921 |             0 |               0 | MiniMax        |             0      |
| mistralai/mistral-large-4-0  |           3 |            3 |            3 |     0.577  |             0 |               0 | Mistral        |             0      |
| moonshotai/kimi-k3           |          10 |           10 |           10 |     0.327  |             0 |               0 | Moonshot       |             0      |
| openai/gpt-6-sol             |          10 |           10 |           10 |     0.241  |             0 |               0 | OpenAI         |             0      |
| qwen/qwen3.8-max-0902        |           4 |            4 |            4 |     0.245  |             0 |               0 | Alibaba (Qwen) |             0      |
| x-ai/grok-4.7                |           8 |            8 |            8 |     0.597  |             0 |               0 | xAI            |             0      |
| z-ai/glm-5.3                 |          10 |           10 |           10 |     0.0561 |             0 |               0 | Zhipu (GLM)    |             0      |

## Pooled effects (random effects across models) vs. humans

| effect      | metric         |   k |   estimate |   ci_low |   ci_high |   tau |   I2 |   replication_rate |   human_estimate |   human_ci_low |   human_ci_high |
|:------------|:---------------|----:|-----------:|---------:|----------:|------:|-----:|-------------------:|-----------------:|---------------:|----------------:|
| MrAB_gains  | evidence ratio |  12 |       2.69 |     1.84 |      3.55 |  1.13 | 0.61 |               0.75 |             1.48 |           1.31 |            1.65 |
| MrAB_losses | evidence ratio |  12 |       1.61 |     1.08 |      2.15 |  0.52 | 0.31 |               0.42 |             2.13 |           1.99 |            2.27 |
| Game        | log OR         |  12 |       3.33 |     2.39 |      4.28 |  0.00 | 0.00 |               0.67 |             1.78 |           1.54 |            2.01 |
| Drink       | Cohen's d      |  12 |       2.85 |     2.09 |      3.60 |  1.05 | 0.69 |               1.00 |             0.76 |           0.66 |            0.86 |
| Jacket      | log OR         |  12 |       2.05 |     0.89 |      3.22 |  1.30 | 0.42 |               0.25 |             0.53 |           0.42 |            0.63 |
| Play        | log OR         |  12 |       2.75 |     1.60 |      3.90 |  1.11 | 0.31 |               0.33 |             0.58 |           0.41 |            0.75 |
| Gym         | Cohen's d      |  12 |       2.52 |     1.82 |      3.21 |  0.97 | 0.67 |               0.83 |             0.72 |           0.50 |            0.94 |
| Plane       | log OR         |  12 |       3.47 |     2.54 |      4.41 |  0.00 | 0.00 |               0.58 |             0.82 |           0.69 |            0.95 |

## Unpooled replication (95% CI > 0 in predicted direction)

Overall: 58/96 effects (60.4%); humans: 133/147 (90.5%).

| model                        | MrAB_gains   | MrAB_losses   | Game   | Drink   | Jacket   | Play   | Gym   | Plane   |
|:-----------------------------|:-------------|:--------------|:-------|:--------|:---------|:-------|:------|:--------|
| anthropic/claude-sonnet-5.5  | no           | no            | no     | yes     | no       | no     | yes   | yes     |
| cohere/command-a-plus        | no           | no            | yes    | yes     | no       | no     | yes   | no      |
| deepseek/deepseek-v4.1-flash | yes          | no            | yes    | yes     | no       | yes    | yes   | yes     |
| google/gemini-3.8-flash      | yes          | yes           | yes    | yes     | no       | no     | yes   | no      |
| meta/muse-spark-1.3          | yes          | yes           | yes    | yes     | yes      | yes    | yes   | yes     |
| minimax/minimax-m3           | yes          | no            | yes    | yes     | no       | no     | no    | yes     |
| mistralai/mistral-large-4-0  | yes          | no            | no     | yes     | no       | no     | no    | no      |
| moonshotai/kimi-k3           | yes          | yes           | no     | yes     | yes      | yes    | yes   | yes     |
| openai/gpt-6-sol             | yes          | yes           | yes    | yes     | no       | no     | yes   | yes     |
| qwen/qwen3.8-max-0902        | yes          | no            | no     | yes     | yes      | yes    | yes   | no      |
| x-ai/grok-4.7                | yes          | no            | yes    | yes     | no       | no     | yes   | no      |
| z-ai/glm-5.3                 | no           | yes           | yes    | yes     | no       | no     | yes   | yes     |

## Exploratory MDS

MDS variance share (dim1-3): 39.4%, 30.7%, 12.5%
