#!/usr/bin/env python3
import tensorflow as tf
import sys
from PIL import Image
import numpy

def get_batch_from_file(path):
	im = Image.open("../small-client.png")
	pix = numpy.array(im.getdata()).reshape(-1 , 28, 28, 1)
	return (pix)

def main(f: str):
    """
        Main function of the program where
        f is a file to a tf model
    """
    save = tf.train.import_meta_graph("mnist.ckpt.meta")
    graph = tf.get_default_graph()

    tf_features = tf.placeholder(tf.float32, [None, 784]);
    tf_targets = tf.placeholder(tf.float32, [None, 10]);
    
    sess = tf.Session()
    save.restore(sess, "./mnist.ckpt")
    tf.reset_default_graph()
    
    pic = get_batch_from_file("../small-client.png")
    print(pic)
    print(sess.run(feed_dict= {
	tf_features: pic,
        tf_targets: 0}))

if __name__ == "__main__":
    f = sys.argv[1]
    main(f);
