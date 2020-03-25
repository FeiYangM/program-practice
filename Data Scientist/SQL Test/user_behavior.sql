
###########Analysis of PV,UV and so on###########################
# pv/uv
SELECT count(distinct user_id) as 'uv', 
       (SELECT count(*) FROM userbehavior
       	where behavior = 'pv') as 'pv',
       (SELECT count(*) FROM userbehavior
       	where behavior = 'pv') / (
       	count(distinct user_id)
       	) as 'pv/uv'
FROM userbehavior;

# bounce rate
SELECT count(distinct user_id) FROM userbehavior
where user_id NOT IN(SELECT distinct user_id FROM userbehavior
                     where behavior = 'buy')
and user_id NOT IN(SELECT distinct user_id FROM userbehavior
                     where behavior = 'cart')
and user_id NOT IN(SELECT distinct user_id FROM userbehavior
                     where behavior = 'fav');

# stat
SELECT behavior, count(*) FROM userbehavior
GROUP BY behavior;

# pv, buy stat
SELECT category, sum(case when behaviro = 'pv' then 1 else 0 end) as pv_count,
                 sum(case when behaviro = 'buy' then 1 else 0 end) as buy_count,
                 sum(case when behaviro = 'cart' then 1 else 0 end) as cart_count,
                 sum(case when behaviro = 'fav' then 1 else 0 end) as fav_count
FROM userbehavior GROUP BY category ORDER BY pv_count desc;

# uv transfer
SELECT behavior, count(distinct user_id) FROM userbehavior
GROUP BY behavior;

# rate of repeat purchase
SELECT sum(concat(round(case when )))


###########Analysis of User Behavior###########################

# pv distribution in date interval
SELECT dates, count(*) FROM userbehavior
where behavior = 'pv'
GROUP BY dates
ORDER BY dates asc;


# product buy times
SELECT product_buys, count(*) as type_count
FROM (SELECT count(user_id) as product_buys 
      FROM userbehavior
      where behavior = 'buy'
      GROUP BY item_id) as product_pool
GROUP BY product_buys
ORDER BY product_buys asc;

# RFM model
SELECT user_id, 
(1 - (TIMEDIFF('2017-12-03 23:59:59', max(datetimes))) / (TIMEDIFF('2017-12-03 23:59:59', '2017-11-25 23:00:00')))
as R_score, count(*) as F_score
FROM userbehavior where behavior = 'buy'
GROUP BY user_id;