-- CREATE table ncaab_spread_historic_results as 
with past_games as (
	select *, 
	row_number() over (partition by away_team, home_team, date(date_upd) order by date_upd desc) as rnk
	from 
	ncaab_betting_lines_historic
)
, main as (
select *,
case when c.away_ml < 0 and (a.game_score_home - a.game_score_away) < c.spread then a.away || ' Covers'
     when c.home_ml < 0 and (a.game_score_home - a.game_score_away) > abs(c.spread) then a.home || ' Covers'
	 when c.spread is null then 'N/A'
	 when c.home_ml < 0 and (a.game_score_home - a.game_score_away) < abs(c.spread) then a.away || ' Covers'
	 when c.away_ml < 0 and (a.game_score_home - a.game_score_away) > c.spread then a.home || ' Covers'
	 end as SpreadDecision,
case when (a.game_score_home + a.game_score_away) >= c.line then 'over' 
	 when (a.game_score_home + a.game_score_away) < c.line then 'under'
	 else 'N/A' end as overUnderPred,
case when (p.t2pts + p.t1pts) >= c.line then 'over' 
	 when (p.t2pts + p.t1pts) < c.line then 'under'
	 else 'N/A' end as over_underActual,
round((a.game_score_home - a.game_score_away),2) as pred_spread,
c.spread,
p.t2pts - p.t1pts as actualSpread,
case when c.away_ml < 0 and (p.t2pts - p.t1pts) < c.spread then a.away || ' Covers'
     when c.home_ml < 0 and (p.t2pts - p.t1pts) > abs(c.spread) then a.home || ' Covers'
	 when c.spread is null then 'N/A'
	 when c.home_ml < 0 and (p.t2pts - p.t1pts) < abs(c.spread) then a.away || ' Covers'
	 when c.away_ml < 0 and (p.t2pts - p.t1pts) > c.spread then a.home || ' Covers'
	 end as spreadOutcome,
case when home_ml < away_ml and (a.game_score_home - a.game_score_away)> 0 then abs(round((a.game_score_home - a.game_score_away) - abs(c.spread)))
	 when away_ml < home_ml and (a.game_score_home - a.game_score_away) < 0 then abs(round(abs((a.game_score_home - a.game_score_away)) - abs(c.spread)))
	 when away_ml < home_ml and (a.game_score_home - a.game_score_away) > 0 then abs(round((a.game_score_home - a.game_score_away) - c.spread))
	 when home_ml < away_ml and (a.game_score_home - a.game_score_away) < 0 then abs(round(abs((a.game_score_home - a.game_score_away)) - c.spread)) end
	 as spread_diff,
round((a.game_score_home + a.game_score_away),2) as pred_total,
c.line,
round(p.t2pts + p.t1pts) as actualTotal,
abs(round((a.game_score_home + a.game_score_away) - c.line)) as total_diff,
home_record,
away_record,
c.home_ml,
c.away_ml
-- round(a.t2fun*100,2) as home_wp,
-- case when a.t2fun >= 0.5 and a.team2 = a.winner then 1 
-- 	 when a.t2fun < 0.5 and a.team2 = a.loser then 1
-- 	 else 0 end as predML
 from ncaab_historic_game_predictions a
left join ncaab_teams_odds_mapping b on b.team = a.home
 left join past_games c on (c.home_team = b."Betting Teams") and date(a."game_date") = date(c."date_upd") and c.rnk = 1
left join ncaab_post_game_results p on p.team2 = a.home and date(p."date") = a.game_date

where date(a.game_date) >= '2023-11-16'
-- WHERE DATE(a."date") = '2023-11-19'
and c.spread is not null 
and p.winner is not null
and source = 'auto'

union all 

select *,
case 
	 when c.home_ml < c.away_ml and (a.game_score_home - a.game_score_away) > abs(c.spread) then a.home || ' Covers2'
	 when c.away_ml < c.home_ml and (a.game_score_home - a.game_score_away) < c.spread then a.away || ' Covers1'
	 when c.home_ml < c.away_ml and (a.game_score_home - a.game_score_away) < abs(c.spread) then a.away || ' Covers3'
	 when c.away_ml < c.home_ml and (a.game_score_home - a.game_score_away) > c.spread then a.home || ' Covers4'
	 when c.spread is null then 'N/A'
	 end as SpreadDecision,
case when (a.game_score_away + a.game_score_home) >= c.line then 'over' 
	 when (a.game_score_away + a.game_score_home) < c.line then 'under'
	 else 'N/A' end as overUnderPred,
case when (t2pts + t1pts) >= c.line then 'over' 
	 when (t2pts + t1pts) < c.line then 'under'
	 else 'N/A' end as over_underActual,
round((a.game_score_home - a.game_score_away),2) as pred_spread,
c.spread,
t1pts - t2pts as actualSpread,
case 
	 when c.home_ml < c.away_ml and (t1pts - t2pts) > abs(c.spread) then a.home || ' Covers2'
	 when c.away_ml < c.home_ml and (t1pts - t2pts) < c.spread then a.away || ' Covers1'
	 when c.home_ml < c.away_ml and (t1pts - t2pts) < abs(c.spread) then a.away || ' Covers3'
	 when c.away_ml < c.home_ml and (t1pts - t2pts) > c.spread then a.home || ' Covers4'
	 when c.spread is null then 'N/A'
	 end as spreadOutcome,
case when home_ml < away_ml and (a.game_score_home - a.game_score_away)> 0 then abs(round((a.game_score_home - a.game_score_away) - abs(c.spread)))
	 when away_ml < home_ml and (a.game_score_home - a.game_score_away) < 0 then abs(round(abs((a.game_score_home - a.game_score_away)) - abs(c.spread)))
	 when away_ml < home_ml and (a.game_score_home - a.game_score_away) > 0 then abs(round((a.game_score_home - a.game_score_away) - c.spread))
	 when home_ml < away_ml and (a.game_score_home - a.game_score_away) < 0 then abs(round(abs((a.game_score_home - a.game_score_away)) - c.spread)) end
	 as spread_diff,
round((a.game_score_away + a.game_score_home),2) as pred_total,
c.line,
round(t2pts + t1pts) as actualTotal,
abs(round((a.game_score_home + a.game_score_away) - c.line)) as total_diff,
home_record,
away_record,
c.home_ml,
c.away_ml
-- round(a.t2fun*100,2) as home_wp,
-- case when a.t2fun >= 0.5 and a.team2 = a.winner then 1 
-- 	 when a.t2fun < 0.5 and a.team2 = a.loser then 1
-- 	 else 0 end as predML
 from ncaab_historic_game_predictions a
left join ncaab_teams_odds_mapping b on b.team = a.home
 left join past_games c on (c.Home_team = b."Betting Teams") and date(a."game_date") = date(c."date_upd") and c.rnk = 1
left join ncaab_post_game_results p on p.team2 = a.home and date(p."date") = a.game_date
where date(a.game_date) >= '2023-11-16'
-- WHERE DATE(a."date") = '2023-11-19'
and c.spread is not null 
and p.winner is not null
and source = 'auto'

), dedup as (
	select *,
	row_number() over (partition by game_date, home, away order by date_upd desc) as rn
	from main
	where game_date is not null
), spread_accuracy as (
	select *,
	cumu_correct/cast(cumu_games as float) as spread_pct
	 from dedup a 
	left join NCAAB_spread_DAILY_ANALYSIS b on a.game_date =  DATE(b.game_date, '+1 days') and b.spread_diff = a.spread_diff
	where rn = 1
)
, decision as (
	select game_date,
	home,
	away,
	SpreadDecision,
	pred_spread,
	spread, 
	spread_diff,
	SpreadOutcome,
	actualspread,
	cumu_games,
	cumu_correct,
	round(spread_pct,3) as spread_pct,
	case when spread_pct between 0.54 and 1 then SpreadDecision
		 when spread_pct between 0 and 0.46 and SpreadDecision like '%' || home || '%' then away || ' Covers'
		 when spread_pct between 0 and 0.46 and SpreadDecision like '%' || away || '%' then home || ' Covers'
		 when spread_pct is null and SpreadDecision like '%' || home || '%' then home || ' Covers'
		 when spread_pct is null and SpreadDecision like '%' || away || '%' then away || ' Covers'
		 else 'No Bet' end as spread_result
	 from spread_accuracy
)
, result as (
	select *,
	1 as bet,
	case when SpreadOutcome = spread_result then 1.9
		 when spread_result = 'No Bet' then 1
		 when spread_result <> SpreadOutcome then 0 end as result
	from decision
	where game_date >= '2023-11-17'
), return as (
	select 
	game_date,
	sum(bet) as bets,
	sum(result) as outcome,
	sum(result) - sum(bet) as return 
	from result
	where result is not null
    and result <> 'No Bet'
	group by 1
	order by 1
)
select *
, sum(return) over (order by game_date) as cum_return
 from return
 group by 1,2,3,4
;

-- select * from NCAAB_spread_DAILY_ANALYSIS
