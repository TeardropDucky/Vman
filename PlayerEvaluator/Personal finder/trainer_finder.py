from PlayerEvaluator.Utility.ConverterHTML import ConverterHTML


class trainer_finder:
    __htmlworker = None
    __htmlretriver = None

    def __init__(self):
        self.__htmlworker = ConverterHTML()

    def search_trainers(self, youth, keeper, outfielder, endPage=10, startPage=1, minPrice=50000, maxPrice=500000,
                        max_age=99):
        if minPrice > maxPrice:
            return None

        trainerArray = []
        for x in range(startPage, endPage + 1):
            tmp_array = self.__htmlworker.get_personal_search('coach', x)
            # First a price check, because there is no reason to look at stats, if the price is too cheap
            tmp_array = [employee for employee in tmp_array if minPrice < employee.value < maxPrice]
            # Now lets find the really good coaches
            tmp_array = [employee for employee in tmp_array if employee.stats['Youngsters'] >= youth
                         and employee.stats['Keepers'] >= keeper and employee.stats['Outfielders'] >= outfielder]
            trainerArray.extend(tmp_array)
            if x % 10 == 0:
                print("done with page " + str(x))

        # Print all the good coaches
        for x in trainerArray:
            print(str(x.id) + " value: " + str(x.value))
            print("stats: " + str(x.stats))
        return trainerArray

    def search_trainer(self, youth, keeper, outfielder, startPage=1, ):
        if startPage < 1:
            print('Start page much be higher than 1')
            return
        trainer = None

        for x in range(startPage, startPage + 100000):
            # get trainer array for page
            tmp_array = self.__htmlworker.get_personal_search('coach', x)
            # Check if page was loaded
            if tmp_array == '404':
                print('No more pages. Last page was ' + str(x))
                return
            # Now lets find the really good coaches
            tmp_array = [employee for employee in tmp_array if employee.stats['Youngsters'] >= youth
                         and employee.stats['Keepers'] >= keeper and employee.stats['Outfielders'] >= outfielder]
            # For now just print, every 10 pages
            if x % 10 == 0:
                print("done with page " + str(x))

            # We found a really good coach, lets end here
            if len(tmp_array) != 0:
                trainer = tmp_array[0]
                print("found a trainer on page " + str(x))
                print(str(trainer.id) + " value " + str(trainer.value))
                return trainer

        return trainer


derp = trainer_finder()
derp.search_trainer(20, 20, 20, 1)
