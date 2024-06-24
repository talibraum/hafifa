WITH cte_date_range
     AS (SELECT id,
                event_date,
                event_name,
                event_address,
                event_desc
         FROM   PUBLIC.events
         WHERE  event_date BETWEEN 0 AND 1719216726488),
     cte_get_last_update
     AS (SELECT id,
                Max(event_date) AS latest_update
         FROM   cte_date_range
         GROUP  BY id)
SELECT all_events.id,
       all_events.event_date,
       all_events.event_name,
       all_events.event_address,
       all_events.event_desc
FROM   PUBLIC.events AS all_events
       INNER JOIN cte_get_last_update AS filtered_events
               ON all_events.id = filtered_events.id
                  AND all_events.event_date = filtered_events.latest_update;