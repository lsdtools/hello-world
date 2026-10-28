# Hello World

The smallest complete LSD package, and a template to start yours from (**Use this template** on GitHub).

It shows the whole model in one file, `src/lsdtools_hello_world/tool.py`:

- a pipeline in three legs: `@tool.load` reads a CSV into a table, `@tool.shape` doubles its `x`
  column, and `@tool.deliver` returns a chart to show the result;
- `@tool.entity`, which wires the three legs into one node you can create, run and watch in LSD;
- `@tool.command`, a command line for the package;
- `@tool.view`, a panel docked in the sidebar.

## Try it

You need lsdtools (`pip install lsdtools`, then `lsdtools setup`).

```bash
lsdtools python src/lsdtools_hello_world/tool.py            # run the pipeline and print the table
lsdtools python src/lsdtools_hello_world/tool.py --window   # ...and open it in a window
lsdtools python tests/test_hello_world.py                    # the test
```

## Use it in LSD

```bash
lsdtools install -e .          # link this folder: edits apply on the next reload, nothing is copied
lsdtools new project my-project
lsdtools open my-project/project.lsd
```

Then enable **Hello World** in the project's Packages and create a **Hello World** node from the tree.

## Make it yours

1. Change `name` in `lsd_package.json` from `lsdtools/hello-world` to `<you>/<your-package>`. The import
   root follows the id, so rename `src/lsdtools_hello_world` to match (`<you>_<your_package>`), and the
   `Tool(...)` id at the top of `tool.py`.
2. Replace the three legs with your own load, shape and deliver steps.
3. Keep the test green: `lsdtools python tests/test_hello_world.py`.

## Files

| File | What it is |
|---|---|
| `lsd_package.json` | the manifest: the package id, its category, its tool and its dependencies |
| `src/lsdtools_hello_world/tool.py` | the package: steps, entity, command and view on one `tool` object |
| `tests/test_hello_world.py` | the pipeline run headless |
| `.vscode/` | run and debug the package from VS Code |
