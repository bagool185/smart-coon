from enum import IntEnum
from xml.etree import ElementTree
from typing import Tuple, List

from matplotlib import pyplot
from matplotlib.patches import Rectangle
from mrcnn.utils import Dataset, compute_ap
from mrcnn.config import Config
import numpy as np

import os

from mrcnn.model import MaskRCNN, load_image_gt, mold_image

from lib.constants import LOGOS


def validate_stock_symbol(stock_symbol: str) -> bool:
    if stock_symbol is None or stock_symbol == '':
        print("I need the symbol in order to fetch the historical market data")
        return False

    return True


class CommandOption(IntEnum):
    EXIT = 0
    WIKI = 1
    STOCK_DATA = 2
    STOCK_HISTORY = 3
    LOGIC_INPUT_ADD = 31
    LOGIC_INPUT_CHECK = 32
    RETRY = 99


class LogoConfig(Config):
    NAME = 'logo_cfg'
    # logos + background
    NUM_CLASSES = len(LOGOS) + 1
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    LEARNING_RATE = 0.01
    STEPS_PER_EPOCH = 100


class LogoDataset(Dataset):

    def load_dataset(self, dataset_dir: str, is_training=True):

        [self.add_class('dataset', index + 1, logo) for index, logo in enumerate(LOGOS)]

        images_dir = os.path.join(dataset_dir, 'images')
        annotations_dir = os.path.join(dataset_dir, 'annotations')

        for index, filename in enumerate(os.listdir(images_dir)):
            # file name without extension
            image_id = os.path.splitext(filename)[0]

            if is_training and index >= 10000:
                continue

            if not is_training and index < 10000:
                continue

            img_path = os.path.join(images_dir, filename)
            annotation_path = os.path.join(annotations_dir, f'{image_id}.xml')
            self.add_image('dataset', image_id=image_id, path=img_path, annotation=annotation_path)

    def load_mask(self, image_id):
        info = self.image_info[image_id]
        path = info['annotation']
        boxes, width, height, name = self.extract_boxes(path)

        masks = np.zeros([height, width, len(boxes)], dtype='uint8')

        class_ids = list()

        for i in range(len(boxes)):
            box = boxes[i]
            row_start, row_end = box[1], box[3]
            col_start, col_end = box[0], box[2]
            masks[row_start:row_end, col_start:col_end, i] = 1
            class_ids.append(self.class_names.index(name))

        return masks, np.asarray(class_ids, dtype='int32')

    def image_reference(self, image_id):
        info = self.image_info[image_id]
        return info['path']

    @staticmethod
    def extract_boxes(filename: str) -> Tuple[List[List[int]], int, int, str]:

        tree = ElementTree.parse(filename)

        root = tree.getroot()
        boxes = list()

        name = root.find('.//object/name').text

        for box in root.findall('.//bndbox'):
            xmin = int(box.find('xmin').text)
            ymin = int(box.find('ymin').text)
            xmax = int(box.find('xmax').text)
            ymax = int(box.find('ymax').text)

            coords = [xmin, ymin, xmax, ymax]
            boxes.append(coords)

        width = int(root.find('.//size/width').text)
        height = int(root.find('.//size/height').text)

        return boxes, width, height, name


def evaluate_model(dataset: LogoDataset, model: MaskRCNN, configuration: LogoConfig) -> np.ndarray:
    average_precisions = list()

    for image_id in dataset.image_ids:
        image, image_meta, gt_class_id, gt_bbox, gt_mask = load_image_gt(dataset, configuration, image_id,
                                                                         use_mini_mask=False)
        scaled_image = mold_image(image, configuration)
        sample = np.expand_dims(scaled_image, 0)
        yhat = model.detect(sample, verbose=0)
        r = yhat[0]
        average_precision, _, _, _ = compute_ap(gt_bbox, gt_class_id, gt_mask, r['rois'], r['class_ids'], r['scores'],
                                                r['masks'])
        average_precisions.append(average_precision)

    mean_average_precision = np.mean(average_precisions)
    return mean_average_precision


def plot_actual_vs_predicted(dataset: LogoDataset, model: MaskRCNN, configuration: LogoConfig, filename: str,
                             n_images=3):
    for i in range(n_images):
        image = dataset.load_image(i)
        mask, _ = dataset.load_mask(i)

        scaled_image = mold_image(image, configuration)
        sample = np.expand_dims(scaled_image, 0)
        pyplot.subplot(n_images, 2, i * 2 + 1)
        pyplot.axis('off')
        pyplot.imshow(image)
        pyplot.title('Actual')

        for j in range(mask.shape[2]):
            pyplot.imshow(mask[:, :, j], cmap='PuBuGn', alpha=0.3)

        pyplot.subplot(n_images, 2, i * 2 + 2)
        pyplot.axis('off')
        pyplot.imshow(image)
        pyplot.title('Predicted')
        ax = pyplot.gca()

        yhat = model.detect(sample, verbose=0)[0]
        for box in yhat['rois']:
            y1, x1, y2, x2 = box
            width, height = x2 - x1, y2 - y1
            rect = Rectangle((x1, y1), width, height, fill=False, color='red')
            ax.add_patch(rect)

    pyplot.savefig(filename)
