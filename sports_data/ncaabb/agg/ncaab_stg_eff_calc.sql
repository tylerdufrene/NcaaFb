with team_rank as (
	select team 
	, g
	, date 
	, season
	, rank() over(partition by team order by date) as team_rank
	from ncaab_all_games_by_season_adv
)

select 
a.g,
a."date",
a.season,
a.team,
a.opp_team,
a.tm,
a.opp_points,
a.ortg,
a.drtg,
a.pace,
a."efg%",
t1.team_rank,
b.ortg as o_ortg, 
b.drtg as o_drtg, 
b.pace as o_pace, 
b."eFG%" as o_efg,
t2.team_rank as opp_rank,
p.ppa
from ncaab_all_games_by_season_adv a 
LEFT join team_rank t1 on a.team = t1.team and a.g = t1.g and a.season = t1.season
left join ncaab_all_teams t on t.school = a.opp_team
left join ncaab_all_games_by_season_adv b on b.team = t.teamlookup and a."date" = b."date"
left join team_rank t2 on b.team = t2.team and b.g = t2.g and b.season = t2.season
left join ncaab_ppa_by_season p on p.season = a.season 