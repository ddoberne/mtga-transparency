import streamlit as st
import event
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns


sns.set_theme()

gem_bundle_prices = ("$4.99", "$9.99", "$19.99", "$49.99", "$99.99")
gem_bundle_values = (750.0/5, 1600.0/10, 3400.0/20, 9200.0/50, 20000.0/100)
gems_per_usd = {}
for i in range(0, len(gem_bundle_prices)):
  gems_per_usd[gem_bundle_prices[i]] = gem_bundle_values[i]

user_bundle = st.sidebar.selectbox('Which bundle do you purchase?', gem_bundle_prices)
user_gems_per_usd = gems_per_usd[user_bundle]
st.sidebar.write(f'Each dollar buys you **{user_gems_per_usd:.0f}** gems.')
st.sidebar.write(f'Packs bought directly from the store cost 200 gems, or **${200/user_gems_per_usd:.2f}**. This is also the value of **1000 coins**.')
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

aggregate = st.sidebar.checkbox('Aggregate results with same payouts', value = True)
show_default = st.sidebar.checkbox('Show default distribution', value = True)
st.sidebar.write()
st.sidebar.write('[GitHub source](https://github.com/ddoberne/mtga-transparency)')

st.title("MTGA Cost Transparency Guide")
#st.write('Currently updating, check back later!')

tab_names = [ 'Bo1 Constr.', 'Bo3 Constr.', 'Q. Draft', 'Tr. Draft', 'Pr. Draft', 'Metagame Challenge', 'Sealed', 'Tr. Sealed']#, 'Arena Open', 'Arena Open (Day 2 Only)', 'Metagame Challenge']
tabs = st.tabs(tab_names)
tab_dict = {}
for i in range(len(tabs)):
  tab_dict[tab_names[i]] = tabs[i]

column_config = {'usd value': st.column_config.NumberColumn(label = None, format= "$%.2f"),
                 '% of results': st.column_config.ProgressColumn(label = None, format = '%.1f%%', min_value = 0, max_value = 100)}

summary = {}

def tab_info(tab_name, e, winrate, gem_prizes, pack_prizes, play_in_points, aggregate, user_gems_per_usd, entry_cost, coin_payout = False, results_only = False):
  results = e.get_distributions(winrate, simplify_results = False)
  default_results = e.get_distributions(.5, simplify_results = False)
  df = pd.DataFrame(results).transpose()
  default_df = pd.DataFrame(default_results).transpose()
  x_axis = 'record'
  if aggregate:
    df = df.groupby('wins').sum()['distribution']
    default_df = default_df.groupby('wins').sum()['distribution']
    x_axis = 'wins'
  df = df.reset_index()
  default_df = default_df.reset_index()
  df = df.rename(columns = {'index':'record'})
  default_df = default_df.rename(columns = {'index':'record'})
  df['% of results'] = df['distribution'] * 100
  default_df['% of results'] = default_df['distribution'] * 100
  df['gem payout'] = df['wins'].map(gem_prizes)
  if coin_payout:
      df['gem payout'] = df['gem payout']/50
  df['pack prizes'] = df['wins'].map(pack_prizes)
  df['play in points'] = df['wins'].map(play_in_points)
  df['usd value'] = df['gem payout'].apply(lambda x: x / user_gems_per_usd)
  df['usd value'] += df['play in points'] * 200 / user_gems_per_usd
  ev = 0
  pack_ev = 0
  for i in df.index:
    ev += df.loc[i, 'distribution'] * (df.loc[i, 'gem payout'] + (200 * df.loc[i, 'play in points']))
    pack_ev += df.loc[i, 'distribution'] * df.loc[i, 'pack prizes']
  rake = entry_cost - ev
  summary[tab_name] = {'entry cost': entry_cost, 'gem ev': ev, 'gem ev %': 100 * (1 - rake/entry_cost), 'usd loss per event': rake/user_gems_per_usd, 'pack ev': pack_ev, 'gems per pack': rake/pack_ev}
  if results_only:
      return df
  fig, ax = plt.subplots(figsize = (8, 3))
  ax.plot(df[[x_axis, '% of results']].set_index(x_axis), 'o-b', linewidth = 3, label = f'{user_winrate * 100:.0f}% wr')
  if show_default:
      ax.plot(default_df[[x_axis, '% of results']].set_index(x_axis), 'o-g', linewidth = 1, label = 'default')
      plt.legend()
  for x, y in zip(df[x_axis], df['% of results']):
    plt.text(x = x, y = y + 1, s = '{:.1f}%'.format(y), color = 'blue')
  ax.yaxis.set_major_formatter(mtick.PercentFormatter())
  ax.set_ylim(0, df['% of results'].max() + 5)
  plt.ylabel('% of results')
  plt.xlabel(x_axis)
  # Writing begins here
  st.header(f'{tab_name} prize distribution for a {user_winrate * 100:.0f}% winrate ({entry_cost} gem/${entry_cost/user_gems_per_usd:.2f} entry)')
  st.pyplot(fig)
  st.dataframe(df[[x_axis, '% of results', 'gem payout', 'pack prizes', 'play in points', 'usd value']], hide_index = True, use_container_width = True, column_config = column_config)
  st.write(f'The expected gem payout for this event given a {winrate * 100:.0f}% winrate is **{ev:.1f}** gems (including play-in points).')
  st.write(f'The expected pack payout is **{pack_ev:.1f}** packs.')
  if ev > entry_cost:
    st.write(f'That means an average **gain** of **{- rake:.1f}** gems (**${-rake/user_gems_per_usd:.2f}**) per event, or **{(- rake) * 100.0/entry_cost:.1f}%**')
  else:
    st.write(f'That means an average **loss** of **{rake:.1f}** gems (**${rake/user_gems_per_usd:.2f}**) per event, or **{(rake) * 100.0/entry_cost:.1f}%**')
    st.write(f'This event converts **{rake:.1f}** gems to **{pack_ev:.1f}** packs, with an efficiency of **{(rake)/pack_ev:.1f}** gems per pack.')


with tab_dict['Bo1 Constr.']:
  tab_name = 'Bo1 Constructed'
  gem_prizes = {0:25, 1:50, 2:75, 3:200, 4:300, 5:400, 6:450, 7:500}
  pack_prizes = {0:0, 1:0, 2:1, 3:1, 4:1, 5:2, 6:2, 7:3}
  play_in_points = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:3}
  entry_cost = 375
  constructed_event = event.Event(rounds = 9, win_thresh = 7, loss_thresh = 3, bo1 = True)
  tab_info(tab_name, constructed_event, user_winrate, gem_prizes, pack_prizes, play_in_points, aggregate, user_gems_per_usd, entry_cost)

with tab_dict['Bo3 Constr.']:
  tab_name = 'Bo3 Constructed'
  gem_prizes = {0:50, 1:100, 2:150, 3:600, 4:800, 5:1000}
  pack_prizes = {0:1, 1:1, 2:2, 3:2, 4:2, 5:3}
  play_in_points = {0:0, 1:0, 2:0, 3:0, 4:0, 5:4}
  entry_cost = 750
  traditional_constructed = event.Event(rounds = 5, win_thresh = 5, loss_thresh = 5, bo1 = False)
  tab_info(tab_name, traditional_constructed, user_winrate, gem_prizes, pack_prizes, play_in_points, aggregate, user_gems_per_usd, entry_cost)

with tab_dict['Q. Draft']:
  tab_name = 'Quick Draft'
  gem_prizes = {0:50, 1:100, 2:200, 3:300, 4:450, 5:650, 6:850, 7:950}
  pack_prizes = {0:1.2, 1:1.22, 2:1.24, 3:1.26, 4:1.3, 5:1.35, 6:1.4, 7:2}
  play_in_points = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
  entry_cost = 750
  quick_draft = event.Event(rounds = 9, win_thresh = 7, loss_thresh = 3, bo1 = True)
  tab_info(tab_name, quick_draft, limited_winrate, gem_prizes, pack_prizes, play_in_points, aggregate, user_gems_per_usd, entry_cost)

with tab_dict['Tr. Draft']:
  tab_name = 'Traditional Draft'
  gem_prizes = {0:100, 1:250, 2:1000, 3:2500}
  pack_prizes = {0:1, 1:1, 2:3, 3:6}
  play_in_points = {0:1, 1:0, 2:0, 3:2}
  entry_cost = 1500
  traditional_draft = event.Event(rounds = 3, win_thresh = 3, loss_thresh = 3, bo1 = False)
  tab_info(tab_name, traditional_draft, limited_winrate, gem_prizes, pack_prizes, play_in_points, aggregate, user_gems_per_usd, entry_cost)

with tab_dict['Pr. Draft']:
  tab_name = 'Premier Draft'
  gem_prizes = {0:50, 1:100, 2:250, 3:1000, 4:1400, 5:1600, 6:1800, 7:2200}
  pack_prizes = {0:1, 1:1, 2:2, 3:2, 4:3, 5:4, 6:5, 7:6}
  play_in_points = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
  entry_cost = 1500
  premier_draft = event.Event(rounds = 9, win_thresh = 7, loss_thresh = 3, bo1 = True)
  tab_info(tab_name, premier_draft, limited_winrate, gem_prizes, pack_prizes, play_in_points, aggregate, user_gems_per_usd, entry_cost)


with tab_dict['Metagame Challenge']:
    tab_name = 'Metagame Challenge'
    gem_prizes = {0:500, 1:1000, 2:1500, 3:2000, 4:2500, 5:3000, 6:4000, 7:5000}
    pack_prizes = {0:0, 1:0, 2:1, 3:3, 4:5, 5:10, 6:20, 7:30}
    play_in_points = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
    entry_cost = 400
    metagame_challenge = event.Event(rounds = 7, win_thresh = 7, loss_thresh = 1, bo1 = False)
    tab_info(tab_name, metagame_challenge, user_winrate, gem_prizes, pack_prizes, play_in_points, aggregate, user_gems_per_usd, entry_cost, coin_payout = True)

with tab_dict['Sealed']:
    tab_name = 'Sealed'
    gem_prizes = {0:200, 1:400, 2:600, 3:1200, 4:1400, 5:1600, 6:2000, 7:2200}
    pack_prizes = {0:3, 1:3, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3}
    play_in_points = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
    entry_cost = 2000
    metagame_challenge = event.Event(rounds = 9, win_thresh = 7, loss_thresh = 3, bo1 = True)
    tab_info(tab_name, sealed, user_winrate, gem_prizes, pack_prizes, play_in_points, aggregate, user_gems_per_usd, entry_cost)


with tab_dict['Tr. Sealed']:
    tab_name = 'Sealed
    gem_prizes = {0:200, 1:500, 2:1200, 3:1800, 4:2200}
    pack_prizes = {0:3, 1:3, 2:3, 3:3, 4:3}
    play_in_points = {0:0, 1:0, 2:0, 3:0, 4:0}
    entry_cost = 2000
    metagame_challenge = event.Event(rounds = 5, win_thresh = 4, loss_thresh = 2, bo1 = True)
    tab_info(tab_name, sealed, user_winrate, gem_prizes, pack_prizes, play_in_points, aggregate, user_gems_per_usd, entry_cost)

st.divider()
if same_winrate:
    st.header(f'Summary of events for {user_winrate * 100:.0f}% winrate')
else:
    st.header(f'Summary of events for {user_winrate * 100:.0f}% constructed and {limited_winrate * 100:.0f}% limited winrates')
summary_df = pd.DataFrame(summary).transpose().reset_index()
summary_df = summary_df.rename(columns = {'index': 'event name'})
summary_config = {'usd loss per event': st.column_config.NumberColumn(label = None, format= "$%.2f"),
                  'gem ev': st.column_config.NumberColumn(label = None, format = '%.1f'),
                  'gem ev %': st.column_config.ProgressColumn(label = None, format = '%.1f%%', min_value = 0, max_value = 100),
                  'pack ev': st.column_config.NumberColumn(label = None, format = '%.1f'),
                  'gems per pack': st.column_config.NumberColumn(label = None, format = '%.1f')}
st.dataframe(data = summary_df, hide_index = True, use_container_width = True, column_config = summary_config)
st.write('(Click on column header to sort table)')
