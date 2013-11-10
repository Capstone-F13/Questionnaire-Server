from django.core import serializers
from django.http import HttpResponse
from django.utils import simplejson
from provider.oauth2.models import AccessToken
from django.contrib.auth.models import User

from questionnaire_server.models import MultipleChoiceAnswer, Patient, Question, UserAnswer

def submit_answer(request):
    if request.method == 'POST':
        json_data = simplejson.loads(request.body)
        try:
            question_id = json_data['question_id']
            # TODO: may be good to ensure the question exists
            question = Question.objects.get(pk=question_id)
            patient_id = json_data['patient_id']
            # TODO: may be good to ensure the patient exists
            patient =  Patient.objects.get(patient_id=patient_id)
            answer_text = None

            if 'answer' in json_data:
                answer_text = json_data['answer']
            elif 'answer_id' in json_data:
                answer_id = json_data['answer_id']
                # TODO: may be good to ensure the answer exists
                answer_text = MultipleChoiceAnswer.objects.get(pk=answer_id)

            if not answer_text:
                return _generate_response({ "error" : "answer/answer_id field is required!" })

            # TODO: check if the answer already exists
            user_answer = UserAnswer(answer=answer_text, question=question, patient=patient)
            user_answer.save()

        except KeyError as e:
            return _generate_response({ "error" : "Malformed data!", "message" : e })
        return _generate_response({ "success" : "Answer submission successful" })

    else:
        return _generate_response({ "error" : "Request needs to post json" })


def get_patients(request, token=None):
    """ return a list of patient id's based off a token that is generated for a user """

    if request.method == 'GET':
        if not token:
            return _generate_response({ "error" : "Request needs a token" })
        access_token = AccessToken.objects.filter(token=token)
        if not access_token:
            return _generate_response({ "error" : "Access Token is not valid" })
        user = access_token[0].user
        patients = Patient.objects.filter(administrators=user)

        patient_ids = []
        for patient in patients:
            patient_ids.append(patient.patient_id)

        return _generate_response({ "patient_ids" : patient_ids })
    else:
        return _generate_response({ "error" : "Expecting a GET request" })


def login_patient(request):
    """ store an access token for a patient so that we can use the token for validation """
    if request.method == 'POST':
        json_data = simplejson.loads(request.body)
        try:
            patient_id = json_data['patient_id']
            access_token = json_data['access_token']
            if Patient.objects.filter(patient_id=patient_id).update(access_token=access_token) == 1:
                return _generate_response({ "success" : "Patient updated with access token" })
            else:
                return _generate_response({ "error" : "Patient id does not exist!" })
        except KeyError as e:
            return _generate_response({ "error" : "Malformed data!", "message" : e })
    else:
        return _generate_response({ "error" : "Expecting a POST request" })


def logout_patient(request):
    """ remove an access token for a patient, called once iOS app logs out """
    if request.method == 'POST':
        json_data = simplejson.loads(request.body)
        try:
            patient_id = json_data['patient_id']
            if Patient.objects.filter(patient_id=patient_id).update(access_token='') == 1:
                return _generate_response({ "success" : "Access token removed from patient" })
            else:
                return _generate_response({ "error" : "Patient id does not exist!" })
        except KeyError as e:
            return _generate_response({ "error" : "Malformed data!", "message" : e })
    else:
        return _generate_response({ "error" : "Expecting a POST request" })


def create_patient(request):
    """ create a patient and store an access token for the patient """
    if request.method == 'POST':
        json_data = simplejson.loads(request.body)
        try:
            patient_id = json_data['patient_id']
            access_token = json_data['access_token']
            if Patient.objects.filter(patient_id=patient_id).update(access_token=access_token) == 1:
                return _generate_response({ "success" : "Patient already exists. Updated with access token" })
            else:
                administrator_id = AccessToken.objects.filter(token=access_token)[0].user.id
                patient = Patient(patient_id=patient_id, access_token=access_token)
                patient.save()
                patient.administrators.add(administrator_id)
                return _generate_response({ "success" : "Patient created with access token" })
        except KeyError as e:
            return _generate_response({ "error" : "Malformed data!", "message" : e })
    else:
        return _generate_response({ "error" : "Expecting a POST request" })


def get_questions(request, access_token=None, patient_id=None):
    """ get a list of questions for a patient """
    if request.method == 'GET':
        patient = Patient.objects.filter(patient_id=patient_id)

        if not patient:
            return _generate_response({ "error" : "Patient id not found" })
        else:
            patient = patient[0]

        if not patient.access_token:
            return_generate_response({ "error" : "Access token not set for patient" })
        if patient.access_token != access_token:
            return _generate_response({ "error" : "Access token not valid for patient" })

        # TODO: get the correct survey here
        questions = Question.objects.all()
        data = serializers.serialize('json', questions, indent=2, relations=('multiple_choice_answer',))
        return HttpResponse(data, mimetype='application/json')
    else:
        return _generate_response({ "error" : "Expecting a GET request" })

def _generate_response(data):
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')
