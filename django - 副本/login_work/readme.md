需求:   
Django + pymysql 实现  
* 用户登录  
* 查看用户列表  


准备数据库数据:  
```
create database school default charset utf8;
CREATE TABLE user(
	id int auto_increment primary key,
	name VARCHAR(15),
  password VARCHAR(16)
);
INSERT INTO user (name, password) VALUES ('han','123456'),('li','654321');
```

