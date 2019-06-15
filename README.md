# food-MNIST

Structure:
----------

```
pec/
    images/
        <class_name>/
            <image_id>.jpg
    meta/
        classes.txt
        test.json
        test.txt
        train.json
        train.txt
```

This dataset has been created from Food-101 dataset for quick training on the food dataset.

# Original README
All images can be found in the "images" folder and are organized per class. All image ids are unique and correspond to the foodspotting.com review ids. Thus the original articles can retrieved trough http://www.foodspotting.com/reviews/<image_id> or through the foodspotting api (http://www.foodspotting.com/api).

The test/train splitting used in the experiment of our paper, can be found in the "meta" directory.

For any questions on the original Food-101 dataset contact bossard@vision.ee.ethz.ch

