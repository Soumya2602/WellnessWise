import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.model_selection import train_test_split
import csv
import os
import sys


def prediction(user_symptoms, days):
    cwd = os.getcwd()
    training = pd.read_csv(f'{cwd}/medicineWeb/maindir/Data/Training.csv')
    cols = training.columns[:-1]
    x = training[cols]
    y = training['prognosis']
    le = LabelEncoder()
    y = le.fit_transform(y)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=42)
    clf = RandomForestClassifier().fit(x_train, y_train)
    symptoms_dict = {}
    severity_dict = {}
    description_dict = {}
    precautions_dict = {}

    for index, symptom in enumerate(x):
        symptoms_dict[symptom] = index

    with open(f'{cwd}/medicineWeb/maindir/Data/symptom_description.csv','r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            description = {row[0]: row[1]}
            description_dict.update(description)

    with open(f'{cwd}/medicineWeb/maindir/Data/symptom_severity.csv','r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        try:
            for row in csv_reader:
                severity_mapping = {row[0]: int(row[1])}
                severity_dict.update(severity_mapping)
        except:
            pass

    with open(f'{cwd}/medicineWeb/maindir/Data/symptom_precaution.csv','r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            prec = {row[0]: [row[1], row[2], row[3], row[4]]}
            precautions_dict.update(prec)
    input_vector = np.zeros(len(symptoms_dict))
    output = {}
    severity = 0
    advice = ''
    for item in user_symptoms:
        input_vector[[symptoms_dict[item]]] = 1
        severity += severity_dict[item]
        if ((severity * days) / (len(user_symptoms) + 1)) > 10:
            advice = "You should take the consultation from the doctor."
        else:
            advice = "The situation is not as bad as of now but you should take precautions. If symptoms still persist then you should go to the doctor."

    for i in list(le.inverse_transform(np.argsort(clf.predict_proba([input_vector])[0])[::-1])[:3]):
        output[i] = {}
        output[i]['desc'] = description_dict[i]
        output[i]['prec'] = precautions_dict[i]

    return advice, output