import streamlit as st
import event
import numpy as np
import pandas as pd

gem_bundle_prices = ("$4.99", "$9.99", "$19.99", "$49.99", "$99.99")
gem_bundle_values = (750.0/5, 1600.0/10, 3400.0/20, 9200.0/50, 20000.0/100)
gems_per_usd = {}
for i in range(0, len(gem_bundle_prices)):
  gems_per_usd[gem_bundle_prices[i]] = gem_bundle_values[i]
  
user_bundle = st.sidebar.selectbox('Which bundle do you purchase?', gem_bundle_prices)
user_gems_per_usd = gems_per_usd[user_bundle]
st.sidebar.write(f'Your gems are worth {user_gems_per_usd:.2f} gems per dollar.')
user_winrate = st.sidebar.slider(label = 'Select game winrate:', min_value = 0.00, max_value = 1.00, value = 0.5, step = 0.01)
st.sidebar.write(f'You win **{100 * ((user_winrate ** 2) + (2 * user_winrate * user_winrate * (1 - user_winrate))):.0f}** of your Bo3s.')
aggregate = st.sidebar.checkbox('Aggregate results with same payouts')

st.title("MTGA Cost Transparency Key")

tab_names = ['Quick Draft', 'Traditional Draft', 'Premier Draft', 'Constructed Event', 'Traditional Constructed Event', 'Arena Open', 'Arena Open (Day 2 Only)', 'Metagame Challenge']
tabs = st.tabs(tab_names)
tab_dict = {}
for i in range(len(tabs)):
  tab_dict[tab_names[i]] = tabs[i]

with tab_dict['Quick Draft']:
  quick_draft = event.Event(rounds = 9, win_thresh = 7, loss_thresh = 3, bo1 = True)
  results = quick_draft.get_distributions(user_winrate, simplify_results = False)
  gem_prizes = {0:50, 1:100, 2:200, 3:300, 4:450, 5:650, 6:850, 7:950}
  pack_prizes = {0:1.2, 1:1.22, 2:1.24, 3:1.26, 4:1.3, 5:1.35, 6:1.4, 7:2}
  print(results)
  df = pd.DataFrame(results).transpose()
  st.dataframe(df)
  st.line_chart(df, y = 'distribution') 



