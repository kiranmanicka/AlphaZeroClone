from MonteCarloTree import Node
import random


def upper_confidence_score(parent,training=False,c=.5):
    if training:
        return random.randrange(len(parent.children))
    else:
        return 0