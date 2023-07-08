import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io

barWidth = 0.15
colors = ["#A4C2F4", "#FFD966", "#EA9999", "#8E7CC3", "#7CC3B2", "#B1C37C", "#F4A4EA", "#F4D6A4"]


def build_plot(plot_data, labels, xticks):
    fig = plt.subplots(figsize=(28, 18))
    initial_positions = np.arange(len(plot_data[0]))

    for i in range(len(plot_data)):
        bar_positions = [x + i * barWidth for x in initial_positions]
        plt.bar(bar_positions, plot_data[i], color=colors[i % len(colors)], width=barWidth, edgecolor='grey',
                label=labels[i])
    for i in range(len(plot_data)):
        for j in range(len(plot_data[i])):
            plt.text(j + i * barWidth, plot_data[i][j], plot_data[i][j],  ha = 'center', fontsize=24)
    plt.xlabel('Metrics', fontweight='bold', fontsize=24)
    plt.ylabel('Index', fontweight='bold', fontsize=24)
    plt.xticks(range(len(plot_data[0])), xticks, fontsize=24)
    plt.yticks(fontsize=24)
    plt.legend(fontsize=24)
    plt.title("DQL Index", fontsize=36)
    return plt


def build_stacked_bar_plot(plot_data, labels, xticks):
    fig, ax = plt.subplots(figsize=(50, 35))
    positions = np.arange(len(plot_data[0]))
    positions = [4 * i for i in positions]
    for i in range(len(plot_data)):
        bottom = 0 if i == 0 else plot_data[0] if i == 1 else np.add(bottom, plot_data[i - 1])
        ax.bar(positions, plot_data[i], 1, bottom=bottom, color=colors[i % len(colors)])

    plt.xlabel('Countries', fontweight='bold', fontsize=20)
    plt.ylabel('GQL Index', fontweight='bold', fontsize=20)
    plt.xticks(positions, xticks, rotation=90, fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(labels, fontsize="20",)
    plt.title("DQL Index", fontsize=36)
    return plt


def plot_to_img(plot):
    buf = io.BytesIO()
    plot.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img
