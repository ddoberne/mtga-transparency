class Event:
  def __init__(self, rounds, win_thresh = 500, loss_thresh = 500, bo1 = True):
    self.rounds = rounds
    self.win_thresh = win_thresh
    self.loss_thresh = loss_thresh
    self.bo1 = bo1

  def get_distributions(self, winrate, simplify_results = False):
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
          new_results[new_key] = {"wins": wins, "losses": losses + 1, "distribution": 0.0, "eliminated": losses + 1 >= self.loss_thresh}
        new_results[new_key]["distribution"] += results[key]["distribution"] * (1 - winrate)

        # If win
        new_key = f"{wins + 1}-{losses}"
        if new_key not in new_results.keys():
          new_results[new_key] = {"wins": wins + 1, "losses": losses, "distribution": 0.0, "eliminated": wins + 1 >= self.win_thresh}
        new_results[new_key]["distribution"] += results[key]["distribution"] * winrate

      results = new_results
    results.pop("void", None)
    if simplify_results:
      for key in results:
        results[key] = results[key]["distribution"]
    return results
