from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import UserForm,UploadFileForm
from .models import UserProfile, CategoriesQ , Ins, Questions
from django.db import connection
import locale
import os, filecmp
import datetime
import mimetypes

# Create your views here.
codes = {200:'success',404:'file not found',400:'Compilation Error',408:'Timeout',1:"Accepted",0:"Wrong Answer"}

def home(request):
    if not request.user.is_authenticated():
        return render(request, 'avs/login.html')
    else:
        dic = []
        ccx=0
        s = []
        for i in CategoriesQ.objects.all():
            s.append(i)
            ccx = ccx + 1
            if ccx % 3 == 0:
                dic.append(s)
                s = []
        if not ccx % 3 == 0:
            dic.append(s)
        return render(request, 'avs/home_new.html', {"dic":dic})


def xsendfile(request, file_path, original_filename):
    fp = open(file_path, 'rb')
    response = HttpResponse(fp.read())
    fp.close()
    type, encoding = mimetypes.guess_type(original_filename)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    response['Content-Length'] = str(os.stat(file_path).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding

    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s' % original_filename.encode('utf-8')
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        #filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(original_filename.encode('utf-8'))
        filename_header = ''
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response

def submissions(request):
    cursor = connection.cursor()
    cursor.execute("Select avs_Questions.Name,avs_submission.language,avs_submission.time_taken,\
        avs_submission.score,avs_submission.Code,avs_submission.verdict from avs_Questions,avs_submission where\
        avs_submission.Qid_id=avs_Questions.id and avs_submission.Uid_id=%s",[request.user.id])
    X =cursor.fetchall()
    return render(request, 'avs/submissions.html', {'x': X})



def QuestionsList(request, Cid):
    category = get_object_or_404(CategoriesQ, pk=Cid)
    cursor = connection.cursor()
    c = category.Cid
    n = category.Name
    cursor.execute("Select avs_Questions.id as ID,avs_Questions.Name as NAM,avs_Questions.Difficulty as DIFF, \
        avs_Questions.Time_Limit as TL, avs_Questions.Memory_Limit as ML from avs_Questions,avs_Ins,avs_CategoriesQ \
        where avs_CategoriesQ.Cid= avs_Ins.category_id and \
        avs_Questions.id=avs_Ins.questions_id and avs_CategoriesQ.Cid=%s",[c])
    X = cursor.fetchall()
    cursor.execute("Select questions_id as ID from avs_solved")
    Y=cursor.fetchall()
    ids=[]
    for i in Y:
        ids.append(i[0])
    return render(request, 'avs/questionsList.html',{'list':X, 'Cname':n, 'solved': ids})

def scoreboard(request):
    cursor = connection.cursor()
    cursor.execute("Select username as Name, score / 100 as QuestionsSolved, score as Score\
     from avs_userprofile, auth_user where avs_userprofile.id = auth_user.id")
    X =cursor.fetchall()
    return render(request, 'avs/scoreboard.html', {'x': X})


def compile(request, Qid,lan,fname):
    question = get_object_or_404(Questions, pk=Qid)
    cursor = connection.cursor()
    c = question.id
    cursor.execute("Select inputTestFile,outputTestFile,Time_Limit \
     from avs_questions,avs_testcase where avs_questions.id=%s",[c])
    X = cursor.fetchall()
    m = []
    TimeL = 0
    compilerError = False
    runTimeError = False
    fnf = False
    maxtt = 0
    for i in X:
        inp = i[0]
        out = i[1]
        tl = i[2]
        TimeL = tl
        with open(inp,'r',encoding=locale.getpreferredencoding()) as a_file:
            a_content = a_file.read()
            with open('Testcase0.txt','w',encoding=locale.getpreferredencoding()) as b_file:
                b_file.write(a_content)

        with open(out,'r',encoding=locale.getpreferredencoding()) as a_file:
            a_content = a_file.read()
            with open('TestcaseOut0.txt','w',encoding=locale.getpreferredencoding()) as b_file:
                b_file.write(a_content) 

        file = 'sub.'+lan
        lang = lan
        testin = 'Testcase0.txt'
        testout = 'TestcaseOut0.txt'
        timeout = str(tl) # secs

        c = compile1(file,lan)
        if c == 400:
            compilerError = True
        if c == 404:
            fof = True
        if c ==200:
            tin = datetime.datetime.now()
            r = run('sub',testin,timeout,lang)  
            tout = datetime.datetime.now()
            tt = (tout-tin)
            if maxtt < float(tt.total_seconds()):
                maxtt = float(tt.total_seconds())
            tt = str(tt)
            if r == 408:
                runTimeError = True
            if r == 404:
                fof = True

            m.append([match(testout),tt])

    x = 1
    for i in m:
        if i[0] is False:
            x = 0

    if compilerError:
        x = 400
    if runTimeError:
        x = 408
    if fnf:
        x = 404

    fil = "sub."+lan
    s = 0
    if x == 1:
        s = 100
    maxtt = str(maxtt)
    v = str(x) 
    cursor.execute("Insert into avs_submission (time_taken,time_limit,language,score,Qid_id,Uid_id,Code,verdict) \
        values (%s,%s,%s,%s,%s,%s,%s,%s)",([maxtt],[TimeL],[lan],[s],[Qid],[request.user.id],[fname],[v]))
    cursor.execute("Select score from avs_userprofile where id = %s",[request.user.id])
    e = cursor.fetchall()
    d = str(int(s) + int(e[0][0]))
    cursor.execute("select count(*) from avs_solved where questions_id = %s and users_id = %s",([Qid],[request.user.id]))
    count = cursor.fetchall()[0]
    if count[0]==0 and x is True:
        cursor.execute("update avs_userprofile set score = %s where id = %s",([d],[request.user.id]))
        cursor.execute("insert into avs_solved (questions_id,users_id)\
         values (%s,%s)",([Qid],[request.user.id]))
    return render(request, 'avs/compile.html',{'verdict':m , 'answer':codes[x]})

def QuestionSolve(request, Qid):
    question = get_object_or_404(Questions, pk=Qid)
    cursor = connection.cursor()
    c = question.id
    cursor.execute("Select avs_Questions.Name,avs_Questions.ProblemStatement, \
    avs_Questions.InputFormat,avs_Questions.OutputFormat,avs_Questions.Constraints,\
    avs_Questions.SampleInput,avs_Questions.SampleOutput,avs_Questions.Memory_limit, \
    avs_Questions.Time_limit from avs_Questions where avs_Questions.id=%s",[c])
    X = cursor.fetchall()
    # t = X[0][1]
    # f = open(t)
    # stat = f.read()
    # f.close()
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            lan = form.cleaned_data['Language']
            fname = handle_uploaded_file(request.FILES['Code'],lan,request.user.id)
            return HttpResponseRedirect('/compile/'+Qid + '/' + lan+'/' + fname +'/')
    else:
        form = UploadFileForm()
    return render(request, 'avs/questionSolve.html',{'list':X,'form':form})

def handle_uploaded_file(f,lan,userid):
    with open('sub.'+lan,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    fname = str(userid) + ''.join(e for e in str(datetime.datetime.now()) if e.isalnum())
    with open(fname+'.'+lan,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk) 
    return fname+'.'+lan

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('avs:home')
            else:
                return render(request, 'avs/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'avs/login.html', {'error_message': 'Invalid login'})
    return render(request, 'avs/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        userprofile = UserProfile(user=user,score=0)
        userprofile.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #albums = Album.objects.filter(user=request.user)
                return redirect('avs:home')
    context = {
        "form": form,
    }
    return render(request, 'avs/register.html', context)


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'avs/login.html', context)

#compiler

def compile1(file,lang):
    if lang == 'java':
        class_file = file[:-4]+"class"
    elif lang == 'c':
        class_file = file[:-2]
    elif lang=='cpp':
        class_file = file[:-4]

    if (os.path.isfile(class_file)):
        os.remove(class_file)
    if (os.path.isfile(file)):
        if lang == 'java':
            os.system('javac '+file)
        elif lang == 'c' or lang == 'cpp':
            os.system('g++ '+file+' -o '+class_file)
        if (os.path.isfile(class_file)):
            return 200
        else:
            return 400
    else:
        return 404

def run(file,input,timeout,lang):
    if lang == 'java':
        cmd = 'java '+file
    elif lang=='c' or lang=='cpp':
        cmd = './'+file
    r = os.system('timeout '+timeout+' '+cmd+' < '+input+' > out.txt')
    if lang == 'java':
        os.remove(file+'.class')
    elif lang == 'c' or lang == 'cpp':
        os.remove(file)
    if r==0:
        return 200
    elif r==31744:
        os.remove('out.txt')
        return 408
    else:
        os.remove('out.txt')
        return 400

def match(output):
    if os.path.isfile('out.txt') and os.path.isfile(output):
        b = filecmp.cmp('out.txt',output)
        #os.remove('out.txt')
        return b
    else:
        return 404
