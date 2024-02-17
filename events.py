tab_name_d = {}
gem_prize_d = {}
pack_prize_d = {}
play_in_point_d = {}
entry_d = {}
round_d = {}
win_thresh_d = {}
loss_thresh_d = {}
bo1_d = {}
event_category_d = {}
coin_payout_d = {}

def populate(name, tab_name, gem_prizes, pack_prizes, play_in_points, entry_cost, rounds, win_thresh, loss_thresh, bo1, event_category, coin_payout = False):
    tab_name_d[name] = tab_name
    gem_prize_d[name] = gem_prizes
    pack_prize_d[name] = pack_prizes
    play_in_point_d[name] = play_in_points
    entry_d[name] = entry_cost
    round_d[name] = rounds
    win_thresh_d[name] = win_thresh
    loss_thresh_d[name] = loss_thresh
    bo1_d[name] = bo1
    event_category_d[name] = event_category
    coin_payout_d[name] = coin_payout

name = 'Bo1 Constr.'
tab_name = 'Bo1 Constructed'
gem_prizes = {0:25, 1:50, 2:75, 3:200, 4:300, 5:400, 6:450, 7:500}
pack_prizes = {0:0, 1:0, 2:1, 3:1, 4:1, 5:2, 6:2, 7:3}
play_in_points = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:3}
entry_cost = 375
rounds = 9
win_thresh = 7
loss_thresh = 3
bo1 = True
event_category = 'constructed'
coin_payout = False
populate(name, tab_name, gem_prizes, pack_prizes, play_in_points, entry_cost, rounds, win_thresh, loss_thresh, bo1, event_category, coin_payout)

name = 'Bo3 Constr.'
tab_name = 'Bo3 Constructed'
gem_prizes = {0:50, 1:100, 2:150, 3:600, 4:800, 5:1000}
pack_prizes = {0:1, 1:1, 2:2, 3:2, 4:2, 5:3}
play_in_points = {0:0, 1:0, 2:0, 3:0, 4:0, 5:4}
entry_cost = 750
rounds = 5
win_thresh = 5
loss_thresh = 5
bo1 = False
event_category = 'constructed'
coin_payout = False
populate(name, tab_name, gem_prizes, pack_prizes, play_in_points, entry_cost, rounds, win_thresh, loss_thresh, bo1, event_category, coin_payout)

name = 'Q. Draft'
tab_name = 'Quick Draft'
gem_prizes = {0:50, 1:100, 2:200, 3:300, 4:450, 5:650, 6:850, 7:950}
pack_prizes = {0:1.2, 1:1.22, 2:1.24, 3:1.26, 4:1.3, 5:1.35, 6:1.4, 7:2}
play_in_points = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
entry_cost = 750
rounds = 9
win_thresh = 7
loss_thresh = 3
bo1 = True
event_category = 'limited'
coin_payout = False
populate(name, tab_name, gem_prizes, pack_prizes, play_in_points, entry_cost, rounds, win_thresh, loss_thresh, bo1, event_category, coin_payout)

name = 'Tr. Draft'
tab_name = 'Traditional Draft'
gem_prizes = {0:100, 1:250, 2:1000, 3:2500}
pack_prizes = {0:1, 1:1, 2:3, 3:6}
play_in_points = {0:1, 1:0, 2:0, 3:2}
entry_cost = 1500
rounds = 3
win_thresh = 3
loss_thresh = 3
bo1 = False
event_category = 'limited'
coin_payout = False
populate(name, tab_name, gem_prizes, pack_prizes, play_in_points, entry_cost, rounds, win_thresh, loss_thresh, bo1, event_category, coin_payout)

name = 'Pr. Draft'
tab_name = 'Premier Draft'
gem_prizes = {0:50, 1:100, 2:250, 3:1000, 4:1400, 5:1600, 6:1800, 7:2200}
pack_prizes = {0:1, 1:1, 2:2, 3:2, 4:3, 5:4, 6:5, 7:6}
play_in_points = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
entry_cost = 1500
rounds = 9
win_thresh = 7
loss_thresh = 3
bo1 = True
event_category = 'limited'
coin_payout = False
populate(name, tab_name, gem_prizes, pack_prizes, play_in_points, entry_cost, rounds, win_thresh, loss_thresh, bo1, event_category, coin_payout)

name = 'Meta Challenge'
tab_name = 'Metagame Challenge'
gem_prizes = {0:500, 1:1000, 2:1500, 3:2000, 4:2500, 5:3000, 6:4000, 7:5000}
pack_prizes = {0:0, 1:0, 2:1, 3:3, 4:5, 5:10, 6:20, 7:30}
play_in_points = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
entry_cost = 400
rounds = 7
win_thresh = 7
loss_thresh = 1
bo1 = False
event_category = 'constructed'
coin_payout = True
populate(name, tab_name, gem_prizes, pack_prizes, play_in_points, entry_cost, rounds, win_thresh, loss_thresh, bo1, event_category, coin_payout)

name = 'Sealed'
tab_name = 'Sealed'
gem_prizes = {0:200, 1:400, 2:600, 3:1200, 4:1400, 5:1600, 6:2000, 7:2200}
pack_prizes = {0:3, 1:3, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3}
play_in_points = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
entry_cost = 2000
rounds = 9
win_thresh = 7
loss_thresh = 3
bo1 = True
event_category = 'limited'
coin_payout = False
populate(name, tab_name, gem_prizes, pack_prizes, play_in_points, entry_cost, rounds, win_thresh, loss_thresh, bo1, event_category, coin_payout)

name = 'Tr. Sealed'
tab_name = 'Traditional Sealed'
gem_prizes = {0:200, 1:500, 2:1200, 3:1800, 4:2200}
pack_prizes = {0:3, 1:3, 2:3, 3:3, 4:3}
play_in_points = {0:0, 1:0, 2:0, 3:0, 4:0}
entry_cost = 2000
rounds = 5
win_thresh = 4
loss_thresh = 2
bo1 = True
event_category = 'limited'
coin_payout = False
populate(name, tab_name, gem_prizes, pack_prizes, play_in_points, entry_cost, rounds, win_thresh, loss_thresh, bo1, event_category, coin_payout)

name = 'Bo1 Qual. (L)'
tab_name = 'Bo1 Qualifier Play-In (Limited)'
gem_prizes = {0:500 , 1:1000 , 2:1500, 3:3000, 4:4500, 5:6000, 6:6000 }
pack_prizes = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
play_in_points = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
entry_cost = 4000
rounds = 7
win_thresh = 6
loss_thresh = 2
bo1 = True
event_category ='limited'
coin_payout = False
populate(name, tab_name, gem_prizes, pack_prizes, play_in_points, entry_cost, rounds, win_thresh, loss_thresh, bo1, event_category, coin_payout)

name = 'Bo3 Qual. (L)'
tab_name = 'Bo3 Qualifier Play-In (Limited)'
gem_prizes = {0:500 , 1:2000 , 2:4500, 3:6000}
pack_prizes = {0:0, 1:0, 2:0, 3:0, 4:0}
play_in_points = {0:0, 1:0, 2:0, 3:0, 4:0}
entry_cost = 4000
rounds = 4
win_thresh = 4
loss_thresh = 1
bo1 = False
event_category ='limited'
coin_payout = False
populate(name, tab_name, gem_prizes, pack_prizes, play_in_points, entry_cost, rounds, win_thresh, loss_thresh, bo1, event_category, coin_payout)
