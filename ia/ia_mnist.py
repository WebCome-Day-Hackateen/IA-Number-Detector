#!/usr/bin/env python3
import tensorflow as tf
import sys

def get_batch_from_file(path):
    with open(path) as f:
        

def main(f: str):
    """
        Main function of the program where
        f is a file to a tf model
    """
    save = tf.train.import_meta_graph("mnist.ckpt.meta")
    graph = tf.get_default_graph()
    
    sess = tf.Session()
    save.restore(sess, "./mnist.ckpt")
    tf.reset_default_graph()
    
    get_batch_from_file("../small-client.png")
    print(sess.run(feed_dict={picture,}))

if __name__ == "__main__":
    f = sys.argv[1]
    main(f);
