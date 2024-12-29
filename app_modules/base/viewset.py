from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

class BaseViewSet(viewsets.ModelViewSet):
    
    model_class = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        context["user"] = self.request.user
        return context
    
    def get_queryset(self):
        qs = self.model_class.objects.all()
        filters = self.get_dynamic_filters()
        return qs.filter(filters)

    def get_dynamic_filters(self):
        return {}
    
    def create(self, request, entity_name, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": f"{entity_name} Created Successfully..."}, status=status.HTTP_201_CREATED)
    
    def update(self, request,entity_name, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": f"{entity_name} Updated Successfully..."})
    
    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object()) 
        return Response({"message": "Deleted Successfully..."},status=status.HTTP_200_OK)

    def handle_not_found(self, entity_name):
        return Response({"error": f"{entity_name} Does Not Exist..."}, status=status.HTTP_404_NOT_FOUND)