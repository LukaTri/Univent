--Insert users into the database. This application works as if you cannot
--create your own profile. This is done theoretion works as if you cannot
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
INSERT INTO Users (first_name, last_name, email, password, user_type) VALUES (
    --user_id
    -- first_name
    'K',
    --last_name
    'Hirageto',
    -- user_email
    'user@email.com',
    -- user_pwd
    'password',
    -- user_type
    '1'
);

INSERT INTO Members (user_id, title, club_name, phone_number) VALUES(
    '1',
    'President',
    'nomad',
    '2017234808'
);

INSERT INTO Users (first_name, last_name, email, password, user_type) VALUES (
    -- first_name
    'Luka',
    --last_name
    'Trikha',
    -- user_email
    'lutri001@goucher.edu',
    -- user_pwd
    'password',
    -- user_type
    '0'
);