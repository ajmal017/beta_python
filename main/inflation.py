'''
monthly inflation (annualized), taken from 'Retirement Modelling
V3.xlsx' (tab 'Inflation Forecast')
'''

inflation_level = [0.0160	,
0.0160	,
0.0160	,
0.0170	,
0.0170	,
0.0170	,
0.0170	,
0.0170	,
0.0170	,
0.0200	,
0.0200	,
0.0200	,
0.0200	,
0.0200	,
0.0200	,
0.0200	,
0.0200	,
0.0200	,
0.0200	,
0.0200	,
0.0200	,
0.0200	,
0.0200	,
0.0200	,
0.0225	,
0.0225	,
0.0225	,
0.0225	,
0.0225	,
0.0225	,
0.0225	,
0.0225	,
0.0225	,
0.0225	,
0.0225	,
0.0225	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0250	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0275	,
0.0270	,
0.0270	,
0.0270	,
0.0270	,
0.0270	,
0.0270	,
0.0270	,
0.0270	,
0.0270	,
0.0270	,
0.0270	,
0.0270	,
0.0280	,
0.0280	,
0.0280	,
0.0280	,
0.0280	,
0.0280	,
0.0280	,
0.0280	,
0.0280	,
0.0280	,
0.0280	,
0.0280	,
0.0290	,
0.0290	,
0.0290	,
0.0290	,
0.0290	,
0.0290	,
0.0290	,
0.0290	,
0.0290	,
0.0290	,
0.0290	,
0.0290	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0310	,
0.0310	,
0.0310	,
0.0310	,
0.0310	,
0.0310	,
0.0310	,
0.0310	,
0.0310	,
0.0310	,
0.0310	,
0.0310	,
0.0320	,
0.0320	,
0.0320	,
0.0320	,
0.0320	,
0.0320	,
0.0320	,
0.0320	,
0.0320	,
0.0320	,
0.0320	,
0.0320	,
0.0330	,
0.0330	,
0.0330	,
0.0330	,
0.0330	,
0.0330	,
0.0330	,
0.0330	,
0.0330	,
0.0330	,
0.0330	,
0.0330	,
0.0340	,
0.0340	,
0.0340	,
0.0340	,
0.0340	,
0.0340	,
0.0340	,
0.0340	,
0.0340	,
0.0340	,
0.0340	,
0.0340	,
0.0350	,
0.0350	,
0.0350	,
0.0350	,
0.0350	,
0.0350	,
0.0350	,
0.0350	,
0.0350	,
0.0350	,
0.0350	,
0.0350	,
0.0360	,
0.0360	,
0.0360	,
0.0360	,
0.0360	,
0.0360	,
0.0360	,
0.0360	,
0.0360	,
0.0360	,
0.0360	,
0.0360	,
0.0370	,
0.0370	,
0.0370	,
0.0370	,
0.0370	,
0.0370	,
0.0370	,
0.0370	,
0.0370	,
0.0370	,
0.0370	,
0.0370	,
0.0380	,
0.0380	,
0.0380	,
0.0380	,
0.0380	,
0.0380	,
0.0380	,
0.0380	,
0.0380	,
0.0380	,
0.0380	,
0.0380	,
0.0390	,
0.0390	,
0.0390	,
0.0390	,
0.0390	,
0.0390	,
0.0390	,
0.0390	,
0.0390	,
0.0390	,
0.0390	,
0.0390	,
0.0400	,
0.0400	,
0.0400	,
0.0400	,
0.0400	,
0.0400	,
0.0400	,
0.0400	,
0.0400	,
0.0400	,
0.0400	,
0.0400	,
0.0410	,
0.0410	,
0.0410	,
0.0410	,
0.0410	,
0.0410	,
0.0410	,
0.0410	,
0.0410	,
0.0410	,
0.0410	,
0.0410	,
0.0350	,
0.0350	,
0.0350	,
0.0350	,
0.0350	,
0.0350	,
0.0350	,
0.0350	,
0.0350	,
0.0350	,
0.0350	,
0.0350	,
0.0340	,
0.0340	,
0.0340	,
0.0340	,
0.0340	,
0.0340	,
0.0340	,
0.0340	,
0.0340	,
0.0340	,
0.0340	,
0.0340	,
0.0330	,
0.0330	,
0.0330	,
0.0330	,
0.0330	,
0.0330	,
0.0330	,
0.0330	,
0.0330	,
0.0330	,
0.0330	,
0.0330	,
0.0320	,
0.0320	,
0.0320	,
0.0320	,
0.0320	,
0.0320	,
0.0320	,
0.0320	,
0.0320	,
0.0320	,
0.0320	,
0.0320	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300	,
0.0300]
