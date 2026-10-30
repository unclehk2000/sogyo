# MODEL 13C — "SŌGYO": the RTH gap on every NQ day
### NQ 1-minute, 2 Jan 2018 – 9 Oct 2026 · 2,011 days · 2019–21 (715 days) never tested before

---

## Why this re-run
- **The earlier study** (Model 13 / 13B) used NQ for 2018 and 2022 – Aug 2026 only: 1,255 days.
- **What this run adds:** the data now covers every year, so 2019–21 is a clean out-of-sample test of everything Sōgyo claims, including the card's GREEN / RED rule. That rule was fitted on the earlier years. Aug–Oct 2026 is new as well.

**Definitions** (as the script draws them):
- **CE1 and CE2.** CE1 = (prior 16:14 close + 09:30 open) ÷ 2. CE2 = (prior 16:59 close + 09:30 open) ÷ 2. The zone runs between them.
- **The middle and the fill.** Z = the middle of the zone. F = the midpoint of the two closes, which is the full fill.
- **Card measures.** Gap = |open − F|. Overnight = the 18:00–09:29 range. ATR = the mean of the last 14 RTH (09:30–16:14) ranges.
- **Context:**
  - SPLIT: the open sits between the two closes.
  - RED: gap > 0.68 ATR.
  - GREEN: overnight ≤ 0.45 ATR.
  - NEUTRAL: everything else.
- **Days kept:** the prior closes and today's open are on the same contract, and both sessions are complete.
- **✓ rule:** p < 0.05 with errors clustered by date, and the same sign in 2018, 2019–21 and 2022–26.

---

## 1. Geometry

| | Median | 75th pct | 90th pct |
|---|---|---|---|
| \|Gap\| (open vs 16:14 close) | 0.41% | 0.78% | 1.31% |
| Zone width \|CE1 − CE2\| | 3.25 pts (0.026%) | 7.4 pts | 14.4 pts |
| Gap in ATR | 0.27 | 0.49 | 0.77 |
| Overnight range in ATR | 0.64 | 0.86 | 1.14 |

- **Context mix:** NEUTRAL 61%, GREEN 21%, RED 13%, SPLIT 5%.
- **Widest zones:** the biggest 16:14 → 16:59 moves are real events, not data errors. Examples: 2 Apr 2025 (tariffs, 398 pts), 22 Feb 2024 and 25 May 2023 (NVDA results).

---

## 2. The target map — holds out of sample ✓

**Zone reached (near level) / far level / full fill, by time** (aligned days, n 1,918):

| By | 09:35 | 09:45 | 10:00 | 10:30 | 11:00 | 12:00 | 16:14 |
|---|---|---|---|---|---|---|---|
| Near level | 39% | 52% | 59% | 66% | 69% | 73% | **78%** |
| Far level | 31% | 44% | 52% | 60% | 64% | 69% | 75% |
| Full fill | 17% | 26% | 34% | 41% | 46% | 51% | **60%** |

**By period:**

| Period | Zone by 10:00 | Zone in RTH | Fill in RTH |
|---|---|---|---|
| 2018 | 61% | 80% | 62% |
| **2019–21 (new)** | 59% | 77% | 59% |
| 2022–26 | 58% | 79% | 61% |

**By year** (zone in RTH): 80, 75, 77, 78, 80, 81, 80 and 80% for 2018–25, and 71% for 2026 (to 9 Oct).

**By gap size** (quintiles of \|gap\|):

| \|Gap\| | ≤ 0.16% | 0.16–0.33% | 0.33–0.56% | 0.56–0.92% | > 0.92% |
|---|---|---|---|---|---|
| Zone in RTH | 94.5% | 90.6% | 80.5% | 68.9% | 56.2% |
| Full fill | 88.3% | 76.2% | 59.9% | 47.5% | 29.2% |
| Median minute to the zone | 0 | 2 | 7 | 14 | 43 |

**Decay:**
- Not reached by 10:00 → reached later in RTH on **47%** of days (n 792).
- Not reached by 11:00 → **29%** (n 590).

These match Model 13 to within 2 points in every cell. The 2019–21 years, never seen before, land on the same numbers.

---

## 3. The card's context

**What each context says about the day** (all 2,011 days):

| Context | Days | Zone by 10:00 | Zone in RTH | Full fill in RTH |
|---|---|---|---|---|
| GREEN (quiet) | 415 | 74% | 87% | **74%** |
| NEUTRAL | 1,233 | 63% | 81% | 64% |
| RED (big gap) | 270 | 16% | 50% | **24%** |
| SPLIT | 93 | 97% | 98% | 94% |

- **RED fills less:** −40 points against NEUTRAL, ✓ in all three periods.
- **GREEN reaches the zone more often:** +6 points, ✓.
- **GREEN fills more often:** +10 points pooled, and +16 points in 2019–21. It is flat in 2018, so it falls short of ✓.
- **SPLIT days:** CE1 and CE2 straddle the open, and both are touched on 91% of these days, usually at once.

**The zone as a wall at the first NY AM touch.** Aligned days, gap ≥ 0.10%, touched by 10:59, n 1,072; median touch at 09:36.
- **The race:** half a gap either way, so the walk null is 50%. Placebos run the same race at the 0.375 and 0.625 fractions.

| Context | Z holds (n) | 2018 | **2019–21** | 2022–26 | Placebos .375 / .625 |
|---|---|---|---|---|---|
| GREEN | 60.3% (237) | 74% | **50%** | 63% | 51 / 56% |
| NEUTRAL | 49.7% (756) | 47% | 50% | 50% | 46 / 46% |
| RED | **32.9%** (79) | 20% | 43% | 27% | 14 / 39% |
| All | 50.8% (1,072) | | | | 45 / 48% |

**GREEN by year:** 74, 50, 53, 48, 61, 62, 55, 67 and 75% (2018–26).

- **RED: the zone breaks toward the fill about 2 times in 3.** Holding falls below 50% in every period (✓). The placebos fail as often, so this is the big-gap day doing it, not the zone itself.
- **NEUTRAL is a coin flip in every period.**
- **GREEN fails out of sample.** It holds 60% pooled, but in 2019–21, the years the 0.68 / 0.45 rule never saw, it held 50.0% (n 66). Each of those years sat at 48–53%.
  - The zone does beat its own placebos on GREEN days by +5 points (✓), but that is relative to weak placebos, not a wall you can lean on.
- **The thresholds aren't steps.** As continuous factors, neither the gap nor the overnight range clears ✓ for the hold rate (p 0.16 and 0.28).

---

## 4. The flipped wall (through, retest, reject) — not an edge
- **Through:** price runs 0.125 × gap beyond the zone's far edge toward the fill.
- **Retest:** price comes back to that edge.
- **Reject:** from the retest, does price go 0.25 × gap further toward the fill before 0.25 × gap back toward the open? The window is 09:30–11:59 and the walk null is 50%.
- **Decoys:** equal-width zones at the 0.375 and 0.625 fractions.

| | Zone (n) | 2018 | 2019–21 | 2022–26 | Decoy .375 | Decoy .625 |
|---|---|---|---|---|---|---|
| All | 51.4% (879) | 55% | 48% | 53% | 51.9% | 42.8% |
| Wide zone (≥ 0.05%) | 55.0% (218) | 58% | 53% | 56% | 53.5% | 41.2% |

**By year:** 55, 46, 48, 50, 52, 52, 58, 46 and 57%.

- **The zone doesn't beat 50%.** All days: p 0.40. Wide zones: p 0.14.
- **The apparent premium over the decoys (+6 to +11 points, ✓) is the 0.625 decoy failing, not the zone working.** The 0.375 decoy does as well as the zone. Model 13B's best lead doesn't survive the extra years.

---

## 5. Verdict

| Question | Answer |
|---|---|
| Does the target map hold on all NQ data? | **Yes.** Zone reached 78%, fill 60%, the same by gap size and time of day. 2019–21 matches the earlier years to within 2 points. |
| Does RED mean the zone breaks? | **Yes.** It holds 33% (2 in 3 break), under 50% in every period, and only 24% of RED days fill. |
| Does GREEN make the zone a wall? | **No, not reliably.** 60% pooled, 50% in the unseen years 2019–21. It does mark days that fill more often (74% vs 64%). |
| Is NEUTRAL anything? | A coin flip at the zone: 50% in every period. |
| Does the flipped wall work? | **No.** 51% (55% on wide zones), not different from 50% or from the nearer decoy. |

**My numbers:**
- **95%** that the target map keeps within ±3 points of these rates.
- **80%** that RED keeps breaking more than half the time.
- **15%** that GREEN works as a wall above 55% in new data.
- **10%** that the flipped wall carries an edge.

**What changed in the indicator:**
- **The card is three rows:** the header with the context pill, the zone's width, and the context read.
- **The context wording now says what the data shows:**
  - GREEN · fill 74%;
  - RED · breaks 2 in 3;
  - NEUTRAL · coin flip;
  - SPLIT · skip.
- **The tooltips:** CE1 / CE2, the gap, the overnight range, the ATR and these rates moved there.

---
*Scripts (`research/`): `sg_days.py` (days, CE1 / CE2, context), `sg_out.py` (touches, the NY AM wall, the flipped wall), `sg_tab.py` + `sg_tab2.py` (tables). Statistics: errors clustered by date; ✓ = p < 0.05 and the same sign in 2018, 2019–21 and 2022–26.*
