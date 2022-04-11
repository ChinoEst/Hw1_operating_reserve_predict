if __name__ == '__main__':
	import argparse
	import csv
	import pandas as pd    
	import numpy as np
	from keras.models import Sequential
	from keras.layers import SimpleRNN, Dense
	from sklearn.preprocessing import MinMaxScaler
    
    
	parser = argparse.ArgumentParser()
	parser.add_argument('--training',
                       default='本年度每日尖峰備轉容量率.csv',
                       help='input training data file name')

	parser.add_argument('--output',
                        default='submission.csv',
                        help='output file name')
	args = parser.parse_args(args=[])

	

	# 載入資料
	train = pd.read_csv('台灣電力公司_過去電力供需資訊.csv', usecols=[2])
	train = train.values
	train = train.astype('float32')
    
    #資料前處理
	MMS = MinMaxScaler(feature_range=(0, 1))
	train = MMS.fit_transform(train)

    #x為昨日數據 ,y為今日數據
	train_x = []
	train_y = []
    
	for i in range(len(train) - 1):
		train_x.append(train[i])
		train_y.append(train[i+1])
        
	train_X = np.array(train_x)
	train_Y = np.array(train_y)

    #build RNN & train
	model = Sequential()
	model.add(SimpleRNN(2, input_shape=(1, 1)))
	model.add(Dense(1))
	model.compile(loss='MSE', optimizer='adam')
	model.fit(train_X, train_Y, epochs= 20, batch_size=2)
	pre = model.predict(train)

    #3月
	March = []
	for i in range(31):
		March.append(pre[-1, 0])
		pre = model.predict(pre)
	output3 = MMS.inverse_transform([March])
    
    #4月1-14
	April = [] 
	for i in range(14):
		April.append(pre[-1, 0])
		pre = model.predict(pre)
	output4 = MMS.inverse_transform([April])    

    #寫入CSV
	with open('submission.csv', 'w', newline='') as csvfile:
		date1 = "2022/3/"
		date2 = "2022/4/"
		writer = csv.writer(csvfile)
		for i in range(31):
	  		writer.writerow([date1 + f"{i+1}" , output3[0][i]])
		for i in range(14):
	  		writer.writerow([date2 + f"{i+1}" , output4[0][i]])
    
    

        
