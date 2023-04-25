--Insert users into the database. This application works as if you cannot
--create your own profile. This is done theoretically by Goucher IT

-- Delete all prior entries
DELETE FROM Approval;
DELETE FROM Club;
DELETE FROM Users;
DELETE FROM Event;
DELETE FROM Registers;
DELETE FROM Ose;

--Insert Clubs first:
INSERT INTO Club VALUES(
    --club_name
    'nomad',
    --club_email
    'club@email.com'
    --bank account info (optional)
    --'varchar(42)'
);

--Insert Club Members second:
INSERT INTO Users (first_name, last_name, email, phone_number, password, title, user_type) VALUES (
    --user_id
    --'001',
    -- club_name (fk)
    --'nomad',
    -- first_name
    'john',
    --last_name
    'doe',
    -- user_email
    'user@email.com',
    -- user pn
    '2017234808',
    -- user_pwd
    'password',
    -- user_title
    'president',
    -- user_type
    '0'
);
INSERT INTO Users (first_name, last_name, email, phone_number, password, title, user_type) VALUES (
    --user_id
    --'003',
    -- club_name (fk)
    --'nomad',
    -- first_name
    'john',
    --last_name
    'doe',
    -- user_email
    'testuser@email.com',
    -- user pn
    '2017234808',
    -- user_pwd
    'password',
    -- user_title
    'president',
    -- user_type
    '0'
);


--Insert Event third:
INSERT INTO Event VALUES(
    --event_name
    'Culture Day',
    --club_name (fk)
    'nomad',
    --time
    '12:00',
    --date
    '2023/04/01',
    --cost
    '10',
    --est_attendance
    '10',
    --event_description
    'the event is cool',
    --primary_location
    'heubeck hall',
    --secondary_location
    'ath'
);

INSERT INTO Event VALUES(
    'Career Day',
    'nomad',
    '24:00',
    '2023/06/26',
    '9999.99',
    '999',
    'this event is to celebrate culture.',
    'Ath',
    'Mary Fisher'
);

--Insert Registers Fourth:
INSERT INTO Registers VALUES(
    --event_name (fk)
    'Culture Day',
    --user_id (fk)
    '001',
    --space_reg_form
    'space form',
    --event_reg_form
    'event form'
);

--Insert OSE Fifth:
INSERT INTO Ose VALUES(
    --user_id
    '002',
    --first_name
    'jane',
    --last_name
    'moe',
    --ose_email
    'ose@email.com',
    --password
    'password2'
);

--Insert Approval Sixth:
INSERT INTO Approval VALUES(
    --event_name (fk)
    'Culture Day',
    --user_id (fk)
    '002'
);
