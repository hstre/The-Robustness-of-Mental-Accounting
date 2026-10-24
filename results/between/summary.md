# Results: mental accounting in LLMs

## Sample per model

| model                        |   n_started |   n_complete |   n_included |   cost_usd |   n_truncated |   n_unparseable | family         |   parse_retry_rate |
|:-----------------------------|------------:|-------------:|-------------:|-----------:|--------------:|----------------:|:---------------|-------------------:|
| anthropic/claude-sonnet-5.5  |           3 |            3 |            3 |     0.17   |             0 |               0 | Anthropic      |             0      |
| cohere/command-a-plus        |           3 |            3 |            3 |     0.0674 |             0 |               0 | Cohere         |             0.0222 |
| deepseek/deepseek-v4.1-flash |           3 |            3 |            3 |     0.0208 |             0 |               0 | DeepSeek       |             0      |
| google/gemini-3.8-flash      |           3 |            3 |            3 |     0.0434 |             0 |               0 | Google         |             0      |
| meta/muse-spark-1.3          |           3 |            3 |            3 |     0.102  |             0 |               0 | Meta           |             0      |
| minimax/minimax-m3           |           3 |            3 |            3 |     0.0142 |             0 |               0 | MiniMax        |             0      |
| mistralai/mistral-large-4-0  |           3 |            3 |            3 |     0.414  |             0 |               0 | Mistral        |             0.0222 |
| moonshotai/kimi-k3           |           3 |            3 |            3 |     0.0787 |             0 |               0 | Moonshot       |             0      |
| openai/gpt-6-sol             |           3 |            3 |            3 |     0.0499 |             0 |               0 | OpenAI         |             0      |
| qwen/qwen3.8-max-0902        |           3 |            3 |            3 |     0.115  |             0 |               0 | Alibaba (Qwen) |             0      |
| x-ai/grok-4.7                |           3 |            3 |            3 |     0.144  |             0 |               0 | xAI            |             0      |
| z-ai/glm-5.3                 |           3 |            3 |            3 |     0.013  |             0 |               0 | Zhipu (GLM)    |             0      |

## Pooled effects (random effects across models) vs. humans

| effect      | metric         |   k |   estimate |   ci_low |   ci_high |    tau |     I2 |   replication_rate |   human_estimate |   human_ci_low |   human_ci_high |
|:------------|:---------------|----:|-----------:|---------:|----------:|-------:|-------:|-------------------:|-----------------:|---------------:|----------------:|
| MrAB_gains  | evidence ratio |  12 |       2.75 |     2.09 |      3.42 |   0.00 |   0.00 |               0.92 |             1.48 |           1.31 |            1.65 |
| MrAB_losses | evidence ratio |  12 |       1.37 |     0.65 |      2.10 |   0.00 |   0.00 |               0.25 |             2.13 |           1.99 |            2.27 |
| Game        | log OR         |  12 |       0.79 |    -0.36 |      1.93 |   0.00 |   0.00 |               0.00 |             1.78 |           1.54 |            2.01 |
| Drink       | Cohen's d      |   0 |     nan    |   nan    |    nan    | nan    | nan    |               0.00 |             0.76 |           0.66 |            0.86 |
| Jacket      | log OR         |   9 |       1.32 |    -0.13 |      2.77 |   0.00 |   0.00 |               0.00 |             0.53 |           0.42 |            0.63 |
| Play        | log OR         |  11 |       0.64 |    -0.67 |      1.96 |   0.00 |   0.00 |               0.00 |             0.58 |           0.41 |            0.75 |
| Gym         | Cohen's d      |   0 |     nan    |   nan    |    nan    | nan    | nan    |               0.00 |             0.72 |           0.50 |            0.94 |
| Plane       | log OR         |   8 |       1.90 |     0.34 |      3.46 |   0.00 |   0.00 |               0.00 |             0.82 |           0.69 |            0.95 |

## Unpooled replication (95% CI > 0 in predicted direction)

Overall: 14/96 effects (14.6%); humans: 133/147 (90.5%).

| model                        | MrAB_gains   | MrAB_losses   | Game   | Drink   | Jacket   | Play   | Gym   | Plane   |
|:-----------------------------|:-------------|:--------------|:-------|:--------|:---------|:-------|:------|:--------|
| anthropic/claude-sonnet-5.5  | yes          | no            | no     | no      | no       | no     | no    | no      |
| cohere/command-a-plus        | no           | no            | no     | no      | no       | no     | no    | no      |
| deepseek/deepseek-v4.1-flash | yes          | no            | no     | no      | no       | no     | no    | no      |
| google/gemini-3.8-flash      | yes          | no            | no     | no      | no       | no     | no    | no      |
| meta/muse-spark-1.3          | yes          | yes           | no     | no      | no       | no     | no    | no      |
| minimax/minimax-m3           | yes          | yes           | no     | no      | no       | no     | no    | no      |
| mistralai/mistral-large-4-0  | yes          | no            | no     | no      | no       | no     | no    | no      |
| moonshotai/kimi-k3           | yes          | no            | no     | no      | no       | no     | no    | no      |
| openai/gpt-6-sol             | yes          | yes           | no     | no      | no       | no     | no    | no      |
| qwen/qwen3.8-max-0902        | yes          | no            | no     | no      | no       | no     | no    | no      |
| x-ai/grok-4.7                | yes          | no            | no     | no      | no       | no     | no    | no      |
| z-ai/glm-5.3                 | yes          | no            | no     | no      | no       | no     | no    | no      |
