__author__ = 'xp'

from Submit import Submit
from Question import Question
from DataBase import DataBaseLinker

class OJDataBaseAdministrator:
    dbLinker = DataBaseLinker.getInstance()

    @staticmethod
    def updataRunning(fileName):
        return OJDataBaseAdministrator.dbLinker.execute("update Submit set result='Running' where codeName='" + fileName + "'")

    @staticmethod
    def getQuestionById(id):
        data = OJDataBaseAdministrator.dbLinker.execute("select * from Question where id='" + id + "'")
        question = Question(data[0]['time'],data[0]['ram'],data[0]['id'],data[0]['context'],data[0]['name'])
        return question

    @staticmethod
    def getSubmitsWhichWating():
        data = OJDataBaseAdministrator.dbLinker.execute("select * from Submit where result='Waiting'")
        submits = []
        for item in data:
            submit = Submit(userID=item['user_id'], result=item['result'], submitTime=item['submit_time'], codeName=item['codeName'], type=item['type'], questionID=item['question_id'])
            submits.append(submit)
        return  submits

if __name__ == '__main__':
    result = OJDataBaseAdministrator.getSubmitsWhichWating()
    data = result[0].getResult()