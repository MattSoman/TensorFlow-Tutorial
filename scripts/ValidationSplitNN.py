"""
    ValidationSplitNN.py  - This example optimises the validation split fraction

    Copyright (C) 2020 Adrian Bevan, Queen Mary University of London

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import warnings
warnings.filterwarnings("ignore")
import tensorflow as tf
import matplotlib.pyplot as plt
import api

#
# Training configuration
#
ValidationSplit = [0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
BatchSize       = 20
Nepochs         = 50

DropoutValue    = 0.6

# The MNIST data is a standard data set of hand written numbers,
#     0, 1, 2, 3, 4, 5, 6, 7, 8, 9
# that can be found online at:
#
#    http://yann.lecun.com/exdb/mnist/
#
# We load these in via keras
x_train, y_train, x_test, y_test = api.getMNIST()

# now specify the loss function - cross entropy
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

all_loss     = []
all_val_loss = []
all_acc      = []
all_val_acc  = []

print("--------------------------------------------------------------------------------------------------------------")
print("Will scan through validation split values to explore the model performance as a function of this hyper parameter")
print("--------------------------------------------------------------------------------------------------------------\n\n")
print("Input data MNIST")
print("2 layer MLP with configuration 784:128:128:10")
print("Dropout value        = ", DropoutValue)
print("Leaky relu parameter = 0.1")
print("ValidationSplit      = ", ValidationSplit)
print("BatchSize            = ", BatchSize)
print("Nepochs              = ", Nepochs, "\n")
print("N(train)             = ", len(x_train))
print("N(test)              = ", len(x_test))

print("Number of training iterations = ", len(ValidationSplit))


for VS in ValidationSplit:
  print("\nTraining model using a validation split of ", VS)

  model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation=tf.keras.layers.LeakyReLU(alpha=0.1)),
    tf.keras.layers.Dropout(DropoutValue),
    tf.keras.layers.Dense(128, activation=tf.keras.layers.LeakyReLU(alpha=0.1)),
    tf.keras.layers.Dropout(DropoutValue),
    tf.keras.layers.Dense(10)
  ])


  # now we can train the model to make predictions.
  #   Use the ADAM optimiser
  #   Specify the metrics to report as accuracy
  #   Specify the loss function (see above)
  # the fit step specifies the number of training epochs
  model.compile(optimizer='adam', loss=loss_fn, metrics=['accuracy'])
  history  = model.fit(x_train, y_train, validation_split=VS, batch_size=BatchSize, epochs=Nepochs)

  all_loss.append(history.history['loss'][-1])
  all_val_loss.append(history.history['val_loss'][-1])
  all_acc.append(history.history['accuracy'][-1])
  all_val_acc.append(history.history['val_accuracy'][-1])
  

print("Display the evolution of the accuracy as a function of the validation sample fraction")
print("  ValidationSplit  = ", ValidationSplit)
print("  accuracy (train) = ", all_acc)
print("  accuracy (test)  = ", all_val_acc)

plt.plot(ValidationSplit, all_acc)
plt.plot(ValidationSplit, all_val_acc)
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('Validation sample fraction')
plt.legend(['train', 'validate'], loc='upper left')
print("Plotting the output to fig/ValidationSplit_MLP_accuracy.*")
plt.savefig("fig/ValidationSplit_MLP_accuracy.pdf")
plt.savefig("fig/ValidationSplit_MLP_accuracy.png")
#plt.show()
plt.clf()

print("Display the evolution of the loss as a function of the validation sample fraction")
print("  ValidationSplit  = ", ValidationSplit)
print("  loss (train) = ", all_loss)
print("  loss (test)  = ", all_val_loss)

# summarize history for loss
plt.plot(ValidationSplit, all_loss)
plt.plot(ValidationSplit, all_val_loss)
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('Validation sample fraction')
plt.legend(['train', 'validate'], loc='upper left')
print("Plotting the output to fig/ValidationSplit_MLP_loss.*")
plt.savefig("fig/ValidationSplit_MLP_loss.pdf")
plt.savefig("fig/ValidationSplit_MLP_loss.png")
#plt.show()

print("\nValidation sample fraction scan done\n")
