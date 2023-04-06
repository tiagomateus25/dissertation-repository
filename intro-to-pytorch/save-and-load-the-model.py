#!/usr/bin/env python3
import torch
import torchvision.models as models

# saving and loading model weights ----------------------------------------------------------------
# saving
model = models.vgg16(pretrained=True)
torch.save(model.state_dict(), 'model_weights.pth')
# loading
model = models.vgg16() # we do not specify pretrained=True, i.e. do not load default weights
model.load_state_dict(torch.load('model_weights.pth'))
model.eval()

# saving and loading models with shapes ---------------------------------------------------------------------
# saving
torch.save(model, 'model.pth')
# loading
model = torch.load('model.pth')