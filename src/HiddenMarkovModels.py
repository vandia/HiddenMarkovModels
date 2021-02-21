import numpy as np
from hmmlearn import hmm
import pandas as pd


class BasketPlayerMM():

    def __init__(self):
        self.states = ['healthy', 'injured']  # --> healthy = 0, injured = 0
        self.observ_states = ['dribble', 'pass', 'shoot'] #dribble:0, pass:1, shoot:2
        self.transitions = [[0.7, 0.3], [0.5, 0.5]]  # --> stay/move to healthy -->0 stay/move to injured -->1
        self.observ_transitions = [[0.2, 0.1, 0.7], [0.3, 0.6, 0.1]]  # hidden states for healthy --> 0 for injured-->1
        self.trans_bin = []
        self.obsrv_trans_bin = []

        for i in self.transitions:
            self.trans_bin.append(self.__gen_bins__(i))

        for i in self.observ_transitions:
            self.obsrv_trans_bin.append(self.__gen_bins__(i))

    def __gen_bins__(self, prob):
        # generate an array monotonically increasing with the cumulative of the probabilities. Each of the bins
        # represent a margin. Those margins will be used to place a number, say x like bins[i-1] <= x < bins[i]
        bins = np.empty((0, len(prob)))
        cum = 0
        for i in range(len(prob)):
            cum += prob[i]
            bins = np.append(bins, cum)

        return bins

    def getRandomHiddenStates(self, n=100):
        st = (0 if np.random.random_sample() >= 0.5 else 1);
        res = np.array([[st]])
        for i in range(n - 1):
            rs = np.random.random_sample()
            st = np.digitize([rs], self.trans_bin[st])[0]
            res = np.append(res, [[st]], axis=0)
        return res

    def getRandomEmissions(self, hidden):

        emission = np.empty((0, 1), dtype=int)
        for i in hidden:
            st=i[0]
            rs = np.random.random_sample()
            emission = np.append(emission, [[np.digitize([rs], self.obsrv_trans_bin[st])[0]]], axis=0)
        return emission


def hidden_mm():
    b = BasketPlayerMM()
    hidden=b.getRandomHiddenStates(300)
    X = b.getRandomEmissions(hidden)
    remodel = hmm.MultinomialHMM(n_components=2, n_iter=100)
    remodel.fit(X)
    print(remodel.transmat_)
    print(remodel.emissionprob_)

    logprob,hidden_decoded=remodel.decode(X)
    df_confusion = pd.crosstab(pd.Series(hidden.flatten()),pd.Series(hidden_decoded), rownames=['Actual'], colnames=['Predicted'], margins=True)

    print(df_confusion)

    exactmodel=hmm.MultinomialHMM(n_components=2)
    exactmodel.fit(X)
    exactmodel.transmat_=[[0.7, 0.3], [0.5, 0.5]]
    exactmodel.emissionprob_=[[0.2, 0.1, 0.7], [0.3, 0.6, 0.1]]
    l,h=exactmodel.decode(X)
    df_confusion = pd.crosstab(pd.Series(hidden.flatten()),pd.Series(h), rownames=['Actual'], colnames=['Predicted'], margins=True)

    print(df_confusion)

if __name__ == '__main__':
    hidden_mm()
