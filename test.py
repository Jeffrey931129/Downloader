import logging

logging.basicConfig(filename='note.log', level=logging.DEBUG, format='[%(levelname)s] %(message)s (%(asctime)s)')

logging.info("test")