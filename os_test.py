import platform

print ("-- Lets run the prerequisite configuration tester --")

print(platform.mac_ver())

import torch
if torch.backends.mps.is_available():
    mps_device = torch.device("mps")
    x = torch.ones(1, device=mps_device)
    print (x)
else:
    print ("MPS device not found.")

print(torch.backends.mps.is_built())