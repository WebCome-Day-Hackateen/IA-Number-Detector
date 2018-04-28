#!/bin/python3
#import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import datetime
from PIL import Image
import sys
import numpy as numpy

def get_batch_from_file(path):
         im = Image.open("../small-client.png").convert("L")
         #pix = numpy.array(im.getdata()).reshape(-1 , 28, 28, 1)
         return (im.getdata())

def main():
    #Dataset
    mnist = input_data.read_data_sets("input/data", one_hot=True)

    #plt.imshow(mnist.train.images[0].reshape(28, 28), cmap="gray")
    #plt.show();

    #Graph input
    tf_features = tf.placeholder(tf.float32, [None, 784])
    tf_targets = tf.placeholder(tf.float32, [None, 10])
    pkeep = tf.placeholder(tf.float32)


    #Reshape
    reshaped_input = tf.reshape(tf_features, shape=[-1, 28, 28, 1])

    #Poid et bias
    W1 = tf.Variable(tf.truncated_normal([6, 6, 1, 6], stddev=0.1))
    B1 = tf.Variable(tf.ones([6]) / 10)
    W2 = tf.Variable(tf.truncated_normal([5, 5, 6, 12], stddev=0.1))
    B2 = tf.Variable(tf.ones([12]) / 10)
    W3 = tf.Variable(tf.truncated_normal([4, 4, 12, 24], stddev=0.1))
    B3 = tf.Variable(tf.ones([24]) / 10)
    W4 = tf.Variable(tf.truncated_normal([7 * 7 * 24, 200], stddev=0.1))
    B4 = tf.Variable(tf.ones([200]) / 10)
    W5 = tf.Variable(tf.truncated_normal([200, 10], stddev=0.1))
    B5 = tf.Variable(tf.zeros([10]))

    #Operation
    Y1 = tf.nn.relu(tf.nn.conv2d(reshaped_input, W1, strides=[1, 1, 1, 1], padding='SAME') + B1)
    tf.summary.histogram("relu1", Y1)
    #Y1 = tf.nn.dropout(Yf, pkeep)
    Y2 = tf.nn.relu(tf.nn.conv2d(Y1, W2, strides=[1, 2, 2, 1], padding='SAME') + B2)
    #Y2 = tf.nn.dropout(Y2f, pkeep)
    tf.summary.histogram("relu2", Y2)
    Y3f = tf.nn.relu(tf.nn.conv2d(Y2, W3, strides=[1, 2, 2, 1], padding='SAME') + B3)
    tf.summary.histogram("relu3", Y3f)
    Y3 = tf.nn.dropout(Y3f, pkeep)

    Y_shaped = tf.reshape(Y3, shape=[-1, 7 * 7 * 24])

    Y4 = tf.nn.relu(tf.matmul(Y_shaped, W4) + B4)
    Y5 = tf.matmul(Y4, W5) + B5
    a1 = tf.nn.softmax(Y5)

    #Error
    l_rate = 0.002
    err = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=tf_targets, logits=Y5))
    train = tf.train.AdamOptimizer(l_rate).minimize(err)

    #accuracy
    good_pred = tf.equal(tf.argmax(a1, 1), tf.argmax(tf_targets, 1))
    res = tf.argmax(a1, 1);
    acc = tf.reduce_mean(tf.cast(good_pred, tf.float32))
    train_err_scalar = tf.summary.scalar("Train cost", err)
    train_acc_scalar = tf.summary.scalar("Train accuracy", acc)
    test_acc_scalar = tf.summary.scalar("Test accuracy", acc)

    #Run
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    train_summary_op = tf.summary.merge([train_err_scalar, train_acc_scalar])
    test_summary_op = tf.summary.merge([test_acc_scalar])

    epoch = 10000
    var = 0.45

    filename = "./logs/mnist_" + str(datetime.datetime.now()).replace(":", "x").replace("-", "x")
    writer = tf.summary.FileWriter(filename, graph=sess.graph)

    saver = tf.train.Saver()
    saver.restore(sess, "./mnist.ckpt")

    if sys.argv[1] == "1":
        saver.restore(sess, "./mnist.ckpt")
        tf.reset_default_graph()
        batches = numpy.reshape(numpy.array(get_batch_from_file("../small-client.png")), (1, 784))
        batches[batches == 255] = 1;
        batches[batches == 1] = 2;
        batches[batches == 0] = 1;
        batches[batches == 2] = 0;
        print (batches);
        c = sess.run([res], feed_dict={
                 tf_features: batches,
                 tf_targets: numpy.reshape([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], (1, 10)),
                 pkeep: 1.
        })
        print (c);
    else:
         for e in range(epoch):
            batch_features, batch_target = mnist.train.next_batch(100)
            print (batch_features[0])
            _, d = sess.run([train, train_summary_op], feed_dict={
	        tf_features: batch_features,
	        tf_targets: batch_target,
	        pkeep: var
	    })
            writer.add_summary(d, e)
            l_rate /= 1.2
            if e % 100 == 0:
                c, sum = sess.run([acc, test_summary_op], feed_dict={
                         tf_features: mnist.test.images,
                         tf_targets: mnist.test.labels,
                         pkeep: 1.
	        })
                writer.add_summary(sum, e)
                print("Accuracy: ", c)
                saver.save(sess, "/tmp/mnist.ckpt")
    # for e in range(epoch):
    #     sess.run(train, feed_dict={
    #         tf_features: mnist.train.images,
    #         tf_targets: mnist.train.labels
    #     })
    #     print(sess.run(acc, feed_dict={
    #         tf_features: mnist.train.images,
    #         tf_targets: mnist.train.labels
    #     }))
    #     print("epoch", e)

if __name__ == '__main__':
    main()
