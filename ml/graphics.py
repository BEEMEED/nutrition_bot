import matplotlib.pyplot as plt

def photo_cal(days,calls,user_id):


    fig, ax = plt.subplots(figsize=(10, 4))
    bars = ax.bar(days, calls, width=0.6, color='#8A2BE2')
    ax.grid(False)
    ax.set_yticks(range(0, max(calls) + 200, 200))
    ax.tick_params(axis='y', which='both', left=False)
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='x', colors='white')
    for i, v in enumerate(calls):
        ax.text(i, v + 20, str(v), ha='center', va='bottom', color='white', fontsize=9)
    fig.patch.set_facecolor('#0F0F1A')
    ax.set_facecolor('#0F0F1A')

    plt.title("общая статистика каллорий", color='white', pad=20)

    plt.savefig(f"pidor_{user_id}.png", dpi=100, bbox_inches='tight')

    plt.close()
