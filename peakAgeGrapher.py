# Noah Purcell
# Plots peak age data for hr, obp, slg

import readBatting
import peakAge
import matplotlib.pyplot as plt
from collections import Counter
    
def get_data():
    batters_df = readBatting.load_data()
    hr_ages = peakAge.getPeakAges(batters_df, "HR")
    obp_ages = peakAge.getPeakAges(batters_df, "OBP")
    slg_ages = peakAge.getPeakAges(batters_df, "SLG")
    return hr_ages, obp_ages, slg_ages

def plot_data():
    hr_ages, obp_ages, slg_ages = get_data()
    hr_hist = Counter(hr_ages)
    obp_hist = Counter(obp_ages)
    slg_hist = Counter(slg_ages)
   
    fig = plt.figure(figsize=(5,10))
    ax1 = fig.add_subplot(3,1,1)
    ax2 = fig.add_subplot(3,1,2)
    ax3 = fig.add_subplot(3,1,3)
    
    axes = [ax1,ax2,ax3]
    hists = [hr_hist, obp_hist, slg_hist]
    titles = ["HR", "OBP", "SLG"]
    colors = ["#ef4433","#3344ef", "#aaaaaa"] # mlbish colors
    for ax, hist, title, col in zip(axes, hists, titles, colors):
        ax.bar([age + 0.1 for age in hist.keys()],
                 hist.values(), color=col)
        ax.axis([19,42,0,275])
        ax.set_xlabel("Peak Age")
        ax.set_ylabel("Frequency")
        ax.set_xticks([i for i in range(19,43)])
        ax.set_title(title, loc="left", size=18, weight="semibold")
    plt.figtext(0.145,1,"MLB Peak Age Since 1955\n", fontsize=24, ha='left', weight="black")
    plt.figtext(0.145, 1.01, "Min. AB: 1500 career, 130 season", fontsize=15)
    fig.tight_layout()
    fig.subplots_adjust(top=.96)
    plt.savefig("mlbPeakAge.png", dpi=fig.dpi, bbox_inches='tight', pad_inches=0.5)


if __name__ == "__main__":
    plot_data()
