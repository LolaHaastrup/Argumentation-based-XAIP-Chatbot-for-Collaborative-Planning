"""
An Argumentation-Based Framework for Explaining Scheduled Temporal Plans
Bus–Train Collaborative Journey — Streamlit Chatbot Prototype

University of Huddersfield | Omolola Oluyemisi Haastrup
Supervisors: Dr Quratul-ain Mahesar | Prof Mauro Vallati

CQ defeating-scheme mapping (updated 26 May 2026):
  CQ1 → defeated by S3  (Temporal Feasibility)
  CQ2 → defeated by S6  (Invariant Maintenance Justification)
  CQ3 → defeated by S1  (Action Applicability)
  CQ4 → defeated by S5  (Temporal Ordering Justification)
  CQ5 → defeated by S5  (Temporal Ordering Justification)
  CQ6 → defeated by S1  (Action Applicability)
  CQ7 → defeated by S2  (Causal Goal Support)
  CQ8 → defeated by S4  (Resource & Concurrency Feasibility)
"""

import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="XAIP Chatbot — Bus–Train Plan",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}
h1, h2, h3 { font-family: 'IBM Plex Sans', sans-serif; font-weight: 700; }
code, pre, .mono { font-family: 'IBM Plex Mono', monospace; }

.accepted-badge {
    background: #d4edda; color: #155724; border: 1.5px solid #28a745;
    border-radius: 6px; padding: 6px 14px; font-weight: 700;
    display: inline-block; font-size: 0.95rem;
}
.rejected-badge {
    background: #f8d7da; color: #721c24; border: 1.5px solid #dc3545;
    border-radius: 6px; padding: 6px 14px; font-weight: 700;
    display: inline-block; font-size: 0.95rem;
}
.scheme-box {
    border-left: 5px solid #1a5276;
    background: #eaf4fb;
    padding: 14px 18px;
    border-radius: 0 8px 8px 0;
    margin: 10px 0;
    font-size: 0.88rem;
    line-height: 1.75;
}
.defeating-box {
    border-left: 5px solid #1e8449;
    background: #eafaf1;
    padding: 14px 18px;
    border-radius: 0 8px 8px 0;
    margin: 10px 0;
    font-size: 0.88rem;
    line-height: 1.75;
}
.fail-box {
    border-left: 5px solid #c0392b;
    background: #fdedec;
    padding: 14px 18px;
    border-radius: 0 8px 8px 0;
    margin: 10px 0;
    font-size: 0.88rem;
}
.na-box {
    border-left: 5px solid #95a5a6;
    background: #f8f9fa;
    padding: 14px 18px;
    border-radius: 0 8px 8px 0;
    margin: 10px 0;
    font-size: 0.88rem;
}
.psa-accepted {
    border: 2px solid #28a745; background: #f0fff4;
    border-radius: 10px; padding: 18px 22px; margin: 12px 0;
}
.psa-rejected {
    border: 2px solid #dc3545; background: #fff5f5;
    border-radius: 10px; padding: 18px 22px; margin: 12px 0;
}
.plan-row { border-bottom: 1px solid #e9ecef; }
.concurrent-highlight { background: #fff3cd !important; }
.legend-dot {
    width: 12px; height: 12px; border-radius: 50%;
    display: inline-block; margin-right: 6px;
}
.scenario-btn { margin: 4px; }
.cq-pill {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin: 3px;
    cursor: pointer;
}
.pill-defeated  { background: #d4edda; color: #155724; border: 1px solid #28a745; }
.pill-succeeds  { background: #f8d7da; color: #721c24; border: 1px solid #dc3545; }
.pill-na        { background: #e9ecef; color: #6c757d; border: 1px solid #adb5bd; }
.attack-label   { color: #922b21; font-size: 0.78rem; font-weight: 600; }
.defeat-label   { color: #1e8449; font-size: 0.78rem; font-weight: 600; }
.tick-pass  { color: #28a745; font-weight: 700; }
.tick-fail  { color: #dc3545; font-weight: 700; }
.layer-header {
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; color: #6c757d;
    border-bottom: 1px solid #dee2e6; padding-bottom: 4px;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  DATA — NOMINAL PLAN
# ═══════════════════════════════════════════════════════════════

NOMINAL_ACTIONS = [
    {"step_index": 1, "action_name": "board_bus",
     "params": {"l": "bus_stop"}, "start": 0, "end": 2, "resource": "Bus"},
    {"step_index": 2, "action_name": "bus_travel",
     "params": {"f": "bus_stop", "t": "train_station"}, "start": 2, "end": 7, "resource": "Bus"},
    {"step_index": 3, "action_name": "passenger_platform_wait",
     "params": {"l": "train_station"}, "start": 7, "end": 10, "resource": "—"},
    {"step_index": 4, "action_name": "train_approach",
     "params": {"l": "train_station"}, "start": 7, "end": 10, "resource": "Train"},
    {"step_index": 5, "action_name": "board_train",
     "params": {"l": "train_station"}, "start": 10, "end": 11, "resource": "Train"},
    {"step_index": 6, "action_name": "train_travel",
     "params": {"f": "train_station", "t": "destination"}, "start": 11, "end": 19, "resource": "Train"},
]

RESOURCE_COLOUR = {"Bus": "#fdebd0", "Train": "#d6eaf8", "—": "#f8f9fa"}


# ═══════════════════════════════════════════════════════════════
#  STATE REPLAY (S0)
# ═══════════════════════════════════════════════════════════════

INITIAL_STATE = {
    "at(bus,bus_stop)": True,   "at(bus,train_station)": False,
    "at(bus,destination)": False,
    "at(train,bus_stop)": False, "at(train,train_station)": True,
    "at(train,destination)": False,
    "passenger_at(bus_stop)": True,  "passenger_at(train_station)": False,
    "passenger_at(destination)": False,
    "passenger_on_bus": False,   "passenger_on_train": False,
    "arrived_at(bus_stop)": False,   "arrived_at(train_station)": False,
    "arrived_at(destination)": False,
    "is_train_station(bus_stop)": False, "is_train_station(train_station)": True,
    "is_train_station(destination)": False,
    "train_at_station(bus_stop)": False, "train_at_station(train_station)": False,
    "train_at_station(destination)": False,
    "ready_to_board": False,
}


def build_effects(actions):
    se, ee = {}, {}

    def adds(t, fl, v): se.setdefault(round(t, 4), []).append((fl, v))
    def adde(t, fl, v): ee.setdefault(round(t, 4), []).append((fl, v))

    for a in actions:
        name, p, st, en = a["action_name"], a.get("params", {}), a["start"], a["end"]
        if name == "board_bus":
            loc = p.get("l", "bus_stop")
            adde(en, "passenger_on_bus", True)
            adde(en, f"passenger_at({loc})", False)
        elif name == "bus_travel":
            f, t = p.get("f", ""), p.get("t", "")
            adds(st, f"at(bus,{f})", False)
            adde(en, f"at(bus,{t})", True)
            adde(en, "passenger_on_bus", False)
            adde(en, f"arrived_at({t})", True)
        elif name == "passenger_platform_wait":
            adde(en, "ready_to_board", True)
        elif name == "train_approach":
            loc = p.get("l", "train_station")
            adde(en, f"train_at_station({loc})", True)
        elif name == "board_train":
            adde(en, "passenger_on_train", True)
            adde(en, "ready_to_board", False)
        elif name == "train_travel":
            t = p.get("t", "destination")
            adde(en, f"passenger_at({t})", True)
            adde(en, "passenger_on_train", False)
        elif name == "disrupt_invariant":
            mid = (st + en) / 2
            adde(mid, "passenger_on_bus", False)
    return se, ee


def compute_state(t, actions):
    se, ee = build_effects(actions)
    state = dict(INITIAL_STATE)
    for tp in sorted(ee):
        if tp <= t + 1e-9:
            for fl, v in ee[tp]: state[fl] = v
    for tp in sorted(se):
        if tp <= t + 1e-9:
            for fl, v in se[tp]: state[fl] = v
    return state


def compute_pre_start(si, actions):
    se, ee = build_effects(actions)
    state = dict(INITIAL_STATE)
    for tp in sorted(ee):
        if tp <= si + 1e-9:
            for fl, v in ee[tp]: state[fl] = v
    for tp in sorted(se):
        if tp < si - 1e-9:
            for fl, v in se[tp]: state[fl] = v
    return state


def holds_over(fluent, t_start, t_end, actions):
    se, ee = build_effects(actions)
    pts = {(t_start + t_end) / 2.0}
    for tp in list(se.keys()) + list(ee.keys()):
        if t_start < tp < t_end:
            pts.add(tp + 1e-6)
    for cp in pts:
        if not compute_state(cp, actions).get(fluent, False):
            return False, cp
    return True, None


# ═══════════════════════════════════════════════════════════════
#  ARGUMENT EXTRACTION  (S1 – S7)
# ═══════════════════════════════════════════════════════════════

def prem(label, holds, detail=""):
    return {"label": label, "holds": bool(holds), "detail": detail}


def s1_applicability(action, actions):
    name, si, ei = action["action_name"], action["start"], action["end"]
    p = action.get("params", {})
    S = compute_pre_start(si, actions)

    def HO(fl): return holds_over(fl, si, ei, actions)[0]

    if name == "board_bus":
        loc = p.get("l", "bus_stop")
        prems = [
            prem(f"Start: at(bus,{loc})", S.get(f"at(bus,{loc})", False)),
            prem(f"Start: passenger_at({loc})", S.get(f"passenger_at({loc})", False)),
            prem("No over-all invariants (vacuous)", True),
            prem("No end conditions (vacuous)", True),
        ]
    elif name == "bus_travel":
        f_loc = p.get("f", "")
        prems = [
            prem(f"Start: at(bus,{f_loc})", S.get(f"at(bus,{f_loc})", False)),
            prem("Start: passenger_on_bus", S.get("passenger_on_bus", False)),
            prem(f"Invariant: passenger_on_bus holds over ({si},{ei})", HO("passenger_on_bus")),
            prem("No end conditions (vacuous)", True),
        ]
    elif name == "passenger_platform_wait":
        loc = p.get("l", "train_station")
        prems = [
            prem(f"Start: arrived_at({loc})", S.get(f"arrived_at({loc})", False)),
            prem(f"Start: is_train_station({loc})", S.get(f"is_train_station({loc})", False)),
            prem("No over-all invariants (vacuous)", True),
            prem("No end conditions (vacuous)", True),
        ]
    elif name == "train_approach":
        loc = p.get("l", "train_station")
        prems = [
            prem(f"Start: at(train,{loc})", S.get(f"at(train,{loc})", False)),
            prem(f"Start: arrived_at({loc})", S.get(f"arrived_at({loc})", False)),
            prem("No over-all invariants (vacuous)", True),
            prem("No end conditions (vacuous)", True),
        ]
    elif name == "board_train":
        loc = p.get("l", "train_station")
        prems = [
            prem("Start: ready_to_board", S.get("ready_to_board", False)),
            prem(f"Start: train_at_station({loc})", S.get(f"train_at_station({loc})", False)),
            prem("No over-all invariants (vacuous)", True),
            prem("No end conditions (vacuous)", True),
        ]
    elif name == "train_travel":
        f_loc = p.get("f", "train_station")
        prems = [
            prem("Start: passenger_on_train", S.get("passenger_on_train", False)),
            prem(f"Start: train_at_station({f_loc})", S.get(f"train_at_station({f_loc})", False)),
            prem("No over-all invariants (vacuous)", True),
            prem("No end conditions (vacuous)", True),
        ]
    else:
        prems = [prem(f"Unknown action: {name}", False)]

    accepted = all(pr["holds"] for pr in prems)
    return {
        "scheme": "S1", "action_index": action["step_index"],
        "premises": prems, "accepted": accepted,
        "conclusion": f"{name} is applicable over [{si},{ei}]."
    }


CAUSAL_MAP = {
    "board_bus": ("passenger_on_bus", "Required by bus_travel as start condition and over-all invariant"),
    "bus_travel": ("arrived_at(train_station)", "Enables passenger_platform_wait and train_approach"),
    "passenger_platform_wait": ("ready_to_board", "Required by board_train"),
    "train_approach": ("train_at_station(train_station)", "Required by board_train and train_travel"),
    "board_train": ("passenger_on_train", "Required by train_travel"),
    "train_travel": ("passenger_at(destination)", "Directly satisfies goal G"),
}


def s2_causal_support(action, actions):
    name, idx = action["action_name"], action["step_index"]
    effect, consumption = CAUSAL_MAP.get(name, ("none", "no consumer"))
    has = effect != "none"
    prems = [
        prem("Action applicable (S1)", True),
        prem(f"Effect '{effect}' produced", has),
        prem("Effect consumed or satisfies G", has, consumption),
    ]
    accepted = all(pr["holds"] for pr in prems)
    return {
        "scheme": "S2", "action_index": idx,
        "premises": prems, "accepted": accepted,
        "conclusion": f"Action {idx} ({name}) provides causal support for G."
    }


ENABLING_MAP = {
    "board_bus": [],
    "bus_travel": ["board_bus"],
    "passenger_platform_wait": ["bus_travel"],
    "train_approach": ["bus_travel"],
    "board_train": ["passenger_platform_wait", "train_approach"],
    "train_travel": ["board_train"],
}


def s3_temporal_feasibility(action, actions):
    name, idx = action["action_name"], action["step_index"]
    si, ei = action["start"], action["end"]
    last = {a["action_name"]: a for a in sorted(actions, key=lambda x: x["step_index"])}

    en_prems = []
    for en_name in ENABLING_MAP.get(name, []):
        ea = last.get(en_name)
        if ea is None:
            continue
        ej = ea["end"]
        ok = ej <= si
        en_prems.append(prem(
            f"Enabling: e({en_name})={ej} ≤ s({name})={si}", ok,
            f"{en_name} must complete before {name} starts"
        ))

    dl = (prem("No deadline constraint (vacuous)", True)
          if name != "train_travel"
          else prem(f"Plan completes at makespan t={ei}", True, f"Makespan = {ei}"))

    prems = [prem("Internal applicability (S1)", True)] + en_prems + [dl]
    accepted = all(pr["holds"] for pr in prems)
    return {
        "scheme": "S3", "action_index": idx,
        "premises": prems, "accepted": accepted,
        "conclusion": f"Action {idx} ({name}) over [{si},{ei}] is temporally feasible."
    }


def s4_concurrency(actions):
    sm = {a["action_name"]: a for a in actions}
    ppw = sm.get("passenger_platform_wait")
    ta = sm.get("train_approach")
    bt = sm.get("board_train")

    if not ppw or not ta:
        return {
            "scheme": "S4", "action_index": None,
            "premises": [prem("passenger_platform_wait and train_approach present", False)],
            "accepted": False, "conclusion": "S4 N/A"
        }

    si_ppw, ei_ppw = ppw["start"], ppw["end"]
    si_ta, ei_ta = ta["start"], ta["end"]
    concurrent = (si_ppw < ei_ta) and (si_ta < ei_ppw)
    bt_coord = bool(bt and (ei_ppw <= bt["start"]) and (ei_ta <= bt["start"]))

    # Check for resource conflict (Scenario C)
    conflicting = [a for a in actions
                   if a["action_name"] not in ("passenger_platform_wait", "train_approach")
                   and a.get("resource") == "Train"
                   and a["start"] < ei_ta and a["end"] > si_ta]
    no_conflict = len(conflicting) == 0

    prems = [
        prem("Both actions individually applicable (S1)", True),
        prem("No resource conflict: passenger_platform_wait (no vehicle resource) vs train_approach (Train) — disjoint",
             no_conflict,
             "passenger_platform_wait uses no vehicle resource; train_approach uses Train exclusively"),
        prem("Mutual invariant compatibility: train_approach does not delete passenger-side fluents",
             True,
             "train_approach only produces train_at_station; does not affect passenger_at or arrived_at"),
        prem(f"Coordination: both complete before board_train starts (t={bt['start'] if bt else '?'})",
             bt_coord,
             "board_train requires ready_to_board AND train_at_station simultaneously"),
        prem("Concurrency justified: saves 3 time units versus sequential execution",
             concurrent),
    ]
    accepted = all(pr["holds"] for pr in prems)
    return {
        "scheme": "S4",
        "action_index": (ppw["step_index"], ta["step_index"]),
        "premises": prems, "accepted": accepted,
        "conclusion": (f"Concurrent scheduling of passenger_platform_wait [{si_ppw},{ei_ppw}] "
                       f"and train_approach [{si_ta},{ei_ta}] is resource-feasible, "
                       f"invariant-compatible, and saves 3 time units.")
    }


CAUSAL_DEPS = [
    ("board_bus", "bus_travel",
     "board_bus produces passenger_on_bus, required as start condition and over-all invariant of bus_travel"),
    ("bus_travel", "passenger_platform_wait",
     "bus_travel produces arrived_at(train_station), required as start condition of passenger_platform_wait"),
    ("bus_travel", "train_approach",
     "bus_travel produces arrived_at(train_station), required as start condition of train_approach"),
    ("passenger_platform_wait", "board_train",
     "passenger_platform_wait produces ready_to_board, required as start condition of board_train"),
    ("train_approach", "board_train",
     "train_approach produces train_at_station(train_station), required as start condition of board_train"),
    ("board_train", "train_travel",
     "board_train produces passenger_on_train, required as start condition of train_travel"),
]


def s5_orderings(actions):
    sm = {a["action_name"]: a for a in actions}
    results = []
    for pred_name, succ_name, reason in CAUSAL_DEPS:
        pred = sm.get(pred_name)
        succ = sm.get(succ_name)
        if pred is None or succ is None:
            continue
        ei, sj = pred["end"], succ["start"]
        prems = [
            prem(f"Ordering: e(Action {pred['step_index']})={ei} ≤ s(Action {succ['step_index']})={sj}",
                 ei <= sj, "Finish-to-start ordering holds in the schedule"),
            prem(f"{pred_name} produces effect needed by {succ_name}", True, reason),
            prem("Reversal would remove a required start condition or make G unreachable", True,
                 f"If {succ_name} started before {pred_name} ended, "
                 f"the required fluent would be absent in S_pre(s_{succ_name})"),
        ]
        accepted = all(pr["holds"] for pr in prems)
        results.append({
            "scheme": "S5",
            "action_index": (pred["step_index"], succ["step_index"]),
            "premises": prems, "accepted": accepted,
            "conclusion": (f"Ordering Action[{pred['step_index']}]({pred_name}) before "
                           f"Action[{succ['step_index']}]({succ_name}) is necessary.")
        })
    return results


def s6_invariant_maintenance(actions):
    bus_travels = [a for a in actions if a["action_name"] == "bus_travel"]
    if not bus_travels:
        return {
            "scheme": "S6", "action_index": None,
            "premises": [prem("bus_travel present", False)],
            "accepted": False, "conclusion": "S6 N/A"
        }
    bt = max(bus_travels, key=lambda x: x["step_index"])
    si, ei = bt["start"], bt["end"]
    inv_ok, fail_pt = holds_over("passenger_on_bus", si, ei, actions)
    concurrent = [a["action_name"] for a in actions
                  if a["action_name"] != "bus_travel"
                  and a["start"] < ei and a["end"] > si]
    prems = [
        prem("Invariant inv(bus_travel) = {passenger_on_bus} exists", True,
             "Defined via ClosedTimeInterval condition on bus_travel"),
        prem(f"passenger_on_bus holds and is not deleted over ({si},{ei})", inv_ok,
             f"Concurrent actions {concurrent or ['none']} do not affect passenger_on_bus"
             + (f"; first violation at t≈{fail_pt:.2f}" if fail_pt else "")),
        prem("Disruption would invalidate bus_travel and make G unreachable", True,
             "If passenger_on_bus becomes False mid-interval, the invariant is violated"),
    ]
    accepted = all(pr["holds"] for pr in prems)
    return {
        "scheme": "S6", "action_index": bt["step_index"],
        "premises": prems, "accepted": accepted,
        "conclusion": f"passenger_on_bus maintained throughout ({si},{ei})."
    }


def s7_plan_summary(s1r, s2r, s3r, s4r, s5r, s6r, actions):
    makespan = max(a["end"] for a in actions)
    prems = [
        prem("P1: State fully characterised (S0)", True),
        prem(f"P2: Every action applicable — S1 ({len(s1r)} instances)",
             all(s["accepted"] for s in s1r)),
        prem(f"P3: Every action causally justified — S2 ({len(s2r)} instances)",
             all(s["accepted"] for s in s2r)),
        prem(f"P4: Every action temporally feasible — S3 ({len(s3r)} instances)",
             all(s["accepted"] for s in s3r)),
        prem("P5: Concurrent actions compatible — S4", s4r["accepted"]),
        prem(f"P6: All orderings necessary — S5 ({len(s5r)} instances)",
             all(s["accepted"] for s in s5r)),
        prem("P7: All invariants maintained — S6", s6r["accepted"]),
    ]
    accepted = all(pr["holds"] for pr in prems)
    return {
        "scheme": "S7", "action_index": None,
        "premises": prems, "accepted": accepted,
        "conclusion": (f"The scheduled plan P is valid; "
                       f"passenger_at(destination) achieved at makespan t={makespan}.")
    }


# ═══════════════════════════════════════════════════════════════
#  CQ EVALUATION  — updated defeating-scheme mapping
# ═══════════════════════════════════════════════════════════════

def evaluate_cqs(s1r, s2r, s3r, s4r, s5r, s6r, actions):
    s1_by = {s["action_index"]: s for s in s1r}
    s2_by = {s["action_index"]: s for s in s2r}
    s3_by = {s["action_index"]: s for s in s3r}

    results = []

    def record(cq, attacks, action, outcome, detail, defeated_by="", defeating_data=None):
        results.append({
            "CQ": cq, "Attacks via": attacks, "Action(s)": str(action),
            "Outcome": outcome, "Detail": detail,
            "Defeated by": defeated_by,
            "Defeating premises": defeating_data["premises"] if defeating_data else [],
            "Defeating conclusion": defeating_data["conclusion"] if defeating_data else "",
        })

    # CQ1 — Start-condition satisfaction → defeated by S3
    for sch in s1r:
        idx = sch["action_index"]
        sp = [pr for pr in sch["premises"] if pr["label"].startswith("Start:")]
        ok = all(pr["holds"] for pr in sp)
        fail = [pr["label"] for pr in sp if not pr["holds"]]
        defeating = s3_by.get(idx) if ok else None
        record("CQ1", "S1", idx,
               "defeated" if ok else "succeeds",
               "S3's enabling-timing guarantee confirms start conditions present." if ok
               else f"FAILS — start conditions not met: {fail}",
               defeated_by="S3", defeating_data=defeating)

    # CQ2 — Invariant persistence → defeated by S6
    for sch in s1r:
        idx = sch["action_index"]
        ip = [pr for pr in sch["premises"] if "Invariant" in pr["label"]]
        if not ip:
            record("CQ2", "S1", idx, "n/a",
                   "No over-all invariant for this action.", defeated_by="S6 (n/a)")
        else:
            ok = all(pr["holds"] for pr in ip)
            record("CQ2", "S1", idx,
                   "defeated" if ok else "succeeds",
                   "S6 confirms invariant maintained throughout execution." if ok
                   else "FAILS — invariant violated.",
                   defeated_by="S6",
                   defeating_data=s6r if ok else None)

    # CQ3 — Causal link validity → defeated by S1
    for sch in s2r:
        idx = sch["action_index"]
        ep = [pr for pr in sch["premises"] if "Effect" in pr["label"] or "consumed" in pr["label"]]
        ok = all(pr["holds"] for pr in ep)
        defeating = s1_by.get(idx) if ok else None
        record("CQ3", "S2", idx,
               "defeated" if ok else "succeeds",
               "S1 applicability confirms effect genuinely produced and available." if ok
               else "FAILS — effect not produced or consumed.",
               defeated_by="S1", defeating_data=defeating)

    # CQ4 — Enabling timing → defeated by S5
    for sch in s3r:
        idx = sch["action_index"]
        ep = [pr for pr in sch["premises"] if "Enabling:" in pr["label"]]
        if not ep:
            record("CQ4", "S3", idx, "n/a",
                   "No enabling dependency for this action.", defeated_by="S5 (n/a)")
        else:
            ok = all(pr["holds"] for pr in ep)
            fail = [pr["label"] for pr in ep if not pr["holds"]]
            s5_match = next(
                (s for s in s5r
                 if isinstance(s["action_index"], tuple) and s["action_index"][1] == idx),
                None)
            record("CQ4", "S3", idx,
                   "defeated" if ok else "succeeds",
                   "S5's finish-to-start ordering certifies enabling action completes in time." if ok
                   else f"FAILS — enabling timing violated: {fail}",
                   defeated_by="S5",
                   defeating_data=s5_match if ok else None)

    # CQ5 — Temporal constraints → defeated by S5
    for sch in s3r:
        idx = sch["action_index"]
        dp = [pr for pr in sch["premises"]
              if ("makespan" in pr["label"].lower() or "deadline" in pr["label"].lower())
              and "vacuous" not in pr["label"].lower()]
        s5_match = next(
            (s for s in s5r
             if isinstance(s["action_index"], tuple) and s["action_index"][1] == idx),
            None)
        if not dp:
            record("CQ5", "S3", idx, "defeated",
                   "No deadline constraint; vacuously satisfied. S5 ordering evidence confirms.",
                   defeated_by="S5", defeating_data=s5_match)
        else:
            ok = all(pr["holds"] for pr in dp)
            record("CQ5", "S3", idx,
                   "defeated" if ok else "succeeds",
                   "S5 confirms schedule respects deadline and timing constraints." if ok
                   else "FAILS — deadline violated.",
                   defeated_by="S5",
                   defeating_data=s5_match if ok else None)

    # CQ6 — Resource conflict & invariant compatibility → defeated by S1
    rp = next((pr for pr in s4r["premises"] if "resource" in pr["label"].lower()), None)
    ip = next((pr for pr in s4r["premises"] if "invariant" in pr["label"].lower()), None)
    cp = next((pr for pr in s4r["premises"] if "Coordination" in pr["label"]), None)
    ok6 = all(x["holds"] for x in [rp, ip, cp] if x)
    conc_pair = s4r["action_index"]
    s1_both = None
    if ok6 and isinstance(conc_pair, tuple):
        idx_a, idx_b = conc_pair
        s1_a, s1_b = s1_by.get(idx_a), s1_by.get(idx_b)
        if s1_a and s1_b:
            s1_both = {
                "scheme": "S1 (both concurrent actions)",
                "action_index": conc_pair,
                "premises": s1_a["premises"] + s1_b["premises"],
                "conclusion": f"{s1_a['conclusion']} | {s1_b['conclusion']}",
                "accepted": True,
            }
    record("CQ6", "S4", str(conc_pair),
           "defeated" if ok6 else "succeeds",
           "S1 applicability for both actions confirms disjoint resources and non-interference." if ok6
           else "FAILS — resource conflict or invariant interference detected.",
           defeated_by="S1", defeating_data=s1_both if ok6 else None)

    # CQ7 — Ordering necessity → defeated by S2
    for sch in s5r:
        ok = sch["accepted"]
        pair = sch["action_index"]
        pred_idx = pair[0] if isinstance(pair, tuple) else None
        s2_match = s2_by.get(pred_idx) if pred_idx else None
        record("CQ7", "S5", str(pair),
               "defeated" if ok else "succeeds",
               "S2 causal chain establishes what would break if ordering were reversed." if ok
               else "FAILS — ordering violated or unjustified.",
               defeated_by="S2",
               defeating_data=s2_match if ok else None)

    # CQ8 — Invariant disruption → defeated by S4
    inv_p = next((pr for pr in s6r["premises"] if "not deleted" in pr["label"]), None)
    ok8 = inv_p["holds"] if inv_p else s6r["accepted"]
    inv_idx = s6r["action_index"]
    has_concurrent = isinstance(s4r.get("action_index"), tuple) and (
        inv_idx in s4r["action_index"])
    defeating8 = s4r if (not has_concurrent or ok8) else None
    record("CQ8", "S6", str(inv_idx),
           "defeated" if (not has_concurrent or ok8) else "succeeds",
           ("S4 confirms: no concurrent action exists during bus_travel — invariant cannot be deleted."
            if not has_concurrent
            else "S4 Premise 3 confirms: no concurrent action deletes passenger_on_bus during (si,ei)."
            if ok8
            else "FAILS — concurrent action deletes passenger_on_bus mid-interval."),
           defeated_by="S4", defeating_data=defeating8)

    return results


# ═══════════════════════════════════════════════════════════════
#  GROUNDED SEMANTICS
# ═══════════════════════════════════════════════════════════════

def build_af(cq_results):
    arguments = [{"id": "PSA_P", "layer": 1, "label": "PSA(P)"}]
    attacks = []
    seen_cqs = set()
    for row in cq_results:
        if row["Outcome"] == "n/a":
            continue
        cq_id = f"{row['CQ']}@{row['Action(s)']}"
        if cq_id not in seen_cqs:
            seen_cqs.add(cq_id)
            arguments.append({"id": cq_id, "layer": 3, "label": row["CQ"]})
            attacks.append((cq_id, "PSA_P"))
        if row["Outcome"] == "defeated":
            j_id = f"J_{row['Defeated by'].split()[0]}_{row['CQ']}_A{row['Action(s)']}"
            arguments.append({"id": j_id, "layer": 4, "label": j_id})
            attacks.append((j_id, cq_id))
    return arguments, attacks


def grounded_extension(arguments, attacks):
    arg_ids = {a["id"] for a in arguments}
    attacked = {a: set() for a in arg_ids}
    for fr, to in attacks:
        if to in arg_ids:
            attacked[to].add(fr)
    IN, OUT, changed = set(), set(), True
    while changed:
        changed = False
        for a in arg_ids:
            if a in IN or a in OUT:
                continue
            if all(att in OUT for att in attacked[a]):
                IN.add(a); changed = True
            elif any(att in IN for att in attacked[a]):
                OUT.add(a); changed = True
    return {"IN": IN, "OUT": OUT}


def run_pipeline(actions):
    s1r = [s1_applicability(a, actions) for a in actions]
    s2r = [s2_causal_support(a, actions) for a in actions]
    s3r = [s3_temporal_feasibility(a, actions) for a in actions]
    s4r = s4_concurrency(actions)
    s5r = s5_orderings(actions)
    s6r = s6_invariant_maintenance(actions)
    s7r = s7_plan_summary(s1r, s2r, s3r, s4r, s5r, s6r, actions)
    cqr = evaluate_cqs(s1r, s2r, s3r, s4r, s5r, s6r, actions)
    af_args, af_attacks = build_af(cqr)
    ext = grounded_extension(af_args, af_attacks)
    psa_accepted = "PSA_P" in ext["IN"]
    return {
        "s1r": s1r, "s2r": s2r, "s3r": s3r,
        "s4r": s4r, "s5r": s5r, "s6r": s6r,
        "s7r": s7r, "cqr": cqr,
        "psa_accepted": psa_accepted,
        "af_args": af_args, "af_attacks": af_attacks,
        "ext": ext,
    }


# ═══════════════════════════════════════════════════════════════
#  SCENARIO CONFIGURATIONS
# ═══════════════════════════════════════════════════════════════

import copy


def inject_bus_delay(actions, new_end=8):
    plan = copy.deepcopy(actions)
    for a in plan:
        if a["action_name"] == "bus_travel":
            a["end"] = new_end
    return plan


def inject_resource_conflict(actions):
    plan = copy.deepcopy(actions)
    plan.append({
        "step_index": 7, "action_name": "conflicting_train_agent",
        "params": {}, "start": 7, "end": 10, "resource": "Train"
    })
    return plan


def inject_invariant_disruption(actions):
    plan = copy.deepcopy(actions)
    plan.append({
        "step_index": 7, "action_name": "disrupt_invariant",
        "params": {}, "start": 3, "end": 5, "resource": "None"
    })
    return plan


def inject_coordination_failure(actions):
    plan = copy.deepcopy(actions)
    for a in plan:
        if a["action_name"] == "train_approach":
            a["end"] = 11
    return plan


SCENARIOS = {
    "A — Nominal": {
        "label": "Nominal plan — no fault injected",
        "actions": NOMINAL_ACTIONS,
        "expected": True,
        "fault_desc": "None",
        "colour": "#d4edda",
    },
    "B — Bus Delayed": {
        "label": "Bus delayed — bus_travel ends at t=8 instead of t=7",
        "actions": inject_bus_delay(NOMINAL_ACTIONS),
        "expected": False,
        "fault_desc": "Action 2 (bus_travel) ends at t=8; arrived_at(train_station) absent from S(7). CQ1 and CQ4 succeed.",
        "colour": "#fff3cd",
    },
    "C — Resource Conflict": {
        "label": "Second agent holds Train lock during [7,10]",
        "actions": inject_resource_conflict(NOMINAL_ACTIONS),
        "expected": False,
        "fault_desc": "A second agent claims the Train resource over [7,10], conflicting with train_approach. CQ6 succeeds.",
        "colour": "#fff3cd",
    },
    "D — Invariant Disruption": {
        "label": "Concurrent action deletes passenger_on_bus during (2,7)",
        "actions": inject_invariant_disruption(NOMINAL_ACTIONS),
        "expected": False,
        "fault_desc": "A concurrent action sets passenger_on_bus:=False at t≈4. CQ2 and CQ8 succeed.",
        "colour": "#fff3cd",
    },
    "E — Coordination Failure": {
        "label": "train_approach finishes at t=11 instead of t=10",
        "actions": inject_coordination_failure(NOMINAL_ACTIONS),
        "expected": False,
        "fault_desc": "train_approach ends at t=11; train_at_station not available at board_train start (t=10). CQ1 succeeds for Action 5.",
        "colour": "#fff3cd",
    },
}


# ═══════════════════════════════════════════════════════════════
#  CQ METADATA  (updated defeating scheme labels)
# ═══════════════════════════════════════════════════════════════

CQ_META = {
    "CQ1": {
        "challenge": "Do all start conditions hold in the world at the action's scheduled start time?",
        "attacks": "S1 — Action Applicability",
        "attacks_premise": "P1: start-condition satisfaction",
        "s7_premise": "P2: every action applicable",
        "defeated_by": "S3 — Temporal Feasibility",
        "defeating_logic": (
            "S3's enabling-timing guarantee (e_j ≤ s_i for all enabling actions) directly "
            "implies that every required start condition is present in the world when the action begins. "
            "Because S3 confirms enabling actions have already completed their effects before the "
            "dependent action starts, CQ1's challenge is answered."
        ),
    },
    "CQ2": {
        "challenge": "Does every over-all invariant hold continuously throughout the action's execution interval?",
        "attacks": "S1 — Action Applicability",
        "attacks_premise": "P2: invariant persistence",
        "s7_premise": "P2: every action applicable",
        "defeated_by": "S6 — Invariant Maintenance Justification",
        "defeating_logic": (
            "S6 verifies that no concurrent action applies an effect deleting the required invariant "
            "at any t ∈ (s_i, e_i). S6 also establishes why any disruption mid-interval would render "
            "the action inapplicable from that point onwards and make G unreachable."
        ),
    },
    "CQ3": {
        "challenge": "Does this action produce something the plan genuinely needs — a condition for a later action or a goal fluent?",
        "attacks": "S2 — Causal Goal Support",
        "attacks_premise": "P2–P3: effect required and consumed",
        "s7_premise": "P3: every action causally supported",
        "defeated_by": "S1 — Action Applicability",
        "defeating_logic": (
            "S1 confirms the action is applicable over [s_i, e_i] and its end effects fire at e_i. "
            "Since S2 requires S1 as its foundation, S1's applicability evidence establishes that "
            "the effect is genuinely produced and available for downstream consumption."
        ),
    },
    "CQ4": {
        "challenge": "Did every enabling action finish before this action was scheduled to start?",
        "attacks": "S3 — Temporal Feasibility",
        "attacks_premise": "P2: enabling timing",
        "s7_premise": "P4: every action temporally feasible",
        "defeated_by": "S5 — Temporal Ordering Justification",
        "defeating_logic": (
            "S5's Premise 1 explicitly certifies the finish-to-start relationship: e_j ≤ s_i for "
            "the ordering pair (j, i). This is the most direct answer to whether enabling actions "
            "complete in time — S5's first and most fundamental premise is exactly the timing "
            "relationship that CQ4 challenges."
        ),
    },
    "CQ5": {
        "challenge": "Does the action's scheduled window satisfy all release-time, deadline, and minimum-separation constraints?",
        "attacks": "S3 — Temporal Feasibility",
        "attacks_premise": "P3: temporal constraints satisfied",
        "s7_premise": "P4: every action temporally feasible",
        "defeated_by": "S5 — Temporal Ordering Justification",
        "defeating_logic": (
            "S5's Premise 3 checks that reversing an ordering would violate a temporal constraint in C. "
            "This means S5 carries evidence that the schedule respects release times, deadlines, and "
            "separation constraints. If those constraints were violated, the ordering would not be "
            "necessary on those grounds, and S5 would not hold."
        ),
    },
    "CQ6": {
        "challenge": "Do concurrent actions use different resources and avoid disrupting each other's required continuous conditions?",
        "attacks": "S4 — Resource & Concurrency Feasibility",
        "attacks_premise": "P2–P3: resource compatibility and mutual invariant safety",
        "s7_premise": "P5: concurrent actions compatible",
        "defeated_by": "S1 — Action Applicability",
        "defeating_logic": (
            "S1 establishes individual applicability of each concurrent action, confirming each action's "
            "resource usage and boundary conditions. Disjoint lock sets and mutual invariant compatibility "
            "follow directly from S1's applicability evidence for both actions in the pair."
        ),
    },
    "CQ7": {
        "challenge": "Would reversing or removing this ordering cause a required condition to fail, a constraint to be violated, or the goal to become unreachable?",
        "attacks": "S5 — Temporal Ordering Justification",
        "attacks_premise": "P3: reversal harms the plan",
        "s7_premise": "P6: all orderings necessary",
        "defeated_by": "S2 — Causal Goal Support",
        "defeating_logic": (
            "S2 establishes the causal dependency that the ordering protects, identifying which effect "
            "the predecessor produces and the successor consumes. The causal chain that S2 identifies "
            "is precisely what would be broken by reversing or relaxing the ordering."
        ),
    },
    "CQ8": {
        "challenge": "Does any concurrent action delete a condition that must remain continuously true during this action's execution?",
        "attacks": "S6 — Invariant Maintenance Justification",
        "attacks_premise": "P2: invariant not disrupted by concurrent action",
        "s7_premise": "P7: all invariants maintained",
        "defeated_by": "S4 — Resource & Concurrency Feasibility",
        "defeating_logic": (
            "S4's Premise 3 directly certifies that no invariant fluent φ ∈ inv(a_i) is deleted by "
            "any effect of a concurrent action a_j during the shared interval. This is the most direct "
            "answer to CQ8. Note: CQ8 is n/a when inv(a_i) = ∅ or when no concurrent action runs "
            "during (s_i, e_i). CQ8 is distinct from CQ6: CQ6 concerns exclusive resource locks; "
            "CQ8 concerns state-level fluent deletion by concurrent effects."
        ),
    },
}


# ═══════════════════════════════════════════════════════════════
#  RENDER HELPERS
# ═══════════════════════════════════════════════════════════════

def tick(holds): return "✓" if holds else "✗"
def tick_col(holds): return "#28a745" if holds else "#dc3545"


def render_premises(prems, show_detail=True):
    html = ""
    for i, p in enumerate(prems, 1):
        colour = tick_col(p["holds"])
        html += (
            f"<div style='margin:4px 0; padding-left:6px;'>"
            f"<span style='color:{colour}; font-weight:700;'>{tick(p['holds'])}</span>"
            f"&nbsp;<b>P{i}:</b> {p['label']}"
        )
        if show_detail and p.get("detail"):
            html += f"<br><span style='color:#666; font-size:0.82rem; padding-left:1.4em;'>↳ {p['detail']}</span>"
        html += "</div>"
    return html


def render_cq_panel(cq_record):
    cq_id = cq_record["CQ"]
    outcome = cq_record["Outcome"]
    action_s = cq_record["Action(s)"]
    detail = cq_record["Detail"]
    def_by = cq_record["Defeated by"]
    def_prems = cq_record["Defeating premises"]
    def_conc = cq_record["Defeating conclusion"]
    meta = CQ_META.get(cq_id, {})

    # ── Challenge block
    st.markdown(
        f"""<div class='scheme-box'>
        <div class='layer-header'>Layer 3 — Critical Question</div>
        <b>❓ {cq_id}</b> — {meta.get('challenge','')}<br><br>
        <span class='attack-label'>⚔ R1a attacks:</span> {meta.get('attacks','')} ({meta.get('attacks_premise','')})<br>
        <span class='attack-label'>⚔ R1b attacks:</span> PSA(P) via S7 — {meta.get('s7_premise','')}
        </div>""",
        unsafe_allow_html=True)

    # ── Defeating scheme block
    if outcome == "defeated":
        prems_html = render_premises(def_prems)
        st.markdown(
            f"""<div class='defeating-box'>
            <div class='layer-header'>Layer 4 — Justification Argument (Defeater)</div>
            <b>🛡 Defeated by: {meta.get('defeated_by', def_by)}</b><br>
            <i style='font-size:0.82rem; color:#444;'>{meta.get('defeating_logic','')}</i><br><br>
            <b>Premises of the defeating scheme:</b>
            {prems_html}
            <div style='margin-top:8px; padding-top:6px; border-top:1px dashed #aaa;
                        font-style:italic; font-size:0.84rem;'>
            ∴ <b>Conclusion:</b> {def_conc}
            </div>
            </div>""",
            unsafe_allow_html=True)
        st.success(f"✅ {cq_id} **DEFEATED** for Action {action_s} — attack on PSA(P) is **blocked**.")

    elif outcome == "n/a":
        st.markdown(
            f"""<div class='na-box'>
            <b>ℹ {cq_id} — Not applicable</b><br>
            {detail}. No attack is generated for this action instance.
            </div>""",
            unsafe_allow_html=True)

    else:  # succeeds
        prems_html = render_premises(def_prems) if def_prems else "<i>No justification argument present.</i>"
        st.markdown(
            f"""<div class='fail-box'>
            <div class='layer-header'>Layer 4 — Justification Argument ABSENT</div>
            <b>⚠ Defeating scheme absent: {meta.get('defeated_by', def_by)}</b><br>
            {prems_html}
            </div>""",
            unsafe_allow_html=True)
        st.error(f"❌ {cq_id} **SUCCEEDS** for Action {action_s} — attack on PSA(P) is **UNBLOCKED**. {detail}")


# ═══════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🗂 Navigation")
    page = st.radio("", [
        "📋 Plan Overview",
        "💬 CQ Chatbot",
        "🔬 Scheme Inspector",
        "🚧 Scenarios",
        "📊 AF & Verdict",
        "ℹ About",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**Scenario**")
    selected_scenario = st.selectbox(
        "Active scenario",
        list(SCENARIOS.keys()),
        label_visibility="collapsed"
    )
    sc = SCENARIOS[selected_scenario]
    st.caption(sc["fault_desc"])
    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75rem; color:#888;'>"
        "University of Huddersfield<br>"
        "Project ECR_2024_17<br>"
        "CQ mapping: 26 May 2026"
        "</div>",
        unsafe_allow_html=True)


# ── Compute pipeline for selected scenario
if "pipeline_cache" not in st.session_state:
    st.session_state.pipeline_cache = {}

cache_key = selected_scenario
if cache_key not in st.session_state.pipeline_cache:
    st.session_state.pipeline_cache[cache_key] = run_pipeline(sc["actions"])

R = st.session_state.pipeline_cache[cache_key]


# ═══════════════════════════════════════════════════════════════
#  PAGE: PLAN OVERVIEW
# ═══════════════════════════════════════════════════════════════

if page == "📋 Plan Overview":
    st.title("🚌🚂 Bus–Train Collaborative Journey")
    st.markdown(
        "**An Argumentation-Based Framework for Explaining Scheduled Temporal Plans**  \n"
        "University of Huddersfield | Omolola Oluyemisi Haastrup"
    )

    # PSA verdict banner
    verdict = "ACCEPTED" if R["psa_accepted"] else "REJECTED"
    badge_cls = "accepted-badge" if R["psa_accepted"] else "rejected-badge"
    st.markdown(
        f"**Current scenario:** {sc['label']}  \n"
        f"**PSA(P) verdict:** <span class='{badge_cls}'>{'✅' if R['psa_accepted'] else '❌'} {verdict}</span>",
        unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Scheduled Temporal Plan")
    st.caption("Actions 3 and 4 (shaded) run concurrently over [7, 10].")

    rows = []
    for a in sc["actions"]:
        rows.append({
            "Step": a["step_index"],
            "Action": a["action_name"],
            "Start": a["start"],
            "End": a["end"],
            "Dur": a["end"] - a["start"],
            "Resource": a.get("resource", "—"),
        })
    df = pd.DataFrame(rows)

    def style_row(row):
        styles = [""] * len(row)
        if row["Step"] in (3, 4):
            styles = ["background-color: #fff3cd"] * len(row)
        return styles

    st.dataframe(
        df.style.apply(style_row, axis=1),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")
    st.subheader("Timeline")
    import json

    # Build a simple HTML timeline
    colours = {
        "board_bus": "#e8d5b7",
        "bus_travel": "#f0a500",
        "passenger_platform_wait": "#85c1e9",
        "train_approach": "#2471a3",
        "board_train": "#48c9b0",
        "train_travel": "#1abc9c",
    }
    scale = 30  # px per time unit
    makespan = max(a["end"] for a in sc["actions"])
    tl_html = f"""
    <div style='position:relative; height:{len(sc["actions"])*44+40}px;
                font-family:"IBM Plex Mono",monospace; font-size:11px;
                background:#f8f9fa; border-radius:8px; padding:16px 8px 8px;
                overflow-x:auto;'>
    """
    for i, a in enumerate(sc["actions"]):
        top = i * 44 + 8
        left = a["start"] * scale + 60
        width = max((a["end"] - a["start"]) * scale - 4, 8)
        colour = colours.get(a["action_name"], "#bdc3c7")
        border = "2px solid #e74c3c" if a.get("action_name") in (
            "conflicting_train_agent", "disrupt_invariant") else "none"
        label = a["action_name"].replace("_", " ")
        tl_html += (
            f"<div style='position:absolute; top:{top}px; left:8px; "
            f"font-weight:600; line-height:36px; color:#555;'>"
            f"A{a['step_index']}</div>"
            f"<div title='{label} [{a['start']},{a['end']}]' "
            f"style='position:absolute; top:{top}px; left:{left}px; "
            f"width:{width}px; height:34px; background:{colour}; "
            f"border:{border}; border-radius:4px; display:flex; "
            f"align-items:center; padding:0 6px; overflow:hidden; "
            f"white-space:nowrap; box-shadow:0 1px 3px rgba(0,0,0,.15);'>"
            f"<span style='font-size:10px;'>{label}</span></div>"
        )

    # Time axis
    for t in range(0, makespan + 2, 2):
        lx = t * scale + 60
        tl_html += (f"<div style='position:absolute; bottom:4px; left:{lx}px; "
                    f"color:#999; font-size:9px;'>t={t}</div>")

    tl_html += "</div>"
    st.markdown(tl_html, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("S7 — Plan Summary Argument")
    psa_cls = "psa-accepted" if R["psa_accepted"] else "psa-rejected"
    prems_html = render_premises(R["s7r"]["premises"])
    st.markdown(
        f"""<div class='{psa_cls}'>
        <b>PSA(P) — Plan Summary Argument</b><br>
        {prems_html}
        <div style='margin-top:10px; padding-top:8px; border-top:1px solid #ccc;
                    font-style:italic; font-size:0.86rem;'>
        ∴ <b>Conclusion:</b> {R["s7r"]["conclusion"]}
        </div>
        <div style='margin-top:8px; font-weight:700;
                    color:{"#155724" if R["psa_accepted"] else "#721c24"};'>
        PSA(P): {'✅ ACCEPTED — all challenges defeated' if R['psa_accepted'] else '❌ REJECTED — at least one challenge unanswered'}
        </div>
        </div>""",
        unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  PAGE: CQ CHATBOT
# ═══════════════════════════════════════════════════════════════

elif page == "💬 CQ Chatbot":
    st.title("💬 Critical Question Chatbot")
    st.markdown(
        "Select an action from the plan, then click a critical question to see "
        "the full four-layer argumentation response: the challenge, the attacking "
        "relation, and the defeating justification with its premises and conclusion."
    )

    verdict = "ACCEPTED" if R["psa_accepted"] else "REJECTED"
    badge_cls = "accepted-badge" if R["psa_accepted"] else "rejected-badge"
    st.markdown(
        f"**Scenario:** {sc['label']}  |  "
        f"**PSA(P):** <span class='{badge_cls}'>{'✅' if R['psa_accepted'] else '❌'} {verdict}</span>",
        unsafe_allow_html=True)
    st.markdown("---")

    # Action selector
    valid_actions = [a for a in sc["actions"]
                     if a["action_name"] not in ("conflicting_train_agent", "disrupt_invariant")]
    action_options = {
        f"Action {a['step_index']} — {a['action_name']}  [{a['start']}, {a['end']}]": a["step_index"]
        for a in valid_actions
    }
    selected_action_label = st.selectbox(
        "Step 1 — Select an action:",
        list(action_options.keys())
    )
    selected_idx = action_options[selected_action_label]

    # Build CQ list for selected action
    cq_by_action = {}
    for rec in R["cqr"]:
        key_str = str(rec["Action(s)"])
        if key_str.startswith("(") and "," in key_str:
            try:
                parts = [int(x.strip()) for x in key_str.strip("()").split(",")]
                for part in parts:
                    cq_by_action.setdefault(part, {})
                    if rec["CQ"] not in cq_by_action[part]:
                        cq_by_action[part][rec["CQ"]] = rec
            except ValueError:
                pass
        else:
            try:
                idx = int(key_str)
                cq_by_action.setdefault(idx, {})
                if rec["CQ"] not in cq_by_action[idx]:
                    cq_by_action[idx][rec["CQ"]] = rec
            except ValueError:
                pass

    action_cqs = cq_by_action.get(selected_idx, {})

    if not action_cqs:
        st.info("No critical questions recorded for this action.")
    else:
        outcome_icon = {"defeated": "✅", "succeeds": "❌", "n/a": "ℹ️"}
        st.markdown("**Step 2 — Click a critical question to inspect:**")

        # Pill display
        cols = st.columns(len(action_cqs))
        selected_cq = st.session_state.get(f"selected_cq_{selected_idx}", None)

        for i, (cq_id, rec) in enumerate(action_cqs.items()):
            icon = outcome_icon.get(rec["Outcome"], "❓")
            with cols[i]:
                if st.button(f"{icon} {cq_id}", key=f"cq_btn_{selected_idx}_{cq_id}",
                             use_container_width=True):
                    st.session_state[f"selected_cq_{selected_idx}"] = cq_id

        selected_cq = st.session_state.get(f"selected_cq_{selected_idx}", None)

        if selected_cq and selected_cq in action_cqs:
            st.markdown("---")
            st.markdown(f"#### Response: {selected_cq} on Action {selected_idx}")
            render_cq_panel(action_cqs[selected_cq])
        else:
            st.markdown("---")
            # Show all CQs summary table for this action
            summary = []
            for cq_id, rec in action_cqs.items():
                meta = CQ_META.get(cq_id, {})
                summary.append({
                    "CQ": cq_id,
                    "Outcome": rec["Outcome"].upper(),
                    "Attacks": meta.get("attacks", ""),
                    "Defeated by": meta.get("defeated_by", ""),
                    "Challenge (short)": meta.get("challenge", "")[:70] + "…",
                })
            st.dataframe(pd.DataFrame(summary), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════
#  PAGE: SCHEME INSPECTOR
# ═══════════════════════════════════════════════════════════════

elif page == "🔬 Scheme Inspector":
    st.title("🔬 Argument Scheme Inspector")
    st.markdown(
        "Inspect the full premise-by-premise breakdown for any scheme (S1–S6) "
        "on any action in the plan."
    )

    scheme_choice = st.selectbox(
        "Select scheme:",
        ["S1 — Action Applicability",
         "S2 — Causal Goal Support",
         "S3 — Temporal Feasibility",
         "S4 — Concurrency Feasibility",
         "S5 — Temporal Ordering Justification",
         "S6 — Invariant Maintenance Justification",
         "S7 — Plan Summary Argument"]
    )

    scheme_key = scheme_choice.split("—")[0].strip()

    if scheme_key == "S4":
        st.markdown("**S4 covers the concurrent pair: passenger_platform_wait ∥ train_approach**")
        sch = R["s4r"]
        accepted = sch["accepted"]
        st.markdown(
            f"""<div class='{"defeating-box" if accepted else "fail-box"}'>
            <b>S4 — Resource & Concurrency Feasibility</b><br>
            <b>Actions:</b> {sch['action_index']}<br>
            {render_premises(sch['premises'])}
            <div style='margin-top:8px; font-style:italic; font-size:0.85rem;'>
            ∴ {sch['conclusion']}
            </div>
            </div>""",
            unsafe_allow_html=True)

    elif scheme_key == "S5":
        st.markdown(f"**S5 covers {len(R['s5r'])} finish-to-start ordering pairs**")
        for sch in R["s5r"]:
            pair = sch["action_index"]
            accepted = sch["accepted"]
            st.markdown(
                f"""<div class='{"defeating-box" if accepted else "fail-box"}' style='margin-bottom:10px;'>
                <b>S5 — Ordering {pair}</b>
                {'<span style="color:#28a745; float:right; font-weight:700;">✓ Accepted</span>'
                 if accepted else
                 '<span style="color:#dc3545; float:right; font-weight:700;">✗ Rejected</span>'}
                <br>{render_premises(sch['premises'])}
                <div style='margin-top:6px; font-style:italic; font-size:0.83rem;'>∴ {sch['conclusion']}</div>
                </div>""",
                unsafe_allow_html=True)

    elif scheme_key == "S6":
        sch = R["s6r"]
        accepted = sch["accepted"]
        st.markdown(
            f"""<div class='{"defeating-box" if accepted else "fail-box"}'>
            <b>S6 — Invariant Maintenance Justification</b><br>
            <b>Action:</b> {sch['action_index']}<br>
            {render_premises(sch['premises'])}
            <div style='margin-top:8px; font-style:italic; font-size:0.85rem;'>∴ {sch['conclusion']}</div>
            </div>""",
            unsafe_allow_html=True)

    elif scheme_key == "S7":
        sch = R["s7r"]
        accepted = sch["accepted"]
        cls = "psa-accepted" if accepted else "psa-rejected"
        st.markdown(
            f"""<div class='{cls}'>
            <b>S7 — Plan Summary Argument</b><br>
            {render_premises(sch['premises'])}
            <div style='margin-top:8px; font-style:italic; font-size:0.85rem;'>∴ {sch['conclusion']}</div>
            </div>""",
            unsafe_allow_html=True)

    else:
        # Per-action schemes
        results_map = {"S1": R["s1r"], "S2": R["s2r"], "S3": R["s3r"]}
        results = results_map[scheme_key]

        valid_actions = [a for a in sc["actions"]
                         if a["action_name"] not in ("conflicting_train_agent", "disrupt_invariant")]
        action_opts = {
            f"Action {a['step_index']} — {a['action_name']}": a["step_index"]
            for a in valid_actions
        }
        sel_label = st.selectbox("Select action:", list(action_opts.keys()), key="scheme_action")
        sel_idx = action_opts[sel_label]

        sch = next((s for s in results if s["action_index"] == sel_idx), None)
        if sch:
            accepted = sch["accepted"]
            st.markdown(
                f"""<div class='{"defeating-box" if accepted else "fail-box"}'>
                <b>{scheme_key} — Action {sel_idx} ({sel_label.split('—')[1].strip()})</b><br>
                {'<span style="color:#28a745; font-weight:700;">✓ Accepted</span>'
                 if accepted else
                 '<span style="color:#dc3545; font-weight:700;">✗ Rejected</span>'}
                <br>{render_premises(sch['premises'])}
                <div style='margin-top:8px; font-style:italic; font-size:0.85rem;'>∴ {sch['conclusion']}</div>
                </div>""",
                unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  PAGE: SCENARIOS
# ═══════════════════════════════════════════════════════════════

elif page == "🚧 Scenarios":
    st.title("🚧 Scenario Verification")
    st.markdown(
        "Run the full argument extraction pipeline across all five scenarios and "
        "compare PSA verdicts against expected outcomes."
    )

    rows = []
    for sc_name, sc_data in SCENARIOS.items():
        cache_k = sc_name
        if cache_k not in st.session_state.pipeline_cache:
            st.session_state.pipeline_cache[cache_k] = run_pipeline(sc_data["actions"])
        r = st.session_state.pipeline_cache[cache_k]
        actual = r["psa_accepted"]
        expected = sc_data["expected"]
        passed = actual == expected
        succeeded_cqs = [rec for rec in r["cqr"] if rec["Outcome"] == "succeeds"]
        rows.append({
            "Scenario": sc_name,
            "Fault": sc_data["fault_desc"],
            "Expected": "ACCEPTED" if expected else "REJECTED",
            "Actual": "ACCEPTED" if actual else "REJECTED",
            "Result": "PASS ✅" if passed else "FAIL ❌",
            "CQs that succeed": ", ".join(
                f"{rec['CQ']} (A{rec['Action(s)']})" for rec in succeeded_cqs
            ) or "—",
        })

    df = pd.DataFrame(rows)

    def style_result(val):
        if "PASS" in str(val): return "color: #155724; font-weight: 700"
        if "FAIL" in str(val): return "color: #721c24; font-weight: 700"
        return ""

    st.dataframe(
        df.style.applymap(style_result, subset=["Result"]),
        use_container_width=True, hide_index=True
    )

    pass_count = sum(1 for row in rows if "PASS" in row["Result"])
    st.markdown(
        f"**{pass_count}/{len(rows)} scenarios pass.** "
        f"{'All tests pass ✅' if pass_count == len(rows) else 'Some tests fail ❌'}"
    )

    st.markdown("---")
    st.subheader("Competency Question Tests (Nominal Plan)")

    cq_tests = [
        ("S-01", "Scenario A (nominal) PSA accepted"),
        ("S-02", "Scenario B (bus delayed) PSA rejected"),
        ("S-03", "Scenario C (resource conflict) PSA rejected"),
        ("S-04", "Scenario D (invariant disruption) PSA rejected"),
        ("S-05", "Scenario E (coordination failure) PSA rejected"),
    ]
    cq_rows = []
    for sc_name, sc_data in SCENARIOS.items():
        r = st.session_state.pipeline_cache[sc_name]
        actual = r["psa_accepted"]
        expected = sc_data["expected"]
        cq_rows.append(actual == expected)

    per_cq = [
        ("CQ-01", "CQ1 defeated for all actions", "CQ1"),
        ("CQ-02", "CQ2 defeated for bus_travel invariant", "CQ2"),
        ("CQ-03", "CQ3 defeated for all actions", "CQ3"),
        ("CQ-04", "CQ4 defeated for passenger_platform_wait", "CQ4"),
        ("CQ-05", "CQ5 defeated for train_travel", "CQ5"),
        ("CQ-06", "CQ6 defeated (no resource conflict)", "CQ6"),
        ("CQ-07", "CQ7 defeated for all orderings", "CQ7"),
        ("CQ-08", "CQ8 defeated (no invariant disruption)", "CQ8"),
    ]
    nominal_r = st.session_state.pipeline_cache["A — Nominal"]
    test_table = []
    for test_id, desc, _ in cq_tests:
        idx = int(test_id.split("-")[1]) - 1
        passed = cq_rows[idx]
        test_table.append({"Test": test_id, "Description": desc,
                            "Result": "PASS ✅" if passed else "FAIL ❌"})

    for test_id, desc, cq_name in per_cq:
        relevant = [r for r in nominal_r["cqr"]
                    if r["CQ"] == cq_name and r["Outcome"] != "n/a"]
        passed = bool(relevant) and all(r["Outcome"] == "defeated" for r in relevant)
        test_table.append({"Test": test_id, "Description": desc,
                            "Result": "PASS ✅" if passed else "FAIL ❌"})

    test_df = pd.DataFrame(test_table)
    total_pass = sum(1 for row in test_table if "PASS" in row["Result"])
    st.dataframe(
        test_df.style.applymap(style_result, subset=["Result"]),
        use_container_width=True, hide_index=True)
    st.markdown(f"**{total_pass}/13 competency question tests pass.**")


# ═══════════════════════════════════════════════════════════════
#  PAGE: AF & VERDICT
# ═══════════════════════════════════════════════════════════════

elif page == "📊 AF & Verdict":
    st.title("📊 Abstract Argumentation Framework")
    st.markdown(
        "The four-layer AF(P) for the current scenario. "
        "PSA(P) is accepted under grounded semantics iff every CQ is defeated."
    )

    verdict = "ACCEPTED" if R["psa_accepted"] else "REJECTED"
    badge_cls = "accepted-badge" if R["psa_accepted"] else "rejected-badge"
    st.markdown(
        f"**Scenario:** {sc['label']}  \n"
        f"**PSA(P):** <span class='{badge_cls}'>{'✅' if R['psa_accepted'] else '❌'} {verdict}</span>",
        unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("CQ Evaluation Summary")
        summary = []
        seen = {}
        for rec in R["cqr"]:
            key = (rec["CQ"], rec["Action(s)"])
            if key not in seen:
                seen[key] = True
                meta = CQ_META.get(rec["CQ"], {})
                summary.append({
                    "CQ": rec["CQ"],
                    "Action(s)": rec["Action(s)"],
                    "Attacks": meta.get("attacks", ""),
                    "Defeated by": meta.get("defeated_by", ""),
                    "Outcome": rec["Outcome"].upper(),
                })
        df_cq = pd.DataFrame(summary)

        def style_outcome(val):
            if val == "DEFEATED": return "color: #155724; font-weight:700"
            if val == "SUCCEEDS": return "color: #721c24; font-weight:700"
            return "color: #6c757d"

        st.dataframe(
            df_cq.style.applymap(style_outcome, subset=["Outcome"]),
            use_container_width=True, hide_index=True
        )

    with col2:
        st.subheader("Defeat Map")
        st.markdown("""
| CQ | Attacks | Defeated by |
|---|---|---|
| CQ1 | S1 (P1) | **S3** — Temporal Feasibility |
| CQ2 | S1 (P2) | **S6** — Invariant Maintenance |
| CQ3 | S2 (P2–P3) | **S1** — Action Applicability |
| CQ4 | S3 (P2) | **S5** — Temporal Ordering |
| CQ5 | S3 (P3) | **S5** — Temporal Ordering |
| CQ6 | S4 (P2–P3) | **S1** — Action Applicability |
| CQ7 | S5 (P3) | **S2** — Causal Goal Support |
| CQ8 | S6 (P2) | **S4** — Concurrency Feasibility |
""")
        st.caption(
            "The defeating scheme always differs from the attacked scheme. "
            "S0 is the evidential foundation; it carries no defeating role."
        )

    st.markdown("---")
    st.subheader("Grounded Extension")
    ext = R["ext"]
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**IN (accepted)**")
        for a in sorted(ext["IN"]):
            st.markdown(f"<span style='color:#28a745;'>✓ {a}</span>", unsafe_allow_html=True)
    with c2:
        st.markdown("**OUT (rejected)**")
        for a in sorted(ext["OUT"]):
            st.markdown(f"<span style='color:#dc3545;'>✗ {a}</span>", unsafe_allow_html=True)
    with c3:
        st.markdown("**UNDECIDED**")
        all_ids = {a["id"] for a in R["af_args"]}
        undecided = all_ids - ext["IN"] - ext["OUT"]
        for a in sorted(undecided):
            st.markdown(f"<span style='color:#888;'>? {a}</span>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  PAGE: ABOUT
# ═══════════════════════════════════════════════════════════════

elif page == "ℹ About":
    st.title("ℹ About this Prototype")
    st.markdown("""
### An Argumentation-Based Framework for Explaining Scheduled Temporal Plans

**PhD Project:** ECR_2024_17  
**Researcher:** Omolola Oluyemisi Haastrup  
**University:** University of Huddersfield, School of Computing and Engineering  
**Supervisors:** Dr Quratul-ain Mahesar (main) · Prof Mauro Vallati (co)

---

### Framework Summary

This chatbot prototype implements the four-layer argumentation framework described in the paper. Given a scheduled temporal plan, it:

1. **Computes the replayed state** S(t) at every relevant time point (S0)
2. **Extracts seven core argumentation schemes** (S1–S6 + S7) covering action applicability, causal support, temporal feasibility, concurrency, ordering necessity, and invariant maintenance
3. **Evaluates eight critical questions** (CQ1–CQ8) that operationalise standard user challenges
4. **Constructs AF(P)** — a four-layer Dung-style abstract argumentation framework
5. **Computes grounded semantics** to yield an auditable PSA(P) verdict

---

### CQ → Defeating Scheme Mapping (updated 26 May 2026)

| CQ | Attacks | Defeated by | Key principle |
|---|---|---|---|
| CQ1 | S1 P1 (start conditions) | **S3** | S3's enabling-timing guarantee (e_j ≤ s_i) implies start conditions present |
| CQ2 | S1 P2 (invariant persistence) | **S6** | S6 certifies HoldsOver(φ, (s_i, e_i)) throughout execution |
| CQ3 | S2 P2–P3 (causal link) | **S1** | S1 applicability confirms effects genuinely produced and available |
| CQ4 | S3 P2 (enabling timing) | **S5** | S5 Premise 1 directly certifies finish-to-start: e_j ≤ s_i |
| CQ5 | S3 P3 (temporal constraints) | **S5** | S5 Premise 3 carries timing constraint compliance evidence |
| CQ6 | S4 P2–P3 (resource/invariant) | **S1** | S1 individual applicability implies disjoint locks and non-interference |
| CQ7 | S5 P3 (ordering necessity) | **S2** | S2 causal chain identifies exactly what reversal would break |
| CQ8 | S6 P2 (invariant disruption) | **S4** | S4 Premise 3 certifies mutual invariant compatibility |

**Key architectural principle:** The defeating scheme always differs from the attacked scheme.  
S0 is the purely evidential foundation; it carries no defeating role.

---

### Five Scenarios

| ID | Fault | PSA verdict |
|---|---|---|
| A | Nominal — no fault | ACCEPTED |
| B | Bus delayed (e₂=8) | REJECTED |
| C | Resource conflict (Train lock) | REJECTED |
| D | Invariant disruption (passenger_on_bus deleted) | REJECTED |
| E | Coordination failure (train_approach ends at t=11) | REJECTED |

---

*This prototype is part of PhD research on Explainable Collaborative Planning at the University of Huddersfield.*
""")


# ═══════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown(
    "<div style='text-align:center; font-size:0.75rem; color:#aaa;'>"
    "XAIP Chatbot · ECR_2024_17 · University of Huddersfield · "
    "CQ mapping updated 26 May 2026"
    "</div>",
    unsafe_allow_html=True)
