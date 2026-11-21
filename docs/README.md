# docs/

Things to open in a browser. Nothing here is graded and nothing here runs your
game &mdash; double-click a file and read it.

| File | What it is |
|---|---|
| `week07_refactor.html` | **The Week 7 refactor, shown.** Ten blocks of this game before and after, side by side, with the block lit in both places and the one line left behind where it used to be. Each one names what had to go in as a parameter and what had to come out as a return. |
| `week10_data.html` | **The Week 10 reshape, stepped.** One step per TODO, in the order the week asks for them, and the arrow walks each step ONE LINE AT A TIME with a note saying what that line is for. Under every pair: the shape it was, the shape it becomes, and the one thing the old shape could not do. |

## For the instructor

Both pages are **generated** &mdash; do not hand-edit either:

```
python Scripts/build_refactor_viewer.py      # Week 7, from the real game files
python Scripts/test_refactor_viewer.py       # 187 checks against both sources
python Scripts/sabotage_refactor_viewer.py   # and that that harness fails closed

python Scripts/build_week10_viewer.py        # Week 10, same idea
python Scripts/test_week10_viewer.py         # every drawn line, and TODO coverage
node   Scripts/test_week10_render.js         # and that the page actually draws
```

Every chunk in either page is sliced at build time out of two real game files,
so the code shown is the code students actually have. The harnesses re-check
that every line still matches both sources and refuse a page that has been
hand-edited.

Week 7's slices come from `solutions/week06_game.py` and the Week 7 answer.
Week 10's come from `solutions/week09_game.py` &mdash; the answer that ships
this week, so the left pane is a file students hold &mdash; and the Week 10
answer. Its harness also checks the mapping **both ways**: every step names a
TODO the skeleton really has, and every TODO that changes the program is shown
by some step, in the skeleton's own order.

> **Keep the page matched to the released skeleton.** `week10_data.html` is
> built against the skeleton students actually received, not against a newer
> working copy. A page showing a TODO their instructions do not have is worse
> than no page: it was rebuilt from `origin/main` for exactly this reason
> after the working copy had moved on.

Neither is a stepper in the running sense. The steppers elsewhere in the
course walk a program *executing*; these show a program being *reshaped*
&mdash; Week 7 the shape of the file, Week 10 the shape of the data. Nothing
in either one runs.
