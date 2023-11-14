_base_ = '/content/mmdetection/configs/mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco.py'

# We also need to change the num_classes in head to match the dataset's annotation
model = dict(
    roi_head=dict(
        bbox_head=dict(num_classes=3),
        mask_head=dict(num_classes=3)))


# Modify dataset related settings
dataset_type = 'mmdetection_seg'
classes = ('multimetre','raspberry','salca')

data = dict(
    train=dict(
          img_prefix='/content/mmdetection_seg/train/',
          classes=classes,
          ann_file='/content/mmdetection_seg/train/train.json'),
    val=dict(
        img_prefix='/content/mmdetection_seg/test/',
        classes=classes,
        ann_file='/content/mmdetection_seg/test/val.json'),
    test=dict(
        img_prefix='/content/mmdetection_seg/test/',
        classes=classes,
        ann_file='/content/mmdetection_seg/test/val.json'))