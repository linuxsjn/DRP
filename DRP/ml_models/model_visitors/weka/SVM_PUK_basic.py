from django.conf import settings
import uuid
from DRP.ml_models.model_visitors.weka.AbstractWekaModelVisitor import AbstractWekaModelVisitor
import os


class SVM_PUK_basic(AbstractWekaModelVisitor):

    maxResponseCount = 1

    def __init__(self, *args, **kwargs):
        super(SVM_PUK_basic, self).__init__(*args, **kwargs)

        self.PUK_OMEGA = 0.5
        self.PUK_SIGMA = 7.0

    def train(self, reactions, descriptorHeaders, filePath):
        arff_file = self._prepareArff(reactions, descriptorHeaders)

        # Currently, we support only one "response" variable.
        headers = [h for h in reactions.expandedCsvHeaders if h in descriptorHeaders]
        response_index = headers.index(list(self.statsModel.container.outcomeDescriptors)[0].csvHeader) + 1

        kernel = "\"weka.classifiers.functions.supportVector.Puk -O {} -S {}\"".format(self.PUK_OMEGA, self.PUK_SIGMA)
        command = "java weka.classifiers.functions.SMO -t {} -d {} -K {} -p 0 -c {}".format(arff_file, filePath, kernel, response_index)
        self._runWekaCommand(command)

    def wekaPredict(self, arff_file, model_file, response_index, results_path):
        command = "java weka.classifiers.functions.SMO -T {} -l {} -p 0 -c {} 1> {}".format(arff_file, model_file, response_index, results_path)
        self._runWekaCommand(command)
