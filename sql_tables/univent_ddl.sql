-- Drop existing tables
DROP TABLE IF EXISTS Club, Users, Members, Event, Registers, OSE, Approval;

-- Create tables for univent database:
CREATE TABLE Club(
    club_name       varchar(42) NOT NULL,
    email           varchar(42) NOT NULL,
    bank_acc_info   varchar(42),

    CONSTRAINT Club_clubname_pk PRIMARY KEY (club_name)
);

CREATE TABLE Users(
    user_id         SERIAL NOT NULL,
    -- club_name       varchar(42),
    first_name      varchar(42) NOT NULL,
    last_name       varchar(42) NOT NULL,
    email           varchar(42) UNIQUE NOT NULL,
    -- phone_number    char(10),
    password        varchar(42) NOT NULL,
    -- title           varchar(42) NOT NULL,
    user_type       numeric(1,0) NOT NULL,

    CONSTRAINT Users_userid_pk PRIMARY KEY (user_id)
    --CONSTRAINT Users_phonenumber_cc CHECK (phone_number NOT LIKE '%[^0-9]%'),
    --CONSTRAINT Users_clubname_fk FOREIGN KEY (club_name)
                                 --REFERENCES Club (club_name)
                                 --ON DELETE CASCADE

);

CREATE TABLE Members(
    user_id         INTEGER NOT NULL,
    title           varchar(42) NOT NULL,
    club_name       varchar(42) NOT NULL,
    phone_number    char(10) NOT NULL,
    
    CONSTRAINT Members_userid_pk PRIMARY KEY (user_id),
    CONSTRAINT Members_phonenumber_cc CHECK (phone_number NOT LIKE '%[^0-9]%'),
    CONSTRAINT Members_clubname_fk FOREIGN KEY (club_name)
                                 REFERENCES Club (club_name)
                                 ON DELETE CASCADE,
    CONSTRAINT Members_userid_fk FOREIGN KEY (user_id)
                                 REFERENCES Users(user_id)
                                 ON DELETE CASCADE
);

-- Create trigger function
CREATE OR REPLACE FUNCTION check_user_type_and_club_name()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM Users u
        WHERE u.user_id = NEW.user_id
          AND u.user_type = 1
    ) THEN
        IF NEW.club_name IS NULL THEN
            -- Trigger actions go here
            -- Replace with the desired actions
            RAISE EXCEPTION 'User with user_id % has user_type = 1 and no associated club_name in Members table', NEW.user_id;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER user_type_and_club_name_trigger
AFTER INSERT OR UPDATE ON Members
FOR EACH ROW
EXECUTE FUNCTION check_user_type_and_club_name();

-- -- Create trigger function
-- CREATE OR REPLACE FUNCTION check_user_type_and_club_name()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     IF NEW.user_type = 1 AND
--        (SELECT club_name FROM Members WHERE user_id = NEW.user_id) IS NULL THEN
--         RAISE EXCEPTION 'User with user_id % has user_type = 1 and no associated club_name in Members table', NEW.user_id;
--     END IF;
    
--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;

-- -- Create the trigger
-- CREATE TRIGGER user_type_and_club_name_trigger
-- AFTER INSERT OR UPDATE ON Members
-- FOR EACH ROW
-- EXECUTE FUNCTION check_user_type_and_club_name();


-- CREATE OR REPLACE FUNCTION enforce_club_name_not_null()
-- RETURNS TRIGGER AS $$
-- BEGIN
--   IF NEW.user_type = 1 AND NEW.club_name IS NULL THEN
--     RAISE EXCEPTION 'Club name cannot be null for users with type 1';
--   END IF;
--   RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER club_name_not_null_trigger
-- BEFORE INSERT OR UPDATE ON Members
-- FOR EACH ROW
-- EXECUTE FUNCTION enforce_club_name_not_null();

CREATE TABLE Event(
    event_name      varchar(42) NOT NULL,
    club_name       varchar(42) NOT NULL,
    event_time      TIME NOT NULL,
    event_date      DATE NOT NULL,
    est_attendance  numeric(3,0) NOT NULL,
    event_desc      varchar(502) NOT NULL,
    primary_loc     varchar(100) NOT NULL,
    secondary_loc   varchar(100) NOT NULL,
    cost            numeric(6,2),

    CONSTRAINT Event_eventname_pk PRIMARY KEY (event_name),
    CONSTRAINT Event_clubname_fk FOREIGN KEY (club_name) 
                                 REFERENCES Club (club_name)
                                 ON DELETE CASCADE,
    CONSTRAINT Event_cost_cc CHECK (est_attendance >= 0 AND est_attendance <= 999),
    CONSTRAINT Event_estattd_cc CHECK (cost >= 0 AND cost <= 9999.99)
    -- Add constraints for date and time later once I understand what to do.
);

CREATE TABLE Registers(
    event_name      varchar(42) NOT NULL,
    user_id         INTEGER NOT NULL,
    space_res_form  varchar(42) NOT NULL, --Research for better desc.
    event_res_form  varchar(42) NOT NULL, --Research for better desc.

    CONSTRAINT Registers_eventname_fk FOREIGN KEY (event_name)
                                      REFERENCES Event (event_name)
                                      ON DELETE CASCADE,
    CONSTRAINT Registers_userid_fk FOREIGN KEY (user_id)
                                   REFERENCES Users (user_id)
                                   ON DELETE CASCADE
);


CREATE TABLE Ose(
    user_id         INTEGER NOT NULL,
    first_name      varchar(42) NOT NULL,
    last_name       varchar(42) NOT NULL,
    email           varchar(42) NOT NULL,
    password        varchar(42) NOT NULL,

    CONSTRAINT Ose_userid_pk PRIMARY KEY (user_id)
);

CREATE TABLE Approval(
    event_name      varchar(42) NOT NULL,
    user_id         INTEGER NOT NULL,

    CONSTRAINT Approval_pk PRIMARY KEY (event_name, user_id),
    CONSTRAINT Approval_eventname_fk FOREIGN KEY (event_name)
                                     REFERENCES Event (event_name)
                                     ON DELETE CASCADE,
    CONSTRAINT Approval_userid_fk FOREIGN KEY (user_id)
                                  REFERENCES Users (user_id)
                                  ON DELETE CASCADE
);