-- Create tables for univent database:
CREATE TABLE Club(
    club_name       varchar(42) NOT NULL,
    email           varchar(42) NOT NULL,
    bank_acc_info   varchar(42),

    CONSTRAINT Club_clubname_pk PRIMARY KEY (club_name)
);

CREATE TABLE Users(
    user_id         varchar(42) NOT NULL,
    club_name       varchar(42) NOT NULL,
    first_name      varchar(42) NOT NULL,
    last_name       varchar(42) NOT NULL,
    email           varchar(42) NOT NULL,
    phone_number    char(10),
    password        varchar(42) NOT NULL,
    title           varchar(42) NOT NULL,

    CONSTRAINT Users_userid_pk PRIMARY KEY (user_id),
    CONSTRAINT Users_phonenumber_cc CHECK (phone_number NOT LIKE '%[^0-9]%'),
    CONSTRAINT Users_clubname_fk FOREIGN KEY (club_name)
                                 REFERENCES Club (club_name)
                                 ON DELETE CASCADE
);

CREATE TABLE Event(
    event_name      varchar(42) NOT NULL,
    club_name       varchar(42) NOT NULL,
    time            varchar(42) NOT NULL, --Research to get time format
    event_date      varchar(42) NOT NULL, --Research to get date format
    cost            numeric(6,2) NOT NULL,
    est_attendance  numeric(3,0) NOT NULL,
    event_desc      varchar(500) NOT NULL, --Research for long entires
    primary_loc     varchar(100) NOT NULL,
    secondary_loc   varchar(100) NOT NULL,

    CONSTRAINT Event_eventname_pk PRIMARY KEY (event_name),
    CONSTRAINT Event_clubname_fk FOREIGN KEY (club_name) 
                                 REFERENCES Club (club_name)
                                 ON DELETE CASCADE,
    CONSTRAINT Event_cost_cc CHECK (cost >= 0),
    CONSTRAINT Event_estattd_cc CHECK (est_attendance >= 0)
    -- Add constraints for date and time later once I understand what to do.
);

CREATE TABLE Registers(
    event_name      varchar(42) NOT NULL,
    user_id         varchar(42) NOT NULL,
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
    user_id         varchar(42) NOT NULL,
    first_name      varchar(42) NOT NULL,
    last_name       varchar(42) NOT NULL,
    email           varchar(42) NOT NULL,
    password        varchar(42) NOT NULL,

    CONSTRAINT Ose_userid_pk PRIMARY KEY (user_id)
);

CREATE TABLE Approval(
    event_name      varchar(42) NOT NULL,
    user_id         varchar(42) NOT NULL,

    CONSTRAINT Approval_pk PRIMARY KEY (event_name, user_id),
    CONSTRAINT Approval_eventname_fk FOREIGN KEY (event_name)
                                     REFERENCES Event (event_name)
                                     ON DELETE CASCADE,
    CONSTRAINT Approval_userid_fk FOREIGN KEY (user_id)
                                  REFERENCES Ose (user_id)
                                  ON DELETE CASCADE
);
