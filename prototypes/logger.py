import logging


def init_logger():
    logger = logging.getLogger('WalkieTalkie')
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    #formatter = logging.Formatter('%(asctime)s : %(name)s : %(filename)s : [%(levelname)s] : %(message)s')
    formatter = logging.Formatter(
        '%(asctime)s : %(filename)s : [%(levelname)s] : %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
