with last_week as (
	select team_team, 
	max(week_num) as last_week
	from ncaaf_avg5_season_stats_by_team_total
	where season = 2023
	group by 1
)
select gs.*,
bl.away_moneyline,
bl.home_moneyline, 
bl.spread,
bl.formatted_spread,
bl.over_under,
s.team_points_season_avg as home_avg_points,
s.opponent_points_season_avg as home_opp_points,
s2.team_points_season_avg as away_avg_points,
s2.opponent_points_season_avg as away_opp_points,
wp.home_win_prob,
e_h.elo as home_elo,
e_a.elo as away_elo,
f_h.fpi as home_fpi,
f_h.offense_efficiency as home_offense_eff,
f_h.defense_efficiency as home_def_eff,
f_h.overall_efficiency as home_overall_eff,
f_h.average_win_probability as home_avg_win_prob,
f_h.fpi_rank as home_fpi_rank,
f_h.game_control as home_game_control,
f_h.strength_of_schedule as home_sos,
f_a.fpi as away_fpi,
f_a.offense_efficiency as away_offense_eff,
f_a.defense_efficiency as away_def_eff,
f_a.overall_efficiency as away_overall_eff,
f_a.average_win_probability as away_avg_win_prob,
f_a.fpi_rank as away_fpi_rank,
f_a.game_control as away_game_control,
f_a.strength_of_schedule as away_sos,
tt.talent_score as home_talent,
tt2.talent_score as away_talent

from ncaaf_game_schedule gs 
left join ncaaf_betting_lines bl on bl.id = gs.id
left join ncaaf_avg5_season_stats_by_team_total s on s.team_team = gs.home_team and s.season = gs.season
left join ncaaf_avg5_season_stats_by_team_total s2 on s2.team_team = gs.away_team and s2.season = gs.season
join last_week lw_h on lw_h.team_team = s.team_team and lw_h.last_week = s.week_num
join last_week lw_a on lw_a.team_team = s2.team_team and lw_a.last_week = s2.week_num
left join ncaaf_metrics_win_prob wp on wp.id = gs.id
left join ncaaf_ratings_elo_score e_h on e_h.team = gs.home_team and e_h.season = 2023
left join ncaaf_ratings_elo_score e_a on e_a.team = gs.away_team and e_a.season = 2023
left join ncaaf_ratings_fpi_score f_h on f_h.team = gs.home_team and f_h.season = 2023
left join ncaaf_ratings_fpi_score f_a on f_a.team = gs.away_team and f_a.season = 2023
left join ncaaf_team_talent_score tt on tt.team = gs.home_team and tt.season = 2023
left join ncaaf_team_talent_score tt2 on tt2.team = gs.away_team and tt2.season = 2023
where gs.season = 2023
and gs.week_num = 10;