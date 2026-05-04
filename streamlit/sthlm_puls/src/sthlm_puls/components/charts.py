import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties
import numpy as np
import pandas as pd
from utils.constants.py import COLORS


def plot_events_weather(df_merged: pd.DataFrame) -> plt.Figure:
    """
    Bar chart showing number of events per day with weather icons and temperature.
    Highlights the best weather day.

    Args:
        df_merged: DataFrame with columns:
                   date, weathercode, temp_max, icon, day_label, antal_events
    Returns:
        matplotlib Figure
    """
    sunny  = df_merged["weathercode"].isin([0, 1, 2])
    rainy  = df_merged["weathercode"].isin([51, 67, 71, 80, 81, 82])

    bar_colors = [
        COLORS["blue_dark"] if (row["weathercode"] in [0, 1, 2] and row["temp_max"] >= 18)
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

    if sunny.any():
        idx = df_merged[sunny]["temp_max"].idxmax()
        ax.annotate(
            text="Sunny & warm —\nperfect for outdoor culture!",
            xy=(idx, df_merged.loc[idx, "num_events"]),
            xytext=(idx - 2.5, df_merged.loc[idx, "num_events"] + y_max * 0.4),
            fontsize=8, color=COLORS["gray_3"],
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.2",
                            linewidth=1.2, color=COLORS["blue_dark"])
        )

    if rainy.any():
        idx = df_merged[rainy]["num_events"].idxmax()
        ax.annotate(
            text="Rainy day —\ngreat time for a museum!",
            xy=(idx, df_merged.loc[idx, "num_events"]),
            xytext=(idx + 1.2, df_merged.loc[idx, "num_events"] + y_max * 0.35),
            fontsize=8, color=COLORS["gray_3"],
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.2",
                            linewidth=1.2, color=COLORS["gray_2"])
        )

    legend_items = [
        mpatches.Patch(color=COLORS["blue_dark"],  label="Best weather day"),
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