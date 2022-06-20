def get_store_util(resource_config):
    which_storage = resource_config.distributed_storage
    if which_storage == 's3':
        from common.store_s3 import S3Helper
        return S3Helper(resource_config.model_best_distributed_s3_url,
                        resource_config.model_best_distributed_s3_access_key,
                        resource_config.model_best_distributed_s3_secret_key,
                        resource_config.model_best_distributed_s3_bucket
                        )
    elif which_storage == 's3_omnitool':
        from common.store_omnitool import S3Helper
        return S3Helper(resource_config.model_best_distributed_s3_url,
                        resource_config.model_best_distributed_s3_access_key,
                        resource_config.model_best_distributed_s3_secret_key,
                        resource_config.model_best_distributed_s3_bucket
                        )
    elif which_storage == "ftp":
        from common.store_ftp import FTPHelper
        return FTPHelper(resource_config.model_best_distributed_ftp_server,
                         resource_config.model_best_distributed_ftp_user,
                         resource_config.model_best_distributed_ftp_password,
                         resource_config.model_best_distributed_ftp_remote_path)
