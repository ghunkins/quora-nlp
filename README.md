# Quora Same Question Classification

This project is an initial solution to the Quora Same Question Classification challenge.

Programmer: `Gregory D. Hunkins`

### Preprocessing

Sentences were split, cleaned, and encoded using the [GloVe](https://nlp.stanford.edu/projects/glove/) vector embedding space.

### Model

The model is a simple LSTM followed by a dense layer. We use an Adam optimizer. All else
is standard for a binary classification problem.

Training is allowed until the validation logloss is no longer decreasing. The model's best
weights are then restored.

A few variations of this model were trained and tested, but this simple version ended up performing the best.

```
__________________________________________________________________________________________________
Layer (type)                    Output Shape         Param #     Connected to
==================================================================================================
input_4 (InputLayer)            (None, 50, 100)      0
__________________________________________________________________________________________________
input_5 (InputLayer)            (None, 50, 100)      0
__________________________________________________________________________________________________
model_3 (Model)                 (None, 100)          80800       input_4[0][0]
                                                                 input_5[0][0]
__________________________________________________________________________________________________
concatenate_2 (Concatenate)     (None, 200)          0           model_3[1][0]
                                                                 model_3[2][0]
__________________________________________________________________________________________________
dense_3 (Dense)                 (None, 100)          20100       concatenate_2[0][0]
__________________________________________________________________________________________________
dropout_5 (Dropout)             (None, 100)          0           dense_3[0][0]
__________________________________________________________________________________________________
dense_4 (Dense)                 (None, 1)            101         dropout_5[0][0]
==================================================================================================
Total params: 101,001
Trainable params: 101,001
Non-trainable params: 0
__________________________________________________________________________________________________
```

The provided test set was split 80-20 to allow for a validation set. The best epoch gave the following accuracy metrics.

```
loss: 0.3098
acc: 0.8585
val_loss: 0.3932
val_acc: 0.8207
```

Unfortunately, a Kaggle reported accuracy on the official test set was not obtained. This is a #TODO (ghunkins).

### Moving Forward & TODO

Clearly the reported accuracy metrics are only acceptable for a first-pass. A guide for
where to improve can be followed from Abhishek Thakur's solution [here](https://www.linkedin.com/pulse/duplicate-quora-question-abhishek-thakur/).

Major areas to look into are:

1. Faster cleaning solutions (better spell check)
2. Feature Engineering (i.e. question length, fuzzy distances, glove distance, etc.)
3. Integration of an Embedding Layer for GloVe
3. A deeper architecture (convolutional layers, more dense final layers)

For now this solution can be seen as a first-pass.



