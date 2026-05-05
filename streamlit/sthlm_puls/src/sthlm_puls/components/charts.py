import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties
import numpy as np
import pandas as pd
from sthlm_puls.utils.constants import COLORS


def plot_events_weather(df_merged: pd.DataFrame) -> plt.Figure:

    bar_colors = [
        COLORS["pink"] if row["temp_max"] == df_merged["temp_max"].max()
        else COLORS["gray_light"]
        for _, row in df_merged.iterrows()
    ]

    fig, ax = plt.subplots(figsize=(13, 6))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    x = np.arange(len(df_merged))
    ax.bar(x, df_merged["num_events"], color=bar_colors,
           width=0.6, edgecolor="none", zorder=2)

    emoji_font = FontProperties(family="Segoe UI Emoji")
    y_max = df_merged["num_events"].max()

    for i, row in df_merged.iterrows():
        ax.text(i, row["num_events"] + y_max * 0.06,
                row["icon"], ha="center", va="bottom",
                fontsize=14, fontproperties=emoji_font)
        ax.text(i, row["num_events"] + y_max * 0.16,
                f"{int(row['temp_max'])}°",
                ha="center", va="bottom", fontsize=8,
                color=COLORS["gray_2"])

    legend_items = [
        mpatches.Patch(color=COLORS["pink"], label="Warmest day"),
        mpatches.Patch(color=COLORS["gray_light"], label="Other days"),
    ]

    ax.legend(handles=legend_items, fontsize=8, frameon=False,
              labelcolor=COLORS["gray_3"], loc="upper left")

    ax.set_xticks(x)
    ax.set_xticklabels(df_merged["day_label"], fontsize=9, color=COLORS["gray_2"])
    ax.set_ylabel("Number of events", fontsize=9, color=COLORS["gray_2"])
    ax.yaxis.set_label_coords(-0.06, 0.8)
    ax.tick_params(axis="both", length=0, colors=COLORS["gray_2"])
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color(COLORS["gray_1"])
    ax.set_ylim(0, y_max * 1.55)
    ax.yaxis.grid(True, color=COLORS["gray_1"], linewidth=0.5, zorder=0)
    ax.set_axisbelow(True)
    ax.set_title(
        "This week's cultural events in Stockholm — pick the right day",
        loc="left", fontsize=12, fontweight="bold",
        color=COLORS["gray_3"], pad=20
    )
    ax.set_xlabel("Day", fontsize=9, color=COLORS["gray_2"])
    ax.xaxis.set_label_coords(0.06, -0.1)

    fig.tight_layout()
    return fig