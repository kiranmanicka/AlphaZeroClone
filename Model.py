import torch
import torch.nn as nn
from torchsummary import summary


class AlphaZeroNetwork(nn.Module):
    def __init__(self,num_res_blocks,num_input_channels,num_intermediate_channels=256):
        super().__init__()
        self.conv_layer=ConvolutionalLayer(num_input_channels,num_intermediate_channels)
        self.res_blocks=[]
        for r in range(num_res_blocks):
            self.res_blocks.append(ResidualBlock(num_intermediate_channels))
        self.value_head=ValueHead(num_intermediate_channels)
        self.policy_head=PolicyHead(num_intermediate_channels,73)


    def forward(self,x):
        x=self.conv_layer(x)
        for r in self.res_blocks:
            x=r(x)
        policy=self.policy_head(x)
        value=self.value_head(x)
        return policy,value


class ResidualBlock(nn.Module):
    def __init__(self,in_channels):
        super().__init__()
        self.relu=nn.ReLU()


        self.conv1=nn.Conv2d(in_channels,in_channels,kernel_size=3,padding=1)
        self.batchnorm1=nn.BatchNorm2d(in_channels)


        self.conv2=nn.Conv2d(in_channels,in_channels,kernel_size=3,padding=1)
        self.batchnorm2=nn.BatchNorm2d(in_channels)

    def forward(self,x):
        y=self.conv1(x)
        y=self.batchnorm1(y)
        y=self.relu(y)
        y=self.conv2(y)
        y=self.batchnorm2(y)
        y=self.relu(y+x)
        return y


class ConvolutionalLayer(nn.Module):
    def __init__(self,in_channels,out_channels):
        super().__init__()
        self.conv1=nn.Conv2d(in_channels,out_channels,kernel_size=3,padding=1)
        self.batchnorm1=nn.BatchNorm2d(out_channels)
        self.relu1=nn.ReLU()

    def forward(self,x):
        x=self.conv1(x)
        x=self.batchnorm1(x)
        x=self.relu1(x)
        return x

class ValueHead(nn.Module):
    def __init__(self,in_channels):
        super().__init__()
        self.one_by_one=nn.Conv2d(in_channels,1,kernel_size=1)
        self.batchnorm1=nn.BatchNorm2d(1)
        self.relu=nn.ReLU()

        self.flatten=nn.Flatten(start_dim=1)

        self.lin1=nn.Linear(64,in_channels,bias=True)
        #relu
        self.lin2=nn.Linear(in_channels,1,bias=True)

        self.tanh=nn.Tanh()


    def forward(self,x):
        x=self.one_by_one(x)
        x=self.batchnorm1(x)
        x=self.relu(x)

        x=self.flatten(x)

        x=self.lin1(x)
        x=self.relu(x)
        x=self.lin2(x)

        return self.tanh(x)


class PolicyHead(nn.Module):
    def __init__(self,in_channels,out_channels):
        super().__init__()
        self.one_by_one=nn.Conv2d(in_channels,in_channels,kernel_size=1)
        self.relu=nn.ReLU()

        self.one_by_one2=nn.Conv2d(in_channels,out_channels,kernel_size=1,bias=True)
        self.softmax=nn.Softmax(dim=1)

        self.flatten=nn.Flatten(start_dim=1)
        


    def forward(self,x):
        x=self.one_by_one(x)
        x=self.relu(x)

        x=self.one_by_one2(x)
        x=self.flatten(x)
        x=self.softmax(x)
        return x.view(-1,73,8,8)

model=AlphaZeroNetwork(10,16)



#print(summary(model,(1,16,8,8)))