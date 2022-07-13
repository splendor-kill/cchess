import os.path
from logging import getLogger

from common.data_helper import check_best_model_notifier

logger = getLogger(__name__)


def load_best_model_weight(model):
    rc = model.config.resource
    config_path = os.path.join(rc.model_dir, rc.model_best_config_path)
    weight_path = os.path.join(rc.model_dir, rc.model_best_weight_path)
    return model.load(config_path, weight_path)


def save_as_best_model(model):
    rc = model.config.resource
    config_path = os.path.join(rc.model_dir, rc.model_best_config_path)
    weight_path = os.path.join(rc.model_dir, rc.model_best_weight_path)
    return model.save(config_path, weight_path)


def reload_best_model_weight_if_changed(model, store_util):
    rc = model.config.resource
    if model.config.model.distributed:
        changed, _ = check_best_model_notifier(store_util, rc)
        if not changed:
            return False
        logger.info('download model because it had new model')
        config_path = os.path.join(rc.model_dir, rc.model_best_config_path)
        weight_path = os.path.join(rc.model_dir, rc.model_best_weight_path)
        model.download(config_path, weight_path)
        return load_best_model_weight(model)
    else:
        logger.debug('start reload the best model if changed')
        digest = model.fetch_digest(rc.model_best_weight_path)
        if digest != model.digest:
            return load_best_model_weight(model)

        logger.debug('the best model is not changed')
        return False
