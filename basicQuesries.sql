-- select * from allData;
-- select * from myQueue;
select * from users;
-- select * from allData;
-- 246b456b-2d82-4dbd-8188-bc53c35c916a, 172365841217201568
-- 842f26be-ed93-4857-bb1e-e902a53108e9
-- delete from applyQueue;
-- insert into applyQueue(jobID, timeOfArrival, selectedResume, email)
-- VALUES ('4d192376-adba-4935-9d33-9b71c9762a2d', 1721590222, '1723586578999306174', 'utsav28.devops@gmail.com'),
-- ('ce1c0a99-c51a-414d-bc8e-72c646ab8f8e', 1721590222, '1723586578999306174', 'utsav28.devops@gmail.com'),
-- ('d597dddc-9b46-404d-9924-f949d82463f2', 1721590222, '1723586591906099998', 'utsav28.devops@gmail.com'),
-- ('95e77b13-dccf-44ec-9422-18d1a40610ff', 1721590222, '1723586591906099998', 'utsav28.devops@gmail.com'),
-- ('b512c11d-2560-4765-a9f7-3b9c82b7cd23', 1721590222, '1723586591906099998', 'utsav28.devops@gmail.com'),
-- ('e6022679-fdc0-4159-acaa-ec5f09331a6d', 1721590222, '1723586591906099998', 'utsav28.devops@gmail.com'),
-- ('c6899560-9f8e-48a8-af9a-309470d28986', 1721590222, '1723586591906099998', 'utsav28.devops@gmail.com'),
-- ('7bf49866-8db7-4fa4-ad4d-eddf611ce8a0', 1721590222, '1723586591906099998', 'utsav28.devops@gmail.com')
select * from applyQueue;
-- DECLARE @currentUnixTimestamp BIGINT;
-- SET @currentUnixTimestamp = DATEDIFF(SECOND, '1970-01-01T00:00:00Z', GETUTCDATE());
-- DECLARE @timestamp24HoursAgo BIGINT;
-- SET @timestamp24HoursAgo = @currentUnixTimestamp - (5 * 60 * 60);
-- DELETE FROM allData
-- WHERE dateUpdated < @timestamp24HoursAgo;

-- delete from applyQueue where email = 'utsav28.devops@gmail.com'
-- SELECT dice_password FROM users WHERE email = 'utsav28.devops@gmail.com';
-- insert into resumeList (resumeId, resumeName, email)
-- VALUES ('1723493740408406275', 'Python Amit Resume', 'aluhar@gmail.com')
-- select * from resumeList;
-- select COUNT(*) from allData;
-- select COUNT(*) from myQueue;
-- select COUNT(*) from applyQueue;

-- select * from scoreBoard;
-- select COUNT(*) from resumeList;

-- SAFE!! Delete Table DATA
-- DELETE FROM applyQueue;
-- DELETE FROM myQueue;
-- DELETE FROM allData;
-- DELETE FROM resumeList;

-- LAVDA LAGI JASE!! Delete Whole TABLE
-- DROP TABLE applyQueue;
-- DROP TABLE myQueue;
-- DROP TABLE allData;
-- DROP TABLE resumeList;
-- DROP TABLE scoreBoard;


-- SELECT score FROM scoreBoard where contender = 'theMachine';

-- QUERY TO SHOW ALL THE MYQUEUE DATA
-- select allData.id, allData.title, applyQueue.timeOfArrival from allData JOIN applyQueue ON allData.id = applyQueue.id ORDER BY applyQueue.timeOfArrival ASC;
-- SELECT COUNT(*) FROM allData JOIN myQueue ON allData.id = myQueue.id;

-- INSERT INTO allData (id, title, location, company, description, datePosted, dateUpdated, myStatus, decisionTime)
-- VALUES ('11111', 'this Is Title', 'location', 'company', 'description', 1721590526, 1721590528, 'pending', NULL);

-- CREATE TABLE scoreBoard(
--     contender VARCHAR(255) PRIMARY KEY,
--     score INT    
-- );

-- INSERT INTO scoreBoard (contender, score)
-- VALUES ('theMachine', 0);

-- SELECT * FROM scoreBoard;
-- SELECT score FROM scoreBoard where contender = 'theMachine';
