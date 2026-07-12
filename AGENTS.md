# AGENTS.md

Guidance for an AI agent (or engineer) working in **`hlsBs-examples`**.

Read this before you touch anything. This repository is a **tutorial**: six worked
examples (`ex0`–`ex5`) of increasing complexity that teach the SLAC **hlsBs** HLS
build system. Unlike `vitis-unified-hls-python-cli-dev` and `simple-hlsBs-example`
(which are `make`-driven, single-target templates), hlsBs here is driven by the
**`hlsRun` CLI + a Python project file**, and each example can emit **many**
components at once. The build engine lives in the shared `ruckus` submodule and is
**reused, never rewritten** per example.

The full reference lives at `firmware/submodules/ruckus/vitis/hlsBs/README.md`; the
tutorial narrative is `README.md`.

---

## 1. What this repository is

- A teaching set of hlsBs projects sharing one design (`firmware/src/streams/`,
  `firmware/include/`) driven by six project files, `firmware/ex*/project/Streams.py`.
- Each `Streams.py` declares a **cartesian product** of components. Complexity grows:

  | Ex | Adds | Components |
  |----|------|-----------|
  | ex0 | the basics (1 build × 1 FPGA) | 1 |
  | ex1 | a 2nd FPGA (clock) | 2 |
  | ex2 | 2 builds × 2 FPGAs | 4 |
  | ex3 | `#include` wildcarding (`Product.Files`) | 4 |
  | ex4 | `#define` values (`Product.Values`) | 4 |
  | ex5 | wildcard `#include` + `#define` combined | 8 |

- The heavy lifting (workspace/cfg/component creation, csim, synth, cosim, package,
  impl, IP family augmentation, DCP rename) is the `vitispy` engine in the `ruckus`
  submodule (`firmware/submodules/ruckus/vitis/hlsBs/`), shared across many SLAC repos.

---

## 2. Separation of steering from engine

| Kind | Where | Who edits it | Purpose |
|------|-------|--------------|---------|
| **Steering** | `firmware/ex*/project/<name>.py` | You, per example | Declare *what* to build (sources, includes, defines, FPGAs, name templates, IP). |
| **Design source** | `firmware/src/streams/*.cc`, `firmware/include/**` | You (shared) | The HLS C++ (`StreamsHls.cc`), the C testbench (`StreamsTb.cc`), headers, seed files. |
| **Reusable engine** | `firmware/submodules/ruckus/vitis/hlsBs/` (submodule) | Nobody, per example — shared/upstream | *How* to build. Reused verbatim. |
| **Generated** | `firmware/ex*/build/`, `firmware/ex*/ip/` | Nobody — produced by the build | Workspace + cfg + DCP logs in `build/`; packaged IP (`.zip`/`.dcp`) in `ip/`. |

- **Treat `firmware/submodules/ruckus/` as read-only shared code.** If the *engine*
  has a bug or missing feature, that is a separate, deliberate change routed
  **upstream to slaclab/ruckus** — not part of editing an example.
- The project file is the single source of truth for an example's synthesis
  parameters; hlsBs generates the per-component Vitis `.cfg` from it.

---

## 3. The workflow (hlsRun CLI — not `make`)

One-time per login (site/project setup; these carry absolute paths so they are
*documented*, not shipped — see `README.md`):

```bash
hlsLocate                # export HLSBS_XILINX_SETUP=<xilinx install root>
source firmware/scripts/setup_env.sh   # sources ruckus setup_hls.sh, defines exSelect
hlsVersion 2025.1        # select the Vitis version
exSelect ex0             # pick which example (sets HLSBS_PROJECT)
```

Per project / structural change, then day-to-day:

```bash
hlsWs  --create          # create the workspace   (<ex>/build/)
hlsCfg --create          # generate cfg + components
hlsRun --all             # csim -> synth -> cosim -> package -> impl -> ip
# or stages: hlsRun --csim=m,r | --synthesis | --cosim | --package | --implementation | --ip
```

Outputs: `<ex>/ip/<component>.zip` and `<component>.dcp`; the Vitis workspace and the
generated `.cfg` live in `<ex>/build/` (DCP journal/log under `<ex>/build/dgn/`).

---

## 4. Project-file API (what a `Streams.py` declares)

`get_products(project)` returns a `Product(project, targets, package, vivado)`:
- **build dict** — `top` (HLS top function, here `doit`), `tb`/`syn` lists of
  `{files, includes[, defines]}`, `csim_argv`, `cosim_argv`.
- **includes** — `{'paths', 'type': 'rel_path'|'abs_path'}` (the key must be present;
  may be an empty list).
- **defines** — `{'name','type':'flag'|'string'|'rel_path'|'abs_file','value'[, 'rel_path']}`.
- **FPGAs** — `Product.Fpga(part, clock, uncertainty, id)`.
- **components** — cartesian bind of `Product.Builds` + `Product.Fpgas` and (advanced)
  `Product.Files` (glob `#include`s) / `Product.Values` (`#define` sweeps). Every class
  **prefix** must be unique.
- **name templates** — `ConfigurationName` and `ComponentName`. The cfg template must be
  unique across every class with more than one member (use `{build_id}`, `{fpga_id}`,
  `{seed_name}`, `{def_seed}`, …).
- **package/vivado** — `Product.Package.Ip/Output`, `Product.Vivado(flow, syn_dcp)`.

`get_ip(project)` returns `project.Ip(dir, zip_file, family[, dgn_dir, …])` controlling
the IP family augmentation (`family` = comma-separated list) and DCP rename.

`get_project_root` / `get_products_root` may be omitted / `return None` to accept
defaults. `get_workspace` is overridden here to `<ex>/build/`.

---

## 5. Conventions & invariants (keep these true)

- **Output layout:** workspace + cfg in `<ex>/build/`, packaged IP in `<ex>/ip/`,
  DCP logs in `<ex>/build/dgn/`. `build*` and `.Xil*` are git-ignored.
- **Unique class prefixes** and a cfg template unique across every multi-member class.
- **Shared design source** lives in `firmware/src/streams/` and `firmware/include/`;
  examples reference it via `os.path.join(project.root, '../...')`.
- **Testbench exit code is the verdict** (0 = pass); the C testbench is self-checking
  and reads `#define`/`#include` seeds so ex3–ex5 need no code edits.
- **License header** on every source file.
- **Do not launch long synthesis without the user being aware** — `hlsRun --all` across
  every component of an example can take many minutes (ex5 = 8 components). Offer
  `hlsRun --csim=m,r` for a fast algorithm check.
- **Do not stage files or make git commits unless explicitly asked.**

---

## 6. Related repos

- `simple-hlsBs-example` — the minimal, `make`-driven, single-target on-ramp to hlsBs.
- `vitis-unified-hls-python-cli-dev` — the `make` + `hls_config.cfg` template these
  examples' conventions are aligned with.

*If you remember one thing: an example = a `project/<name>.py` descriptor over shared
`src/`+`include/` and the shared ruckus/hlsBs engine, run with `hlsRun`. Keep edits in
the example's project file and shared sources — never in the submodule.*
