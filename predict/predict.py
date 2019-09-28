import numpy as np 
import tensorflow as tf 
import os



class predict():
    def __init__(self):
        self.X = tf.placeholder(tf.float32,[None,48,4,1],name='X')
        self.label =tf.placeholder(tf.float32,[None,48,1,1],name='label')
        self.keep_prob = tf.placeholder(tf.float32, name="keep_prob")  

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
    
    def read_data(self,filename,count):
        dataset = tf.data.TFRecordDataset(filename)
        dataset = dataset.map(...)
        dataset = dataset.shuffle(buffer_size=10000)
        dataset = dataset.batch(32)
        dataset = dataset.repeat()


    def nn_generate(self):
        #X = tf.placeholder(tf.float32,[None,48,4],name='X')
        conv1=tf.layers.conv2d(
            inputs=self.X,
            filters=32,
            kernel_size=[1,1],
            strides=1,
            padding='same',
            activation=tf.nn.tanh
        )
        #[?,48,4]
        pool1=tf.layers.max_pooling2d(
            inputs=conv1,
            pool_size=[2,2],
            strides=2
        )
        #[?,24,2]
        conv2=tf.layers.conv2d(
            inputs=pool1,
            filters=64,
            kernel_size=[1,3],
            strides=1,
            padding='same',
            activation=tf.nn.tanh
        )
        #输出变成了  [?,14,14,64]
        pool2=tf.layers.max_pooling2d(
            inputs=conv2,
            pool_size=[2,2],
            strides=2
        )
        #[?,12,1]
        flat=tf.reshape(pool2,[-1,12*1*64])
        dense=tf.layers.dense(
            inputs=flat,
            units=1024,
            activation=tf.nn.tanh
        )
        dropout=tf.layers.dropout(
            inputs=dense,
            rate=self.keep_prob,
        )
        logits=tf.layers.dense(
            inputs=dropout,
            units=48
        )
        return logits
        

    def discriminator(self,x,drop):
        conv1=tf.layers.conv2d(
            inputs=x,
            filters=32,
            kernel_size=[1,3],
            strides=1,
            padding='same',
            activation=tf.nn.tanh
        )
        #[?,48,]
        # pool1=tf.layers.max_pooling2d(
        #     inputs=conv1,
        #     pool_size=[1,2],
        #     strides=2
        # )
        # #[?,24,]
        conv2=tf.layers.conv2d(
            inputs=conv1,
            filters=64,
            kernel_size=[1,5],
            strides=1,
            padding='same',
            activation=tf.nn.tanh
        )
        #输出变成了  [?,14,64]
        # pool2=tf.layers.max_pooling2d(
        #     inputs=conv2,
        #     pool_size=[1,2],
        #     strides=2
        # )
        # #[?,7,64]
        flat=tf.reshape(conv2,[-1,48*64])
        dense=tf.layers.dense(
            inputs=flat,
            units=256,
            activation=tf.nn.tanh
        )
        dropout=tf.layers.dropout(
            inputs=dense,
            rate=drop,
        )
        logits=tf.layers.dense(
            inputs=dropout,
            units=1
        )
        D_prob = tf.nn.sigmoid(logits)
        return D_prob,logits

    def train(self):
        # X = tf.placeholder(tf.float32,[None,48,4],name='X')
        # label =tf.placeholder(tf.float32,[None,48,],name='label')
        # keep_prob = tf.placeholder(tf.float32, name="keep_prob") 
        print('G_sample') 
        #G_sample = self.nn_generate(self.X,self.keep_prob)
        G_sample = self.nn_generate()
        G_sample =tf.expand_dims(G_sample, -1)
        G_sample =tf.expand_dims(G_sample, -1)
        print('G_sample_finish------------------------------------------------') 
        print(G_sample.get_shape())
        D_real, D_logit_real = self.discriminator(self.label,self.keep_prob)
        print('discriminator1_finish---------------------------------------------') 
        D_fake, D_logit_fake = self.discriminator(G_sample,self.keep_prob)
        # D_loss = -tf.reduce_mean(tf.log(D_real) + tf.log(1. - D_fake))
        # G_loss = -tf.reduce_mean(tf.log(D_fake))
        # D_loss = D_loss_real + D_loss_fake
        D_loss_real = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=D_logit_real, labels=tf.ones_like(D_logit_real)))
        D_loss_fake = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=D_logit_fake, labels=tf.zeros_like(D_logit_fake)))
        D_loss = D_loss_real + D_loss_fake
        print('D_loss_finish---------------------------------------------') 
        G_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=D_logit_fake, labels=tf.ones_like(D_logit_fake)))
        D_solver = tf.train.AdamOptimizer(0.001).minimize(D_loss)
        G_solver = tf.train.AdamOptimizer(0.001).minimize(G_loss)
        print('AdamOptimizer_finish---------------------------------------------') 
        return D_solver,G_solver

if __name__ == '__main__':
    os.environ["TF_CPP_MIN_LOG_LEVEL"]='3'
    
    
    with tf.compat.v1.Session() as sess:
        pre = predict()
        init_op = tf.global_variables_initializer()
        sess.run(init_op)
        
        
        
        
        # for it in range(20000):
        #     x,label = pre.read_decode('data/train.tfrecords',100)
        #     coord=tf.train.Coordinator()
        #     threads= tf.train.start_queue_runners(coord=coord)
        #     example, l = sess.run([x,label])
        #     example[:,:,0] =example[:,:,0]/10000000
        #     example[:,:,2] =example[:,:,2]/100000000
        #     example=example[:,:,:,np.newaxis]
        #     l=l[:,:,np.newaxis]
        #     l=l[:,:,np.newaxis]
        #     print(example.shape,l.shape)
        #     D_solver,G_solver = sess.run(pre.train(),feed_dict={pre.X:example,pre.label:l,pre.keep_prob:0.7})
        #     print('------------------------------------------------')
        #     print(D_solver,G_solver)
        for it in range(20000):
            x,label = pre.read_decode('data/train.tfrecords',100)
            coord=tf.train.Coordinator()
            threads= tf.train.start_queue_runners(coord=coord)
            example, l = sess.run([x,label])
            example[:,:,0] =example[:,:,0]/10000000
            example[:,:,2] =example[:,:,2]/100000000
            example=example[:,:,:,np.newaxis]
            l=l[:,:,np.newaxis]
            l=l[:,:,np.newaxis]
            print('--------------------------',example)
            g = sess.run(pre.nn_generate(),feed_dict={pre.X:example,pre.keep_prob:0.7})
            print(g.shape)
