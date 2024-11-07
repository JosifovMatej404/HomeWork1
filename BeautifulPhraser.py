from bs4 import BeautifulSoup
import RequestHandler

class Pharser:
    def __init__(self, parent):
        self.parent = parent

    def get_data(self, target):
        if target == "suppliers": return self.get_data_array("https://www.mse.mk/mk/issuers/free-market")
        else: return self.get_data_array("https://www.mse.mk/en/stats/symbolhistory/" + str(target))

    def get_data_from_html(self, target, html):
        return self.get_data_array_from_html("https://www.mse.mk/en/stats/symbolhistory/" + str(target), html)

    def get_data_array(self, path):
        html = RequestHandler.get_html_page(path)
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all("tr")
        header_data = self.get_headers(path)
        data_array = [] #data object for all companies

        if len(header_data.headers) <= 0: self.parent.fail_response()

        for row in rows:
            data = row.find_all("td")
            data_object = []
            if len(data) < len(header_data.headers): continue
            if len(header_data.headers) > 7: data_object = SupplierData(data)
            else: data_object = Data(data)
            data_array.append(data_object) 
        return data_array
    
    def get_data_array_from_html(self, path, html):
        print("HTML" + str(html))
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all("tr")
        header_data = self.get_headers(path)
        data_array = [] #data object for all companies

        if len(header_data.headers) <= 0: self.parent.fail_response()

        for row in rows:
            data = row.find_all("td")
            data_object = []
            if len(data) < len(header_data.headers): continue
            if len(header_data.headers) > 7: data_object = SupplierData(data)
            else: data_object = Data(data)
            data_array.append(data_object) 
        return data_array
    
    
    @staticmethod
    def get_headers(path):
        html = RequestHandler.get_html_page(path)
        soup = BeautifulSoup(html, 'html.parser')
        header_data = soup.find_all("th")
        return HeaderData(header_data)

class SupplierData:
    def __init__(self, row):
        data_array = []
        for data in row:
            if not data.string: data_array.append("NULL")
            else: data_array.append(data.string.strip())
        self.date = data_array[0]
        self.last_trade_price = data_array[1]
        self.max = data_array[2]
        self.min = data_array[3]
        self.avg_price = data_array[4]
        self.percent_change = data_array[5]
        self.volume = data_array[6]
        self.turnover_best_denars = data_array[7]
        self.total_turnover_denars = data_array[8]

class Data:
    def __init__(self, row):
        data_array = []
        for data in row:
            data_array.append(data.string.strip())
        self.code = data_array[0]
        self.description = data_array[1]
        self.isin = data_array[2]
        self.total_hv = data_array[3]

    def __str__(self):
        return self.description
    
class HeaderData:
    def __init__(self, row):
        self.headers = []
        for data in row:
            self.headers.append(data.string.strip())