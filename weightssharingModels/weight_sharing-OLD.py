import torch
from torch import nn, optim
from torch.autograd import Variable
from torch.nn import functional as F

import sys
sys.path.insert(0, "../")
from generic_helpers import *

import time
import copy

""" FRAMEWORK FOR WEIGHTSHARING """

def train_model_ws(model, train_input, train_target, train_classes, test_input, test_target, test_classes, optimizer, mini_batch_size, nb_epochs, verbose):
    criterion = torch.nn.BCEWithLogitsLoss()
    train_target = train_target.type(torch.FloatTensor).view(-1, 1) # from torch.Size([1000]) to torch.Size([1000, 1])
    nb_samples = len(train_input)
    
    val_acc_history = []
    test_acc_history = []
    
    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0
    
    since = time.time()
    for e in range(0, nb_epochs):
        
        for phase in ['train', 'val']:
            if phase == 'train': model.train()
            else: model.eval()
                
            running_loss = 0.0
            running_corrects = 0
            
            for b in range(0, train_input.size(0), mini_batch_size):
                optimizer.zero_grad()
                with torch.set_grad_enabled(phase == 'train'):
                    output = model(train_input.narrow(0, b, mini_batch_size))
                    target = train_target.narrow(0, b, mini_batch_size)
                    loss = criterion(output, target)
                    
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()
                        
                running_loss += loss.item() * train_input.size(0)
                output_to_prediction = torch.ge(torch.sigmoid(output), 0.5)
                running_corrects += torch.sum(output_to_prediction == target.type(torch.ByteTensor))       

            epoch_loss = running_loss / nb_samples
            epoch_acc = running_corrects.double() / nb_samples
            
            if verbose and (e % 100 == 99):
                print('phase: %s, epoch: %d, loss: %.5f, acc: %.4f' %
                      (phase, e+1, epoch_loss, epoch_acc))
                
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())
            if phase == 'val':
                val_acc_history.append(epoch_acc)
                
        test_acc = test_model_ws(model, test_input, test_target)
        test_acc_history.append(test_acc)
                
    time_elapsed = time.time() - since
    print('Training complete in %.0f min %.0f s' % (time_elapsed // 60, time_elapsed % 60))
    print('Best val acc: %.4f' % (best_acc))
    
    model.load_state_dict(best_model_wts)
    return model, time_elapsed, best_acc.item(), val_acc_history, test_acc_history

######################################################################

def test_model_ws(model, test_input, test_target):
    model.eval()
    test_output = model(test_input)
    output_to_prediction = torch.ge(torch.sigmoid(test_output), 0.5).flatten()
    nb_correct = torch.sum(output_to_prediction == test_target.type(torch.ByteTensor)).item()
    acc_pairs = nb_correct / len(test_input)
    return acc_pairs

######################################################################
"""
def multiple_training_runs(model, nb_runs, optimizer, train_input, train_target, test_input, test_target, mini_batch_size=1000, nb_epochs=300, verbose=True, plot=True):
    list_time = []
    list_best_acc = [] # (best) accuracy on training set
    list_acc_test = [] # accuracy on test set
    list_val_acc_history = []
    list_test_acc_history = []
    
    initial_model_wts = copy.deepcopy(model.state_dict())
            
    for i in range(nb_runs):
        model.load_state_dict(initial_model_wts)
        model, time_elapsed, best_acc, val_acc_history, test_acc_history = train_model_ws(model, train_input, train_target, test_input, test_target, optimizer, mini_batch_size=mini_batch_size, nb_epochs=nb_epochs, verbose=verbose)
        list_time.append(time_elapsed)
        list_best_acc.append(best_acc)
        list_val_acc_history.append(val_acc_history)
        list_test_acc_history.append(test_acc_history)
        
        acc_test = test_model_ws(model, test_input, test_target)
        list_acc_test.append(acc_test)
        
    if plot == True:
        title = 'Plot for 10 runs with weight_sharing framework (binary cross-entropy loss) and model = {}, \n accuracy obtained during training (model in eval mode) on the training set, and on the test set'.format(model.name)
        mean_val_acc_history, std_val_acc_history = mean_per_epoch_list(list_val_acc_history)
        mean_test_acc_history, std_test_acc_history = mean_per_epoch_list(list_test_acc_history)
        plot_history(mean_val_acc_history, std_val_acc_history, mean_test_acc_history, std_test_acc_history, title)
        
    mean_time, std_time = compute_properties(list_time)
    mean_best_acc, std_best_acc = compute_properties(list_best_acc)
    mean_acc_test, std_acc_test = compute_properties(list_acc_test)
    
    return mean_time, std_time, mean_best_acc, std_best_acc, mean_acc_test, std_acc_test
"""