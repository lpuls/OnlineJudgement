# coding:utf-8
__author__ = 'xp'

import time

from Submit import Submit
from PathData import DATA
from Question import Question
from TestData import TestData
from DataBaseLinker import DataBaseLinker


class OJDataBaseAdministrator:
    __mutex = True

    @staticmethod
    def wait_mutex():
        while True:
            # 因数据库不能同时访问，所以只有当数据库信号量为真时，才可进行访问
            if OJDataBaseAdministrator.__mutex:
                OJDataBaseAdministrator.__mutex = False
                break
            time.sleep(0.1)

    @staticmethod
    def release_mutex():
        OJDataBaseAdministrator.__mutex = True

    @staticmethod
    def updata_submit_result(result, code_name):
        OJDataBaseAdministrator.wait_mutex()
        result = DataBaseLinker.getInstance().execute("update Submit set result='" + result
                                                      + "' where codeName='" + code_name + "'")
        OJDataBaseAdministrator.release_mutex()
        return result

    @staticmethod
    def updata_submit_time(run_time, code_name):
        OJDataBaseAdministrator.wait_mutex()
        result = DataBaseLinker.getInstance().execute("update Submit set time='" + run_time
                                                      + "' where codeName='" + code_name + "'")
        OJDataBaseAdministrator.release_mutex()
        return result

    @staticmethod
    def get_question(question_id):
        OJDataBaseAdministrator.wait_mutex()
        result = DataBaseLinker.getInstance().execute("select * from Question where id='" + str(question_id) + "'")
        question = Question(result[0])
        OJDataBaseAdministrator.release_mutex()
        return question

    @staticmethod
    def get_submit_which_waiting():
        OJDataBaseAdministrator.wait_mutex()
        result = DataBaseLinker.getInstance().execute("select * from Submit where result='waiting'")
        OJDataBaseAdministrator.release_mutex()
        submits = []
        for item in result:
            submit = Submit(item)
            submits.append(submit)
        return submits

    @staticmethod
    def get_test_data_by_question_id(id):
        OJDataBaseAdministrator.wait_mutex()
        result = DataBaseLinker.getInstance().execute("select * from TestData where question_id='" + str(id) + "'")
        OJDataBaseAdministrator.release_mutex()
        test_datas = []
        for item in result:
            test_data = TestData(item)
            test_datas.append(test_data)
        return test_datas

    @staticmethod
    def get_user_by_user_id(question_id):
        OJDataBaseAdministrator.wait_mutex()
        result = DataBaseLinker.getInstance().execute("select * from Users where user_id='" + str(question_id) + "'")
        OJDataBaseAdministrator.release_mutex()
        return result

    @staticmethod
    def update_compiler_error(code_name):
        return OJDataBaseAdministrator.updata_submit_result('Compiler Error', code_name)

    @staticmethod
    def update_running(code_name):
        return OJDataBaseAdministrator.updata_submit_result('Running', code_name)

    @staticmethod
    def update_memory_limit_exceeded(code_name):
        return OJDataBaseAdministrator.updata_submit_result('Memory Limit Exceeded', code_name)

    @staticmethod
    def update_time_limit_exceeded(code_name):
        return OJDataBaseAdministrator.updata_submit_result('Time Limit Exceeded', code_name)

    @staticmethod
    def update_runtime_error(code_name):
        return OJDataBaseAdministrator.updata_submit_result('Runtime Error', code_name)

    @staticmethod
    def update_wrong_answer(code_name):
        return OJDataBaseAdministrator.updata_submit_result('Wrong Answer', code_name)

    @staticmethod
    def update_output_limit_exceeded(code_name):
        return OJDataBaseAdministrator.updata_submit_result('Output Limit Exceeded', code_name)

    @staticmethod
    def update_presentation_error(code_name):
        return OJDataBaseAdministrator.updata_submit_result('Presentation Error', code_name)

    @staticmethod
    def update_accepted(code_name, run_time='N/A'):
        OJDataBaseAdministrator.updata_submit_time(run_time, code_name)
        OJDataBaseAdministrator.updata_submit_result('Accepted', code_name)

    @staticmethod
    def add_question(question):
        OJDataBaseAdministrator.wait_mutex()
        result = DataBaseLinker.getInstance().execute("insert into Question (name, context, time, ram, point) value ('"
                                                      + question.get_name() + "', '" + question.get_context() + "',"
                                                      + str(question.get_time())+","+str(question.get_ram())+","
                                                      + str(question.get_point()) + ")")
        OJDataBaseAdministrator.release_mutex()
        return result

    @staticmethod
    def add_submit(submit):
        sql = "insert into Submit (user_id, question_id, submit_time, type, codeName, result) value ('"
        sql = sql + submit.get_user_id() + "','" + str(submit.get_question_id()) \
                  + "','" + submit.get_submit_time() + "','" + submit.get_language_type() \
                  + "','" + submit.get_code_name() + "','" + submit.get_result() + "')"
        OJDataBaseAdministrator.wait_mutex()
        result = DataBaseLinker.getInstance().execute(sql)
        OJDataBaseAdministrator.release_mutex()
        return result

    @staticmethod
    def add_test_data(test_data):
        sql = "insert into TestData (question_id, test_data, result_data) value ("
        sql = sql + str(test_data.get_question_id()) + ",'" + test_data.get_test_data() + "','" \
                  + test_data.get_result_data() + "')"
        OJDataBaseAdministrator.wait_mutex()
        result = DataBaseLinker.getInstance().execute(sql)
        OJDataBaseAdministrator.release_mutex()
        return result

    @staticmethod
    def add_user(user_id, password, user_school="", user_name="None Name"):
        sql = "insert into Users (user_id, user_name, user_password, user_school) value ('"
        sql = sql + user_id + "','" + user_name + "','" + password + "','" + user_school + "')"
        OJDataBaseAdministrator.wait_mutex()
        result = DataBaseLinker.getInstance().execute(sql)
        OJDataBaseAdministrator.release_mutex()
        return result

    @staticmethod
    def update_by_result(result, code_name):
        if result == DATA.MEMORY_LIMIT_EXCEEDED:
            OJDataBaseAdministrator.update_memory_limit_exceeded(code_name)
        elif result == DATA.TIME_LIMIT_EXCEEDED:
            OJDataBaseAdministrator.update_time_limit_exceeded(code_name)
        elif result == DATA.WRONG_ANSWER:
            OJDataBaseAdministrator.update_wrong_answer(code_name)
        elif result == DATA.OUTPUT_LIMIT_EXCEEDED:
            OJDataBaseAdministrator.update_output_limit_exceeded(code_name)
        elif result == DATA.PRESENTATION_ERROR:
            OJDataBaseAdministrator.update_presentation_error(code_name)
