CREATE TABLE student(Sno varchar(20) not null primary key, 
                      Sname varchar(20) not null,
                      Sbirth datetime,
                      Sex varchar(20) not null
                      );
CREATE TABLE course(Cno varchar(20) not null primary key,
                    Cname varchar(20) not null,
                    Tno Decimal(4,1)
                    );
CREATE TABLE score(Sno varchar(20) not null,
                   Cno varchar(20) not null,
                   Degree Decimal(4,1),
                   primary key(Sno, Cno));
CREATE TABLE teacher(Tno varchar(20) not null primary key,
                     Tname varchar(20));
insert into student(Sno, Sname, Sbirth, Sex) values('0001', '猴子', '1989-01-01', '男');
insert into student(Sno, Sname, Sbirth, Sex) values('0002', '猴子', '1990-12-01', '男');
insert into student(Sno, Sname, Sbirth, Sex) values('0003', '小明', '1991-12-21' , '女');
insert into student(Sno, Sname, Sbirth, Sex) values('0004', '小王', '1990-05-20', '男');

insert into score(Sno, Cno, Degree) values('0001' , '0001' , 80);
insert into score(Sno, Cno, Degree) values('0001' , '0002' , 90);
insert into score(Sno, Cno, Degree) values('0001' , '0003' , 99);
insert into score(Sno, Cno, Degree) values('0002' , '0002' , 60);
insert into score(Sno, Cno, Degree) values('0002' , '0003' , 80);
insert into score(Sno, Cno, Degree) values('0003' , '0001' , 80);
insert into score(Sno, Cno, Degree) values('0003' , '0002' , 80);
insert into score(Sno, Cno, Degree) values('0003' , '0003' , 80);


insert into course(Cno, Cname, Tno) values('0001' , '语文' , '0002');
insert into course(Cno, Cname, Tno) values('0002' , '数学' , '0001');
insert into course(Cno, Cname, Tno) values('0003' , '英语' , '0003');

insert into teacher(Tno, Tname) values('0001' , '大马哥');
insert into teacher(Tno, Tname) values('0002' , '小马哥');
insert into teacher(Tno, Tname) values('0003' , null);
insert into teacher(Tno, Tname) values('0004' , '');


# count the number of teachers named ma
SELECT count(Tno) FROM teacher where Tname like '%马%';
# count total score of 0002 class
SELECT sum(Degree) FROM score where Cno = '0002';
# the number of students with classes
SELECT count(distinct Sno) as 学生人数 FROM score;

# max and min score of each class
SELECT Cno, max(Degree) as MAX_score, min(Degree) as MIN_score 
FROM score group by Cno;

# number of student enrolled in each class
SELECT Cno, count(Sno) FROM score Group by Cno;
# count number of each sex
SELECT Sex, count(*) FROM student Group by Sex;

# average score higher than 60
SELECT Sno, avg(Degree) FROM score Group by Sno
having avg(Degree) > 60;

# students with at least two classes
SELECT Sno, count(Cno) FROM score Group by Sno
having count(Cno) > 1;

# name exists more than once
SELECT Sname FROM student Group by Sname having count(Sname) > 1;
# score lower than 90
SELECT Cno FROM score where Degree < 90 Order by Cno desc;

# order by average of each class and Cno
SELECT Cno, avg(Degree) FROM score
Group by Cno
Order by avg(Degree) asc, Cno desc;

# students with at least two classes lower than 90
SELECT Sno, avg(Degree) FROM score
where Degree < 90
Group by Sno
having count(Cno) >= 2;

# students without all of the classes
SELECT Sno, Sname FROM student
where Sno in(
SELECT Sno FROM score
GROUP BY Sno
having count(Cno) < (SELECT count(Cno) FROM course)
);

# top 2 scores in each classes
(SELECT * FROM score where Cno = '0001'ORDER BY Degree desc limit 2)
union all
(SELECT * FROM score where Cno = '0002'ORDER BY Degree desc limit 2)
union all
(SELECT * FROM score where Cno = '0003'ORDER BY Degree desc limit 2);

# query number, name, total classes and total grades for each student
SELECT a.Sno, a.Sname, count(b.Cno), sum(b.Degree)
FROM student as a LEFT JOIN score as b
on a.Sno = b.Sno
GROUP BY a.Sno;

# query students with average score > 60
SELECT a.Sno, a.Sname, avg(b.Degree)
FROM student as a LEFT JOIN score as b
on a.Sno = b.Sno
GROUP BY a.SNO
having avg(b.Degree) > 60;

# query classes of students
SELECT a.Sno, a.Sname, c.Cno, c.Cname 
FROM student as a inner JOIN score as b
on a.Sno = b.Sno
inner JOIN course as c
on b.Cno = c.Cno;

# number of pass or fail for each class
SELECT Cno, sum(case when Degree >= 60 then 1
                     else 0
                end) as pass_n,
            sum(case when Degree < 60 then 1
                     else 0
                end) as non_pass
FROM score
GROUP BY Cno;

# count numbers scored in 60-85 and 85-100
SELECT a.Cno, b.Cname,
       sum(case when a.Degree between 85 and 100 then 1
                else 0
           end) as '85-100',
       sum(case when a.Degree >=60 and a.Degree<85 then 1
                else 0
           end) as '60-85'
FROM score as a 
RIGHT JOIN course as b
on a.Cno = b.Cno
GROUP BY a.Cno, b.Cname;

# query student scored > 80
SELECT a.Sno, a.Sname FROM student as a
RIGHT JOIN score as b
on a.Sno = b.Sno
where b.Cno = '0003' and b.Degree > 80;





