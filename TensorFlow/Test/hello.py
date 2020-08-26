import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import tensorflow as tf

hello = tf.constant("hello world")

print(hello)
print(hello.numpy()) # Tensor flow(Cuda, cuDNN) Test code