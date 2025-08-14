from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import Employee, Chat, Order
from .helper import *

from datetime import date


@login_required
def index(request):
    return redirect("chat")


def loginView(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        # Get username from email
        try:
            username = Employee.objects.get(email=email).user.username
        except Employee.DoesNotExist:
            return HttpResponse("Invalid username or password.")

        # Check if account is inactive
        if Employee.objects.get(email=email).status == "Inactive":
            return HttpResponse("Your account is inactive.")

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return HttpResponse("Invalid username or password.")

    return render(request, 'login.html')


def logoutView(request):
    logout(request)
    return redirect("login")


@login_required
def chatView(request):
    reply = """I can answer payroll totals for 'this week/month/year/last month', 
custom ranges like 'from YYYY-MM-DD to YYYY-MM-DD', 
and 'customer <name>' for orders."""

    user = Employee.objects.get(user=request.user)
    chats = Chat.objects.filter(user=user)

    if request.method == "POST":
        message = (request.POST.get("message") or "").strip()

        if not message:
            return JsonResponse({"error": "empty message"}, status=400)

        # Add user message to chat
        Chat.objects.create(user=user, message=message, role="user")

        # Parse user intent and handle orders by customer intent
        intent, payload = parse_intent(message)
        now = ist_now()  # IST aware

        if intent == "payroll_range":
            if payload == "this_week":
                start, end = start_of_week_ist(now), now.date()
                payload_str = "This week"
            elif payload == "this_month":
                start, end = month_bounds(now)
                payload_str = "This month"
            elif payload == "last_month":
                start, end = prev_month_bounds(now)
                payload_str = "Last month"
            elif payload == "this_year":
                start, end = date(now.year, 1, 1), now.date()
                payload_str = "This year"

            total = payroll_sum(start, end)
            reply = f"{payload_str}'s total payroll from {start} to {end}: \n\n₹{total:.2f}"

        elif intent == "payroll_custom":
            try:
                start = date.fromisoformat(payload[0])
                end = date.fromisoformat(payload[1])
            except ValueError:
                reply = "Invalid dates. Use `from YYYY-MM-DD to YYYY-MM-DD` format."
            else:
                total = payroll_sum(start, end)
                reply = f"Payroll total from {start} to {end}: ₹{total:.2f}"

        elif intent == "orders_by_customer":
            orders = Order.objects.filter(customer_name__iexact=payload)
            print(orders)
            if orders.exists():
                orders = list(orders.values())
                lines = [
                    f"{r['pid']}: {r['customer_name']} | {r['stage']} | {r['contract_price']}" for r in orders[:10]]
                reply = f"Recent orders from {payload}:\n\n" + "\n".join(lines)
            else:
                reply = f"No orders found for customer: {payload}"

        # Add assistant response to chat
        Chat.objects.create(user=user, message=reply, role="assistant")

        # Get updated chat history
        chats = Chat.objects.filter(user=user)

    return render(request, 'chat.html', {"chats": chats})
