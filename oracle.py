import json, math

def pos(x): return isinstance(x,(int,float)) and math.isfinite(x) and x>0
def jround(x): return math.floor(x+0.5)
def jsnum(x):
    if isinstance(x,float) and x==int(x): return str(int(x))
    return str(x)
def r1(x): return jround(x*10)/10

DIAM={"1.25":0.55,"2.5":0.8,"4":0.95}

def hose_plan(rated,hoseIn,hoseFt):
    if not pos(rated): return {"error":"the sticker CFM must be above zero"}
    if hoseIn not in DIAM: return {"error":"pick a hose diameter"}
    if not pos(hoseFt): return {"error":"the hose length must be above zero"}
    mult=max(0.4,1-0.015*max(0,hoseFt-7))
    return {"eff":r1(rated*DIAM[hoseIn]*mult)}

def render_hose(r,rated,hoseIn,hoseFt):
    return ("Your "+jsnum(rated)+" CFM vac through "+jsnum(hoseFt)+" ft of "+hoseIn
            +" in hose figures about "+jsnum(r["eff"])+" CFM at the tool - the sticker was measured with no hose at all.")

def filter_plan(cfm,state,hepa):
    if not pos(cfm): return {"error":"the CFM must be above zero"}
    if state not in ("clean","loaded"): return {"error":"pick clean or loaded"}
    f=1.0
    if state=="loaded": f*=0.75
    if hepa: f*=0.85
    return {"eff":r1(cfm*f)}

def render_filter(r,cfm,state,hepa):
    if state=="clean" and not hepa:
        return ("Your "+jsnum(cfm)+" CFM stays about "+jsnum(r["eff"])
                +" with a clean filter - it only stays innocent if you wash it.")
    parts=[]
    if state=="loaded": parts.append("A loaded filter")
    if hepa: parts.append("the HEPA cartridge")
    verb=" take " if len(parts)>1 else " takes "
    who=" and ".join(parts); who=who[0].upper()+who[1:]
    return (who+verb+"your "+jsnum(cfm)+" CFM down to about "+jsnum(r["eff"])
            +" - suction dies at the filter, not the motor.")

def circuit_plan(vac,tool,circ):
    if not pos(vac) or not pos(tool) or not pos(circ):
        return {"error":"amps must all be above zero"}
    load=vac+tool; limit=0.8*circ
    return {"load":r1(load),"limit":r1(limit),"over":load>limit}

def render_circuit(r,vac,tool,circ):
    s=("Your vac ("+jsnum(vac)+" A) and tool ("+jsnum(tool)+" A) pull "+jsnum(r["load"])
       +" A on a "+jsnum(circ)+" A circuit - ")
    if r["over"]:
        return s+"past the "+jsnum(r["limit"])+" A continuous line, so the breaker votes no; run one motor at a time."
    return s+"inside the "+jsnum(r["limit"])+" A continuous line, so the breaker stays out of it."

cases=[]
def add(tool,args):
    if tool=="hose": r=hose_plan(*args); fn=render_hose
    elif tool=="filter": r=filter_plan(*args); fn=render_filter
    else: r=circuit_plan(*args); fn=render_circuit
    case={"tool":tool,"args":args,"result":r}
    if "error" not in r: case["render"]=fn(r,*args)
    cases.append(case)

for a in [(150,"2.5",12),(150,"1.25",7),(200,"4",10),(90,"2.5",25),(150,"2.5",7),(120,"1.25",15),(175,"4",30),(100,"2.5",50)]:
    add("hose",a)
for a in [(111,"loaded",False),(111,"clean",True),(111,"loaded",True),(150,"clean",False),(94,"loaded",False),(80,"clean",True),(120,"loaded",True)]:
    add("filter",a)
for a in [(11,13,15),(9,6,20),(12,10,15),(8,7,20),(10,10,20),(14,6,15),(7,4,15)]:
    add("circuit",a)
add("hose",[0,"2.5",12]); add("hose",[150,"3",12]); add("filter",[0,"clean",False]); add("filter",[100,"dirty",False]); add("circuit",[0,13,15])

json.dump(cases,open("expected.json","w"),separators=(",",":"))
print(len(cases),"cases")
