from django.http import HttpRequest, JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.http import require_http_methods
from django.db import models
import json

class CRUDModel(models.Model):
    class Meta:
        abstract = True

    id = models.AutoField(primary_key=True)
    __accessible_fields : list[str] = []

    __mesg_notfound = "Object not found."
    __mesg_nogetid = "Missing object ID."
    __mesg_noquery = "No valid query parameters found."

    @classmethod
    @require_http_methods("POST")
    def api_create(cls, request : HttpRequest):
        body = json.loads(request.body)

        obj = cls()

        for field in cls.api_Fields:
            try:
                setattr(obj,field,body[field])
            except KeyError:
                pass # Ignore fields that don't exist

        obj.save()

        return JsonResponse({"status":"success","data":model_to_dict(obj)},status=200)

    @classmethod
    @require_http_methods(["GET"])
    def api_read(cls, request : HttpRequest):
        if request.GET.get("id") is not None:
            id = request.GET.get("id")

            try:
                obj = cls.objects.get(pk=id)
                return JsonResponse({"status": "success", "data": model_to_dict(obj)},status=200)
            except cls.DoesNotExist:
                return JsonResponse({"status": "error", "message": cls.__mesg_notfound},status=404)
        else:
            return JsonResponse({"status": "error", "message": cls.__mesg_nogetid},status=400)
        
    @classmethod
    @require_http_methods(["GET"])
    def api_search(cls, request : HttpRequest):
        u_query : dict = request.GET.dict()

        query = {}
        for qk in u_query.keys():
            if qk in cls.api_Fields:
                # If a query field is in the allowed list, rename it's key to match the query format
                query[f"{qk}__icontains"] = u_query[qk]

        if len(query) == 0:
            return JsonResponse({"status": "error", "message": cls.__mesg_noquery}, status=400)

        query_result = cls.objects.filter(**query)

        objects = [model_to_dict(p) for p in query_result]

        return JsonResponse({"status": "success", "data": objects},status=200)
    
    @classmethod
    @require_http_methods(["POST"])
    def api_update(cls, request : HttpRequest):
        body = json.loads(request.body)

        try:
            id = body["id"]
        except KeyError:
            return JsonResponse({"status":"error","message":cls.__mesg_nogetid},status=400)
        
        try:
            obj = cls.objects.get(id=id)
        except cls.DoesNotExist:
            return JsonResponse({"status":"error","message":cls.__mesg_notfound},status=404)

        for field in cls.__accessible_fields:
            try:
                setattr(obj,field,body[field])
            except KeyError:
                pass # Ignore fields that don't exist

        obj.save()
        
        return JsonResponse({"status":"success","data":model_to_dict(obj)},status=200)
    
    @classmethod
    @require_http_methods(["DELETE"])
    def api_delete(cls, request : HttpRequest):
        if request.GET.get("id") is not None:
            id = request.GET.get("id")

            try:
                obj = cls.objects.get(pk=id)
                obj.delete()
            except cls.DoesNotExist:
                return JsonResponse({"status":"error","message":cls.__mesg_notfound},status=404)

            return JsonResponse({"status":"success"},status=200)

        else:
            return JsonResponse({"status": "error", "message": cls.__mesg_nogetid},status=400)