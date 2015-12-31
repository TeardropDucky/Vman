from PlayerEvaluator.Utility.ConverterHTML import ConverterHTML


class scout_finder:
    __htmlworker = None
    __htmlretriver = None

    def __init__(self):
        self.__htmlworker = ConverterHTML()

    def search_scouts(self, potential, discipline, endPage=10, startPage=1, minPrice=10000, maxPrice=500000, max_age=99):
        if minPrice > maxPrice:
            return None

        scoutArray = []
        for x in range(startPage, endPage + 1):
            tmp_array = self.__htmlworker.get_personal_search('scout', x)
            # First a price check, because there is no reason to look at stats, if the price is too cheap
            tmp_array = [employee for employee in tmp_array if minPrice < employee.value < maxPrice]
            # Now lets find the really good coaches
            tmp_array = [employee for employee in tmp_array if employee.stats['Potential'] >= potential
                         and employee.stats['Discipline'] >= discipline]
            scoutArray.extend(tmp_array)
            if x % 10 == 0:
                print("done with page " + str(x))

        # Print all the good scouts
        for x in scoutArray:
            print(str(x.id) + " value: " + str(x.value))
            print("stats: " + str(x.stats))
        return scoutArray

    def search_scout(self, potential, discipline, startPage=1, ):
        if startPage < 1:
            print('Start page much be higher than 1')
            return
        scouts = None

        for x in range(startPage, startPage + 100000):
            # get trainer array for page
            tmp_array = self.__htmlworker.get_personal_search('scout', x)
            # Check if page was loaded
            if tmp_array == '404':
                print('No more pages. Last page was ' + str(x))
                return
            # Now lets find the really good scouts
            tmp_array = [employee for employee in tmp_array if employee.stats['Potential'] >= potential
                         and employee.stats['Discipline'] >= discipline]
            # For now just print, every 10 pages
            if x % 10 == 0:
                print("done with page " + str(x))

            # We found a really good scout, lets end here
            if len(tmp_array) != 0:
                scouts = tmp_array[0]
                print("found a scout on page " + str(x))
                print(str(scouts.id) + " value " + str(scouts.value))
                return scouts

        return scouts


derp = scout_finder()
derp.search_scout(20,20,5)
derp.search_scouts(20,20,25)