
DROP TABLE IF EXISTS PUBLIC.events;
CREATE TABLE events
             (
                          id UUID DEFAULT Gen_random_uuid(),
                          event_date BIGINT DEFAULT Extract(epoch FROM CURRENT_TIMESTAMP) * 1000,
                          event_name TEXT NOT NULL,
                          event_address TEXT NOT NULL,
                          event_desc TEXT NOT NULL,
                          PRIMARY KEY (id,event_date)
             );