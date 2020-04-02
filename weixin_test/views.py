from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse,HttpResponseRedirect
from wechatpy import parse_message,create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import WeChatClient
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from wechatpy.replies import ArticlesReply
from wechatpy.oauth import WeChatOAuth
from .models import Patient,Result
import json
from .users import data
from django.template import RequestContext
from wechatpy.replies import ArticlesReply

# test account information
TOKEN = 'hellowx'
appID = 'wx6c11f5e4bbd229bd'
appsecret = '1605f2bca63385b87ec35daffa2227ea'
redirect_uri = "https://georgecaozi.pythonanywhere.com/weixin/register_form_after_oath"
oauthClient = WeChatOAuth(app_id=appID,secret=appsecret,redirect_uri=redirect_uri,scope='snsapi_userinfo')
client = WeChatClient(appID,appsecret)
template_ID = 'H4kLGQVAOsECMjiXzytItVBsNZp0-i-loGaRBcgwKRk'

@csrf_exempt
def index(request):
    if request.method == 'GET':      
        signature = request.GET.get('signature','')
        timestamp = request.GET.get('timestamp','')
        nonce = request.GET.get('nonce','')
        echostr = request.GET.get('echostr','')
        try:
            check_signature(TOKEN,signature,timestamp,nonce)
        except InvalidSignatureException:
            echostr = 'error'
        response = HttpResponse(echostr,content_type="text/plain")
        return response
    elif request.method == 'POST':
        reply = None
        msg = parse_message(request.body)
        if msg.type == 'text':
            reply = create_reply('感谢关注病理科微信公众号，病理结果会第一时间推送，请密切关注',msg)
        elif msg.event == 'subscribe':
            reply = ArticlesReply(message=msg)
            reply.add_article({
                'title':'一步步教你如何登记病人信息，及时得到病理结果推送',
                'description':'tutorial',
                'image':'images/steps.jpg'
            })
        response = HttpResponse(reply.render(),content_type='application/xml')
        return response
    else:
        return HttpResponse('ERROR')



def create_menu(request):
    client.menu.create({
        "button":[
            {"type":"view","name":"登记","url":"http://georgecaozi.pythonanywhere.com/weixin/register_form/"},
            {"type":"view","name":"查询","url":"http://georgecaozi.pythonanywhere.com/weixin/query_form"},
            {"type":"view","name":"登录","url":"http://georgecaozi.pythonanywhere.com/weixin/login_form"}
            ]
        }
            )
    return HttpResponse('ok')


def get_openid(request):
    # return redirect(oauthClient.authorize_url)
    return HttpResponseRedirect(oauthClient.authorize_url)


def register_form(request):
    if request.method == 'GET':
        code = request.GET['code']
        res = oauthClient.fetch_access_token(code=code)
        params = {'openid':res['openid']}
    else:
        params = {'openid':'error'}
    return render_to_response('weixin/register_form.html', params)

def query_form(request):
    return render_to_response('weixin/query_form.html')
    

@csrf_exempt
def register(request):
    if request.method == "POST":
        p_id = request.POST.get('patient_id_first','')
        p_name = request.POST.get('patient_name','')
        p_gender = request.POST.get('patient_gender','')
        p_age = request.POST.get('patient_age','23')
        p_openID = request.POST.get('patient_openID','')
        p_result = Result.objects.get(result="正在处理中")
        try:
            _ = Patient.objects.get(patient_id = p_id)
        except Patient.DoesNotExist:
            p = Patient(patient_id = p_id,
                    patient_name=p_name,
                    patient_gender=p_gender,
                    patient_age=p_age,
                    patient_openID = p_openID,
                    patient_result = p_result
                )
            p.save()
            send_message(template_ID,p)
            return HttpResponseRedirect('register_success/')
        else:
            context_dict = {'patient_id':p_id,
                            'patient_name':p_name,
                            'patient_age':p_age,
                            'patient_gender':p_gender,
                            'patient_openID':p_openID,
                            'patient_result':p_result
                    }
            return render(request,'weixin/register_form_override.html',context_dict)
           
    return HttpResponse('Data not received',content_type="text/plain")


@csrf_exempt
def query(request):
    if request.method == "POST":
        p_id = request.POST.get("patient_id",'')
        try:
            p = Patient.objects.get(patient_id = p_id)
        except Patient.DoesNotExist:
            return render_to_response('weixin/query_error.html')
        return render(request,'weixin/query_result.html',{'patient':p})

def register_success(request):
    return render_to_response('weixin/register_success.html')

@csrf_exempt
def register_override(request):
    if request.method == "POST":                                                                                                                
        p_id = request.POST.get('patient_id','')
        p_name = request.POST.get('patient_name','')
        p_gender = request.POST.get('patient_gender','')
        p_age = request.POST.get('patient_age','')
        p_openID = request.POST.get('patient_openID','')
        p_result = Result.objects.get(result="正在处理中")
        p = Patient.objects.get(patient_id = p_id)
        p.delete()
        p = Patient(patient_id = p_id,
                patient_name=p_name,
                patient_gender=p_gender,
                patient_age=p_age,
                patient_openID = p_openID,
                patient_result = p_result
             )
        p.save()
        send_message(template_ID,p)
        return HttpResponseRedirect('register_success/')
    return HttpResponse('Data not received',content_type="text/plain")  


def login_form(request):
    return render_to_response('weixin/login_form.html')


@csrf_exempt
def login(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name','')
        user_password = request.POST.get('user_password','')
        try:
            if data[user_name] == user_password:
                return render_to_response('weixin/admin_query_form.html')
            else:
                return render_to_response('weixin/login_error.html')
        except:
            return render_to_response('weixin/query_error.html')
        
        
           
    return HttpResponse('Data not received',content_type="text/plain")

@csrf_exempt
def admin_query(request):
    if request.method == 'POST':
        p_id = request.POST.get('patient_id','')
        try:
            p = Patient.objects.get(patient_id = p_id)
            return render(request,'weixin/admin_query_result.html',{'patient':p})
        except Patient.DoesNotExist:
            return render_to_response('weixin/query_error.html')
    return HttpResponse('Data not received',content_type="text/plain")

def send_message(template_ID,patient):
    data={
          'patient_id':{'value':patient.patient_id},
          'patient_name':{'value':patient.patient_name},
          'patient_age':{'value':patient.patient_age},
          'patient_gender':{'value':patient.patient_gender},
          'patient_result':{'value':patient.patient_result.result,'color':'#B22222'}
        }
    client.message.send_template(patient.patient_openID,template_ID,data)



@csrf_exempt
def admin_query_override(request):
    if request.method == "POST":                                                                                                                
        p_id = request.POST.get('patient_id','')
        p_name = request.POST.get('patient_name','')
        p_gender = request.POST.get('patient_gender','')
        p_age = request.POST.get('patient_age','')
        p_openID = request.POST.get('patient_openID','')
        p_result = Result.objects.get(result=request.POST.get('patient_result',''))
        p = Patient.objects.get(patient_id = p_id)
        p.delete()
        p = Patient(patient_id = p_id,
                    patient_name=p_name,
                    patient_gender=p_gender,
                    patient_age=p_age,
                    patient_openID = p_openID,
                    patient_result = p_result
             )
        p.save()
        send_message(template_ID,p)
        return render_to_response('weixin/admin_query_success.html')
    return HttpResponse('Data not received',content_type="text/plain") 

