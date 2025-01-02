from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `cron_job` ADD `job_id` VARCHAR(50)   COMMENT '任务id';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `cron_job` DROP COLUMN `job_id`;"""
