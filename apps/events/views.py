from django.shortcuts import render
from django.views.generic import View
from events.models import Event
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def test(request):
	return render(request, 'course-listtest.html')


class EventListView(View):
    def get(self, request):
        events = Event.objects.all().order_by("-add_time")

        # Sort by the number of students and the number of courses
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                events = events.order_by("-students")
            elif sort == 'hot':
                events = events.order_by("-click_nums")

        # Pagination of course institutions
        # Try to get the page parameter passed by the foreground get request
        # If it is an invalid configuration parameter, the first page is returned by default.
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Take 3 out here, each page shows 3
        p = Paginator(events, 3, request=request)
        page = p.page(page)

        return render(request, 'eventlist.html', {
            'events': page,
            'events':page,
            'sort': sort
        })



class EventDetailView(View):
    def get(self, request, event_id):
        event = Event.objects.get(id=event_id)
        # Increase clicks
        event.click_nums += 1
        event.save()

        tag = event.tag

        has_attended = False
        # First check in the user_course table whether
        # the user is already associated with the course. If not, save an association record.
        # if request.user.is_authenticated:
        #     user_courses = UserCourse.objects.filter(
        #         user=request.user,
        #         course=course
        #     )
        #     if user_courses:
        #         has_attended = True

        price = event.price

        return render(request, 'eventdetail.html', {
            'course': event,
            'has_attended': has_attended,
            'price' : price,
        })