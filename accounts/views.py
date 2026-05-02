from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .serializers import SignupSerializer, LoginSerializer, UserSerializer
from .models import CustomUser
from django.contrib import messages


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User created successfully",
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Login successful",
                    "user": UserSerializer(user).data,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)


# Template-based Views for Frontend


class SignupTemplateView(View):
    """Template-based signup view"""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return render(request, "signup.html")

    def post(self, request):
        email = request.POST.get("email")
        name = request.POST.get("name")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "signup.html")

        user = CustomUser.objects.create_user(email=email, password=password, name=name)
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect("dashboard")


class LoginTemplateView(View):
    """Template-based login view"""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return render(request, "login.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid email or password.")
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid email or password.")

        return render(request, "login.html")


class LogoutView(View):
    """Logout view"""

    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully!")
        return redirect("login")
