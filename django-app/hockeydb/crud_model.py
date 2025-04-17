from django.http import HttpRequest, JsonResponse, HttpResponseNotAllowed
from django.forms.models import model_to_dict
from django.utils.log import log_response
from django.db import models
import json
from warnings import warn
from hockeydb.build_mode import BuildMode

class CRUDModel(models.Model):
    class Meta:
        abstract = True

    id = models.AutoField(primary_key=True)

    """
    While I would have liked to dunder the following fields, it screws up inheritance so I can't.
    """
    _accessible_fields : list[str] = []

    _mesg_notfound = "Object not found."
    _mesg_nogetid = "Missing object ID."
    _mesg_noquery = "No valid query parameters found."

    def __require_methods(methods : list[str]):
        """
        Check if a class function is being passed the correct HTTP method.
        Django implements a similar functionaity, but it expects the request to be the first argument, which doesn't work on classmethods.
        This also steals a bit of code from Django's implementation.
        """
        def __inner_decorator(func : callable):
            def __wrapper(cls, request : HttpRequest, *args, **kwargs):
                if request.method not in methods:
                    response = HttpResponseNotAllowed(methods)
                    log_response(
                            "Method Not Allowed (%s): %s",
                            request.method,
                            request.path,
                            response=response,
                            request=request,
                    )
                    return response
                else:
                    return func(cls, request, *args, **kwargs)
            return __wrapper
        return __inner_decorator
    
    def __exception_handler(func : callable):
        """
        Magically handle exceptions so we don't have to think about them.
        If in DEV mode, just do nothing and let django's handler do it for us.
        If in PROD mode, return a message explaining that an exception occured, but don't give too many details for security.
        """
        if BuildMode.is_prod:
            def handled_method(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    return JsonResponse({"status":"error", "message": f"A {type(e).__name__} type exception occured."},status=500)
            return handled_method
        else:
            return func       

    @classmethod
    @__exception_handler
    @__require_methods(["POST"])
    def api_create(cls, request : HttpRequest):
        body = json.loads(request.body)

        obj = cls()

        for field in cls._accessible_fields:
            try:
                setattr(obj,field,body[field])
            except KeyError:
                pass # Ignore fields that don't exist

        obj.save()

        return JsonResponse({"status":"success","data":model_to_dict(obj)},status=200)

    @classmethod
    @__exception_handler
    @__require_methods(["GET"])
    def api_read(cls, request : HttpRequest):
        if request.GET.get("id") is not None:
            id = request.GET.get("id")

            try:
                obj = cls.objects.get(pk=id)
                return JsonResponse({"status": "success", "data": model_to_dict(obj)},status=200)
            except cls.DoesNotExist:
                return JsonResponse({"status": "error", "message": cls._mesg_notfound},status=404)
        else:
            return JsonResponse({"status": "error", "message": cls._mesg_nogetid},status=400)
        
    @classmethod
    @__exception_handler
    @__require_methods(["GET"])
    def api_search(cls, request : HttpRequest):
        u_query : dict = request.GET.dict()

        query = {}
        for qk in u_query.keys():
            if qk in cls._accessible_fields:
                # If a query field is in the allowed list, rename it's key to match the query format
                query[f"{qk}__icontains"] = u_query[qk]

        if len(query) == 0:
            return JsonResponse({"status": "error", "message": cls._mesg_noquery}, status=400)

        query_result = cls.objects.filter(**query)

        objects = [model_to_dict(p) for p in query_result]

        return JsonResponse({"status": "success", "data": objects},status=200)
    
    @classmethod
    @__exception_handler
    @__require_methods(["POST"])
    def api_update(cls, request : HttpRequest):
        body = json.loads(request.body)

        try:
            id = body["id"]
        except KeyError:
            return JsonResponse({"status":"error","message":cls._mesg_nogetid},status=400)
        
        try:
            obj = cls.objects.get(id=id)
        except cls.DoesNotExist:
            return JsonResponse({"status":"error","message":cls._mesg_notfound},status=404)

        for field in cls._accessible_fields:
            try:
                setattr(obj,field,body[field])
            except KeyError:
                pass # Ignore fields that don't exist

        obj.save()
        
        return JsonResponse({"status":"success","data":model_to_dict(obj)},status=200)
    
    @classmethod
    @__exception_handler
    @__require_methods(["DELETE"])
    def api_delete(cls, request : HttpRequest):
        if request.GET.get("id") is not None:
            id = request.GET.get("id")

            try:
                obj = cls.objects.get(pk=id)
                obj.delete()
            except cls.DoesNotExist:
                return JsonResponse({"status":"error","message":cls._mesg_notfound},status=404)

            return JsonResponse({"status":"success"},status=200)

        else:
            return JsonResponse({"status": "error", "message": cls._mesg_nogetid},status=400)