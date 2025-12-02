from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer

class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=201)
        return Response(serializer.errors, status=400)


class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"]
        )

        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=200)
        return Response({"error": "Invalid credentials"}, status=401)


class LogoutAPI(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out"}, status=200)


class ProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Request
from .serializers import RequestSerializer

class RequestCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class RequestListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_requests = Request.objects.filter(user=request.user)
        serializer = RequestSerializer(user_requests, many=True)
        return Response(serializer.data)


class RequestDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        try:
            req = Request.objects.get(pk=pk)
            if req.user != request.user:
                return None
            return req
        except Request.DoesNotExist:
            return None

    def get(self, request, pk):
        req = self.get_object(request, pk)
        if not req:
            return Response({"error": "Not found"}, status=404)
        serializer = RequestSerializer(req)
        return Response(serializer.data)

    def put(self, request, pk):
        req = self.get_object(request, pk)
        if not req:
            return Response({"error": "Not authorized"}, status=403)

        serializer = RequestSerializer(req, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        req = self.get_object(request, pk)
        if not req:
            return Response({"error": "Not authorized"}, status=403)
        req.delete()
        return Response({"message": "Request deleted"}, status=200)
from .models import Review
from .serializers import ReviewSerializer


class ReviewCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ReviewListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reviews = Review.objects.all().order_by("-created_at")
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class ReviewDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            return review
        except Review.DoesNotExist:
            return None

    def get(self, request, pk):
        review = self.get_object(request, pk)
        if not review:
            return Response({"error": "Not found"}, status=404)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, pk):
        review = self.get_object(request, pk)
        if not review:
            return Response({"error": "Not found"}, status=404)
        if review.user != request.user:
            return Response({"error": "Not authorized"}, status=403)

        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        review = self.get_object(request, pk)
        if not review:
            return Response({"error": "Not found"}, status=404)
        if review.user != request.user:
            return Response({"error": "Not authorized"}, status=403)

        review.delete()
        return Response({"message": "Review deleted"}, status=200)
