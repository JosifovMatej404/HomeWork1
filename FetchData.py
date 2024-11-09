from bs4 import BeautifulSoup 
import RequestHandler


class FetchData:
    
    def fetch_data_for_10_years(self):
        url = f"https://www.mse.mk/en/stats/symbolhistory/ALK"
        html = RequestHandler.get_html_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all("tr")
        header_data = soup.find_all("th")
        data_array = [] #data object for all companies

        print(rows)

        return data_array
    


class SupplierData:
    def __init__(self, row):
        data_array = []
        for data in row:
            data_array.append(data.string)
        self.date = data_array[0]
        self.last_trade_price = data_array[1]
        self.max = data_array[2]
        self.min = data_array[3]
        self.avg_price = data_array[4]
        self.percent_change = data_array[5]
        self.volume = data_array[6]
        self.turnover_best_denars = data_array[7]
        self.total_turnover_denars = data_array[8]


