from createScaledDataSet import Dataset
from sklearn.neural_network import MLPRegressor
import numpy as np
from sklearn.preprocessing import StandardScaler  
from sklearn.metrics import mean_squared_error as MSE
from math import sqrt

def run():
	dataset = Dataset(0.7)

	data_train = dataset.get_training_data();
	label_train = dataset.get_training_labels();
	data_val = dataset.get_validation_data();
	label_val = dataset.get_validation_label();

	mlp = MLPRegressor(hidden_layer_sizes=(100,50,), random_state=1, max_iter=1,
                   warm_start=True, learning_rate_init =0.000001)	

	for i in range(5000):
	    mlp.fit(data_train, label_train)
	    if(i % 100 == 0):
	        #print("Validation set score: %f" % mlp.score(X_val, y_val)) 
	        #print("Training set score: %f" % mlp.score(X_train, y_train))
	        p = mlp.predict(data_val);
	        mse = MSE( label_val, p )
	        rmse = sqrt( mse )
	        print rmse
	
	print("Training set score: %f" % mlp.score(X_train, y_train))


run()

