-- select * from allData;
-- select * from myQueue;
select * from applyQueue;
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
