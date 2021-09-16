import re
from django.shortcuts import render
from .ques_gen import Ques_Gen_Book
import sqlite3
import sqlvalidator
import numpy as np
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
import string
from django.views.generic import TemplateView
count = 0
from questions import forms

def Login(request):
    context = {'form': forms.UserCreateForm()}
    return render(request,'login.html', context=context)

def SignUp(request):
    form_class = {'form': forms.UserCreateForm()}
    success_url = reverse_lazy("login")
    return render(request,'signup.html', context=form_class)

def TestPage(request):
    return render(request,'test.html')

def ThanksPage(request):
    return render(request,'thanks.html')

def index(request):
    return render(request,'index.html')

def question_gen_level(request):
    return render(request,'question_gen_level.html')

def question_gen_1(request):
    # global count
    # if count > 0:
    #     question_gen_2(request)
    hint1, hint2, dis_hint = "'No hints available'", "'No hints available'", False
    hint3='hidden'
    dis_hint = "hidden"
    disa = 'hidden'
    out_dis = 'hidden'
    ques_gen = Ques_Gen_Book()
    if not request.POST.get('ques'):
        ques, query = ques_gen.lvl_1_ques()
    else:
        ques = request.POST.get('ques')
        query = request.POST.get('correct_answer')
    answer, feedback, output, dis= '','','','hidden'
    print(request.POST)

    if request.POST.get('answer'):
        print("A")
        connection = sqlite3.connect("C:/Users/Riddhi Shah/Desktop/bookss.db")
        crsr = connection.cursor()

        correct_answer = str(request.POST.get('correct_answer'))
        print(correct_answer)
        crsr.execute(correct_answer)
        ans = crsr.fetchall()
        print('A', ans)

        user_ans = str(request.POST.get('answer'))
        print(user_ans)
        user_ans_check = sqlvalidator.parse(user_ans)
        answer = user_ans
        print(type(answer))
        print(type(ans))

        def Convert(string):
            li = list(string.split(" "))
            return li

        user_anss = Convert(answer)
        print(type(user_anss))

        print(len(user_ans.split()))
        print(len(correct_answer.split()))
        print(user_ans)

        if " " not in user_ans.strip():
            print('in')
            feedback = 'SyntaxError: No space provided'
        elif (len(user_ans.split()) != len(correct_answer.split())):
            feedback = 'Incomplete Input'
            # hint3 = 'visible'

        origs = []

        with open('C:/Users/Riddhi Shah/Desktop/ITS/intelligent_tutoring_system/keyword.txt',
                  mode='r') as fpp:
            for line in fpp.readlines():
                origs.append(line.split('\n')[0].lower())
        arrs = [re.sub(r'[^\w\s]', '', ele.lower()) for ele in user_anss]
        print(arrs)
        arr_copied = arrs.copy()
        flag = False
        for ele in arrs:
            if ele in origs:
                hint1, dis_hint = "'Keyword Error: " + ele + "'", "visible"
                flag = True
                break
        print(string.punctuation)
        print(answer)
        if '"' in user_ans:
            print('yo')
            feedback='Wrong answer'
            hint1, dis_hint = "'SyntaxError!! Double quotes are not supported in SQL '", "visible"

        elif not feedback:
            print('In')
            if (flag):
                print('In in', arr_copied)
                if (ele in origs):
                    print('chk', ele)
                    hint1, dis_hint = "'Keyword Error: " + ele + "'", 'visible'
                    feedback = "Incorrect Answer"
            elif not user_ans_check.is_valid():
                print('validator')
                feedback = 'Incorrect Answer'
                # hint3 = 'visible'
                if not (user_ans_check.errors == ['']):
                    Error = user_ans_check.errors
                    print(Error)
                    print('Error:', user_ans_check.errors)
                    print(type(Error))
                    listToStr = ' '.join([str(elem) for elem in Error])
                    print(type(listToStr))
                    print(listToStr)
                    err = 'The argument of WHERE must be type boolean, not type typing.Any'

                    if (err == listToStr):
                        hint1, dis_hint = "Incomplete where clause statement", 'visible'
                    elif isinstance(user_ans_check.errors, list):
                        hint1, dis_hint = "'" + user_ans_check.errors[0] + "'", "visible"
                    else:
                        hint1, dis_hint = "'" + user_ans_check.errors + "'", "visible"
            else:
                try:
                    crsr.execute(user_ans)
                    user_ans = crsr.fetchall()
                    print('B', user_ans)
                    output = user_ans
                    # for out in user_ans:
                    #     output += ', '.join(out) + ' <br> '
                    test_1 = set(ans) - set(user_ans)
                    test_2 = set(user_ans) - set(ans)
                    final = list(test_1) + list(test_2)
                    print(test_1, test_2, final)
                    # if (len(user_anss) != len(ans)):
                    #     feedback = 'Incomplete Input'
                    #     # hint3 = 'visible'
                    if (arr_copied != []):
                        if (ele in origs):
                            print(ele)
                            hint1, dis_hint = "'Keyword Error: " + ele + "'", True
                    if (len(final) == 0):
                        feedback = 'Correct Answer'
                        dis = 'visible'
                        hint3 = 'visible'
                        answer = ""
                        out_dis = 'visible'
                        # global count
                        # count += 1
                        # if (count > 0):
                        #     print('voila')
                            # request.POST.set('ques', '')
                            # question_gen_2(request)
                    else:
                        feedback = 'Incorrect Answer'
                        # hint3 = 'visible'
                    if (len(final) == 0):
                        feedback = 'Correct Answer'
                        dis = 'visible'
                        hint3 = 'visible'
                        answer = ""
                        out_dis = 'visible'
                        # global count
                        # count += 1
                        # if (count > 0):
                            # print('voila')
                            # request.POST.set('ques', '')
                            # question_gen_2(request)
                except:
                    hint1 = "'No syntax errors...Go to Hints 2!'"
                    dis_hint=False
                    # punc = '''!()-[]{};:'"\, <>./?@#$%^&~'''
                    arr1 = user_ans.split()
                    arr2 = user_ans.split()
                    ori = []
                    orig = []
                    with open('C:/Users/Riddhi Shah/Desktop/ITS/intelligent_tutoring_system/keywords.txt',
                              mode='r') as fp:
                        for line in fp.readlines():
                            ori.append(line.split('\n')[0].lower())
                    with open('C:/Users/Riddhi Shah/Desktop/ITS/intelligent_tutoring_system/tablename.txt',
                              mode='r') as f:
                        for line in f.readlines():
                            orig.append(line.split('\n')[0].lower())

                    arr1 = [re.sub(r'[^\w\s]', '', elem.lower()) for elem in arr1]
                    print(arr1)
                    arr_copy = arr1.copy()
                    for elem in arr1:
                        if elem:
                            if elem in ori:
                                arr_copy.remove(elem)
                            else:
                                break

                    if (arr_copied != []):
                        if (ele in origs):
                            print(ele)
                            hint1, dis_hint = "'Keyword Error: " + ele + "'", 'visible'
                    if (arr_copy == []):
                        print('Correct Answer')
                        out_dis='visible'
                        # # global count
                        # count += 1
                        # if (count > 0):
                        #     print('voila')
                        #     # request.POST.set('ques', '')
                        #     question_gen_2(request)
                    else:
                        feedback = 'Incorrect Answer'
                        # hint3 = 'visible'
                        print(elem)
                        if elem in orig:
                            msg = 'table name not found'
                            hint2, disa = "'Table does not exist: " + elem + "'", 'visible'
                            # dis_hint='hidden'
                            hint3 = 'visible'
                        else:
                            msg = 'No such attribute    '
                            hint2, disa = "'No such attribute found: " + elem + "'", 'visible'
                            # dis_hint='hidden'
                            hint3 = 'visible'
    else:
        feedback = 'Please give some input'
        print('empty')

    context = {'ques':ques,'feedback':feedback,'output':output,'out_dis':out_dis,'query':query, 'dis': dis, 'dis_hint':dis_hint, 'disa':disa, 'hint1':hint1, 'hint2':hint2, 'hint3':hint3, 'answer':answer}
    return render(request,'question_gen.html', context=context)

def question_gen_2(request):
    hint1, hint2, dis_hint = "'No hints available'", "'No hints available'", False
    hint3 = 'hidden'
    dis_hint = "hidden"
    disa = 'hidden'
    out_dis='hidden'
    ques_gen = Ques_Gen_Book()
    if not request.POST.get('ques'):
        ques, query = ques_gen.lvl_2_ques()
    else:
        ques = request.POST.get('ques')
        query = request.POST.get('correct_answer')
    answer, feedback, output, dis = '', '', '', 'hidden'
    print(request.POST)

    if request.POST.get('answer'):
        print("A")
        connection = sqlite3.connect("C:/Users/Riddhi Shah/Desktop/bookss.db")
        crsr = connection.cursor()

        correct_answer = str(request.POST.get('correct_answer'))
        print(correct_answer)
        crsr.execute(correct_answer)
        ans = crsr.fetchall()
        print('A', ans)

        user_ans = str(request.POST.get('answer'))
        print(user_ans)
        user_ans_check = sqlvalidator.parse(user_ans)
        answer = user_ans
        print(type(answer))
        print(type(ans))

        def Convert(string):
            li = list(string.split(" "))
            return li

        user_anss = Convert(answer)
        print(type(user_anss))

        print(len(user_ans.split()))
        print(len(correct_answer.split()))
        print(user_ans)
        # print(user_ans.isspace())

        if " " not in user_ans.strip():
            print('in')
            feedback = 'SyntaxError: No space provided'
        elif (len(user_ans.split()) != len(correct_answer.split())):
            feedback = 'Incomplete Input'
            # hint3 = 'visible'

        origs = []

        with open('C:/Users/Riddhi Shah/Desktop/ITS/intelligent_tutoring_system/keyword.txt',
                  mode='r') as fpp:
            for line in fpp.readlines():
                origs.append(line.split('\n')[0].lower())
        arrs = [re.sub(r'[^\w\s]', '', ele.lower()) for ele in user_anss]
        print(arrs)
        arr_copied = arrs.copy()
        flag = False
        for ele in arrs:
            if ele in origs:
                hint1, dis_hint = "'Keyword Error: " + ele + "'", "visible"
                flag = True
                break
        print(string.punctuation)
        print(answer)
        if '"' in user_ans:
            print('yo')
            feedback = 'Wrong answer'
            hint1, dis_hint = "'SyntaxError!! Double quotes are not supported in SQL '", "visible"
        elif not feedback:
            print('In')
            if (flag):
                print('In in', arr_copied)
                if (ele in origs):
                    print('chk', ele)
                    hint1, dis_hint = "'Keyword Error: " + ele + "'", 'visible'
                    feedback = "Incorrect Answer"
            elif not user_ans_check.is_valid():
                print('validator')
                feedback = 'Incorrect Answer'
                # hint3 = 'visible'
                if not (user_ans_check.errors == ['']):
                    Error = user_ans_check.errors
                    print(Error)
                    print('Error:', user_ans_check.errors)
                    print(type(Error))
                    listToStr = ' '.join([str(elem) for elem in Error])
                    print(type(listToStr))
                    print(listToStr)
                    err = 'The argument of WHERE must be type boolean, not type typing.Any'

                    if (err == listToStr):
                        hint1, dis_hint = "Incomplete where clause statement", 'visible'
                    elif isinstance(user_ans_check.errors, list):
                        hint1, dis_hint = "'" + user_ans_check.errors[0] + "'", "visible"
                    else:
                        hint1, dis_hint = "'" + user_ans_check.errors + "'", "visible"

            else:
                print('ya')
                try:
                    crsr.execute(user_ans)
                    user_ans = crsr.fetchall()
                    print('B', user_ans)
                    output = user_ans
                    # for out in user_ans:
                    #     output += ', '.join(out) + ' <br> '
                    test_1 = set(ans) - set(user_ans)
                    test_2 = set(user_ans) - set(ans)
                    final = list(test_1) + list(test_2)
                    print(test_1, test_2, final)

                    # if (len(user_anss) != len(ans)):
                    #     feedback = 'Incomplete Input'
                    #     # hint3 = 'visible'

                    if (arr_copied != []):
                        if (ele in origs):
                            print(ele)
                            hint1, dis_hint = "'Keyword Error: " + ele + "'", True
                    if (len(final) == 0):
                        feedback = 'Correct Answer'
                        dis = 'visible'
                        hint3 = 'visible'
                        answer = ""
                        out_dis = 'visible'
                        # global count
                        # count += 1
                        # if (count > 0):
                        #     print('voila')
                        # request.POST.set('ques', '')
                        # question_gen_2(request)

                    else:
                        feedback = 'Incorrect Answer'
                        # hint3 = 'visible'
                    if (len(final) == 0):
                        feedback = 'Correct Answer'
                        dis = 'visible'
                        hint3 = 'visible'
                        answer = ""
                        out_dis = 'visible'
                        # global count
                        # count += 1
                        # if (count > 0):
                        # print('voila')
                        # request.POST.set('ques', '')
                        # question_gen_2(request)
                except:
                    hint1 = "'No syntax errors...Go to Hints 2!'"
                    dis_hint = False
                    # punc = '''!()-[]{};:'"\, <>./?@#$%^&~'''
                    arr1 = user_ans.split()
                    arr2 = user_ans.split()
                    ori = []
                    orig = []
                    with open('C:/Users/Riddhi Shah/Desktop/ITS/intelligent_tutoring_system/keywords.txt',
                              mode='r') as fp:
                        for line in fp.readlines():
                            ori.append(line.split('\n')[0].lower())
                    with open('C:/Users/Riddhi Shah/Desktop/ITS/intelligent_tutoring_system/tablename.txt',
                              mode='r') as f:
                        for line in f.readlines():
                            orig.append(line.split('\n')[0].lower())

                    arr1 = [re.sub(r'[^\w\s]', '', elem.lower()) for elem in arr1]
                    print(arr1)
                    arr_copy = arr1.copy()
                    for elem in arr1:
                        if elem:
                            if elem in ori:
                                arr_copy.remove(elem)
                            else:
                                break

                    if (arr_copied != []):
                        if (ele in origs):
                            print(ele)
                            hint1, dis_hint = "'Keyword Error: " + ele + "'", 'visible'
                    if (arr_copy == []):
                        print('Correct Answer')
                        out_dis = 'visible'
                        # # global count
                        # count += 1
                        # if (count > 0):
                        #     print('voila')
                        #     # request.POST.set('ques', '')
                        #     question_gen_2(request)
                    else:
                        feedback = 'Incorrect Answer'
                        # hint3 = 'visible'
                        print(elem)
                        if elem in orig:
                            msg = 'table name not found'
                            hint2, disa = "'Table does not exist: " + elem + "'", 'visible'
                            hint3 = 'visible'
                        else:
                            msg = 'No such attribute    '
                            hint2, disa = "'No such attribute name found: " + elem + "'", 'visible'
                            hint3 = 'visible'
    else:
        feedback = 'Please give some input'
        print('empty')

    context = {'ques': ques, 'feedback': feedback, 'output': output,'out_dis':out_dis, 'query': query, 'dis': dis, 'dis_hint': dis_hint,
               'disa': disa, 'hint1': hint1, 'hint2': hint2, 'hint3': hint3, 'answer': answer}
    return render(request, 'question_gen.html', context=context)

def question_gen_3(request):
    hint1, hint2, dis_hint = "'No hints available'", "'No hints available'", False
    hint3 = 'hidden'
    dis_hint = "hidden"
    disa = 'hidden'
    out_dis = 'hidden'
    ques_gen = Ques_Gen_Book()
    if not request.POST.get('ques'):
        ques, query = ques_gen.lvl_3_ques()
    else:
        ques = request.POST.get('ques')
        query = request.POST.get('correct_answer')
    answer, feedback, output, dis = '', '', '', 'hidden'
    print(request.POST)

    if request.POST.get('answer'):
        print("A")
        connection = sqlite3.connect("C:/Users/Riddhi Shah/Desktop/bookss.db")
        crsr = connection.cursor()

        correct_answer = str(request.POST.get('correct_answer'))
        print(correct_answer)
        crsr.execute(correct_answer)
        ans = crsr.fetchall()
        print('A', ans)

        user_ans = str(request.POST.get('answer'))
        print(user_ans)
        user_ans_check = sqlvalidator.parse(user_ans)
        answer = user_ans
        print(type(answer))
        print(type(ans))

        def Convert(string):
            li = list(string.split(" "))
            return li

        user_anss = Convert(answer)
        print(type(user_anss))

        print(len(user_ans.split()))
        print(len(correct_answer.split()))
        print(user_ans)
        # print(user_ans.isspace())

        if " " not in user_ans.strip():
            print('in')
            feedback = 'Syntax Error: No space provided'
        elif (len(user_ans.split()) != len(correct_answer.split())):
            feedback = 'Incomplete Input'
            # hint3 = 'visible'

        origs = []

        with open('C:/Users/Riddhi Shah/Desktop/ITS/intelligent_tutoring_system/keyword.txt',
                  mode='r') as fpp:
            for line in fpp.readlines():
                origs.append(line.split('\n')[0].lower())
        arrs = [re.sub(r'[^\w\s]', '', ele.lower()) for ele in user_anss]
        print(arrs)
        arr_copied = arrs.copy()
        flag = False
        for ele in arrs:
            if ele in origs:
                hint1, dis_hint = "'Keyword error: " + ele + "'", "visible"
                flag = True
                break
        print(string.punctuation)
        print(answer)
        if '"' in user_ans:
            print('yo')
            feedback = 'Wrong answer'
            hint1, dis_hint = "'Syntax error!! Double quotes are not supported in SQL '", "visible"
        elif not feedback:
            print('In')
            if (flag):
                print('In in', arr_copied)
                if (ele in origs):
                    print('chk', ele)
                    hint1, dis_hint = "'Keyword error: " + ele + "'", 'visible'
                    feedback = "Incorrect Answer"
            elif not user_ans_check.is_valid():
                print('validator')
                feedback = 'Incorrect Answer'
                # hint3 = 'visible'
                if not (user_ans_check.errors == ['']):
                    Error = user_ans_check.errors
                    print(Error)
                    print('Error:', user_ans_check.errors)
                    print(type(Error))
                    listToStr = ' '.join([str(elem) for elem in Error])
                    print(type(listToStr))
                    print(listToStr)
                    err = 'The argument of WHERE must be type boolean, not type typing.Any'

                    if (err == listToStr):
                        hint1, dis_hint = "Incomplete where clause statement", 'visible'
                    elif isinstance(user_ans_check.errors, list):
                        hint1, dis_hint = "'" + user_ans_check.errors[0] + "'", "visible"
                    else:
                        hint1, dis_hint = "'" + user_ans_check.errors + "'", "visible"

            else:
                print('ya')
                try:
                    crsr.execute(user_ans)
                    user_ans = crsr.fetchall()
                    print('B', user_ans)
                    output = user_ans
                    # for out in user_ans:
                    #     output += ', '.join(out) + ' <br> '
                    test_1 = set(ans) - set(user_ans)
                    test_2 = set(user_ans) - set(ans)
                    final = list(test_1) + list(test_2)
                    print(test_1, test_2, final)

                    # if (len(user_anss) != len(ans)):
                    #     feedback = 'Incomplete Input'
                    #     # hint3 = 'visible'

                    if (arr_copied != []):
                        if (ele in origs):
                            print(ele)
                            hint1, dis_hint = "'Keyword error: " + ele + "'", True
                    if (len(final) == 0):
                        feedback = 'Correct Answer'
                        dis = 'visible'
                        hint3 = 'visible'
                        answer = ""
                        out_dis = 'visible'
                        # global count
                        # count += 1
                        # if (count > 0):
                        #     print('voila')
                        # request.POST.set('ques', '')
                        # question_gen_2(request)

                    else:
                        feedback = 'Incorrect Answer'
                        # hint3 = 'visible'
                    if (len(final) == 0):
                        feedback = 'Correct Answer'
                        dis = 'visible'
                        hint3 = 'visible'
                        answer = ""
                        out_dis = 'visible'
                        # global count
                        # count += 1
                        # if (count > 0):
                        # print('voila')
                        # request.POST.set('ques', '')
                        # question_gen_2(request)
                except:
                    hint1 = "'No syntax errors...Go to Hints 2!'"
                    dis_hint = False
                    # punc = '''!()-[]{};:'"\, <>./?@#$%^&~'''
                    arr1 = user_ans.split()
                    arr2 = user_ans.split()
                    ori = []
                    orig = []
                    with open('C:/Users/Riddhi Shah/Desktop/ITS/intelligent_tutoring_system/keywords.txt',
                              mode='r') as fp:
                        for line in fp.readlines():
                            ori.append(line.split('\n')[0].lower())
                    with open('C:/Users/Riddhi Shah/Desktop/ITS/intelligent_tutoring_system/tablename.txt',
                              mode='r') as f:
                        for line in f.readlines():
                            orig.append(line.split('\n')[0].lower())

                    arr1 = [re.sub(r'[^\w\s]', '', elem.lower()) for elem in arr1]
                    print(arr1)
                    arr_copy = arr1.copy()
                    for elem in arr1:
                        if elem:
                            if elem in ori:
                                arr_copy.remove(elem)
                            else:
                                break

                    if (arr_copied != []):
                        if (ele in origs):
                            print(ele)
                            hint1, dis_hint = "'Keyword error: " + ele + "'", 'visible'
                    if (arr_copy == []):
                        print('Correct Answer')
                        out_dis = 'visible'
                        # # global count
                        # count += 1
                        # if (count > 0):
                        #     print('voila')
                        #     # request.POST.set('ques', '')
                        #     question_gen_2(request)
                    else:
                        feedback = 'Incorrect Answer'
                        # hint3 = 'visible'
                        print(elem)
                        if elem in orig:
                            msg = 'table name not found'
                            hint2, disa = "'Table does not exist: " + elem + "'", 'visible'
                            hint3 = 'visible'
                        else:
                            msg = 'No such attribute    '
                            hint2, disa = "'No such attribute name found: " + elem + "'", 'visible'
                            hint3 = 'visible'
    else:
        feedback = 'Please give some input'
        print('empty')

    context = {'ques': ques, 'feedback': feedback, 'output': output,'out_dis':out_dis, 'query': query, 'dis': dis, 'dis_hint': dis_hint,
               'disa': disa, 'hint1': hint1, 'hint2': hint2, 'hint3': hint3, 'answer': answer}
    return render(request, 'question_gen.html', context=context)

def question_gen_4(request):
    hint1, hint2, dis_hint = "'No hints available'", "'No hints available'", False
    hint3 = 'hidden'
    dis_hint = "hidden"
    disa = 'hidden'
    out_dis = 'hidden'
    ques_gen = Ques_Gen_Book()
    if not request.POST.get('ques'):
        ques, query = ques_gen.lvl_4_ques()
    else:
        ques = request.POST.get('ques')
        query = request.POST.get('correct_answer')
    answer, feedback, output, dis = '', '', '', 'hidden'
    print(request.POST)

    if request.POST.get('answer'):
        print("A")
        connection = sqlite3.connect("C:/Users/Riddhi Shah/Desktop/bookss.db")
        crsr = connection.cursor()

        correct_answer = str(request.POST.get('correct_answer'))
        print(correct_answer)
        crsr.execute(correct_answer)
        ans = crsr.fetchall()
        print('A', ans)

        user_ans = str(request.POST.get('answer'))
        print(user_ans)
        user_ans_check = sqlvalidator.parse(user_ans)
        answer = user_ans
        print(type(answer))
        print(type(ans))

        def Convert(string):
            li = list(string.split(" "))
            return li

        user_anss = Convert(answer)
        print(type(user_anss))

        print(len(user_ans.split()))
        print(len(correct_answer.split()))
        print(user_ans)
        # print(user_ans.isspace())

        if " " not in user_ans.strip():
            print('in')
            feedback = 'SyntaxError: No space provided'
        elif (len(user_ans.split()) != len(correct_answer.split())):
            feedback = 'Incomplete Input'
            # hint3 = 'visible'

        origs = []

        with open('C:/Users/Riddhi Shah/Desktop/ITS/intelligent_tutoring_system/keyword.txt',
                  mode='r') as fpp:
            for line in fpp.readlines():
                origs.append(line.split('\n')[0].lower())
        arrs = [re.sub(r'[^\w\s]', '', ele.lower()) for ele in user_anss]
        print(arrs)
        arr_copied = arrs.copy()
        flag = False
        for ele in arrs:
            if ele in origs:
                hint1, dis_hint = "'Keyword error: " + ele + "'", "visible"
                flag = True
                break
        print(string.punctuation)
        print(answer)
        if '"' in user_ans:
            print('yo')
            feedback = 'wrong answer'
            hint1, dis_hint = "'Syntax error!! Double quotes are not supported in SQL '", "visible"
        elif not feedback:
            print('In')
            if (flag):
                print('In in', arr_copied)
                if (ele in origs):
                    print('chk', ele)
                    hint1, dis_hint = "'Keyword error: " + ele + "'", 'visible'
                    feedback = "Incorrect Answer"
            elif not user_ans_check.is_valid():
                print('validator')
                feedback = 'Incorrect Answer'
                # hint3 = 'visible'
                if not (user_ans_check.errors == ['']):
                    Error = user_ans_check.errors
                    print(Error)
                    print('Error:', user_ans_check.errors)
                    print(type(Error))
                    listToStr = ' '.join([str(elem) for elem in Error])
                    print(type(listToStr))
                    print(listToStr)
                    err = 'The argument of WHERE must be type boolean, not type typing.Any'

                    if (err == listToStr):
                        hint1, dis_hint = "Incomplete where clause statement", 'visible'
                    elif isinstance(user_ans_check.errors, list):
                        hint1, dis_hint = "'" + user_ans_check.errors[0] + "'", "visible"
                    else:
                        hint1, dis_hint = "'" + user_ans_check.errors + "'", "visible"

            else:
                print('ya')
                try:
                    crsr.execute(user_ans)
                    user_ans = crsr.fetchall()
                    print('B', user_ans)
                    output = user_ans
                    # for out in user_ans:
                    #     output += ', '.join(out) + ' <br> '
                    test_1 = set(ans) - set(user_ans)
                    test_2 = set(user_ans) - set(ans)
                    final = list(test_1) + list(test_2)
                    print(test_1, test_2, final)

                    # if (len(user_anss) != len(ans)):
                    #     feedback = 'Incomplete Input'
                    #     # hint3 = 'visible'

                    if (arr_copied != []):
                        if (ele in origs):
                            print(ele)
                            hint1, dis_hint = "'Keyword error: " + ele + "'", True
                    if (len(final) == 0):
                        feedback = 'Correct Answer'
                        dis = 'visible'
                        hint3 = 'visible'
                        answer = ""
                        out_dis = 'visible'
                        # global count
                        # count += 1
                        # if (count > 0):
                        #     print('voila')
                        # request.POST.set('ques', '')
                        # question_gen_2(request)

                    else:
                        feedback = 'Incorrect Answer'
                        # hint3 = 'visible'
                    if (len(final) == 0):
                        feedback = 'Correct Answer'
                        dis = 'visible'
                        hint3 = 'visible'
                        answer = ""
                        out_dis = 'visible'
                        # global count
                        # count += 1
                        # if (count > 0):
                        # print('voila')
                        # request.POST.set('ques', '')
                        # question_gen_2(request)
                except:
                    hint1 = "'No syntax errors...Go to Hints 2!'"
                    dis_hint = False
                    # punc = '''!()-[]{};:'"\, <>./?@#$%^&~'''
                    arr1 = user_ans.split()
                    arr2 = user_ans.split()
                    ori = []
                    orig = []
                    with open('C:/Users/Riddhi Shah/Desktop/ITS/intelligent_tutoring_system/keywords.txt',
                              mode='r') as fp:
                        for line in fp.readlines():
                            ori.append(line.split('\n')[0].lower())
                    with open('C:/Users/Riddhi Shah/Desktop/ITS/intelligent_tutoring_system/tablename.txt',
                              mode='r') as f:
                        for line in f.readlines():
                            orig.append(line.split('\n')[0].lower())

                    arr1 = [re.sub(r'[^\w\s]', '', elem.lower()) for elem in arr1]
                    print(arr1)
                    arr_copy = arr1.copy()
                    for elem in arr1:
                        if elem:
                            if elem in ori:
                                arr_copy.remove(elem)
                            else:
                                break

                    if (arr_copied != []):
                        if (ele in origs):
                            print(ele)
                            hint1, dis_hint = "'Keyword error: " + ele + "'", 'visible'
                    if (arr_copy == []):
                        print('Correct Answer')
                        out_dis = 'visible'
                        # # global count
                        # count += 1
                        # if (count > 0):
                        #     print('voila')
                        #     # request.POST.set('ques', '')
                        #     question_gen_2(request)
                    else:
                        feedback = 'Incorrect Answer'
                        # hint3 = 'visible'
                        print(elem)
                        if elem in orig:
                            msg = 'table name not found'
                            hint2, disa = "'Table does not exist: " + elem + "'", 'visible'
                            hint3 = 'visible'
                        else:
                            msg = 'No such attribute    '
                            hint2, disa = "'No such attribute name found: " + elem + "'", 'visible'
                            hint3 = 'visible'
    else:
        feedback = 'Please give some input'
        print('empty')

    context = {'ques': ques, 'feedback': feedback, 'output': output,'out_dis':out_dis ,'query': query, 'dis': dis, 'dis_hint': dis_hint,
               'disa': disa, 'hint1': hint1, 'hint2': hint2, 'hint3': hint3, 'answer': answer}
    return render(request, 'question_gen.html', context=context)
