from flask import Blueprint, render_template, request
import pickle


site = Blueprint('site', __name__)


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


@site.route('/result', methods=['POST'])
def result():
    data = request.form
    test_data = preprocess_data(data)
    print(f'test data = {test_data}')
    asd_model = pickle.load(open('ASD_Model/pkl_model.pkl', 'rb'))
    test_result = asd_model.predict([test_data])[0]
    print(f'ASD RESULT: {test_result}')

    return render_template('result.jinja', test_result=test_result)


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
    # sex = male
    test_data.append('1')
    # eth = asian
    test_data.append('6')
    # jaundice = no
    test_data.append('0')
    # family with asd = no
    test_data.append('0')
    # assigner = family member
    test_data.append('0')
    # within 24_36 = yes
    test_data.append('1')
    # within 0_12 = no
    test_data.append('0')

    return test_data
