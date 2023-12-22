with past_games as (
	select *, 
	row_number() over (partition by away_team, home_team, date(date_upd) order by date_upd desc) as rnk
	from 
	ncaab_betting_lines_historic
)
, outcome as (
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
round((a.game_score_home - a.game_score_away),2) as pred_total,
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

)

select 
-- away_team, 
-- away_ml,
-- home_team, 
-- home_ml,
-- t1propt,
-- t2propt,
-- t1pts,
-- t2pts,
-- spread,
-- spreadDecision,
-- SpreadOutcome,
-- pred_spread,
-- actualSpread,
-- overUnderPred,
-- Over_underActual,
-- line,
-- pred_total,
-- actualtotal,
-- case when SpreadOutcome = SpreadDecision then 1 else 0 end as accurate_spread,
-- case when overUnderPred = over_underActual then 1 else 0 end as accurate_over
spread_diff,
count(*) as allGames,
sum(case when spreadOutcome=SpreadDecision then 1 else 0 end)/cast(count(*) as float) as spread_pct,
sum(case when overUnderPred=over_UnderActual then 1 else 0 end)/cast(Count(*) as float) as ou_pct
-- avg(predML)
 from outcome
where date("date") >= '2023-11-16'
 group by 1
;
