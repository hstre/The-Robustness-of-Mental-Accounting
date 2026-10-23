# Mental Accounting in LLMs – Replikation von Priolo et al. (2026)

Nachbau der Studie *The Robustness of Mental Accounting Across 21 Countries*
(Priolo et al., Journal of Consumer Research, 2026, doi:10.1093/jcr/ucag022) mit
Sprachmodellen über die OpenRouter-API. **Modelle ersetzen die Länder**, unabhängige
Gespräche (Samples bei Temperatur 1) ersetzen die Teilnehmenden.

## Was 1:1 übernommen ist

| Paper | Hier |
|---|---|
| 7 Szenarien, 17 Items (Table 1), Wortlaut der englischen Version | identisch (`ma_llm/scenarios.py`) |
| Within-subjects: jede Person sieht alle Bedingungen | jedes Gespräch sieht alle 17 Items |
| 4 Blöcke (5/4/4/4), Blockreihenfolge randomisiert, Reihenfolge im Block fest, Bedingungen eines Szenarios nie im selben Block | identisch (konkrete Blockzuordnung rekonstruiert, s. u.) |
| Eine Seite pro Szenario, frühere Antworten bleiben „im Gedächtnis“ | ein Chat-Turn pro Seite, Verlauf bleibt im Kontext |
| Danach Financial Literacy (4 Items) und Ernsthaftigkeitsfrage (1–5) | identisch |
| Ausschluss: Completion < 100 % oder Ernsthaftigkeit < 4 | identisch (nicht parsebare Antwort nach 2 Nachfragen = unvollständig) |
| Zielgröße 250 pro Land | `n_participants: 250` pro Modell |
| Effektmaße: Evidence Ratio (MrAB, vs. Zufall 1/9), log OR (Game, Jacket, Play, Plane), Cohen's d (Drink: log-Preis; Gym) | identisch |
| Replikation = 95 %-Intervall schließt 0 in vorhergesagter Richtung aus | identisch |
| Hierarchische Meta-Analyse über Länder | Random-Effects-Meta-Analyse über Modelle |
| Between-subjects-Check über die zuerst gesehene Bedingung (Jacket, Play, Plane) | identisch |
| Explorative MDS über Länder × Szenarien | identisch über Modelle × Szenarien |

## Abweichungen (bewusst oder unvermeidbar)

1. **Statistik frequentistisch statt Bayes (brms/Stan).** Statt N(0, 2.5)-Priors wird bei
   binären Outcomes eine +0.5-Korrektur verwendet. Bei n = 250 ist der Unterschied klein,
   aber nicht null – vor allem bei Modellen, die fast deterministisch antworten.
2. **Geldbeträge:** Verwendet werden die Beträge aus Table 1. Die tatsächlich in den USA
   gezeigten, einkommensangepassten Beträge und die exakten Financial-Literacy-Items liegen
   nur auf OSF (https://osf.io/kgesy). Wenn ihr die OSF-Materialien habt, bitte in
   `scenarios.py` übernehmen.
3. **Blockzuordnung** der 17 Items ist aus den Angaben im Paper rekonstruiert, nicht die Originaldatei.
4. **Gym:** Das Paper nennt nicht, welches der drei Items (oder welcher Index) in das d
   eingeht. Primär ausgewertet wird „I feel like I wasted $20“.
5. **Game:** 12 Preise pro Person; Outcome „Preis ≥ Marktwert“ ($5 bzw. $10), Effekt
   Fremder vs. Freund; SE per Cluster-Bootstrap über Personen.
6. **Keine Demografie, kein GDP, keine LOI-Ausschlüsse** – für LLMs sinnlos. Einwilligung
   wird nicht abgefragt, nur eine kurze Einleitung.
7. **Zufallsvariation ≠ Personenvariation.** Die Varianz zwischen Samples eines Modells ist
   keine Populationsvarianz. Konfidenzintervalle pro Modell beschreiben die Stabilität des
   Modellverhaltens, nicht eine Population. Das muss in jeder Interpretation stehen.
8. `openai/gpt-6-sol` und `anthropic/claude-sonnet-5.5` akzeptieren über OpenRouter keinen
   `temperature`-Parameter (laut `check`); dort gilt der Provider-Default.
9. Reasoning wird einheitlich auf `effort: low` gesetzt (konfigurierbar). Das beeinflusst
   die Antworten vermutlich; ggf. als eigene Bedingung variieren.

## Modelle (12 Familien)

Konfiguriert in `config/study.yaml`, geprüft am 23.10.2026 gegen die OpenRouter-Modellliste:

OpenAI `gpt-6-sol` · Anthropic `claude-sonnet-5.5` · Google `gemini-3.8-flash` ·
Meta `muse-spark-1.3` · Mistral `mistral-large-4-0` · DeepSeek `deepseek-v4.1-flash` ·
Qwen `qwen3.8-max-0902` · xAI `grok-4.7` · Moonshot `kimi-k3` · Zhipu `glm-5.3` ·
Cohere `command-a-plus` · MiniMax `minimax-m3`

## Ablauf

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY=sk-or-...

python -m ma_llm check                 # IDs, Preise, unterstützte Parameter
python -m ma_llm estimate              # grobe Kostenschätzung (aktuell ~$220 für 12 × 250)
python -m ma_llm preview               # Prompts eines simulierten Teilnehmers ansehen

python -m ma_llm run --n 10            # Pilot: 10 pro Modell, Parse-/Verweigerungsraten prüfen
python -m ma_llm analyze               # -> results/
python -m ma_llm run                   # volle Stichprobe (setzt fort, wo abgebrochen)
python -m ma_llm analyze
```

`run` ist fortsetzbar: bereits gespeicherte Teilnehmende (`data/raw/<modell>.jsonl`)
werden übersprungen, API-Fehler werden nicht gespeichert und beim nächsten Lauf wiederholt.
Gespeichert wird das komplette Transkript inkl. Rohantworten, Reihenfolge und Kosten.

## Outputs (`results/`)

- `summary.md` – Stichprobe, gepoolte Effekte vs. Menschen (Table 3), Replikationsmatrix
- `effects_by_model.csv` – alle Effekte pro Modell mit SE/CI
- `meta.csv` – Random-Effects-Schätzer, τ, I², Replikationsrate, Humanwerte
- `descriptives.csv` – Antwortanteile/Mediane pro Modell (zum Plausibilisieren)
- `between_subjects.csv`, `profile_vs_humans.csv`, `mds_coordinates.csv`
- `figure1_llm.png` – Gegenstück zu Figure 1

## Tests

```bash
python -m pytest -q
```

Die Tests prüfen Parsing und die gesamte Pipeline mit einem synthetischen Teilnehmer,
der die klassischen Effekte zeigt (keine echten API-Calls).
