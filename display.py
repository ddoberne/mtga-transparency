import streamlit as st
import event
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import events


sns.set_theme()
st.set_page_config(layout="wide")
local_tax = st.sidebar.number_input(label = 'Local tax rate in %', value = 0.0, step = 1.0)

gem_bundle_prices_f = [round(x * (1 + local_tax / 100), 2) for x in (4.99, 9.99, 19.99, 49.99, 99.99)]
gem_bundle_index = {}
gem_bundle_prices_str = ["" for x in range(len(gem_bundle_prices_f))]
gem_bundle_count = (750, 1600, 3400, 9200, 20000)
gem_bundle_values = [0.0 for x in range(len(gem_bundle_prices_f))]
gems_per_usd = {}
for i in range(0, len(gem_bundle_prices_f)):
  gem_bundle_values[i] = gem_bundle_count[i]/gem_bundle_prices_f[i]
  gem_bundle_prices_str[i] = "$" + str(gem_bundle_prices_f[i]) + " → " + str(gem_bundle_count[i]) + "💎"
  gems_per_usd[gem_bundle_prices_str[i]] = gem_bundle_values[i]
  gem_bundle_index[gem_bundle_prices_str[i]] = i

user_bundle = st.sidebar.selectbox('Which bundle do you purchase?', gem_bundle_prices_str)

user_gems_per_usd = gems_per_usd[user_bundle]

st.sidebar.write(f'Each dollar buys you **{user_gems_per_usd:.0f}** 💎 which buys {user_gems_per_usd/200:.2f} packs in the store.')
same_winrate = st.sidebar.checkbox('Use same winrate for constructed and limited', value = True)
if same_winrate:
    user_winrate = st.sidebar.slider(label = 'Select game winrate (%):', min_value = 0, max_value = 100, value = 50, step = 1)/100.0
    limited_winrate = user_winrate
    st.sidebar.write(f'You win **{100 * ((user_winrate ** 2) + (2 * user_winrate * user_winrate * (1 - user_winrate))):.1f}%** of your Bo3s.')
else:
    user_winrate = st.sidebar.slider(label = 'Select constructed game winrate (%):', min_value = 0, max_value = 100, value = 50, step = 1)/100.0
    st.sidebar.write(f'You win **{100 * ((user_winrate ** 2) + (2 * user_winrate * user_winrate * (1 - user_winrate))):.1f}%** of your constructed Bo3s.')
    limited_winrate = st.sidebar.slider(label = 'Select limited game winrate (%):', min_value = 0, max_value = 100, value = 50, step = 1)/100.0
    st.sidebar.write(f'You win **{100 * ((limited_winrate ** 2) + (2 * limited_winrate * limited_winrate * (1 - limited_winrate))):.1f}%** of your limited Bo3s.')

value_pack_reward = st.sidebar.number_input(label = 'Perceived 💎 value of a pack:', min_value = 0, value = 100, step = 1)
st.sidebar.write(f'You value every pack at $**{value_pack_reward/user_gems_per_usd:.2f}**')
value_pack_draft = st.sidebar.number_input(label = 'Perceived 💎 value of a draft/sealed pack:', min_value = 0, value = 50, step = 1)
st.sidebar.write(f'You value every draft pack at $**{value_pack_draft/user_gems_per_usd:.2f}**')
value_play_in_point = st.sidebar.number_input(label = 'Perceived 💎 value of a play in point:', min_value = 0, value = 100, step = 1)
st.sidebar.write(f'You value every play in point at $**{value_play_in_point/user_gems_per_usd:.2f}**')

value_gold = st.sidebar.number_input(label = 'Perceived 💎 value of a single rewarded 🪙:', min_value = 0.0, value = 0.15, step = 0.01)
st.sidebar.write(f'You value 100 🪙 at $**{100 * value_gold/user_gems_per_usd:.2f}**')



aggregate = st.sidebar.checkbox('Aggregate results with same payouts', value = True)
show_default = st.sidebar.checkbox('Show default distribution', value = True)

all_events = [ 'Bo1 Constr.', 'Bo3 Constr.', 'Q. Draft', 'Tr. Draft', 'Pr. Draft', 'Pick 2 Draft', 'Meta Challenge', 'Sealed', 'Tr. Sealed', 'Bo1 Qual. (L)', 'Bo3 Qual. (L)', 'Cube', 'Tr. Cube', 'Direct Draft']#, 'Arena Open', 'Arena Open (Day 2 Only)']
current_events = []
current_events.append('Bo1 Constr.')
current_events.append('Bo3 Constr.')
current_events.append('Q. Draft')
current_events.append('Tr. Draft')
current_events.append('Pr. Draft')
current_events.append('Pick 2 Draft')

#current_events.append('Meta Challenge')
current_events.append('Sealed')
current_events.append('Tr. Sealed')
#current_events.append('Bo1 Qual. (L)')
#current_events.append('Bo3 Qual. (L)')

tab_names = st.sidebar.multiselect('Select events to compare:', options = all_events, default = current_events)

value_box = 0
if 'Direct Draft' in tab_names:
    value_box = st.sidebar.number_input(label='Perceived 💎 value of a play booster box:', min_value=0, value=20000, step=1)
    st.sidebar.write(f'You value a play booster box at $**{value_box / user_gems_per_usd:.2f}**')


st.sidebar.write()
st.sidebar.write('[GitHub source](https://github.com/ddoberne/mtga-transparency)')
st.sidebar.write()
st.sidebar.caption('This calculator assumes that your winrate does **not** change based on your event record, potentially causing overestimation of top-heavy event payouts.')
st.title("MTGA Cost Transparency Guide")
#st.write('Currently updating, check back later!')

tabs = st.tabs(tab_names)
tab_dict = {}
for i in range(len(tabs)):
  tab_dict[tab_names[i]] = tabs[i]

column_config = {'usd value': st.column_config.NumberColumn(label = None, format= "$%.2f"),
                 'games played': st.column_config.NumberColumn(label = "games played Ø", format= "%.2f"),
                 '% of results': st.column_config.ProgressColumn(label = None, format = '%.1f%%', min_value = 0, max_value = 100)}

summary = {}

def tab_info(tab_name, e, winrate, gem_prizes, pack_prizes, box_prices, play_in_points, aggregate, user_gems_per_usd, entry_cost, entry_cost_gold, packs_draft, packs_sealed, coin_payout = False, results_only = False):
  results = e.get_distributions(winrate, simplify_results = False)
  default_results = e.get_distributions(.5, simplify_results = False)
  df = pd.DataFrame(results).transpose()
  default_df = pd.DataFrame(default_results).transpose()
  x_axis = 'record'
  if aggregate:
    df['games played'] = df['games played'] * df['distribution']
    df = df.groupby('wins').sum()
    df['games played'] = (df['games played'] / df['distribution'].where(df['distribution'] != 0))
    df = df[['distribution','games played']]
    default_df = default_df.groupby('wins').sum()['distribution']
    x_axis = 'wins'
  df = df.reset_index()
  default_df = default_df.reset_index()
  df = df.rename(columns = {'index':'record'})
  default_df = default_df.rename(columns = {'index':'record'})
  df['% of results'] = df['distribution'] * 100
  default_df['% of results'] = default_df['distribution'] * 100
  df['gem payout'] = df['wins'].map(gem_prizes)
  df['pack prizes'] = df['wins'].map(pack_prizes)
  df['box prices'] = df['wins'].map(box_prices)
  df['play in points'] = df['wins'].map(play_in_points)
  df['usd value'] = df['gem payout'].apply(lambda x: x / user_gems_per_usd)
  df['usd value'] += df['play in points'] * 200 / user_gems_per_usd
  df['usd value'] += df['box prices'] * 125
  ev = 0
  pack_ev = 0
  ev_value = 0
  ev_play_in = 0
  ev_gold = 0
  ev_box = 0
  ev_played = (df['games played'] * df['distribution']).sum()
  for i in df.index:
    if not coin_payout:
        ev += df.loc[i, 'distribution'] * (df.loc[i, 'gem payout'])
    else:
        ev_gold += df.loc[i, 'distribution'] * (df.loc[i, 'gem payout'])
    pack_ev += df.loc[i, 'distribution'] * df.loc[i, 'pack prizes']
    ev_play_in += df.loc[i, 'distribution'] * df.loc[i, 'play in points']
    ev_box += df.loc[i, 'distribution'] * df.loc[i, 'box prices']
  ev_value += pack_ev * value_pack_reward
  ev_value += packs_draft * value_pack_draft
  ev_value += packs_sealed * value_pack_draft
  ev_value += ev_play_in * value_play_in_point
  ev_value += ev_gold * value_gold
  ev_value += ev_box * value_box
  ev_value += ev

  if coin_payout:
      df['gem payout'] = 0
  rake = entry_cost - ev
  gems_per_gold = ev/entry_cost_gold if entry_cost_gold > 0 and not coin_payout else np.nan
  gems_per_pack = rake/pack_ev if pack_ev > 0 else np.nan
  gold_per_pack = (entry_cost_gold - ev_gold) / pack_ev if pack_ev > 0 and entry_cost_gold > 0 else np.nan
  gem_cost_per_game = rake / ev_played
  summary[tab_name] = {'entry 🪙': entry_cost_gold if entry_cost_gold > 0 else np.nan,
                       'entry 💎': entry_cost,
                       '💎 return': ev,
                       '💎 return %': 100 * (1 - rake/entry_cost),
                       '💎 value': ev_value,
                       '💎 value %': 100 * (1 - (entry_cost - ev_value)/entry_cost),
                       '💎 loss in $': rake/user_gems_per_usd,
                       'value loss in $': (entry_cost - ev_value)/user_gems_per_usd,
                       'pack ev': pack_ev,
                       '💎 per pack': gems_per_pack,
                       '🪙 per pack': gold_per_pack,
                       '💎 per 🪙': gems_per_gold,
                       'box ev': ev_box,
                       'games ev': ev_played,
                       '💎 cost per game': gem_cost_per_game,
                       '$ cost per game': gem_cost_per_game / user_gems_per_usd,
                       'value loss per game': (entry_cost - ev_value) / ev_played}
  if results_only:
      return df
  fig, ax = plt.subplots(figsize = (8, 3))
  ax.plot(df[[x_axis, '% of results']].set_index(x_axis), 'o-b', linewidth = 3, label = f'{user_winrate * 100:.0f}% wr')
  if show_default and user_winrate != 0.5:
      ax.plot(default_df[[x_axis, '% of results']].set_index(x_axis), 'o-g', linewidth = 1, label = 'default(50% wr)')
      plt.legend()
  for x, y in zip(df[x_axis], df['% of results']):
    plt.text(x = x, y = y + 1, s = '{:.1f}%'.format(y), color = 'blue')
  ax.yaxis.set_major_formatter(mtick.PercentFormatter())
  ax.set_ylim(0, df['% of results'].max() + 5)
  plt.ylabel('% of results')
  plt.xlabel(x_axis)
  # Writing begins here
  st.header(f'{events.tab_name_d[tab_name]} prize distribution for a {user_winrate * 100:.0f}% winrate (Entry cost: {str(entry_cost_gold) + "🪙 or " if entry_cost_gold > 0 else ""}{entry_cost}💎 (${entry_cost/user_gems_per_usd:.2f}))')
  st.pyplot(fig)
  st.dataframe(df[[x_axis, '% of results', 'games played' ,'gem payout', 'pack prizes', 'box prices', 'play in points', 'usd value']], hide_index = True, width = 'stretch', column_config = column_config)
  if coin_payout:
      st.write(f'The expected payout for this event given a {winrate * 100:.0f}% winrate is **{ev_gold:.1f}** 🪙.')
  else:
    st.write(f'The expected payout for this event given a {winrate * 100:.0f}% winrate is **{ev:.1f}**💎.')
  if ev > entry_cost:
      st.write(f'On average you will play **{ev_played:.2f}** games **gaining** **{-gem_cost_per_game:.2f}**💎($**{(-gem_cost_per_game / user_gems_per_usd):.2f}**) per game')
  else:
      st.write(f'On average you will play **{ev_played:.2f}** games **costing** **{gem_cost_per_game:.2f}**💎($**{(gem_cost_per_game / user_gems_per_usd):.2f}**) per game')
  if coin_payout:
      rake_gold = entry_cost_gold - ev_gold
      if ev_gold > entry_cost_gold:
        st.write(f'That means an average **gain** of **{- rake_gold:.1f}**🪙 per event, or **{(- rake_gold) * 100.0/entry_cost_gold:.1f}%**')
      else:
        st.write(f'That means an average **loss** of **{rake_gold:.1f}**🪙 per event, or **{(rake_gold) * 100.0/entry_cost_gold:.1f}%**')
        efficiency = rake/pack_ev if pack_ev > 0 else 0
        if pack_ev > 0:
            st.write(f'This event converts **{pack_ev:.1f}**🪙 to **{pack_ev:.1f}** packs, with an efficiency of **{efficiency:.1f}**🪙 per pack.')
  else:
      if ev > entry_cost:
        st.write(f'That means an average **gain** of **{- rake:.1f}**💎 (**${-rake/user_gems_per_usd:.2f}**) per event, or **{(- rake) * 100.0/entry_cost:.1f}%**')
      else:
        st.write(f'That means an average **loss** of **{rake:.1f}**💎 (**${rake/user_gems_per_usd:.2f}**) per event, or **{(rake) * 100.0/entry_cost:.1f}%**')
        efficiency = rake/pack_ev if pack_ev > 0 else 0
        if pack_ev > 0:
            st.write(f'This event converts **{rake:.1f}**💎 to **{pack_ev:.1f}** packs, with an efficiency of **{efficiency:.1f}** gems per pack.')
  if entry_cost_gold > 0 and not coin_payout:
    st.write(f'This event can convert **{entry_cost_gold:.1f}**🪙 to **{ev:.1f}**💎 at a rate of **{gems_per_gold:.3f}** gems per gold.')
  if coin_payout:
      st.write(f'This event can convert **{entry_cost:.1f}**💎 to **{ev_gold:.1f}**🪙 at a rate of **{ev_gold/entry_cost:.1f}** gold per gem')
  if ev_box > 0:
      st.write(f'This event can convert **{entry_cost:.1f}**💎 to **{ev_box:.3f}** play booster boxes')
  if pack_ev > 0:
    st.write(f'The expected pack payout is **{pack_ev:.1f}** packs.')
  if ev_value > entry_cost:
    st.write(f'The perceived value **gain** of this event is **{ev_value - entry_cost:.1f}**💎 or **${(ev_value - entry_cost) / user_gems_per_usd:.1f}**')
  else:
    st.write(f'The perceived value **loss** of this event is **{entry_cost - ev_value:.1f}**💎 or **${(entry_cost - ev_value) / user_gems_per_usd:.1f}**')

for tab_name in tab_names:
    with tab_dict[tab_name]:
      gem_prizes = events.gem_prize_d[tab_name]
      pack_prizes = events.pack_prize_d[tab_name]
      box_prices = events.booster_box_price_d[tab_name]
      pack_draft = events.pack_draft_d[tab_name]
      pack_sealed = events.pack_sealed_d[tab_name]
      play_in_points = events.play_in_point_d[tab_name]
      entry_cost = events.entry_d[tab_name]
      entry_cost_gold = events.entry_coin_d[tab_name]
      coin_payout = events.coin_payout_d[tab_name]
      event_object = event.Event(rounds = events.round_d[tab_name], win_thresh = events.win_thresh_d[tab_name], loss_thresh = events.loss_thresh_d[tab_name],
                                 bo1 = events.bo1_d[tab_name])

      if events.event_category_d[tab_name] == 'constructed':
          winrate = user_winrate
      else:
          winrate = limited_winrate
      tab_info(tab_name, event_object, winrate, gem_prizes, pack_prizes, box_prices, play_in_points, aggregate, user_gems_per_usd, entry_cost, entry_cost_gold, pack_draft, pack_sealed, events.coin_payout_d[tab_name])


st.divider()
if same_winrate:
    st.header(f'Summary of events for {user_winrate * 100:.0f}% winrate')
else:
    st.header(f'Summary of events for {user_winrate * 100:.0f}% constructed and {limited_winrate * 100:.0f}% limited winrates')
summary_df = pd.DataFrame(summary).transpose().reset_index()
summary_df = summary_df.rename(columns = {'index': 'event name'})
summary_config = {'💎 loss in $': st.column_config.NumberColumn(label = None, format= "$%.2f"),
                  'value loss in $': st.column_config.NumberColumn(label = None, format= "$%.2f"),
                  '💎 return': st.column_config.NumberColumn(label = None, format = '%.1f'),
                  '💎 return %': st.column_config.ProgressColumn(label = None, format = '%.1f%%', min_value = 0, max_value = 100),
                  'pack ev': st.column_config.NumberColumn(label = None, format = '%.1f'),
                  '💎 per pack': st.column_config.NumberColumn(label = None, format = '%.1f'),
                  '🪙 per pack': st.column_config.NumberColumn(label=None, format='%.0f'),
                  '💎 per 🪙': st.column_config.NumberColumn(label = None, format = '%.3f'),
                  '💎 value': st.column_config.NumberColumn(label=None, format='%.1f'),
                  '💎 value %': st.column_config.ProgressColumn(label=None, format='%.1f%%', min_value=0, max_value=100),
                  '💎 cost per game': st.column_config.NumberColumn(label=None, format='%.1f'),
                  '$ cost per game': st.column_config.NumberColumn(label=None, format="$%.2f"),
                  '💎 value loss per game': st.column_config.NumberColumn(label=None, format="$%.2f")
                  }
summary_df = summary_df.sort_values('💎 value %', ascending=False)
default_columns = ['event name', 'entry 🪙', 'entry 💎', '💎 return', '💎 return %', '💎 loss in $', '💎 value', '💎 value %', 'value loss in $', '💎 per 🪙', '💎 cost per game', '$ cost per game']

column_names = st.multiselect('Select columns to display:', options = summary_df.columns, default = default_columns)

st.dataframe(data = summary_df[column_names], hide_index = True, width = 'content', column_config = summary_config)
st.write('(Click on column header to sort table)')
