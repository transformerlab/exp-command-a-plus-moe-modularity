"""Paper figures (post-consolidation). Values trace to ../FINDINGS.md.
Run: python make_figures.py   (matplotlib + numpy only; no GPU/model needed)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

GREEN, AMBER, RED = "#27ae60", "#e8a33d", "#c0392b"

# ---- Fig 1: family separation, Qwen3 (positive control) vs Command A+ ----
labels = ["Qwen3-30B-A3B\n(positive control)", "Command A+\n(this work)"]
within = [0.60, 0.49]   # within-group top-set Jaccard (lang-lang)
cross = [0.19, 0.40]    # cross-group (lang-task / cap-lang)
gap = [0.41, 0.09]
x = np.arange(2); w = 0.35
fig, ax = plt.subplots(figsize=(5.2, 3.8))
ax.bar(x - w/2, within, w, label="within-group (lang-lang)", color="#2980b9")
ax.bar(x + w/2, cross, w, label="cross-group (lang-task / cap-lang)", color="#e67e22")
for i in range(2):
    ax.annotate(f"gap={gap[i]:.2f}", (x[i], max(within[i], cross[i]) + 0.03), ha="center",
                fontsize=9, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(labels); ax.set_ylabel("top-set expert Jaccard")
ax.set_ylim(0, 0.75); ax.set_title("Family separation: clean in Qwen3, absent in Command A+")
ax.legend(fontsize=8); ax.grid(alpha=0.3, axis="y")
fig.tight_layout(); fig.savefig("fig1_separation.png", dpi=150); plt.close(fig)

# ---- Fig 2: selectivity scatter (on-target vs worst off-target; below y=x/3 = selective) ----
# (family, on-target NLL increase, worst off-target, verdict-color)  [consolidation 1f061675]
fams = [("ar", 1.80, 0.43, GREEN), ("es", 1.29, 0.43, AMBER), ("zh", 0.63, 0.37, RED),
        ("math", 0.37, 0.08, AMBER), ("code", 0.49, 0.17, RED), ("general", 0.10, 0.07, RED)]
fig, ax = plt.subplots(figsize=(5.4, 4.2))
xs = np.linspace(0, 2.0, 100)
ax.plot(xs, xs/3.0, "--", color="gray", label=r"selectivity bound $y=x/3$")
ax.fill_between(xs, 0, xs/3.0, color="#27ae60", alpha=0.06)
for name, on, off, c in fams:
    ax.scatter(on, off, s=90, color=c, edgecolor="black", zorder=3)
    ax.annotate(name, (on, off), textcoords="offset points", xytext=(7, 4), fontsize=10, fontweight="bold")
ax.set_xlabel("on-target effect (NLL increase)"); ax.set_ylabel("worst off-target effect (NLL increase)")
ax.set_xlim(0, 2.0); ax.set_ylim(0, 0.6)
ax.set_title("Selectivity: only Arabic sits clearly in the selective region")
hg = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=GREEN, markersize=9, label="modular (CI rule)"),
      plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=AMBER, markersize=9, label="boundary (point only)"),
      plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=RED, markersize=9, label="not modular"),
      plt.Line2D([0], [0], ls="--", color="gray", label=r"selectivity bound $y=x/3$")]
ax.legend(handles=hg, fontsize=8, loc="upper right")
ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("fig2_selectivity.png", dpi=150); plt.close(fig)

# ---- Fig 3: verdict depends on the measurement (heatmap) ----
# 0=no(red), 1=boundary(amber), 2=modular(green), nan=grey (metric had no power to test this cell)
GREY = "#9aa0a6"
NA = np.nan
rows = ["ar", "es", "zh", "math", "code", "general"]
cols = ["task\naccuracy", "passage / problem\nNLL", "indep-corpus /\nsolution NLL (CI)"]
M = np.array([
    [NA, 2, 2],   # ar:  accuracy = Belebele near-ceiling/low-power -> untestable, not a real null
    [NA, 2, 1],   # es
    [NA, 0, 0],   # zh
    [0, 0, 1],    # math
    [0, 0, 0],    # code
    [0, 0, 0],    # general
], dtype=float)
cmap = ListedColormap([RED, AMBER, GREEN]); cmap.set_bad(GREY)
fig, ax = plt.subplots(figsize=(6.6, 4.0))
ax.imshow(M, cmap=cmap, vmin=0, vmax=2, aspect="auto")
ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols, fontsize=9)
ax.set_yticks(range(len(rows))); ax.set_yticklabels(rows, fontsize=11)
txt = {0: "no", 1: "boundary", 2: "modular"}
for i in range(len(rows)):
    for j in range(len(cols)):
        v = M[i, j]
        label = "low power" if np.isnan(v) else txt[int(v)]
        ax.text(j, i, label, ha="center", va="center", color="white", fontsize=9, fontweight="bold")
ax.set_title("Modularity verdict depends on the measurement\n(only Arabic is modular wherever it can be tested)")
fig.tight_layout(); fig.savefig("fig3_metric_flip.png", dpi=150); plt.close(fig)

print("wrote fig1_separation.png, fig2_selectivity.png, fig3_metric_flip.png")
