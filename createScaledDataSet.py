import csv
import numpy as np
import pandas as pd

class Dataset(object):

    def get_normalized_values(self, array, data_types):
        for i in range(0, len(data_types)):
            if data_types[i][0] == 'n':
                array[:,i] = (array[:,i] -  np.mean(array[:,i])) / np.std(array[:,i])
        return array

    def get_vectorized_array(self, array, data_types):
    	data_types_with_intvalues = np.copy(data_types)

    	for i in range(0, len(data_types)):
    		if data_types[i][0] == 'i':
    			#largest_value =  "{0:b}".format(10) max binary length
    			#convert every valye to binary and fill the vector
    			data_types_with_intvalues[i][1] = 2
    	print data_types_with_intvalues


    def write_scaled_data_set(self, array):
    	df = pd.DataFrame(array)
    	df.to_csv("dataset_utentittel_small_scaled.csv", sep=',', header=False, index=False)
    
    def write_vectorized_data_set(self, array):
        print "Hello, gorgeous!"

    def get_training_data(self):
    	return self._training_data
    
    def get_training_labels(self):
    	return self._training_labels
    
    def get_validation_data(self):
    	return self._validation_data

    def get_validation_label(self):
    	return self._validation_labels

    def __init__(self, training_percentage):
    	self.data_types = [
            ('s',   1),		#Datetime 
            ('i',   1), 	#Hour
            ('i',   1),		#Weekday
            ('i',   1), 	#Station Id
            ('s',   1),		#Station name
            ('n',   1),		#Lat
            ('n',   1),		#Lon
            ('n',   1),		#MASL
            ('i',   1),		#Number of locks
            ('i',   1),		#Av. locks
            ('i',   1)]		#Av. bikes

        self._data = dataset = pd.read_csv('data-utentittel-small.csv', header=None, sep=',')
        self._raw_data_and_labels = self._data.as_matrix()

        print self._raw_data_and_labels[1]
        self._normalized_values = self.get_normalized_values(np.copy(self._raw_data_and_labels), self.data_types);
        print self._normalized_values[1]
        print len(self._normalized_values)

        self.write_scaled_data_set(self._normalized_values)

        self._all_data = self._normalized_values[:, 0 : len(self.data_types) - 1]
        self._all_labels = self._normalized_values[:, len(self.data_types)-1 : len(self.data_types)]

        split_training_index = int(len(self._normalized_values)* training_percentage)

        self._training_data = self._all_data[0 : split_training_index]
        self._training_labels = self._all_labels[0 : split_training_index]

        self._validation_data = self._all_data[split_training_index : ,]
        self._validation_labels = self._all_labels[split_training_index :,]


        #self._vectorized_data_and_labels = self.get_vectorized_array(self._normalized_values, self.data_types);



	