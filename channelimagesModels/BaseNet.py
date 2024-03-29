from torch import nn
from torch.nn import functional as F

input_size = 14*14

class BaseNet1C(nn.Module):
    """ Fully-connected module for _1channel2images framework (1C) """
    def __init__(self, nb_classes=10, nb_hidden=200):
        super(BaseNet1C, self).__init__()
        self.name = "BaseNet1C"
        self.fc1 = nn.Linear(1*input_size, nb_hidden)
        self.fc2 = nn.Linear(nb_hidden, nb_hidden)
        self.fc3 = nn.Linear(nb_hidden, nb_classes)
        
    def forward(self, x):
        # every 1x14x14 image is reshaped as a 196 1D tensor, len(x) = batch_size
        x = x.reshape((len(x), -1))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
    def return_new(self):
        return BaseNet1C()

######################################################################

class BaseNet2C(nn.Module):
    """ Fully-connected module for _2channels1image framework (2C) """
    def __init__(self, nb_classes=1, nb_hidden=50):
        super(BaseNet2C, self).__init__()
        self.name = "BaseNet2C"
        self.fc1 = nn.Linear(2*input_size, nb_hidden)
        self.fc2 = nn.Linear(nb_hidden, nb_hidden)
        self.fc3 = nn.Linear(nb_hidden, nb_classes)
        self.drop = nn.Dropout(p=0.5)
        
    def forward(self, x):
        # every 2x14x14 image is reshaped as a 1D tensor
        x = x.reshape((len(x), -1))
        x = F.relu(self.fc1(x))
        x = self.drop(F.relu(self.fc2(x)))
        x = self.drop(self.fc3(x))
        return x
    
    def return_new(self):
        return BaseNet2C()
        
        



