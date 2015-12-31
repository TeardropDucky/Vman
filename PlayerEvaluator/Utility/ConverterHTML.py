import re
from PlayerEvaluator.Models.Player import Player
from PlayerEvaluator.Models.Employee import Employee
from PlayerEvaluator.Utility.RetrieverHTML import RetrieverHTML


class ConverterHTML:
    __retriever = None
    __response_body = None  # Remember to reset this to None after each function

    def __init__(self):
        self.__retriever = RetrieverHTML('himmelherren@gmail.com', 'anders')

    # *****************************************************************************************************************
    #   Functions getting data to a player
    #
    #
    # *****************************************************************************************************************

    def get_player_information(self, player=None):
        if player is None:
            return None
        __player = player

        __player = self.get_player_stats(__player)
        __player = self.get_player_transfer_value(__player)
        __player = self.get_player_evaluation(__player)

        return __player

    def get_player_stats(self, player=None):
        if player is None:
            return None
        __player = player
        ''' Get HTML data or set it if already known'''
        if self.__response_body is None:
            self.__response_body = self.__retriever.get_player_information(__player)

        stats = re.findall(r'<div class="value">(.*?)</div>', str(self.__response_body))

        __player.stats = {
            'total': stats[0],
            'passing': stats[1],
            'pace': stats[2],
            'finishing': stats[3],
            'acceleration': stats[4],
            'dribbling': stats[5],
            'endurance': stats[6],
            'tackling': stats[7],
            'leadership': stats[8],
            'setplays': stats[9],
            'fighting': stats[10]
        }
        return __player

    def get_player_transfer_value(self, player=None):
        if player is None:
            return None
        __player = player

        '''
        Get transfer value. A user might possible have placed the player on the transferlist. If so the transferlist
        value is retrieved and saved in the player too
        '''
        __transferValues = re.findall(r'\d*,\d*,\d{1,3}\s[C]', str(self.__response_body))

        if len(__transferValues) > 1:
            __player.value = (__transferValues[1][:len(__transferValues[1])])
            __player.transferlist = (__transferValues[0][:len(__transferValues[0])])

        else:
            __player.value = (__transferValues[0][:len(__transferValues[0])])

        return __player

    def get_player_evaluation(self, player=None):
        if player is None:
            return None
        __player = player

        __evaluation = re.findall(r'[a-f0-9][a-f0-9]">\d+<', str(self.__response_body))

        __player.evaluation = __evaluation[0][
                              4:len(__evaluation[0]) - 1]  # for some reason there is an extra char, so -1

        return __player

    def get_player_training(self, player=None):
        if player is None:
            return None
        __player = player
        return __player

    # *****************************************************************************************************************
    #   *Functions getting data to an employee
    #
    #
    # *****************************************************************************************************************

    def get_personal(self, employee=None):
        if employee is None:
            return None
        __employee = employee

        html = self.__retriever.get_personal_info(__employee)

        stats1 = re.findall('g>(\w+?)</', str(html))
        __employee.age = stats1[0]
        if stats1[1] == 'Trainer':
            __employee.position = 'coach'
        else:
            __employee.position = 'scout'
        __employee.stats = {
            'youth': stats1[3],
            'keeper': stats1[4],
            'fielders': stats1[5],
            'disciplin': stats1[6],
            'potential': stats1[7],
            'leadership': stats1[8],
            'abilty': stats1[9],
            'motivation': stats1[10]
        }

        return __employee

    def get_personal_search(self, role='coach', page=1, min_age=0, max_age=99):

        self.__response_body = self.__retriever.get_personal_search(role, page, min_age, max_age)
        if self.__response_body == '404':
            return '404'
        # \d+, \d{1,2}, \d{1,2}, \d{1,2}, \d{1,2}, \d{1,2}, \d{1,2}, \d{1,2}, \d{1,2}
        full_personnel_array = re.findall(
                r'\d+, \d{1,2}, \d{1,2}, \d{1,2}, \d{1,2}, \d{1,2}, \d{1,2}, \d{1,2}, \d{1,2}',
                str(self.__response_body))
        cost = re.findall(r'\d{1,3},\d{1,3} [C]', str(self.__response_body))

        cost = [str.replace(str.replace(x, ',', ''), ' C', '') for x in cost]
        string_result = []
        for i in range(0,len(cost)):
            string_result.append(full_personnel_array[i] + ', ' + cost[i])
        employee_list = []
        for item in string_result:
            data = item.split(', ')
            data = [int(x) for x in data]
            tmp_employee = Employee(data[0])
            tmp_employee.value = data[9]
            tmp_employee.stats = {
                'Youngsters': data[1],
                'Keepers': data[2],
                'Outfielders': data[3],
                'Discipline': data[4],
                'Potential': data[5],
                'Management': data[6],
                'Ability': data[7],
                'Motivation': data[8]
            }
            employee_list.append(tmp_employee)

        return employee_list


derp = ConverterHTML()
derp.get_personal_search()
