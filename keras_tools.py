# coding=utf-8
import tensorflow as tf
from keras import backend as K


def keras_allow_growth():
    """
    This function instruct Keras (and tensorflow at the back) to allocate only the available amount of GPU memory
    and not all of it
    :return:
    """
    # TensorFlow wizardry
    config = tf.ConfigProto()

    # Don't pre-allocate memory; allocate as-needed
    config.gpu_options.allow_growth = True

    # Create a session with the above options specified.
    K.tensorflow_backend.set_session(tf.Session(config=config))


def keras_allow_growth_memory_limit(memory_fraction=0.5):
    """
    This function instruct Keras (and tensorflow at the back) to allocate up to only the proportion of available
    GPU memory provided by memory_fraction and not all of it.
    This does not seem to work as expected. Only one of the 2 options seems to be effective.
    :param memory_fraction:
    :return:
    """
    # TensorFlow wizardry
    config = tf.ConfigProto()

    # Don't pre-allocate memory; allocate as-needed
    config.gpu_options.allow_growth = True

    # Only allow a total of half the GPU memory to be allocated
    config.gpu_options.per_process_gpu_memory_fraction = memory_fraction

    # Create a session with the above options specified.
    K.tensorflow_backend.set_session(tf.Session(config=config))


def keras_allow_memory_limit(memory_fraction=0.5):
    """
    This function instruct Keras (and tensorflow at the back) both to allocate up to only the proportion of available
    GPU memory provided by memory_fraction and not all of it and also only the necessary memory for the model run.

    Example if available memory is 7GB and the model requirements are at 25.GB then with the above function:
    7/2=3.5GB will be allocated by Keras from which 2.5 will be used from the model (the other would appear
    allocated though)

    :param memory_fraction:
    :return:
    """
    # TensorFlow wizardry
    config = tf.ConfigProto()

    # Don't pre-allocate memory; allocate as-needed
    # config.gpu_options.allow_growth = True

    # Only allow a total of half the GPU memory to be allocated
    config.gpu_options.per_process_gpu_memory_fraction = memory_fraction

    # Create a session with the above options specified.
    K.tensorflow_backend.set_session(tf.Session(config=config))


def define_devices(use_cpu=True):
    num_cores = 1
    if not use_cpu:
        num_GPU = 1
        num_CPU = 1
    else:
        num_CPU = 1
        num_GPU = 0

    config = tf.ConfigProto(intra_op_parallelism_threads=num_cores,
                            inter_op_parallelism_threads=num_cores,
                            allow_soft_placement=True,
                            device_count={'CPU': num_CPU,
                                          'GPU': num_GPU}
                            )

    session = tf.Session(config=config)
    K.set_session(session)


def huber_loss(y_true, y_pred, weights=1.0, delta=1.0):
    """
    Just calling tensorflow huber loss function from keras
    :param y_true:
    :param y_pred:
    :param weights:
    :param delta:
    :return:
    """
    # tf.losses.huber_loss(
    #     labels,
    #     predictions,
    #     weights=1.0,
    #     delta=1.0,
    #     scope=None,
    #     loss_collection=tf.GraphKeys.LOSSES,
    #     reduction=Reduction.SUM_BY_NONZERO_WEIGHTS
    # )

    return tf.losses.huber_loss(y_true, y_pred, weights, delta)
