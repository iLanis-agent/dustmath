// Dust math - shop vac and dust collection honesty.
// The sticker CFM was measured with no hose at all. The hose decides what
// you get, the filter takes its cut, and the breaker gets a vote.
// Verdicts judge the unrounded figure; rounding is for display only.
var DustMath = (function () {
  function pos(x) { return typeof x === "number" && isFinite(x) && x > 0; }
  function r1(x) { return Math.round(x * 10) / 10; }

  // Labeled norms: hose diameter keeps this much of the sticker CFM.
  var DIAM = { "1.25": 0.55, "2.5": 0.8, "4": 0.95 };

  function hosePlan(ratedCfm, hoseIn, hoseFt) {
    if (!pos(ratedCfm)) return { error: "the sticker CFM must be above zero" };
    if (!DIAM[hoseIn]) return { error: "pick a hose diameter" };
    if (!pos(hoseFt)) return { error: "the hose length must be above zero" };
    // Labeled norm: 1.5% lost per foot past seven, capped at 60% lost.
    var mult = Math.max(0.4, 1 - 0.015 * Math.max(0, hoseFt - 7));
    var eff = ratedCfm * DIAM[hoseIn] * mult;
    return { eff: r1(eff) };
  }

  function renderHose(r, ratedCfm, hoseIn, hoseFt) {
    return "Your " + ratedCfm + " CFM vac through " + hoseFt + " ft of " + hoseIn
      + " in hose figures about " + r.eff + " CFM at the tool - the sticker was measured with no hose at all.";
  }

  function filterPlan(cfm, state, hepa) {
    if (!pos(cfm)) return { error: "the CFM must be above zero" };
    if (state !== "clean" && state !== "loaded") return { error: "pick clean or loaded" };
    var f = 1;
    if (state === "loaded") f *= 0.75;
    if (hepa) f *= 0.85;
    return { eff: r1(cfm * f) };
  }

  function renderFilter(r, cfm, state, hepa) {
    if (state === "clean" && !hepa) {
      return "Your " + cfm + " CFM stays about " + r.eff + " with a clean filter - it only stays innocent if you wash it.";
    }
    var parts = [];
    if (state === "loaded") parts.push("A loaded filter");
    if (hepa) parts.push("the HEPA cartridge");
    var verb = parts.length > 1 ? " take " : " takes ";
    var who = parts.join(" and "); who = who.charAt(0).toUpperCase() + who.slice(1);
    return who + verb + "your " + cfm + " CFM down to about " + r.eff
      + " - suction dies at the filter, not the motor.";
  }

  function circuitPlan(vacAmps, toolAmps, circuitAmps) {
    if (!pos(vacAmps) || !pos(toolAmps) || !pos(circuitAmps)) return { error: "amps must all be above zero" };
    var load = vacAmps + toolAmps;
    var limit = 0.8 * circuitAmps;
    return { load: r1(load), limit: r1(limit), over: load > limit };
  }

  function renderCircuit(r, vacAmps, toolAmps, circuitAmps) {
    var s = "Your vac (" + vacAmps + " A) and tool (" + toolAmps + " A) pull " + r.load
      + " A on a " + circuitAmps + " A circuit - ";
    if (r.over) return s + "past the " + r.limit + " A continuous line, so the breaker votes no; run one motor at a time.";
    return s + "inside the " + r.limit + " A continuous line, so the breaker stays out of it.";
  }

  return {
    hosePlan: hosePlan, renderHose: renderHose,
    filterPlan: filterPlan, renderFilter: renderFilter,
    circuitPlan: circuitPlan, renderCircuit: renderCircuit
  };
})();
if (typeof module !== "undefined") module.exports = DustMath;
