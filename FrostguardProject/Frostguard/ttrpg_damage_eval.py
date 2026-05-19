from collections import Counter
import numpy as np

# --- Define the dice ---
black  = [0,1,1,1,2,2]
blue   = [1,1,2,2,2,3]
orange = [1,2,2,3,3,4]

# --- Map ranks to dice pools ---
rank_to_dice = {
    0: [],
    1: [black],
    2: [blue],
    3: [black, black],
    4: [blue, black],
    5: [blue, blue],
    6: [blue, black, black],
    7: [blue, blue, black],
    8: [blue, blue, blue],
    9: [orange, blue, blue],
    10:[orange, orange, blue],
    11:[orange, orange, orange],  # 11+ treated same
}

# --- Helper to compute probability mass function of a dice pool ---
def pmf_of_sum(dice_lists):
    pmf = Counter({0: 1.0})
    for d in dice_lists:
        new = Counter()
        for s, p in pmf.items():
            for face in d:
                new[s + face] += p * (1/len(d))
        pmf = new
    total = sum(pmf.values())
    for k in pmf:
        pmf[k] /= total
    return dict(sorted(pmf.items()))

# --- Function to evaluate damage for a given rank and Block value ---
def evaluate_damage(rank, block):
    dice = rank_to_dice.get(rank, rank_to_dice[11])  # ranks >11 use 11
    pmf = pmf_of_sum(dice)
    vals = np.array(list(pmf.keys()))
    probs = np.array(list(pmf.values()))

    mean_raw = float((vals * probs).sum())
    std_raw = float(np.sqrt(((vals - mean_raw) ** 2 * probs).sum()))

    # Post-block expected damage
    expected_damage = float(((np.maximum(vals - block, 0)) * probs).sum())
    p_hit = float((vals > block).dot(probs))

    # Build damage distribution after block
    damage_dist = Counter()
    for v, p in pmf.items():
        dmg = max(v - block, 0)
        damage_dist[dmg] += p

    return {
        "Rank": rank,
        "Block": block,
        "Mean_raw": round(mean_raw, 3),
        "Std_raw": round(std_raw, 3),
        "Expected_damage": round(expected_damage, 3),
        "P_hit": round(p_hit, 3),
        "Distribution": {d: round(p, 4) for d, p in sorted(damage_dist.items())}
    }

# --- Example usage ---
if __name__ == "__main__":
    rank = 10
    block = 4
    result = evaluate_damage(rank, block)
    print("Rank {Rank} vs Block {Block}".format(**result))
    print("Raw mean:", result["Mean_raw"], "±", result["Std_raw"])
    print("Expected damage:", result["Expected_damage"])
    print("Probability of hitting:", result["P_hit"])
    print("Damage distribution:")
    for dmg, p in result["Distribution"].items():
        print(f"  {dmg}: {p*100:.1f}%")
