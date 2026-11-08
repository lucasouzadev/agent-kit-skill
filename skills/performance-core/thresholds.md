# Thresholds and budgets

## Public thresholds (external floors)
| Area | Metric | Threshold |
|---|---|---|
| Web (p75, real visits, mobile and desktop separately) | LCP · INP · CLS | ≤ 2.5 s · ≤ 200 ms · ≤ 0.1 (INP replaced FID in March 2024) |
| Android (Google Play visibility) | User-perceived crash · ANR | < 1.09 % · < 0.47 % overall; 8 % per device model |
| Android | Cold · warm · hot start | "Excessive" at ≥ 5 s · ≥ 2 s · ≥ 1.5 s |
| Apple | Main-thread hang | Reported from 250 ms ("micro hangs"); "Everything above 500 ms we consider a proper hang"; ideally no main-thread work > 100 ms |
| Any UI (RAIL, 2015 mental model) | Response · task · frame | ~100 ms · ~50 ms · ~16 ms |

Google announces threshold changes ahead of time; Android vitals warns that memory, bitmap memory and code-optimization thresholds may affect store visibility from February 2027.

## Budget template (copy to the project)
| Budget | Target | Gate |
|---|---|---|
| Initial JS / binary size | <value> | CI fails above +<tolerance> |
| Cold start (entry device) | <value> | benchmark per PR |
| INP / hang rate | <value> | field alert per version |
| Memory peak on the longest flow | <value> | profile per release |
| Requests on first load | <value> | lab check per PR |
