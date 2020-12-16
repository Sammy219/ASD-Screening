from flask import Blueprint, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import pickle

site = Blueprint('site', __name__)
UPLOAD_FOLDER = 'app/uploads'


@site.route('/')
def index():
    return render_template('home.jinja')


@site.route('/test-page')
def test_page():
    return render_template('test-page.jinja')


@site.route('/about')
def about():
    return render_template('about.jinja')


@site.route('/questionare-test')
def questionare_test():
    return render_template('questionare-test.jinja')


@site.route('/image-test')
def image_test():
    return render_template('image-test.jinja')


@site.route('/result', methods=['POST'])
def result():
    form_data = request.form
    print(f"form: {form_data}")
    file = request.files
    print(f"file: {file}")
    print(f"form_data: {bool(form_data)}\nfile: {bool(file)}")
    if bool(form_data) and not bool(file):
        test_data = preprocess_data(form_data)
        print(f'test data = {test_data}')
        asd_model = pickle.load(open('asd_model/pkl_model.pkl', 'rb'))
        test_result = asd_model.predict([test_data])[0]
        print(f'ASD RESULT: {test_result}')

        return render_template('result.jinja', test_result=test_result)
    else:
        file = request.files["image"]
        upload_image_path = f"{UPLOAD_FOLDER}/{file.filename}"
        print(upload_image_path)
        file.save(upload_image_path)
        result = predict_image(upload_image_path)

        return render_template('result.jinja', test_result=result)


def preprocess_data(data):
    # order of input: questions 1-10, sex, eth, jnd, fam, ass, 24_36, 0_12
    test_data = []
    answers = [data[key] for key in data if key.startswith('q')]
    print(answers)
    for i in range(len(answers)):
        if i == len(answers) - 1:
            if answers[i] == '1' or answers[i] == '2' or answers[i] == '3':
                answers[i] = '1'
            else:
                answers[i] = '0'
        else:
            if answers[i] == '3' or answers[i] == '4' or answers[i] == '5':
                answers[i] = '1'
            else:
                answers[i] = '0'
    print(answers)
    test_data = [ans for ans in answers]
    # sex
    test_data.append(data['sex'])
    # ethnicity
    test_data.append(data['ethnicity'])
    # jaundice
    test_data.append(data['jaundice'])
    # family with asd
    test_data.append(data['family_mem_with_asd'])
    # assigner
    test_data.append(data['assigner'])
    # within 24_36
    test_data.append('1' if data['age'] == '2' else '0')
    # within 0_12
    test_data.append('1' if data['age'] == '0' else '0')

    return test_data


def predict_image(path_to_image):
    model = load_model('ASD_Model/densenet_87.h5')
    image = load_img(path_to_image, target_size=(224, 224))
    img_array = img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)
    pred = model.predict(img_array)
    result = pred[0]
    print(f"Image prediction: {result}")
    answer = np.argmax(result)
    print(f"Answer: {answer}")
    return answer

