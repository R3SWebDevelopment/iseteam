from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext


from iseteam.trips.decorators import login_required_staff


@login_required_staff(login_url='/login/')
@login_required(login_url='/login/')
def admin_all_staff(request):
    staff = User.objects.filter(is_staff=True, is_active=True)
    return render_to_response('admin/staff/all_staff.html',
                              {'staff': staff},
                              context_instance=RequestContext(request))
