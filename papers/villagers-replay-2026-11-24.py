#!/usr/bin/env python3
"""Replay the seven first lines of Villagers (24 November 2026).

Run with Python 3 and a checkout of EShapiro2/GLP at
17f0c0d3fd330f9576de9c38f1e6dcbc24a5a615:
  python3 villagers-replay-2026-11-24.py /path/to/GLP/calculus --output /new/directory

The optional, newly created output directory retains the generated contracts, tool
logs and exact diagnostic messages. The script never writes to the GLP checkout.
Tool faults are observations and are printed with their individual exit codes.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

# Table 1 and the order of the first lines in section 2.
GROUPS = {
    'Village Communication': [
        'Secure Friendship', 'Encounters', 'Groups', 'Feeds', 'Children'
    ],
    'Village Government': [
        'Democratic Community', 'Backed Community Bank', 'Disputes', 'Warnings'
    ],
    'Village Money': [
        'Community Bank', 'Mutual Credit', 'Joint Accounts'
    ],
    'Village Services': [
        'Community Market', 'Gigs', 'Rides', 'Lodging', 'Ads'
    ],
    'Village Life': [
        'Jobs', 'Help', 'Lending', 'Library', 'Lost and Found',
        'Carpool', 'Home Exchange', 'Partners', 'Dating'
    ],
    'Village Commons': [
        'Meeting Rooms', 'Appointments', 'Tennis Courts', 'Rehearsal Rooms'
    ],
}

# Tables 1 and 2 transcribed independently of the GLP catalogue.
PARENTS = """Secure Friendship = Friendship
Encounters = Knowledge
Groups = Friendship
Feeds = Labelled Overlay
Children = Warded Groups
Democratic Community = Community Bank|Constitution
Backed Community Bank = Community Bank
Disputes = Organisation
Warnings = Organisation
Community Bank = Bank
Mutual Credit = Bank
Joint Accounts = Coins
Community Market = Community Network|Overlay|Recommendations
Gigs = Community Network|Overlay|Recommendations
Rides = Community Network|Second-Score Auction
Lodging = Community Network|Overlay|Recommendations
Ads = Community Network|Overlay
Jobs = Free Matching
Help = Free Matching
Lending = Free Matching
Library = Knowledge
Lost and Found = Free Matching
Carpool = Free Matching
Home Exchange = Free Matching
Partners = Free Matching
Dating = Free Matching
Meeting Rooms = Booking
Appointments = Booking
Tennis Courts = Booking|Partners
Rehearsal Rooms = Booking|Partners
Knowledge =
Friendship = Knowledge
Guardians = Friendship
Warded Groups = Groups|Guardians
Services = Guardians
Rendezvous = Services
Anonymous Rendezvous = Rendezvous
Organisation = Guardians
Constitution = Organisation
Booking = Organisation
Notes = Knowledge
Coins = Notes
Bonds = Coins
Denominated Coins = Coins
Denominated Currencies = Bonds|Denominated Coins
Bank = Organisation|Denominated Currencies
Community Network = Backed Community Bank
Recommendations = Knowledge
Overlay = Friendship
Labelled Overlay = Overlay
Local Overlay = Overlay
Auction = Local Overlay
Second-Score Auction = Auction
Gossip = Friendship
Matching = Gossip
Anonymous Matching = Matching|Anonymous Rendezvous
Free Matching = Anonymous Matching"""


def slug(name):
    return name.replace(" ", "-")


def replay(catalogue, work):
    contracts = catalogue / "contracts"
    tools = work / "tools"
    shutil.copytree(catalogue / "tools", tools, ignore=shutil.ignore_patterns("__pycache__"))
    for folder in ("gr", "rev", "logs"):
        (work / folder).mkdir()
    shutil.copyfile(catalogue / "NAMES.txt", work / "NAMES.txt")
    sys.path.insert(0, str(tools))
    import derive

    published = derive.Deriver(str(contracts))
    parents = {}
    for line in PARENTS.splitlines():
        name, value = line.split("=", 1)
        parents[name.strip()] = value.strip().split("|") if value.strip() else []

    for name, listed in parents.items():
        actual = published.parents(name)
        if set(actual) != set(listed):
            raise ValueError(f"{name}: paper names {listed}, registry gives {actual}")
    facing = {name for group in GROUPS.values() for name in group}
    closure = facing.copy()
    pending = list(facing)
    while pending:
        for parent in parents[pending.pop()]:
            if parent not in closure:
                closure.add(parent)
                pending.append(parent)
    if closure != set(parents):
        raise ValueError(f"Catalogue closure differs: {closure.symmetric_difference(parents)}")
    print(f"{len(published.names)} catalogue contracts; {len(facing)} facing, "
          f"{len(closure - facing)} support, {sum(map(len, parents.values()))} direct parent references")
    for name in parents:
        for src, dest in (("logic-pragmas.txt", "gr"), ("contract.txt", "rev")):
            shutil.copyfile(contracts / slug(name) / src, work / dest / (slug(name) + ".txt"))
    wrappers = dict(GROUPS, Villagers=list(GROUPS))
    with (work / "NAMES.txt").open("a", encoding="utf-8") as registry:
        registry.write("\n")
        for name, parts in wrappers.items():
            key = slug(name)
            atom = key.lower().replace("-", "_")
            registry.write(f"{name} | {name} | {key} | {atom} | {atom}\n")
            statement = name + " unites " + ", ".join(parts[:-1]) + " and " + parts[-1] + "."
            for folder in ("gr", "rev"):
                (work / folder / (key + ".txt")).write_text(name + "\n" + statement + "\n")

    def run(tool, args, log_name):
        result = subprocess.run([sys.executable, "-I", str(tools / (tool + ".py")), *args],
                                cwd=work, text=True, capture_output=True)
        log = work / "logs" / log_name
        log.with_suffix(".stdout").write_text(result.stdout)
        log.with_suffix(".stderr").write_text(result.stderr)
        log.with_suffix(".exit").write_text(str(result.returncode) + "\n")
        return result

    expanded = run("expand", ["--out", str(work / "expanded.tex")], "expand")
    print("expand.py", expanded.returncode, expanded.stderr.strip(), sep="\n")
    schemas = run("gcsas", [], "gcsas")
    print("gcsas.py", schemas.returncode)
    print(next(line for line in schemas.stdout.splitlines() if "contracts," in line and "with a fault" in line))
    for name in parents:
        for folder, archived in (("sas", "schemas.txt"), ("sasx", "full-schemas.txt")):
            if (work / folder / (slug(name) + ".txt")).read_bytes() != (contracts / slug(name) / archived).read_bytes():
                raise ValueError(f"Control changed: {name} {archived}")
    print(f"All {2 * len(parents)} published schema files reproduced byte-for-byte.")
    derivation = work / "derivation.txt"
    first = work / "first-lines.txt"
    result = run("derive", [*wrappers, "--out", str(derivation), "--first-lines", str(first)], "derive")
    if result.returncode:
        raise RuntimeError(result.stderr)
    print(result.stdout.strip())
    proposed = {}
    for name, present, suggested in re.findall(r"^([^\n]+)\n    present:  ([^\n]+)\n    proposed: ([^\n]+)", first.read_text(), re.M):
        proposed[name] = present == suggested
    for name in wrappers:
        key = slug(name)
        checks = next(line for line in schemas.stdout.splitlines() if re.match(re.escape(name) + r"\s+commute", line))
        relation = run("relations", ["--json", name], key + "-relations")
        if relation.stdout.strip():
            row = json.loads(relation.stdout)[0]
            rel = "holds" if row["holds"] else f"{len(row['failures'])} differences"
        else:
            rel = relation.stderr.splitlines()[-1]
        term = run("toglp", [name], key + "-term")
        report = term.stderr.splitlines()[-1] if term.returncode else term.stdout.strip()
        print(f"{checks} | exact declaration {proposed[name]} | normalized relation {rel} | {report}")
    for name in ("Village Commons", "Villagers"):
        rule = next(line for line in (work / "sasx" / (slug(name) + ".txt")).read_text().splitlines()
                    if line.startswith("Booking:1") and " Book:" in line)
        print(name, rule, sep="\n")
    matching = [n for n in GROUPS["Village Life"] if n != "Library"]
    for names in (matching + ["Free Matching"], ["Booking", "Meeting Rooms", "Appointments"]):
        blobs = set()
        for name in names:
            data = (contracts / slug(name) / "term.glp.txt").read_bytes()
            blobs.add(hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest())
        print(f"{', '.join(names)}: {len(blobs)} distinct term(s) {', '.join(sorted(blobs))}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("calculus", type=Path, help="the calculus directory of the GLP checkout")
    p.add_argument("--output", type=Path, help="new directory in which to keep the generated evidence")
    args = p.parse_args()
    sys.dont_write_bytecode = True
    if args.output:
        args.output.mkdir(parents=True, exist_ok=False)
        replay(args.calculus.resolve(), args.output.resolve())
    else:
        with tempfile.TemporaryDirectory() as dest:
            replay(args.calculus.resolve(), Path(dest))


if __name__ == "__main__":
    main()
