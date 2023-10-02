from django.shortcuts import render
from django.http import HttpResponse ,  JsonResponse
from django.views.decorators.csrf import csrf_exempt #used to bypass csrf token
from .models import Client, Project,User
import json
import datetime

# Create your views here.
@csrf_exempt
def get_client(request):
    c=Client.objects.all()
    print(c)
    context={}
    #context['clients']=c
    i=0
    for x in c:
        context[i]={
            'id':x.id,
            'client_name':x.client_name,
            'created_by':x.uid.first_name
        }
        i+=1
        
    # res = {'success':'response from get client'}
    json_data = json.dumps(context,default=str)
    return HttpResponse(json_data)

@csrf_exempt
def create_client(request):
    if request.method == 'POST':
        # Use request.POST.get() to safely access 'cname' and 'user_id'
        cname = request.POST.get('cname', None)
        user_id = request.POST.get('user_id', None)

        if cname is not None and user_id is not None:
            # Check if the user with the specified ID exists
            try:
                u = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User with the provided ID does not exist.'}, status=404)

            # Create the client with the provided name and user
            c = Client.objects.create(client_name=cname, uid=u)
            c.save()

            res = {'success': 'Response from post client'}
            return JsonResponse(res)

        else:
            # Handle the case where 'cname' or 'user_id' is missing in the POST data
            error_data = {'error': 'Missing parameters: cname and/or user_id'}
            return JsonResponse(error_data, status=400)
    else:
        # Handle other HTTP methods if needed
        return JsonResponse({'message': 'This view only accepts POST requests.'}, status=405)

@csrf_exempt
def update_client(request, rid):
    if request.method == 'POST':
        try:
            # Attempt to parse the JSON data from the request's body
            data = json.loads(request.body)
            
            # Check if 'cname' is present in the JSON data
            if 'cname' in data:
                ucname = data['cname']
                # Retrieve the client by its ID
                try:
                    client = Client.objects.get(id=rid)
                except Client.DoesNotExist:
                    return JsonResponse({'error': 'Client not found'}, status=404)
                
                # Update the client's name and the 'updated_at' timestamp
                client.client_name = ucname
                client.updated_at = datetime.datetime.now()
                client.save()
                
                return JsonResponse({'success': 'Client updated successfully'})
            else:
                return JsonResponse({'error': 'Missing "cname" field in JSON data'}, status=400)
        except json.JSONDecodeError as e:
            # Handle JSON decoding error
            return JsonResponse({'error': f'Invalid JSON data: {str(e)}'}, status=400)
    else:
        return JsonResponse({'message': 'This view only accepts POST requests.'}, status=405)

@csrf_exempt 
def delete_client(request,rid):
    c=Client.objects.filter(id=rid)
    c.delete()

    res = {'success':'deleted successfully'}
    json_data = json.dumps(res)
    return HttpResponse(json_data)


@csrf_exempt
def create_project_for_client(request, client_id):
    if request.method == 'POST':
        try:
            # Attempt to parse the JSON data from the request's body
            data = json.loads(request.body)
            
            # Check if 'project_name' and 'users' fields are present in the JSON data
            if 'project_name' in data and 'users' in data:
                project_name = data['project_name']
                users = data['users']
                
                # Retrieve the client by its ID
                try:
                    client = Client.objects.get(id=client_id)
                except Client.DoesNotExist:
                    return JsonResponse({'error': 'Client not found'}, status=404)
                
                # Create the project and assign users to it
                project = Project.objects.create(
                    project_name=project_name,
                    client=client,
                )
                for user_info in users:
                    user_id = user_info['id']
                    # You may want to validate user_id or handle cases where the user doesn't exist
                    user = User.objects.get(id=user_id)
                    project.users.add(user)
                
                return JsonResponse({'success': 'Project created successfully'}, status=201)
            else:
                return JsonResponse({'error': 'Missing "project_name" or "users" field(s) in JSON data'}, status=400)
        except json.JSONDecodeError as e:
            # Handle JSON decoding error
            return JsonResponse({'error': f'Invalid JSON data: {str(e)}'}, status=400)
    else:
        return JsonResponse({'message': 'This view only accepts POST requests.'}, status=405)