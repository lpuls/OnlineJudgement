# OnlineJudgement

## 这是一个在线测评系统：
  1. 能够进行代码的编译（解释）
  
  2. 以Docket为沙盒，确定外部提交的代码不会影响到服务器运行
  
  3. 自得运行代码，并能通过数据库的测试数据与结果，对运行的输出进行正确性匹配
  
  4. 多线程运行，确定大量提交数据时不会出现塞阻
  
  
## 安装说明
  1. 以Python作为主要开发语言，请确定运行环境有Python
  
  2. 以Mysql作为数据库，请确认运行环境安装有Mysql，若不存在，则可执行如下操作（以Ubuntu为例）
   > sudo apt-get install mysql-server<br>
   > apt-get isntall mysql-client<br>
   > sudo apt-get install libmysqlclient-dev<br>
   > mysql -u 用户名 -p 数据库名 < DataBaseSQL.sql（该操作会创建所需要的数据表，并导入部份测试用题目）<br>
  
  3. 本程序以Docket作为沙盒系统，因此请确认运行环境有Docker，若不存在，则可执行如下操作
  
  4. 启动Docker后，创建容器，并安装所需要的编译环境和运行环境，用于测评时的编译与运行
  
  5. 执行python Codes/MAIN.py，以运行OJ程序

   
## 关于前端
  前端虽然有开发，但本人对于Web方面的知识有所欠缺，因此不推荐使。
  
  
  
