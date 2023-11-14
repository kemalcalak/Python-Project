_base_ = '/content/mmdetection/configs/faster_rcnn/faster_rcnn_r50_caffe_fpn_mstrain_3x_coco.py'

# We also need to change the num_classes in head to match the dataset's annotation
model = dict(
    roi_head=dict(
        bbox_head=dict(num_classes=4)))

# Modify dataset related settings
dataset_type = 'mmdet_data_f1'
classes = ('ferrari','mclaren','mercedes','redbull')

data = dict(
    train=dict(
        dataset=dict(
          img_prefix='/content/mmdet_data_f1/images/',
          classes=classes,
          ann_file='/content/mmdet_data_f1/train.json')
    ),
    val=dict(
        img_prefix='/content/mmdet_data_f1/images_val/',
        classes=classes,
        ann_file='/content/mmdet_data_f1/val.json'),
    test=dict(
        img_prefix='/content/mmdet_data_f1/images_val/',
        classes=classes,
        ann_file='/content/mmdet_data_f1/val.json'))