# -*- coding: utf-8 -*-

import tensorflow as tf
from data_set import data_set_dict
from data_prepare import get_data
from model import Net
import shutil
import numpy as np

tf.logging.set_verbosity(tf.logging.INFO)
path = 'E:\\tsproject\\t_data'
data_name = 'Yoga'
data_set = data_set_dict[data_name]
validation = False
retrain = True
learning_rate = 0.0001
batch_size = 4
total_round=1500

    
def main(_):
    if validation:
        val_set = np.loadtxt(path + '\\' +  data_name + '\\' + data_name+'_TRAIN',delimiter=',')
        val_test1=val_set[0:len(val_set)//3]
        val_train1=val_set[len(val_set)//3:]
        val_test2=val_set[len(val_set)//3:(len(val_set)//3+(len(val_set)-len(val_set)//3)//2)]
        val_train2=np.concatenate((val_set[0:len(val_set)//3],val_set[(len(val_set)//3+(len(val_set)-len(val_set)//3)//2):]),axis=0)
        val_test3=val_set[(len(val_set)//3+(len(val_set)-len(val_set)//3)//2):]
        val_train3=val_set[:(len(val_set)//3+(len(val_set)-len(val_set)//3)//2)]
        
        np.savetxt(path  + '\\' + data_name  + '\\' + data_name+ '_VAL_TEST1' ,val_test1 ,delimiter=',')
        np.savetxt(path  + '\\' + data_name  + '\\' + data_name + '_VAL_TRAIN1' ,val_train1 ,delimiter=',')
        np.savetxt(path  + '\\' + data_name  + '\\' + data_name+ '_VAL_TEST2' ,val_test2 ,delimiter=',')
        np.savetxt(path  + '\\' + data_name  + '\\' + data_name + '_VAL_TRAIN2' ,val_train2 ,delimiter=',')
        np.savetxt(path  + '\\' + data_name  + '\\' + data_name+ '_VAL_TEST3' ,val_test3 ,delimiter=',')
        np.savetxt(path  + '\\' + data_name  + '\\' + data_name + '_VAL_TRAIN3' ,val_train3 ,delimiter=',')
        
        data_info=(['_VAL_TRAIN1','_VAL_TEST1',len(val_train1),len(val_test1)],['_VAL_TRAIN2','_VAL_TEST2',len(val_train2),len(val_test2)],
                    ['_VAL_TRAIN3','_VAL_TEST3',len(val_train3),len(val_test3)])
        
        val_error_num = 0
        val_test_num = len(val_test1)+len(val_test2)+len(val_test3)
        
        for train_path, test_path,  train_size, test_size in data_info:
            train_set = [path + '\\' +  data_name + '\\' + data_name+ train_path]
            test_set = [path  + '\\' +  data_name + '\\' + data_name+ test_path]
            steps = total_round*train_size//batch_size
            model_url = path + '\\'+'cnn' + '\\' + data_name + '\\'  
            error_num = 0
    
            if retrain:
                shutil.rmtree(model_url,ignore_errors=True)
           
            model = Net()
        
            hps = {
                'learning_rate': learning_rate,
                   }   
        
            estimator = tf.estimator.Estimator(model.model_fn, model_url, params=hps)
            logging_hook = tf.train.LoggingTensorHook({}, every_n_iter=100, at_end=True)
        

            estimator.train(
                lambda: get_data(train_set, data_set.length, data_set.classes_num, 
                                 batch_size,True),  
                [logging_hook],
                steps=steps)
        
            result= estimator.evaluate(
                lambda: get_data(test_set, data_set.length, data_set.classes_num, 
                                test_size, False), 
                steps=1)

            error_num = (1-result['accuracy'])*test_size  
            
            val_error_num = val_error_num + error_num  
        print('*****************************************************************************')
        print('The validation error is', val_error_num/val_test_num)
    
    
    else:
        steps = total_round*data_set.train_size//batch_size
        
        train_set = [path + '\\' +  data_name + '\\' + data_name+'_TRAIN']
        test_set = [path  + '\\' +  data_name + '\\' + data_name+'_TEST']
        model_url = path + '\\'+'cnn' + '\\' + data_name + '\\'   
           
        if retrain:
            shutil.rmtree(model_url,ignore_errors=True)
           
        model = Net()
        
        hps = {
            'learning_rate': learning_rate,
               }   
        
        estimator = tf.estimator.Estimator(model.model_fn, model_url, params=hps)
        logging_hook = tf.train.LoggingTensorHook({}, every_n_iter=100, at_end=True)
                    
        estimator.train(
            lambda: get_data(train_set, data_set.length, data_set.classes_num, 
                             batch_size,True),  
            [logging_hook],
            steps=steps)
        
        result= estimator.evaluate(
            lambda: get_data(test_set, data_set.length, data_set.classes_num, 
                            data_set.test_size, False), 
            steps=1)

        print('*****************************************************************************')
        print('accuracy:',result['accuracy'])
        print('error:',1-result['accuracy'])
                    
if __name__ == '__main__':
     tf.app.run()
