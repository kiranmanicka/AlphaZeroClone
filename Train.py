from Model import optimizer,AlphaZeroLoss
from Dataset import Dataset as dataset


def train(model,epochs=5,batch_size=1000):
    d=dataset()
    inp,value,policy=d.query()
    for epoch in range(epochs):
        for i in range(0,len(inp),batch_size):
            if i+batch_size > len(inp):
                continue
            input_batch=inp[i:i+batch_size]
            value_batch,policy_batch=value[i:i+batch_size],policy[i:i+batch_size]
            policy_pred,value_pred=model(input_batch)
            loss=AlphaZeroLoss((value_pred,policy_pred),(value_batch.reshape(batch_size,1),policy_batch),model)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        inp,value,policy=d.query()
