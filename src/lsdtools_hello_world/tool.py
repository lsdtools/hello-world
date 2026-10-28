"""Hello World — an lsd tool package.

Author steps, an entity, commands, and views on one ``tool`` object. Run this file directly to test;
link the repository root (``lsd package link .``) to use it in LSD Desktop.

The FULL model in one file. A pipeline runs in three legs:

* ``@tool.load``    — takes a ``src: Source`` (the LOAD-in the framework injects) → a ``Table``;
* ``@tool.shape``   — one ``Table`` → another;
* ``@tool.deliver`` — ends it by **returning a** ``ViewerPayload`` (here a ``ChartPayload``) to SHOW a
  result; the framework persists it and routes it to any viewer (the DELIVER-out, symmetric to Source).

``@tool.entity`` wires the three legs into one creatable node. Then the headline: a ``View`` gets that
node's data through ONE verb — ``view.watch(entity)`` — and refreshes on every re-run. No hand-feeding;
the desktop's drag-and-drop and "Show in >" are just sugar over this same verb.
"""
from lsdtools import (
    ChartPayload, Context, Engine, Source, Table, Tool, View, action, param, views,
)

tool = Tool("lsdtools/hello-world", label="Hello World")


@tool.load
def rows(src: Source) -> Table:
    """LOAD leg: read the picked source into a Table (``src: Source`` is injected — file / sql / …)."""
    return src.read()


@tool.shape
def double(t: Table) -> Table:
    """SHAPE leg: double the ``x`` column — replace with your real transform."""
    return t.with_column("x", t["x"] * 2)


@tool.deliver
def chart(t: Table) -> ChartPayload:
    """DELIVER leg: return a payload to SHOW a result — the framework persists it and routes it to a
    viewer. (``LayerPayload`` for 3-D geometry, ``ChartPayload`` for a chart, ``LegendPayload`` for a
    legend; a plain deliver that only writes a file returns nothing.)"""
    ys = [r["x"] for r in t.to_pylist()]
    return ChartPayload(kind="bar", title="Hello World",
                        series=[{"name": "x", "x": list(range(len(ys))), "y": ys}])


@tool.entity(label="Hello World")
def dataset(src: str = ""):
    """A creatable entity: the load -> shape -> deliver pipeline wired into one node you run and watch."""
    return chart(t=double(t=rows(src=Source.file(src))))


@tool.command("run", help="Run the demo pipeline on a CSV and print the result")
def run(ctx: Context, src: str) -> int:
    Engine().run(double(t=rows(src=Source.file(src)))).print()
    return 0


class RunPanel(View):
    """A panel is a View: param() fields + @action operations, rendered in the UI or console."""

    src = param(str, default="", label="CSV path")

    @action(label="Watch it", style="suggested")
    def watch_it(self):
        # THE one verb: a table View holds the entity's output and refreshes on every re-run.
        entity, view = dataset(src=self.src), views.table(title="Hello World")
        engine = self.ctx.engine or Engine()
        engine.workspace.add(entity)
        engine.add(view)
        view.watch(entity)                 # any order works; also auto-pulls if already run
        engine.run_all()
        self.ctx.ui.notify(f"{view.title}: {len(entity.output)} rows")


@tool.view("lsdtools/hello-world.panel", title="Hello World", location="sidebar")
def panel(ctx: Context):
    return RunPanel()          # self.ctx is injected on mount — no manual wiring


if __name__ == "__main__":
    import os
    import sys
    import tempfile
    # A tiny CSV to feed the file-source load (real packages point at their own data).
    demo_csv = os.path.join(tempfile.mkdtemp(), "demo.csv")
    Table({"x": range(8)}).write_csv(demo_csv)

    engine = Engine()
    entity = dataset(src=demo_csv)                 # an entity — its verb is `run`
    view = views.table(title="Hello World")          # a data view — its verb is `show`
    engine.workspace.add(entity)
    engine.add(view)
    view.watch(entity)                             # THE one verb — any order works
    engine.run_all()                               # entity runs -> chart payload lands; view holds the table
    view.show(mode="window" if "--window" in sys.argv else "text")   # desktop opens a real window
