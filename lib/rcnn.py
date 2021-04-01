from utils import LogoDataset, LogoConfig, evaluate_model, plot_actual_vs_predicted
from mrcnn.model import MaskRCNN

import os

import tensorflow as tf


class LogoClassifier:

    def __init__(self, dataset_base_dir, weights_file, model_dir='./'):
        self.dataset_base_dir = dataset_base_dir
        self.weights_path = weights_file
        self.model_dir = model_dir
        self._enable_gpu_processing()
        self._prepare_datasets()

    def train(self):
        model = MaskRCNN(mode='training', model_dir=self.model_dir, config=self.config)
        model.load_weights(self.weights_path, by_name=True)
        model.train(self.train_set, self.test_set, learning_rate=self.config.LEARNING_RATE, epochs=15, layers='heads')

    def test(self):

        model = MaskRCNN(mode='inference', model_dir=self.model_dir, config=self.config)
        model.load_weights(self.weights_path, by_name=True)

        test_mean_average_precision = evaluate_model(self.test_set, model, self.config)
        print(f"Testing set mean average precision: {test_mean_average_precision}")

        plot_actual_vs_predicted(self.test_set, model, self.config, filename='test_set_prediction_results.png')

    def _prepare_datasets(self):
        self.train_set = LogoDataset()
        self.train_set.load_dataset(dataset_dir=self.dataset_base_dir, is_training=True)
        self.train_set.prepare()

        self.test_set = LogoDataset()
        self.test_set.load_dataset(dataset_dir=self.dataset_base_dir, is_training=False)
        self.test_set.prepare()

        self.config = LogoConfig()
        self.config.display()

    @staticmethod
    def _enable_gpu_processing():
        gpus = tf.config.experimental.list_physical_devices('GPU')

        if gpus:
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
            except RuntimeError as e:
                print(e)


if __name__ == "__main__":
    classifier = LogoClassifier(dataset_base_dir=r'C:\Users\bagool\Downloads\openlogo',
                                weights_file=os.path.join('../data', 'mask_rcnn_logo_cfg_0001.h5'))

    classifier.test()
