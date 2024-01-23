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

tab_names = ['Q. Draft', 'Tr. Draft', 'Pr. Draft', 'Bo1 Constructed', 'Bo3 Constructed', 'Arena Open', 'Arena Open (Day 2 Only)', 'Metagame Challenge']
tabs = st.tabs(tab_names)
tab_dict = {}
for i in range(len(tabs)):
  tab_dict[tab_names[i]] = tabs[i]

def tab_info(e, winrate, gem_prizes, pack_prizes, aggregate, user_gems_per_usd):
  results = e.get_distributions(winrate, simplify_results = False)
  df = pd.DataFrame(results).transpose()
  x_axis = 'record'
  if aggregate:
    df = df.groupby('wins').sum()['distribution']
    x_axis = 'wins'
  df.reset_index()
  df = df.rename({'index':'record'})
  st.write('here is the df')
  st.write(df)
  df['gem_payout'] = df['wins'].map(gem_prizes)
  df['pack_prizes'] = df['wins'].map(pack_prizes)
  df['usd_value'] = df['gem_payout'].apply(lambda x: x / user_gems_per_usd)
  df['% of results'] = df['distribution'] * 100
  ig, ax = plt.subplots()
  ax.plot(df[[x_axis, '% of results']].set_index(x_axis), 'o-b')
  
  for x, y in zip(df[x_axis], df['% of results']):
    plt.text(x = x, y = y + .3, s = '{:.1f}%'.format(y), color = 'blue')
  ax.yaxis.set_major_formatter(mtick.PercentFormatter())
  ax.set_ylim(0, df['% of results'].max() + 5)
  plt.ylabel('% of results')
  plt.xlabel(x_axis)
  st.pyplot(fig)
  st.dataframe(df)
  

with tab_dict['Q. Draft']:
  st.header(f'Quick Draft prize distribution for a {user_winrate}% winrate')
  gem_prizes = {0:50, 1:100, 2:200, 3:300, 4:450, 5:650, 6:850, 7:950}
  pack_prizes = {0:1.2, 1:1.22, 2:1.24, 3:1.26, 4:1.3, 5:1.35, 6:1.4, 7:2}
  quick_draft = event.Event(rounds = 9, win_thresh = 7, loss_thresh = 3, bo1 = True)
  tab_info(quick_draft, user_winrate, gem_prizes, pack_prizes, aggregate, user_gems_per_usd)
  '''results = quick_draft.get_distributions(user_winrate, simplify_results = False)
  df = pd.DataFrame(results).transpose()
  x_axis = 'record'
  if aggregate:
    df = df.groupby('wins').sum()['distribution']
    x_axis = 'wins'
  df = df.reset_index()
  df = df.rename({'index':'record'})
  df['% of results'] = df['distribution'] * 100
  df['gem_payout'] = df['wins'].map(gem_prizes)
  df['pack_prizes'] = df['wins'].map(pack_prizes)
  df['usd_value'] = df['gem_payout'].apply(lambda x: x / user_gems_per_usd)
  st.dataframe(df)
  fig, ax = plt.subplots()
  ax.plot(df[[x_axis, '% of results']].set_index(x_axis), 'o-b')
  
  for x, y in zip(df[x_axis], df['% of results']):
    plt.text(x = x, y = y + .3, s = '{:.1f}%'.format(y), color = 'blue')
  ax.yaxis.set_major_formatter(mtick.PercentFormatter())
  ax.set_ylim(0, df['% of results'].max() + 5)
  plt.ylabel('% of results')
  plt.xlabel(x_axis)
  st.pyplot(fig)'''

with tab_dict['Tr. Draft']:
  traditional_draft = event.Event(rounds = 3, win_thresh = 3, loss_thresh = 3, bo1 = False)
  results = traditional_draft.get_distributions(user_winrate, simplify_results = aggregate)
  gem_prizes = {0:100, 1:250, 2:1000, 3:2500}
  pack_prizes = {0:1, 1:1, 2:3, 3:6}
  st.write('test')
