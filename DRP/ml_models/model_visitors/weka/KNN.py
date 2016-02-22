from django.conf import settings
import uuid
from DRP.ml_models.model_visitors.weka.AbstractWekaModelVisitor import AbstractWekaModelVisitor
import os


class KNN(AbstractWekaModelVisitor):

    maxResponseCount = 1

    def __init__(self, *args, **kwargs):
        super(KNN, self).__init__(*args, **kwargs)


    def wekaTrain(self, arff_file, filePath, response_index):
        command = "java weka.classifiers.lazy.IBk -t {} -d {} -p 0 -c {}".format(arff_file, filePath, response_index)
        self._runWekaCommand(command)

    def wekaPredict(self, arff_file, model_file, response_index, results_path):
        command = "java weka.classifiers.lazy.IBk -T {} -l {} -p 0 -c {} 1> {}".format(arff_file, model_file, response_index, results_path)
        self._runWekaCommand(command)
