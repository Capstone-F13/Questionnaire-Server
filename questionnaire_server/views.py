from django.http import HttpResponse
from django.utils import simplejson

from questionnaire_server.models import MultipleChoiceAnswer, Patient, Question, UserAnswer

def submit_answer(request):
    if request.method == 'POST':
        json_data = simplejson.loads(request.body)
        try:
            question_id = json_data['question_id']
            question = Question.objects.get(pk=question_id)
            patient_id = json_data['patient_id']
            patient =  Patient.objects.get(patient_id=patient_id)
            answer_text = None

            if 'answer' in json_data:
                answer_text = json_data['answer']
            elif 'answer_id' in json_data:
                answer_id = json_data['answer_id']
                answer_text = MultipleChoiceAnswer.objects.get(pk=answer_id)

            if not answer_text:
                return HttpResponse(simplejson.dumps({ "error" : "answer/answed_id field is required!" }))

            # TODO: check if the answer already exists 
            user_answer = UserAnswer(answer=answer_text, question=question, patient=patient)
            user_answer.save()

        except KeyError as e:
            return HttpResponse(simplejson.dumps({ "error" : "Malformed data!", "message" : e }))
        return HttpResponse(simplejson.dumps({ "success" : "Got json data" }))

    else:
        return HttpResponse(simplejson.dumps({ "error" : "Request needs to post json" }))
