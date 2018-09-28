import tensorflow as tf
import dataset as dt
import util
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


class Model(object):
    def __init__(self, input_shape, output_shape):
        self.x = tf.placeholder(dtype=tf.float32, shape=[None] + input_shape)
        self.y = tf.placeholder(dtype=tf.float32, shape=[None] + output_shape)

        self.d, self.logits = self._build_model()
        # self.logits = self.d['logits']
        self.loss = self._build_loss()

    def _build_model(self):
        d = dict()
        # mean subtraction
        x_mean = 0.0
        x_input = self.x-x_mean
        # x_input = tf.reshape(tensor=self.x, shape=[-1, 256, 256, 1])

        # 256 * 256 * 3
        # encoder part #
        # conv1 - relu1 - pool1

        # encoder ######################################################################################################
        # input shape : (batch, 256, 256, 1)
        print("encoder start")

        print("input's shape : ", x_input.shape)

        with tf.variable_scope('conv1'):
            weight = tf.get_variable(name='weight', shape=[3, 3, 1, 32], dtype=tf.float32)
            bias = tf.get_variable(name='bias', shape=[32], dtype=tf.float32)
            layer1 = tf.nn.conv2d(input=x_input, filter=weight, strides=[1, 2, 2, 1], padding='SAME') + bias
            layer1 = tf.nn.relu(layer1)
            print("layer1's shape : ", layer1.shape)
            # Conv -> (?, 128, 128, 32)

        with tf.variable_scope('conv2'):
            weight = tf.get_variable(name='weight', shape=[3, 3, 32, 64], dtype=tf.float32)
            bias = tf.get_variable(name='bias', shape=[64], dtype=tf.float32)
            layer2 = tf.nn.conv2d(input=layer1, filter=weight, strides=[1, 2, 2, 1], padding='SAME') + bias
            layer2 = tf.nn.relu(layer2)
            print("layer2's shape : ", layer2.shape)
            # Conv -> (?, 64, 64, 64)

        with tf.variable_scope('conv3'):
            weight = tf.get_variable(name='weight', shape=[3, 3, 64, 128], dtype=tf.float32)
            bias = tf.get_variable(name='bias', shape=[128], dtype=tf.float32)
            layer3 = tf.nn.conv2d(input=layer2, filter=weight, strides=[1, 2, 2, 1], padding='SAME') + bias
            layer3 = tf.nn.relu(layer3)
            print("layer3's shape : ", layer3.shape)
            # Conv -> (?,  32,  32, 128)

        with tf.variable_scope('conv4'):
            weight = tf.get_variable(name='weight', shape=[3, 3, 128, 256], dtype=tf.float32)
            bias = tf.get_variable(name='bias', shape=[256], dtype=tf.float32)
            layer4 = tf.nn.conv2d(input=layer3, filter=weight, strides=[1, 2, 2, 1], padding='SAME') + bias
            layer4 = tf.nn.relu(layer4)
            print("layer4's shape : ", layer4.shape)
            # Conv -> (?,  16,  16, 256)

        with tf.variable_scope('conv5'):
            weight = tf.get_variable(name='weight', shape=[3, 3, 256, 512], dtype=tf.float32)
            bias = tf.get_variable(name='bias', shape=[512], dtype=tf.float32)
            layer5 = tf.nn.conv2d(input=layer4, filter=weight, strides=[1, 2, 2, 1], padding='SAME') + bias
            layer5 = tf.nn.relu(layer5)
            print("layer5's shape : ", layer5.shape)
            # Conv -> (?,  8,  8, 512)

        with tf.variable_scope('conv6'):
            weight = tf.get_variable(name='weight', shape=[3, 3, 512, 1024], dtype=tf.float32)
            bias = tf.get_variable(name='bias', shape=[1024], dtype=tf.float32)
            layer6 = tf.nn.conv2d(input=layer5, filter=weight, strides=[1, 2, 2, 1], padding='SAME') + bias
            layer6 = tf.nn.relu(layer6)
            print("layer6's shape : ", layer6.shape)
            # Conv -> (?,  4,  4, 1024)

        print("decoder start")
        # decoder ######################################################################################################
        with tf.variable_scope('deconv1'):
            weight = tf.get_variable(name='weight', shape=[3, 3, 512, 1024], dtype=tf.float32)

            output_shape = layer6.get_shape().as_list()
            output_shape[0] = 10
            output_shape[1] *= 2
            output_shape[2] *= 2
            output_shape[3] = weight.get_shape().as_list()[2]

            layer7 = tf.nn.conv2d_transpose(value=layer6, filter=weight, output_shape=output_shape
                                            , strides=[1, 2, 2, 1], padding='SAME')
            layer7 = tf.nn.relu(layer7)
            print("layer7's shape : ", layer7.shape)
            # DeConv -> (?, 8, 8, 512)

        with tf.variable_scope('deconv2'):
            weight = tf.get_variable(name='weight', shape=[3, 3, 256, 512], dtype=tf.float32)

            output_shape = layer7.get_shape().as_list()
            output_shape[0] = 10
            output_shape[1] *= 2
            output_shape[2] *= 2
            output_shape[3] = weight.get_shape().as_list()[2]

            layer8 = tf.nn.conv2d_transpose(value=layer7, filter=weight, output_shape=output_shape
                                            , strides=[1, 2, 2, 1], padding='SAME')
            layer8 = tf.nn.relu(layer8)
            print("layer8's shape : ", layer8.shape)
            # DeConv -> (?, 16, 16, 256)

        with tf.variable_scope('deconv3'):
            weight = tf.get_variable(name='weight', shape=[3, 3, 128, 256], dtype=tf.float32)

            output_shape = layer8.get_shape().as_list()
            output_shape[0] = 10
            output_shape[1] *= 2
            output_shape[2] *= 2
            output_shape[3] = weight.get_shape().as_list()[2]

            layer9 = tf.nn.conv2d_transpose(value=layer8, filter=weight, output_shape=output_shape
                                            , strides=[1, 2, 2, 1], padding='SAME')
            layer9 = tf.nn.relu(layer9)
            print("layer9's shape : ", layer9.shape)
            # DeConv -> (?, 32, 32, 128)

        with tf.variable_scope('deconv4'):
            weight = tf.get_variable(name='weight', shape=[3, 3, 64, 128], dtype=tf.float32)

            output_shape = layer9.get_shape().as_list()
            output_shape[0] = 10
            output_shape[1] *= 2
            output_shape[2] *= 2
            output_shape[3] = weight.get_shape().as_list()[2]

            layer10 = tf.nn.conv2d_transpose(value=layer9, filter=weight, output_shape=output_shape
                                             , strides=[1, 2, 2, 1], padding='SAME')
            layer10 = tf.nn.relu(layer10)
            print("layer10's shape : ", layer10.shape)
            # DeConv -> (?, 64, 64, 64)

        with tf.variable_scope('deconv5'):
            weight = tf.get_variable(name='weight', shape=[3, 3, 32, 64], dtype=tf.float32)

            output_shape = layer10.get_shape().as_list()
            output_shape[0] = 10
            output_shape[1] *= 2
            output_shape[2] *= 2
            output_shape[3] = weight.get_shape().as_list()[2]

            layer11 = tf.nn.conv2d_transpose(value=layer10, filter=weight, output_shape=output_shape
                                             , strides=[1, 2, 2, 1], padding='SAME')
            layer11 = tf.nn.relu(layer11)
            print("layer11's shape : ", layer11.shape)
            # DeConv -> (?, 128, 128, 32)

        with tf.variable_scope('deconv6'):
            weight = tf.get_variable(name='weight', shape=[3, 3, 3, 32], dtype=tf.float32)

            output_shape = layer11.get_shape().as_list()
            output_shape[0] = 10
            output_shape[1] = 256
            output_shape[2] = 256
            output_shape[3] = weight.get_shape().as_list()[2]

            layer12 = tf.nn.conv2d_transpose(value=layer11, filter=weight, output_shape=output_shape
                                             , strides=[1, 2, 2, 1], padding='SAME')
            layer12 = tf.nn.relu(layer12)
            logits = layer12

            d['logits'] = logits
            print("layer12's shape : ", layer12.shape)
            # DeConv -> (?, 256, 256, 3)

        print("output's shape : ", layer12.shape)
        return d, logits

    def _build_loss(self):

        loss = tf.reduce_mean(tf.square(self.logits - self.y))
        loss = loss / (256 * 256)
        """
        로스 함수를 리턴하는 함수 loss 는 mean square error
        :return: loss
        """
        return loss


if __name__ == "__main__":

    data = r"./data/train"
    x, y = util.read_color_data_set(data)
    train_data = dt.DataSet(x, y)
    print(train_data)
    m = Model(input_shape=[256, 256, 1], output_shape=[256, 256, 3])

    optimizer = tf.train.AdamOptimizer(learning_rate=0.01).minimize(m.loss)
    batch_size = 10

    # train

    graph = tf.get_default_graph()
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    with tf.Session(graph=graph, config=config) as sess:

        save_dir = './save'
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        saver = tf.train.Saver()
        sess.run(tf.global_variables_initializer())
        print('Learning started. It takes sometime.')
        iterator = train_data.num_of_data // batch_size
        print("iterator : ", iterator)
        for epoch in range(10):
            avg_cost = 0
            for i in range(iterator):

                batch_x, batch_y = train_data.next_batch(batch_size)
                # print(batch_x.shape, batch_y.shape)
                _, loss = sess.run([optimizer, m.loss], feed_dict={m.x: batch_x, m.y: batch_y})
                # print("iterator : ", i, ", loss : ", loss)
                # print("batch_y = ", batch_y)
                avg_cost += loss

            print("epoch : ", epoch, ", loss : ", avg_cost/iterator)
            saver.save(sess, os.path.join(save_dir, 'color.ckpt'))  # 현재 모델의 파라미터들을 저장함

        print("Learning Done")

