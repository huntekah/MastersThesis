from sklearn.metrics import fbeta_score
from scipy.sparse import lil_matrix
from statistics import mean
#changes
class MeanMultiLabelFbeta():
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        self.y_true = args[0]
        self.y_pred = args[1]
        if (len(self.y_true) != len(self.y_pred)):
            raise IndexError(f"the predicted and expected arrays differ in length {len(self.y_true)}!={len(self.y_pred)}")
        return self.mean_multilabel_fbeta_score(**kwargs)

    def mean_multilabel_fbeta_score(self,**kwargs):
        beta = kwargs['beta']
        result = mean([self.multilabel_fbeta_score(yt,yp,beta) for yt,yp in zip(self.y_true,self.y_pred)])
        return result

    def multilabel_fbeta_score(self, y_true, y_pred, beta):
        tp = len(list(set(y_true).intersection(y_pred)))
        fn = len(y_true) - tp
        fp = len(y_pred) - tp
        if tp == 0 and fp == 0 and fn == 0:
            return 1.0
        return ((1 + beta**2) * tp) / ( ((1 + beta ** 2) * tp) + ( (beta**2) * fn ) + fp )