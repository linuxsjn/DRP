python -u build_model.py -p @descs/full.dsc -trs geoffrey_split_for_thesis_0 -tes geoffrey_split_for_thesis_1 -v -mt SVM_PUK_basic -d "geoffrey thesis SVM all descriptors no examplepy, no feature selection" &> SVM_basic_thesis_noexamplepy.out &
python -u build_model.py -p @descs/full.dsc -trs geoffrey_split_for_thesis_0 -tes geoffrey_split_for_thesis_1 -v -mt SVM_PUK_BCR -d "geoffrey thesis BCR SVM all descriptors no examplepy, no feature selection" &> SVM_BCR_thesis_noexamplepy.out &
python -u build_model.py -p @descs/full.dsc -trs geoffrey_split_for_thesis_0 -tes geoffrey_split_for_thesis_1 -v -mt KNN -d "geoffrey thesis BCR SVM all descriptors no examplepy, no feature selection" &> KNN_thesis_noexamplepy.out &
python -u build_model.py -p @descs/full.dsc -trs geoffrey_split_for_thesis_0 -tes geoffrey_split_for_thesis_1 -v -mt J48 -d "geoffrey thesis BCR SVM all descriptors no examplepy, no feature selection" &> J48_thesis_noexamplepy.out &
python -u build_model.py -p @descs/full.dsc -trs geoffrey_split_for_thesis_0 -tes geoffrey_split_for_thesis_1 -v -mt NaiveBayes -d "geoffrey thesis BCR SVM all descriptors no examplepy, no feature selection" &> NB_thesis_noexamplepy.out &
