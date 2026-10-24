# Results: mental accounting in LLMs

## Sample per model

| model                        |   n_started |   n_complete |   n_included |   cost_usd |   n_truncated |   n_unparseable | family         |   parse_retry_rate |
|:-----------------------------|------------:|-------------:|-------------:|-----------:|--------------:|----------------:|:---------------|-------------------:|
| anthropic/claude-sonnet-5.5  |           3 |            3 |            3 |     0.516  |             0 |               0 | Anthropic      |             0      |
| cohere/command-a-plus        |           3 |            3 |            2 |     0.229  |             0 |               0 | Cohere         |             0.0758 |
| deepseek/deepseek-v4.1-flash |           3 |            1 |            1 |     0.0795 |             2 |               0 | DeepSeek       |             0.0667 |
| google/gemini-3.8-flash      |           3 |            3 |            3 |     0.109  |             0 |               0 | Google         |             0      |
| meta/muse-spark-1.3          |           3 |            3 |            3 |     0.167  |             0 |               0 | Meta           |             0      |
| minimax/minimax-m3           |           3 |            3 |            3 |     0.0375 |             0 |               0 | MiniMax        |             0      |
| mistralai/mistral-large-4-0  |           3 |            3 |            3 |     0.652  |             0 |               0 | Mistral        |             0.0303 |
| moonshotai/kimi-k3           |           3 |            3 |            3 |     0.189  |             0 |               0 | Moonshot       |             0      |
| openai/gpt-6-sol             |           3 |            3 |            3 |     0.0803 |             0 |               0 | OpenAI         |             0      |
| qwen/qwen3.8-max-0902        |           3 |            3 |            3 |     0.2    |             0 |               0 | Alibaba (Qwen) |             0      |
| x-ai/grok-4.7                |           3 |            3 |            3 |     0.37   |             0 |               0 | xAI            |             0      |
| z-ai/glm-5.3                 |           3 |            3 |            3 |     0.013  |             0 |               0 | Zhipu (GLM)    |             0      |

## Pooled effects (random effects across models) vs. humans

| effect      | metric         |   k |   estimate |   ci_low |   ci_high |   tau |   I2 |   replication_rate |   human_estimate |   human_ci_low |   human_ci_high |
|:------------|:---------------|----:|-----------:|---------:|----------:|------:|-----:|-------------------:|-----------------:|---------------:|----------------:|
| MrAB_gains  | evidence ratio |  11 |       0.16 |    -0.73 |      1.06 |  0.00 | 0.00 |               0.00 |             1.48 |           1.31 |            1.65 |
| MrAB_losses | evidence ratio |  11 |       0.16 |    -0.73 |      1.06 |  0.00 | 0.00 |               0.00 |             2.13 |           1.99 |            2.27 |
| Game        | log OR         |  11 |       0.16 |    -1.01 |      1.34 |  0.00 | 0.00 |               0.00 |             1.78 |           1.54 |            2.01 |
| Drink       | Cohen's d      |   9 |       0.48 |    -0.27 |      1.23 |  0.68 | 0.37 |               0.09 |             0.76 |           0.66 |            0.86 |
| Jacket      | log OR         |  11 |       0.14 |    -0.99 |      1.28 |  0.00 | 0.00 |               0.00 |             0.53 |           0.42 |            0.63 |
| Play        | log OR         |  11 |       0.00 |    -1.27 |      1.27 |  0.00 | 0.00 |               0.00 |             0.58 |           0.41 |            0.75 |
| Gym         | Cohen's d      |   5 |       1.07 |     0.29 |      1.84 |  0.00 | 0.00 |               0.00 |             0.72 |           0.50 |            0.94 |
| Plane       | log OR         |  11 |       0.81 |    -0.21 |      1.82 |  0.00 | 0.00 |               0.00 |             0.82 |           0.69 |            0.95 |

## Unpooled replication (95% CI > 0 in predicted direction)

Overall: 1/88 effects (1.1%); humans: 133/147 (90.5%).

| model                       | MrAB_gains   | MrAB_losses   | Game   | Drink   | Jacket   | Play   | Gym   | Plane   |
|:----------------------------|:-------------|:--------------|:-------|:--------|:---------|:-------|:------|:--------|
| anthropic/claude-sonnet-5.5 | no           | no            | no     | no      | no       | no     | no    | no      |
| cohere/command-a-plus       | no           | no            | no     | no      | no       | no     | no    | no      |
| google/gemini-3.8-flash     | no           | no            | no     | no      | no       | no     | no    | no      |
| meta/muse-spark-1.3         | no           | no            | no     | no      | no       | no     | no    | no      |
| minimax/minimax-m3          | no           | no            | no     | yes     | no       | no     | no    | no      |
| mistralai/mistral-large-4-0 | no           | no            | no     | no      | no       | no     | no    | no      |
| moonshotai/kimi-k3          | no           | no            | no     | no      | no       | no     | no    | no      |
| openai/gpt-6-sol            | no           | no            | no     | no      | no       | no     | no    | no      |
| qwen/qwen3.8-max-0902       | no           | no            | no     | no      | no       | no     | no    | no      |
| x-ai/grok-4.7               | no           | no            | no     | no      | no       | no     | no    | no      |
| z-ai/glm-5.3                | no           | no            | no     | no      | no       | no     | no    | no      |

## Exploratory MDS

MDS variance share (dim1-3): 59.3%, 34.5%, 6.2%
