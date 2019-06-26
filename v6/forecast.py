from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
from datetime import datetime
from matplotlib import pyplot

#data_path = '../../input/AAPL.csv'


class ForecastModel():
    def __init__(self, data_path, index_name, row):
        # original exchange data
        self.original_data = pd.read_csv(data_path, index_col=index_name)
        self.original_data = self.original_data[row]
        self.number_of_elements = len(self.original_data)

        # setting up hold out 70/30
        self.training_size = int(self.number_of_elements*0.7)
        self.training_data = self.original_data[0:self.training_size]
        self.test_data     = self.original_data[self.training_size:self.number_of_elements]

        self.actual = [x for x in self.training_data]
        self.predictions = list()

        
    def use_arima(self, training_data, p, d, q):
        model = ARIMA(training_data, order=(p,d,q))
        model_fit = model.fit(disp=False)
        return model_fit.forecast()[0]
    

    def begin_forecast(self, debug=True):
        for value in self.test_data:
            actual_value = value
            prediction = self.use_arima(self.actual, 3, 1, 0)
            if debug:
                print('Actual=%f, Predicted=%f' % (actual_value, prediction))
            self.predictions.append(prediction)
            self.actual.append(actual_value)

    def show_plot(self):
        pyplot.plot(self.test_data)
        pyplot.plot(self.predictions, color='red')
        pyplot.show()