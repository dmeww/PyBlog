-- blog = Blog()
--         blog.bid = int(target[0])
--         blog.content = target[1]
--         blog.title = target[2]
--         blog.uid = int(target[3])
--         blog.date = target[4]
--         blog.umail = target[5]
--         blog.status = int(target[6])
--         blog.comment = int(target[7])
--         blog.report = int(target[8])

create table blog
(
    bid     bigint auto_increment primary key comment 'ID主键',
    content varchar(5000) comment '文章主体',
    title   varchar(50) comment '文章标题',
    uid     bigint comment '作者ID',
    date    varchar(30) comment '发布日期',
    umail   varchar(30) comment '用户邮箱',
    status  int comment '用户状态',
    comment int comment '评论数量',
    report  int comment '举报数量'
);


# comment = Comment()
#         comment.id = int(target[0])
#         comment.content = target[1]
#         comment.umail = target[2]
#         comment.bid = int(target[3])

create table comment
(
    id      bigint auto_increment primary key comment '评论ID',
    content varchar(300) comment '评论内容',
    umail   varchar(30) comment '评论者邮箱',
    bid     bigint comment '评论者ID'

);

# User(uid=int(target[0]),
#     password=target[1],
#     mail=target[2],
#     status=int(target[3]),
#         report=int(target[4]))

create table user
(
    uid      bigint auto_increment primary key comment '用户ID',
    password varchar(30) comment '用户密码',
    mail     varchar(30) comment '用户邮箱',
    status   int comment '用户状态',
    report   int comment '用户举报数'
);





