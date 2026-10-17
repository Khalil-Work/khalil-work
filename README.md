### 👋 MOHAMMED AHMED

PhD researcher (@ UCAS) · Mechanical Engineer — **scientific computing, CFD,
heat transfer, and numerical verification.** I build small, tested solvers
and estimation tools where featured claims are checked against analytic
references and figures come from recorded runs.

---

## 🌀 Featured result — [Vortex Notebook](https://github.com/khalil-official/vortex-notebook)

<div align="center">
  <img src="https://raw.githubusercontent.com/khalil-official/vortex-notebook/main/docs/results/vorticity_evolution.gif" alt="Computed vorticity evolution from the Vortex Notebook spectral solver" width="640">
</div>

<p align="center"><sub>Recorded from the computed nonlinear run (N = 128,
ν = 5e-4 m²/s, 41 frames): strictly de-aliased 2D spectral Navier–Stokes.
Taylor–Green verification error sits at the floating-point roundoff floor
(1.3e-15); RK4 convergence order measured at 4.03–4.12; the nonlinear
operator matches an independent 3/2-rule padded reference to 1e-12.</sub></p>

- ▶ [Executable Jupyter guide](https://github.com/khalil-official/vortex-notebook/blob/main/docs/vortex_notebook.ipynb) — derivations + live verification cases
- 🔬 [Numerical evidence](https://github.com/khalil-official/vortex-notebook/blob/main/docs/verification.md) — what each of the 12 tests does and does not establish
- ⚡ Quick start: `pip install -r requirements-dev.txt && python -m pytest tests -q`

**Also verified:** [Shockline](https://github.com/khalil-official/shockline-euler)
— conservative 1D Euler waves (first-order Rusanov + second-order
MUSCL/SSP-RK3) against an exact Newton-iteration Riemann solver: exact
advected-contact convergence orders 1 and 2 through N=800, published Sod
star state to 5e-5, 11 tests + CI, and a 41-frame computed shock-tube
animation ([results](https://github.com/khalil-official/shockline-euler/blob/main/docs/verification.md)).

**Also verified:** [Droplet Journey](https://github.com/khalil-official/droplet-journey)
— 0-D droplet evaporation and heating with the Spalding d²-law, correct
sphere-area lumped heating, and documented threshold stops: frozen-state
d² validation to 1.7e-16, agreement with an independent tight-tolerance
reference below 1e-7, 10 tests + CI, and a 41-frame dense-sampled
animation ([results](https://github.com/khalil-official/droplet-journey/blob/main/docs/verification.md)).

## 📐 Verified original projects

| Project | What it is | Evidence |
| --- | --- | --- |
| [Vortex Notebook](https://github.com/khalil-official/vortex-notebook) | 2D spectral Navier–Stokes (vorticity–streamfunction, strict 2/3-rule, RK4) + executed notebook | 12 tests; roundoff-floor Taylor–Green; padded-reference alias check |
| [Shockline](https://github.com/khalil-official/shockline-euler) | Conservative 1D Euler finite-volume solvers with exact Riemann benchmarks | 11 tests; contact-convergence orders 1 & 2; 41-frame animation |
| [Droplet Journey](https://github.com/khalil-official/droplet-journey) | 0-D droplet evaporation and heating with physical stopping events | 10 tests; roundoff-floor d² law; independent reference; 41-frame animation |

*(This index grows as additional original projects complete review — more
are in progress.)*

## 🤝 Contributions and bug reports

The featured verified originals above ship reproduction commands, pinned
dependencies, recorded result data, and CI — if one of them does not
reproduce for you, please open an issue with the exact command, your
runtime versions, and the observed vs. documented numbers; that is the
fastest path to a fix. Useful reports with a minimal reproducer are always
welcome.

## 📊 Community stats

<div align="center">

<img src="https://github-profile-repo.vercel.app/?username=khalil-official&theme=flat&no-frame=true&column=6&margin-w=12" alt="Community-generated public GitHub statistics" width="100%">

</div>

<p align="center"><sub>Community-generated public GitHub statistics from the
open-source <a href="https://github.com/ryo-ma/github-profile-trophy">github-profile-trophy</a>
service — not official GitHub awards, engineering-quality ratings, or
percentile ranks. Commit counts include the disclosed reconstructed calendar
records described in those repositories.</sub></p>

---

🔬 Links: [LinkedIn](https://www.linkedin.com/in/mohammed-khalil1/) ·
[YouTube](https://www.youtube.com/@MohammedKHALIIL)
