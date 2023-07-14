from Model import optimizer,AlphaZeroLoss
from Dataset import Dataset as dataset


def train(model,epochs=5,batch_size=1000):
    d=dataset()
    inp,value,policy=d.query()
    for epoch in range(epochs):
        #total_accuracy=0
        for i in range(0,len(inp),batch_size):
            print(i)
            if i+batch_size > len(inp):
                continue
            #print(i)
            input_batch=inp[i:i+batch_size]
            value_batch,policy_batch=value[i:i+batch_size],policy[i:i+batch_size]
            policy_pred,value_pred=model(input_batch)
            loss=AlphaZeroLoss((value_pred,policy_pred),(value_batch.reshape(batch_size,1),policy_batch),model)
            #print(value_batch.dtype,policy_pred.dtype,value_pred.dtype,policy_batch.dtype)
            #total_accuracy+=get_accuracy(y_batch,y_pred,batch_size)
            #print(get_accuracy(y_batch,y_pred))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            #print(loss)
        #validation_accuracy=get_accuracy(validation_y,model(validation_x))
        #print(f'Finished epoch {epoch}, latest loss {loss}, validation accuracy {validation_accuracy}')
        inp,value,policy=d.query()
