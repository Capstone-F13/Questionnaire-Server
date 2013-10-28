from django.http import HttpResponse
from django.utils import simplejson
from provider.oauth2.models import AccessToken

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
                return HttpResponse(simplejson.dumps({ "error" : "answer/answed_id field is required!" }))

            # TODO: check if the answer already exists
            user_answer = UserAnswer(answer=answer_text, question=question, patient=patient)
            user_answer.save()

        except KeyError as e:
            return HttpResponse(simplejson.dumps({ "error" : "Malformed data!", "message" : e }))
        return HttpResponse(simplejson.dumps({ "success" : "Answer submission successful" }))

    else:
        return HttpResponse(simplejson.dumps({ "error" : "Request needs to post json" }))


def get_patients(request, token=None):
    """ return a list of patient id's based off a token that is generated for a user """

    if request.method == 'GET':
        if not token:
            return HttpResponse(simplejson.dumps({ "error" : "Request needs a token" }))
        access_token = AccessToken.objects.filter(token=token)
        if not access_token:
            return HttpResponse(simplejson.dumps({ "error" : "Access Token is not valid" }))
        user = access_token[0].user
        patients = Patient.objects.filter(administrators=user)

        patient_ids = []
        for patient in patients:
            patient_ids.append(patient.patient_id)

        return HttpResponse(simplejson.dumps({ "patient_ids" : patient_ids }), mimetype="application/json")
    else:
        return HttpResponse(simplejson.dumps({ "error" : "Expecting a GET request" }))


def login_patient(request):
    """ store an access token for a patient so that we can use the token for validation """
    if request.method == 'POST':
        json_data = simplejson.loads(request.body)
        try:
            patient_id = json_data['patient_id']
            access_token = json_data['access_token']
            if Patient.objects.filter(patient_id=patient_id).update(access_token=access_token) == 1:
                return HttpResponse(simplejson.dumps({ "success" : "Patient updated with access token" }))
            else:
                return HttpResponse(simplejson.dumps({ "error" : "Patient id does not exist!" }))
        except KeyError as e:
            return HttpResponse(simplejson.dumps({ "error" : "Malformed data!", "message" : e }))
    else:
        return HttpResponse(simplejson.dumps({ "error" : "Expecting a POST request" }))


def logout_patient(request):
    """ remove an access token for a patient, called once iOS app logs out """
    if request.method == 'DELETE':
        print 'made it'
        json_data = simplejson.loads(request.body)
        try:
            patient_id = json_data['patient_id']
            if Patient.objects.filter(patient_id=patient_id).update(access_token='') == 1:
                return HttpResponse(simplejson.dumps({ "success" : "Access token removed from patient" }))
            else:
                return HttpResponse(simplejson.dumps({ "error" : "Patient id does not exist!" }))
        except KeyError as e:
            return HttpResponse(simplejson.dumps({ "error" : "Malformed data!", "message" : e }))
    else:
        return HttpResponse(simplejson.dumps({ "error" : "Expecting a POST request" }))
