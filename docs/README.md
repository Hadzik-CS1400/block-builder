# docs/

Things to open in a browser. Nothing here is graded and nothing here runs your
game &mdash; double-click a file and read it.

| File | What it is |
|---|---|
| `week07_refactor.html` | **The Week 7 refactor, shown.** Ten blocks of this game before and after, side by side, with the block lit in both places and the one line left behind where it used to be. Each one names what had to go in as a parameter and what had to come out as a return. |
| `week10_data.html` | **The Week 10 reshape, stepped.** One step per TODO, in the skeleton's own order, each with the real lines from both game files side by side. Under every pair: the shape it was, the shape it becomes, and the one thing the old shape could not do. |

## For the instructor

Both pages are **generated** &mdash; do not hand-edit either:

```
python Scripts/build_refactor_viewer.py      # Week 7, from the real game files
python Scripts/test_refactor_viewer.py       # 187 checks against both sources
python Scripts/sabotage_refactor_viewer.py   # and that that harness fails closed

python Scripts/build_week10_viewer.py        # Week 10, same idea
python Scripts/test_week10_viewer.py         # every drawn line, and TODO coverage
```

Every chunk in either page is sliced at build time out of two real game files,
so the code shown is the code students actually have. The harnesses re-check
that every line still matches both sources and refuse a page that has been
hand-edited.

Week 7's slices come from `solutions/week06_game.py` and the Week 7 answer.
Week 10's come from the Week 9 answer and the Week 10 answer, and its harness
also checks the mapping **both ways**: every tab names a TODO the skeleton
really has, and every TODO that changes the program is shown by some tab. That
second direction is the one that earns its keep &mdash; it caught TODO 1c
shipping with no tab explaining it, which is the change the skeleton itself
calls the most common way to lose an hour that week.

Neither is a stepper. The steppers elsewhere in the course walk a program
*running*; these show a program being *reshaped* &mdash; Week 7 the shape of
the file, Week 10 the shape of the data. Nothing in either one executes.
