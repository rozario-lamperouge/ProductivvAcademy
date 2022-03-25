from django.shortcuts import render
from django.views.generic import View
from courses.models import Course, CourseResource, Video, Lesson
from django.db.models import Q
from django.shortcuts import redirect

from django.http import HttpResponse
from django.core.mail import send_mail
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite, CourseComments, UserCourse
from users.models import UserProfile
from utils.mixin_utils import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum
from .forms import NameForm
from PIL import Image, ImageDraw, ImageFont
from wsgiref.util import FileWrapper
import mimetypes


class Payment(LoginRequiredMixin, View):

    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        user = request.user
        user_id = request.user.id
        amount = course.price
        transaction = Transaction.objects.create(made_by=user, amount=amount)
        transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY

        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(transaction.made_by.email)),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            # ('USER', request.user),
            # ('COURSE_ID', course_id),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'https://www.productivvacademy.com/course/callback/'+str(course_id)+"/"+str(user_id)+"/"),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)
        
        transaction.checksum = checksum
        transaction.save()

        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        return render(request, 'redirect.html', context=paytm_params)


@csrf_exempt
def callback(request,course_id,user_id):
    course = Course.objects.get(id=course_id)
    user = UserProfile.objects.get(pk=user_id)
    print(user)
    # Judging Favorite
    has_fav_course = False
    has_fav_org = False
    print(request.user)

    if request.method == 'POST':
        paytm_checksum = ''
        print(request.body)
        print(request.POST)
        received_data = dict(request.POST)
        print(received_data)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        print(paytm_params)
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            print("Checksum Matched")
            received_data['message'] = "Checksum Matched"
        else:
            print("Checksum Mismatched")
            received_data['message'] = "Checksum Mismatched"

        # if request.user.is_authenticated:
        #     if UserFavorite.objects.filter(user=request.user, fav_id=course.id,
        #                                    fav_type=1):
        #         has_fav_course = True
        #     if UserFavorite.objects.filter(user=request.user,
        #                                    fav_id=course.course_org.id,
        #                                    fav_type=2):
        #         has_fav_org = True

        tag = course.tag
        # If there is tag
        if tag:
            related_courses = Course.objects.filter(tag=tag)[:1]
        else:
            # If it is empty, pass an empty array, otherwise it is an empty string, and it will be wrong to traverse in html
            related_courses = []

        has_attended = False
        # First check in the user_course table whether
        # the user is already associated with the course. If not, save an association record.
        if request.user.is_authenticated:
            user_courses = UserCourse.objects.filter(
                user=user,
                course=course
            )
            if user_courses:
                has_attended = True

        print("POINT 1", request.user)
        vid = Video.objects.filter(lesson__course=course)
        course_lessons = Lesson.objects.filter(course=course)
        i = 0
        while True:
            try:
                lessonid = vid.get(id=i)
                break
            except:
                i = i + 1

        firstvid = lessonid
        price = course.price

        # register the course to user if transaction is sucess
        if paytm_params['STATUS'] == "TXN_SUCCESS":
            user_courses = UserCourse.objects.filter(
            user=user,
            course=course
        )
            try:
                Recipient = [request.user.username]
                Message = "you have been Successfully enrolled to the course "+course.name+" you can access the course at www.productivvacademy.com/course/detail/"+str(course.id)+"\n Join our whatsapp community by clicking on this link : "+str(course.teacher_advice)+" If the link dosent work, text us at +91 9176555773"
                sender = 'richardrozario.a@gmail.com'
                Subject = 'Sucess Message'

                send_mail(Subject,Message,sender,Recipient)

                Recipient = ['productivvacademy@gmail.com']
                Message = "Course Name: "+course.name
                sender = 'richardrozario.a@gmail.com'
                Subject = 'New Purchase'

                send_mail(Subject,Message,sender,Recipient)

            except:
                print("MAIL NOT SENT")


            # If no record is found,
            # it means that the user has not started learning, then save a record and let the number of students plus one
            if not user_courses:
                user_course = UserCourse(user=user, course=course)
                user_course.save()
                # Number of students plus one
                course.students += 1
                course.save()

            msg = "Payment success, Happy Learning!"
            return render(request, 'congrats.html', {
            'course': course,
            'related_courses': related_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
            'has_attended': has_attended,
            'firstvid': firstvid,
            'course_lessons': course_lessons,
            'price' : price,
            'msg' : msg,
        })

        else:
            msg = "Payment Failed. Try Again"
            return render(request, 'course-detailtest.html', {
            'course': course,
            'related_courses': related_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
            'has_attended': has_attended,
            'firstvid': firstvid,
            'course_lessons': course_lessons,
            'price' : price,
            'msg' : msg,
        })

        # return render(request, 'callback.html', context=received_data)



class CourseListView(View):
    def get(self, request):
        courses = Course.objects.all().order_by("-add_time")
        # Popular courses on the right
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            courses = courses.filter(Q(name__icontains=search_keywords) | Q(
                desc__icontains=search_keywords) | Q(
                detail__icontains=search_keywords))

        # Sort by the number of students and the number of courses
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                courses = courses.order_by("-students")
            elif sort == 'hot':
                courses = courses.order_by("-click_nums")

        # Pagination of course institutions
        # Try to get the page parameter passed by the foreground get request
        # If it is an invalid configuration parameter, the first page is returned by default.
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Take 3 out here, each page shows 3
        p = Paginator(courses, 3, request=request)
        page = p.page(page)

        return render(request, 'course-listtest.html', {
            'courses': page,
            'course':page,
            'hot_courses': hot_courses,
            'sort': sort
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        # Increase clicks
        course.click_nums += 1
        course.save()

        # Judging Favorite
        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id,
                                           fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=course.course_org.id,
                                           fav_type=2):
                has_fav_org = True

        tag = course.tag
        # If there is tag
        if tag:
            related_courses = Course.objects.filter(tag=tag)[:1]
            # ***Problems with the following code*** #
            # all_related_courses = Course.objects.filter(tag=tag)
            # related_courses =[]
            # for course in all_related_courses:
            #     if int(course.id) == int(course_id):
            #         related_courses.append(course)
            # ******************* #
        else:
            # If it is empty, pass an empty array, otherwise it is an empty string, and it will be wrong to traverse in html
            related_courses = []

        has_attended = False
        # First check in the user_course table whether
        # the user is already associated with the course. If not, save an association record.
        if request.user.is_authenticated:
            user_courses = UserCourse.objects.filter(
                user=request.user,
                course=course
            )
            if user_courses:
                has_attended = True

        vid = Video.objects.filter(lesson__course=course)
        course_lessons = Lesson.objects.filter(course=course)
        
        i = 0
        while True:
            try:
                lessonid = vid.get(id=i)
                break
            except:
                i = i + 1

        firstvid = lessonid
        price = course.price

        return render(request, 'course-detailtest.html', {
            'course': course,
            'related_courses': related_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
            'has_attended': has_attended,
            'firstvid': firstvid,
            'course_lessons': course_lessons,
            'price' : price,
        })


class CourseInfoView(LoginRequiredMixin, View):
    """Course Chapter Information"""

    def get(self, request, course_id):
        # cvid = cles.video_set.all().order_by("name")
        course = Course.objects.get(id=course_id)

        course_resource = CourseResource.objects.filter(course=course)
        # ?
        # course_resource = CourseResource.objects.get(id=course_id)

        # First check in the user_course table whether
        # the user is already associated with the course. If not, save an association record.
        user_courses = UserCourse.objects.filter(
            user=request.user,
            course=course
        )

        # If no record is found,
        # it means that the user has not started learning, then save a record and let the number of students plus one
        # if not user_courses:
        #     user_course = UserCourse(user=request.user, course=course)
        #     user_course.save()
        #     # Number of students plus one
        #     course.students += 1
        #     course.save()

        # First instantiate a user_courses operation class according to the course
        user_courses = UserCourse.objects.filter(course=course)
        # Take all the corresponding users in this instance and put them into user_ids
        user_ids = [user_course.user.id for user_course in user_courses]
        # The __in rule is used to indicate that as long as user_id is equal to any one of the user_ids array,
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # Take all courses ID
        course_ids = [user_course.course.id for user_course in
                      all_user_courses]
        # Get other courses
        related_courses = Course.objects.filter(id__in=course_ids).order_by(
            "-click_nums")[:5]
        return render(request, 'course-video.html', {
            'course': course,
            'course_resource': course_resource,
            'user_courses': user_courses,
            'related_courses': related_courses
        })


class CourseCommentsView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course_resource = CourseResource.objects.filter(course=course)
        comments = CourseComments.objects.all()
        return render(request, 'course-comment.html', {
            'course': course,
            'course_resource': course_resource,
            'comments': comments
        })


class AddCommentsView(LoginRequiredMixin, View):
    """Add Course Review"""

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}',
                                content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if int(course_id) > 0 and comments:
            course_comment = CourseComments()
            # get only takes one, if multiple or none are met,
            # an exception occurs, and filter returns an array without throwing
            course = Course.objects.get(id=int(course_id))
            course_comment.course = course
            course_comment.comments = comments
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse('{"status":"success", "msg":"Added Successfully"}',
                                content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"Add Failed"}',
                                content_type='application/json')


# Playing video view
class VideoPlayView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, video_id):
        # id It is the value added by default in the data table.
        video = Video.objects.get(id=int(video_id))
        # Find the corresponding course
        course = video.lesson.course
        # Check if the user has started the lesson
        user_courses = UserCourse.objects.filter(user=request.user,
                                                 course=course)
        # Join the user's curriculum if not yet
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        # Query Course Resources
        all_resources = CourseResource.objects.filter(course=course)
        # Select student relations who have studied this course
        user_courses = UserCourse.objects.filter(course=course)
        # Remove user_id from relationship
        user_ids = [user_course.user_id for user_course in user_courses]
        # For the courses learned by these users, the foreign key will automatically have the id and get the field
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # Remove all course id
        course_ids = [user_course.course_id for user_course in
                      all_user_courses]
        # Get other lessons learned by users who have taken this course
        related_courses = Course.objects.filter(id__in=course_ids).order_by(
            "-click_nums").exclude(id=course.id)[:4]

        vidid = int(video_id)
        cvids = Video.objects.filter(lesson__course=course).order_by('id')

        course_lessons = Lesson.objects.filter(course=course).order_by('id')
        vprv, vnxt = 0, 0

        # previous lesson
        try:
            vidprv = vidid-1
            vprv = cvids.get(id=vidprv)
        except:
            vprv = cvids.get(id=vidid)

        # next lesson
        try:
            vidnxt = vidid+1
            for i in range(500):
                try:
                    vnxt = cvids.get(id=vidnxt)
                    if vnxt != None:
                        break
                except:
                    vidnxt = vidnxt + 1
            vnxt = cvids.get(id=vidnxt)


        except:
            finish = "Finish Course"
            return render(request, "course-playtest.html", {
            "course": course,
            "all_resources": all_resources,
            "related_courses": related_courses,
            "video": video,
            "Next" : vnxt,
            "Previous" : vprv,
            "course_lessons": course_lessons,
            "finish" : finish,
        })


        # Whether to collect courses
        return render(request, "course-playtest.html", {
            "course": course,
            "all_resources": all_resources,
            "related_courses": related_courses,
            "video": video,
            "Next" : vnxt,
            "Previous" : vprv,
            "course_lessons": course_lessons
        })


def certificate(request,course_id):
    course = Course.objects.get(id=course_id)
    user = request.user

    user_course = UserCourse.objects.get(
            user=request.user,
            course=course
        )
    if user_course.certified == True:
        return render(request, 'certificategiven.html')


    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user_course.certified = True
            user_course.save()
            # process the data in form.cleaned_data as required
            Name = form.cleaned_data['Full_Name']
            # font = ImageFont.truetype('arial.ttf',100)

            # # module_dir = os.path.dirname(__file__)
            # # file_path = os.path.join(module_dir, 'Certificate.jpg')
            # file_path = 'static/img/template.jpg'

            # if len(Name) > 11:
            #     x = 600
            # else:
            #     x = 800

            # img = Image.open(file_path)
            # draw = ImageDraw.Draw(img)
            # draw.text(xy=(x,630),text='{}'.format(Name),fill=(0,0,0),font=font)

            # try:
            #     os.remove('static/img/Certificate.jpg')
            # except:
            #     pass

            # imgpath = 'img/Certificate.jpg'
            # print(imgpath)
            # img.save('static/img/Certificate.jpg')


            # mail = EmailMessage("Certificate",
            #   "hey bitch",
            #   settings.EMAIL_HOST_USER,
            #   ['richardrozario2000@gmail.com'])
            # mail.attach_file('main/static/main/images/Certificate.jpg')
            # mail.send()
            # print("SUCESS")

            Recipient = ['productivvacademy@gmail.com']
            Message = "Name : "+Name+"\nCourse Name: "+course.name
            sender = 'richardrozario.a@gmail.com'
            Subject = 'Certificate'

            send_mail(Subject,Message,sender,Recipient)

            return render(request, 'certificate.html',{"name":Name})

    # if a GET (or any other method) we'll create a blank form
    else:
        if user_course.certified == False:
            form = NameForm()
            return render(request, 'certificateform.html', {'form': form,'id':course_id})


