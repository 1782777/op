import numpy as np 
import tensorflow as tf 
import os



class predict():
    def __init__(self):
        pass

    def read_decode(self,filename,count):
        reader = tf.TFRecordReader()
        filename_queue = tf.train.string_input_producer([filename],) 
        _,serialized_example =reader.read(filename_queue)
        features= tf.io.parse_single_example(
            serialized_example,
            features={
                'x':tf.io.FixedLenFeature([], tf.string),
                'label':tf.io.FixedLenFeature([], tf.string)
            }   
        )
        
        x = tf.decode_raw(features['x'], tf.float64)
        label = tf.decode_raw(features['label'], tf.float64)
        x.set_shape([192])
        label.set_shape([48])
        x_tensor,label_tensor = tf.train.shuffle_batch([x,label],
                        batch_size=count,
                        capacity=8000,
                        num_threads=4,
                        min_after_dequeue=2000)
        x_tensor =tf.reshape(x_tensor,[count,48,4])
        return  x_tensor,label_tensor


if __name__ == '__main__':
    pre = predict()
    x,label = pre.read_decode('data/train.tfrecords',100)
    with tf.Session() as sess: #开始一个会话
        # init_op = tf.global_variables_initializer()
        # sess.run(init_op)
        coord=tf.train.Coordinator()
        threads= tf.train.start_queue_runners(coord=coord)
        example, l = sess.run([x,label])
        #example = example.reshape([1,48,4])
        print(example.shape, l.shape)

