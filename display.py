import streamlit as st
import event
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick




gem_bundle_prices = ("$4.99", "$9.99", "$19.99", "$49.99", "$99.99")
gem_bundle_values = (750.0/5, 1600.0/10, 3400.0/20, 9200.0/50, 20000.0/100)
gems_per_usd = {}
for i in range(0, len(gem_bundle_prices)):
  gems_per_usd[gem_bundle_prices[i]] = gem_bundle_values[i]
  
user_bundle = st.sidebar.selectbox('Which bundle do you purchase?', gem_bundle_prices)
user_gems_per_usd = gems_per_usd[user_bundle]
st.sidebar.write(f'Your gems are worth **{user_gems_per_usd}** gems per dollar.')
user_winrate = st.sidebar.slider(label = 'Select game winrate:', min_value = 0.00, max_value = 1.00, value = 0.5, step = 0.01)
st.sidebar.write(f'You win **{100 * ((user_winrate ** 2) + (2 * user_winrate * user_winrate * (1 - user_winrate))):.1f}%** of your Bo3s.')
aggregate = st.sidebar.checkbox('Aggregate results with same payouts', value = True)

st.title("MTGA Cost Transparency Key")
#st.write('Currently updating, check back later!')

tab_names = ['Q. Draft', 'Tr. Draft', 'Pr. Draft', 'Bo1 Constructed', 'Bo3 Constructed', 'Arena Open', 'Arena Open (Day 2 Only)', 'Metagame Challenge']
tabs = st.tabs(tab_names)
tab_dict = {}
for i in range(len(tabs)):
  tab_dict[tab_names[i]] = tabs[i]

def tab_info(e, winrate, gem_prizes, pack_prizes, aggregate, user_gems_per_usd, entry_cost):
  results = e.get_distributions(user_winrate, simplify_results = False)
  df = pd.DataFrame(results).transpose()
  x_axis = 'record'
  if aggregate:
    df = df.groupby('wins').sum()['distribution']
    x_axis = 'wins'
  df = df.reset_index()
  df = df.rename(columns = {'index':'record'})
  df['% of results'] = df['distribution'] * 100
  df['gem_payout'] = df['wins'].map(gem_prizes)
  df['pack_prizes'] = df['wins'].map(pack_prizes)
  df['usd_value'] = df['gem_payout'].apply(lambda x: x / user_gems_per_usd)
  fig, ax = plt.subplots()
  ax.plot(df[[x_axis, '% of results']].set_index(x_axis), 'o-b')
  
  for x, y in zip(df[x_axis], df['% of results']):
    plt.text(x = x, y = y + .3, s = '{:.1f}%'.format(y), color = 'blue')
  ax.yaxis.set_major_formatter(mtick.PercentFormatter())
  ax.set_ylim(0, df['% of results'].max() + 5)
  plt.ylabel('% of results')
  plt.xlabel(x_axis)
  st.pyplot(fig)
  st.dataframe(df[[x_axis, '% of results', 'gem_payout', 'pack_prizes', 'usd_value']])
  ev = 0
  for i in df.index:
    ev += df.loc[i, 'distribution'] * df.loc[i, 'gem_payout']
  st.write(f'The expected gem payout for this event given a {winrate * 100}% winrate is {ev:.1f} gems.')
  if ev > entry_cost:
    st.write(f'That means an average gain of {ev - entry_cost:.1f} gems per event, or {(ev - entry_cost) * 100.0/entry_cost:.1f}%')
  else:
    st.write(f'That means an average loss of {entry_cost - ev:.1f} gems per event, or {(entry_cost - ev) * 100.0/entry_cost:.1f}%')
    
  

with tab_dict['Q. Draft']:
  st.header(f'Quick Draft prize distribution for a {user_winrate * 100}% winrate')
  gem_prizes = {0:50, 1:100, 2:200, 3:300, 4:450, 5:650, 6:850, 7:950}
  pack_prizes = {0:1.2, 1:1.22, 2:1.24, 3:1.26, 4:1.3, 5:1.35, 6:1.4, 7:2}
  entry_cost = 750
  quick_draft = event.Event(rounds = 9, win_thresh = 7, loss_thresh = 3, bo1 = True)
  tab_info(quick_draft, user_winrate, gem_prizes, pack_prizes, aggregate, user_gems_per_usd, entry_cost)

with tab_dict['Tr. Draft']:
  st.header(f'Traditional Draft prize distribution for a {user_winrate * 100}% winrate')
  gem_prizes = {0:100, 1:250, 2:1000, 3:2500}
  pack_prizes = {0:1, 1:1, 2:3, 3:6}
  entry_cost = 1500
  traditional_draft = event.Event(rounds = 3, win_thresh = 3, loss_thresh = 3, bo1 = False)
  tab_info(traditional_draft, user_winrate, gem_prizes, pack_prizes, aggregate, user_gems_per_usd, entry_cost)

with tab_dict['Pr. Draft']:
  st.header(f'Premier Draft prize distribution for a {user_winrate * 100}% winrate')
  gem_prizes = {0:50, 1:100, 2:250, 3:1000, 4:1400, 5:1600, 6:1800, 7:2200}
  pack_prizes = {0:1, 1:1, 2:2, 3:2, 4:3, 5:4, 6:5, 7:6}
  entry_cost = 1500
  premier_draft = event.Event(rounds = 9, win_thresh = 7, loss_thresh = 3, bo1 = True)
  tab_info(premier_draft, user_winrate, gem_prizes, pack_prizes, aggregate, user_gems_per_usd, entry_cost)

with tab_dict['Bo1 Constructed']:
  st.header(f'Constructed Event prize distribution for a {user_winrate * 100}% winrate')
  gem_prizes = {0:25, 1:50, 2:75, 3:200, 4:300, 5:400, 6:450, 7:500}
  pack_prizes = {0:0, 1:0, 2:1, 3:1, 4:1, 5:2, 6:2, 7:3}
  entry_cost = 375
  constructed_event = event.Event(rounds = 9, win_thresh = 7, loss_thresh = 3, bo1 = True)
  tab_info(constructed_event, user_winrate, gem_prizes, pack_prizes, aggregate, user_gems_per_usd, entry_cost)

with tab_dict['Bo3 Constructed']:
  st.header(f'Traditional Constructed prize distribution for a {user_winrate * 100}% winrate')
  gem_prizes = {0:50, 1:100, 2:150, 3:600, 4:800, 5:1000}
  pack_prizes = {0:1, 1:1, 2:2, 3:2, 4:2, 5:3}
  entry_cost = 750
  traditional_constructed = event.Event(rounds = 5, win_thresh = 5, loss_thresh = 5, bo1 = False)
  tab_info(traditional_constructed, user_winrate, gem_prizes, pack_prizes, aggregate, user_gems_per_usd, entry_cost)
