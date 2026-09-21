if(typeof window!=='undefined'){
(() => {
'use strict';
const V134_VERSION='13.4A';
const V134_STREET_EVENTS=[{"id":"v134e_ash_toll","districts":["ash_blocks"],"title":"RED JACK TOLL","text":"A half-dozen colors step from a tenement arch and stretch a chain across the lane. Their lieutenant recognizes the crew before he recognizes the vehicle tags.","category":"threat","choices":[{"label":"Pay the street tax · ¢180","effects":[{"type":"credits","delta":-180},{"type":"localHeat","delta":-2},{"type":"time","minutes":6}],"requires":{"credits":180}},{"label":"[CYBER SWORD / GUNSLINGER] Make them reconsider","effects":[{"type":"gangPressure","delta":-4},{"type":"notoriety","delta":2},{"type":"rep","faction":"iron","delta":2}],"requires":{"classes":["Cyber Sword","Gunslinger"]}},{"label":"Back into the alleys","effects":[{"type":"time","minutes":12},{"type":"unrest","delta":1}]}],"weight":1.25},{"id":"v134e_ash_fire","districts":["ash_blocks"],"title":"SCRAPYARD FIRE","text":"A battery stack cooks off behind a corrugated wall. Scavengers are trying to drag a trapped mechanic clear while everyone else strips the yard.","category":"opportunity","choices":[{"label":"Help pull the mechanic out","effects":[{"type":"trustAny","delta":2},{"type":"unrest","delta":-2},{"type":"time","minutes":8}]},{"label":"Strip the abandoned crates","effects":[{"type":"salvage","delta":3},{"type":"notoriety","delta":1},{"type":"gangPressure","delta":1}]},{"label":"[HACKER] Kill the battery cascade","effects":[{"type":"salvage","delta":2},{"type":"security","delta":1},{"type":"localHeat","delta":-2}],"requires":{"classes":["Hacker"]}}],"weight":1.05},{"id":"v134e_ash_runner","districts":["ash_blocks"],"title":"BLEEDING RUNNER","text":"A teenage courier collapses between two shuttered storefronts with a data capsule taped under his ribs. Someone is already searching the block.","category":"opportunity","choices":[{"label":"Get him to a clinic","effects":[{"type":"time","minutes":14},{"type":"rumor"},{"type":"trustAny","delta":3}]},{"label":"Take the capsule","effects":[{"type":"credits","delta":320},{"type":"localHeat","delta":5},{"type":"unrest","delta":2}]},{"label":"[AGENTEX] Hide him and spoof the searchers","effects":[{"type":"rumor"},{"type":"hiddenRoute"},{"type":"location"},{"type":"localHeat","delta":-3}],"requires":{"classes":["AgentEX"]}}],"weight":0.95},{"id":"v134e_ash_recruiter","districts":["ash_blocks"],"title":"STREET RECRUITER","text":"A Red Jack talent scout watches the crew cross the courtyard. She offers a name, a cheap pistol and an address for someone who wants real work.","category":"ambient","choices":[{"label":"Hear the pitch","effects":[{"type":"contract"},{"type":"rep","faction":"iron","delta":1}]},{"label":"Trade names instead","effects":[{"type":"rumor"},{"type":"trustAny","delta":1}]},{"label":"Keep walking","effects":[]}],"weight":0.85},{"id":"v134e_flood_rise","districts":["floodline"],"title":"FLASH RISE","text":"Warning horns echo over Lowwater as a pump relay fails. Water is already climbing over the lower causeway.","category":"threat","choices":[{"label":"Take the high detour","effects":[{"type":"time","minutes":16},{"type":"localHeat","delta":-1}]},{"label":"[HACKER] Restart the relay","effects":[{"type":"prosperity","delta":2},{"type":"security","delta":1},{"type":"trustAny","delta":2}],"requires":{"classes":["Hacker"]}},{"label":"Push through before it closes","effects":[{"type":"time","minutes":3},{"type":"injuryRisk","chance":0.22},{"type":"notoriety","delta":1}]}],"weight":1.1},{"id":"v134e_flood_market","districts":["floodline"],"title":"FLOATING MARKET","text":"A line of chained pontoons has become a night market: medicine, stolen filters, knockoff optics and fresh fish under violet tarps.","category":"opportunity","choices":[{"label":"Buy field supplies · ¢220","effects":[{"type":"credits","delta":-220},{"type":"heal","amount":12}],"requires":{"credits":220}},{"label":"Work the sellers for information","effects":[{"type":"rumor"},{"type":"time","minutes":7}]},{"label":"[AGENTEX] Find the real broker","effects":[{"type":"hiddenRoute"},{"type":"trustAny","delta":2}],"requires":{"classes":["AgentEX"]}}],"weight":0.9,"night":true},{"id":"v134e_flood_courier","districts":["floodline"],"title":"DROWNED COURIER","text":"A courier bike is wedged against a flood barrier. The rider is gone. The armored dispatch case is not.","category":"opportunity","choices":[{"label":"[HACKER] Crack the case quietly","effects":[{"type":"credits","delta":420},{"type":"rumor"}],"requires":{"classes":["Hacker"]}},{"label":"Force it open","effects":[{"type":"credits","delta":280},{"type":"localHeat","delta":4},{"type":"notoriety","delta":1}]},{"label":"Mark it for the local fixer","effects":[{"type":"trustAny","delta":4},{"type":"rep","faction":"spine","delta":2}]}],"weight":0.9},{"id":"v134e_flood_pump","districts":["floodline"],"title":"PUMP WARD EXTORTION","text":"A protection crew has locked the neighborhood pumps behind a payment terminal. Residents are queuing with credsticks and murder in their eyes.","category":"threat","choices":[{"label":"Pay the ward's arrears · ¢350","effects":[{"type":"credits","delta":-350},{"type":"unrest","delta":-5},{"type":"prosperity","delta":2}],"requires":{"credits":350}},{"label":"[HACKER] Zero the payment ledger","effects":[{"type":"unrest","delta":-4},{"type":"localHeat","delta":5},{"type":"rep","faction":"wraiths","delta":2}],"requires":{"classes":["Hacker"]}},{"label":"Tell the protection crew to leave","effects":[{"type":"gangPressure","delta":-5},{"type":"notoriety","delta":3}],"requires":{"classes":["Cyber Sword","Gunslinger","AgentEX"]}}],"weight":1.0},{"id":"v134e_market_whisper","districts":["old_market"],"title":"BROKER WHISPER","text":"A tea seller pours a second cup without asking. Under the saucer is a handwritten time, a room number and the name of someone who should not be in Chrome City.","category":"opportunity","choices":[{"label":"Buy the story · ¢120","effects":[{"type":"credits","delta":-120},{"type":"rumor"}],"requires":{"credits":120}},{"label":"Offer a better story","effects":[{"type":"trustAny","delta":2},{"type":"rep","faction":"spine","delta":1}]},{"label":"Leave the saucer untouched","effects":[]}],"weight":1.1},{"id":"v134e_market_pickpocket","districts":["old_market"],"title":"PICKPOCKET RING","text":"Three children move through the crowd in a practiced pattern. One distracts. One lifts. The third watches who notices.","category":"threat","choices":[{"label":"Let ¢90 disappear","effects":[{"type":"credits","delta":-90},{"type":"localHeat","delta":-1}],"requires":{"credits":90}},{"label":"[AGENTEX] Catch the watcher, not the hand","effects":[{"type":"rumor"},{"type":"gangPressure","delta":-2}],"requires":{"classes":["AgentEX"]}},{"label":"[GUNSLINGER] Pin the thief's sleeve to the stall","effects":[{"type":"notoriety","delta":1},{"type":"unrest","delta":1},{"type":"credits","delta":70}],"requires":{"classes":["Gunslinger"]}}],"weight":0.95},{"id":"v134e_market_auction","districts":["old_market"],"title":"BACK-ROOM AUCTION","text":"A shutter rolls up for exactly twelve minutes. Inside, mercs bid on confiscated corporate hardware by serial number.","category":"opportunity","choices":[{"label":"Bid on parts · ¢400","effects":[{"type":"credits","delta":-400},{"type":"salvage","delta":5}],"requires":{"credits":400}},{"label":"[HACKER] Trace the auction manifest","effects":[{"type":"rumor"},{"type":"contract"}],"requires":{"classes":["Hacker"]}},{"label":"Watch who buys","effects":[{"type":"rumor"},{"type":"time","minutes":10}]}],"weight":0.9,"night":true},{"id":"v134e_market_dead_drop","districts":["old_market"],"title":"UNCLAIMED DEAD DROP","text":"A maintenance locker flashes the old two-pulse Spine code. The pickup window expired an hour ago.","category":"opportunity","choices":[{"label":"Take the package","effects":[{"type":"contract"},{"type":"localHeat","delta":3}]},{"label":"Call the broker channel","effects":[{"type":"trustAny","delta":2},{"type":"rumor"}]},{"label":"Walk away","effects":[]}],"weight":0.9},{"id":"v134e_neon_door","districts":["neon_row"],"title":"VELVET DOOR","text":"The club's face-recognition arch turns amber on your crew. The bouncer smiles professionally and places one hand on a concealed shock baton.","category":"threat","choices":[{"label":"Buy discretion · ¢260","effects":[{"type":"credits","delta":-260},{"type":"localHeat","delta":-4}],"requires":{"credits":260}},{"label":"[AGENTEX] Make the guest list agree","effects":[{"type":"localHeat","delta":-5},{"type":"rumor"}],"requires":{"classes":["AgentEX"]}},{"label":"Make a scene","effects":[{"type":"notoriety","delta":4},{"type":"unrest","delta":2},{"type":"rep","faction":"chrome","delta":1}]}],"weight":1.05,"night":true},{"id":"v134e_neon_collapse","districts":["neon_row"],"title":"CHROME COLLAPSE","text":"A club kid seizes beside a noodle counter, neural ports strobing fault-red. The clinic across the street wants payment before opening the door.","category":"ambient","choices":[{"label":"Cover the clinic · ¢180","effects":[{"type":"credits","delta":-180},{"type":"trustAny","delta":2},{"type":"prosperity","delta":1}],"requires":{"credits":180}},{"label":"[HACKER] Isolate the feedback loop","effects":[{"type":"trustAny","delta":3},{"type":"rumor"}],"requires":{"classes":["Hacker"]}},{"label":"Keep moving","effects":[]}],"weight":0.8,"night":true},{"id":"v134e_neon_fence","districts":["neon_row"],"title":"MAKO FENCE","text":"A Mako runner opens a flight case full of immaculate serial-scrubbed weapon parts. He says you have six minutes before the owner notices.","category":"opportunity","choices":[{"label":"Buy the case · ¢520","effects":[{"type":"credits","delta":-520},{"type":"salvage","delta":7},{"type":"localHeat","delta":2}],"requires":{"credits":520}},{"label":"Trade the location of a patrol","effects":[{"type":"rep","faction":"chrome","delta":3},{"type":"rumor"}]},{"label":"Set him up","effects":[{"type":"security","delta":1},{"type":"gangPressure","delta":2},{"type":"notoriety","delta":-1}]}],"weight":0.9},{"id":"v134e_neon_scan","districts":["neon_row"],"title":"AD-SCAN SWARM","text":"A cloud of promotional drones pivots in perfect unison and begins matching faces against a private bounty feed.","category":"threat","choices":[{"label":"[HACKER] Poison the feed","effects":[{"type":"notoriety","delta":-3},{"type":"localHeat","delta":-3}],"requires":{"classes":["Hacker"]}},{"label":"Duck through service alleys","effects":[{"type":"time","minutes":9},{"type":"localHeat","delta":-1}]},{"label":"Shoot one down","effects":[{"type":"salvage","delta":1},{"type":"notoriety","delta":3}],"requires":{"classes":["Gunslinger","Sniper"]}}],"weight":1.0},{"id":"v134e_rail_union","districts":["rail_crown"],"title":"UNION LINE","text":"Workers have chained two freight doors shut. A foreman recognizes the crew and asks which side of the lockout you are on.","category":"ambient","choices":[{"label":"Back the workers","effects":[{"type":"rep","faction":"iron","delta":3},{"type":"prosperity","delta":1},{"type":"security","delta":-1}]},{"label":"Take the contractor's money · ¢300","effects":[{"type":"credits","delta":300},{"type":"unrest","delta":3},{"type":"localHeat","delta":2}]},{"label":"Stay out of it","effects":[]}],"weight":0.9},{"id":"v134e_rail_theft","districts":["rail_crown"],"title":"MOVING FREIGHT","text":"A container seal pops as a train crawls through Platform Ward. Someone planned this theft down to the second. They did not plan for you.","category":"opportunity","choices":[{"label":"Lift a crate","effects":[{"type":"salvage","delta":4},{"type":"notoriety","delta":2}]},{"label":"[AGENTEX] Follow the thieves instead","effects":[{"type":"contract"},{"type":"rumor"}],"requires":{"classes":["AgentEX"]}},{"label":"Call it in","effects":[{"type":"security","delta":2},{"type":"rep","faction":"meridian","delta":2}]}],"weight":0.95},{"id":"v134e_rail_inspector","districts":["rail_crown"],"title":"TRANSIT INSPECTOR","text":"A rail-security team sweeps the platform, checking weapons licenses and cargo declarations.","category":"threat","choices":[{"label":"Pay the administrative fee · ¢210","effects":[{"type":"credits","delta":-210},{"type":"localHeat","delta":-2}],"requires":{"credits":210}},{"label":"[AGENTEX] Produce the right forms","effects":[{"type":"localHeat","delta":-4}],"requires":{"classes":["AgentEX"]}},{"label":"Leave by the maintenance catwalk","effects":[{"type":"time","minutes":11},{"type":"hiddenRoute"}]}],"weight":1.0},{"id":"v134e_rail_convoy","districts":["rail_crown"],"title":"STRANDED CONVOY","text":"An armored freight crawler has thrown a drive assembly across the crossing. Its escort is arguing with a mechanic and blocking half the ward.","category":"opportunity","choices":[{"label":"Help repair it","effects":[{"type":"credits","delta":180},{"type":"rep","faction":"iron","delta":1},{"type":"time","minutes":10}]},{"label":"[HACKER] Pull the manifest first","effects":[{"type":"rumor"},{"type":"contract"}],"requires":{"classes":["Hacker"]}},{"label":"Use the traffic jam to disappear","effects":[{"type":"notoriety","delta":-2},{"type":"time","minutes":6}]}],"weight":0.8},{"id":"v134e_dock_customs","districts":["dock_nine"],"title":"CUSTOMS SWEEP","text":"Customs drones descend between container stacks while armed inspectors seal both ends of the lane.","category":"threat","choices":[{"label":"Submit to inspection","effects":[{"type":"time","minutes":8},{"type":"localHeat","delta":2}]},{"label":"[HACKER] Reassign your container tag","effects":[{"type":"localHeat","delta":-4},{"type":"notoriety","delta":-1}],"requires":{"classes":["Hacker"]}},{"label":"Cut through the stacks","effects":[{"type":"time","minutes":10},{"type":"salvage","delta":1}]}],"weight":1.1},{"id":"v134e_dock_cache","districts":["dock_nine"],"title":"MISROUTED CONTAINER","text":"A container door is open three centimeters. Inside: military ration packs, drone actuators and a manifest for a ship that does not exist.","category":"opportunity","choices":[{"label":"Take the actuators","effects":[{"type":"salvage","delta":5},{"type":"localHeat","delta":3}]},{"label":"Sell the manifest · ¢340","effects":[{"type":"credits","delta":340},{"type":"rep","faction":"spine","delta":1}]},{"label":"[AGENTEX] Put a tracker on it","effects":[{"type":"contract"},{"type":"rumor"}],"requires":{"classes":["AgentEX"]}}],"weight":0.95},{"id":"v134e_dock_smuggler","districts":["dock_nine"],"title":"SMUGGLER'S WINDOW","text":"A tug captain gives you a frequency and says the harbor cameras will be blind for exactly ninety seconds.","category":"opportunity","choices":[{"label":"Use it to move clean","effects":[{"type":"notoriety","delta":-3},{"type":"localHeat","delta":-4}]},{"label":"Sell the window","effects":[{"type":"credits","delta":260},{"type":"unrest","delta":1}]},{"label":"Ask where the blind spot leads","effects":[{"type":"hiddenRoute"}]}],"weight":0.85},{"id":"v134e_dock_brawl","districts":["dock_nine"],"title":"DOCKSIDE BRAWL","text":"Two crews spill out of a bonded warehouse, fists first and weapons coming out second.","category":"threat","choices":[{"label":"Circle around","effects":[{"type":"time","minutes":9}]},{"label":"[CYBER SWORD] End it before guns clear holsters","effects":[{"type":"unrest","delta":-2},{"type":"notoriety","delta":2},{"type":"trustAny","delta":1}],"requires":{"classes":["Cyber Sword"]}},{"label":"Bet on the smaller crew · ¢100","effects":[{"type":"credits","delta":160},{"type":"unrest","delta":1}],"requires":{"credits":100}}],"weight":0.9},{"id":"v134e_forge_accident","districts":["forge_belt"],"title":"LINE ACCIDENT","text":"A press line locks with two workers inside its safety cage. Management has not stopped production.","category":"ambient","choices":[{"label":"Force the line down","effects":[{"type":"prosperity","delta":-1},{"type":"unrest","delta":-2},{"type":"rep","faction":"iron","delta":2}]},{"label":"[HACKER] Trip the safety controller","effects":[{"type":"unrest","delta":-3},{"type":"trustAny","delta":2}],"requires":{"classes":["Hacker"]}},{"label":"Take the service bounty · ¢240","effects":[{"type":"credits","delta":240},{"type":"unrest","delta":2}]}],"weight":0.95},{"id":"v134e_forge_union","districts":["forge_belt"],"title":"SHIFT VOTE","text":"A union organizer mistakes the crew for hired intimidation. Then she realizes who you are and asks for protection instead.","category":"opportunity","choices":[{"label":"Stand with the vote","effects":[{"type":"rep","faction":"iron","delta":4},{"type":"contract"}]},{"label":"Sell neutrality · ¢280","effects":[{"type":"credits","delta":280},{"type":"trustAny","delta":-1}]},{"label":"Decline","effects":[]}],"weight":0.85},{"id":"v134e_forge_parts","districts":["forge_belt"],"title":"HOT MACHINE PARTS","text":"A maintenance pallet holds actuator assemblies with the serials burned off. The forklift operator pretends not to see you.","category":"opportunity","choices":[{"label":"Buy the pallet · ¢360","effects":[{"type":"credits","delta":-360},{"type":"salvage","delta":6}],"requires":{"credits":360}},{"label":"Take one and leave","effects":[{"type":"salvage","delta":2},{"type":"localHeat","delta":2}]},{"label":"[AGENTEX] Find who ordered the serial scrub","effects":[{"type":"rumor"},{"type":"contract"}],"requires":{"classes":["AgentEX"]}}],"weight":0.9},{"id":"v134e_forge_foreman","districts":["forge_belt"],"title":"ATLAS FOREMAN","text":"An Atlas foreman offers cash for a quiet five-minute conversation about a production line that officially does not exist.","category":"opportunity","choices":[{"label":"Listen","effects":[{"type":"credits","delta":150},{"type":"rumor"}]},{"label":"Sell the lead to Iron","effects":[{"type":"rep","faction":"iron","delta":3},{"type":"localHeat","delta":3}]},{"label":"Ask for the address, not the story","effects":[{"type":"contract"}]}],"weight":0.85},{"id":"v134e_under_signal","districts":["undergrid"],"title":"GHOST SIGNAL","text":"Your comms fill with a narrow-band handshake that only exists for three seconds at a time. It is moving through the utility mesh with you.","category":"opportunity","choices":[{"label":"[HACKER] Follow the handshake","effects":[{"type":"hiddenRoute"},{"type":"rumor"}],"requires":{"classes":["Hacker"]}},{"label":"Record it for later","effects":[{"type":"rumor"}]},{"label":"Kill wireless and move dark","effects":[{"type":"localHeat","delta":-2},{"type":"time","minutes":5}]}],"weight":1.15},{"id":"v134e_under_drone","districts":["undergrid"],"title":"MAINTENANCE DRONE","text":"A municipal repair drone blocks the tunnel, repeatedly asking for a work order from a department abolished twelve years ago.","category":"ambient","choices":[{"label":"[HACKER] Rewrite its task queue","effects":[{"type":"salvage","delta":2},{"type":"security","delta":1}],"requires":{"classes":["Hacker"]}},{"label":"Push it into an alcove","effects":[{"type":"time","minutes":3}]},{"label":"Follow it","effects":[{"type":"interactable"},{"type":"hiddenRoute"}]}],"weight":0.85},{"id":"v134e_under_leak","districts":["undergrid"],"title":"DATA LEAK","text":"Condensation drips through a cracked conduit onto an exposed municipal fiber trunk. Half a district's unsecured telemetry is spilling into the tunnel.","category":"opportunity","choices":[{"label":"[HACKER] Harvest the leak","effects":[{"type":"credits","delta":260},{"type":"rumor"},{"type":"localHeat","delta":2}],"requires":{"classes":["Hacker"]}},{"label":"Sell the coordinates","effects":[{"type":"credits","delta":180},{"type":"rep","faction":"wraiths","delta":2}]},{"label":"Patch it","effects":[{"type":"security","delta":1},{"type":"trustAny","delta":2}]}],"weight":0.95},{"id":"v134e_under_ambush","districts":["undergrid"],"title":"LIGHTS OUT","text":"Every service light ahead dies at once. Footsteps stop behind you. Someone planned the darkness.","category":"threat","choices":[{"label":"[AGENTEX] Reverse the ambush","effects":[{"type":"localHeat","delta":-2},{"type":"credits","delta":160}],"requires":{"classes":["AgentEX"]}},{"label":"[CYBER SWORD] Walk straight through","effects":[{"type":"notoriety","delta":2},{"type":"gangPressure","delta":-3}],"requires":{"classes":["Cyber Sword"]}},{"label":"Retreat to the last junction","effects":[{"type":"time","minutes":10}]}],"weight":1.05},{"id":"v134e_civic_scan","districts":["civic_circuit"],"title":"CIVIC ID SWEEP","text":"Police barricades fold across the boulevard as drones begin random biometric checks.","category":"threat","choices":[{"label":"Wait your turn","effects":[{"type":"time","minutes":8},{"type":"localHeat","delta":2}]},{"label":"[AGENTEX] Pass as municipal contractors","effects":[{"type":"localHeat","delta":-3}],"requires":{"classes":["AgentEX"]}},{"label":"[HACKER] Desync the scanner queue","effects":[{"type":"notoriety","delta":-2},{"type":"security","delta":-1}],"requires":{"classes":["Hacker"]}}],"weight":1.15},{"id":"v134e_civic_trauma","districts":["civic_circuit"],"title":"TRAUMA OVERFLOW","text":"An emergency ward has patients on the sidewalk. A nurse recognizes your gear and asks if you have med supplies to spare.","category":"ambient","choices":[{"label":"Donate supplies · ¢200","effects":[{"type":"credits","delta":-200},{"type":"prosperity","delta":2},{"type":"trustAny","delta":2}],"requires":{"credits":200}},{"label":"Offer muscle for crowd control","effects":[{"type":"credits","delta":120},{"type":"unrest","delta":-2}],"requires":{"classes":["Cyber Sword","Gunslinger"]}},{"label":"Move on","effects":[]}],"weight":0.85},{"id":"v134e_civic_courier","districts":["civic_circuit"],"title":"SEALED COURT FILE","text":"A court courier drops an encrypted evidence capsule during a collision with a delivery drone.","category":"opportunity","choices":[{"label":"Return it","effects":[{"type":"security","delta":1},{"type":"rep","faction":"meridian","delta":1}]},{"label":"[HACKER] Copy it before returning","effects":[{"type":"rumor"},{"type":"contract"},{"type":"localHeat","delta":2}],"requires":{"classes":["Hacker"]}},{"label":"Sell it to a broker","effects":[{"type":"credits","delta":300},{"type":"rep","faction":"spine","delta":2}]}],"weight":0.9},{"id":"v134e_civic_protest","districts":["civic_circuit"],"title":"CIVIC PROTEST","text":"A labor march and a security cordon collide at the same intersection. Cameras are already broadcasting.","category":"ambient","choices":[{"label":"Help keep a lane open","effects":[{"type":"unrest","delta":-2},{"type":"time","minutes":6}]},{"label":"Stand with the march","effects":[{"type":"rep","faction":"iron","delta":2},{"type":"notoriety","delta":1}]},{"label":"Use the crowd as cover","effects":[{"type":"localHeat","delta":-3}]}],"weight":0.9},{"id":"v134e_glass_security","districts":["glass_heights"],"title":"PRIVATE SECURITY","text":"A quiet electric patrol car matches your walking speed. No sirens. No threats. Just a polite request to explain why you are here.","category":"threat","choices":[{"label":"Show a clean itinerary · ¢300","effects":[{"type":"credits","delta":-300},{"type":"localHeat","delta":-4}],"requires":{"credits":300}},{"label":"[AGENTEX] Become somebody expected","effects":[{"type":"localHeat","delta":-5},{"type":"rep","faction":"meridian","delta":1}],"requires":{"classes":["AgentEX"]}},{"label":"Refuse the conversation","effects":[{"type":"notoriety","delta":3},{"type":"security","delta":1}]}],"weight":1.15},{"id":"v134e_glass_crash","districts":["glass_heights"],"title":"EXECUTIVE CRASH","text":"An autonomous limousine clips a garden barrier and locks itself down. The passenger is alive, furious and very important.","category":"opportunity","choices":[{"label":"Open the vehicle","effects":[{"type":"credits","delta":260},{"type":"trustAny","delta":2}]},{"label":"[HACKER] Read the vehicle log first","effects":[{"type":"rumor"},{"type":"contract"}],"requires":{"classes":["Hacker"]}},{"label":"Leave before security arrives","effects":[{"type":"localHeat","delta":-1}]}],"weight":0.85},{"id":"v134e_glass_valet","districts":["glass_heights"],"title":"VALET LEAK","text":"A valet recognizes a corporate target from one of your old jobs and casually mentions where their car goes every Thursday.","category":"opportunity","choices":[{"label":"Tip him · ¢100","effects":[{"type":"credits","delta":-100},{"type":"rumor"}],"requires":{"credits":100}},{"label":"Offer future work","effects":[{"type":"contract"},{"type":"trustAny","delta":1}]},{"label":"Forget you heard it","effects":[]}],"weight":0.8},{"id":"v134e_glass_invite","districts":["glass_heights"],"title":"PRIVATE INVITATION","text":"A concierge delivers a physical envelope embossed with a logo that does not appear in any registry.","category":"opportunity","choices":[{"label":"Accept the invitation","effects":[{"type":"contract"},{"type":"localHeat","delta":1}]},{"label":"[AGENTEX] Verify the host first","effects":[{"type":"rumor"},{"type":"localHeat","delta":-1}],"requires":{"classes":["AgentEX"]}},{"label":"Sell the invitation · ¢250","effects":[{"type":"credits","delta":250},{"type":"rep","faction":"spine","delta":1}]}],"weight":0.75,"night":true},{"id":"v134e_helix_courier","districts":["helix_financial"],"title":"FINANCIAL COURIER","text":"A bonded courier pauses at the curb while two security drones argue over conflicting route authorizations.","category":"opportunity","choices":[{"label":"[HACKER] Create a third authorization","effects":[{"type":"credits","delta":380},{"type":"rumor"},{"type":"localHeat","delta":3}],"requires":{"classes":["Hacker"]}},{"label":"Alert security","effects":[{"type":"rep","faction":"meridian","delta":2},{"type":"security","delta":1}]},{"label":"Follow the courier","effects":[{"type":"contract"},{"type":"time","minutes":10}]}],"weight":0.95},{"id":"v134e_helix_bio","districts":["helix_financial"],"title":"BIOMETRIC PLAZA","text":"The plaza gates silently increase their sampling resolution as the crew enters the sensor field.","category":"threat","choices":[{"label":"[AGENTEX] Spoof pedestrian credentials","effects":[{"type":"localHeat","delta":-4}],"requires":{"classes":["AgentEX"]}},{"label":"[HACKER] Loop the last clean scan","effects":[{"type":"notoriety","delta":-2},{"type":"localHeat","delta":-2}],"requires":{"classes":["Hacker"]}},{"label":"Turn around","effects":[{"type":"time","minutes":8}]}],"weight":1.05},{"id":"v134e_helix_insider","districts":["helix_financial"],"title":"INSIDER CALL","text":"A disposable handset rings from beneath a bench. The caller knows your current street and wants to sell a trading-desk access schedule.","category":"opportunity","choices":[{"label":"Buy it · ¢280","effects":[{"type":"credits","delta":-280},{"type":"contract"},{"type":"rumor"}],"requires":{"credits":280}},{"label":"Demand proof","effects":[{"type":"rumor"},{"type":"time","minutes":5}]},{"label":"Trace the caller","effects":[{"type":"localHeat","delta":2},{"type":"hiddenRoute"}],"requires":{"classes":["Hacker","AgentEX"]}}],"weight":0.9},{"id":"v134e_helix_kiosk","districts":["helix_financial"],"title":"PUBLIC DATA KIOSK","text":"A civic-finance kiosk briefly displays a maintenance console before returning to sanitized market news.","category":"opportunity","choices":[{"label":"[HACKER] Reopen maintenance mode","effects":[{"type":"rumor"},{"type":"credits","delta":120}],"requires":{"classes":["Hacker"]}},{"label":"Report the fault","effects":[{"type":"rep","faction":"meridian","delta":1}]},{"label":"Ignore it","effects":[]}],"weight":0.75},{"id":"v134e_meridian_gate","districts":["meridian_arcology"],"title":"CONTRACTOR AUDIT","text":"Meridian security is performing random contractor audits. Your route passes directly through the temporary inspection zone.","category":"threat","choices":[{"label":"Buy a contractor packet · ¢420","effects":[{"type":"credits","delta":-420},{"type":"localHeat","delta":-4}],"requires":{"credits":420}},{"label":"[AGENTEX] Become the auditors","effects":[{"type":"localHeat","delta":-6},{"type":"rumor"}],"requires":{"classes":["AgentEX"]}},{"label":"[HACKER] Corrupt the audit queue","effects":[{"type":"notoriety","delta":2},{"type":"security","delta":-1}],"requires":{"classes":["Hacker"]}}],"weight":1.2},{"id":"v134e_meridian_proto","districts":["meridian_arcology"],"title":"PROTOTYPE TRANSFER","text":"A sealed technical cart moves between two arcology wings under unusually light escort.","category":"opportunity","choices":[{"label":"Shadow it","effects":[{"type":"contract"},{"type":"rumor"},{"type":"time","minutes":8}]},{"label":"[HACKER] Poll its telemetry","effects":[{"type":"rumor"},{"type":"salvage","delta":2}],"requires":{"classes":["Hacker"]}},{"label":"Flag it to a rival buyer","effects":[{"type":"credits","delta":320},{"type":"rep","faction":"spine","delta":2}]}],"weight":0.9},{"id":"v134e_meridian_defector","districts":["meridian_arcology"],"title":"EMPLOYEE DEFECTION","text":"A terrified systems engineer whispers your fixer code as she passes. Her access badge is still active. Her exit plan is not.","category":"opportunity","choices":[{"label":"Take the extraction job","effects":[{"type":"contract"},{"type":"trustAny","delta":2}]},{"label":"[AGENTEX] Walk her through security now","effects":[{"type":"credits","delta":350},{"type":"notoriety","delta":3},{"type":"localHeat","delta":5}],"requires":{"classes":["AgentEX"]}},{"label":"Sell the lead","effects":[{"type":"credits","delta":220},{"type":"rep","faction":"spine","delta":1}]}],"weight":0.85},{"id":"v134e_meridian_compliance","districts":["meridian_arcology"],"title":"COMPLIANCE SWEEP","text":"Every public display goes white. A Meridian voice orders all visitors to remain where they are while an internal incident is contained.","category":"threat","choices":[{"label":"Comply","effects":[{"type":"time","minutes":12},{"type":"localHeat","delta":1}]},{"label":"[HACKER] Find the incident channel","effects":[{"type":"rumor"},{"type":"contract"}],"requires":{"classes":["Hacker"]}},{"label":"Use the service evacuation lane","effects":[{"type":"hiddenRoute"},{"type":"localHeat","delta":2}]}],"weight":1.0},{"id":"v134e_crown_convoy","districts":["crown_spire"],"title":"DIPLOMATIC CONVOY","text":"A diplomatic motorcade seals the avenue. Counter-snipers appear on rooftops that looked empty a moment ago.","category":"ambient","choices":[{"label":"Wait for the cordon","effects":[{"type":"time","minutes":10},{"type":"localHeat","delta":-1}]},{"label":"[SNIPER] Read the overwatch pattern","effects":[{"type":"rumor"},{"type":"security","delta":1}],"requires":{"classes":["Sniper"]}},{"label":"Use the embassy service lane","effects":[{"type":"hiddenRoute"},{"type":"localHeat","delta":2}]}],"weight":0.85},{"id":"v134e_crown_watcher","districts":["crown_spire"],"title":"BLACK OFFICE WATCHER","text":"A person in an immaculate coat has appeared in three reflections without ever crossing the street.","category":"threat","choices":[{"label":"[AGENTEX] Lose the tail","effects":[{"type":"localHeat","delta":-4},{"type":"rumor"}],"requires":{"classes":["AgentEX"]}},{"label":"Confront them","effects":[{"type":"notoriety","delta":2},{"type":"contract"}],"requires":{"classes":["Cyber Sword","Gunslinger"]}},{"label":"Feed them a false route","effects":[{"type":"localHeat","delta":-2},{"type":"time","minutes":6}],"requires":{"classes":["Hacker","AgentEX"]}}],"weight":1.05},{"id":"v134e_crown_courier","districts":["crown_spire"],"title":"EMBASSY COURIER","text":"A courier exits a diplomatic compound carrying an old-fashioned locked case and no electronic devices.","category":"opportunity","choices":[{"label":"Follow at distance","effects":[{"type":"contract"},{"type":"time","minutes":8}]},{"label":"[AGENTEX] Swap the case at the crossing","effects":[{"type":"credits","delta":440},{"type":"notoriety","delta":4},{"type":"rumor"}],"requires":{"classes":["AgentEX"]}},{"label":"Sell the sighting","effects":[{"type":"credits","delta":180},{"type":"rep","faction":"spine","delta":1}]}],"weight":0.8},{"id":"v134e_crown_gala","districts":["crown_spire"],"title":"GALA ACCESS","text":"A diplomatic aide mistakes one of your crew for hired security and hands over a temporary event credential.","category":"opportunity","choices":[{"label":"Keep the credential","effects":[{"type":"contract"},{"type":"localHeat","delta":-1}]},{"label":"[AGENTEX] Extend its access tier","effects":[{"type":"hiddenRoute"},{"type":"rumor"}],"requires":{"classes":["AgentEX"]}},{"label":"Return it","effects":[{"type":"rep","faction":"meridian","delta":2},{"type":"security","delta":1}]}],"weight":0.75,"night":true}];
const V134_DISTRICT_STREET_PROFILES={"ash_blocks":{"actors":["gang","gang","courier","scavenger"],"risk":0.72,"color":"#ff5a35"},"floodline":{"actors":["gang","courier","smuggler","scavenger"],"risk":0.62,"color":"#7f63ff"},"old_market":{"actors":["broker","courier","gang","vendor"],"risk":0.44,"color":"#d7b06c"},"neon_row":{"actors":["gang","security","courier","vendor"],"risk":0.58,"color":"#ff38b8"},"rail_crown":{"actors":["security","worker","courier","freight"],"risk":0.48,"color":"#ffb23d"},"dock_nine":{"actors":["security","smuggler","worker","freight"],"risk":0.54,"color":"#ff9a2f"},"forge_belt":{"actors":["security","worker","worker","courier"],"risk":0.47,"color":"#d76528"},"undergrid":{"actors":["wraith","scavenger","courier","hunter"],"risk":0.68,"color":"#6c77ff"},"civic_circuit":{"actors":["security","security","courier","civilian"],"risk":0.42,"color":"#45bfff"},"glass_heights":{"actors":["security","security","courier","executive"],"risk":0.38,"color":"#a78aff"},"helix_financial":{"actors":["security","security","courier","executive"],"risk":0.49,"color":"#66e6ff"},"meridian_arcology":{"actors":["security","security","contractor","courier"],"risk":0.62,"color":"#d9f7ff"},"crown_spire":{"actors":["security","diplomat","security","courier"],"risk":0.46,"color":"#f2d76b"}};
const V134_INTERACTABLE_TYPES={"terminal":{"icon":"T","label":"PUBLIC TERMINAL","color":"#43d7e8","action":"terminal"},"camera":{"icon":"◉","label":"SURVEILLANCE CAMERA","color":"#ff6b77","action":"camera"},"service_hatch":{"icon":"H","label":"SERVICE HATCH","color":"#7f63ff","action":"hatch"},"cargo_cache":{"icon":"□","label":"CARGO CACHE","color":"#e4ad4c","action":"cargo"},"crashed_drone":{"icon":"D","label":"CRASHED DRONE","color":"#6bd9ff","action":"drone"},"street_vendor":{"icon":"$","label":"STREET VENDOR","color":"#e8bd65","action":"vendor"},"med_dispenser":{"icon":"+","label":"MED DISPENSER","color":"#66d690","action":"med"},"comm_kiosk":{"icon":"C","label":"COMM KIOSK","color":"#b060ff","action":"comm"},"graffiti":{"icon":"G","label":"FACTION GRAFFITI","color":"#ff7a9a","action":"graffiti"},"dead_drop":{"icon":"×","label":"DEAD DROP","color":"#f2d76b","action":"dead_drop"},"vending":{"icon":"V","label":"VENDING BANK","color":"#8ad4df","action":"vending"},"payphone":{"icon":"P","label":"ENCRYPTED PAYPHONE","color":"#9b8cff","action":"payphone"},"taxi_stand":{"icon":"→","label":"AUTOCAB STAND","color":"#f0b24d","action":"taxi"},"corpse":{"icon":"†","label":"UNIDENTIFIED BODY","color":"#c4cbd0","action":"corpse"}};
const V134_NOTORIETY_PRESSURE={SAFE:0,WATCHED:.16,HUNTED:.36,CONTRACT:.62,BURNED:.92};
window.V134_STREET_EVENTS=V134_STREET_EVENTS;
window.V134_INTERACTABLE_TYPES=V134_INTERACTABLE_TYPES;
window.V134_NOTORIETY_PRESSURE=V134_NOTORIETY_PRESSURE;

const V134_WALKABLE=new Set([1,2,3,4,5,6,8,9,10,11,12,13,14]);
const V134_ACTOR_RUNTIME=new Map();
const V134_REACHABLE_CACHE=new Map();
let V134_LAST_ACTOR_TICK=0;
let V134_STREET_TOAST_TIMER=0;

function C(label,effects=[],requires=null){return{label,effects,...(requires?{requires}:{})}}
function hashV134(s){let h=2166136261>>>0;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)}h^=h>>>13;h=Math.imul(h,0x5bd1e995);h^=h>>>15;return h>>>0}
function randV134(...p){return hashV134(p.join('|'))/4294967295}
function clampV134(v,a,b){return Math.max(a,Math.min(b,v))}
function currentWorldV134(){return window.currentDistrictV133?.()||null}
function walkableV134(world,x,y){if(!world||x<0||y<0||x>=world.w||y>=world.h)return false;return V134_WALKABLE.has(world.terrain[y*world.w+x])}
function classAvailableV134(classes=[]){return (Game.roster||[]).some(u=>classes.includes(u.className))}
function districtMetaV134(id){return (window.V11_SECTORS||[]).find(s=>s.id===id)||{}}
function hoodV134(world,x=Game.ovPlayer?.x,y=Game.ovPlayer?.y){return window.neighborhoodAtV133?.(x,y,world)||world?.neighborhoods?.[0]||null}

function ensureLivingStreetsStateV134(){
 if(!Game.livingStreetsV134||typeof Game.livingStreetsV134!=='object')Game.livingStreetsV134={};
 const s=Game.livingStreetsV134;
 s.version=1;s.neighborhoods=s.neighborhoods||{};s.actors=s.actors||{};s.interactables=s.interactables||{};
 s.consumed=s.consumed||{};s.recentEvents=s.recentEvents||[];s.stepCount=s.stepCount||0;s.lastEventStep=Number.isFinite(s.lastEventStep)?s.lastEventStep:-999;
 s.actorCooldown=s.actorCooldown||{};s.stats=s.stats||{events:0,interactions:0,patrolContacts:0,contracts:0,routes:0};s.streetContracts=s.streetContracts||[];
 return s
}
window.ensureLivingStreetsStateV134=ensureLivingStreetsStateV134;

function ensureNeighborhoodStateV134(world=currentWorldV134()){
 const s=ensureLivingStreetsStateV134();if(!world)return null;
 s.neighborhoods[world.id]=s.neighborhoods[world.id]||{};
 const meta=districtMetaV134(world.id),baseSec=Number(meta.security||2);
 for(const n of world.neighborhoods){
   if(!s.neighborhoods[world.id][n.id]){
     const seed=hashV134(`${world.id}:${n.id}:state`);
     s.neighborhoods[world.id][n.id]={
       id:n.id,name:n.name,security:clampV134(baseSec+((seed%3)-1),0,5),
       prosperity:clampV134(2+((seed>>>4)%4),0,5),unrest:clampV134(1+((seed>>>8)%5),0,5),
       gangPressure:clampV134(1+((seed>>>12)%5),0,5),localHeat:0,secrets:0,
       controller:meta.controller||'local',events:0
     }
   }
 }
 return s.neighborhoods[world.id]
}
window.ensureNeighborhoodStateV134=ensureNeighborhoodStateV134;

function currentNeighborhoodStateV134(world=currentWorldV134()){
 if(!world)return null;const all=ensureNeighborhoodStateV134(world),n=hoodV134(world);return n?all[n.id]:null
}
window.currentNeighborhoodStateV134=currentNeighborhoodStateV134;

function modifyNeighborhoodV134(field,delta,world=currentWorldV134()){
 const h=currentNeighborhoodStateV134(world);if(!h)return;
 if(field==='localHeat')h[field]=clampV134((h[field]||0)+delta,0,100);
 else h[field]=clampV134((h[field]||0)+delta,0,5);
 h.events=(h.events||0)+1;updateNeighborhoodHUDV134()
}

function reachableMaskV134(world){
 const key=`${world.id}:${world.signature||world.w+'x'+world.h}`,cached=V134_REACHABLE_CACHE.get(key);if(cached)return cached;
 const mask=new Uint8Array(world.w*world.h),root=world.transit?.[0]||Object.values(world.locations||{})[0];
 if(!root){V134_REACHABLE_CACHE.set(key,mask);return mask}
 const sx=Math.round(root.x),sy=Math.round(root.y);if(!walkableV134(world,sx,sy)){V134_REACHABLE_CACHE.set(key,mask);return mask}
 const qx=new Int32Array(world.w*world.h),qy=new Int32Array(world.w*world.h);let head=0,tail=0;
 qx[tail]=sx;qy[tail]=sy;tail++;mask[sy*world.w+sx]=1;
 const dirs=[[1,0],[-1,0],[0,1],[0,-1]];
 while(head<tail){const x=qx[head],y=qy[head];head++;for(const[dx,dy]of dirs){const nx=x+dx,ny=y+dy;if(nx<0||ny<0||nx>=world.w||ny>=world.h)continue;const idx=ny*world.w+nx;if(mask[idx]||!walkableV134(world,nx,ny))continue;mask[idx]=1;qx[tail]=nx;qy[tail]=ny;tail++}}
 V134_REACHABLE_CACHE.set(key,mask);return mask
}
window.reachableMaskV134=reachableMaskV134;
function nearestWalkableV134(world,x,y,used=null,max=24,requireConnected=true){
 const mask=requireConnected?reachableMaskV134(world):null;
 for(let r=0;r<=max;r++)for(let dy=-r;dy<=r;dy++)for(let dx=-r;dx<=r;dx++){
   if(r&&Math.abs(dx)!==r&&Math.abs(dy)!==r)continue;const nx=Math.round(x+dx),ny=Math.round(y+dy),k=`${nx},${ny}`;
   if(!walkableV134(world,nx,ny)||used?.has(k))continue;
   if(mask&&!mask[ny*world.w+nx])continue;
   return{x:nx,y:ny}
 }
 return null
}
window.nearestWalkableV134=nearestWalkableV134;
function actorLabelV134(type){
 return{security:'SECURITY PATROL',gang:'GANG CREW',courier:'COURIER',scavenger:'SCAVENGERS',broker:'BROKER RUNNER',vendor:'STREET VENDOR',worker:'WORK CREW',freight:'FREIGHT TEAM',smuggler:'SMUGGLER',wraith:'WRAITH CELL',hunter:'BOUNTY TEAM',civilian:'CIVILIANS',executive:'EXECUTIVE DETAIL',contractor:'CONTRACTOR TEAM',diplomat:'DIPLOMATIC DETAIL'}[type]||type.toUpperCase()
}
function actorColorV134(type,world){
 if(type==='security'||type==='executive'||type==='contractor'||type==='diplomat')return'#d9f7ff';
 if(type==='gang')return'#ff5a46';if(type==='hunter')return'#ff396b';if(type==='wraith')return'#7f63ff';
 if(type==='courier'||type==='broker')return'#e4ad4c';if(type==='smuggler')return'#b060ff';
 if(type==='vendor')return'#d7b06c';if(type==='worker'||type==='freight')return'#ff9a2f';
 return world?.cfg?.accent||'#43d7e8'
}

function applyStreetClashPopulationV134(world,actors,s=ensureLivingStreetsStateV134()){
 const clash=s.lastStreetCombat;if(!clash||clash.district!==world?.id||!clash.neighborhood||!actors?.length)return actors;
 const stamp=`${clash.missionId}:${clash.success?'won':'lost'}`;if(s.populationAftermath?.[world.id]===stamp)return actors;
 const hoodIndex=world.neighborhoods.findIndex(n=>n.id===clash.neighborhood);if(hoodIndex<0)return actors;
 const local=actors.filter(a=>a.targetHood%world.neighborhoods.length===hoodIndex);
 const hostileGang=['gang','wraith'].includes(clash.actorType),hostileLaw=['security','contractor'].includes(clash.actorType);
 if(hostileGang){
   if(clash.success){for(const a of local)if(a.type==='gang'||a.type==='wraith')a.type='courier'}
   else{const a=local.find(a=>!['gang','wraith','hunter'].includes(a.type));if(a)a.type=clash.actorType}
 }else if(hostileLaw){
   if(clash.success){const a=local.find(a=>!['security','contractor','executive'].includes(a.type));if(a)a.type='security'}
   else{for(const a of local)if(a.type==='security'||a.type==='contractor')a.type='worker'}
 }else if(clash.actorType==='hunter'&&!clash.success){const a=local.find(a=>a.type!=='hunter');if(a)a.type='hunter'}
 s.populationAftermath=s.populationAftermath||{};s.populationAftermath[world.id]=stamp;return actors
}
window.applyStreetClashPopulationV134=applyStreetClashPopulationV134;

function ensureStreetActorsV134(world=currentWorldV134()){
 const s=ensureLivingStreetsStateV134();if(!world)return[];
 if(s.actors[world.id]?.length){
   const used=new Set();for(const a of s.actors[world.id]){const idx=a.y*world.w+a.x;if(!walkableV134(world,a.x,a.y)||!reachableMaskV134(world)[idx]){const n=world.neighborhoods[a.targetHood%world.neighborhoods.length],p=nearestWalkableV134(world,n.x,n.y,used,40);if(p){a.x=p.x;a.y=p.y}}used.add(`${a.x},${a.y}`)}
   return applyStreetClashPopulationV134(world,s.actors[world.id],s)
 }
 const prof=V134_DISTRICT_STREET_PROFILES[world.id]||{actors:['courier','security'],risk:.4},used=new Set(),actors=[];
 const count=clampV134(4+Math.floor(world.neighborhoods.length*.55)+(world.id==='old_market'||world.id==='neon_row'?2:0),5,10);
 for(let i=0;i<count;i++){
   const n=world.neighborhoods[i%world.neighborhoods.length],angle=randV134(world.id,i,'actorA')*Math.PI*2,rad=4+randV134(world.id,i,'actorR')*Math.max(10,n.radius);
   const p=nearestWalkableV134(world,n.x+Math.cos(angle)*rad,n.y+Math.sin(angle)*rad,used);if(!p)continue;used.add(`${p.x},${p.y}`);
   const type=prof.actors[i%prof.actors.length],id=`v134a_${world.id}_${i}`;
   actors.push({id,type,x:p.x,y:p.y,targetHood:(i+1)%world.neighborhoods.length,steps:0,contacts:0})
 }
 s.actors[world.id]=actors;return applyStreetClashPopulationV134(world,actors,s)
}
window.ensureStreetActorsV134=ensureStreetActorsV134;

function actorPathV134(actor,world){
 const key=`${world.id}:${actor.id}`,cached=V134_ACTOR_RUNTIME.get(key);
 if(cached&&cached.targetHood===actor.targetHood&&cached.path?.length&&cached.path[0]?.x===actor.x&&cached.path[0]?.y===actor.y)return cached.path;
 const n=world.neighborhoods[actor.targetHood%world.neighborhoods.length],goal=nearestWalkableV134(world,n.x,n.y);if(!goal)return null;
 const path=window.findDistrictPathV133?.({x:actor.x,y:actor.y},goal,world);if(path?.length)V134_ACTOR_RUNTIME.set(key,{targetHood:actor.targetHood,path});return path
}
// PWA12.77: dossier operations leave a location-bound consequence on the
// existing living city. Read only completed, history-backed outcomes: no
// rendering, idling, repeated HUD opens or reload can generate a second effect.
// The canonical journal already persists in save schema 14.
function intelDistrictAftermathV134(world=currentWorldV134()){
 const relief={securityRelief:0,traceRelief:0,closed:0};
 if(!world?.id)return relief;
 const finished=new Map((Game.missionHistory||[]).filter(m=>m?.id&&m.intelFollowUpV14).map(m=>[m.id,m]));
 const seen=new Set();
 for(const entry of Game.journal||[]){
   if(!entry?.id?.startsWith('intel_outcome_')||!entry.missionId||seen.has(entry.missionId))continue;
   const mission=finished.get(entry.missionId);
   if(!mission||entry.id!==`intel_outcome_${mission.id}`||entry.decision!==mission.intelFollowUpV14.decision)continue;
   const site=entry.districtId||mission.sectorId;
   if(site!==world.id)continue;
   seen.add(entry.missionId);relief.closed++;
   // A disabled audit relay reduces active security scans; wiping the access
   // mirror lowers recognition pressure without disabling physical guards.
   if(entry.decision==='disclose')relief.securityRelief=Math.min(2,relief.securityRelief+1);
   else if(entry.decision==='erase')relief.traceRelief=Math.min(12,relief.traceRelief+6);
 }
 return relief;
}
window.intelDistrictAftermathV134=intelDistrictAftermathV134;
function actorThreatV134(actor,world){
 const n=Game.notoriety||0,h=currentNeighborhoodStateV134(world),pressure=n>=90?.92:n>=70?.62:n>=45?.36:n>=20?.16:0;
 const local=((h?.localHeat||0)/100)+((h?.security||0)/5)*.15;
 if(actor.type==='hunter')return .80+pressure*.20;
 if(actor.type==='security'||actor.type==='contractor'){
   const relief=intelDistrictAftermathV134(world);
   return clampV134(pressure+local*.35-relief.securityRelief*.10-relief.traceRelief*.012,0,1);
 }
 if(actor.type==='gang')return ((h?.gangPressure||0)/5)*.45+((h?.unrest||0)/5)*.22;
 if(actor.type==='wraith')return .25+pressure*.20;
 return .05
}
function actorContactCheckV134(actors,world,s){
 // The cut audit relay and erased access mirror make patrol recognition harder
 // only within the affected district; gang and bounty encounters remain intact.
 const relief=intelDistrictAftermathV134(world);
 for(const a of actors){
   const d=Math.hypot((Game.ovPlayer?.x||0)-a.x,(Game.ovPlayer?.y||0)-a.y),cool=s.actorCooldown[a.id]||0;
   const patrol=a.type==='security'||a.type==='contractor';
   const encounterThreshold=.30+(patrol?relief.securityRelief*.12+relief.traceRelief*.012:0);
   if(d<=2.3&&s.stepCount>=cool&&actorThreatV134(a,world)>encounterThreshold&&!Game._v134EventOpen){
     s.actorCooldown[a.id]=s.stepCount+55;s.stats.patrolContacts++;triggerActorEncounterV134(a,world);return true
   }
 }
 return false
}
function advanceStreetActorsV134(world=currentWorldV134(),ticks=1){
 if(!world||Game.screen!=='overworld-screen'||Game._v134EventOpen)return 0;
 const actors=ensureStreetActorsV134(world),s=ensureLivingStreetsStateV134(),count=Math.max(0,Math.floor(ticks||0));let advanced=0;
 for(let tick=0;tick<count&&!Game._v134EventOpen;tick++){
   for(const a of actors){
     const targeted=Game._v133TravelTarget?.kind==='v134'&&Game._v133TravelTarget?.subtype==='actor'&&Game._v133TravelTarget?.id===a.id;
     if(targeted)continue;
     const path=actorPathV134(a,world),key=`${world.id}:${a.id}`;
     if(path?.length>1){const step=path[1];a.x=step.x;a.y=step.y;a.steps++;path.shift();const rec=V134_ACTOR_RUNTIME.get(key);if(rec)rec.path=path}
     else{a.targetHood=(a.targetHood+1+Math.floor(randV134(world.id,a.id,a.steps,'turn')*(world.neighborhoods.length-1)))%world.neighborhoods.length;V134_ACTOR_RUNTIME.delete(key)}
   }
   advanced++;actorContactCheckV134(actors,world,s)
 }
 return advanced
}
window.advanceStreetActorsV134=advanceStreetActorsV134;
/* Compatibility entry point retained for old render-loop callers. It no longer
   consumes wall-clock time; simulation advances only through explicit actions. */
function updateStreetActorsV134(t,world=currentWorldV134()){return 0}
window.updateStreetActorsV134=updateStreetActorsV134;

function interactablePoolV134(world){
 const g=world.cfg.grammar;
 if(g==='undergrid')return['terminal','camera','service_hatch','crashed_drone','comm_kiosk','dead_drop','corpse'];
 if(g==='dock'||g==='forge'||g==='rail')return['terminal','camera','cargo_cache','crashed_drone','street_vendor','comm_kiosk','dead_drop','vending'];
 if(g==='glass'||g==='helix'||g==='meridian'||g==='crown')return['terminal','camera','med_dispenser','comm_kiosk','payphone','taxi_stand','dead_drop'];
 if(g==='market'||g==='neon')return['terminal','street_vendor','comm_kiosk','graffiti','dead_drop','vending','payphone','camera'];
 return['terminal','camera','service_hatch','cargo_cache','crashed_drone','street_vendor','graffiti','dead_drop','vending','corpse']
}
function ensureInteractablesV134(world=currentWorldV134()){
 const s=ensureLivingStreetsStateV134();if(!world)return[];
 if(s.interactables[world.id]?.length){
   const used=new Set();for(const o of s.interactables[world.id]){const idx=o.y*world.w+o.x;if(!walkableV134(world,o.x,o.y)||!reachableMaskV134(world)[idx]){const n=world.neighborhoods.find(x=>x.id===o.neighborhood)||world.neighborhoods[0],p=nearestWalkableV134(world,n.x,n.y,used,40);if(p){o.x=p.x;o.y=p.y}}used.add(`${o.x},${o.y}`)}
   return s.interactables[world.id]
 }
 const pool=interactablePoolV134(world),used=new Set(),arr=[],count=clampV134(7+world.neighborhoods.length*2,12,18);
 for(let i=0;i<count;i++){
   const n=world.neighborhoods[i%world.neighborhoods.length],angle=randV134(world.id,i,'intA')*Math.PI*2,rad=3+randV134(world.id,i,'intR')*Math.max(8,n.radius*.95);
   const p=nearestWalkableV134(world,n.x+Math.cos(angle)*rad,n.y+Math.sin(angle)*rad,used);if(!p)continue;used.add(`${p.x},${p.y}`);
   const type=pool[hashV134(`${world.id}:${i}:type`)%pool.length],id=`v134i_${world.id}_${i}`;
   arr.push({id,type,x:p.x,y:p.y,neighborhood:n.id,uses:0})
 }
 s.interactables[world.id]=arr;return arr
}
window.ensureInteractablesV134=ensureInteractablesV134;

function ensureV134UI(){
 const wrap=document.querySelector('#overworld-screen .wrap');if(!wrap)return;
 if(!document.getElementById('v134-neighborhood-status')){const e=document.createElement('div');e.id='v134-neighborhood-status';wrap.appendChild(e)}
 if(!document.getElementById('v134-street-toast')){const e=document.createElement('div');e.id='v134-street-toast';wrap.appendChild(e)}
 if(!document.getElementById('v134-street-event-modal')){
   const e=document.createElement('div');e.id='v134-street-event-modal';e.innerHTML='<div class="v134-event-box" id="v134-street-event-box"></div>';wrap.appendChild(e)
 }
 updateNeighborhoodHUDV134()
}
window.ensureV134UI=ensureV134UI;

function updateNeighborhoodHUDV134(){
 const e=document.getElementById('v134-neighborhood-status'),world=currentWorldV134();if(!e||!world)return;
 const h=currentNeighborhoodStateV134(world);if(!h)return;e.style.setProperty('--v134-accent',world.cfg.accent);
 const relief=intelDistrictAftermathV134(world);
 const intelStatus=relief.closed?`<small class="v134-intel-district-status">${relief.securityRelief?'AUDIT RELAY OFFLINE · PATROL PRESSURE -'+relief.securityRelief:''}${relief.securityRelief&&relief.traceRelief?' · ':''}${relief.traceRelief?'ACCESS MIRROR ERASED · TRACE -'+relief.traceRelief:''}</small>`:'';
 const clash=ensureLivingStreetsStateV134().lastStreetCombat;
 const clashHere=clash&&clash.district===world.id&&(!clash.neighborhood||clash.neighborhood===h.id);
 const clashStatus=clashHere?`<small class="v134-clash-status ${clash.success?'won':'lost'}">${clash.success?'BLOCK HELD':'BLOCK CEDED'} · ${actorLabelV134(clash.actorType)} · DAY ${clash.day}</small>`:'';
 e.innerHTML=`<b>${h.name.toUpperCase()}</b><span>SEC ${h.security}/5 · UNREST ${h.unrest}/5 · GANG ${h.gangPressure}/5<br>LOCAL HEAT ${h.localHeat} · PROSPERITY ${h.prosperity}/5</span>${clashStatus}${intelStatus}`
}
window.updateNeighborhoodHUDV134=updateNeighborhoodHUDV134;

function streetToastV134(text){
 const e=document.getElementById('v134-street-toast');if(!e)return;e.textContent=text;e.classList.add('show');clearTimeout(V134_STREET_TOAST_TIMER);V134_STREET_TOAST_TIMER=setTimeout(()=>e.classList.remove('show'),1700)
}
function describeRequirementV134(r){
 if(!r)return'';const bits=[];if(r.credits)bits.push(`¢${r.credits}`);if(r.classes)bits.push(r.classes.join('/'));if(r.rep)bits.push(`${r.rep.faction} REP ${r.rep.min}+`);return bits.join(' · ')
}
function requirementMetV134(r){
 if(!r)return true;if(r.credits&&Game.credits<r.credits)return false;if(r.classes&&!classAvailableV134(r.classes))return false;if(r.rep&&(Game.rep?.[r.rep.faction]||0)<r.rep.min)return false;return true
}
function revealRumorV134(){
 if(typeof generateRumorsV13==='function')generateRumorsV13(true);
 const unseen=(Game.rumors||[]).filter(r=>!r.followed);if(unseen.length){const r=unseen[hashV134(`${Game.day}:${Game.hour}:${unseen.length}`)%unseen.length];r.known=true;streetToastV134(`RUMOR ACQUIRED · ${r.title||'new lead'}`);return r}
 streetToastV134('Street intel added to your network.');return null
}
function unlockHiddenRouteV134(world=currentWorldV134()){
 if(!world)return false;const s=ensureLivingStreetsStateV134(),links=(window.V133_TRANSIT_LINKS||[]).filter(l=>l.type==='hidden'&&(l.from.district===world.id||l.to.district===world.id)&&!Game.districtWorldsV133.hiddenLinks[l.id]);
 if(!links.length){revealRumorV134();return false}const l=links[hashV134(`${world.id}:${s.stepCount}:route`)%links.length];Game.districtWorldsV133.hiddenLinks[l.id]=true;s.stats.routes++;streetToastV134(`HIDDEN ROUTE DISCOVERED · ${l.name}`);return true
}
window.unlockHiddenRouteV134=unlockHiddenRouteV134;

function createStreetContractV134(world=currentWorldV134()){
 if(!world)return null;const s=ensureLivingStreetsStateV134(),types=['raid','steal','rescue','secure','bounty'],type=types[hashV134(`${world.id}:${s.stepCount}:contract`)%types.length],meta=districtMetaV134(world.id),id=`v134street_${world.id}_${Game.day}_${s.stepCount}`;
 const diff=clampV134(1+Math.floor((Game.notoriety||0)/28)+Math.floor((meta.security||2)/2),1,5);
 const m={id,name:`Street Lead · ${world.cfg.name}`,type,objective:type,sectorId:world.id,targetFaction:meta.controller||'spine',enemies:['Guard','Enforcer'],diff,reward:550+diff*260,xp:120+diff*70,factionRepGain:2,factionRepLoss:{},desc:`A lead discovered on the street in ${world.cfg.name}.`,v134Street:true};
 const local=(Game.contacts||[]).filter(c=>c.sectorId===world.id);const c=local[0]||Game.contacts?.[0];if(c){c.missions=c.missions||[];c.missions.push(m)}s.streetContracts.push(id);s.stats.contracts++;addJournal?.('side','Street Contract',`${m.name} entered the broker network.`);streetToastV134(`NEW STREET CONTRACT · ${m.name}`);return m
}
window.createStreetContractV134=createStreetContractV134;

function discoverLocationV134(world=currentWorldV134()){
 if(!world)return false;const s=ensureLivingStreetsStateV134(),unknown=(window.V13_DISTRICT_LOCATIONS?.[world.id]||[]).filter(l=>!Game.cityLife?.discovered?.[l.id]);
 if(!unknown.length)return false;const l=unknown[hashV134(`${world.id}:${s.stepCount}:loc`)%unknown.length];Game.cityLife.discovered[l.id]=true;streetToastV134(`LOCATION DISCOVERED · ${l.name}`);return true
}
function modifyTrustAnyV134(delta,world=currentWorldV134()){
 const local=(window.V13_CONTACTS||[]).filter(c=>c.sectorId===world?.id&&Game.contactRelations?.[c.id]?.known);if(!local.length)return;const c=local[hashV134(`${world.id}:${Game.livingStreetsV134.stepCount}:trust`)%local.length];if(typeof changeContactTrustV13==='function')changeContactTrustV13(c.id,delta,'Street encounter')
}
function applyStreetEffectV134(e,world=currentWorldV134()){
 if(!e)return;
 switch(e.type){
   case'credits':Game.credits=Math.max(0,(Game.credits||0)+(e.delta||0));break;
   case'salvage':Game.salvage=(Game.salvage||0)+(e.delta||0);break;
   case'notoriety':if(typeof addNotorietyV12==='function')addNotorietyV12(e.delta||0,'Street encounter');else Game.notoriety=clampV134((Game.notoriety||0)+(e.delta||0),0,100);break;
   case'rep':Game.rep[e.faction]=(Game.rep[e.faction]||0)+(e.delta||0);break;
   case'localHeat':modifyNeighborhoodV134('localHeat',e.delta||0,world);break;
   case'unrest':modifyNeighborhoodV134('unrest',e.delta||0,world);break;
   case'security':modifyNeighborhoodV134('security',e.delta||0,world);break;
   case'gangPressure':modifyNeighborhoodV134('gangPressure',e.delta||0,world);break;
   case'prosperity':modifyNeighborhoodV134('prosperity',e.delta||0,world);break;
   case'rumor':revealRumorV134();break;
   case'hiddenRoute':unlockHiddenRouteV134(world);break;
   case'contract':createStreetContractV134(world);break;
   case'trustAny':modifyTrustAnyV134(e.delta||0,world);break;
   case'time':advanceTime(e.minutes||1);break;
   case'heal':for(const u of Game.roster||[])u.hp=Math.min(u.maxHp||u.hp,(u.hp||0)+(e.amount||5));break;
   case'injuryRisk':if(randV134(Game.day,Game.hour,Game.livingStreetsV134.stepCount,'injury')<(e.chance||.2)){const u=(Game.roster||[])[0];if(u){u.hp=Math.max(1,(u.hp||1)-12);streetToastV134('ROUGH PASSAGE · crew member hurt')}}break;
   case'interactable':spawnBonusInteractableV134(world);break;
   case'location':discoverLocationV134(world);break;
   case'streetCombat':setTimeout(()=>launchStreetCombatV134(e.actorType||'gang',world),80);break;
 }
}
function closeStreetEventV134(){
 const m=document.getElementById('v134-street-event-modal');m?.classList.remove('open');Game._v134EventOpen=false;Game.pendingPath=null;Game._v133TravelTarget=null;updateNeighborhoodHUDV134();updateOverworldHUD?.();saveGame?.(0,true)
}
function openStreetEventV134(ev,source='street'){
 ensureV134UI();const world=currentWorldV134(),box=document.getElementById('v134-street-event-box'),modal=document.getElementById('v134-street-event-modal');if(!box||!modal||!ev)return false;
 Game._v134EventOpen=true;Game.pendingPath=null;Game._v133TravelTarget=null;box.style.setProperty('--v134-accent',world?.cfg?.accent||'#43d7e8');
 const h=currentNeighborhoodStateV134(world),choices=ev.choices||[];
 box.innerHTML=`<div class="v134-event-kicker">${(world?.cfg?.name||'CHROME CITY').toUpperCase()} // ${(h?.name||'STREET').toUpperCase()} // ${(ev.category||source).toUpperCase()}</div><h2>${ev.title}</h2><p>${ev.text}</p><div id="v134-event-choices"></div><div class="v134-event-footer">Notoriety ${Game.notoriety||0} · Local Heat ${h?.localHeat||0} · Security ${h?.security||0}/5</div>`;
 const list=box.querySelector('#v134-event-choices');
 choices.forEach((ch,i)=>{const ok=requirementMetV134(ch.requires),b=document.createElement('button');b.className='v134-event-choice';b.disabled=!ok;b.innerHTML=`${ch.label}${ch.requires?`<small>${ok?'AVAILABLE':'REQUIRES'} · ${describeRequirementV134(ch.requires)}</small>`:''}`;b.onclick=()=>{for(const e of ch.effects||[])applyStreetEffectV134(e,world);const s=ensureLivingStreetsStateV134();s.stats.events++;s.recentEvents.unshift(ev.id);s.recentEvents=s.recentEvents.slice(0,12);if(h)h.events=(h.events||0)+1;closeStreetEventV134()};list.appendChild(b)});
 if(!choices.length){const b=document.createElement('button');b.className='v134-event-choice';b.textContent='CONTINUE';b.onclick=closeStreetEventV134;list.appendChild(b)}
 modal.classList.add('open');return true
}
window.openStreetEventV134=openStreetEventV134;

function notorietyPressureV134(){
 const n=Game.notoriety||0;if(n>=90)return V134_NOTORIETY_PRESSURE.BURNED;if(n>=70)return V134_NOTORIETY_PRESSURE.CONTRACT;if(n>=45)return V134_NOTORIETY_PRESSURE.HUNTED;if(n>=20)return V134_NOTORIETY_PRESSURE.WATCHED;return 0
}
function eligibleStreetEventsV134(world=currentWorldV134()){
 if(!world)return[];const s=ensureLivingStreetsStateV134(),h=currentNeighborhoodStateV134(world),night=(Game.hour||12)>=20||(Game.hour||12)<6;
 return V134_STREET_EVENTS.filter(e=>e.districts.includes(world.id)&&(!e.night||night)&&!s.recentEvents.slice(0,6).includes(e.id)).map(e=>{
   let w=e.weight||1;if(e.category==='threat')w*=1+notorietyPressureV134()+((h?.localHeat||0)/100)+((h?.unrest||0)/5)*.25;if(e.category==='opportunity')w*=1+((h?.prosperity||0)/5)*.15;return{e,w}
 })
}
function runEncounterDirectorV134(force=false,world=currentWorldV134()){
 const s=ensureLivingStreetsStateV134();if(!world||Game._v134EventOpen)return false;const h=currentNeighborhoodStateV134(world),prof=V134_DISTRICT_STREET_PROFILES[world.id]||{risk:.4};
 const since=s.stepCount-s.lastEventStep;if(!force&&since<30)return false;
 const chance=.055+(prof.risk||.4)*.035+notorietyPressureV134()*.045+((h?.localHeat||0)/100)*.035;
 if(!force&&randV134(world.id,s.stepCount,Game.day,Math.floor(Game.hour||0),'director')>chance)return false;
 const pool=eligibleStreetEventsV134(world);if(!pool.length)return false;const total=pool.reduce((a,x)=>a+x.w,0),roll=randV134(world.id,s.stepCount,'pick')*total;let acc=0,pick=pool[0].e;for(const x of pool){acc+=x.w;if(roll<=acc){pick=x.e;break}}
 s.lastEventStep=s.stepCount;return openStreetEventV134(pick,'director')
}
window.runEncounterDirectorV134=runEncounterDirectorV134;

function streetContactSupportV134(world=currentWorldV134()){
 if(!world)return null;
 const defs=window.V13_CONTACTS||[];
 const candidates=defs.filter(d=>d.sectorId===world.id&&Game.contactRelations?.[d.id]?.known).map(d=>({
   id:d.id,name:d.name,faction:d.faction,trust:Number(Game.contactRelations[d.id]?.trust||0),influence:Number(Game.contactRelations[d.id]?.influence||0)
 })).filter(c=>c.trust>=20).sort((a,b)=>(b.trust-a.trust)||(b.influence-a.influence)||a.id.localeCompare(b.id));
 if(!candidates.length)return null;
 const c=candidates[0],tier=c.trust>=45?2:1;
 return{...c,tier,label:tier>=2?'LOCAL BACKUP':'LOCAL WARNING'}
}
window.streetContactSupportV134=streetContactSupportV134;

function launchStreetCombatV134(actorType='gang',world=currentWorldV134()){
 if(!world||Game.activeMission)return false;
 const s=ensureLivingStreetsStateV134(),meta=districtMetaV134(world.id),support=streetContactSupportV134(world);
 const enemyMap={security:['Guard','Enforcer'],contractor:['Guard','Enforcer'],gang:['Raider','Enforcer'],hunter:['Enforcer','Sniper'],wraith:['Raider','Hacker']};
 const enemies=[...(enemyMap[actorType]||['Guard','Enforcer'])];
 let diff=clampV134(1+Math.floor((Game.notoriety||0)/30)+Math.floor((meta.security||2)/2),1,5);
 // PWA12.104: a trusted contact only helps when they physically operate in this district.
 // Their warning lowers encounter pressure; high-trust contacts also peel one hostile away before initiative begins.
 if(support){diff=Math.max(1,diff-1);if(support.tier>=2&&enemies.length>1)enemies.pop()}
 const hood=hoodV134(world),actorFaction={wraith:'wraiths',gang:'iron',security:meta.controller||'meridian',contractor:meta.controller||'meridian',hunter:meta.controller||'spine'}[actorType]||meta.controller||'spine';
 const streetShape=actorType==='security'||actorType==='contractor'?'checkpoint':actorType==='hunter'?'alley':(['undergrid','floodline','dock_nine'].includes(world.id)?'underpass':'alley');
 const supportText=support?` ${support.name} ${support.tier>=2?'calls in local help and thins the hostile line':'feeds you a warning before contact'}.`:'';
 const m={id:`v134streetfight_${world.id}_${Game.day}_${s.stepCount}`,name:`Street Clash · ${world.cfg.name}`,type:'bounty',objective:'bounty',sectorId:world.id,targetFaction:actorFaction,enemies:[...enemies],diff,reward:180+diff*90,xp:80+diff*45,factionRepGain:0,factionRepLoss:{},contact:support?.id||null,desc:`A ${actorLabelV134(actorType).toLowerCase()} confrontation in ${world.cfg.name} turns into a tactical firefight.${supportText} No timer: initiative advances only when combatants act.`,v134StreetEncounter:true,v134StreetActorType:actorType,v134StreetNeighborhood:hood?.id||null,v134ContactSupport:support?{id:support.id,name:support.name,tier:support.tier,label:support.label}:null,tacticalShape:streetShape,v134StreetArena:streetShape};
 s.stats.streetCombats=(s.stats.streetCombats||0)+1;
 addJournal?.('side','Street Clash',`${m.name}: a physical street encounter escalated into tactical combat.${support?` ${support.name} provided ${support.label.toLowerCase()}.`:''}`);
 saveGame?.(0,true);
 if(typeof V10PrevStartMission==='function'){V10PrevStartMission(m);return true}
 if(typeof startMission==='function'){startMission(m);return true}
 Game.activeMission=m;setTimeout(()=>{showScreen('combat');initCombat(m)},120);return true
}
window.launchStreetCombatV134=launchStreetCombatV134;

function settleStreetCombatV134(m,success){
 if(!m?.v134StreetEncounter)return false;const s=ensureLivingStreetsStateV134(),district=s.neighborhoods?.[m.sectorId],h=(m.v134StreetNeighborhood&&district?.[m.v134StreetNeighborhood])||Object.values(district||{})[0];
 if(h){h.localHeat=clampV134((h.localHeat||0)+(success?8:4),0,100);h.unrest=clampV134((h.unrest||0)+(success?1:2),0,5);if(['gang','wraith'].includes(m.v134StreetActorType))h.gangPressure=clampV134((h.gangPressure||0)+(success?-2:2),0,5);if(['security','contractor'].includes(m.v134StreetActorType))h.security=clampV134((h.security||0)+(success?1:0),0,5);h.events=(h.events||0)+1}
 if(m.targetFaction&&Game.rep){Game.rep[m.targetFaction]=(Game.rep[m.targetFaction]||0)+(success?-1:0);if(Game.heat)Game.heat[m.targetFaction]=clampV134((Game.heat[m.targetFaction]||0)+(success?5:2),0,100)}
 const relation=m.contact&&Game.contactRelations?.[m.contact];if(success&&relation?.known&&typeof changeContactTrustV13==='function')changeContactTrustV13(m.contact,1,'Won a street clash nearby');
 s.stats.streetVictories=(s.stats.streetVictories||0)+(success?1:0);s.stats.streetDefeats=(s.stats.streetDefeats||0)+(success?0:1);s.lastStreetCombat={missionId:m.id,district:m.sectorId,neighborhood:m.v134StreetNeighborhood||null,actorType:m.v134StreetActorType,success:!!success,day:Game.day};
 if(currentWorldV134()?.id===m.sectorId)applyStreetClashPopulationV134(currentWorldV134(),ensureStreetActorsV134(currentWorldV134()),s);
 addJournal?.('side',success?'Street Clash Won':'Street Clash Lost',`${m.name}: ${success?'the crew held the street':'emergency extraction ceded the block'}. Neighborhood pressure shifted.`);updateNeighborhoodHUDV134();saveGame?.(0,true);return true
}
window.settleStreetCombatV134=settleStreetCombatV134;
if(typeof Events!=='undefined'&&typeof Events.on==='function')Events.on('mission:success',m=>settleStreetCombatV134(m,true));
const V134PrevReturnToOverworld=returnToOverworld;
returnToOverworld=function(success){const m=Game.activeMission;if(m?.v134StreetEncounter&&success===false)settleStreetCombatV134(m,false);return V134PrevReturnToOverworld.apply(this,arguments)};

function triggerActorEncounterV134(actor,world=currentWorldV134()){
 const type=actor.type,label=actorLabelV134(type),hostile=['security','gang','hunter','wraith','contractor'].includes(type);
 const ev={id:`actor_${actor.id}_${Game.livingStreetsV134.stepCount}`,title:label,text:
   type==='security'||type==='contractor'?'The patrol slows and turns toward your crew. Their optics are already comparing faces against a live watchlist.':
   type==='gang'?'The crew spreads across the street and decides you look profitable enough to stop.':
   type==='hunter'?'The bounty team does not pretend this is a random meeting. Their weapons are still low, for now.':
   type==='wraith'?'A masked cell emerges from service shadows and waits for your reaction.':
   type==='courier'?'A courier recognizes your fixer tag and offers a sealed lead for a price.':
   'A street crew pauses long enough to decide whether you are business or trouble.',
   category:hostile?'threat':'ambient',choices:[]};
 if(type==='security'||type==='contractor'){
   ev.choices=[
    C('Submit to a quick scan',[{type:'localHeat',delta:2},{type:'time',minutes:4}]),
    C('[AGENTEX] Talk through the inspection',[{type:'localHeat',delta:-3}],{classes:['AgentEX']}),
    C('[HACKER] Corrupt the watchlist hit',[{type:'notoriety',delta:-1},{type:'localHeat',delta:-2}],{classes:['Hacker']})
   ]
 }else if(type==='gang'||type==='hunter'||type==='wraith'){
   ev.choices=[
    C('Pay them off · ¢220',[{type:'credits',delta:-220},{type:'localHeat',delta:-2}],{credits:220}),
    C('[CYBER SWORD / GUNSLINGER] Hold the street',[{type:'gangPressure',delta:-2},{type:'notoriety',delta:2}],{classes:['Cyber Sword','Gunslinger']}),
    C('Stand and fight · tactical combat',[{type:'streetCombat',actorType:type}]),
    C('Back away',[{type:'time',minutes:7}])
   ]
 }else{
   ev.choices=[
    C('Talk',[{type:'rumor'}]),
    C('Offer work',[{type:'contract'}]),
    C('Keep moving',[])
   ]
 }
 window.CR14StreetPresentation?.setStreetEventArt?.('streetActors',type,label,actorColorV134(type,world));
 actor.contacts=(actor.contacts||0)+1;return openStreetEventV134(ev,'patrol')
}
window.triggerActorEncounterV134=triggerActorEncounterV134;


function spawnBonusInteractableV134(world=currentWorldV134()){
 if(!world)return null;const s=ensureLivingStreetsStateV134(),arr=ensureInteractablesV134(world),n=hoodV134(world),p=nearestWalkableV134(world,n.x+4,n.y+4);if(!p)return null;
 const id=`v134i_bonus_${world.id}_${s.stepCount}`,obj={id,type:'dead_drop',x:p.x,y:p.y,neighborhood:n.id,uses:0};arr.push(obj);return obj
}
function interactableEventV134(obj,world=currentWorldV134()){
 const def=V134_INTERACTABLE_TYPES[obj.type],common={id:`int_${obj.id}_${obj.uses}`,category:'opportunity'};
 const map={
  terminal:{title:'PUBLIC TERMINAL',text:'The kiosk is poorly segmented from the district service network.',choices:[C('[HACKER] Open service access',[{type:'rumor'},{type:'credits',delta:90}],{classes:['Hacker']}),C('Search public records',[{type:'rumor'},{type:'time',minutes:3}]),C('Leave',[])]},
  camera:{title:'SURVEILLANCE CAMERA',text:'A municipal camera tracks the intersection with more enthusiasm than its age suggests.',choices:[C('[HACKER] Loop the feed',[{type:'localHeat',delta:-4}],{classes:['Hacker']}),C('Destroy it',[{type:'security',delta:-1},{type:'notoriety',delta:1}],{classes:['Gunslinger','Sniper']}),C('Avoid its field',[{type:'time',minutes:3}])]},
  hatch:{title:'SERVICE HATCH',text:'The seal is old, but someone has opened it recently.',choices:[C('[HACKER] Open the lock',[{type:'hiddenRoute'}],{classes:['Hacker']}),C('[CYBER SWORD] Force it',[{type:'hiddenRoute'},{type:'notoriety',delta:1}],{classes:['Cyber Sword']}),C('Mark it on the map',[{type:'rumor'}])]},
  cargo:{title:'CARGO CACHE',text:'The container seal has been replaced with a cheap aftermarket lock.',choices:[C('Take useful parts',[{type:'salvage',delta:2},{type:'localHeat',delta:1}]),C('[AGENTEX] Find the owner',[{type:'contract'}],{classes:['AgentEX']}),C('Leave it',[])]},
  drone:{title:'CRASHED DRONE',text:'The drone is dead, but its memory and actuators may not be.',choices:[C('[HACKER] Extract memory',[{type:'rumor'},{type:'salvage',delta:1}],{classes:['Hacker']}),C('Strip components',[{type:'salvage',delta:2}]),C('Leave it',[])]},
  vendor:{title:'STREET VENDOR',text:'A folding counter appears wherever security cameras do not look.',choices:[C('Buy supplies · ¢120',[{type:'credits',delta:-120},{type:'heal',amount:6}],{credits:120}),C('Ask what is moving tonight',[{type:'rumor'}]),C('Move on',[])]},
  med:{title:'MED DISPENSER',text:'The public dispenser still has two sealed trauma cartridges.',choices:[C('Buy cartridge · ¢100',[{type:'credits',delta:-100},{type:'heal',amount:10}],{credits:100}),C('[HACKER] Release emergency stock',[{type:'heal',amount:8},{type:'localHeat',delta:1}],{classes:['Hacker']}),C('Leave it',[])]},
  comm:{title:'COMM KIOSK',text:'The booth carries several encrypted community channels under harmless public labels.',choices:[C('Listen for traffic',[{type:'rumor'}]),C('[HACKER] Trace the hidden channel',[{type:'hiddenRoute'},{type:'rumor'}],{classes:['Hacker']}),C('Leave',[])]},
  graffiti:{title:'FACTION MARK',text:'Fresh paint overlays three older claims to the same wall.',choices:[C('Read the territory shift',[{type:'rumor'}]),C('Cover it',[{type:'gangPressure',delta:-1},{type:'unrest',delta:1}]),C('Ignore it',[])]},
  dead_drop:{title:'DEAD DROP',text:'The cache is keyed to an old broker protocol and has not been collected.',choices:[C('Open it',[{type:'contract'},{type:'localHeat',delta:2}]),C('Forward the code to a fixer',[{type:'trustAny',delta:2}]),C('Leave it untouched',[])]},
  vending:{title:'VENDING BANK',text:'Food, batteries, stimulant gum and six kinds of synthetic coffee.',choices:[C('Buy crew supplies · ¢60',[{type:'credits',delta:-60},{type:'heal',amount:3}],{credits:60}),C('Move on',[])]},
  payphone:{title:'ENCRYPTED PAYPHONE',text:'The receiver is warm. A number is scratched into the underside.',choices:[C('Call the number',[{type:'rumor'},{type:'contract'}]),C('[AGENTEX] Verify the route first',[{type:'hiddenRoute'}],{classes:['AgentEX']}),C('Do not touch it',[])]},
  taxi:{title:'AUTOCAB STAND',text:'A privately routed cab can get you across the neighborhood without using public transit logs.',choices:[C('Take the clean ride · ¢150',[{type:'credits',delta:-150},{type:'localHeat',delta:-3},{type:'time',minutes:4}],{credits:150}),C('Keep walking',[])]},
  corpse:{title:'UNIDENTIFIED BODY',text:'No wallet. No visible weapon. One datajack has been deliberately melted.',choices:[C('Search the clothing',[{type:'credits',delta:80},{type:'localHeat',delta:1}]),C('[HACKER] Recover the jack remnants',[{type:'rumor'}],{classes:['Hacker']}),C('Notify a clinic',[{type:'trustAny',delta:1}])]}
 }[obj.type]||{title:def?.label||'STREET OBJECT',text:'Something useful may be here.',choices:[C('Inspect',[{type:'rumor'}]),C('Leave',[])]};
 return{...common,...map}
}
function interactWithV134(obj,world=currentWorldV134()){
 if(!obj||ensureLivingStreetsStateV134().consumed[obj.id])return false;obj.uses=(obj.uses||0)+1;ensureLivingStreetsStateV134().stats.interactions++;
 const ev=interactableEventV134(obj,world),def=V134_INTERACTABLE_TYPES[obj.type];
 window.CR14StreetPresentation?.setStreetEventArt?.('streetInteractables',obj.type,def?.label||obj.type,def?.color||world?.cfg?.accent);
 const result=openStreetEventV134(ev,'interactable');
 if(['cargo_cache','crashed_drone','dead_drop','corpse'].includes(obj.type))ensureLivingStreetsStateV134().consumed[obj.id]=true;
 return result
}
window.interactWithV134=interactWithV134;


function livingMarkerAtV134(q,world=currentWorldV134()){
 if(!world)return null;const ints=ensureInteractablesV134(world).filter(o=>!Game.livingStreetsV134.consumed[o.id]);
 for(const o of ints)if(Math.hypot(o.x-q.x,o.y-q.y)<=1.05)return{subtype:'interactable',id:o.id,obj:o};
 for(const a of ensureStreetActorsV134(world))if(Math.hypot(a.x-q.x,a.y-q.y)<=1.1)return{subtype:'actor',id:a.id,obj:a};
 return null
}
function routeLivingTargetV134(mark,world=currentWorldV134()){
 const p={x:mark.obj.x,y:mark.obj.y},path=window.findDistrictPathV133?.(Game.ovPlayer,p,world);if(!path?.length){streetToastV134('NO STREET ROUTE');return false}
 if(path.length<=2)return completeLivingStreetTargetV134({kind:'v134',subtype:mark.subtype,id:mark.id});
 Game.pendingPath=path;Game._v133TravelTarget={kind:'v134',subtype:mark.subtype,id:mark.id,label:mark.subtype==='actor'?actorLabelV134(mark.obj.type):V134_INTERACTABLE_TYPES[mark.obj.type]?.label||'Street object'};Game.ovCamera.follow=true;return true
}
function handleLivingStreetTapV134(q){
 const world=currentWorldV134(),mark=livingMarkerAtV134(q,world);if(!mark)return false;const d=Math.hypot(Game.ovPlayer.x-mark.obj.x,Game.ovPlayer.y-mark.obj.y);
 return d<=2.1?!!completeLivingStreetTargetV134({kind:'v134',subtype:mark.subtype,id:mark.id}):!!routeLivingTargetV134(mark,world)
}
window.handleLivingStreetTapV134=handleLivingStreetTapV134;

function completeLivingStreetTargetV134(target){
 const world=currentWorldV134();if(!target||!world)return false;
 if(target.subtype==='interactable'){const obj=ensureInteractablesV134(world).find(x=>x.id===target.id);return interactWithV134(obj,world)}
 if(target.subtype==='actor'){const a=ensureStreetActorsV134(world).find(x=>x.id===target.id);return a?triggerActorEncounterV134(a,world):false}
 return false
}
window.completeLivingStreetTargetV134=completeLivingStreetTargetV134;

const STREET_TEXT_METRICS_V134=new Map();
function cachedStreetTextWidthV134(ctx,text){const key=ctx.font+'\n'+text;let w=STREET_TEXT_METRICS_V134.get(key);if(w===undefined){w=ctx.measureText(text).width;STREET_TEXT_METRICS_V134.set(key,w)}return w}
function drawLivingStreetsV134(ctx,world,W,H,t,hover){
 if(window.CR14StreetPresentation?.drawLivingStreetsV14)return window.CR14StreetPresentation.drawLivingStreetsV14(ctx,world,W,H,t,hover);
 if(!world||!ctx)return;ensureNeighborhoodStateV134(world);const s=ensureLivingStreetsStateV134();
 const w2s=window.worldToScreen;
 for(const o of ensureInteractablesV134(world)){
   if(s.consumed[o.id])continue;const p=w2s(o.x+.5,o.y+.5);if(p.x<-20||p.y<-20||p.x>W+20||p.y>H+20)continue;const d=V134_INTERACTABLE_TYPES[o.type]||{},r=Math.max(4,Math.min(7,t*.16));
   ctx.save();ctx.translate(p.x,p.y);ctx.fillStyle='rgba(4,10,14,.88)';ctx.strokeStyle=d.color||'#43d7e8';ctx.lineWidth=1.3;ctx.beginPath();ctx.rect(-r,-r,r*2,r*2);ctx.fill();ctx.stroke();ctx.fillStyle=d.color||'#43d7e8';ctx.font=`800 ${Math.max(6,r*1.1)}px Orbitron`;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(d.icon||'•',0,.5);ctx.restore()
 }
 for(const a of ensureStreetActorsV134(world)){
   const p=w2s(a.x+.5,a.y+.5);if(p.x<-24||p.y<-24||p.x>W+24||p.y>H+24)continue;const col=actorColorV134(a.type,world),r=Math.max(5,Math.min(8,t*.19));
   ctx.save();ctx.translate(p.x,p.y);ctx.shadowColor=col;ctx.shadowBlur=8;ctx.fillStyle='rgba(4,9,13,.94)';ctx.strokeStyle=col;ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.shadowBlur=0;ctx.fillStyle=col;ctx.beginPath();ctx.moveTo(0,-r*.55);ctx.lineTo(r*.45,r*.38);ctx.lineTo(-r*.45,r*.38);ctx.closePath();ctx.fill();
   if(Math.hypot((Game.ovPlayer?.x||0)-a.x,(Game.ovPlayer?.y||0)-a.y)<4.5&&t>=24){ctx.font=`700 ${Math.max(6,t*.16)}px Share Tech Mono`;ctx.textAlign='center';const label=actorLabelV134(a.type),mw=cachedStreetTextWidthV134(ctx,label);ctx.fillStyle='rgba(2,6,9,.84)';ctx.fillRect(-mw/2-3,r+3,mw+6,10);ctx.fillStyle=col;ctx.fillText(label,0,r+10)}
   ctx.restore()
 }
}
window.drawLivingStreetsV134=drawLivingStreetsV134;

function onStreetStepV134(world=currentWorldV134()){
 const s=ensureLivingStreetsStateV134();s.stepCount++;ensureNeighborhoodStateV134(world);const actors=ensureStreetActorsV134(world);ensureInteractablesV134(world);
 /* Six quarter-minute player steps ~= 1.5 game minutes, matching the old
    actor cadence without tying simulation to animation-frame wall time. */
 if(s.stepCount%6===0)advanceStreetActorsV134(world,1);else actorContactCheckV134(actors,world,s);
 updateNeighborhoodHUDV134();runEncounterDirectorV134(false,world)
}
window.onStreetStepV134=onStreetStepV134;

function restoreLivingStreetsV134(data){
 Game.livingStreetsV134=data?.livingStreetsV134||null;ensureLivingStreetsStateV134();V134_ACTOR_RUNTIME.clear();V134_REACHABLE_CACHE.clear();
 const world=currentWorldV134();if(world){ensureNeighborhoodStateV134(world);ensureStreetActorsV134(world);ensureInteractablesV134(world)}updateNeighborhoodHUDV134()
}
window.restoreLivingStreetsV134=restoreLivingStreetsV134;

function runDiagnosticsV134(){
 const rows=[],add=(n,ok,d='')=>rows.push({name:n,ok:!!ok,details:d});try{
   const s=ensureLivingStreetsStateV134(),world=currentWorldV134();ensureNeighborhoodStateV134(world);const actors=ensureStreetActorsV134(world),ints=ensureInteractablesV134(world);
   add('52 authored street events',V134_STREET_EVENTS.length===52,V134_STREET_EVENTS.length);
   add('14 interactable types',Object.keys(V134_INTERACTABLE_TYPES).length>=14,Object.keys(V134_INTERACTABLE_TYPES).length);
   add('neighborhood state',Object.keys(s.neighborhoods[world.id]||{}).length===world.neighborhoods.length);
   add('visible street actors',actors.length>=5,actors.length);add('physical interactables',ints.length>=12,ints.length);
   add('encounter director',typeof runEncounterDirectorV134==='function');add('notoriety pressure',notorietyPressureV134()>=0);
   add('hidden-route outcomes',typeof unlockHiddenRouteV134==='function');add('street contracts',typeof createStreetContractV134==='function');
   add('save state',!!Game.livingStreetsV134);add('v13.3 retained',!!ChromeRequiem.modules?.DistrictWorldsV133);add('v12 tactical retained',!!ChromeRequiem.modules?.TacticalV12)
 }catch(e){add('exception',false,e.message)}
 return{version:V134_VERSION,passed:rows.filter(x=>x.ok).length,total:rows.length,results:rows}
}
window.runDiagnosticsV134=runDiagnosticsV134;

/* Save/load wrappers */
const V134PrevSerialize=serializeGame;
serializeGame=function(){const d=JSON.parse(V134PrevSerialize());d.version=V134_VERSION;d.livingStreetsV134=JSON.parse(JSON.stringify(ensureLivingStreetsStateV134()));return JSON.stringify(d)};
const V134PrevLoad=loadGame;
loadGame=function(slot){
 let data=null;for(const p of ['chrome_requiem_v13_'+slot,'chrome_requiem_v12_'+slot,'chrome_requiem_v11_'+slot,'chrome_requiem_v10_'+slot,'chrome_requiem_v9_'+slot,'chrome_requiem_v8_'+slot,'chrome_requiem_v7_'+slot,'chrome_requiem_save_'+slot]){const raw=localStorage.getItem(p);if(raw){try{data=JSON.parse(raw)}catch(e){}break}}
 const ok=V134PrevLoad(slot);if(ok){restoreLivingStreetsV134(data);ensureV134UI()}return ok
};
const V134PrevNew=startNewGame;
startNewGame=function(name,className,background){const r=V134PrevNew(name,className,background);Game.livingStreetsV134=null;ensureLivingStreetsStateV134();const w=currentWorldV134();ensureNeighborhoodStateV134(w);ensureStreetActorsV134(w);ensureInteractablesV134(w);ensureV134UI();return r};

window.ChromeRequiem.version=V134_VERSION;
window.ChromeRequiem.modules.LivingStreetsV134={
 events:V134_STREET_EVENTS,interactables:V134_INTERACTABLE_TYPES,profiles:V134_DISTRICT_STREET_PROFILES,
 ensure:ensureLivingStreetsStateV134,director:runEncounterDirectorV134,actors:ensureStreetActorsV134,diagnostics:runDiagnosticsV134
};
ensureLivingStreetsStateV134();ensureV134UI();
})();
}



const livingCallV14=(name,...args)=>{
 const fn=globalThis[name];
 if(typeof fn!=='function')throw new Error(`LivingStreetsV14 missing legacy implementation: ${name}`);
 return fn(...args);
};
const LivingStreetsV14=Object.freeze({
 version:'13.4A',
 get events(){return globalThis.V134_STREET_EVENTS},
 get interactableTypes(){return globalThis.V134_INTERACTABLE_TYPES},
 get notorietyPressure(){return globalThis.V134_NOTORIETY_PRESSURE},
 ensureState:(...args)=>livingCallV14('ensureLivingStreetsStateV134',...args),
 ensureNeighborhoodState:(...args)=>livingCallV14('ensureNeighborhoodStateV134',...args),
 ensureActors:(...args)=>livingCallV14('ensureStreetActorsV134',...args),
 ensureInteractables:(...args)=>livingCallV14('ensureInteractablesV134',...args),
 runEncounterDirector:(...args)=>livingCallV14('runEncounterDirectorV134',...args),
 handleTap:(...args)=>livingCallV14('handleLivingStreetTapV134',...args),
 onStreetStep:(...args)=>livingCallV14('onStreetStepV134',...args),
 restore:(...args)=>livingCallV14('restoreLivingStreetsV134',...args),
 diagnostics:(...args)=>livingCallV14('runDiagnosticsV134',...args)
});
globalThis.ChromeRequiemV14Domains ||= {};
globalThis.ChromeRequiemV14Domains.world ||= {};
globalThis.ChromeRequiemV14Domains.world.livingStreets=LivingStreetsV14;
