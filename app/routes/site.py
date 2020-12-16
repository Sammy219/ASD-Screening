from flask import Blueprint, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import pickle

site = Blueprint('site', __name__)
UPLOAD_FOLDER = 'app/uploads'
QUESTIONS = [
    [{'id': 'q1', 'txt': 'Apakah anak Anda melihat Anda saat Anda memanggil namanya?'},
     {'id': 'q1a1', 'txt': 'Selalu'},
     {'id': 'q1a2', 'txt': 'Biasanya'},
     {'id': 'q1a3', 'txt': 'Kadang-kadang'},
     {'id': 'q1a4', 'txt': 'Jarang'},
     {'id': 'q1a5', 'txt': 'Tidak pernah'}],
    [{'id': 'q2', 'txt': 'Seberapa mudah Anda melakukan kontak mata dengan anak Anda?'},
     {'id': 'q2a1', 'txt': 'Sangat mudah'},
     {'id': 'q2a2', 'txt': 'Cukup mudah'},
     {'id': 'q2a3', 'txt': 'Cukup sulit'},
     {'id': 'q2a4', 'txt': 'Sangat sulit'},
     {'id': 'q2a5', 'txt': 'Tidak mungkin'}],
    [{'id': 'q3', 'txt': 'Seberapa sering anak Anda menunjuk untuk menunjukkan bahwa dia menginginkan sesuatu? (mis. '
                         'mainan yang di luar jangkauan)'},
     {'id': 'q3a1', 'txt': 'Berkali-kali sehari'},
     {'id': 'q3a2', 'txt': 'Beberapa kali sehari'},
     {'id': 'q3a3', 'txt': 'Beberapa kali seminggu'},
     {'id': 'q3a4', 'txt': 'Kurang dari sekali seminggu'},
     {'id': 'q3a5', 'txt': 'Tidak pernah'}],
    [{'id': 'q4', 'txt': 'Apakah anak Anda menunjukkan minat yang sama dengan Anda? (mis. menunjuk pemandangan yang '
                         'menarik)'},
     {'id': 'q4a1', 'txt': 'Berkali-kali sehari'},
     {'id': 'q4a2', 'txt': 'Beberapa kali sehari'},
     {'id': 'q4a3', 'txt': 'Beberapa kali seminggu'},
     {'id': 'q4a4', 'txt': 'Kurang dari sekali seminggu'},
     {'id': 'q4a5', 'txt': 'Tidak pernah'}],
    [{'id': 'q5', 'txt': 'Apakah anak Anda berpura-pura? (misalnya merawat boneka, berbicara di telepon mainan)'},
     {'id': 'q5a1', 'txt': 'Berkali-kali sehari'},
     {'id': 'q5a2', 'txt': 'Beberapa kali sehari'},
     {'id': 'q5a3', 'txt': 'Beberapa kali seminggu'},
     {'id': 'q5a4', 'txt': 'Kurang dari sekali seminggu'},
     {'id': 'q5a5', 'txt': 'Tidak pernah'}],
    [{'id': 'q6', 'txt': 'Apakah anak Anda mengikuti apa yang Anda lihat?'},
     {'id': 'q6a1', 'txt': 'Berkali-kali sehari'},
     {'id': 'q6a2', 'txt': 'Beberapa kali sehari'},
     {'id': 'q6a3', 'txt': 'Beberapa kali seminggu'},
     {'id': 'q6a4', 'txt': 'Kurang dari sekali seminggu'},
     {'id': 'q6a5', 'txt': 'Tidak pernah'}],
    [{'id': 'q7', 'txt': 'Jika Anda atau orang lain dalam keluarga terlihat kesal, apakah anak Anda menunjukkan '
                         'tanda-tanda ingin menghibur mereka? (misalnya membelai rambut, memeluknya)'},
     {'id': 'q7a1', 'txt': 'Selalu'},
     {'id': 'q7a2', 'txt': 'Biasanya'},
     {'id': 'q7a3', 'txt': 'Kadang-kadang'},
     {'id': 'q7a4', 'txt': 'Jarang'},
     {'id': 'q7a5', 'txt': 'Tidak pernah'}],
    [{'id': 'q8', 'txt': 'Maukah Anda menjelaskan kata-kata pertama anak Anda sebagai'},
     {'id': 'q8a1', 'txt': 'Sangat khas'},
     {'id': 'q8a2', 'txt': 'Cukup khas'},
     {'id': 'q8a3', 'txt': 'Sedikit tidak biasa'},
     {'id': 'q8a4', 'txt': 'Sangat tidak biasa'},
     {'id': 'q8a5', 'txt': 'Anak saya tidak berbicara'}],
    [{'id': 'q9', 'txt': 'Apakah anak Anda menggunakan gerakan sederhana? (mis. melambaikan tangan)'},
     {'id': 'q9a1', 'txt': 'Berkali-kali sehari'},
     {'id': 'q9a2', 'txt': 'Beberapa kali sehari'},
     {'id': 'q9a3', 'txt': 'Beberapa kali seminggu'},
     {'id': 'q9a4', 'txt': 'Kurang dari sekali seminggu'},
     {'id': 'q9a5', 'txt': 'Tidak pernah'}],
    [{'id': 'q10', 'txt': 'Apakah anak Anda tidak menatap apa pun (melamun) tanpa ada tujuan yang jelas?'},
     {'id': 'q10a1', 'txt': 'Berkali-kali sehari'},
     {'id': 'q10a2', 'txt': 'Beberapa kali sehari'},
     {'id': 'q10a3', 'txt': 'Beberapa kali seminggu'},
     {'id': 'q10a4', 'txt': 'Kurang dari sekali seminggu'},
     {'id': 'q10a5', 'txt': 'Tidak pernah'}],
]


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
    return render_template('questionare-test.jinja', questions=QUESTIONS)


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
        prob = asd_model.predict_proba([test_data])
        class_pred = np.argmax(prob)
        print(f"PROBABILITY: {prob}")

        return render_template('result.jinja', class_pred=class_pred, confidence=prob[class_pred]*100)
    else:
        file = request.files["image"]
        upload_image_path = f"{UPLOAD_FOLDER}/{file.filename}"
        print(upload_image_path)
        file.save(upload_image_path)
        class_pred, conf = predict_image(upload_image_path)

        return render_template('result.jinja', class_pred=class_pred, confidence=conf*100)


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
    model = load_model('ASD_Model/Mobilenet-90.66.h5')
    image = load_img(path_to_image, target_size=(224, 224))
    img_array = img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)
    pred = model.predict(img_array)
    result = pred[0]
    print(f"Image prediction: {result}")
    answer = np.argmax(result)
    print(f"Answer: {answer}")
    return answer, result[answer]

