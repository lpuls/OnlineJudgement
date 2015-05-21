__author__ = 'xp'


class DATA:
    # the path of codes, exes, shell, and error log file in docker
    HOST_CODES_PATH = '/home/xp/codes'
    HOST_EXES_PATH = '/home/xp/exes'
    HOST_SHELL_PATH = '/home/xp/shellFiles'
    HOST_ERROR_LOG_PATH = '/home/xp/ErrorLog'

    # the path of codes, exes, and shell in docker
    DOCKER_CODES_PATH = '/home/codes'
    DOCKER_EXES_PATH = '/home/exes'
    DOCKER_SHELL_PATH = '/home/shellFiles'

    # the times of judgment
    JUDGEMENT_TIMES = 5

    # the number of judgment thread
    THREAD_TOTAL = 1

    # the image name of docker which will be used
    DOCKER_IMAGE_NAME = 'xpsama/xp_oj_compile:v1.2'

    # the result of online judgement
    WAITING = 'Waiting'
    COMPILE_ERROR = 'Compile Error'
    MEMORY_LIMIT_EXCEEDED = 'Memory Limit exceeded'
    TIME_LIMIT_EXCEEDED = 'Time Limit Exceeded'
    RUNTIME_ERROR = 'Runtime error'
    WRONG_ANSWER = 'Wrong Answer'
    OUTPUT_LIMIT_EXCEEDED = 'Output Limit Exceeded'
    PRESENTATION_ERROR = 'Presentation Error'
    ACCEPT = 'Accept'

    # the number total of system out
    RESULT_LINES_MORE = 5

    # the sleep time of Manufacture
    MANUFACTURE_SLEEP_TIME = 5