# AnyLearn Labs 🎓

**Self-paced learning platform built with Django**

A beautiful, modern SaaS platform for online courses and educational content. Features a blog, course catalog, and payment integration for paid courses.

![AnyLearn Labs](https://img.shields.io/badge/Django-5.0.1-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **🎨 Beautiful Dark Theme**: Elegant design with gold accents inspired by Claude Design
- **📚 Course Management**: Create and manage self-paced courses with lessons
- **✍️ Blog System**: Share essays and articles about learning
- **💳 Payment Integration**: Stripe integration for paid courses
- **👥 User Enrollment**: Track student progress through courses
- **📧 Newsletter**: Email subscription system
- **🔐 Admin Interface**: Django admin for content management
- **📱 Responsive Design**: Works perfectly on all devices

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone or download the repository**

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Create environment file**
```bash
copy .env.example .env
```
Edit `.env` and add your settings (SECRET_KEY, Stripe keys, etc.)

6. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create a superuser**
```bash
python manage.py createsuperuser
```

8. **Run the development server**
```bash
python manage.py runserver
```

9. **Access the site**
- Main site: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
AnyLearn Labs/
├── anylearn_labs/          # Main project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI configuration
├── blog/                   # Blog application
│   ├── models.py          # Blog post models
│   ├── views.py           # Blog views
│   ├── admin.py           # Blog admin
│   └── urls.py            # Blog URLs
├── courses/                # Courses application
│   ├── models.py          # Course, Lesson, Enrollment models
│   ├── views.py           # Course views
│   ├── admin.py           # Course admin
│   └── urls.py            # Course URLs
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── home.html          # Landing page
│   ├── courses/           # Course templates
│   └── blog/              # Blog templates
├── static/                 # Static files
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── images/            # Images
├── design/                 # Original design files
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables example
└── README.md              # This file
```

## 🎨 Design System

The design is based on a beautiful dark theme with warm accent colors:

- **Background**: Deep brown (#14110d)
- **Text**: Warm cream (#fff3e4)
- **Accent**: Golden (#facb8d)
- **Font**: Lora (serif) for elegance

## 📚 Adding Content

### Create Courses

1. Log in to the admin panel: http://127.0.0.1:8000/admin/
2. Go to "Courses" → "Add Course"
3. Fill in course details:
   - Title, description
   - Difficulty level (Beginner/Intermediate/Advanced)
   - Lesson count and estimated hours
   - Price (or mark as free)
   - Upload thumbnail (optional)
4. Add lessons to your course
5. Mark as "Published" when ready

### Create Blog Posts

1. Go to "Blog Posts" → "Add Blog Post"
2. Fill in post details:
   - Title and content
   - Excerpt for listings
   - Estimated read time
   - Publication date
3. Mark as "Published" when ready

## 💳 Payment Integration

The platform includes Stripe integration structure for paid courses:

1. Sign up for Stripe: https://stripe.com/
2. Get your API keys from Stripe Dashboard
3. Add keys to `.env` file:
   ```
   STRIPE_PUBLIC_KEY=pk_test_your_key
   STRIPE_SECRET_KEY=sk_test_your_key
   ```

## 🔧 Configuration

### Database

By default, the project uses SQLite. To use PostgreSQL or MySQL:

1. Install database driver:
```bash
pip install psycopg2-binary  # PostgreSQL
# or
pip install mysqlclient      # MySQL
```

2. Update `DATABASES` in `settings.py`

### Static Files

For production, collect static files:
```bash
python manage.py collectstatic
```

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG = False` in settings
- [ ] Update `ALLOWED_HOSTS`
- [ ] Use a strong `SECRET_KEY`
- [ ] Set up proper database (PostgreSQL/MySQL)
- [ ] Configure static files with WhiteNoise or CDN
- [ ] Set up media file storage (AWS S3, etc.)
- [ ] Configure email backend for newsletters
- [ ] Set up SSL certificate (HTTPS)
- [ ] Add Stripe webhook handlers

### Deployment Platforms

The project can be deployed to:
- **Heroku** (easy deployment)
- **Railway** (modern platform)
- **DigitalOcean** (flexible)
- **AWS** (scalable)
- **PythonAnywhere** (beginner-friendly)

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📧 Support

For questions or support, please open an issue on GitHub or contact support.

## 🎯 Roadmap

- [ ] User authentication and profiles
- [ ] Course completion certificates
- [ ] Video lesson support
- [ ] Quiz and assessment system
- [ ] Discussion forums
- [ ] Mobile app
- [ ] Advanced analytics

## 🙏 Acknowledgments

- Design inspired by Claude Design System
- Built with Django and Python
- Icons from SVG

---

**Built with ❤️ using Django and Claude Code**

*Start your learning journey today!*
# AnyLearn-Labs-Site
