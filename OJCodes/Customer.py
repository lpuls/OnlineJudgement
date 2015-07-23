# _*_ coding:utf-8 _*_
__author__ = 'xp'

import time
import random

from Log import Log
from PathData import DATA
from ShellCreater import ShellCreater
from DockerRunner import DockerRunner
from Manufacturer import Manufacturer
from TimeSuperivsor import TimeSupervisor
from AnalysisResult import AnalysisResult
from OJDataBaseAdministrator import OJDataBaseAdministrator as OJDBA


class Customer:
    def __init__(self):
        self.__timeSupervisor = TimeSupervisor(container_id=None, time_limit=DATA.CONTAINER_LIFETIME)

    # this function is used to compile the code and return compile result
    def compile(self, submit):
        Log.customer_log('CUSTOMER: Start Compile')
        shell = ShellCreater.create_compile_shell(submit.get_code_name(), submit.get_code_name(), submit.get_language_type())
        container = DockerRunner.getInstance().createContainer('COMPILE')
        result = DockerRunner.getInstance().exec_command(container=container,
                                                        cmd='.' + DATA.DOCKER_SHELL_PATH + '/' + shell.get_name())
        DockerRunner.getInstance().remove_container(container=container)
        Log.customer_log('CUSTOMER: Over Compile')
        Log.customer_log('CUSTOMER: COMPILE RESULT : \n' + str(result))
        if result is not None:
            if AnalysisResult.compile_analysis(result=result):
                return True
        return False

    # this function is used to calling docker and run the program
    def run_program(self, exe_name, interpreter, question, param=[]):
        shell = ShellCreater.create_run_shell(exe_name=exe_name, interpreter=interpreter, question=question, param=param)
        container = DockerRunner.getInstance().createContainer('RUN')

        # set containerID of __timeSupervisor
        self.__timeSupervisor.set_container_id(container_id=container)

        # run docker and get result of program which running
        self.__timeSupervisor.reset()
        self.__timeSupervisor.start()
        result = DockerRunner.getInstance().exec_command(container=container,
                                                        cmd='.' + DATA.DOCKER_SHELL_PATH + '/' + shell.get_name())
        self.__timeSupervisor.stop()
        # remove running container which running program
        Log.customer_log('Remove Container')
        DockerRunner.getInstance().remove_container(container=container)
        Log.customer_log('Remove success')
        # verification result
        return result

    # TODO 评测线程
    # the function of judgement thread
    def consumption(self):
        Log.customer_log('CUSTOMER: Start This Thread......')
        while True:
            Log.customer_log('-----------------------------------------------------------------------------------------')
            try:
                Log.customer_log('CUSTOMER: Start......')
                submit = Manufacturer.getInstance().get_queue_head()
                if submit is None:
                    Log.customer_log('CUSTOMER: None Data')
                    time.sleep(3)
                    continue
                Log.customer_log('CUSTOMER: The submit code name is : ' + str(submit.get_code_name()))
                # TODO 评测中的编译
                # 若成功则继续执行，否则回写代码
                if self.compile(submit):
                    Log.customer_log('CUSTOMER: Compile......')
                    question = OJDBA.get_question(submit.get_question_id())
                    test_datas = OJDBA.get_test_data_by_question_id(submit.get_question_id())
                    # 若测试案例小于系统定的测试次数，则只运行测试案例的数量，否则进行系统测试次数
                    test_time = len(test_datas) if len(test_data) < DATA.JUDGEMENT_TIMES else DATA.JUDGEMENT_TIMES
                    test_datas_length = len(test_datas)
                    accept_total = 0  # AC的总次数
                    run_time_total = 0  # 程序运行次数
                    # 评测程序5次并且每次的结果都是AC，则将其写回数据库
                    # TODO 评测过程
                    for i in range(0, test_time):
                        Log.customer_log('CUSTOMER: ------------------------------------------------')
                        # get a random position and choose a test Data by this position
                        test_data_position = random.randint(0, test_datas_length-1)
                        test_data = test_datas[test_data_position]
                        test_datas[test_data_position] = test_datas[test_datas_length-1]
                        test_datas_length -= 1
                        # run the program and get the result
                        Log.customer_log('CUSTOMER: Start......')
                        result = self.run_program(submit.get_code_name(), submit.get_language_type(),
                                                  question, test_data.get_test_data_by_list())
                        Log.customer_log('CUSTOMER: the test data list' + str(test_data.get_result_data_by_list()))
                        Log.customer_log('CUSTOMER: \n' + result)
                        # access data base and update the submit result
                        if result is not None:
                            Log.customer_log('CUSTOMER: Judgement......')
                            run_time = AnalysisResult.analysis_time(result)
                            run_time_total += float(run_time.replace('ms', ''))
                            analysis_result = AnalysisResult.analysis(result, test_data.get_result_data_by_list())
                            Log.customer_log('CUSTOMER: AnalysisResult is ' + analysis_result)
                            if analysis_result != DATA.ACCEPT:
                                OJDBA.update_by_result(analysis_result, submit.get_code_name())
                                break
                            else:
                                accept_total += 1
                        else:
                            Log.customer_log('CUSTOMER: Run timer Error')
                            OJDBA.update_runtime_error(submit.get_code_name())
                    # if acceptTotal is 5, update data base the result is ac
                    if accept_total == 5:
                        OJDBA.update_accepted(code_name=submit.get_code_name(),
                                             run_time=(str(run_time_total / DATA.JUDGEMENT_TIMES) + 'MS'))
                else:
                    Log.customer_log('CUSTOMER: Compile Error')
                    OJDBA.update_compiler_error(submit.get_code_name())
                Log.customer_log('CUSTOMER: Over......')
            except Exception, e:
                OJDBA.update_runtime_error(submit.get_code_name())
                print 'The error message is : ' + str(e.message)
