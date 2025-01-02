from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `cron_job` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '任务id',
    `name` VARCHAR(50) NOT NULL  COMMENT '任务名称',
    `rule` VARCHAR(50) NOT NULL  COMMENT '执行的规则',
    `status` BOOL NOT NULL  COMMENT '状态' DEFAULT 0,
    `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `env_id` INT NOT NULL COMMENT '关联环境',
    `project_id` INT NOT NULL COMMENT '所属项目',
    `task_id` INT NOT NULL COMMENT '执行任务',
    CONSTRAINT `fk_cron_job_test_env_419918e4` FOREIGN KEY (`env_id`) REFERENCES `test_env` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_cron_job_test_pro_8b210413` FOREIGN KEY (`project_id`) REFERENCES `test_project` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_cron_job_test_tas_4b48673f` FOREIGN KEY (`task_id`) REFERENCES `test_task` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='定时任务';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `cron_job`;"""
