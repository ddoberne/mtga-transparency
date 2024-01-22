class Event:
  def __init__(self, rounds, elim_thresh, bo1):
    self.rounds = rounds
    self.elim_threshold = elim_thresh
    self.bo1 = bo1

  def get_distributions(self, winrate):
    if self.bo1 == False:
      winrate = (winrate ** 2) + (2 * winrate * winrate * (1 - winrate))
    results = {"0-0":{"wins": 0, "losses": 0, "distribution": 1.0, "eliminated": False}}
    for round in range(1, self.rounds + 1):
      new_results = {"void": 0}
      for key in results:
        if key == "void":
          continue

        # If eliminated, pass
        if results[key]["eliminated"]:
          new_results[key] = results[key]
          continue
        wins = results[key]["wins"]
        losses = results[key]["losses"]

        # If loss
        new_key = f"{wins}-{losses + 1}"
        if new_key not in new_results.keys():
          new_results[new_key] = {"wins": wins, "losses": losses + 1, "distribution": 0.0, "eliminated": losses >= self.elim_threshold}
        new_results[new_key]["distribution"] += results[key]["distribution"] * (1 - winrate)

        # If win
        new_key = f"{wins + 1}-{losses}"
        if new_key not in new_results.keys():
          new_results[new_key] = {"wins": wins + 1, "losses": losses, "distribution": 0.0, "eliminated": losses >= self.elim_threshold}
        new_results[new_key]["distribution"] += results[key]["distribution"] * winrate

      results = new_results
    results.pop("void", None)
    for key in results:
      results[key] = results[key]["distribution"]
    return results
