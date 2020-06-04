import fasttext

PRE_TRAINED_MODEL = fasttext.load_model("./language_detection_models/models/all_languages_model.bin")
CUSTOM_MODEL = fasttext.load_model("./language_detection_models/models/custom_model.bin")
CUSTOM_MODEL_THRESHOLD = 0.6
PRE_TRAINED_MODEL_THRESHOLD = 0.75


def get_language_from_label(label):
    """
    This helper function will return language name from provided label['english', 'roman-urdu'].

    :param label: Predicted label of model
    :return: Name of Language
    """
    english_labels = ['__label__eng', '__label__en']
    roman_urdu_labels = ['__label__rurdu']
    if label in english_labels:
        return "english"
    elif label in roman_urdu_labels:
        return "roman-urdu"
    return "Error in parsing label: {}".format(label)


def get_language(message, custom_model_threshold=CUSTOM_MODEL_THRESHOLD,
                 pretrained_model_threshold=PRE_TRAINED_MODEL_THRESHOLD, debug=False):
    """
    Predict language using ensemble of fastText pre-trained model and custom_model(for roman-urdu & english).

    Decision Criteria:
        english:   pre-trained model predict english, given pre-trained(P) > pretrained_model_threshold
        englisg/roman:   predictions by custom_model,
                        given pre-trained(P) < pretrained_model_threshold & custom_model(P) > custom_model_threshold
        'None':   if none of above matches.

    :param message: Candidate string for classification
    :param custom_model_threshold: Custom_model will be judged on this threshold
    :param pretrained_model_threshold: Pre-trained model will be judged on this threshold
    :param debug: Will return scores with predicted language if True
    :return: Identified Language
    """
    result = PRE_TRAINED_MODEL.predict(message)
    language, score = get_language_from_label(result[0][0]), result[1][0]
    if score >= pretrained_model_threshold:
        if debug:
            return language, score
        return language
    else:
        result = CUSTOM_MODEL.predict(message)
        language, score = get_language_from_label(result[0][0]), result[1][0]
        if debug:
            return language, score

        if score >= custom_model_threshold:
            return language
    print("Low confidence for language detection: message:{}, result: {}".format(message, (language, score)))
    return None


def test_fasttext_model(test_data, model, threshold):
    """
    Test any fasttext model with custom test set confidence threshold.

    :param test_data: list of sentence of format(<label> <sentence>)
                    e.g. '__label__eng how are you doing today?'
    :param model: FastText model
    :param threshold: results with confidence above this threhsold will be considered valid. [Default: 0.6]
    :return: True_Positives, False_Positives, Accuracy_of_Prediction
    """
    labels = [line.split(" ")[0] for line in test_data if "__label" in line]
    test = [" ".join(line.split(" ")[1:]) for line in test_data if "__label" in line]
    true_positives, false_positives = [], []
    for index, line in enumerate(test):
        result = model.predict(line)
        if result[1][0] > threshold and get_language_from_label(result[0][0]) == get_language_from_label(labels[index]):
            true_positives.append((line, result[0][0], result[1][0]))
        else:
            false_positives.append((line, result[0][0], result[1][0]))
    accuracy = len(true_positives) / (len(true_positives) + len(false_positives)) * 100
    return true_positives, false_positives, accuracy


def test_combined_pipeline(test_data, threshold):
    """
        Test custom pipeline for prediction using ensemble of fastText pre-trained model and
        custom_model(for roman-urdu & english). Reference function: 'get_language'

    :param test_data: List of sentence of format(<label> <sentence>)
                    e.g. '__label__eng how are you doing today?'
    :param threshold: Results with confidence above this threhsold will be considered valid. Default: 0.6
    :return: True_Positives, False_Positives, Accuracy_of_Prediction
    """
    labels = [line.split(" ")[0] for line in test_data if "__label" in line]
    test = [" ".join(line.split(" ")[1:]) for line in test_data if "__label" in line]
    true_positives, false_positives = [], []
    for index, line in enumerate(test):
        result, score = get_language(line, custom_model_threshold=threshold, debug=True)
        if result and result == get_language_from_label(labels[index]):
            true_positives.append((line, result, score))
        else:
            false_positives.append((line, result, score))
    accuracy = len(true_positives) / (len(true_positives) + len(false_positives)) * 100
    return true_positives, false_positives, accuracy


def train_custom_model(path_to_training_file):
    """
        Will train a fasttext supervised text classification model for language detection. Labeled should folow the
        format: '__label__eng how are you doing today'
                '__label__rurdu ap kesy hain ap'

    :param path_to_training_file: Complete path to file conatining training data
    :return: fasttext model instance
    """
    return fasttext.train_supervised(path_to_training_file)
