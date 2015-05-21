create database XPOJ;
use XPOJ;
drop table Question;
create table Question(
	id int primary key auto_increment,
	name varchar(50) not null,
	context TEXT not null,
	time numeric default 1000,
	ram numeric default 65536,
    point int default 1,
    submitTotal int default 1,
    acceptTOtal int default 0
)engine=INNODB auto_increment=0000 default charset=gbk;
select * from Question;
insert into Question (name, context, time, ram) value ('plus', 'Asked to enter a and b, and the output b,Input 10, 20, Output 30',1,1);
insert into Question (name, context, time, ram, point) value ('plus', '输入一串数字，然后按从小到大的顺序输出\n输入：\n5(有多少个数字)\n7，5，6，1，3\n输出：\n1，3，5，6，7,',1,1,10);
drop table Users;
create table Users(
	user_id varchar(20) primary key,
	user_name varchar(50) not null,
	user_password varchar(50) not null,
	user_school varchar(100),
    user_point int default 0
);
select * from Users;
insert into Users (user_id, user_name, user_password, user_school) value ('root', 'admin', 'rootadmin', 'TKK');
insert into Users (user_id, user_name, user_password, user_school) value ('xp','xp','085850','TKK');
create table Submit(
	user_id varchar(20),
	question_id int,
	submit_time time not null,
	type varchar(10) default 'C++',
	codeName varchar(100) primary key,
	result varchar(30) not null default 'Waiting',
	constraint fk_user_id foreign key (user_id) references Users(user_id),
	constraint fk_question_id foreign key (question_id) references Question(id)
);
select * from Submit;
insert into Submit (user_id, question_id, submit_time, type, codeName, result) value ('xp',1,'2015-06-06 12:23:23','cpp','xp_0000_20150606122323_cpp','waiting');
insert into Submit (user_id, question_id, submit_time, type, codeName, result) value ('xp',1,'2015-05-15 22:24:00','cpp','xp_0000_20150515222400_cpp','waiting');
insert into Submit (user_id, question_id, submit_time, type, codeName, result) value ('xp',1,'2015-06-06 12:23:24','cpp','xp_0000_20150606122324_cpp','waiting');
insert into Submit (user_id, question_id, submit_time, type, codeName, result) value ('xp',1,'2015-06-06 12:23:25','cpp','xp_0000_20150606122325_cpp','waiting');
drop table TestData;
create table TestData(
	question_id int,
    test_data varchar(100),
    result_data varchar(100),
    constraint fk_question_id_TD foreign key (question_id) references Question(id)
);
select * from TestData;
insert into TestData (question_id, test_data, result_data) value (1,'[1,1]','[2]');
insert into TestData (question_id, test_data, result_data) value (1,'[-1,-1]','[-2]');
insert into TestData (question_id, test_data, result_data) value (1,'[10,10]','[20]');
insert into TestData (question_id, test_data, result_data) value (1,'[65530,1]','[65531]');
insert into TestData (question_id, test_data, result_data) value (1,'[-65530,1]','[-65529]');
insert into TestData (question_id, test_data, result_data) value (1,'[0,0]','[0]');
insert into TestData (question_id, test_data, result_data) value (1,'[10,0]','[10]');
insert into TestData (question_id, test_data, result_data) value (1,'[0,10]','[10]');
insert into TestData (question_id, test_data, result_data) value (1,'[-1,1]','[0]');
insert into TestData (question_id, test_data, result_data) value (1,'[1,-1]','[0]');
alter table Question add column submitTotal int not null default 1;
alter table Question add column acceptTotal int not null default 0;
