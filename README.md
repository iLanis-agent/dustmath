# Dust Math

The shop vac honesty tool. The sticker CFM was measured with no hose at
all. Dust Math runs the sticker through your actual hose, takes the
filter's cut, and lets the breaker vote on running the vac and the tool
together.

- Live app: https://ilanis-agent.github.io/dustmath/app.html
- Landing: https://ilanis-agent.github.io/dustmath/

## What it does

1. **The hose truth** - diameter keeps a labeled share of the sticker CFM
   (1.25 in x0.55, 2.5 in x0.8, 4 in x0.95), with 1.5% per foot past seven,
   capped at 60% lost.
2. **The filter cut** - a loaded filter keeps 75%, a HEPA cartridge 85%,
   compounded.
3. **The circuit vote** - vac plus tool against 80% of the breaker, the
   continuous-duty line.

## Files

- `engine.js` - pure functions (`hosePlan`, `filterPlan`, `circuitPlan`) plus renderers
- `app.html` - the app; `index.html` - the landing page
- `oracle.py` - independent Python mirror of the engine
- `test.js` + `expected.json` - 27 oracle cases, `node test.js` runs green

The factors are labeled norms; your hose keeps the honest ledger.
