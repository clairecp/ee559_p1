import torch
from torch import nn
from torch.nn import functional as F

class NetSharing1(nn.Module):
    """ Base module """
    def __init__(self, nb_hidden=50):
        super(NetSharing1, self).__init__()
        self.name = "NetSharing1"
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3)
        self.fc1 = nn.Linear(512, nb_hidden)
        self.fc2 = nn.Linear(nb_hidden, 1)
 
    def forward(self, x):
        x0 = x[:,0,:,:].view(-1,1,14,14)
        x1 = x[:,1,:,:].view(-1,1,14,14)        
        x_list = [x0, x1]
        res = []        
        for x in x_list:
            x = F.relu(F.max_pool2d(self.conv1(x), kernel_size=2, stride=2))
            x = F.relu(F.max_pool2d(self.conv2(x), kernel_size=2, stride=2))
            x = x.view(-1, 256)
            res.append(x)
        x = torch.cat((res[0], res[1]),1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
    
    def return_new(self):
        return NetSharing1()

    
class NetSharing2(nn.Module):
    """ Increase the number of channels produced by the convolutions """
    def __init__(self, nb_hidden=50):
        super(NetSharing2, self).__init__()
        self.name = "NetSharing2"
        self.conv1 = nn.Conv2d(1, 64, kernel_size=3)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3)
        self.fc1 = nn.Linear(512, nb_hidden)
        self.fc2 = nn.Linear(2*nb_hidden, 1)
 
    def forward(self, x):
        x0 = x[:,0,:,:].view(-1,1,14,14)
        x1 = x[:,1,:,:].view(-1,1,14,14)
        x_list = [x0, x1]
        res = []
        for x in x_list:
            x = F.relu(F.max_pool2d(self.conv1(x), kernel_size=2, stride=2))
            x = F.relu(F.max_pool2d(self.conv2(x), kernel_size=2, stride=2))
            x = x.view(-1, 512)
            x = F.relu(self.fc1(x))
            res.append(x)
        x = torch.cat((res[0], res[1]), 1)
        x = self.fc2(x)
        return x
    
    def return_new(self):
        return NetSharing2()
    
class NetSharing3(nn.Module): # 0.86 without dropout in 50 iter  # 0.85 with p=0.5 #0.856 with p=0.3
    # Current config 0.87
    """ Increase the number of channels produced by the convolutions """
    def __init__(self, nb_hidden=100):
        super(NetSharing3, self).__init__()
        self.name = "NetSharing3"
        self.conv1 = nn.Conv2d(1, 64, kernel_size=3)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3)
        self.fc1 = nn.Linear(512, nb_hidden)
        self.fc2 = nn.Linear(nb_hidden, 1)
        self.drop = nn.Dropout(p=0)
 
    def forward(self, x):
        x0 = x[:,0,:,:].view(-1,1,14,14)
        x1 = x[:,1,:,:].view(-1,1,14,14)
        x_list = [x0, x1]
        res = []
        for x in x_list:
            x = F.relu(F.max_pool2d(self.conv1(x), kernel_size=2, stride=2))
            x = F.relu(F.max_pool2d(self.conv2(x), kernel_size=2, stride=2))
            x = x.view(-1, 512)
            x = self.drop(F.relu(self.fc1(x)))
            res.append(x)
 
        #x = torch.cat((res[0], res[1]), 1)
        x = res[0] - res[1]
        x = self.fc2(x)
        return x
    
    def return_new(self):
        return NetSharing3()
    
class NetSharing4(nn.Module): # 0.85 with p=0.3 #0.84 with p=0.1
    # Current config 0.86
    """ Increase the number of channels produced by the convolutions """
    def __init__(self, nb_hidden=40):
        super(NetSharing4, self).__init__()
        self.name = "NetSharing4"
        self.conv1 = nn.Conv2d(1, 8, kernel_size=3)
        self.conv2 = nn.Conv2d(8, 16, kernel_size=5)
        self.fc1 = nn.Linear(144, nb_hidden)
        self.fc2 = nn.Linear(nb_hidden, 1)
        self.drop = nn.Dropout(p=0.5)
 
    def forward(self, x):
        x0 = x[:,0,:,:].view(-1,1,14,14)
        x1 = x[:,1,:,:].view(-1,1,14,14)
        x_list = [x0, x1]
        res = []
        for x in x_list:
            x = F.relu(F.max_pool2d(self.conv1(x), kernel_size=2, stride=1))
            x = F.relu(F.max_pool2d(self.conv2(x), kernel_size=2, stride=2))
            #print(x.shape)
            x = x.view(-1, 144)
            x = self.drop(F.relu(self.fc1(x)))
            res.append(x)
 
        x = res[1] - res[0]
        x = self.fc2(x)
        return x
    
    def return_new(self):
        return NetSharing4()
    
    
class NetSharing5(nn.Module): # 0.84 with p=0.1 and p=0.2 in 150 iter, retry with substract and p=0.4
    #0.84 with sub and p=0.4 #0.85 with sub and p=0.1
    # Current config 0.83
    def __init__(self, nb_hidden=10): #0.8 with nb_hidden=10 and p=0.5
        super(NetSharing5, self).__init__()
        self.name = "NetSharing5"
        self.conv1 = nn.Conv2d(1, 4, kernel_size=3)
        self.conv2 = nn.Conv2d(4, 8, kernel_size=4)
        self.conv3 = nn.Conv2d(8, 12, kernel_size=3)
        self.fc1 = nn.Linear(48, nb_hidden)
        self.fc2 = nn.Linear(nb_hidden, 1)
        self.drop = nn.Dropout(p=0)
 
    def forward(self, x):
        x0 = x[:,0,:,:].view(-1,1,14,14)
        x1 = x[:,1,:,:].view(-1,1,14,14)
        x_list = [x0, x1]
        res = []
        for x in x_list:
            x = F.relu(F.max_pool2d(self.conv1(x), kernel_size=2, stride=1))
            x = F.relu(F.max_pool2d(self.conv2(x), kernel_size=2, stride=1))
            x = F.relu(F.max_pool2d(self.conv3(x), kernel_size=2, stride=2))
            x = x.view(-1, 48)
            x = self.drop(F.relu(self.fc1(x)))
            res.append(x)
 
        #x = torch.cat((res[0], res[1]),1)
        x = res[0] - res[1]
        x = self.fc2(x)
        return x
    
    def return_new(self):
        return NetSharing5()
    
class NetSharing6(nn.Module): #0.673 for p=0.5  # 0.84 with p=0.1 !! # 0.82 with p=0 # 0.81 with p=0.2 retrying with substraction and nb_hidden=6 instead of 4
    #0.86 with p=0.15 and substraction
    #0.82 with p=0.3
    # Current config 0.82
    def __init__(self, nb_hidden=6):
        super(NetSharing6, self).__init__()
        self.name = "NetSharing6"
        self.conv1 = nn.Conv2d(1, 3, kernel_size=3)
        self.conv2 = nn.Conv2d(3, 6, kernel_size=3)
        self.conv3 = nn.Conv2d(6, 12, kernel_size=4)
        self.fc1 = nn.Linear(48, nb_hidden)
        self.fc2 = nn.Linear(nb_hidden, 1)
        self.drop = nn.Dropout(p=0) # retry with p=0.2
 
    def forward(self, x):
        x0 = x[:,0,:,:].view(-1,1,14,14)
        x1 = x[:,1,:,:].view(-1,1,14,14)
        x_list = [x0, x1]
        res = []
        for x in x_list:
            x = F.relu(F.max_pool2d(self.conv1(x), kernel_size=2, stride=1))
            x = F.relu(F.max_pool2d(self.conv2(x), kernel_size=2, stride=1))
            x = F.relu(F.max_pool2d(self.conv3(x), kernel_size=2, stride=2))
            #print(x.shape)
            x = x.view(-1, 48)
            x = self.drop(F.relu(self.fc1(x)))
            res.append(x)
 
        #x = torch.cat((res[0], res[1]),1)
        x = res[0] - res[1]
        x = self.fc2(x)
        return x
    
    def return_new(self):
        return NetSharing6()
    
class NetSharing7(nn.Module): #0.81 with p=0.5 in 75 # 0.84 with p=0.2 #0.82 with p =0.1 # retrying with substraction
    # Current config 0.85
    def __init__(self, nb_hidden=4):
        super(NetSharing7, self).__init__()
        self.name = "NetSharing7"
        self.conv1 = nn.Conv2d(1, 4, kernel_size=3)
        self.conv2 = nn.Conv2d(4, 6, kernel_size=4)
        self.fc1 = nn.Linear(96, nb_hidden)
        self.fc2 = nn.Linear(nb_hidden, 1)
        self.drop = nn.Dropout(p=0.1)
 
    def forward(self, x):
        x0 = x[:,0,:,:].view(-1,1,14,14)
        x1 = x[:,1,:,:].view(-1,1,14,14)
        x_list = [x0, x1]
        res = []
        for x in x_list:
            x = F.relu(F.max_pool2d(self.conv1(x), kernel_size=2, stride=1))
            x = F.relu(F.max_pool2d(self.conv2(x), kernel_size=2, stride=2))
            #print(x.shape)
            x = x.view(-1, 96)
            x = self.drop(F.relu(self.fc1(x)))
            res.append(x)
 
        #x = torch.cat((res[0], res[1]),1)
        x = res[0] - res[1]
        x = self.fc2(x)
        return x
    
    def return_new(self):
        return NetSharing7()
    
class NetSharing8(nn.Module): # 0.84 with p=0.5 in 75 # 0.87 with p=0.3 
    # 0.87 with p=0.15 retrying with subtraction
    # 0.85 with p=0.15 and substract
    # current config 0.83
    def __init__(self, nb_hidden=10):
        super(NetSharing8, self).__init__()
        self.name = "NetSharing8"
        self.conv1 = nn.Conv2d(1, 4, kernel_size=3)
        self.conv2 = nn.Conv2d(4, 6, kernel_size=4)
        self.fc1 = nn.Linear(96, nb_hidden)
        self.fc2 = nn.Linear(nb_hidden, 1)
        self.drop = nn.Dropout(p=0)
 
    def forward(self, x):
        x0 = x[:,0,:,:].view(-1,1,14,14)
        x1 = x[:,1,:,:].view(-1,1,14,14)
        x_list = [x0, x1]
        res = []
        for x in x_list:
            x = F.relu(F.max_pool2d(self.conv1(x), kernel_size=2, stride=1))
            x = F.relu(F.max_pool2d(self.conv2(x), kernel_size=2, stride=2))
            #print(x.shape)
            x = x.view(-1, 96)
            x = self.drop(F.relu(self.fc1(x)))
            res.append(x)
 
        #x = torch.cat((res[0], res[1]),1)
        x = res[0] - res[1]
        x = self.fc2(x)
        return x
    
    def return_new(self):
        return NetSharing8()
    
class NetSharing9(nn.Module): # 0.84 with p=0.5 in 75 # 0.87 with p=0.3 
    # 0.87 with p=0.15 retrying with subtraction
    # 0.81 with sub
    # retrying with cat and no drop
    def __init__(self, nb_hidden=10):
        super(NetSharing9, self).__init__()
        self.name = "NetSharing9"
        self.conv1 = nn.Conv2d(1, 4, kernel_size=3)
        self.conv2 = nn.Conv2d(4, 6, kernel_size=4)
        self.fc1 = nn.Linear(2*96, nb_hidden)
        self.fc2 = nn.Linear(nb_hidden, 1)
        self.drop = nn.Dropout(p=0.)
 
    def forward(self, x):
        x0 = x[:,0,:,:].view(-1,1,14,14)
        x1 = x[:,1,:,:].view(-1,1,14,14)
        x_list = [x0, x1]
        res = []
        for x in x_list:
            x = F.relu(F.max_pool2d(self.conv1(x), kernel_size=2, stride=1))
            x = F.relu(F.max_pool2d(self.conv2(x), kernel_size=2, stride=2))
            #print(x.shape)
            x = x.view(-1, 96)
            res.append(x)
 
        x = torch.cat((res[0], res[1]),1)
        #x = res[0] - res[1]
        x = self.drop(F.relu(self.fc1(x)))
        x = self.fc2(x)
        return x
    
    def return_new(self):
        return NetSharing9()
    