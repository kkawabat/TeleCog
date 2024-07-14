from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.voice_response import VoiceResponse, Gather

from telecog_main.models import Assessment


# https://stackoverflow.com/a/72009181/4231985
@csrf_exempt
def greetings(request):
    resp = VoiceResponse()

    gather = Gather(num_digits=1, action='assessment1')
    gather.say("Welcome to Linus Telephone cognition screening, if you are interested in taking our 1 minute cognitive assessment on the phone please press 1.")
    resp.append(gather)
    return HttpResponse(str(resp))


@csrf_exempt
def assessment1(request):
    resp = VoiceResponse()

    choice = 2
    if 'Digits' in request.POST:
        choice = request.POST['Digits']

    if choice == '1':
        call_sid = request.POST['CallSid']
        print(call_sid)
        Assessment(call_sid=call_sid).save()

        resp.say("Great! Please note that the call will be recorded in order to assess your responses. "
                 "We will begin this assessment with an object naming test, "
                 "after the beep please name as many object as you can think of that starts with the letter, B.")
        resp.record(action='assessment2', method='POST', timeout=30, maxLength=30,
                    transcribe=True, transcribeCallback='analyze_object_naming', playBeep=True)
        resp.say("Great you have finished the assessment!")
    else:
        resp.say("To learn more information about our screening please visit us at our website linus dot health, thank you.")

    return HttpResponse(str(resp))


@csrf_exempt
def analyze_object_naming(request):
    ass = Assessment.objects.get(call_sid=request.POST['CallSid'])
    text = request.POST['TranscriptionText']
    print(text)
    ass.object_naming_result = len([t for t in text.split() if t.lower().startswith('b')])
    ass.object_naming_transcript = text
    ass.save()
    return HttpResponse(status=200)


@csrf_exempt
def assessment2(request):
    resp = VoiceResponse()

    ass = Assessment.objects.get(call_sid=request.POST['CallSid'])
    if ass.object_naming_result is None:

        resp.say("Please wait a moment while we process your responses, this might take a moment")
        resp.pause(length=5)
        resp.redirect('assessment2')
    else:

        resp.say(f"Your results are in you scored {ass.object_naming_result} on the object naming test.")
        if ass.object_naming_result < 5:
            resp.say(f"Your results indicate that you might have a slight cognitive impairment.")
        else:
            resp.say(f"Your results indicate that you have a normal cognitive functions.")
        resp.say("To learn more about what you can do with your cognitive health please visit us at our website Linus dot health")
    return HttpResponse(str(resp))
