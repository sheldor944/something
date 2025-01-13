import sys
import logging

#logger
logger = logging.getLogger(__name__)

#formatter
formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')

#standard output handler
stdout_handler = logging.StreamHandler(sys.stdout)

#set formatter
stdout_handler.setFormatter(formatter)

#add handler to logger
logger.handlers =[stdout_handler]

#set log level
logger.setLevel(logging.INFO)