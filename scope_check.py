"""Find functions that use game state they were never given.

This is the fault class behind Week 12's whole repair session. Two shapes:

    health -= health_loss        inside a function that has no `health`
                                 parameter -> UnboundLocalError, every time

    show_day_status(day, health, ...)   inside a function that has no
                                        `health` parameter -> works silently,
                                        reading whatever module level holds

Both are the same mistake. Only the first one tells you. This finds both.

    python scope_check.py game.py

A name is reported when a function reads or writes it, the function does not
declare it as a parameter or assign it locally, and module level holds it as
a plain variable -- not a def, not an ALL_CAPS constant, not an import. Those
three are the legitimate reasons to reach outward; game state is not.
"""
import ast
import io
import sys


def module_state(tree):
    """Names assigned at module level that are not constants or imports."""
    state, funcs, consts, imports = set(), set(), set(), set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs.add(node.name)
        elif isinstance(node, ast.ClassDef):
            funcs.add(node.name)
        elif isinstance(node, ast.Import):
            for a in node.names:
                imports.add((a.asname or a.name).split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for a in node.names:
                imports.add(a.asname or a.name)
    # assignments anywhere at module level, including inside the main loop
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        for t in ([node.target] if isinstance(node, (ast.AugAssign, ast.AnnAssign))
                  else node.targets if isinstance(node, ast.Assign) else []):
            for n in ast.walk(t):
                if isinstance(n, ast.Name):
                    (consts if n.id.isupper() else state).add(n.id)
    return state - funcs - consts - imports, funcs | consts | imports


def params_of(fn):
    """Just the parameters -- these are the names that arrive bound."""
    a = fn.args
    names = {p.arg for p in a.posonlyargs + a.args + a.kwonlyargs}
    for extra in (a.vararg, a.kwarg):
        if extra:
            names.add(extra.arg)
    return names


def unbound_risks(fn, assigned, state):
    """Names the function ASSIGNS, that shadow module state, and are READ first.

    `health -= loss` with no `health` parameter is the whole Week 12 crash:
    the augmented assignment makes `health` local for the entire function, so
    its own right-hand side has nothing to read. Python raises
    UnboundLocalError every single time this line runs.

    `assigned` is the names bound inside the body, parameters excluded -- a
    parameter arrives with a value, so it can never be unbound. A name that
    is only ever read is not here either; that one resolves to module level
    and is the silent half of the fault, reported separately.
    """
    aug_targets = {id(n.target) for n in ast.walk(fn)
                   if isinstance(n, ast.AugAssign) and isinstance(n.target, ast.Name)}
    first = {}
    for node in ast.walk(fn):
        if not isinstance(node, ast.Name) or node.id not in assigned:
            continue
        if node.id not in state:
            continue
        key = (node.lineno, node.col_offset)
        if node.id not in first or key < first[node.id][0]:
            reads = isinstance(node.ctx, ast.Load) or id(node) in aug_targets
            first[node.id] = (key, reads)
    return {n: pos[0] for n, (pos, reads) in first.items() if reads}


def locals_of(fn):
    """Parameters plus every name the function assigns, binds or imports."""
    names = params_of(fn)
    for node in ast.walk(fn):
        if node is fn:
            continue
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names.add(node.name)
            continue
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            names.add(node.id)
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            names.update(node.names)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for al in node.names:
                names.add((al.asname or al.name).split(".")[0])
        elif isinstance(node, ast.ExceptHandler) and node.name:
            names.add(node.name)
        elif isinstance(node, (ast.comprehension,)):
            for n in ast.walk(node.target):
                if isinstance(n, ast.Name):
                    names.add(n.id)
    return names


def check(path):
    src = io.open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    state, allowed = module_state(tree)

    findings = []
    for fn in [n for n in ast.walk(tree)
               if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
        mine = locals_of(fn)
        params = params_of(fn)
        seen = {}
        for node in ast.walk(fn):
            if isinstance(node, ast.Name) and node.id in state and node.id not in mine:
                writes = not isinstance(node.ctx, ast.Load)
                if node.id not in seen or writes:
                    seen[node.id] = (node.lineno, "reads")
        for name, line in unbound_risks(fn, mine - params, state).items():
            seen[name] = (line, "unbound")
        for name, (line, kind) in sorted(seen.items(), key=lambda kv: kv[1][0]):
            findings.append((fn.lineno, fn.name, name, line, kind))

    if not findings:
        print("  ok -- no function reaches for game state it was not given")
        return 0

    print("  %d function(s) use state they were never given:\n" % len(
        {f[1] for f in findings}))
    last = None
    for fnline, fnname, name, line, kind in findings:
        if fnname != last:
            print("  %s()  line %d" % (fnname, fnline))
            last = fnname
        note = "CRASHES -> UnboundLocalError every time" if kind == "unbound" else \
               "reads   -> silent, works by accident"
        print("      %-10s line %-5d %s" % (name, line, note))
    print("\n  Fix: take it as a parameter. If the function changes it,")
    print("  `return` it too, and have the caller catch the result.")
    return 1


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "game.py"
    print("\n  scope_check: %s\n" % target)
    sys.exit(check(target))
