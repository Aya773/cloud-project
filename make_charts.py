import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("results_threaded.csv")
df["setup"] = df["setup"].map({"vm": "App on VM", "container": "Container"})
df["rss_mb"] = df["rss_kb"] / 1024

stats = df.groupby("setup").agg(
    startup_mean=("startup_ms", "mean"), startup_std=("startup_ms", "std"),
    rss_mean=("rss_mb", "mean"), rss_std=("rss_mb", "std"),
    rps_mean=("req_per_sec", "mean"), rps_std=("req_per_sec", "std"),
)
print(stats.round(2))

order = ["App on VM", "Container"]
colors = ["#4C72B0", "#DD8452"]

def bar(metric, ylabel, title, fname):
    m = stats.loc[order, metric + "_mean"]
    s = stats.loc[order, metric + "_std"]
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    ax.bar(order, m, yerr=s, capsize=5, color=colors)
    for i, name in enumerate(order):
        pts = df[df["setup"] == name]
        col = {"startup": "startup_ms", "rss": "rss_mb", "rps": "req_per_sec"}[metric]
        ax.scatter([i] * len(pts), pts[col], color="black", s=12, zorder=3)
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=9)
    fig.tight_layout()
    fig.savefig(fname, dpi=300)
    plt.close(fig)

bar("startup", "Startup time (ms)", "Time to first response", "chart_startup.png")
bar("rss", "Memory, RSS (MB)", "Idle memory of app process", "chart_memory.png")
bar("rps", "Requests per second", "Throughput (ab, 10 concurrent)", "chart_throughput.png")

boot = [155.67, 152.89, 153.99]
cont = df[df["setup"] == "Container"]["startup_ms"] / 1000
fig, ax = plt.subplots(figsize=(3.4, 2.6))
means = [sum(boot) / 3, cont.mean()]
ax.bar(["New VM boot", "Container start"], means, color=["#55A868", "#DD8452"])
ax.scatter([0] * 3, boot, color="black", s=12, zorder=3)
ax.scatter([1] * 3, cont, color="black", s=12, zorder=3)
ax.set_yscale("log")
ax.set_ylabel("Seconds (log scale)")
ax.set_title("VM boot vs. container start", fontsize=9)
fig.tight_layout()
fig.savefig("chart_boot.png", dpi=300)
print("Charts saved.")
