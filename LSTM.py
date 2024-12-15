import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data


# deal with specification here
# dataset should be a csv file with one abc file stored in each line?
# special tokens at the beginning: mode, time signature,  type of song, genre
# body of each line is a vector of notes and bar lines

# should we try parsing bars as their own tokens? Probably won't work since there are so many unique bars
# how do we make sure the model generates a song of right length?
# could there be any way of mathematically keeping track perhaps?
# problem is having it output barlines at the right moment.
# we could just build the model without barlines and add them later?
#

















