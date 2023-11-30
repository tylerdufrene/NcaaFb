with spread as (
	select cws.*,
	case when cast(fcs_p as float) >= 0.5 then favorite_team 
		 when cast(fcs_p as float) < 0.5 then underdog_team 
		 else 'N/A' end as Pick,
	fcs_p
	 from 
	 (
	 select
	favorite_team,
	underdog_team, 
	spread,
	formatted_spread,
	favorite_avg_points - favorite_opp_points as fav_diff,
	favorite_sos,
	(favorite_avg_points - favorite_opp_points + 0.1) / favorite_sos as fav_points,
	underdog_avg_points - underdog_opp_points as ud_diff, 
	underdog_sos,
	(underdog_avg_points - underdog_opp_points + 0.1) / underdog_sos as ud_points,
	((favorite_avg_points - favorite_opp_points + 0.1) / favorite_sos)*1.1 - ((underdog_avg_points - underdog_opp_points + 0.1) / underdog_sos) as points
	 from ncaaf_current_week_stats cws
	 where hm_team = 'favorite'
	 union all 
	  select
	favorite_team,
	underdog_team, 
	spread,
	formatted_spread,
	favorite_avg_points - favorite_opp_points as fav_diff,
	favorite_sos,
	(favorite_avg_points - favorite_opp_points + 0.1) / favorite_sos as fav_points,
	underdog_avg_points - underdog_opp_points as ud_diff, 
	underdog_sos,
	(underdog_avg_points - underdog_opp_points + 0.1) / underdog_sos as ud_points,
	((favorite_avg_points - favorite_opp_points + 0.1) / favorite_sos) - ((underdog_avg_points - underdog_opp_points + 0.1) / underdog_sos)*1.1 as points
	 from ncaaf_current_week_stats
	 where hm_team = 'underdog'
	 ) cws
	 left join ncaaf_odds_static o on cast(cws.points as float) >= cast(o.lower as float) and cast(cws.points as float) < cast(o.upper as float)
), ou as (
	select cws.*
	, cover_p
	, lower
	, avg_points_diff
	, upper
	, case when o.cover_p >= 0.5 then 'Over'
		   when o.cover_p < 0.5 then 'Under' 
		   else 'N/A' end as Pick 
	from 
	(
		select 
		favorite_team,
		underdog_team, 
		spread,
		formatted_spread,
		over_under,
		favorite_avg_points + favorite_opp_points as fav_diff,
		underdog_avg_points + underdog_opp_points as ud_diff, 
		(favorite_avg_points + favorite_opp_points + underdog_avg_points + underdog_opp_points) / 2 as avg_points,
		((favorite_avg_points + favorite_opp_points + underdog_avg_points + underdog_opp_points) / 2) - over_under as avg_points_diff
		 from ncaaf_current_week_stats
	 ) cws 
	  left join ncaaf_odds_static o on cast(cws.avg_points_diff as float) between cast(o.lower as float) and cast(o.upper as float)
)

select 
s.favorite_team 
, s.underdog_team
, s.formatted_spread 
, o.over_under
, s.pick as spread_pick
, o.pick as ou_pick
, s.fcs_p
, o.cover_p
 from spread s 
left join ou o on o.favorite_team = s.favorite_team 
order by s.favorite_team
 ;
 