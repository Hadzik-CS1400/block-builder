# docs/

Things to open in a browser. Nothing here is graded and nothing here runs your
game &mdash; double-click a file and read it.

| File | What it is |
|---|---|
| `week07_refactor.html` | **The Week 7 refactor, shown.** Six blocks of this game before and after, side by side, with the block lit in both places and the one line left behind where it used to be. Each one names what had to go in as a parameter and what had to come out as a return. |

## For the instructor

`week07_refactor.html` is **generated** &mdash; do not hand-edit it:

```
python Scripts/build_refactor_viewer.py      # rebuild from the real game files
python Scripts/test_refactor_viewer.py       # 187 checks against both sources
python Scripts/sabotage_refactor_viewer.py   # and that that harness fails closed
```

Every chunk in the page is sliced at build time out of
`solutions/week06_game.py` (the before) and the Week 7 answer (the after), so
the code shown is the code students actually have. The harness re-checks that
every line, every call site, every parameter and every return still matches
both files, and refuses a page that has been hand-edited.

It is deliberately **not** a stepper. The five steppers elsewhere in the course
walk a program *running*; this shows a program being *reshaped*, which is the
only thing Week 7 asks for.
