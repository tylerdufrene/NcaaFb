select 
a.home,
a.away,
s.spread_diff,
round(s.spread_pct,2) as spread_pct,
case when s.spread_pct between 0.54 and 1 then SpreadOutcome
     when s.spread_pct between 0 and 0.46 and SpreadOutcome like '%' || home || '%' then away || ' Covers'
	 when s.spread_pct between 0 and 0.46 and SpreadOutcome like '%' || away || '%' then home || ' Covers'
	 when s.spread_pct is null and SpreadOutcome like '%' || home || '%' then away || ' Covers'
	 when s.spread_pct is null and SpreadOutcome like '%' || away || '%' then home || ' Covers'
	 else 'Do not bet' end as spread_result,
t.total_diff,
round(t.ou_pct,2) as ou_pct,
case when t.ou_pct between 0.61 and 1 then overUnder
     when t.ou_pct between 0 and 0.40 and overUnder = 'over' then 'Under'
	 when t.ou_pct between 0 and 0.40 and overUnder = 'under' then 'Over'
	 else 'Do not bet' end as total_result,
home_win_prob,
home_ml,
away_ml
from ncaab_current_day_bets_to_make a 
left join ncaab_ou_accuracy t on t.total_diff = a.total_diff 
left join ncaab_spread_accuracy s on s.spread_diff = a.spread_diff
order by home
;


