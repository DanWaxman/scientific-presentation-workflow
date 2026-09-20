#!/usr/bin/env python3
"""Reproducible synthetic Bayesian regression gallery. MIT © 2026 Daniel Waxman.

    python code/generate_figures.py --compute --plot
    python code/generate_figures.py --plot       # uses only cached arrays

The model is y = intercept + slope*x + Normal(0, sigma²), with a N(0, I)
coefficient prior and known sigma. Bands are pointwise posterior credible
intervals for the latent regression mean, NOT observation predictive intervals.
Each animation frame uses only its displayed prefix of the observation order;
the conjugate posterior is recomputed analytically for each prefix in --compute.
The residual panel shows simulated noise y minus the known generating mean.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import re
from statistics import NormalDist

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import MaxNLocator
import numpy as np

from plot_style import STYLE_COLORS, apply_slide_style, add_nested_band
from plot_style import despine_curve_axis, save_figure, save_mp4

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "code" / "_cache" / "synthetic.npz"
FIGS = ROOT / "figs"
SEED = 2026
SCHEMA = 1
LEVELS = np.array([.95, .80, .50])


# BEGIN SLIDE EXCERPT
def posterior(X, y, sigma):
    precision = np.eye(2) + X.T @ X / sigma**2
    covariance = np.linalg.inv(precision)
    mean = covariance @ X.T @ y / sigma**2
    return mean, covariance
# END SLIDE EXCERPT


def compute() -> None:
    rng = np.random.default_rng(SEED)
    n, sigma = 24, .35
    x = rng.uniform(-1., 1., n)  # Acquisition order is independent of x.
    beta = np.array([.5, 1.4])
    X = np.column_stack((np.ones(n), x))
    y = X @ beta + rng.normal(0., sigma, n)
    grid = np.linspace(-1.1, 1.1, 221)
    G = np.column_stack((np.ones(grid.size), grid))
    means, covariances, curves, sds = [], [], [], []
    for k in range(n + 1):
        mean, covariance = posterior(X[:k], y[:k], sigma)
        means.append(mean)
        covariances.append(covariance)
        curves.append(G @ mean)
        sds.append(np.sqrt(np.einsum("ij,jk,ik->i", G, covariance, G)))
    z = np.array([NormalDist().inv_cdf((1 + p) / 2) for p in LEVELS])
    curves, sds = np.array(curves), np.array(sds)
    lower = curves[:, None, :] - z[None, :, None] * sds[:, None, :]
    upper = curves[:, None, :] + z[None, :, None] * sds[:, None, :]
    covariance = np.array(covariances)
    assert np.all(np.linalg.eigvalsh(covariance) > 0)
    assert np.all(np.diff(lower, axis=1) >= 0)
    assert np.all(np.diff(upper, axis=1) <= 0)
    provenance = {
        "schema": SCHEMA, "seed": SEED, "n_observations": n,
        "prior": "coefficients ~ N(0, I_2)", "known_noise_sd": sigma,
        "truth_coefficients": beta.tolist(), "levels": LEVELS.tolist(),
        "bands": "pointwise posterior credible intervals for the latent mean",
        "animation": "exact conjugate updates with only the displayed observation prefix",
        "numpy": np.__version__, "matplotlib": matplotlib.__version__,
    }
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(CACHE, schema=SCHEMA, x=x, y=y, sigma=sigma, grid=grid,
                        truth=G @ beta, residual=y-X @ beta, curves=curves,
                        lower=lower, upper=upper, coefficient_mean=np.array(means),
                        coefficient_covariance=covariance, levels=LEVELS, z=z,
                        provenance=json.dumps(provenance, indent=2))
    print(f"Computed {CACHE}")


def style_axis(ax, *, residual=False):
    despine_curve_axis(ax)
    ax.set(xlabel="$x$", xlim=(-1.1, 1.1))
    ax.xaxis.set_major_locator(MaxNLocator(4))
    ax.yaxis.set_major_locator(MaxNLocator(4))
    if residual:
        ax.set(ylabel="$y-f_\\star(x)$", ylim=(-1.1, 1.1))
    else:
        ax.set(ylabel="$y$", ylim=(-3.1, 3.1))


def update_code_excerpt() -> None:
    """Keep marked HTML code listings identical to the executable source."""
    source = Path(__file__).read_text(encoding="utf-8")
    excerpt = source.split("# BEGIN SLIDE EXCERPT\n", 1)[1].split(
        "# END SLIDE EXCERPT", 1)[0].rstrip()
    deck = ROOT / "index.html"
    if not deck.exists():
        return
    original = deck.read_text(encoding="utf-8")
    updated = re.sub(
        r'(<code\b[^>]*\bdata-code-source="posterior"[^>]*>).*?(</code>)',
        lambda match: match[1] + html.escape(excerpt) + match[2],
        original, flags=re.DOTALL,
    )
    if updated != original:
        deck.write_text(updated, encoding="utf-8")


def draw_regression(ax, data, count, *, legend=False):
    grid = data["grid"]
    add_nested_band(ax, grid, list(zip(data["lower"][count], data["upper"][count])),
                    color=STYLE_COLORS["dark_teal"])
    ax.plot(grid, data["truth"], "--", color=STYLE_COLORS["black"], lw=1.6,
            label="Truth")
    ax.plot(grid, data["curves"][count], color=STYLE_COLORS["dark_teal"],
            label="Posterior mean")
    ax.scatter(data["x"][:count], data["y"][:count], s=22, linewidths=0,
               color=STYLE_COLORS["neutral_gray"], alpha=.72, zorder=4,
               label="Observations")
    style_axis(ax)
    if legend:
        ax.legend(loc="upper left", ncol=1, fontsize=12, handlelength=1.7,
                  labelspacing=.25, borderaxespad=.15)


def plot() -> None:
    if not CACHE.exists():
        raise SystemExit("No synthetic cache found. Run --compute once before --plot.")
    with np.load(CACHE, allow_pickle=False) as source:
        data = {key: source[key] for key in source.files}
    if int(data["schema"]) != SCHEMA:
        raise SystemExit("Synthetic cache schema changed; rerun --compute.")
    update_code_excerpt()
    apply_slide_style(font_size=18)
    n = len(data["x"])
    fig, ax = plt.subplots(figsize=(4.3, 3.), layout="constrained")
    draw_regression(ax, data, n, legend=True)
    ax.set_ylim(-1.8, 2.9)
    save_figure(fig, FIGS / "regression", formats=("png", "svg"), tight=False)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(4.3, 3.), layout="constrained")
    noise_bands = [(-z * float(data["sigma"]) * np.ones_like(data["grid"]),
                    z * float(data["sigma"]) * np.ones_like(data["grid"]))
                   for z in data["z"]]
    add_nested_band(ax, data["grid"], noise_bands, color=STYLE_COLORS["purple"])
    ax.axhline(0., ls="--", color=STYLE_COLORS["black"], lw=1.6)
    ax.scatter(data["x"], data["residual"], s=23, linewidths=0,
               color=STYLE_COLORS["neutral_gray"], alpha=.8)
    style_axis(ax, residual=True)
    ax.text(.03, .97, "True noise: 95 / 80 / 50%", ha="left", va="top",
            transform=ax.transAxes, fontsize=11, color=STYLE_COLORS["neutral_gray"])
    save_figure(fig, FIGS / "residuals", formats=("png", "svg"), tight=False)
    plt.close(fig)

    # Fixed axes and one shared frame clock. Eight-second acquisition, then a
    # two-second final hold. HTML controls looping; --plot runs no inference.
    fig, ax = plt.subplots(figsize=(8.6, 3.4), layout="constrained")
    fps = 24
    frames = np.concatenate((np.floor(np.linspace(0, n, 8*fps)).astype(int),
                             np.full(2*fps, n)))

    def update(count):
        ax.clear()
        draw_regression(ax, data, int(count))
        ax.legend(loc="upper left", fontsize=12, ncol=3, handlelength=1.8)
        ax.text(.98, .06, f"Observations: {int(count)} / {n}", transform=ax.transAxes,
                ha="right", va="bottom", fontsize=14,
                color=STYLE_COLORS["neutral_gray"])
        return []

    update(0)
    save_figure(fig, FIGS / "animation-initial", formats=("png",), tight=False)
    update(n)
    save_figure(fig, FIGS / "animation-final", formats=("png",), tight=False)
    movie = FuncAnimation(fig, update, frames=frames, interval=1000/fps, blit=False)
    save_mp4(movie, FIGS / "animation.mp4", fps=fps, dpi=150)
    plt.close(fig)
    print(f"Rendered cached figures to {FIGS}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compute", action="store_true", help="Generate seeded data and exact posteriors")
    parser.add_argument("--plot", action="store_true", help="Render figures/video from cached arrays")
    args = parser.parse_args()
    if not args.compute and not args.plot:
        parser.error("Choose --compute, --plot, or both")
    if args.compute:
        compute()
    if args.plot:
        plot()


if __name__ == "__main__":
    main()
