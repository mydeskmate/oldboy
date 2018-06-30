需求:   
Django + pymysql 实现  
* 用户登录  
* 查看用户列表  


准备数据表:  
```
create database school default charset utf8;
CREATE TABLE user(
	id int auto_increment primary key,
	name VARCHAR(15),
	gender char(4)
);


```

