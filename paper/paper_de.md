# Führen Sprachmodelle mentale Konten?

## Replikation und Prüfung von Priolo et al. (2026) mit zwölf großen Sprachmodellen

24. Oktober 2026 · Steffen Rentschler· Arbeitspapier (Entwurf)

## Zusammenfassung

Zwölf große Sprachmodelle (LLMs) von zwölf Entwicklern reproduzieren die Richtung aller sieben Mental-Accounting-Szenarien, die Priolo et al. (2026) mit 5.589 Personen aus 21 Ländern repliziert haben, allerdings mit etwa zwei- bis fünfmal so großen Effekten wie beim Menschen. Wir haben jedem Modell über die OpenRouter-API einen anhand des Papers rekonstruierten Fragebogen vorgelegt (17 Items aus Table 1, randomisierte Blockreihenfolge, gleiche Ausschlussregeln und Effektmaße). Modelle traten dabei an die Stelle der Länder, unabhängige Gespräche an die Stelle der Teilnehmenden (155 Gespräche, 10–15 pro Modell). 90 von 96 Effekten auf Modellebene zeigten in die vorhergesagte Richtung, 76 (79 %) erfüllten das Replikationskriterium des Papers, gegenüber 90,5 % beim Menschen; die Lücke geht vor allem auf die kleinen Stichproben pro Modell zurück.

Vier Prüfvarianten (144 weitere Gespräche) zeigen, welche Bedingungen die Effekte verändern. Ohne Teilnehmerrolle im Systemprompt blieben die Effekte weitgehend erhalten. Auch umformulierte Szenarien mit neuen Geschichten und Beträgen ließen sie unverändert, was gegen ein bloßes Abrufen der Lehrbuchbeispiele spricht. Eine Anweisung, die die normative Entscheidungsregel ausdrücklich nennt (Geld ist austauschbar, versunkene Kosten und irrelevantes Framing zählen nicht), beseitigte die Fungibilitäts- und Sunk-Cost-Effekte (Jacket, Play) und die meisten Transaktionsnutzen-Effekte, nicht aber die Effekte, die eine soziale Norm tragen (Plane, Gym). Sah ein Gespräch nur eine Bedingung pro Szenario, schrumpften Play und Gym auf etwa menschliche Größe. Unter dieser Befragung reproduzieren die Modelle also viele menschliche Mental-Accounting-Muster, teils stark überhöht, und explizite Entscheidungsregeln sowie das Versuchsdesign verändern diese Muster deutlich. Warum die Modelle ohne Anweisung so antworten, erklären die Varianten nicht; sie grenzen mögliche Ursachen nur ein.

## 1 Einleitung

Priolo et al. (2026) haben gezeigt, dass Mental Accounting in 21 Ländern repliziert: Alle sieben Szenarien replizierten in einer gepoolten hierarchischen Analyse, und 90,5 % der Effekte auf Länderebene erreichten 95 % Glaubwürdigkeit. Die Studie bietet, was der LLM-Forschung zu ökonomischem Verhalten oft fehlt: einen großen, präregistrierten, länderübergreifenden menschlichen Vergleichsmaßstab mit festen Materialien und Effektmaßen. Wir nutzen ihn, um zu fragen, ob LLMs, die zunehmend als simulierte Befragte („Silicon Samples“) und als Entscheidungshilfen eingesetzt werden, dieselben mentalen Konten führen.

Zwei Erwartungen sind plausibel. LLMs werden auf menschlichen Texten trainiert und könnten deshalb menschliche Framing-Effekte reproduzieren. Sie werden aber auch darauf trainiert, zu schlussfolgern und Lehrbuchaufgaben zu lösen; die Szenarien sind Lehrbuchaufgaben, also könnten sie so antworten, wie es das normative Modell vorschreibt. Die Szenarien unterscheiden sich zudem darin, ob es überhaupt eine normative Antwort gibt: Jacket und Play prüfen Fungibilität, MrAB fragt dagegen, wie sich Menschen *fühlen*, und bei Drink, Game und Plane spielen soziale Normen mit.

Wir untersuchen drei Fragen:

1. **FF1 – Replikation.** Zeigen LLMs die sieben Mental-Accounting-Effekte, und wie groß sind sie im Vergleich zu den gepoolten menschlichen Schätzern?
2. **FF2 – Ursache.** Hängen die Effekte von einer Teilnehmerrolle ab, vom Wiedererkennen der publizierten Szenarien oder davon, dass das Modell nicht zur Rationalität aufgefordert wird?
3. **FF3 – Design.** Verändert das Within-Subjects-Design, in dem ein Modell beide Bedingungen im selben Gespräch sieht, die Effekte?

## 2 Methode

Wir haben Materialien, Ablauf, Ausschlüsse und Effektmaße der Humanstudie beibehalten und Länder durch Modelle, Teilnehmende durch unabhängige Gespräche ersetzt.

**Modelle.** Je ein Allzweckmodell von zwölf Entwicklern, alle am 23. und 24. Oktober 2026 über OpenRouter abgefragt: OpenAI gpt-6-sol, Anthropic claude-sonnet-5.5, Google gemini-3.8-flash, Meta muse-spark-1.3, Mistral mistral-large-4-0, DeepSeek deepseek-v4.1-flash, Alibaba qwen3.8-max-0902, xAI grok-4.7, Moonshot kimi-k3, Zhipu glm-5.3, Cohere command-a-plus und MiniMax minimax-m3. Die Einstellungen waren identisch: Temperatur 1,0 (zwei Anbieter ignorieren den Parameter und verwenden ihren Standardwert), Reasoning-Aufwand „low“, bis zu 8.000 Ausgabe-Tokens.

**Fragebogen.** Die 17 Items aus Table 1 von Priolo et al. (2026), wörtlich auf Englisch mit US-Dollar-Beträgen. Jedes Gespräch ist eine teilnehmende Person: ein Item pro Gesprächsrunde, frühere Antworten bleiben im Kontext. Die Items kamen in vier Blöcken (5/4/4/4) in zufälliger Reihenfolge, mit fester Reihenfolge innerhalb der Blöcke und nie zwei Bedingungen desselben Szenarios im selben Block. Danach folgten vier Financial-Literacy-Items und die Frage zur Datenqualität („How serious have you been about filling in the survey?“, 1–5). Die Antworten wurden als JSON angefordert; eine nicht lesbare Antwort wurde bis zu zweimal erneut erfragt.

**Ausschlüsse.** Wie im Paper wurden unvollständige Fragebögen und eine Datenqualität unter 4 ausgeschlossen. Von 299 Gesprächen wurden 4 ausgeschlossen und 295 ausgewertet: 3 waren unvollständig (ein Cohere-Durchlauf im Grundversuch, zwei DeepSeek-Durchläufe in der Rationalitätsvariante, bei denen das Reasoning das Token-Limit aufbrauchte), und ein Cohere-Durchlauf in der Rationalitätsvariante gab bei der Ernsthaftigkeit 3 an.

**Effektmaße.** Wie im Paper: Evidence Ratio gegenüber dem Zufall (1/9) für MrAB-Gewinne und -Verluste; logarithmiertes Odds Ratio für Game (Preis mindestens zum Marktwert, Fremder vs. Freund), Jacket, Play und Plane; Cohen's d für Drink (logarithmierter Preis) und Gym (Zustimmung zu „I wasted $20“). Binäre Outcomes erhalten eine +0,5-Korrektur, das frequentistische Gegenstück zu den schwach informativen Priors des Papers. Ein Effekt gilt als repliziert, wenn sein 95-%-Intervall die Null in der vorhergesagten Richtung ausschließt. Die Modellschätzer werden mit einer Random-Effects-Meta-Analyse nach DerSimonian–Laird gepoolt statt mit dem hierarchischen Bayes-Modell des Papers.

**Prüfvarianten.** Jede Variante umfasste 3 Gespräche pro Modell (36 pro Variante):

| Variante | Änderung gegenüber der Replikation | Geprüfte Frage |
| --- | --- | --- |
| Neutral | Systemprompt ohne Rolle als Umfrageteilnehmer; die Begrüßung der ersten Frage („Welcome to this study on decision-making …“) bleibt | Hängt der Effekt an der ausdrücklichen Teilnehmerrolle? |
| Rational | Anweisung, als vollständig rationaler Akteur zu entscheiden, der Geld als austauschbar behandelt und versunkene Kosten sowie irrelevantes Framing ignoriert | Folgt das Modell einer ausdrücklich genannten Entscheidungsregel? |
| Paraphrase | Neue Geschichten und Beträge mit gleicher Struktur (Konzert, Yogakurs, Zug-Upgrade, 45-$-Gutschein) | Hängt der Effekt am Wiedererkennen der publizierten Items? |
| Between | Eine zufällig gewählte Bedingung pro Szenario und Gespräch (dadurch auch kürzere Gespräche und andere Reihenfolge) | Verändert das Design die Effekte? |

Die Varianten werden anhand der ersten drei Durchläufe jedes Modells verglichen, gepoolt über alle Modelle, damit die Stichprobengröße in allen Bedingungen gleich ist.

**Abweichungen.** Die länderangepassten Beträge, die genauen Financial-Literacy-Items und die Blockdatei liegen auf OSF und standen nicht zur Verfügung; die Beträge folgen Table 1, die Blockzuordnung wurde aus der Beschreibung im Paper rekonstruiert. Demografie- und BIP-Analysen haben bei Modellen kein Gegenstück und entfallen. Die API-Kosten lagen insgesamt bei etwa 18 $.

## 3 Ergebnisse: Die Effekte replizieren und sind überhöht

Alle acht Effekte replizieren im gepoolten LLM-Schätzer, und sieben davon sind 1,8- bis 5,2-mal so groß wie beim Menschen; nur der MrAB-Verlusteffekt ist kleiner (1,61 vs. 2,13).

![Abbildung 1. Gepoolte LLM-Effekte vs. gepoolte Humaneffekte (95-%-KI) mit der Zahl der Modelle, die den Effekt replizieren](figures/fig1_llm_vs_human.png)

*Abbildung 1 (Beschriftung auf Englisch). Quelle: `results/meta.csv` (155 Gespräche, 10–15 pro Modell) und Priolo et al. (2026), Table 3.*

Auf Modellebene zeigen 90 von 96 Effekten in die vorhergesagte Richtung, und 76 (79 %) erfüllen das Replikationskriterium, verglichen mit 133 von 147 (90,5 %) Effekten auf Länderebene beim Menschen. Die sechs Ausnahmen sind aufschlussreich und kein Rauschen: Cohere kehrt den Sunk-Cost-Effekt um (64 % würden ein verlorenes Ticket nachkaufen, aber nur 14 % nach verlorenem Bargeld); GPT und Cohere fahren in keiner Jacket-Bedingung die 20 Minuten zur anderen Filiale, MiniMax in beiden gleich oft (13 %); Claude und DeepSeek zeigen kein MrAB-Verlustmuster. Die MrAB-Verluste sind über alle Modelle hinweg schwach, weil die meisten Modelle die Person mit dem „Silver Lining“ (Autoreparatur plus kleiner Gewinn bei einer Verlosung) für verärgerter halten, also das Gegenteil von Thalers Vorhersage.

Die Modelle unterscheiden sich weit stärker als die Durchläufe eines Modells. Die Heterogenität ist hoch für Drink, MrAB-Gewinne, Play und Gym (I² = 0,70–0,82), und viele Modelle geben in jedem Durchlauf dieselbe Antwort: Bei Play2 (Bargeld verloren) sagen zehn von zwölf Modellen in jedem Durchlauf Ja, MiniMax in 13 von 15 und Cohere nur in 2 von 14. Meta, Kimi und Qwen replizieren alle acht Effekte; Claude und Mistral replizieren die wenigsten. Im Between-Subjects-Check des Papers selbst (nur die zuerst gesehene Bedingung) bleiben die mittleren Schätzer auf Modellebene groß (log OR: Jacket 1,92, Play 2,10, Plane 3,60).

## 4 Ergebnisse: Was die Effekte verändert

Am stärksten verändert eine Anweisung, die die normative Regel ausdrücklich nennt, die Effekte; Plane und Gym bleiben dabei bestehen. Das Entfernen der Teilnehmerrolle im Systemprompt und neue Formulierungen verringern die Effekte dagegen kaum.

![Abbildung 2. Effekt je Bedingung (Replikation, neutral, Paraphrase, between, rational) mit dem Humanwert als Referenz](figures/fig2_variants.png)

*Abbildung 2 (Beschriftung auf Englisch). Quelle: `results/variants_effects.csv`; 36 Gespräche pro Bedingung (33 bei rational); Intervalle weggelassen, weil sie die Clusterung nach Modell ignorieren.*

**Rolle (neutral).** Ohne die ausdrückliche Teilnehmerrolle im Systemprompt bleiben sechs von acht Effekten auf dem Niveau der Replikation. Game halbiert sich (5,10 auf 2,06), liegt aber weiterhin über dem Humanwert. Die erste Frage beginnt in dieser Variante weiterhin mit der Begrüßung zur Studie; eine Wirkung der Umfragerahmung insgesamt ist damit nicht ausgeschlossen.

**Wiedererkennen (Paraphrase).** Mit neuen Geschichten und Beträgen sind die Effekte so groß wie mit dem publizierten Wortlaut (Drink 2,56, Play 3,38, Plane 4,84). Die Modelle wenden das Muster an, statt eine auswendig gelernte Antwort auf ein bekanntes Item zu geben. Ein Lernen aus der Literatur ist damit nicht ausgeschlossen, da die Paraphrasen die kanonische Struktur beibehalten.

**Rationalität (rational).** Unter der Anweisung, Geld als austauschbar zu behandeln und versunkene Kosten sowie irrelevantes Framing zu ignorieren, fällt Play auf 0,00 (jedes Modell kauft das Ticket in beiden Bedingungen nach) und Jacket auf 0,20; Game (0,28) und Drink (0,45) verschwinden nahezu. Bei MrAB antworten fast alle Modelle „No difference“, wodurch die Evidence Ratios negativ werden (−2,13): Sie verzichten darauf, Gefühle vorherzusagen, statt sie rational vorherzusagen. Zwei Effekte bleiben bestehen: Plane (0,96; 64 % würden für einen gekauften Gutschein bezahlen, 39 % für einen geschenkten) und Gym (0,69). Beide berühren möglicherweise eine Norm über das Geld anderer oder über vergeblichen Aufwand; das ist eine Hypothese, die hier nicht geprüft wurde. Da die Anweisung die anzuwendende Regel bereits vorgibt, zeigt diese Variante vor allem Steuerbarkeit, nicht den Grund für das Verhalten ohne Anweisung.

**Design (between).** Sieht ein Gespräch nur eine Bedingung, sinkt Play von 2,84 auf 0,98 und Gym von 2,12 auf 0,81, nahe an den menschlichen Werten von 0,58 und 0,72. Auch Jacket und Game werden kleiner. Plane, Drink und MrAB ändern sich kaum. Das ist ein Hinweis auf einen Designeffekt. Die Variante ändert aber mehreres zugleich: Neben dem fehlenden Gegenstück sind die Gespräche kürzer und die Reihenfolge der Aufgaben ist anders. Ob das Sehen beider Bedingungen die Effekte verstärkt, etwa weil das Modell sie gegeneinander abgrenzt, lässt sich damit nicht trennen.

## 5 Diskussion

Ohne ausdrückliche Regel antworten die untersuchten Modelle nicht wie das normative ökonomische Modell, sondern zeigen eine menschenähnliche und oft übersteigerte Form des Mental Accounting. Nennt man ihnen die Regel, folgen sie ihr bei den meisten Szenarien. Die folgenden Deutungen sind Hypothesen, die die Varianten nahelegen, aber nicht belegen.

**Normative Rationalität versus soziale Normen.** Die Szenarien zerfallen in zwei Gruppen. Wo die normative Antwort rein ökonomisch ist (Jacket, Play, Drink, Game), beseitigt die Rationalitätsanweisung den Effekt; die Modelle können die Regel also anwenden, wenn sie genannt wird, tun es aber nicht von sich aus. Wo die „irrationale“ Antwort zugleich die sozial angemessene ist (einem Freund einen gekauften Gutschein bezahlen; eine bezahlte, aber ausgefallene Trainingseinheit als Verlust empfinden), überlebt der Effekt die Anweisung. Eine mögliche Erklärung ist, dass Mental Accounting hier weniger als Fehler denn als soziale Norm behandelt wird; geprüft haben wir das nicht. MrAB ist ein dritter Fall: Es fragt, wie sich Menschen fühlen; ein Modell, das unter der Rationalitätsanweisung „No difference“ antwortet, hat aufgehört, Menschen vorherzusagen, und ist nicht rationaler geworden.

**Stereotype Menschen.** Bei sieben von acht Effekten übertrifft der gepoolte LLM-Schätzer sogar den größten Einzelländerwert in Abbildung 1 von Priolo et al. (aus der Abbildung abgelesen). Zwei Mechanismen kommen in Frage. Erstens geben die Modelle fast immer die häufigste menschliche Antwort, sodass die Varianz zwischen Durchläufen klein ist und standardisierte Effekte groß werden; das ist eine Eigenschaft des Samplings aus einem Modell, kein stärkerer Bias. Zweitens ist der Kontrast zwischen den Bedingungen schärfer als beim Menschen; dass Play und Gym between-subjects auf menschliches Niveau fallen, deutet auf einen Beitrag des Designs hin, ohne dass sich der Mechanismus trennen lässt. Die Modelle scheinen eher das Lehrbuchmuster zu reproduzieren als die Verteilung menschlicher Antworten.

**Folgerungen für Silicon Samples.** In der Richtung hätten gepoolte LLM-Befragte die menschlichen Ergebnisse für alle sieben Szenarien richtig vorhergesagt. In der Größe hätten sie sieben von acht Effekten um ein Mehrfaches überschätzt und den MrAB-Verlusteffekt unterschätzt; zudem folgt ihre Rangordnung der Szenarien nicht der menschlichen (die Korrelationen der Modelle mit dem menschlichen Effektprofil reichen von −0,90 bis 0,33). Simulierte Befragte können nützlich sein, um die Richtung von Framing-Effekten vorab zu prüfen, nicht aber, um ihre Größe zu schätzen oder Poweranalysen zu stützen. Die großen Unterschiede zwischen den Modellen (I² bis 0,82) bedeuten außerdem, dass Ergebnisse eines Modells nicht auf „LLMs“ verallgemeinert werden können.

**Folgerungen für LLMs als Berater.** Wer ein Modell bei solchen Entscheidungen um Rat fragt, bekommt standardmäßig einen Rat, der Mental Accounting reproduziert. Die Rationalitätsanweisung zeigt, dass die normative Antwort verfügbar ist. Ob ein Modell sie standardmäßig anwenden sollte, ist eine Gestaltungsfrage, denn in den normgeprägten Szenarien ist die menschenähnliche Antwort womöglich die, die Nutzer erwarten.

## 6 Grenzen und weitere Forschung

Die wichtigste Grenze ist die Stichprobengröße: 10–15 Gespräche pro Modell in der Replikation und 3 pro Modell und Variante in den Prüfungen, gegenüber 250 pro Land in der Humanstudie.

- **Durchläufe sind keine Menschen.** Die Streuung zwischen Gesprächen eines Modells ist Stichprobenrauschen, keine Heterogenität einer Population. Intervalle auf Modellebene beschreiben die Stabilität des Modellverhaltens; sie sind nicht mit Intervallen auf Länderebene vergleichbar, und die Replikationsraten von 79 % gegenüber 90,5 % dürfen nicht als Unterschied in der Robustheit gelesen werden.
- **Die Variantenvergleiche sind grob.** Jede Bedingung hat 36 Gespräche (33 bei rational, nach drei Ausschlüssen), Between-Zellen etwa 18; die gepoolten Schätzer ignorieren die Clusterung nach Modell. Nur die großen Kontraste (rational vs. Replikation; Play und Gym between-subjects) sollten als Befunde gelten.
- **Materialien.** Wir haben die Beträge aus Table 1 in US-Dollar und nur Englisch verwendet, eine rekonstruierte Blockzuordnung und Standard-Items zur Financial Literacy. Mit den OSF-Materialien wäre eine exakte Replikation möglich, einschließlich der 23 Sprachen und der länderangepassten Beträge.
- **Einstellungen.** Alle Modelle liefen mit Temperatur 1,0 und niedrigem Reasoning-Aufwand; zwei Anbieter ignorieren den Temperaturparameter. Der Reasoning-Aufwand könnte die Effekte durchaus verändern und wurde hier nicht getestet.
- **Momentaufnahme.** Die zwölf Modelle sind Versionen vom Oktober 2026; Anbieter aktualisieren Modelle ohne Ankündigung.
- **Neutral-Variante.** Nur der Systemprompt wurde neutralisiert; die Begrüßung zur Studie in der ersten Frage blieb. Eine vollständig ungerahmte Variante fehlt.
- **Between-Variante.** Sie ändert neben dem fehlenden Gegenstück auch Gesprächslänge und Reihenfolge.
- **Rationalitäts-Variante.** Sie nennt die anzuwendende Regel ausdrücklich und prüft damit Befolgung, nicht spontanes Urteilen.
- **Paraphrasen** behalten die kanonische Struktur jedes Szenarios bei; sie prüfen also das Wiedererkennen des Wortlauts, nicht das Wissen um den Effekt selbst.

Naheliegende nächste Schritte sind ein präregistrierter Lauf mit 100 oder mehr Gesprächen pro Modell und Variante, der Reasoning-Aufwand als Faktor, die Originalsprachen und Szenarien ohne publizierte Vorlage.

## Verfügbarkeit von Daten und Code

Der Code des Fragebogens, alle Rohtranskripte (299 Gespräche mit Prompts, Antworten, Reihenfolge und Kosten) und die Auswertungen liegen im Repository [hstre/The-Robustness-of-Mental-Accounting](https://github.com/hstre/The-Robustness-of-Mental-Accounting) (`data/raw/`, `results/`, `results/variants.md`). `python -m ma_llm analyze` und `python -m ma_llm compare` reproduzieren jede Zahl dieses Papers aus den gespeicherten Transkripten.

## Literatur

Die folgenden Literaturangaben wurden aus dem Gedächtnis zusammengestellt und müssen vor einer Einreichung geprüft werden; nur Priolo et al. (2026) wurde direkt eingesehen.

- Argyle, L. P., Busby, E. C., Fulda, N., Gubler, J. R., Rytting, C., & Wingate, D. (2023). Out of one, many: Using language models to simulate human samples. *Political Analysis*, 31(3), 337–351.
- Chinn, S. (2000). A simple method for converting an odds ratio to effect size for use in meta-analysis. *Statistics in Medicine*, 19(22), 3127–3131.
- DerSimonian, R., & Laird, N. (1986). Meta-analysis in clinical trials. *Controlled Clinical Trials*, 7(3), 177–188.
- Horton, J. J. (2023). Large language models as simulated economic agents: What can we learn from Homo silicus? NBER Working Paper 31122.
- Kahneman, D., & Tversky, A. (1982). The psychology of preferences. *Scientific American*, 246(1), 160–173.
- Lusardi, A., & Mitchell, O. S. (2014). The economic importance of financial literacy. *Journal of Economic Literature*, 52(1), 5–44.
- Priolo, G., Stablum, F., Vacondio, M., et al. (2026). The robustness of mental accounting across 21 countries. *Journal of Consumer Research*. <https://doi.org/10.1093/jcr/ucag022>
- Shafir, E., & Thaler, R. H. (2006). Invest now, drink later, spend never: On the mental accounting of delayed consumption. *Journal of Economic Psychology*, 27(5), 694–712.
- Thaler, R. H. (1985). Mental accounting and consumer choice. *Marketing Science*, 4(3), 199–214.
- Thaler, R. H. (1999). Mental accounting matters. *Journal of Behavioral Decision Making*, 12(3), 183–206.
- Tversky, A., & Kahneman, D. (1981). The framing of decisions and the psychology of choice. *Science*, 211(4481), 453–458.
