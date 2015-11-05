from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tapas.serializers import TapaSerializer, BarSerializer, ComentarioSerializer, FotoSerializer, ValoracionSerializer
from tapas.models import Tapa, Bar
from rest_framework.views import APIView
from django.http import Http404
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import string
import math 

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# TODO: Solo mostrar lo que esten a una determinada distancia 
class TapasList(APIView):
    
    """
    Muestra un listado de las tapas ordenado por su puntuacion media.
    """
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        
        tapas = Tapa.objects.all().order_by('-puntuacionMedia')
        data = request.GET
        latitudActual=request.GET.get('latitud','')
        longitudActual=request.GET.get('longitud','')
        
        rango=1000
        
        lista_tapas=[]
        latitudActual=float(latitudActual)
        longitudActual=float(longitudActual)
        print latitudActual
        print longitudActual
        
        for tapa in tapas:
        
            longitud=tapa.bar.longitud
            latitud=tapa.bar.latitud
                
            longitud=float(longitud)
            latitud=float(latitud)
        
            metrosLongitudPuntoA= longitud*(10000000/90)
            metrosLatitudPuntoA=latitud*(40000000/360)
        
            metrosLongitudActual= longitudActual*(10000000/90)
            metrosLatitudActual= latitudActual*(40000000/360)
        
            diferenciaLongitudMetros= metrosLongitudPuntoA-metrosLongitudActual
            diferenciaLatitudMetros=metrosLatitudPuntoA-metrosLatitudActual
        
            diferenciaLongitudMetros=diferenciaLongitudMetros*diferenciaLongitudMetros
            diferenciaLatitudMetros=diferenciaLatitudMetros*diferenciaLatitudMetros
        
            sumaMetros=diferenciaLatitudMetros+diferenciaLongitudMetros
        
        
            distancia= math.sqrt(sumaMetros)
        
            print ("distancia: "+ str(distancia))
            print rango
        
            if distancia<rango:
                lista_tapas.append(tapa) 
        
        
        # NOTA ACLARATORIA
        # unicode(request.user) == request.user.username
        # no se puede poner directamente request.user (objeto completo)
        # si se puede poner request.user.* (siendo * cualquier campo de la clase User como el id) 
        
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
            'serializer': TapaSerializer(lista_tapas, many=True).data
        }
        
        return Response(content)


class TapasListBar(APIView):
    
    """
    Muestra un listado de las tapas de un determinado bar.
    """
    
    def get(self, request, id_bar):
        tapas = Tapa.objects.filter(bar=id_bar)
        serializer = TapaSerializer(tapas, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def anyadirBar(request):
    
    """
    Vista que nos permite crear un nuevo bar.
    """
    
    if request.method == 'POST':
        serializer = BarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def anyadirTapa(request):
    
    """
    Vista que nos permite crear una nueva tapa.
    """
    
    if request.method == 'POST':
        serializer = TapaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
def anyadirComentario(request):
    
    """
    Vista que nos permite crear un nuevo comentario.
    """
    
    if request.method == 'POST':
        serializer = ComentarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
   
   
@api_view(['POST'])  
def anyadirFoto(request):
    
    """
    Vista que nos permite crear un nuevo bar.
    """
    
    if request.method == 'POST':
        serializer = FotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

@api_view(['POST']) 
def anyadirValoracion(request):
    
    """
    Vista que nos permite crear un nuevo bar.
    """
    
    if request.method == 'POST':
        serializer = ValoracionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class TapaDetail(APIView):
    
    """
    Muestra los detalles de una tapa.
    """
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_object(self, id_tapa):
        try:
            return Tapa.objects.get(pk=id_tapa)
        except Tapa.DoesNotExist:
            raise Http404

    def get(self, request, id_tapa):
        tapas = self.get_object(id_tapa)
        serializer = TapaSerializer(tapas)
        return Response(serializer.data)
    
              
class BarDetail(APIView):
    
    """
    Devuelve una lista de los bares.
    """
    
    def get_object(self, id_bar):
        try:
            return Bar.objects.get(pk=id_bar)
        except Bar.DoesNotExist:
            raise Http404

    def get(self, request, id_bar):
        bares = self.get_object(id_bar)
        serializer = BarSerializer(bares)
        return Response(serializer.data)              