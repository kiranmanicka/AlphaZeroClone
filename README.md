# AlphaZeroClone
Implementation of the AlphaZero Model made by Google DeepMind. Utilizes a Neural Network with 10 residual blocks and 2 heads for value and policy.
The agent plays through a Monte Carlo Tree

Users can train their own Alpha Zero models, save them to disk, and compete these models against eachother.

python play.py create, will initiate the training sequence which consists of the agent playing multiple games against itself on several different processes
and then training the neural network. The model will then be saved to an ouput file called model<version_number>.pth

python play.py play will take an already save model instance and further train it. The output will be save to file called model<version_number>.pth

python play.py compete will take two saved model instances and play them against eachother and specified number of times and return the results.
