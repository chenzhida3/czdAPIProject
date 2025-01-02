from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '用户id',
    `username` VARCHAR(50) NOT NULL  COMMENT '用户名',
    `password` VARCHAR(128) NOT NULL  COMMENT '密码',
    `email` VARCHAR(50) NOT NULL  COMMENT '邮箱',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `is_superuser` BOOL NOT NULL  COMMENT '是否是超级管理员' DEFAULT 0
) CHARACTER SET utf8mb4 COMMENT='用户表';
CREATE TABLE IF NOT EXISTS `test_file` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '文件id',
    `file` VARCHAR(100) NOT NULL  COMMENT '文件路径',
    `info` JSON   COMMENT '文件信息',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0
) CHARACTER SET utf8mb4 COMMENT='测试文件表';
CREATE TABLE IF NOT EXISTS `test_project` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '项目id',
    `name` VARCHAR(50) NOT NULL  COMMENT '项目名称',
    `leader` VARCHAR(20) NOT NULL  COMMENT '负责人',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0
) CHARACTER SET utf8mb4 COMMENT='项目表';
CREATE TABLE IF NOT EXISTS `test_env` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '环境id',
    `global_variables` JSON   COMMENT '全局变量',
    `debug_global_variable` JSON   COMMENT '调试模式全局变量',
    `db` JSON   COMMENT '数据库配置',
    `headers` JSON   COMMENT '全局请求头',
    `global_func` LONGTEXT   COMMENT '全局工具函数',
    `name` VARCHAR(50) NOT NULL  COMMENT '测试环境名称',
    `host` VARCHAR(50) NOT NULL  COMMENT '测试环境的host地址',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `project_id` INT NOT NULL,
    CONSTRAINT `fk_test_env_test_pro_f21b8019` FOREIGN KEY (`project_id`) REFERENCES `test_project` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='环境表';
CREATE TABLE IF NOT EXISTS `interface_manager` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '接口id',
    `name` VARCHAR(50) NOT NULL  COMMENT '接口名称',
    `url` VARCHAR(200) NOT NULL  COMMENT '接口地址',
    `method` VARCHAR(50) NOT NULL  COMMENT '请求方法',
    `type` VARCHAR(50) NOT NULL  COMMENT '接口类型' DEFAULT '1',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `project_id` INT NOT NULL COMMENT '所属项目',
    CONSTRAINT `fk_interfac_test_pro_e885d8d6` FOREIGN KEY (`project_id`) REFERENCES `test_project` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='接口管理';
CREATE TABLE IF NOT EXISTS `interface_case` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '接口id',
    `title` VARCHAR(50) NOT NULL  COMMENT '用例标题',
    `headers` JSON   COMMENT '请求头',
    `request` JSON   COMMENT '请求参数',
    `file` JSON   COMMENT '文件参数',
    `setup_script` LONGTEXT   COMMENT '前置脚本',
    `teardown_script` LONGTEXT   COMMENT '后置脚本',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `interface_id` INT NOT NULL COMMENT '所属接口',
    CONSTRAINT `fk_interfac_interfac_059a21c4` FOREIGN KEY (`interface_id`) REFERENCES `interface_manager` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='接口用例';
CREATE TABLE IF NOT EXISTS `test_scenes` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '业务流id',
    `name` VARCHAR(50) NOT NULL  COMMENT '业务流名称',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `project_id` INT NOT NULL COMMENT '所属项目',
    CONSTRAINT `fk_test_sce_test_pro_ba40e5e0` FOREIGN KEY (`project_id`) REFERENCES `test_project` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='业务流表';
CREATE TABLE IF NOT EXISTS `scene_to_case` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '业务流id',
    `sort` INT   COMMENT '排序',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `icase_id` INT NOT NULL COMMENT '接口用例',
    `scene_id` INT NOT NULL COMMENT '业务流',
    CONSTRAINT `fk_scene_to_interfac_3bafe8ea` FOREIGN KEY (`icase_id`) REFERENCES `interface_case` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_scene_to_test_sce_20ba29d0` FOREIGN KEY (`scene_id`) REFERENCES `test_scenes` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='业务流和接口用例中间表';
CREATE TABLE IF NOT EXISTS `test_task` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '任务id',
    `name` VARCHAR(50) NOT NULL  COMMENT '任务名称',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `project_id` INT NOT NULL COMMENT '所属项目',
    CONSTRAINT `fk_test_tas_test_pro_dbda564e` FOREIGN KEY (`project_id`) REFERENCES `test_project` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='测试任务';
CREATE TABLE IF NOT EXISTS `test_record` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '记录id',
    `all` INT NOT NULL  COMMENT '总用例数' DEFAULT 0,
    `success` INT NOT NULL  COMMENT '成功用例数' DEFAULT 0,
    `fail` INT NOT NULL  COMMENT '失败用例数' DEFAULT 0,
    `error` INT NOT NULL  COMMENT '错误用例数' DEFAULT 0,
    `pass_rate` DOUBLE NOT NULL  COMMENT '通过率' DEFAULT 0,
    `tester` VARCHAR(50) NOT NULL  COMMENT '执行人',
    `statues` VARCHAR(50) NOT NULL  COMMENT '运行状态',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `env_id` INT NOT NULL COMMENT '关联环境',
    `task_id` INT NOT NULL COMMENT '关联任务',
    CONSTRAINT `fk_test_rec_test_env_1bf08e6d` FOREIGN KEY (`env_id`) REFERENCES `test_env` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_test_rec_test_tas_1048b413` FOREIGN KEY (`task_id`) REFERENCES `test_task` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='运行记录';
CREATE TABLE IF NOT EXISTS `test_report` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '报告id',
    `info` JSON NOT NULL  COMMENT '报告信息',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `record_id` INT NOT NULL UNIQUE COMMENT '关联测试记录',
    CONSTRAINT `fk_test_rep_test_rec_8a1a7ffa` FOREIGN KEY (`record_id`) REFERENCES `test_record` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='测试报告';
CREATE TABLE IF NOT EXISTS `test_task_test_scenes` (
    `test_task_id` INT NOT NULL,
    `testscene_id` INT NOT NULL,
    FOREIGN KEY (`test_task_id`) REFERENCES `test_task` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`testscene_id`) REFERENCES `test_scenes` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uidx_test_task_t_test_ta_691a0f` (`test_task_id`, `testscene_id`)
) CHARACTER SET utf8mb4 COMMENT='关联业务流';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
