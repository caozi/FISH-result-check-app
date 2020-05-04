from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse,HttpResponseRedirect
from wechatpy import parse_message,create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import WeChatClient
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from wechatpy.oauth import WeChatOAuth
from .models import Patient, Doctors, Member
from .weixin_config import TOKEN, appID, appsecret, template_ID
from django.http import JsonResponse


redirect_uri = "https://georgecaozi.pythonanywhere.com/weixin/register_form_after_oath"
redirect_uri_patient = "https://georgecaozi.pythonanywhere.com/weixin/patient_query"
redirect_uri_member = "https://georgecaozi.pythonanywhere.com/weixin/login_with_oath"
oauthClient = WeChatOAuth(app_id=appID, secret=appsecret, redirect_uri=redirect_uri)
oauthClient_member = WeChatOAuth(app_id=appID, secret=appsecret, redirect_uri=redirect_uri_member)
oauthClient_patient = WeChatOAuth(app_id=appID, secret=appsecret, redirect_uri=redirect_uri_patient)
client = WeChatClient(appID, appsecret)



@csrf_exempt
def index(request):
    if request.method == 'GET':      
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echostr = request.GET.get('echostr', '')
        try:
            check_signature(TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            echostr = 'error'
        response = HttpResponse(echostr, content_type="text/plain")
        return response
    elif request.method == 'POST':
        reply = None
        msg = parse_message(request.body)
        if msg.type == 'text':
            reply = create_reply('感谢关注病理科微信公众号测试号，病理结果会第一时间推送，请密切关注', msg)
        elif msg.event == 'subscribe':
            reply = create_reply('感谢关注病理科微信公众号测试号，点击登记菜单，填写病人信息，系统会第一时间推送病理报告状态，请密切关注', msg)
        response = HttpResponse(reply.render(), content_type='application/xml')
        return response
    else:
        return HttpResponse('ERROR')


def create_menu(request):
    client.menu.create({
        "button": [
            {"type": "view", "name": "登记", "url": "http://georgecaozi.pythonanywhere.com/weixin/register_form/"},
            {"type": "view", "name": "查询", "url": "http://georgecaozi.pythonanywhere.com/weixin/query_form"},
            {"type": "view", "name": "登录", "url": "http://georgecaozi.pythonanywhere.com/weixin/login_form"}
            ]
        }
            )
    return HttpResponse('ok')


def get_openid(request):
    return HttpResponseRedirect(oauthClient.authorize_url)


def register_form(request):
    if request.method == 'GET':
        code = request.GET['code']
        res = oauthClient.fetch_access_token(code=code)
        params = {'openid': res['openid']}
    else:
        params = {'openid': 'error'}
    return render_to_response('weixin/register_form.html', params)


def query_form(request):
    registered = request.session.get('registered', False)
    if registered:
        open_ID = request.session['openID']
        p = Patient.objects.get(patient_openID=open_ID)
        return render(request, 'weixin/query_result.html', {'patient': p})
    else:
        return render_to_response('weixin/query_error.html')
    

@csrf_exempt
def register(request):
    if request.method == "POST":
        p_id = request.POST.get('patient_id_first', '')
        p_name = request.POST.get('patient_name', '')
        p_openID = request.POST.get('patient_openID', '')
        p_status = "正在处理中"
        p = Patient(patient_id=p_id,
                    patient_name=p_name,
                    patient_openID=p_openID,
                    patient_status=p_status
                )
        p.save()
        request.session['registered'] = True
        request.session['openID'] = p_openID
        send_message(template_ID, p)
        return HttpResponseRedirect('register_success/')
    return HttpResponse('Data not received', content_type="text/plain")


@csrf_exempt
def query(request):
    if request.method == "POST":
        p_id = request.POST.get("patient_id", '')
        p = Patient.objects.get(patient_id=p_id)
        return render(request, 'weixin/query_result.html', {'patient': p})


def register_success(request):
    return render_to_response('weixin/register_success.html')


def login_form(request):
    authorized = request.session.get('authorized', False)
    if authorized:
        patients_not_informed = Patient.objects.exclude(patient_status='请来报告中心取病理报告')
        return render(request, 'weixin/admin_patients_not_informed.html', {'patients_not_informed': patients_not_informed})
    else:
        return HttpResponseRedirect(oauthClient_member.authorize_url)


@csrf_exempt
def login(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name', '')
        user_password = request.POST.get('user_password', '')
        user = Doctors.objects.get(doctor_name=user_name)
        if user.doctor_password == user_password:
            patients_not_informed = Patient.objects.exclude(patient_status='请来报告中心取病理报告')
            return render(request, 'weixin/admin_patients_not_informed.html', {'patients_not_informed': patients_not_informed})
        else:
            return render_to_response('weixin/login_error.html')
    return HttpResponse('Data not received', content_type="text/plain")


@csrf_exempt
def admin_query(request):
    if request.method == 'POST':
        p_id = request.POST.get('patient_id', '')
        try:
            p = Patient.objects.get(patient_id = p_id)
            return render(request, 'weixin/admin_query_result.html', {'patient': p})
        except Patient.DoesNotExist:
            return render_to_response('weixin/query_error.html')
    return HttpResponse('Data not received', content_type="text/plain")


def send_message(template_ID, patient):
    data = {
          'patient_id': {'value': patient.patient_id},
          'patient_name': {'value': patient.patient_name},
          'patient_status': {'value': patient.patient_status, 'color': '#B22222'}
        }
    client.message.send_template(patient.patient_openID, template_ID, data)



@csrf_exempt
def admin_query_override(request):
    if request.method == "POST":                                                                                                                
        p_id = request.POST.get('patient_id', '')
        p_name = request.POST.get('patient_name', '')
        p_openID = request.POST.get('patient_openID', '')
        p_status = request.POST.get('patient_status', '')
        p = Patient.objects.get(patient_id=p_id)
        p.delete()
        p = Patient(patient_id=p_id,
                    patient_name=p_name,
                    patient_openID=p_openID,
                    patient_status=p_status
             )
        p.save()
        send_message(template_ID, p)
        return render_to_response('weixin/admin_query_success.html')
    return HttpResponse('Data not received', content_type="text/plain")


def check_patient_ID_exist(request):
    p_id = request.GET.get('patient_id', None)
    try:
        _ = Patient.objects.get(patient_id=p_id)
    except Patient.DoesNotExist:
        data = {}
    else:
        data = {'exist': True}
    return JsonResponse(data)


def check_user_name(request):
    user_name = request.GET.get('user_name', None)
    try:
        _ = Doctors.objects.get(doctor_name=user_name)
    except:
        data = {}
    else:
        data = {'exist': True}
    return JsonResponse(data)


def back_to_admin_query(request):
    patients_not_informed = Patient.objects.exclude(patient_status='请来报告中心取病理报告')
    return render(request, 'weixin/admin_patients_not_informed.html', {'patients_not_informed': patients_not_informed})


def login_with_oath(request):
    code = request.GET['code']
    res = oauthClient_member.fetch_access_token(code=code)
    try:
        _ = Member.objects.get(member_openID=res['openid'])
        request.session['authorized'] = True
        patients_not_informed = Patient.objects.exclude(patient_status='请来报告中心取病理报告')
        return render(request, 'weixin/admin_patients_not_informed.html', {'patients_not_informed': patients_not_informed})
    except:
        return render_to_response('weixin/login_error.html')


def patient_query(request):
    code = request.GET['code']
    res = oauthClient_member.fetch_access_token(code=code)
    try:
        p = Patient.objects.get(patient_openID=res['openid'])
        return render(request, 'weixin/query_result.html', {'patient': p})
    except:
        return render_to_response('weixin/query_error.html')