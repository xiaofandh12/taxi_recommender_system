drop view beijing_taxi_201211_trajectories_view_20121101

create view trajectories_view_20121104
as
select * from taxi_tracks_occupied_crusing_20121104 where id in (
select track_id from taxi_tracks_attr_20121104 where 
total_length <= 80 and 
max_length < 2 and 
total_tracks_cuid_count < 100 and 
o_total_tracks_cuid_count > 2 and 
c_total_tracks_cuid_count > 2)
