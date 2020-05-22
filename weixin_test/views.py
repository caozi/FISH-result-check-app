from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import WeChatClient
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from wechatpy.oauth import WeChatOAuth
from .models import Patient, Doctor
from .weixin_config import TOKEN, appID, appsecret, template_ID
from django.http import JsonResponse

redirect_uri = "https://georgecaozi.pythonanywhere.com/weixin/register_form_after_oath"
redirect_uri_member = "https://georgecaozi.pythonanywhere.com/weixin/login_with_oath"
oauthClient = WeChatOAuth(app_id=appID, secret=appsecret, redirect_uri=redirect_uri)
oauthClient_member = WeChatOAuth(app_id=appID, secret=appsecret, redirect_uri=redirect_uri_member)
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


# 创建菜单
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


# 会诊登记页面
def register_form(request):
    if request.method == 'GET':
        code = request.GET['code']
        res = oauthClient.fetch_access_token(code=code)
        doctors_names = Doctor.objects.values('doctor_name')
        params = {'openid': res['openid'],
                  'doctors': doctors_names
                  }
        return render_to_response('weixin/register_form.html', params)
    else:
        return HttpResponseRedirect(oauthClient.authorize_url)


# 会诊登记页面处理
@csrf_exempt
def register(request):
    if request.method == "POST":
        p_id = request.POST.get('patient_id_first', '')
        p_name = request.POST.get('patient_name', '')
        p_openID = request.POST.get('patient_openID', '')
        p_phone = request.POST.get('patient_phone', '')
        p_doctor = Doctor.objects.get(doctor_name=request.POST.get('patient_doctor'))
        p = Patient(patient_id=p_id,
                    patient_name=p_name,
                    patient_openID=p_openID,
                    patient_phone=p_phone,
                    patient_doctor=p_doctor,
                    patient_status="正在处理中",
                    patient_note='无',
                    )
        p.save()
        request.session['registered'] = True
        request.session['openID'] = p_openID
        send_message(template_ID, p)
        return render_to_response('weixin/register_success.html')
    return HttpResponse('Data not received', content_type="text/plain")


# 查询
def query_form(request):
    registered = request.session.get('registered', False)
    if registered:
        p_openID = request.session['openID']
        p = Patient.objects.get(patient_openID=p_openID)
        return render(request, 'weixin/query_result.html', {'patient': p})
    else:
        return render_to_response('weixin/query_error.html')


# 登录页面
def login_form(request):
    authorized = request.session.get('authorized', False)
    if authorized:
        d_openID = request.session.get('openID')
        doctor = Doctor.objects.get(doctor_openID=d_openID)
        patients_not_informed = Patient.objects.filter(patient_doctor=doctor).exclude(
            patient_status='请来报告中心取病理报告').order_by('patient_id')
        return render(request, 'weixin/admin_patients_not_informed.html',
                      {'patients_not_informed': patients_not_informed})
    else:
        return HttpResponseRedirect(oauthClient_member.authorize_url)


@csrf_exempt
def admin_query_override(request):
    if request.method == "POST":
        p_id = request.POST.get('patient_id', '')
        p_status = request.POST.get('patient_status', '')
        p_note = request.POST.get('patient_note', '')
        p = Patient.objects.get(patient_id=p_id)
        p.patient_status = p_status
        p.patient_note = p_note
        p.save()
        send_message(template_ID, p)
        return render_to_response('weixin/admin_query_success.html')
    return HttpResponse('Data not received', content_type="text/plain")


# 检查患者输入的会诊号是否存在
def check_patient_ID_exist(request):
    p_id = request.GET.get('patient_id', None)
    try:
        _ = Patient.objects.get(patient_id=p_id)
    except Patient.DoesNotExist:
        data = {}
    else:
        data = {'exist': True}
    return JsonResponse(data)


@csrf_exempt
def admin_query(request):
    if request.method == 'POST':
        p_id = request.POST.get('patient_id', '')
        try:
            p = Patient.objects.get(patient_id=p_id)
            return render(request, 'weixin/admin_query_result.html', {'patient': p})
        except Patient.DoesNotExist:
            return render_to_response('weixin/query_error.html')
    return HttpResponse('Data not received', content_type="text/plain")


@csrf_exempt
def admin_query_override(request):
    p_id = request.GET.get('patient_id')
    p_status = request.GET.get('patient_status')
    p_note = request.GET.get('patient_note')
    p = Patient.objects.get(patient_id=p_id)
    p.patient_status = p_status
    p.patient_note = p_note
    p.save()
    try:
        send_message(template_ID, p)
    except :
        data = {'notify': False}
    else:
        data = {'notify': True}
    return JsonResponse(data)



def back_to_admin_query(request):
    notify = request.POST.get('notify')
    p_id = request.POST.get('patient_id')
    if notify == 'success':
        d_openID = request.session.get('openID')
        doctor = Doctor.objects.get(doctor_openID=d_openID)
        patients_not_informed = Patient.objects.filter(patient_doctor=doctor).exclude(
            patient_status='请来报告中心取病理报告').order_by('patient_id')
        return render(request, 'weixin/admin_patients_not_informed.html',
                      {'patients_not_informed': patients_not_informed})
    else:
        p = Patient.objects.get(patient_id=p_id)
        return render(request, 'weixin/notify_by_phone.html', {'patient': p})


def back_to_admin_query_after_phone(request):
    d_openID = request.session.get('openID')
    doctor = Doctor.objects.get(doctor_openID=d_openID)
    patients_not_informed = Patient.objects.filter(patient_doctor=doctor).exclude(
        patient_status='请来报告中心取病理报告').order_by('patient_id')
    return render(request, 'weixin/admin_patients_not_informed.html',
                  {'patients_not_informed': patients_not_informed})




def login_with_oath(request):
    code = request.GET['code']
    res = oauthClient_member.fetch_access_token(code=code)
    try:
        _ = Doctor.objects.get(doctor_openID=res['openid'])
        request.session['authorized'] = True
        request.session['openID'] = res['openid']
        doctor = Doctor.objects.get(doctor_openID=res['openid'])
        patients_not_informed = Patient.objects.filter(patient_doctor=doctor).exclude(
            patient_status='请来报告中心取病理报告').order_by('patient_id')
        return render(request, 'weixin/admin_patients_not_informed.html',
                      {'patients_not_informed': patients_not_informed})
    except:
        return render_to_response('weixin/login_error.html')


def send_message(template_ID, patient):
    data = {
        'patient_id': {'value': patient.patient_id},
        'patient_name': {'value': patient.patient_name},
        'patient_status': {'value': patient.patient_status, 'color': '#B22222'},
        'patient_note': {'value': patient.patient_note, 'color': '#B22222'},
        'patient_doctor': {'value': patient.patient_doctor.doctor_name}
    }
    client.message.send_template(patient.patient_openID, template_ID, data)
