CREATE TABLE `mj_monitor_job` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `mj_id` int NOT NULL COMMENT '对应账号的 mj_id',
  `job_id` char(36) DEFAULT NULL COMMENT '唯一的 job_id，用于标识每个工作事件',
  `job_type` varchar(50) DEFAULT NULL COMMENT '作业类型，例如 "v6-1_raw_diffusion"',
  `event_type` varchar(50) DEFAULT NULL COMMENT '事件类型，例如 "variation"',
  `full_command` text COMMENT '完整的命令字符串',
  `enqueue_time` datetime DEFAULT NULL COMMENT '入队时间，记录事件被提交的时间',
  `width` int DEFAULT NULL COMMENT '图像宽度',
  `height` int DEFAULT NULL COMMENT '图像高度',
  `batch_size` int DEFAULT NULL COMMENT '批处理大小',
  `published` tinyint(1) DEFAULT NULL COMMENT '是否已发布',
  `username` varchar(50) DEFAULT NULL COMMENT '用户名，提交事件的用户',
  `user_id` char(36) DEFAULT NULL COMMENT '用户唯一标识符',
  `user_hidden` tinyint(1) DEFAULT NULL COMMENT '用户是否隐藏',
  `current_status` varchar(50) DEFAULT NULL COMMENT '当前状态，例如 "running"',
  `liked_by_user` tinyint(1) DEFAULT NULL COMMENT '用户是否喜欢此事件',
  `parent_grid` int DEFAULT NULL COMMENT '相关的父网格',
  `parent_id` char(36) DEFAULT NULL COMMENT '父事件的唯一标识符',
  `rating` int DEFAULT NULL COMMENT '事件的评分',
  `shown` tinyint(1) DEFAULT NULL COMMENT '是否已显示',
  `discord_url` varchar(255) DEFAULT NULL COMMENT '相关的 Discord URL',
  `create_source` varchar(50) DEFAULT '' COMMENT '创建来源，''discord''表示通过 Discord 创建，''site''表示官网创建',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `del_flag` char(1) NOT NULL DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
  PRIMARY KEY (`id`),
  UNIQUE KEY `job_id` (`job_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='mj监控任务列表';



CREATE TABLE `mj_account` (
  `mj_id` int NOT NULL COMMENT '对应账号的 mj_id',

  `user_id` char(36) DEFAULT NULL COMMENT '用户唯一标识符',

  `email` varchar(200) DEFAULT NULL COMMENT '邮箱',
  `token` varchar(255) DEFAULT NULL COMMENT 'Token',
  `cookie` varchar(6000) DEFAULT NULL COMMENT 'Cookie',
  `subscribe_time` datetime DEFAULT NULL COMMENT '开通时间',
  `expire_time` datetime DEFAULT NULL COMMENT '到期时间',
  `remark`  varchar(1000) DEFAULT NULL COMMENT '备注',

  `monitor_status` varchar(50) DEFAULT NULL COMMENT '监控状态',
  `last_monitor_time` datetime DEFAULT NULL COMMENT '最近监控时间',
  `error_msg` varchar(1000) DEFAULT NULL COMMENT '异常信息',


  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `del_flag` char(1) NOT NULL DEFAULT '0' COMMENT '删除标志(0代表存在 2代表删除)',

  PRIMARY KEY (`id`),
  UNIQUE KEY `mj_id` (`mj_id`),
  UNIQUE KEY `token` (`token`),
  KEY `ix_monitor_status` (`monitor_status`) USING BTREE,
  KEY `ix_email` (`email`) USING BTREE
  
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='mj账号';
