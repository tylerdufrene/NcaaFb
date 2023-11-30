select 
home,
away,
case when c.away_ml < 0 and a.spread < c.spread then a.away || ' Covers'
     when c.home_ml < 0 and a.spread > abs(c.spread) then a.home || ' Covers'
	 when c.spread is null then 'N/A'
	 when c.home_ml < 0 and a.spread < abs(c.spread) then a.away || ' Covers'
	 when c.away_ml < 0 and a.spread > c.spread then a.home || ' Covers'
	 end as SpreadOutcome,
case when a.game_score_total >= c.line then 'over' 
	 when a.game_score_total < c.line then 'under'
	 else 'N/A' end as overUnder,
round(a.spread,2) as pred_spread,
c.spread,
case when home_ml < away_ml and a.spread > 0 then abs(round(a.spread - abs(c.spread)))
	 when away_ml < home_ml and a.spread < 0 then abs(round(abs(a.spread) - abs(c.spread)))
	 when away_ml < home_ml and a.spread > 0 then abs(round(a.spread - c.spread)) 
	 when home_ml < away_ml and a.spread < 0 then abs(round(abs(a.spread) - c.spread)) end
	 as spread_diff,
round(a.game_score_total,2) as pred_total,
c.line,
abs(round(a.game_score_total - c.line)) as total_diff,
home_record,
away_record,
c.home_ml,
c.away_ml,
round(a.home_win_prob*100,2) as home_win_prob,
round(a.game_score_home,2) as home_score,
round(a.game_score_away,2) as away_score
-- b.team,
-- c.*

 from ncaab_todays_game_predictions a
left join ncaab_teams_odds_mapping b on b.team = a.home 
left join ncaab_betting_lines c on c.home_team = b."Betting Teams"
where c.spread is not NULL

UNION ALL 

select 
home,
away,
case when c.away_ml < 0 and a.spread < c.spread then a.away || ' Covers'
     when c.home_ml < 0 and a.spread > abs(c.spread) then a.home || ' Covers'
	 when c.spread is null then 'N/A'
	 when c.home_ml < 0 and a.spread < abs(c.spread) then a.away || ' Covers'
	 when c.away_ml < 0 and a.spread > c.spread then a.home || ' Covers'
	 end as SpreadOutcome,
case when a.game_score_total >= c.line then 'over' 
	 when a.game_score_total < c.line then 'under'
	 else 'N/A' end as overUnder,
round(a.spread,2) as pred_spread,
c.spread,
case when home_ml < away_ml and a.spread > 0 then abs(round(a.spread - abs(c.spread)))
	 when away_ml < home_ml and a.spread < 0 then abs(round(abs(a.spread) - abs(c.spread)))
	 when away_ml < home_ml and a.spread > 0 then abs(round(a.spread - c.spread)) 
	 when home_ml < away_ml and a.spread < 0 then abs(round(abs(a.spread) - c.spread)) end
	 as spread_diff,
round(a.game_score_total,2) as pred_total,
c.line,
abs(round(a.game_score_total - c.line)) as total_diff,
home_record,
away_record,
c.home_ml,
c.away_ml,
round(a.home_win_prob*100,2) as home_win_prob,
round(a.game_score_home,2) as home_score,
round(a.game_score_away,2) as away_score
-- b.team,
-- c.*

 from ncaab_todays_game_predictions a
left join ncaab_teams_odds_mapping b on b.team = a.away 
left join ncaab_betting_lines c on c.away_team = b."Betting Teams"
where c.spread is not null

UNION ALL 

select 
home,
away,
case when c.home_ml < 0 and a.spread < c.spread then a.away || ' Covers'
     when c.away_ml < 0 and a.spread > abs(c.spread) then a.home || ' Covers'
	 when c.spread is null then 'N/A'
	 when c.away_ml < 0 and a.spread < abs(c.spread) then a.away || ' Covers'
	 when c.home_ml < 0 and a.spread > c.spread then a.home || ' Covers'
	 end as SpreadOutcome,
case when a.game_score_total >= c.line then 'over' 
	 when a.game_score_total < c.line then 'under'
	 else 'N/A' end as overUnder,
round(a.spread,2) as pred_spread,
c.spread,
case when away_ml < home_ml and a.spread > 0 then abs(round(a.spread - abs(c.spread)))
	 when home_ml < away_ml and a.spread < 0 then abs(round(abs(a.spread) - abs(c.spread)))
	 when home_ml < away_ml and a.spread > 0 then abs(round(a.spread - c.spread)) 
	 when away_ml < home_ml and a.spread < 0 then abs(round(abs(a.spread) - c.spread)) end
	 as spread_diff,
round(a.game_score_total,2) as pred_total,
c.line,
abs(round(a.game_score_total - c.line)) as total_diff,
away_record,
home_record,
c.away_ml,
c.home_ml,
round(a.home_win_prob*100,2) as home_win_prob,
round(a.game_score_home,2) as home_score,
round(a.game_score_away,2) as away_score
-- b.team,
-- c.*

 from ncaab_todays_game_predictions a
left join ncaab_teams_odds_mapping b on b.team = a.home 
left join ncaab_betting_lines c on c.away_team = b."Betting Teams"
where c.spread is not null
;