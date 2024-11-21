from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, get_object_or_404
from .models import Deployment
from .tasks import deploy_to_vps
from django.contrib import messages

# Create your views here.

@staff_member_required
def trigger_deployment(request, deployment_id):
    deployment = get_object_or_404(Deployment, id=deployment_id)
    deploy_to_vps(deployment_id)
    messages.success(request, 'Deployment process started')
    return redirect('admin:deploy_deployment_changelist')
