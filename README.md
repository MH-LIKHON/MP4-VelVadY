source venv/bin/activate

python manage.py runserver



Starting development server at http://127.0.0.1:8000/




https://didactic-parakeet-v945gq97vgj2pgrg-8000.app.github.dev/admin/login/?next=/admin/auth/user/


Question,

Testimornial should i do html or better for mp4?


Note:

1-
Replace those href="{% url '...' %}" with just: html:- href="#"
- 'subscriptions', 'order_history', 'credits'	⚠️ Use href="#" temporarily if not defined 


2-
For now: search box links to /services/?q=...
You already confirmed this part works visually
We will come back and:
Build the Service model
Build the services view
Load dynamic services from the database


3- Replace this in home html now has href #
<a href="{% url 'service_detail' 1 %}" class="btn btn-dark mt-auto">View</a>
<a href="{% url 'service_detail' 2 %}" class="btn btn-dark mt-auto">View</a>
<a href="{% url 'service_detail' 3 %}" class="btn btn-dark mt-auto">View</a>

4 - database sql or postsql